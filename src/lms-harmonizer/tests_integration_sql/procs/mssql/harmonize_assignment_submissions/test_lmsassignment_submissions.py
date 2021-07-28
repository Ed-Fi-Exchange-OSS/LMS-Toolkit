# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
from tests_integration_sql.mssql_loader import (
    insert_edfi_student,
    insert_lms_assignment,
    insert_lms_section,
    insert_edfi_section,
    insert_descriptor,
    insert_lmsx_sourcesystem_descriptor,
    insert_lmsx_assignmentcategory_descriptor,
    insert_lms_assignment_submissions,
    insert_lms_user,
    insert_lmsx_assignmentsubmissionstatus_descriptor,
)
from tests_integration_sql.mssql_connection import MSSqlConnection, query
from tests_integration_sql.server_config import ServerConfig
from tests_integration_sql.orchestrator import run_harmonizer
from edfi_lms_harmonizer.helpers.constants import SOURCE_SYSTEM


SOURCE_SYSTEMS = [SOURCE_SYSTEM.CANVAS, SOURCE_SYSTEM.GOOGLE, SOURCE_SYSTEM.SCHOOLOGY]
USER_TEST_EMAIL = "test@email.email"


def descriptor_namespace_for(source_system: str) -> str:
    return f"uri://ed-fi.org/edfilms/AssignmentCategoryDescriptor/{source_system}"


def submission_descriptor_namespace_for(source_system: str) -> str:
    return f"uri://ed-fi.org/edfilms/SubmissionStatusDescriptor/{source_system}"


def describe_when_lms_and_ods_tables_are_both_empty():
    def it_should_run_successfully(test_db_config: ServerConfig):
        # act
        run_harmonizer(test_db_config)
        # assert - no errors


def describe_when_there_are_assignment_submissions_to_insert():
    SIS_SECTION_ID = "sis_section_id"
    ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER = "assignment_identifier"
    ASSIGNMENT_CATEGORY = "test_category"
    ASSIGNMENT_SUBMISSION_STATUS = "test_submission_status"
    USER_SIS_ID = "test_sis_id"
    SUBMISSION_TEST_IDENTIFIER = "submission_test_identifier"
    SUBMISSION_TEST_LMS_IDENTIFIER = 99

    @pytest.mark.parametrize("source_system", SOURCE_SYSTEMS)
    def it_should_insert_the_submissions_successfully(
        test_db_config: ServerConfig, source_system: str
    ):
        # arrange
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:

            insert_descriptor(
                connection, descriptor_namespace_for(source_system), ASSIGNMENT_CATEGORY
            )
            insert_lmsx_assignmentcategory_descriptor(connection, 1)

            insert_descriptor(
                connection, descriptor_namespace_for(source_system), source_system
            )
            insert_lmsx_sourcesystem_descriptor(connection, 2)

            insert_descriptor(
                connection,
                submission_descriptor_namespace_for(source_system),
                ASSIGNMENT_SUBMISSION_STATUS,
            )
            insert_lmsx_assignmentsubmissionstatus_descriptor(connection, 3)

            insert_lms_section(connection, SIS_SECTION_ID, source_system)
            insert_edfi_section(connection, SIS_SECTION_ID)
            connection.execute(
                """UPDATE LMS.LMSSECTION SET
                    EdFiSectionId = (SELECT TOP 1 ID FROM EDFI.SECTION)"""
            )

            assignment_id = insert_lms_assignment(
                connection,
                ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER,
                source_system,
                1,
                ASSIGNMENT_CATEGORY,
            )

            insert_lms_user(connection, USER_SIS_ID, USER_TEST_EMAIL, source_system)
            insert_edfi_student(connection, USER_SIS_ID)
            connection.execute(
                """UPDATE LMS.LMSUSER SET
                    EdFiStudentId = (SELECT TOP 1 ID FROM EDFI.Student)"""
            )

            insert_lms_assignment_submissions(
                connection,
                SUBMISSION_TEST_LMS_IDENTIFIER,
                SUBMISSION_TEST_IDENTIFIER,
                assignment_id,
                1,
                ASSIGNMENT_SUBMISSION_STATUS,
                source_system,
                False,
            )

        # act
        run_harmonizer(test_db_config)

        # assert
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSAssignmentSubmission = query(
                connection, "SELECT * from [lmsx].[AssignmentSubmission]"
            )

            assert len(LMSAssignmentSubmission) == 1
            assert (
                int(LMSAssignmentSubmission[0]["AssignmentSubmissionIdentifier"])
                == SUBMISSION_TEST_LMS_IDENTIFIER
            )


