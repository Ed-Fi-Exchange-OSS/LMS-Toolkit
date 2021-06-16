# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from sqlalchemy.engine.base import Connection
from tests_integration_sql.mssql_helper import (
    insert_lms_user,
    insert_lms_user_deleted,
    insert_edfi_student_with_usi,
    insert_edfi_student_identification_code,
    script_sql,
)

SOURCE_SYSTEM = "Google Classroom"
PROC_SQL_DEFINITION = script_sql("1020-lms-user-google-classroom.sql")


def describe_when_lms_and_ods_tables_are_both_empty():
    def it_should_run_successfully(test_mssql_db: Connection):
        # arrange
        test_mssql_db.execute(PROC_SQL_DEFINITION)

        # act
        test_mssql_db.execute("EXEC lms.harmonize_lmsuser_google_classroom;")

        # assert - no errors


def describe_when_lms_and_ods_tables_have_no_matches():
    def it_should_run_successfully(test_mssql_db: Connection):
        # arrange
        test_mssql_db.execute(PROC_SQL_DEFINITION)
        insert_lms_user(test_mssql_db, "sis_id_1", SOURCE_SYSTEM)
        insert_lms_user(test_mssql_db, "sis_id_2", SOURCE_SYSTEM)
        insert_edfi_student_with_usi(test_mssql_db, 1)
        insert_edfi_student_with_usi(test_mssql_db, 2)
        insert_edfi_student_identification_code(test_mssql_db, 1, "not_sis_id_1")
        insert_edfi_student_identification_code(test_mssql_db, 2, "not_sis_id_2")

        # act
        test_mssql_db.execute("EXEC lms.harmonize_lmsuser_google_classroom;")

        # assert
        LMSUser = test_mssql_db.execute(
            "SELECT EdFiStudentId from lms.LMSUser"
        ).fetchall()
        assert len(LMSUser) == 2
        assert LMSUser[0]["EdFiStudentId"] is None
        assert LMSUser[1]["EdFiStudentId"] is None


def describe_when_lms_and_ods_tables_have_a_match():
    STUDENT_ID = "10000000-0000-0000-0000-000000000000"
    SIS_ID = "sis_id"

    def it_should_run_successfully(test_mssql_db: Connection):
        # arrange
        test_mssql_db.execute(PROC_SQL_DEFINITION)
        insert_lms_user(test_mssql_db, SIS_ID, SOURCE_SYSTEM)
        insert_edfi_student_with_usi(test_mssql_db, 1, STUDENT_ID)
        insert_edfi_student_identification_code(test_mssql_db, 1, SIS_ID)

        # act
        test_mssql_db.execute("EXEC lms.harmonize_lmsuser_google_classroom;")

        # assert
        LMSUser = test_mssql_db.execute(
            "SELECT EdFiStudentId from lms.LMSUser"
        ).fetchall()
        assert len(LMSUser) == 1
        assert LMSUser[0]["EdFiStudentId"] == STUDENT_ID


def describe_when_lms_and_ods_tables_have_a_match_to_deleted_record():
    STUDENT_ID = "10000000-0000-0000-0000-000000000000"
    SIS_ID = "sis_id"

    def it_should_ignore_the_deleted_record(test_mssql_db: Connection):
        # arrange
        test_mssql_db.execute(PROC_SQL_DEFINITION)
        insert_lms_user_deleted(test_mssql_db, SIS_ID, SOURCE_SYSTEM)
        insert_edfi_student_with_usi(test_mssql_db, 1, STUDENT_ID)
        insert_edfi_student_identification_code(test_mssql_db, 1, SIS_ID)

        # act
        test_mssql_db.execute("EXEC lms.harmonize_lmsuser_google_classroom;")

        # assert
        LMSUser = test_mssql_db.execute(
            "SELECT EdFiStudentId from lms.LMSUser"
        ).fetchall()
        assert len(LMSUser) == 1
        assert LMSUser[0]["EdFiStudentId"] is None


def describe_when_single_student_has_multiple_identification_codes_with_one_match():
    STUDENT_ID = "10000000-0000-0000-0000-000000000000"
    SIS_ID = "sis_id"

    def it_should_run_successfully(test_mssql_db: Connection):
        # arrange
        test_mssql_db.execute(PROC_SQL_DEFINITION)
        insert_lms_user(test_mssql_db, SIS_ID, SOURCE_SYSTEM)
        insert_edfi_student_with_usi(test_mssql_db, 1, STUDENT_ID)
        insert_edfi_student_identification_code(test_mssql_db, 1, "not_sis_id")
        insert_edfi_student_identification_code(test_mssql_db, 1, SIS_ID)
        insert_edfi_student_identification_code(test_mssql_db, 1, "also_not_sis_id")

        # act
        test_mssql_db.execute("EXEC lms.harmonize_lmsuser_google_classroom;")

        # assert
        LMSUser = test_mssql_db.execute(
            "SELECT EdFiStudentId from lms.LMSUser"
        ).fetchall()
        assert len(LMSUser) == 1
        assert LMSUser[0]["EdFiStudentId"] == STUDENT_ID


def describe_when_lms_and_ods_tables_have_one_match_and_one_not_match():
    STUDENT_ID = "10000000-0000-0000-0000-000000000000"
    SIS_ID = "sis_id"
    NOT_MATCHING_SIS_ID = "not_matching_sis_id"

    def it_should_run_successfully(test_mssql_db: Connection):
        # arrange
        test_mssql_db.execute(PROC_SQL_DEFINITION)
        insert_lms_user(test_mssql_db, SIS_ID, SOURCE_SYSTEM)
        insert_lms_user(test_mssql_db, NOT_MATCHING_SIS_ID, SOURCE_SYSTEM)

        insert_edfi_student_with_usi(test_mssql_db, 1, STUDENT_ID)
        insert_edfi_student_identification_code(test_mssql_db, 1, SIS_ID)

        insert_edfi_student_with_usi(test_mssql_db, 2, STUDENT_ID)
        insert_edfi_student_identification_code(
            test_mssql_db, 2, "also_not_matching_sis_id"
        )

        # act
        test_mssql_db.execute("EXEC lms.harmonize_lmsuser_google_classroom;")

        # assert
        LMSUser = test_mssql_db.execute(
            "SELECT EdFiStudentId, SISUserIdentifier from lms.LMSUser"
        ).fetchall()
        assert len(LMSUser) == 2
        assert LMSUser[0]["SISUserIdentifier"] == SIS_ID
        assert LMSUser[0]["EdFiStudentId"] == STUDENT_ID
        assert LMSUser[1]["SISUserIdentifier"] == NOT_MATCHING_SIS_ID
        assert LMSUser[1]["EdFiStudentId"] is None
