# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from sqlalchemy.engine.base import Connection
from tests_integration_sql.mssql_helper import (
    insert_lms_user,
    script_sql,
    insert_edfi_student,
    manually_set_lmsuser_edfistudentid,
)

SOURCE_SYSTEM = "Canvas"
VIEW_SQL_DEFINITION = script_sql("1070-view-exceptions_LMSUser.sql")


def describe_given_there_is_one_unmatched_user() -> None:
    STUDENT_ID = "10000000-0000-0000-0000-000000000000"
    SIS_ID = "sis_id"

    def describe_when_querying_for_user_exceptions() -> None:
        def it_should_return_that_one_user(test_mssql_db: Connection) -> None:
            # Arrange

            test_mssql_db.execute(VIEW_SQL_DEFINITION)
            insert_lms_user(test_mssql_db, SIS_ID, SOURCE_SYSTEM)
            insert_edfi_student(test_mssql_db, SIS_ID, STUDENT_ID)

            # Act
            results = test_mssql_db.execute(
                "SELECT COUNT(1) FROM LMSX.exceptions_LMSUser"
            )

            # Assert
            results.first()[0] == 1


def describe_given_there_are_no_unmatched_users() -> None:
    STUDENT_ID = "10000000-0000-0000-0000-000000000000"
    SIS_ID = "sis_id"

    def describe_when_querying_for_user_exceptions() -> None:
        def it_should_return__no_records(test_mssql_db: Connection) -> None:
            # Arrange

            test_mssql_db.execute(VIEW_SQL_DEFINITION)
            insert_lms_user(test_mssql_db, SIS_ID, SOURCE_SYSTEM)
            insert_edfi_student(test_mssql_db, SIS_ID, STUDENT_ID)
            manually_set_lmsuser_edfistudentid(test_mssql_db, SIS_ID, STUDENT_ID)

            # Act
            results = test_mssql_db.execute(
                "SELECT COUNT(1) FROM LMSX.exceptions_LMSUser"
            )

            # Assert
            assert results.first()[0] == 0