def describe_when_there_are_assignment_submissions_to_insert_from_an_unknown_source_system():
    SIS_SECTION_ID = "sis_section_id"
    ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER = "assignment_identifier"
    ASSIGNMENT_CATEGORY = "test_category"
    ASSIGNMENT_SUBMISSION_STATUS = "test_submission_status"
    USER_SIS_ID = "test_sis_id"
    SUBMISSION_TEST_IDENTIFIER = "submission_test_identifier"
    SUBMISSION_TEST_LMS_IDENTIFIER = 99
    UNKNOWN_SOURCE_SYSTEM = "Unknown"

    def it_should_not_insert_the_submissions(test_db_config: ServerConfig):
        # arrange
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:

            insert_descriptor(
                connection,
                descriptor_namespace_for(UNKNOWN_SOURCE_SYSTEM),
                ASSIGNMENT_CATEGORY,
            )
            insert_lmsx_assignmentcategory_descriptor(connection, 1)

            insert_descriptor(
                connection,
                descriptor_namespace_for(UNKNOWN_SOURCE_SYSTEM),
                UNKNOWN_SOURCE_SYSTEM,
            )
            insert_lmsx_sourcesystem_descriptor(connection, 2)

            insert_descriptor(
                connection,
                submission_descriptor_namespace_for(UNKNOWN_SOURCE_SYSTEM),
                ASSIGNMENT_SUBMISSION_STATUS,
            )
            insert_lmsx_assignmentsubmissionstatus_descriptor(connection, 3)

            insert_lms_section(connection, SIS_SECTION_ID, UNKNOWN_SOURCE_SYSTEM)
            insert_edfi_section(connection, SIS_SECTION_ID)
            connection.execute(
                """UPDATE LMS.LMSSECTION SET
                    EdFiSectionId = (SELECT TOP 1 ID FROM EDFI.SECTION)"""
            )

            assignment_id = insert_lms_assignment(
                connection,
                ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER,
                UNKNOWN_SOURCE_SYSTEM,
                1,
                ASSIGNMENT_CATEGORY,
            )

            insert_lms_user(
                connection, USER_SIS_ID, USER_TEST_EMAIL, UNKNOWN_SOURCE_SYSTEM
            )
            insert_edfi_student(connection, USER_SIS_ID)
            connection.execute(
                """UPDATE LMS.LMSUSER SET
                    EdFiStudentId = (SELECT TOP 1 ID FROM EDFI.Student)"""
            )

            insert_lms_assignment_submissions(
                connection,
                SUBMISSION_TEST_LMS_IDENTIFIER,
                SUBMISSION_TEST_IDENTIFIER,
                assignment_id,
                1,
                ASSIGNMENT_SUBMISSION_STATUS,
                UNKNOWN_SOURCE_SYSTEM,
                False,
            )

        # act
        run_harmonizer(test_db_config)

        # assert
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSAssignmentSubmission = query(
                connection, "SELECT * from [lmsx].[AssignmentSubmission]"
            )

            assert len(LMSAssignmentSubmission) == 0


