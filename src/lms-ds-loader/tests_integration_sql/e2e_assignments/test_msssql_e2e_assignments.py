# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Tuple
from sqlalchemy.engine.base import Connection
from edfi_lms_ds_loader.Sql_lms_operations import SqlLmsOperations
from edfi_lms_ds_loader.loader_facade import run_loader
from tests_integration_sql.mssql_e2e_helper import (
    insert_section,
    main_arguments,
)

CSV_PATH = "tests_integration_sql/e2e_assignments/data"
SOURCE_SYSTEM = "BestLMS"


def insert_record(
    connection: Connection,
    ss_identifier: str,
    source_system: str,
    section_identifier: int,
):
    connection.execute(
        f"""
    INSERT INTO [lms].[Assignment]
           ([SourceSystemIdentifier]
           ,[SourceSystem]
           ,[LMSSectionIdentifier]
           ,[Title]
           ,[AssignmentCategory]
           ,[AssignmentDescription]
           ,[StartDateTime]
           ,[EndDateTime]
           ,[DueDateTime]
           ,[MaxPoints]
           ,[SourceCreateDate]
           ,[SourceLastModifiedDate]
           ,[CreateDate]
           ,[LastModifiedDate]
           ,[DeletedAt])
     VALUES
           (N'{ss_identifier}'
           ,N'{source_system}'
           ,{section_identifier}
           ,N'{ss_identifier}'
           ,N'online_upload'
           ,N'{ss_identifier}'
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,100
           ,NULL
           ,NULL
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,NULL
           )
"""
    )


def describe_when_a_record_is_missing_in_the_csv():
    def it_should_soft_delete_the_record(
        test_mssql_db: Tuple[SqlLmsOperations, Connection]
    ):
        adapter, connection = test_mssql_db

        # arrange - note csv file has only B123456
        insert_section(connection, "B098765", SOURCE_SYSTEM, 1)
        insert_record(connection, "B123456", SOURCE_SYSTEM, 1)
        insert_record(connection, "B234567", SOURCE_SYSTEM, 1)

        # act
        run_loader(main_arguments(adapter, CSV_PATH))

        # assert - B234567 has been soft deleted
        Assignment = connection.execute(
            "SELECT SourceSystemIdentifier from lms.Assignment WHERE DeletedAt IS NOT NULL"
        ).fetchall()
        assert len(Assignment) == 1
        assert Assignment[0]["SourceSystemIdentifier"] == "B234567"


def describe_when_a_record_is_from_one_source_system_of_two_in_the_csv():
    def it_should_match_the_record(
        test_mssql_db: Tuple[SqlLmsOperations, Connection]
    ):
        adapter, connection = test_mssql_db

        insert_section(connection, "B098765", SOURCE_SYSTEM, 1)
        insert_section(connection, "F098765", "FirstLMS", 2)

        insert_record(connection, "B123456", SOURCE_SYSTEM, 1)
        insert_record(connection, "F234567", "FirstLMS", 2)

        # act
        run_loader(main_arguments(adapter, CSV_PATH))

        # assert - records are unchanged
        Assignment = connection.execute(
            "SELECT SourceSystem, SourceSystemIdentifier, DeletedAt from lms.Assignment"
        ).fetchall()
        assert len(Assignment) == 2
        assert [SOURCE_SYSTEM, "FirstLMS"] == [x["SourceSystem"] for x in Assignment]
        assert ["B123456", "F234567"] == [
            x["SourceSystemIdentifier"] for x in Assignment
        ]
        assert [None, None] == [x["DeletedAt"] for x in Assignment]


def describe_when_a_record_is_from_one_source_system_in_the_csv():
    def it_should_match_the_record(
        test_mssql_db: Tuple[SqlLmsOperations, Connection]
    ):
        adapter, connection = test_mssql_db

        insert_section(connection, "B098765", SOURCE_SYSTEM, 1)
        insert_section(connection, "B109876", SOURCE_SYSTEM, 2)

        insert_record(connection, "B123456", SOURCE_SYSTEM, 1)
        insert_record(connection, "B234567", SOURCE_SYSTEM, 2)

        # act
        run_loader(main_arguments(adapter, CSV_PATH))

        # assert - records are unchanged
        Assignment = connection.execute(
            "SELECT SourceSystem, SourceSystemIdentifier, DeletedAt from lms.Assignment"
        ).fetchall()
        assert len(Assignment) == 2
        assert [SOURCE_SYSTEM, SOURCE_SYSTEM] == [x["SourceSystem"] for x in Assignment]
        assert ["B123456", "B234567"] == [
            x["SourceSystemIdentifier"] for x in Assignment
        ]
        assert [None, None] == [x["DeletedAt"] for x in Assignment]
