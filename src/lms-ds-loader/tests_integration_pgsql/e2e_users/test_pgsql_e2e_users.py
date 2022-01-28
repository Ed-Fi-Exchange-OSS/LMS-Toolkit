# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Tuple
from sqlalchemy.engine.base import Connection
from edfi_lms_ds_loader.sql_lms_operations import SqlLmsOperations
from edfi_lms_ds_loader.loader_facade import run_loader
from tests_integration_pgsql.pgsql_e2e_helper import main_arguments, insert_user

CSV_PATH = "tests_integration_mssql/e2e_users/data"
SOURCE_SYSTEM = "BestLMS"


def describe_when_a_record_is_missing_in_the_csv():
    def it_should_soft_delete_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection]
    ):
        adapter, connection = test_pgsql_db

        # arrange - note csv file has only B123456
        insert_user(connection, "B123456", SOURCE_SYSTEM, 9998)
        insert_user(connection, "B234567", SOURCE_SYSTEM, 9999)

        # act
        run_loader(main_arguments(adapter, CSV_PATH))

        # assert - B234567 has been soft deleted
        LMSUser = connection.execute(
            "select sourcesystemidentifier from lms.lmsuser where deletedat is not null"
        ).fetchall()
        assert len(LMSUser) == 1
        assert LMSUser[0]["sourcesystemidentifier"] == "B234567"


def describe_when_a_record_is_from_one_source_system_in_the_csv():
    def it_should_not_soft_delete_record_from_different_source_system(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection]
    ):
        adapter, connection = test_pgsql_db

        # arrange - note csv file has only B123456 from BestLMS. F234567 is from
        # a different source system. Although it is missing from the file, it
        # should not be soft deleted.
        insert_user(connection, "B123456", SOURCE_SYSTEM, 99898)
        insert_user(connection, "F234567", "FirstLMS", 99899)

        # act
        run_loader(main_arguments(adapter, CSV_PATH))

        # assert - records are unchanged
        LMSUser = connection.execute(
            "select sourcesystem, sourcesystemidentifier, deletedat from lms.lmsuser order by sourcesystemidentifier"
        ).fetchall()
        assert len(LMSUser) == 2

        def get_user(source_system: str) -> dict:
            query = [x for x in LMSUser if x["sourcesystem"] == source_system]
            assert len(query) == 1, f"No record returned for {source_system}"

            return query[0]

        first = get_user("FirstLMS")
        assert "F234567" == first["sourcesystemidentifier"], "First sourcesystemidentifier"
        assert first["deletedat"] is None, "First deletedat"

        first = get_user(SOURCE_SYSTEM)
        assert "B123456" == first["sourcesystemidentifier"], "Best sourcesystemidentifier"
        assert first["deletedat"] is None, "Best deletedat"
