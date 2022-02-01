# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Tuple
from sqlalchemy.engine.base import Connection
from edfi_lms_ds_loader.sql_lms_operations import SqlLmsOperations
from edfi_lms_ds_loader.loader_facade import run_loader
from tests_integration_pgsql.pgsql_e2e_helper import (
    insert_assignment,
    insert_section,
    insert_user,
    main_arguments,
)
from tests_integration_pgsql.conftest import ConnectionSettings

CSV_PATH = "tests_integration_mssql/e2e_assignment_submissions/data"
SOURCE_SYSTEM = "BestLMS"


def insert_record(
    connection: Connection,
    ss_identifier: str,
    source_system: str,
    assignment_identifier: int,
    user_identifier: int,
):
    connection.execute(
        f"""
    insert into lms.assignmentsubmission
           (sourcesystemidentifier
           ,sourcesystem
           ,assignmentidentifier
           ,lmsuseridentifier
           ,submissionstatus
           ,submissiondatetime
           ,earnedpoints
           ,grade
           ,sourcecreatedate
           ,sourcelastmodifieddate
           ,createdate
           ,lastmodifieddate
           ,deletedat)
     values
           ('{ss_identifier}'
           ,'{source_system}'
           ,{assignment_identifier}
           ,{user_identifier}
           ,'Returned'
           ,'2021-01-01 00:00:00'
           ,100
           ,n'a'
           ,null
           ,null
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,null
           )
"""
    )


def describe_when_a_record_is_missing_in_the_csv():
    def it_should_soft_delete_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection, ConnectionSettings]
    ):
        adapter, connection, settings = test_pgsql_db

        # arrange - note csv file has only B123456
        user_identifier = 13
        insert_user(connection, "U123456", SOURCE_SYSTEM, user_identifier)

        section_identifier = 14
        insert_section(connection, "S098765", SOURCE_SYSTEM, section_identifier)

        assignment_identifier = 15
        insert_assignment(connection, "B098765", SOURCE_SYSTEM, assignment_identifier, section_identifier)

        insert_record(connection, "B123456", SOURCE_SYSTEM, assignment_identifier, user_identifier)
        insert_record(connection, "B234567", SOURCE_SYSTEM, assignment_identifier, user_identifier)

        # act
        run_loader(main_arguments(adapter, CSV_PATH, settings))

        # assert - B234567 has been soft deleted
        AssignmentSubmission = connection.execute(
            "select sourcesystemidentifier from lms.assignmentsubmission where deletedat is not null"
        ).fetchall()
        assert len(AssignmentSubmission) == 1
        assert AssignmentSubmission[0]["sourcesystemidentifier"] == "B234567"


def describe_when_a_record_is_from_one_source_system_of_two_in_the_csv():
    def it_should_match_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection, ConnectionSettings]
    ):
        adapter, connection, settings = test_pgsql_db

        user_identifier = 11
        insert_user(connection, "U123456", SOURCE_SYSTEM, user_identifier)
        user_identifier = 12
        insert_user(connection, "U123456", "FirstLMS", user_identifier)

        section_identifier = 13
        insert_section(connection, "S098765", SOURCE_SYSTEM, section_identifier)
        section_identifier = 14
        insert_section(connection, "S098765", "FirstLMS", section_identifier)

        assignment_identifier_1 = 15
        insert_assignment(connection, "B098765", SOURCE_SYSTEM, assignment_identifier_1, section_identifier)
        assignment_identifier_2 = 16
        insert_assignment(connection, "F098765", SOURCE_SYSTEM, assignment_identifier_2, section_identifier)

        insert_record(connection, "B123456", SOURCE_SYSTEM, assignment_identifier_1, user_identifier)
        insert_record(connection, "F234567", "FirstLMS", assignment_identifier_2, user_identifier)

        # act
        run_loader(main_arguments(adapter, CSV_PATH, settings))

        # assert - records are unchanged
        AssignmentSubmission = connection.execute(
            "select sourcesystem, sourcesystemidentifier, deletedat from lms.assignmentsubmission order by sourcesystemidentifier"
        ).fetchall()
        assert len(AssignmentSubmission) == 2
        assert [SOURCE_SYSTEM, "FirstLMS"] == [
            x["sourcesystem"] for x in AssignmentSubmission
        ]
        assert ["B123456", "F234567"] == [
            x["sourcesystemidentifier"] for x in AssignmentSubmission
        ]
        assert [None, None] == [x["deletedat"] for x in AssignmentSubmission]


def describe_when_a_record_is_from_one_source_system_in_the_csv():
    def it_should_match_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection, ConnectionSettings]
    ):
        adapter, connection, settings = test_pgsql_db
        user_identifier = 11
        insert_user(connection, "U123456", SOURCE_SYSTEM, user_identifier)

        section_identifier_1 = 12
        insert_section(connection, "S098765", SOURCE_SYSTEM, section_identifier_1)
        section_identifier_2 = 13
        insert_section(connection, "S109876", SOURCE_SYSTEM, section_identifier_2)

        assignment_identifier_1 = 14
        insert_assignment(connection, "B098765", SOURCE_SYSTEM, assignment_identifier_1, section_identifier_1)
        assignment_identifier_2 = 15
        insert_assignment(connection, "B109876", SOURCE_SYSTEM, assignment_identifier_2, section_identifier_2)

        insert_record(connection, "B123456", SOURCE_SYSTEM, assignment_identifier_1, user_identifier)
        insert_record(connection, "B234567", SOURCE_SYSTEM, assignment_identifier_2, user_identifier)

        # act
        run_loader(main_arguments(adapter, CSV_PATH, settings))

        # assert - records are unchanged
        AssignmentSubmission = connection.execute(
            "select sourcesystem, sourcesystemidentifier, deletedat from lms.assignmentsubmission order by sourcesystemidentifier"
        ).fetchall()
        assert len(AssignmentSubmission) == 2
        assert [SOURCE_SYSTEM, SOURCE_SYSTEM] == [
            x["sourcesystem"] for x in AssignmentSubmission
        ]
        assert ["B123456", "B234567"] == [
            x["sourcesystemidentifier"] for x in AssignmentSubmission
        ]
        assert [None, None] == [x["deletedat"] for x in AssignmentSubmission]
