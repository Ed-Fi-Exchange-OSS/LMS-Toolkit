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
    insert_user,
    insert_user_section_association,
    main_arguments,
)
from tests_integration_pgsql.conftest import ConnectionSettings

CSV_PATH = "tests_integration_mssql/e2e_attendance/data"
SOURCE_SYSTEM = "BestLMS"


def insert_record(
    connection: Connection,
    ss_identifier: str,
    source_system: str,
    section_identifier: int,
    user_identifier: int,
    user_section_association_identifier: int,
):
    connection.execute(
        f"""
    insert into lms.lmsuserattendanceevent
           (sourcesystemidentifier
           ,sourcesystem
           ,lmsuseridentifier
           ,lmssectionidentifier
           ,lmsuserlmssectionassociationidentifier
           ,eventdate
           ,attendancestatus
           ,sourcecreatedate
           ,sourcelastmodifieddate
           ,deletedat
           ,createdate
           ,lastmodifieddate)
     values
           ('{ss_identifier}'
           ,'{source_system}'
           ,'{user_identifier}'
           ,'{section_identifier}'
           ,'{user_section_association_identifier}'
           ,'2021-01-01 00:00:00'
           ,'active'
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
        insert_section(connection, "B098765", SOURCE_SYSTEM, 1)
        insert_user_section_association(connection, "UB123456", SOURCE_SYSTEM, 1, 1, 1)

        insert_record(connection, "B123456", SOURCE_SYSTEM, 1, 1, 1)
        insert_record(connection, "B234567", SOURCE_SYSTEM, 1, 1, 1)

        # act
        run_loader(main_arguments(adapter, CSV_PATH, settings))

        # assert - B234567 has been soft deleted
        LMSUserAttendanceEvent = connection.execute(
            "select sourcesystemidentifier from lms.lmsuserattendanceevent where deletedat is not null"
        ).fetchall()
        assert len(LMSUserAttendanceEvent) == 1
        assert LMSUserAttendanceEvent[0]["sourcesystemidentifier"] == "B234567"


def describe_when_a_record_is_from_one_source_system_of_two_in_the_csv():
    def it_should_match_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection, ConnectionSettings]
    ):
        adapter, connection, settings = test_pgsql_db
        insert_user(connection, "U123456", SOURCE_SYSTEM, 1)
        insert_user(connection, "U123456", "FirstLMS", 2)

        insert_section(connection, "B098765", SOURCE_SYSTEM, 1)
        insert_section(connection, "F098765", "FirstLMS", 2)

        insert_user_section_association(connection, "UB123456", SOURCE_SYSTEM, 1, 1, 1)
        insert_user_section_association(connection, "UF123456", SOURCE_SYSTEM, 2, 2, 2)

        insert_record(connection, "B123456", SOURCE_SYSTEM, 1, 1, 1)
        insert_record(connection, "F234567", "FirstLMS", 2, 2, 2)

        # act
        run_loader(main_arguments(adapter, CSV_PATH, settings))

        # assert - records are unchanged
        LMSUserAttendanceEvent = connection.execute(
            "select sourcesystem, sourcesystemidentifier, deletedat from lms.lmsuserattendanceevent order by sourcesystemidentifier"
        ).fetchall()
        assert len(LMSUserAttendanceEvent) == 2
        assert [SOURCE_SYSTEM, "FirstLMS"] == [
            x["sourcesystem"] for x in LMSUserAttendanceEvent
        ]
        assert ["B123456", "F234567"] == [
            x["sourcesystemidentifier"] for x in LMSUserAttendanceEvent
        ]
        assert [None, None] == [x["deletedat"] for x in LMSUserAttendanceEvent]


def describe_when_a_record_is_from_one_source_system_in_the_csv():
    def it_should_match_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection, ConnectionSettings]
    ):
        adapter, connection, settings = test_pgsql_db
        insert_user(connection, "U123456", SOURCE_SYSTEM, 1)

        insert_section(connection, "B098765", SOURCE_SYSTEM, 1)
        insert_section(connection, "B109876", SOURCE_SYSTEM, 2)

        insert_user_section_association(connection, "UB098765", SOURCE_SYSTEM, 1, 1, 1)
        insert_user_section_association(connection, "UF109876", SOURCE_SYSTEM, 2, 1, 2)

        insert_record(connection, "B123456", SOURCE_SYSTEM, 1, 1, 1)
        insert_record(connection, "B234567", SOURCE_SYSTEM, 2, 1, 2)

        # act
        run_loader(main_arguments(adapter, CSV_PATH, settings))

        # assert - records are unchanged
        LMSUserAttendanceEvent = connection.execute(
            "select sourcesystem, sourcesystemidentifier, deletedat from lms.lmsuserattendanceevent order by sourcesystemidentifier"
        ).fetchall()
        assert len(LMSUserAttendanceEvent) == 2
        assert [SOURCE_SYSTEM, SOURCE_SYSTEM] == [
            x["sourcesystem"] for x in LMSUserAttendanceEvent
        ]
        assert ["B123456", "B234567"] == [
            x["sourcesystemidentifier"] for x in LMSUserAttendanceEvent
        ]
        assert [None, None] == [x["deletedat"] for x in LMSUserAttendanceEvent]
