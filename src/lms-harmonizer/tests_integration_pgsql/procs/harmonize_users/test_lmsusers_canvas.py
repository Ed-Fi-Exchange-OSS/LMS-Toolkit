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


def describe_when_harmonizing_canvas_users():
    def describe_given_lms_and_ods_tables_are_both_empty():
        def it_should_run_successfully(test_db_config: PgsqlServerConfig):
            # act
            run_harmonizer(test_db_config)
            # assert - no errors

    def describe_given_lms_and_ods_tables_have_no_matches():
        def it_should_run_successfully(test_db_config: PgsqlServerConfig):
            SIS_ID_1 = "c_sis_id_1"
            SIS_ID_2 = "c_sis_id_2"

            # arrange
            with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
                insert_lms_user(connection, SIS_ID_1, "c_e1@e.com", SOURCE_SYSTEM)
                insert_lms_user(connection, SIS_ID_2, "c_e2@e.com", SOURCE_SYSTEM)
                insert_edfi_student(connection, "c_not_matching_sis_id_1")
                insert_edfi_student(connection, "c_not_matching_sis_id_2")

            # act
            run_harmonizer(test_db_config)

            # assert
            with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
                LMSUser = query(
                    connection,
                    f"select edfistudentid from lms.lmsuser where sourcesystemidentifier in ('{SIS_ID_1}','{SIS_ID_2}')",
                )
                assert len(LMSUser) == 2
                assert LMSUser[0]["edfistudentid"] is None
                assert LMSUser[1]["edfistudentid"] is None

    def describe_given_lms_and_ods_tables_have_a_match():
        STUDENT_ID = "3C000000-0000-0000-0000-000000000000"
        SIS_ID = "c_sis_id_3a"
        UNIQUE_ID = f"{SIS_ID}1"

        def it_should_run_successfully(test_db_config: PgsqlServerConfig):
            # arrange
            with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
                insert_lms_user(connection, SIS_ID, "c_e3a@e.com", SOURCE_SYSTEM)
                insert_edfi_student(connection, UNIQUE_ID, STUDENT_ID)

            # act
            run_harmonizer(test_db_config)

            # assert
            with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
                LMSUser = query(
                    connection,
                    f"select edfistudentid from lms.lmsuser where sourcesystemidentifier='{SIS_ID}'",
                )
                assert len(LMSUser) == 1
                assert LMSUser[0]["edfistudentid"] == STUDENT_ID

    def describe_given_lms_and_ods_tables_have_a_match_to_deleted_record():
        STUDENT_ID = "4C000000-0000-0000-0000-000000000000"
        SIS_ID = "c_sis_id_4"
        UNIQUE_ID = f"{SIS_ID}1"

        def it_should_ignore_the_deleted_record(test_db_config: PgsqlServerConfig):
            # arrange
            with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
                insert_lms_user_deleted(connection, SIS_ID, "c_e4@e.com", SOURCE_SYSTEM)
                insert_edfi_student(connection, UNIQUE_ID, STUDENT_ID)

            # act
            run_harmonizer(test_db_config)

            # assert
            with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
                LMSUser = query(
                    connection,
                    f"select edfistudentid from lms.lmsuser where sourcesystemidentifier='{SIS_ID}'",
                )
                assert len(LMSUser) == 1
                assert LMSUser[0]["edfistudentid"] is None

    def describe_given_lms_and_ods_tables_have_one_match_and_one_not_match():
        STUDENT_ID = "5C000000-0000-0000-0000-000000000000"
        SIS_ID = "c_sis_id_5"
        UNIQUE_ID = f"{SIS_ID}1"
        NOT_MATCHING_SIS_ID = "c_not_matching_sis_id_2"

        def it_should_run_successfully(test_db_config: PgsqlServerConfig):
            # arrange
            with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
                insert_lms_user(connection, SIS_ID, "c_e5@e.com", SOURCE_SYSTEM)
                insert_edfi_student(connection, UNIQUE_ID, STUDENT_ID)

                insert_lms_user(
                    connection, NOT_MATCHING_SIS_ID, "c_e6@e.com", SOURCE_SYSTEM
                )
                insert_edfi_student(connection, "c_also_not_matching_unique_id")

            # act
            run_harmonizer(test_db_config)

            # assert
            with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
                LMSUser = query(
                    connection,
                    (
                        f"select edfistudentid, sourcesystemidentifier from lms.lmsuser where "
                        f"sourcesystemidentifier in ('{NOT_MATCHING_SIS_ID}','{SIS_ID}')"
                    ),
                )
                assert len(LMSUser) == 2
                assert LMSUser[0]["sourcesystemidentifier"] == NOT_MATCHING_SIS_ID
                assert LMSUser[0]["edfistudentid"] is None
                assert LMSUser[1]["sourcesystemidentifier"] == SIS_ID
                assert LMSUser[1]["edfistudentid"] == STUDENT_ID
