# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Tuple
from sqlalchemy.engine.base import Connection
from edfi_lms_ds_loader.sql_lms_operations import SqlLmsOperations
from edfi_lms_ds_loader.loader_facade import run_loader
from tests_integration_pgsql.pgsql_e2e_helper import main_arguments, insert_section
from tests_integration_pgsql.conftest import ConnectionSettings

CSV_PATH = "tests_integration_mssql/e2e_sections/data"
SOURCE_SYSTEM = "BestLMS"


def describe_when_a_record_is_missing_in_the_csv():
    def it_should_soft_delete_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection, ConnectionSettings]
    ):
        adapter, connection, settings = test_pgsql_db

        # arrange - note csv file has only B123456
        insert_section(connection, "B123456", SOURCE_SYSTEM, 99988)
        insert_section(connection, "B234567", SOURCE_SYSTEM, 99989)

        # act
        run_loader(main_arguments(adapter, CSV_PATH, settings))

        # assert - B234567 has been soft deleted
        LMSSection = connection.execute(
            "select sourcesystemidentifier from lms.lmssection where deletedat is not null"
        ).fetchall()
        assert len(LMSSection) == 1
        assert LMSSection[0]["sourcesystemidentifier"] == "B234567"


def describe_when_a_record_is_from_one_source_system_in_the_csv():
    def it_should_match_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection, ConnectionSettings]
    ):
        adapter, connection, settings = test_pgsql_db

        # arrange - note csv file has only B123456 from BestLMS
        insert_section(connection, "B123456", SOURCE_SYSTEM, 99998)
        insert_section(connection, "F234567", "FirstLMS", 99999)

        # act
        run_loader(main_arguments(adapter, CSV_PATH, settings))

        # assert - records are unchanged
        LMSSection = connection.execute(
            "select sourcesystem, sourcesystemidentifier, deletedat from lms.lmssection order by sourcesystemidentifier"
        ).fetchall()
        assert len(LMSSection) == 2
        assert [SOURCE_SYSTEM, "FirstLMS"] == [x["sourcesystem"] for x in LMSSection]
        assert ["B123456", "F234567"] == [
            x["sourcesystemidentifier"] for x in LMSSection
        ]
        assert [None, None] == [x["deletedat"] for x in LMSSection]
