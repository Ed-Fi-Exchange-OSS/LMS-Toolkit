# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
from tests_integration_pgsql.pgsql_loader import (
    insert_edfi_section_association,
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
from tests_integration_pgsql.pgsql_connection import PgsqlConnection, query
from tests_integration_pgsql.pgsql_server_config import PgsqlServerConfig
from tests_integration_pgsql.pgsql_orchestrator import run_harmonizer
from edfi_lms_harmonizer.helpers.constants import SOURCE_SYSTEM


SOURCE_SYSTEMS = [SOURCE_SYSTEM.CANVAS, SOURCE_SYSTEM.GOOGLE, SOURCE_SYSTEM.SCHOOLOGY]
USER_TEST_EMAIL = "test@email.email"


def descriptor_namespace_for(source_system: str) -> str:
    return f"uri://ed-fi.org/edfilms/AssignmentCategoryDescriptor/{source_system}"


def submission_descriptor_namespace_for(source_system: str) -> str:
    return f"uri://ed-fi.org/edfilms/SubmissionStatusDescriptor/{source_system}"


def describe_when_lms_and_ods_tables_are_both_empty():
    def it_should_run_successfully(test_db_config: PgsqlServerConfig):
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
        test_db_config: PgsqlServerConfig, source_system: str
    ):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:

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
                """update lms.lmssection set
                    edfisectionid = (select id from edfi.section limit 1)"""
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
                """update lms.lmsuser set
                    edfistudentid = (select id from edfi.student limit 1)"""
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
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSAssignmentSubmission = query(
                connection, "select * from lmsx.assignmentsubmission"
            )

            assert len(LMSAssignmentSubmission) == 1
            assert (
                LMSAssignmentSubmission[0]["assignmentsubmissionidentifier"]
                == SUBMISSION_TEST_IDENTIFIER
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

    def it_should_not_insert_the_submissions(test_db_config: PgsqlServerConfig):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:

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
                """update lms.lmssection set
                    edfisectionid = (select id from edfi.section limit 1)"""
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
                """update lms.lmsuser set
                    edfistudentid = (select id from edfi.student limit 1)"""
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
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSAssignmentSubmission = query(
                connection, "select * from lmsx.assignmentsubmission"
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
        test_db_config: PgsqlServerConfig, source_system: str
    ):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:

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
                """update lms.lmssection set
                    edfisectionid = (select id from edfi.section limit 1)"""
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
                """update lms.lmsuser set
                    edfistudentid = (select id from edfi.student limit 1)"""
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
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            connection.execute(
                f"""
                update lms.assignmentsubmission set
                    grade='{SUBMISSION_GRADE}',
                    lastmodifieddate=now()"""
            )  # In the first insert it is set to 0

        # act
        run_harmonizer(test_db_config)

        # assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSAssignmentSubmission = query(
                connection, "select * from lmsx.assignmentsubmission"
            )

            assert LMSAssignmentSubmission[0]["grade"] == SUBMISSION_GRADE


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
        test_db_config: PgsqlServerConfig, source_system: str
    ):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:

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
                """update lms.lmssection set
                    edfisectionid = (select id from edfi.section limit 1)"""
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
                """update lms.lmsuser set
                    edfistudentid = (select id from edfi.student limit 1)"""
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
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSAssignmentSubmission = query(
                connection, "select * from lmsx.assignmentsubmission"
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
        test_db_config: PgsqlServerConfig, source_system: str
    ):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:

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
                """update lms.lmssection set
                    edfisectionid = (select id from edfi.section limit 1)"""
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
                """update lms.lmsuser set
                    edfistudentid = (select id from edfi.student limit 1)"""
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
            connection.execute("update lms.assignment set deletedat = now()")

        # act
        run_harmonizer(test_db_config)

        # assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSAssignmentSubmission = query(
                connection, "select * from lmsx.assignmentsubmission"
            )

            assert len(LMSAssignmentSubmission) == 0


