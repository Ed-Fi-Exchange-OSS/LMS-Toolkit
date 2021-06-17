# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from edfi_sql_adapter import sql_adapter


def describe_when_creating_mssql_engine() -> None:
    def describe_given_username_and_password() -> None:
        def it_should_create_an_engine_with_proper_connection_string() -> None:
            expected_connection_string = (
                "mssql+pyodbc://a:b@c,1/d?driver=ODBC+Driver+17+for+SQL+Server"
            )

            actual = sql_adapter.create_mssql_adapter("a", "b", "c", "d", 1)

            assert str(actual.engine.url) == expected_connection_string

    def describe_using_integrated_security() -> None:
        def it_should_create_an_engine_with_proper_connection_string() -> None:
            expected_connection_string = (
                "mssql+pyodbc://c,1/d?driver=ODBC+Driver+17+for+SQL+Server"
            )

            actual = sql_adapter.create_mssql_adapter_with_integrated_security(
                "c", "d", 1
            )
            assert str(actual.engine.url) == expected_connection_string


def describe_when_creating_postgresql_engine() -> None:
    def describe_given_username_and_password() -> None:
        def it_should_create_an_engine_with_proper_connection_string() -> None:
            expected_connection_string = "postgresql://a:b@c:1/d"

            actual = sql_adapter.create_postgresql_adapter("a", "b", "c", "d", 1)

            assert str(actual.engine.url) == expected_connection_string