def describe_when_there_are_assignment_submissions_to_update():
    SIS_SECTION_ID = "sis_section_id"
    ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER = "assignment_identifier"
    ASSIGNMENT_CATEGORY = "test_category"
    ASSIGNMENT_SUBMISSION_STATUS = "test_submission_status"
    USER_SIS_ID = "test_sis_id"
    SUBMISSION_TEST_IDENTIFIER = "submission_test_identifier"
    SUBMISSION_TEST_LMS_IDENTIFIER = 99
    SUBMISSION_GRADE = "85"

    @pytest.mark.parametrize("source_system", SOURCE_SYSTEMS)
    def it_should_update_the_submissions_successfully(
        test_db_config: ServerConfig, source_system: str
    ):
        # arrange
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:

            insert_descriptor(
                connection, descriptor_namespace_for(source_system), ASSIGNMENT_CATEGORY
            )
            insert_lmsx_assignmentcategory_descriptor(connection, 1)

            insert_descriptor(
                connection, descriptor_namespace_for(source_system), source_system
            )
            insert_lmsx_sourcesystem_descriptor(connection, 2)

            insert_descriptor(
                connection,
                submission_descriptor_namespace_for(source_system),
                ASSIGNMENT_SUBMISSION_STATUS,
            )
            insert_lmsx_assignmentsubmissionstatus_descriptor(connection, 3)

            insert_lms_section(connection, SIS_SECTION_ID, source_system)
            insert_edfi_section(connection, SIS_SECTION_ID)
            connection.execute(
                """UPDATE LMS.LMSSECTION SET
                    EdFiSectionId = (SELECT TOP 1 ID FROM EDFI.SECTION)"""
            )

            assignment_id = insert_lms_assignment(
                connection,
                ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER,
                source_system,
                1,
                ASSIGNMENT_CATEGORY,
            )

            insert_lms_user(connection, USER_SIS_ID, USER_TEST_EMAIL, source_system)
            insert_edfi_student(connection, USER_SIS_ID)
            connection.execute(
                """UPDATE LMS.LMSUSER SET
                    EdFiStudentId = (SELECT TOP 1 ID FROM EDFI.Student)"""
            )

            insert_lms_assignment_submissions(
                connection,
                SUBMISSION_TEST_LMS_IDENTIFIER,
                SUBMISSION_TEST_IDENTIFIER,
                assignment_id,
                1,
                ASSIGNMENT_SUBMISSION_STATUS,
                source_system,
                False,
            )

        run_harmonizer(test_db_config)
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:
            connection.execute(
                f"""
                UPDATE LMS.ASSIGNMENTSUBMISSION SET
                    GRADE=N'{SUBMISSION_GRADE}',
                    LASTMODIFIEDDATE=GETDATE()"""
            )  # In the first insert it is set to 0

        # act
        run_harmonizer(test_db_config)

        # assert
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSAssignmentSubmission = query(
                connection, "SELECT * from [lmsx].[AssignmentSubmission]"
            )

            assert LMSAssignmentSubmission[0]["Grade"] == SUBMISSION_GRADE


def describe_when_there_are_assignment_submissions_for_deleted_assignments():
    SIS_SECTION_ID = "sis_section_id"
    ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER = "assignment_identifier"
    ASSIGNMENT_CATEGORY = "test_category"
    ASSIGNMENT_SUBMISSION_STATUS = "test_submission_status"
    USER_SIS_ID = "test_sis_id"
    SUBMISSION_TEST_IDENTIFIER = "submission_test_identifier"
    SUBMISSION_TEST_LMS_IDENTIFIER = 99

    @pytest.mark.parametrize("source_system", SOURCE_SYSTEMS)
    def it_should_not_insert_the_submissions(
        test_db_config: ServerConfig, source_system: str
    ):
        # arrange
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:

            insert_descriptor(
                connection, descriptor_namespace_for(source_system), ASSIGNMENT_CATEGORY
            )
            insert_lmsx_assignmentcategory_descriptor(connection, 1)

            insert_descriptor(
                connection, descriptor_namespace_for(source_system), source_system
            )
            insert_lmsx_sourcesystem_descriptor(connection, 2)

            insert_descriptor(
                connection,
                submission_descriptor_namespace_for(source_system),
                ASSIGNMENT_SUBMISSION_STATUS,
            )
            insert_lmsx_assignmentsubmissionstatus_descriptor(connection, 3)

            insert_lms_section(connection, SIS_SECTION_ID, source_system)
            insert_edfi_section(connection, SIS_SECTION_ID)
            connection.execute(
                """UPDATE LMS.LMSSECTION SET
                    EdFiSectionId = (SELECT TOP 1 ID FROM EDFI.SECTION)"""
            )

            assignment_id = insert_lms_assignment(
                connection,
                ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER,
                source_system,
                1,
                ASSIGNMENT_CATEGORY,
            )

            insert_lms_user(connection, USER_SIS_ID, USER_TEST_EMAIL, source_system)
            insert_edfi_student(connection, USER_SIS_ID)
            connection.execute(
                """UPDATE LMS.LMSUSER SET
                    EdFiStudentId = (SELECT TOP 1 ID FROM EDFI.Student)"""
            )

            insert_lms_assignment_submissions(
                connection,
                SUBMISSION_TEST_LMS_IDENTIFIER,
                SUBMISSION_TEST_IDENTIFIER,
                assignment_id,
                1,
                ASSIGNMENT_SUBMISSION_STATUS,
                source_system,
                True,  # deleted = True
            )

        # act
        run_harmonizer(test_db_config)

        # assert
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSAssignmentSubmission = query(
                connection, "SELECT * from [lmsx].[AssignmentSubmission]"
            )

            assert len(LMSAssignmentSubmission) == 0


