# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from tests_integration_pgsql.pgsql_loader import (
    insert_lms_section,
    insert_edfi_section,
    insert_lms_section_deleted,
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
                connection,
                "select sourcesystemidentifier from lmsx.exceptions_lmssection",
            )

            assert len(exceptions) == 0


def describe_when_lms_and_ods_tables_have_no_matches():
    SIS_ID_1 = "e+sis_id_1_a"
    SIS_ID_2 = "e+sis_id_1_b"

    def it_should_return_exceptions(test_db_config: PgsqlServerConfig):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            insert_lms_section(connection, SIS_ID_1, SOURCE_SYSTEM)
            insert_lms_section(connection, SIS_ID_2, SOURCE_SYSTEM)
            insert_edfi_section(connection, "e+not_matching_sis_id_1")
            insert_edfi_section(connection, "e+not_matching_sis_id_2")

        # act
        run_harmonizer(test_db_config)

        # assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            exceptions = query(
                connection,
                f"select sourcesystemidentifier from lmsx.exceptions_lmssection where sourcesystemidentifier  IN ('{SIS_ID_1}','{SIS_ID_2}')",
            )

            assert len(exceptions) == 2
            assert exceptions[0]["sourcesystemidentifier"] == SIS_ID_1
            assert exceptions[1]["sourcesystemidentifier"] == SIS_ID_2


def describe_when_lms_and_ods_tables_have_a_match():
    SIS_ID = "e+sis_id_2"
    SECTION_ID = "10000000-0000-0000-0000-000000000002"

    def it_should_return_no_exceptions(test_db_config: PgsqlServerConfig):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            insert_lms_section(connection, SIS_ID, SOURCE_SYSTEM)
            insert_edfi_section(connection, SIS_ID, SECTION_ID)

        # act
        run_harmonizer(test_db_config)

        # assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            exceptions = query(
                connection,
                f"select sourcesystemidentifier from lmsx.exceptions_lmssection where sourcesystemidentifier = '{SIS_ID}'",
            )

            assert len(exceptions) == 0


def describe_when_lms_and_ods_tables_have_a_match_to_deleted_record():
    SECTION_ID = "10000000-0000-0000-0000-000000000003"
    SIS_ID = "e+sis_id_3"

    def it_should_return_no_exceptions(test_db_config: PgsqlServerConfig):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            insert_lms_section_deleted(connection, SIS_ID, SOURCE_SYSTEM)
            insert_edfi_section(connection, SIS_ID, SECTION_ID)

        # act
        run_harmonizer(test_db_config)

        # assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            exceptions = query(
                connection,
                f"select sourcesystemidentifier from lmsx.exceptions_lmssection where sourcesystemidentifier = '{SIS_ID}'",
            )

            assert len(exceptions) == 0


def describe_when_lms_and_ods_tables_have_one_match_and_one_not_match():
    SECTION_ID = "10000000-0000-0000-0000-000000000004"
    SIS_ID = "e+sis_id_4"
    NOT_MATCHING_SIS_ID = "e+not_matching_sis_id_4"

    def it_should_return_one_exception(test_db_config: PgsqlServerConfig):
        # arrange
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            insert_lms_section(connection, SIS_ID, SOURCE_SYSTEM)  # Matching section
            insert_edfi_section(connection, SIS_ID, SECTION_ID)  # Matching section

            insert_lms_section(
                connection, NOT_MATCHING_SIS_ID, SOURCE_SYSTEM
            )  # Not matching section
            insert_edfi_section(
                connection, "also_not_matching_sis_id"
            )  # Not matching section

        # act
        run_harmonizer(test_db_config)

        # assert
        with PgsqlConnection(test_db_config).pyodbc_conn() as connection:
            exceptions = query(
                connection,
                f"select sourcesystemidentifier from lmsx.exceptions_lmssection where sourcesystemidentifier = '{NOT_MATCHING_SIS_ID}'",
            )

            assert len(exceptions) == 1
            assert exceptions[0]["sourcesystemidentifier"] == NOT_MATCHING_SIS_ID
