# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from tests_integration_pgsql.pgsql_loader import (
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


SOURCE_SYSTEM = 'Canvas'
USER_TEST_EMAIL = "test@email.email"
QUERY_FOR_ASSIGNMENT_SUBMISSION_EXCEPTIONS = """
SELECT
    count(*) as count
FROM
    lmsx.assignment_submissions_exceptions
    """


def descriptor_namespace_for(source_system: str) -> str:
    return f"uri://ed-fi.org/edfilms/AssignmentCategoryDescriptor/{source_system}"


def submission_descriptor_namespace_for(source_system: str) -> str:
    return f"uri://ed-fi.org/edfilms/SubmissionStatusDescriptor/{source_system}"


def describe_when_lms_and_ods_tables_are_both_empty():
    def it_should_return_zero(test_db_config: PgsqlServerConfig):
        result = None
        # act
        run_harmonizer(test_db_config)
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            result = query(connection, QUERY_FOR_ASSIGNMENT_SUBMISSION_EXCEPTIONS)

        # assert - no errors
        result[0]['count'] == 0


def describe_when_there_are_submissions_in_ods_and_lms():
    SIS_SECTION_ID = "sis_section_id"
    ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER = "assignment_identifier"
    ASSIGNMENT_CATEGORY = "test_category"
    ASSIGNMENT_SUBMISSION_STATUS = "test_submission_status"
    USER_SIS_ID = "test_sis_id"
    SUBMISSION_TEST_IDENTIFIER = "submission_test_identifier"
    SUBMISSION_TEST_LMS_IDENTIFIER = 99

    def it_should_return_zero(
        test_db_config: PgsqlServerConfig
    ):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:

            insert_descriptor(
                connection, descriptor_namespace_for(SOURCE_SYSTEM), ASSIGNMENT_CATEGORY
            )
            insert_lmsx_assignmentcategory_descriptor(connection, 1)

            insert_descriptor(
                connection, descriptor_namespace_for(SOURCE_SYSTEM), SOURCE_SYSTEM
            )
            insert_lmsx_sourcesystem_descriptor(connection, 2)

            insert_descriptor(
                connection,
                submission_descriptor_namespace_for(SOURCE_SYSTEM),
                ASSIGNMENT_SUBMISSION_STATUS,
            )
            insert_lmsx_assignmentsubmissionstatus_descriptor(connection, 3)

            insert_lms_section(connection, SIS_SECTION_ID, SOURCE_SYSTEM)
            insert_edfi_section(connection, SIS_SECTION_ID)
            connection.execute(
                """update lms.lmssection set
                    edfisectionid = (select id from edfi.section limit 1)"""
            )

            assignment_id = insert_lms_assignment(
                connection,
                ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER,
                SOURCE_SYSTEM,
                1,
                ASSIGNMENT_CATEGORY,
            )

            insert_lms_user(connection, USER_SIS_ID, USER_TEST_EMAIL, SOURCE_SYSTEM)
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
                SOURCE_SYSTEM,
                False,
            )

        # act
        result = None
        run_harmonizer(test_db_config)

        # assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            result = query(connection, QUERY_FOR_ASSIGNMENT_SUBMISSION_EXCEPTIONS)

        result[0]['count'] == 0


def describe_when_there_are_submissions_in_lms_only():
    SIS_SECTION_ID = "sis_section_id"
    ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER = "assignment_identifier"
    ASSIGNMENT_CATEGORY = "test_category"
    ASSIGNMENT_SUBMISSION_STATUS = "test_submission_status"
    USER_SIS_ID = "test_sis_id"
    SUBMISSION_TEST_IDENTIFIER = "submission_test_identifier"
    SUBMISSION_TEST_LMS_IDENTIFIER = 99

    def it_should_return_the_count_of_exceptions_not_in_zero(
        test_db_config: PgsqlServerConfig
    ):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:

            insert_descriptor(
                connection, descriptor_namespace_for(SOURCE_SYSTEM), ASSIGNMENT_CATEGORY
            )
            insert_lmsx_assignmentcategory_descriptor(connection, 1)

            insert_descriptor(
                connection, descriptor_namespace_for(SOURCE_SYSTEM), SOURCE_SYSTEM
            )
            insert_lmsx_sourcesystem_descriptor(connection, 2)

            insert_descriptor(
                connection,
                submission_descriptor_namespace_for(SOURCE_SYSTEM),
                ASSIGNMENT_SUBMISSION_STATUS,
            )
            insert_lmsx_assignmentsubmissionstatus_descriptor(connection, 3)

            insert_lms_section(connection, SIS_SECTION_ID, SOURCE_SYSTEM)
            insert_edfi_section(connection, SIS_SECTION_ID)
            connection.execute(
                """update lms.lmssection set
                    edfisectionid = (select id from edfi.section limit 1)"""
            )

            assignment_id = insert_lms_assignment(
                connection,
                ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER,
                SOURCE_SYSTEM,
                1,
                ASSIGNMENT_CATEGORY,
            )

            insert_lms_user(connection, USER_SIS_ID, USER_TEST_EMAIL, SOURCE_SYSTEM)
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
                SOURCE_SYSTEM,
                False,
            )

        # act
        result = None
        run_harmonizer(test_db_config)
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            connection.execute("delete from lmsx.assignmentsubmission")

        # assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            result = query(connection, QUERY_FOR_ASSIGNMENT_SUBMISSION_EXCEPTIONS)

        result[0]['count'] == 1