def describe_when_there_are_lmsx_assignment_submissions_and_lms_assignment_is_deleted():
    SIS_SECTION_ID = "sis_section_id"
    ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER = "assignment_identifier"
    ASSIGNMENT_CATEGORY = "test_category"
    ASSIGNMENT_SUBMISSION_STATUS = "test_submission_status"
    USER_SIS_ID = "test_sis_id"
    SUBMISSION_TEST_IDENTIFIER = "submission_test_identifier"
    SUBMISSION_TEST_LMS_IDENTIFIER = 99

    @pytest.mark.parametrize("source_system", SOURCE_SYSTEMS)
    def it_should_not_insert_any_submissions(
        test_db_config: ServerConfig, source_system: str
    ):
        # arrange
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:

            insert_descriptor(
                connection, descriptor_namespace_for(source_system), ASSIGNMENT_CATEGORY
            )
            insert_lmsx_assignmentcategory_descriptor(connection, 1)

            insert_descriptor(
                connection, descriptor_namespace_for(source_system), source_system
            )
            insert_lmsx_sourcesystem_descriptor(connection, 2)

            insert_descriptor(
                connection,
                submission_descriptor_namespace_for(source_system),
                ASSIGNMENT_SUBMISSION_STATUS,
            )
            insert_lmsx_assignmentsubmissionstatus_descriptor(connection, 3)

            insert_lms_section(connection, SIS_SECTION_ID, source_system)
            insert_edfi_section(connection, SIS_SECTION_ID)
            connection.execute(
                """UPDATE LMS.LMSSECTION SET
                    EdFiSectionId = (SELECT TOP 1 ID FROM EDFI.SECTION)"""
            )

            assignment_id = insert_lms_assignment(
                connection,
                ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER,
                source_system,
                1,
                ASSIGNMENT_CATEGORY,
            )

            insert_lms_user(connection, USER_SIS_ID, USER_TEST_EMAIL, source_system)
            insert_edfi_student(connection, USER_SIS_ID)
            connection.execute(
                """UPDATE LMS.LMSUSER SET
                    EdFiStudentId = (SELECT TOP 1 ID FROM EDFI.Student)"""
            )

            insert_lms_assignment_submissions(
                connection,
                SUBMISSION_TEST_LMS_IDENTIFIER,
                SUBMISSION_TEST_IDENTIFIER,
                assignment_id,
                1,
                ASSIGNMENT_SUBMISSION_STATUS,
                source_system,
                False,
            )

            run_harmonizer(test_db_config)
            connection.execute("update lms.assignment set deletedat = GETDATE()")

        # act
        run_harmonizer(test_db_config)

        # assert
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSAssignmentSubmission = query(
                connection, "SELECT * from [lmsx].[AssignmentSubmission]"
            )

            assert len(LMSAssignmentSubmission) == 0