def describe_when_there_are_past_assignments_without_submissions():
    ASSIGNMENT_CATEGORY = "test_category"
    SIS_SECTION_ID = "sis_section_id"
    ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER = "assignment_identifier"
    ASSIGNMENT_SUBMISSION_STATUS_MISSING = "missing"  # the stored procedure looks for a descriptor with codevalue = missing
    ASSIGNMENT_SUBMISSION_STATUS_UPCOMING = "Upcoming"  # the stored procedure also needs a descriptor with codevalue = Upcoming
    USER_SIS_ID = "test_sis_id"

    @pytest.mark.parametrize("source_system", SOURCE_SYSTEMS)
    def it_should_create_missing_submissions_for_associated_students(
            test_db_config: PgsqlServerConfig, source_system: str):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:

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
                ASSIGNMENT_SUBMISSION_STATUS_MISSING,
            )
            insert_lmsx_assignmentsubmissionstatus_descriptor(connection, 3)

            insert_descriptor(
                connection,
                submission_descriptor_namespace_for(source_system),
                ASSIGNMENT_SUBMISSION_STATUS_UPCOMING,
            )
            insert_lmsx_assignmentsubmissionstatus_descriptor(connection, 4)

            insert_lms_section(connection, SIS_SECTION_ID, source_system)
            insert_edfi_section(connection, SIS_SECTION_ID)
            connection.execute(
                """update lms.lmssection set
                    edfisectionid = (select id from edfi.section limit 1)"""
            )

            insert_lms_assignment(
                connection,
                ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER,
                source_system,
                1,
                ASSIGNMENT_CATEGORY,
                past_due_date=True
            )

            insert_lms_user(connection, USER_SIS_ID, USER_TEST_EMAIL, source_system)
            insert_edfi_student(connection, USER_SIS_ID)
            connection.execute(
                """update lms.lmsuser set
                    edfistudentid = (select id from edfi.student limit 1)"""
            )
            insert_edfi_section_association(
                connection,
                SIS_SECTION_ID,
                USER_SIS_ID
            )

        # act
        run_harmonizer(test_db_config)

        # assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSAssignmentSubmission = query(
                connection, "select * from lmsx.assignmentsubmission"
            )
            # We are only interested in creating missing submissions for Schoology
            if (source_system == SOURCE_SYSTEM.SCHOOLOGY):
                assert len(LMSAssignmentSubmission) == 1
            else:
                assert len(LMSAssignmentSubmission) == 0


def describe_when_there_are_future_assignments_without_submissions():
    ASSIGNMENT_CATEGORY = "test_category"
    SIS_SECTION_ID = "sis_section_id"
    ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER = "assignment_identifier"
    ASSIGNMENT_SUBMISSION_STATUS_MISSING = "missing"  # the stored procedure looks for a descriptor with codevalue = missing
    ASSIGNMENT_SUBMISSION_STATUS_UPCOMING = "Upcoming"  # the stored procedure also needs a descriptor with codevalue = Upcoming
    USER_SIS_ID = "test_sis_id"

    @pytest.mark.parametrize("source_system", SOURCE_SYSTEMS)
    def it_should_create_missing_submissions_for_associated_students(
            test_db_config: PgsqlServerConfig, source_system: str):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:

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
                ASSIGNMENT_SUBMISSION_STATUS_MISSING,
            )
            insert_lmsx_assignmentsubmissionstatus_descriptor(connection, 3)

            insert_descriptor(
                connection,
                submission_descriptor_namespace_for(source_system),
                ASSIGNMENT_SUBMISSION_STATUS_UPCOMING,
            )
            insert_lmsx_assignmentsubmissionstatus_descriptor(connection, 4)

            insert_lms_section(connection, SIS_SECTION_ID, source_system)
            insert_edfi_section(connection, SIS_SECTION_ID)
            connection.execute(
                """update lms.lmssection set
                    edfisectionid = (select id from edfi.section limit 1)"""
            )

            insert_lms_assignment(
                connection,
                ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER,
                source_system,
                1,
                ASSIGNMENT_CATEGORY
            )

            insert_lms_user(connection, USER_SIS_ID, USER_TEST_EMAIL, source_system)
            insert_edfi_student(connection, USER_SIS_ID)
            connection.execute(
                """update lms.lmsuser set
                    edfistudentid = (select id from edfi.student limit 1)"""
            )
            insert_edfi_section_association(
                connection,
                SIS_SECTION_ID,
                USER_SIS_ID
            )

        # act
        run_harmonizer(test_db_config)

        # assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSAssignmentSubmission = query(
                connection, "select * from lmsx.assignmentsubmission"
            )
            # We are only creating records for Schoology
            if (source_system == SOURCE_SYSTEM.SCHOOLOGY):
                assert len(LMSAssignmentSubmission) == 1
            else:
                assert len(LMSAssignmentSubmission) == 0
