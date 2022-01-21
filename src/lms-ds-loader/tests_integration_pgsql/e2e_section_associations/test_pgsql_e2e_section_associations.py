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
    main_arguments,
    insert_user_section_association
)

CSV_PATH = "tests_integration_sql/e2e_section_associations/data"
SOURCE_SYSTEM = "BestLMS"


def describe_when_a_record_is_missing_in_the_csv():
    def it_should_soft_delete_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection]
    ):
        adapter, connection = test_pgsql_db

        # arrange - note csv file has only B123456
        user_identifier = 10
        insert_user(connection, "U123456", SOURCE_SYSTEM, user_identifier)
        section_identifier = 10
        insert_section(connection, "B098765", SOURCE_SYSTEM, section_identifier)

        insert_user_section_association(connection, "B123456", SOURCE_SYSTEM, 10, user_identifier, section_identifier)
        insert_user_section_association(connection, "B234567", SOURCE_SYSTEM, 11, user_identifier, section_identifier)

        # act
        run_loader(main_arguments(adapter, CSV_PATH))

        # assert - B234567 has been soft deleted
        LMSUserLMSSectionAssociation = connection.execute(
            "select sourcesystemidentifier from lms.lmsuserlmssectionassociation where deletedat is not null"
        ).fetchall()
        assert len(LMSUserLMSSectionAssociation) == 1
        assert LMSUserLMSSectionAssociation[0]["sourcesystemidentifier"] == "B234567"


def describe_when_a_record_is_from_one_source_system_of_two_in_the_csv():
    def it_should_match_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection]
    ):
        adapter, connection = test_pgsql_db
        user_identifier_1 = 10
        insert_user(connection, "U123456", SOURCE_SYSTEM, user_identifier_1)
        user_identifier_2 = 11
        insert_user(connection, "U123456", "FirstLMS", user_identifier_2)

        section_identifier_1 = 10
        insert_section(connection, "B098765", SOURCE_SYSTEM, section_identifier_1)
        section_identifier_2 = 11
        insert_section(connection, "F098765", "FirstLMS", section_identifier_2)

        insert_user_section_association(connection, "B123456", SOURCE_SYSTEM, 11, user_identifier_1, section_identifier_1)
        insert_user_section_association(connection, "F234567", "FirstLMS", 12, user_identifier_2, section_identifier_2)

        # act
        run_loader(main_arguments(adapter, CSV_PATH))

        # assert - records are unchanged
        LMSUserLMSSectionAssociation = connection.execute(
            "select sourcesystem, sourcesystemidentifier, deletedat from lms.lmsuserlmssectionassociation order by sourcesystemidentifier"
        ).fetchall()
        assert len(LMSUserLMSSectionAssociation) == 2
        assert [SOURCE_SYSTEM, "FirstLMS"] == [
            x["sourcesystem"] for x in LMSUserLMSSectionAssociation
        ]
        assert ["B123456", "F234567"] == [
            x["sourcesystemidentifier"] for x in LMSUserLMSSectionAssociation
        ]
        assert [None, None] == [x["deletedat"] for x in LMSUserLMSSectionAssociation]


def describe_when_a_record_is_from_one_source_system_in_the_csv():
    def it_should_match_the_record(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection]
    ):
        adapter, connection = test_pgsql_db
        user_identifier = 10
        insert_user(connection, "U123456", SOURCE_SYSTEM, user_identifier)

        section_identifier_1 = 11
        insert_section(connection, "B098765", SOURCE_SYSTEM, section_identifier_1)
        section_identifier_2 = 12
        insert_section(connection, "B109876", SOURCE_SYSTEM, section_identifier_2)

        insert_user_section_association(connection, "B123456", SOURCE_SYSTEM, 11, user_identifier, section_identifier_1)
        insert_user_section_association(connection, "B234567", SOURCE_SYSTEM, 12, user_identifier, section_identifier_2)

        # act
        run_loader(main_arguments(adapter, CSV_PATH))

        # assert - records are unchanged
        LMSUserLMSSectionAssociation = connection.execute(
            "select sourcesystem, sourcesystemidentifier, deletedat from lms.lmsuserlmssectionassociation order by sourcesystemidentifier"
        ).fetchall()
        assert len(LMSUserLMSSectionAssociation) == 2
        assert [SOURCE_SYSTEM, SOURCE_SYSTEM] == [
            x["sourcesystem"] for x in LMSUserLMSSectionAssociation
        ]
        assert ["B123456", "B234567"] == [
            x["sourcesystemidentifier"] for x in LMSUserLMSSectionAssociation
        ]
        assert [None, None] == [x["deletedat"] for x in LMSUserLMSSectionAssociation]
