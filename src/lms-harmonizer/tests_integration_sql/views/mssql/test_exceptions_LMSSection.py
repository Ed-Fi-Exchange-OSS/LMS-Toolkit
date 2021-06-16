# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from sqlalchemy.engine.base import Connection
from tests_integration_sql.mssql_helper import (
    insert_lms_section,
    script_sql,
    insert_edfi_section,
    manually_set_lmssection_edfisectionid,
)

SOURCE_SYSTEM = "Canvas"
VIEW_SQL_DEFINITION = script_sql("1040-view-exceptions_LMSSection.sql")


def describe_given_there_is_one_unmatched_user() -> None:
    SECTION_ID = "10000000-0000-0000-0000-000000000000"
    SIS_ID = "sis_id"

    def describe_when_querying_for_user_exceptions() -> None:
        def it_should_return_that_one_user(test_mssql_db: Connection) -> None:
            # Arrange

            test_mssql_db.execute(VIEW_SQL_DEFINITION)
            insert_lms_section(test_mssql_db, SIS_ID, SOURCE_SYSTEM)
            insert_edfi_section(test_mssql_db, SIS_ID, SECTION_ID)

            # Act
            results = test_mssql_db.execute(
                "SELECT COUNT(1) FROM edfilms.exceptions_LMSSection"
            )

            # Assert
            results.first()[0] == 1


def describe_given_there_are_no_unmatched_users() -> None:
    SECTION_ID = "10000000-0000-0000-0000-000000000000"
    SIS_ID = "sis_id"

    def describe_when_querying_for_user_exceptions() -> None:
        def it_should_return__no_records(test_mssql_db: Connection) -> None:
            # Arrange

            test_mssql_db.execute(VIEW_SQL_DEFINITION)
            insert_lms_section(test_mssql_db, SIS_ID, SOURCE_SYSTEM)
            insert_edfi_section(test_mssql_db, SIS_ID, SECTION_ID)
            manually_set_lmssection_edfisectionid(test_mssql_db, SIS_ID, SECTION_ID)

            # Act
            results = test_mssql_db.execute(
                "SELECT COUNT(1) FROM edfilms.exceptions_LMSSection"
            )

            # Assert
            assert results.first()[0] == 0
