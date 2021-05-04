# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Tuple
from sqlalchemy.engine.base import Connection
from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations
from edfi_lms_ds_loader.loader_facade import run_loader
from tests_integration_sql.mssql_e2e_helper import main_arguments

CSV_PATH = "tests_integration_sql/e2e_sections/data"
SOURCE_SYSTEM = "BestLMS"


def insert_record(connection: Connection, ss_identifier: str, source_system: str):
    connection.execute(
        f"""
    INSERT INTO [lms].[LMSSection]
           ([SourceSystemIdentifier]
           ,[SourceSystem]
           ,[SISSectionIdentifier]
           ,[Title]
           ,[SectionDescription]
           ,[Term]
           ,[LMSSectionStatus]
           ,[SourceCreateDate]
           ,[SourceLastModifiedDate]
           ,[CreateDate]
           ,[LastModifiedDate]
           ,[DeletedAt])
     VALUES
           (N'{ss_identifier}'
           ,N'{source_system}'
           ,N'{ss_identifier}'
           ,N'{ss_identifier}'
           ,N'{ss_identifier}'
           ,N'{ss_identifier}'
           ,N'Archived'
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
        test_mssql_db: Tuple[MssqlLmsOperations, Connection]
    ):
        adapter, connection = test_mssql_db

        # arrange - note csv file has only B123456
        insert_record(connection, "B123456", SOURCE_SYSTEM)
        insert_record(connection, "B234567", SOURCE_SYSTEM)

        # act
        run_loader(main_arguments(adapter, CSV_PATH))

        # assert - B234567 has been soft deleted
        LMSSection = connection.execute(
            "SELECT SourceSystemIdentifier from lms.LMSSection WHERE DeletedAt IS NOT NULL"
        ).fetchall()
        assert len(LMSSection) == 1
        assert LMSSection[0]["SourceSystemIdentifier"] == "B234567"


def describe_when_a_record_is_from_one_source_system_in_the_csv():
    def it_should_match_the_record(
        test_mssql_db: Tuple[MssqlLmsOperations, Connection]
    ):
        adapter, connection = test_mssql_db

        # arrange - note csv file has only B123456 from BestLMS
        insert_record(connection, "B123456", SOURCE_SYSTEM)
        insert_record(connection, "F234567", "FirstLMS")

        # act
        run_loader(main_arguments(adapter, CSV_PATH))

        # assert - records are unchanged
        LMSSection = connection.execute(
            "SELECT SourceSystem, SourceSystemIdentifier, DeletedAt from lms.LMSSection"
        ).fetchall()
        assert len(LMSSection) == 2
        assert [SOURCE_SYSTEM, "FirstLMS"] == [x["SourceSystem"] for x in LMSSection]
        assert ["B123456", "F234567"] == [
            x["SourceSystemIdentifier"] for x in LMSSection
        ]
        assert [None, None] == [x["DeletedAt"] for x in LMSSection]
