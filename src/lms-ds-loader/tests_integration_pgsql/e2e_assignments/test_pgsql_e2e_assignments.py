# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Tuple
from sqlalchemy.engine.base import Connection
from edfi_lms_ds_loader.sql_lms_operations import SqlLmsOperations
from edfi_lms_ds_loader.loader_facade import run_loader
from tests_integration_pgsql.pgsql_e2e_helper import (
    insert_section,
    main_arguments,
    insert_assignment
)
from tests_integration_pgsql.conftest import ConnectionSettings

CSV_PATH = "tests_integration_mssql/e2e_assignments/data"
SOURCE_SYSTEM = "BestLMS"


def describe_when_a_record_is_missing_in_the_csv():
    def it_should_soft_delete_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection, ConnectionSettings]
    ):
        adapter, connection, settings = test_pgsql_db

        # arrange - note csv file has only B123456
        section_identifier = 11
        insert_section(connection, "B098765", SOURCE_SYSTEM, section_identifier)
        insert_assignment(connection, "B123456", SOURCE_SYSTEM, 11, section_identifier)
        insert_assignment(connection, "B234567", SOURCE_SYSTEM, 12, section_identifier)

        # act
        run_loader(main_arguments(adapter, CSV_PATH, settings))

        # assert - B234567 has been soft deleted
        Assignment = connection.execute(
            "select sourcesystemidentifier from lms.assignment where deletedat is not null"
        ).fetchall()
        assert len(Assignment) == 1
        assert Assignment[0]["sourcesystemidentifier"] == "B234567"


def describe_when_a_record_is_from_one_source_system_of_two_in_the_csv():
    def it_should_match_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection, ConnectionSettings]
    ):
        adapter, connection, settings = test_pgsql_db

        section_identifier_1 = 11
        insert_section(connection, "B098765", SOURCE_SYSTEM, section_identifier_1)
        section_identifier_2 = 12
        insert_section(connection, "F098765", "FirstLMS", section_identifier_2)

        insert_assignment(connection, "B123456", SOURCE_SYSTEM, 11, section_identifier_1)
        insert_assignment(connection, "F234567", "FirstLMS", 12, section_identifier_2)

        # act
        run_loader(main_arguments(adapter, CSV_PATH, settings))

        # assert - records are unchanged
        Assignment = connection.execute(
            "select sourcesystem, sourcesystemidentifier, deletedat from lms.assignment order by sourcesystemidentifier"
        ).fetchall()
        assert len(Assignment) == 2
        assert [SOURCE_SYSTEM, "FirstLMS"] == [x["sourcesystem"] for x in Assignment]
        assert ["B123456", "F234567"] == [
            x["sourcesystemidentifier"] for x in Assignment
        ]
        assert [None, None] == [x["deletedat"] for x in Assignment]


def describe_when_a_record_is_from_one_source_system_in_the_csv():
    def it_should_match_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection, ConnectionSettings]
    ):
        adapter, connection, settings = test_pgsql_db

        section_identifier_1 = 13
        insert_section(connection, "B098765", SOURCE_SYSTEM, section_identifier_1)
        section_identifier_2 = 14
        insert_section(connection, "B109876", SOURCE_SYSTEM, section_identifier_2)

        insert_assignment(connection, "B123456", SOURCE_SYSTEM, 11, section_identifier_1)
        insert_assignment(connection, "B234567", SOURCE_SYSTEM, 12, section_identifier_2)

        # act
        run_loader(main_arguments(adapter, CSV_PATH, settings))

        # assert - records are unchanged
        Assignment = connection.execute(
            "select sourcesystem, sourcesystemidentifier, deletedat from lms.assignment order by sourcesystemidentifier"
        ).fetchall()
        assert len(Assignment) == 2
        assert [SOURCE_SYSTEM, SOURCE_SYSTEM] == [x["sourcesystem"] for x in Assignment]
        assert ["B123456", "B234567"] == [
            x["sourcesystemidentifier"] for x in Assignment
        ]
        assert [None, None] == [x["deletedat"] for x in Assignment]
