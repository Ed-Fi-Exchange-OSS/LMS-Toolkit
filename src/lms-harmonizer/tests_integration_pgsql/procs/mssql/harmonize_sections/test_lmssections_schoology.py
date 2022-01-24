# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from tests_integration_sql.mssql_loader import (
    insert_lms_section,
    insert_lms_section_deleted,
    insert_edfi_section,
)
from tests_integration_sql.mssql_connection import MSSqlConnection, query
from tests_integration_sql.server_config import ServerConfig
from tests_integration_sql.orchestrator import run_harmonizer


SOURCE_SYSTEM = "Schoology"


def describe_when_lms_and_ods_tables_are_both_empty():
    def it_should_run_successfully(test_db_config: ServerConfig):
        # act
        run_harmonizer(test_db_config)
        # assert - no errors


def describe_when_lms_and_ods_tables_have_no_matches():
    def it_should_run_successfully(test_db_config: ServerConfig):
        # arrange
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:
            insert_lms_section(connection, "sis_id_1", SOURCE_SYSTEM)
            insert_lms_section(connection, "sis_id_2", SOURCE_SYSTEM)
            insert_edfi_section(connection, "not_matching_sis_id_1")
            insert_edfi_section(connection, "not_matching_sis_id_2")

        # act
        run_harmonizer(test_db_config)

        # assert
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSSection = query(connection, "SELECT EdFiSectionId from lms.LMSSection")
            assert len(LMSSection) == 2
            assert LMSSection[0]["EdFiSectionId"] is None
            assert LMSSection[1]["EdFiSectionId"] is None


def describe_when_lms_and_ods_tables_have_a_match():
    SIS_ID = "sis_id"
    SECTION_ID = "10000000-0000-0000-0000-000000000000"

    def it_should_run_successfully(test_db_config: ServerConfig):
        # arrange
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:
            insert_lms_section(connection, SIS_ID, SOURCE_SYSTEM)
            insert_edfi_section(connection, SIS_ID, SECTION_ID)

        # act
        run_harmonizer(test_db_config)

        # assert
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSSection = query(connection, "SELECT EdFiSectionId from lms.LMSSection")
            assert len(LMSSection) == 1
            assert LMSSection[0]["EdFiSectionId"] == SECTION_ID


def describe_when_lms_and_ods_tables_have_a_match_to_deleted_record():
    SECTION_ID = "10000000-0000-0000-0000-000000000000"
    SIS_ID = "sis_id"

    def it_should_ignore_the_deleted_record(test_db_config: ServerConfig):
        # arrange
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:
            insert_lms_section_deleted(connection, SIS_ID, SOURCE_SYSTEM)
            insert_edfi_section(connection, SIS_ID, SECTION_ID)

        # act
        run_harmonizer(test_db_config)

        # assert
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSSection = query(connection, "SELECT EdFiSectionId from lms.LMSSection")
            assert len(LMSSection) == 1
            assert LMSSection[0]["EdFiSectionId"] is None


def describe_when_lms_and_ods_tables_have_one_match_and_one_not_match():
    SECTION_ID = "10000000-0000-0000-0000-000000000000"
    SIS_ID = "sis_id"
    NOT_MATCHING_SIS_ID = "not_matching_sis_id"

    def it_should_run_successfully(test_db_config: ServerConfig):
        # arrange
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:
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
        with MSSqlConnection(test_db_config).pyodbc_conn() as connection:
            LMSSection = query(
                connection,
                "SELECT EdFiSectionId, SISSectionIdentifier from lms.LMSSection",
            )
            assert len(LMSSection) == 2
            assert LMSSection[0]["SISSectionIdentifier"] == SIS_ID
            assert LMSSection[0]["EdFiSectionId"] == SECTION_ID
            assert LMSSection[1]["SISSectionIdentifier"] == NOT_MATCHING_SIS_ID
            assert LMSSection[1]["EdFiSectionId"] is None
