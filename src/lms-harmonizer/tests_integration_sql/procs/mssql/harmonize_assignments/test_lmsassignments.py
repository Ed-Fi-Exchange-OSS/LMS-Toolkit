# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from sqlalchemy.engine.base import Connection
from tests_integration_sql.mssql_helper import (
    insert_lms_assignment,
    script_sql,
    insert_lms_section,
    insert_edfi_section,
    insert_descriptor,
    insert_lmsx_sourcesystem_descriptor,
    insert_lmsx_assignmentcategory_descriptor
)

SOURCE_SYSTEM = "Test_LMS"
DESCRIPTOR_NAMESPACE = "uri://ed-fi.org/edfilms/AssignmentCategoryDescriptor/" + SOURCE_SYSTEM

PROC_SQL_DEFINITION = script_sql("1080-lms-assignment.sql")
PROC_EXEC_STATEMENT = "EXEC lms.harmonize_assignment;"


def describe_when_lms_and_ods_tables_are_both_empty():
    def it_should_run_successfully(test_mssql_db: Connection):
        # arrange
        test_mssql_db.execute(PROC_SQL_DEFINITION)

        # act
        test_mssql_db.execute(PROC_EXEC_STATEMENT)
        # assert - no errors


def describe_when_lms_and_ods_tables_have_no_section_matches():
    def it_should_run_successfully(test_mssql_db: Connection):
        section_id_1 = "sis_id_1"
        section_id_2 = "sis_id_2"
        # arrange
        test_mssql_db.execute(PROC_SQL_DEFINITION)
        insert_lms_section(test_mssql_db, section_id_1, SOURCE_SYSTEM)
        insert_lms_section(test_mssql_db, section_id_2, SOURCE_SYSTEM)
        insert_edfi_section(test_mssql_db, "not_matching_sis_id_1")
        insert_edfi_section(test_mssql_db, "not_matching_sis_id_2")

        # act
        test_mssql_db.execute(PROC_EXEC_STATEMENT)

        # assert
        LMSSection = test_mssql_db.execute(
            "SELECT AssignmentIdentifier from [lmsx].[Assignment]"
        ).fetchall()
        assert len(LMSSection) == 0


def describe_when_there_are_assignments_to_insert():
    SIS_SECTION_ID = "sis_section_id"
    ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER = "assignment_identifier"
    ASSIGNMENT_CATEGORY = 'test_category'

    def it_should_run_successfully(test_mssql_db: Connection):
        # arrange
        test_mssql_db.execute(PROC_SQL_DEFINITION)

        insert_descriptor(test_mssql_db, DESCRIPTOR_NAMESPACE, ASSIGNMENT_CATEGORY)
        insert_lmsx_assignmentcategory_descriptor(test_mssql_db, 1)

        insert_descriptor(test_mssql_db, DESCRIPTOR_NAMESPACE, SOURCE_SYSTEM)
        insert_lmsx_sourcesystem_descriptor(test_mssql_db, 2)

        insert_lms_section(test_mssql_db, SIS_SECTION_ID, SOURCE_SYSTEM)
        insert_edfi_section(test_mssql_db, SIS_SECTION_ID)

        insert_lms_assignment(
            test_mssql_db,
            ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER,
            SOURCE_SYSTEM,
            1,
            ASSIGNMENT_CATEGORY
            )

        # act
        test_mssql_db.execute(PROC_EXEC_STATEMENT)

        # assert
        LMSAssignment = test_mssql_db.execute(
            "SELECT AssignmentIdentifier from [lmsx].[Assignment]"
        ).fetchall()
        DESCRIPTORS = test_mssql_db.execute(
            "SELECT * from [edfi].[descriptor]"
        ).fetchall()
        print(DESCRIPTORS)
        assert len(LMSAssignment) == 1
        assert LMSAssignment[0]["AssignmentIdentifier"] == ASSIGNMENT_SOURCE_SYSTEM_IDENTIFIER
