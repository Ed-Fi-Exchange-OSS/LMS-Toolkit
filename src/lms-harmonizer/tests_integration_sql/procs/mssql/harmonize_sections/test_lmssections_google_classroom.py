# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from sqlalchemy.engine.base import Connection
from tests_integration_sql.mssql_helper import (
    script_sql,
    insert_lms_section,
    insert_lms_section_deleted,
    insert_edfi_section,
)

SOURCE_SYSTEM = "Google"
PROC_SQL_DEFINITION = script_sql("1040-lms-section-google-classroom.sql")
PROC_EXEC_STATEMENT = "EXEC lms.harmonize_lmssection_google_classroom;"


def describe_when_lms_and_ods_tables_are_both_empty():
    def it_should_run_successfully(test_mssql_db: Connection):
        # arrange
        test_mssql_db.execute(PROC_SQL_DEFINITION)

        # act
        test_mssql_db.execute(PROC_EXEC_STATEMENT)
        # assert - no errors


def describe_when_lms_and_ods_tables_have_no_matches():
    def it_should_run_successfully(test_mssql_db: Connection):
        # arrange
        test_mssql_db.execute(PROC_SQL_DEFINITION)
        insert_lms_section(test_mssql_db, "sis_id_1", SOURCE_SYSTEM)
        insert_lms_section(test_mssql_db, "sis_id_2", SOURCE_SYSTEM)
        insert_edfi_section(test_mssql_db, "not_matching_sis_id_1")
        insert_edfi_section(test_mssql_db, "not_matching_sis_id_2")

        # act
        test_mssql_db.execute(PROC_EXEC_STATEMENT)

        # assert
        LMSSection = test_mssql_db.execute(
            "SELECT EdFiSectionId from lms.LMSSection"
        ).fetchall()
        assert len(LMSSection) == 2
        assert LMSSection[0]["EdFiSectionId"] is None
        assert LMSSection[1]["EdFiSectionId"] is None


def describe_when_lms_and_ods_tables_have_a_match():
    SIS_ID = "sis_id"
    SECTION_ID = "10000000-0000-0000-0000-000000000000"

    def it_should_run_successfully(test_mssql_db: Connection):
        # arrange
        test_mssql_db.execute(PROC_SQL_DEFINITION)
        insert_lms_section(test_mssql_db, SIS_ID, SOURCE_SYSTEM)
        insert_edfi_section(test_mssql_db, SIS_ID, SECTION_ID)

        # act
        test_mssql_db.execute(PROC_EXEC_STATEMENT)

        # assert
        LMSSection = test_mssql_db.execute(
            "SELECT EdFiSectionId from lms.LMSSection"
        ).fetchall()
        assert len(LMSSection) == 1
        assert LMSSection[0]["EdFiSectionId"] == SECTION_ID


def describe_when_lms_and_ods_tables_have_a_match_to_deleted_record():
    SECTION_ID = "10000000-0000-0000-0000-000000000000"
    SIS_ID = "sis_id"

    def it_should_ignore_the_deleted_record(test_mssql_db: Connection):
        # arrange
        test_mssql_db.execute(PROC_SQL_DEFINITION)
        insert_lms_section_deleted(test_mssql_db, SIS_ID, SOURCE_SYSTEM)
        insert_edfi_section(test_mssql_db, SIS_ID, SECTION_ID)

        # act
        test_mssql_db.execute(PROC_EXEC_STATEMENT)

        # assert
        LMSSection = test_mssql_db.execute(
            "SELECT EdFiSectionId from lms.LMSSection"
        ).fetchall()
        assert len(LMSSection) == 1
        assert LMSSection[0]["EdFiSectionId"] is None


def describe_when_lms_and_ods_tables_have_one_match_and_one_not_match():
    SECTION_ID = "10000000-0000-0000-0000-000000000000"
    SIS_ID = "sis_id"
    NOT_MATCHING_SIS_ID = "not_matching_sis_id"

    def it_should_run_successfully(test_mssql_db: Connection):
        # arrange
        test_mssql_db.execute(PROC_SQL_DEFINITION)
        insert_lms_section(test_mssql_db, SIS_ID, SOURCE_SYSTEM)  # Matching section
        insert_edfi_section(test_mssql_db, SIS_ID, SECTION_ID)  # Matching section

        insert_lms_section(
            test_mssql_db, NOT_MATCHING_SIS_ID, SOURCE_SYSTEM
        )  # Not matching section
        insert_edfi_section(
            test_mssql_db, "also_not_matching_sis_id"
        )  # Not matching section

        # act
        test_mssql_db.execute(PROC_EXEC_STATEMENT)

        # assert
        LMSSection = test_mssql_db.execute(
            "SELECT EdFiSectionId, SISSectionIdentifier from lms.LMSSection"
        ).fetchall()
        assert len(LMSSection) == 2
        assert LMSSection[0]["SISSectionIdentifier"] == SIS_ID
        assert LMSSection[0]["EdFiSectionId"] == SECTION_ID
        assert LMSSection[1]["SISSectionIdentifier"] == NOT_MATCHING_SIS_ID
        assert LMSSection[1]["EdFiSectionId"] is None
