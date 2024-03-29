# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Tuple
from sqlalchemy.engine.base import Connection
from edfi_lms_ds_loader.sql_lms_operations import SqlLmsOperations
from edfi_lms_ds_loader.loader_facade import run_loader
from tests_integration_mssql.mssql_e2e_helper import (
    insert_section,
    insert_user,
    main_arguments,
)

CSV_PATH = "tests_integration_mssql/e2e_section_activities/data"
SOURCE_SYSTEM = "BestLMS"


def insert_record(
    connection: Connection,
    ss_identifier: str,
    source_system: str,
    section_identifier: int,
    user_identifier: int,
):
    connection.execute(
        f"""
    INSERT INTO [lms].[LMSSectionActivity]
           ([SourceSystemIdentifier]
           ,[SourceSystem]
           ,[LMSUserIdentifier]
           ,[LMSSectionIdentifier]
           ,[ActivityType]
           ,[ActivityDateTime]
           ,[ActivityStatus]
           ,[ParentSourceSystemIdentifier]
           ,[ActivityTimeInMinutes]
           ,[SourceCreateDate]
           ,[SourceLastModifiedDate]
           ,[DeletedAt]
           ,[CreateDate]
           ,[LastModifiedDate])
     VALUES
           (N'{ss_identifier}'
           ,N'{source_system}'
           ,N'{user_identifier}'
           ,N'{section_identifier}'
           ,N'Discussion'
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,N'Published'
           ,NULL
           ,100
           ,NULL
           ,NULL
           ,NULL
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           )
"""
    )


def describe_when_a_record_is_missing_in_the_csv():
    def it_should_soft_delete_the_record(
        test_mssql_db: Tuple[SqlLmsOperations, Connection]
    ):
        adapter, connection = test_mssql_db

        # arrange - note csv file has only B123456
        insert_user(connection, "U123456", SOURCE_SYSTEM, 1)
        insert_section(connection, "B098765", SOURCE_SYSTEM, 1)

        insert_record(connection, "B123456", SOURCE_SYSTEM, 1, 1)
        insert_record(connection, "B234567", SOURCE_SYSTEM, 1, 1)

        # act
        run_loader(main_arguments(adapter, CSV_PATH))

        # assert - B234567 has been soft deleted
        LMSSectionActivity = connection.execute(
            "SELECT SourceSystemIdentifier from lms.LMSSectionActivity WHERE DeletedAt IS NOT NULL"
        ).fetchall()
        assert len(LMSSectionActivity) == 1
        assert LMSSectionActivity[0]["SourceSystemIdentifier"] == "B234567"


def describe_when_a_record_is_from_one_source_system_of_two_in_the_csv():
    def it_should_match_the_record(test_mssql_db: Tuple[SqlLmsOperations, Connection]):
        adapter, connection = test_mssql_db
        insert_user(connection, "U123456", SOURCE_SYSTEM, 1)
        insert_user(connection, "U123456", "FirstLMS", 2)

        insert_section(connection, "B098765", SOURCE_SYSTEM, 1)
        insert_section(connection, "F098765", "FirstLMS", 2)

        insert_record(connection, "B123456", SOURCE_SYSTEM, 1, 1)
        insert_record(connection, "F234567", "FirstLMS", 2, 2)

        # act
        run_loader(main_arguments(adapter, CSV_PATH))

        # assert - records are unchanged
        LMSSectionActivity = connection.execute(
            "SELECT SourceSystem, SourceSystemIdentifier, DeletedAt from lms.LMSSectionActivity"
        ).fetchall()
        assert len(LMSSectionActivity) == 2
        assert [SOURCE_SYSTEM, "FirstLMS"] == [
            x["SourceSystem"] for x in LMSSectionActivity
        ]
        assert ["B123456", "F234567"] == [
            x["SourceSystemIdentifier"] for x in LMSSectionActivity
        ]
        assert [None, None] == [x["DeletedAt"] for x in LMSSectionActivity]


def describe_when_a_record_is_from_one_source_system_in_the_csv():
    def it_should_match_the_record(test_mssql_db: Tuple[SqlLmsOperations, Connection]):
        adapter, connection = test_mssql_db
        insert_user(connection, "U123456", SOURCE_SYSTEM, 1)

        insert_section(connection, "B098765", SOURCE_SYSTEM, 1)
        insert_section(connection, "B109876", SOURCE_SYSTEM, 2)

        insert_record(connection, "B123456", SOURCE_SYSTEM, 1, 1)
        insert_record(connection, "B234567", SOURCE_SYSTEM, 2, 1)

        # act
        run_loader(main_arguments(adapter, CSV_PATH))

        # assert - records are unchanged
        LMSSectionActivity = connection.execute(
            "SELECT SourceSystem, SourceSystemIdentifier, DeletedAt from lms.LMSSectionActivity"
        ).fetchall()
        assert len(LMSSectionActivity) == 2
        assert [SOURCE_SYSTEM, SOURCE_SYSTEM] == [
            x["SourceSystem"] for x in LMSSectionActivity
        ]
        assert ["B123456", "B234567"] == [
            x["SourceSystemIdentifier"] for x in LMSSectionActivity
        ]
        assert [None, None] == [x["DeletedAt"] for x in LMSSectionActivity]
