# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

import edfi_sql_adapter.sql_adapter as sql_adapter


def describe_given_sql_server_on_localhost() -> None:
    def describe_given_integrated_security() -> None:
        def describe_when_executing_a_simple_statement() -> None:
            def it_should_not_throw_an_error() -> None:
                adapter = sql_adapter.create_mssql_adapter_with_integrated_security("localhost", "master")
                adapter.execute([sql_adapter.Statement("SELECT 1/1", "info message")])

        def describe_when_executing_a_statement_with_an_error() -> None:
            def it_should_raise_an_error() -> None:
                with pytest.raises(Exception):
                    adapter = sql_adapter.create_mssql_adapter_with_integrated_security("localhost", "master")
                    adapter.execute([sql_adapter.Statement("SELECT 1/0", "divide by zero")])
