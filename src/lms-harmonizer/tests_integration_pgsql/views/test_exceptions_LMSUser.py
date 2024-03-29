# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from tests_integration_pgsql.pgsql_loader import (
    insert_lms_user,
    insert_lms_user_deleted,
    insert_edfi_student,
)
from tests_integration_pgsql.pgsql_connection import PgsqlConnection, query
from tests_integration_pgsql.pgsql_server_config import PgsqlServerConfig
from tests_integration_pgsql.pgsql_orchestrator import run_harmonizer


SOURCE_SYSTEM = "Canvas"


def describe_when_lms_and_ods_tables_are_both_empty():
    def it_should_return_no_exceptions(test_db_config: PgsqlServerConfig):
        # act
        run_harmonizer(test_db_config)

        # Assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            exceptions = query(
                connection, "select sourcesystemidentifier from lmsx.exceptions_lmsuser"
            )

            assert len(exceptions) == 0


def describe_when_lms_and_ods_tables_have_no_matches():
    SIS_ID_1 = "v+sis_id_1_a"
    SIS_ID_2 = "v+sis_id_1_b"

    def it_should_return_exceptions(test_db_config: PgsqlServerConfig):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            insert_lms_user(connection, SIS_ID_1, "v+e1@e.com", SOURCE_SYSTEM)
            insert_lms_user(connection, SIS_ID_2, "v+e2@e.com", SOURCE_SYSTEM)
            insert_edfi_student(connection, "v+not_matching_sis_id_1")
            insert_edfi_student(connection, "v+not_matching_sis_id_2")

        # act
        run_harmonizer(test_db_config)

        # assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            exceptions = query(
                connection, f"select sourcesystemidentifier from lmsx.exceptions_lmsuser where sourcesystemidentifier in ('{SIS_ID_1}', '{SIS_ID_2}')"
            )

            assert len(exceptions) == 2
            assert exceptions[0]["sourcesystemidentifier"] == SIS_ID_1
            assert exceptions[1]["sourcesystemidentifier"] == SIS_ID_2


def describe_when_lms_and_ods_tables_have_a_match():
    STUDENT_ID = "10000000-0000-0000-0000-000000000001"
    SIS_ID = "v+sis_id_1"
    UNIQUE_ID = f"{SIS_ID}1"

    def it_should_return_no_exceptions(test_db_config: PgsqlServerConfig):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            insert_lms_user(connection, SIS_ID, "v+e1_1@e.com", SOURCE_SYSTEM)
            insert_edfi_student(connection, UNIQUE_ID, STUDENT_ID)

        # act
        run_harmonizer(test_db_config)

        # assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            exceptions = query(
                connection, f"select sourcesystemidentifier from lmsx.exceptions_lmsuser where sourcesystemidentifier = '{SIS_ID}'"
            )

            assert len(exceptions) == 0


def describe_when_lms_and_ods_tables_have_a_match_to_deleted_record():
    STUDENT_ID = "10000000-0000-0000-0000-000000000002"
    SIS_ID = "v+sis_id_2"
    UNIQUE_ID = f"{SIS_ID}1"

    def it_should_return_no_exceptions(test_db_config: PgsqlServerConfig):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            insert_lms_user_deleted(connection, SIS_ID, "v+e1_2@e.com", SOURCE_SYSTEM)
            insert_edfi_student(connection, UNIQUE_ID, STUDENT_ID)

        # act
        run_harmonizer(test_db_config)

        # assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            exceptions = query(
                connection, f"select sourcesystemidentifier from lmsx.exceptions_lmsuser where sourcesystemidentifier = '{SIS_ID}'"
            )

            assert len(exceptions) == 0


def describe_when_lms_and_ods_tables_have_one_match_and_one_not_match():
    STUDENT_ID = "10000000-0000-0000-0000-000000000003"
    SIS_ID = "v+sis_id_3"
    UNIQUE_ID = f"{SIS_ID}1"
    NOT_MATCHING_SIS_ID = "v+not_matching_sis_id"

    def it_should_return_one_exception(test_db_config: PgsqlServerConfig):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            insert_lms_user(connection, SIS_ID, "v+e1_3@e.com", SOURCE_SYSTEM)
            insert_edfi_student(connection, UNIQUE_ID, STUDENT_ID)

            insert_lms_user(connection, NOT_MATCHING_SIS_ID, "v+e2_3@e.com", SOURCE_SYSTEM)
            insert_edfi_student(connection, "v+also_not_matching_unique_id")

        # act
        run_harmonizer(test_db_config)

        # assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            exceptions = query(
                connection, f"select sourcesystemidentifier from lmsx.exceptions_lmsuser where sourcesystemidentifier = '{NOT_MATCHING_SIS_ID}'"
            )

            assert len(exceptions) == 1
            assert exceptions[0]["sourcesystemidentifier"] == NOT_MATCHING_SIS_ID
