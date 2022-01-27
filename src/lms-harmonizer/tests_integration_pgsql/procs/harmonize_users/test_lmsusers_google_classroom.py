# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from tests_integration_pgsql.pgsql_loader import (
    insert_lms_user,
    insert_lms_user_deleted,
    insert_edfi_student_with_usi,
    insert_edfi_student_electronic_mail,
)
from tests_integration_pgsql.pgsql_connection import PgsqlConnection, query
from tests_integration_pgsql.pgsql_server_config import PgsqlServerConfig
from tests_integration_pgsql.pgsql_orchestrator import run_harmonizer


SOURCE_SYSTEM = "Google"


def describe_when_harmonizing_google_users():
    def describe_given_lms_and_ods_tables_have_no_matches():
        def it_should_run_successfully(test_db_config: PgsqlServerConfig):
            SIS_ID_1 = "g_sis_id_1"
            SIS_ID_2 = "g_sis_id_2"

            # arrange
            with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
                insert_lms_user(connection, SIS_ID_1, "g_e1@e.com", SOURCE_SYSTEM)
                insert_lms_user(connection, SIS_ID_2, "g_e2@e.com", SOURCE_SYSTEM)
                insert_edfi_student_with_usi(connection, 111)
                insert_edfi_student_with_usi(connection, 121)
                insert_edfi_student_electronic_mail(connection, 111, "g_not_e1@e.com")
                insert_edfi_student_electronic_mail(connection, 121, "g_not_e2@e.com")

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
        STUDENT_ID = "1C200000-0000-0000-0000-000000000000"
        SIS_ID = "g_sis_id2"
        EMAIL = "g_email2@e.com"

        def it_should_run_successfully(test_db_config: PgsqlServerConfig):
            # arrange
            with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
                insert_lms_user(connection, SIS_ID, EMAIL, SOURCE_SYSTEM)
                insert_edfi_student_with_usi(connection, 31, STUDENT_ID)
                insert_edfi_student_electronic_mail(connection, 31, EMAIL)

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
        STUDENT_ID = "2C200000-0000-0000-0000-000000000000"
        SIS_ID = "g_sis_id3"
        EMAIL = "g_email3@e.com"

        def it_should_ignore_the_deleted_record(test_db_config: PgsqlServerConfig):
            # arrange
            with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
                insert_lms_user_deleted(connection, SIS_ID, EMAIL, SOURCE_SYSTEM)
                insert_edfi_student_with_usi(connection, 41, STUDENT_ID)
                insert_edfi_student_electronic_mail(connection, 41, EMAIL)

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

    def describe_given_single_student_has_multiple_emails_with_one_match():
        STUDENT_ID = "3C200000-0000-0000-0000-000000000000"
        SIS_ID = "g_sis_id4"
        EMAIL = "g_email4@e.com"

        def it_should_run_successfully(test_db_config: PgsqlServerConfig):
            # arrange
            with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
                insert_lms_user(connection, SIS_ID, EMAIL, SOURCE_SYSTEM)
                insert_edfi_student_with_usi(connection, 51, STUDENT_ID)
                insert_edfi_student_electronic_mail(connection, 51, "g_not_emai4l@e.com")
                insert_edfi_student_electronic_mail(connection, 51, EMAIL)
                insert_edfi_student_electronic_mail(connection, 51, "g_also_not_email4@e.com")

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

    def describe_given_lms_and_ods_tables_have_one_match_and_one_not_match():
        STUDENT_ID = "4C200000-0000-0000-0000-000000000000"
        SIS_ID = "g_sis_id5"
        EMAIL = "g_email5@e.com"

        NOT_MATCHING_STUDENT_ID = "5C200000-0000-0000-0000-000000000000"
        NOT_MATCHING_SIS_ID = "g_not_matching_sis_id5"
        NOT_MATCHING_EMAIL = "g_not_email5@e.com"

        def it_should_run_successfully(test_db_config: PgsqlServerConfig):
            # arrange
            with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
                insert_lms_user(connection, SIS_ID, EMAIL, SOURCE_SYSTEM)
                insert_lms_user(
                    connection, NOT_MATCHING_SIS_ID, NOT_MATCHING_EMAIL, SOURCE_SYSTEM
                )

                insert_edfi_student_with_usi(connection, 61, STUDENT_ID)
                insert_edfi_student_electronic_mail(connection, 61, EMAIL)

                insert_edfi_student_with_usi(connection, 62, NOT_MATCHING_STUDENT_ID)
                insert_edfi_student_electronic_mail(connection, 62, "g_also_not_email5@e.com")

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
