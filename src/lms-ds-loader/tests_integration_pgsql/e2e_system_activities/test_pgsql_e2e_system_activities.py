# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Tuple
from sqlalchemy.engine.base import Connection
from edfi_lms_ds_loader.sql_lms_operations import SqlLmsOperations
from edfi_lms_ds_loader.loader_facade import run_loader
from tests_integration_pgsql.pgsql_e2e_helper import main_arguments, insert_user
from tests_integration_pgsql.conftest import ConnectionSettings

CSV_PATH = "tests_integration_mssql/e2e_system_activities/data"
SOURCE_SYSTEM = "BestLMS"


def insert_record(connection: Connection, ss_identifier: str, source_system: str):
    connection.execute(
        f"""
    insert into lms.lmssystemactivity
           (sourcesystemidentifier
           ,sourcesystem
           ,lmsuseridentifier
           ,activitytype
           ,activitydatetime
           ,activitystatus
           ,parentsourcesystemidentifier
           ,activitytimeinminutes
           ,sourcecreatedate
           ,sourcelastmodifieddate
           ,deletedat
           ,createdate
           ,lastmodifieddate)
     values
           ('{ss_identifier}'
           ,'{source_system}'
           ,1
           ,'sign-in'
           ,'2021-01-01 00:00:00'
           ,'active'
           ,null
           ,null
           ,null
           ,null
           ,null
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           )
"""
    )


def describe_when_a_record_is_missing_in_the_csv():
    def it_should_soft_delete_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection, ConnectionSettings]
    ):
        adapter, connection, settings = test_pgsql_db

        # arrange - note csv file has only B123456
        insert_user(connection, "U123456", SOURCE_SYSTEM, 1)
        insert_record(connection, "B123456", SOURCE_SYSTEM)
        insert_record(connection, "B234567", SOURCE_SYSTEM)

        # act
        run_loader(main_arguments(adapter, CSV_PATH, settings))

        # assert - B234567 has been soft deleted
        LMSSystemActivity = connection.execute(
            "select sourcesystemidentifier from lms.lmssystemactivity where deletedat is not null"
        ).fetchall()
        assert len(LMSSystemActivity) == 1
        assert LMSSystemActivity[0]["sourcesystemidentifier"] == "B234567"


def describe_when_a_record_is_from_one_source_system_in_the_csv():
    def it_should_match_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection, ConnectionSettings]
    ):
        adapter, connection, settings = test_pgsql_db

        # arrange - note csv file has only B123456 from BestLMS
        insert_user(connection, "U123456", SOURCE_SYSTEM, 1)
        insert_record(connection, "B123456", SOURCE_SYSTEM)
        insert_record(connection, "F234567", "FirstLMS")

        # act
        run_loader(main_arguments(adapter, CSV_PATH, settings))

        # assert - records are unchanged
        LMSSystemActivity = connection.execute(
            "select sourcesystem, sourcesystemidentifier, deletedat from lms.lmssystemactivity order by sourcesystemidentifier"
        ).fetchall()
        assert len(LMSSystemActivity) == 2
        assert [SOURCE_SYSTEM, "FirstLMS"] == [
            x["sourcesystem"] for x in LMSSystemActivity
        ]
        assert ["B123456", "F234567"] == [
            x["sourcesystemidentifier"] for x in LMSSystemActivity
        ]
        assert [None, None] == [x["deletedat"] for x in LMSSystemActivity]
