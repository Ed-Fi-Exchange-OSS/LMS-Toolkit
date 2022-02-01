# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Iterable, Tuple
from os import environ

import pytest
from dotenv import load_dotenv

from unittest.mock import MagicMock
from pandas import DataFrame
from sqlalchemy.engine.base import Connection, Transaction

from edfi_lms_ds_loader.migrator import migrate
from edfi_lms_ds_loader.sql_lms_operations import SqlLmsOperations

from edfi_sql_adapter.sql_adapter import (
    Adapter,
    create_mssql_adapter_with_integrated_security,
    create_mssql_adapter,
)

load_dotenv()


def pytest_addoption(parser):
    """
    Injects command line options mirroring the harmonizer itself
    """
    parser.addoption(
        "--server",
        action="store",
        default="localhost",
        help="Database server name or IP address",
    )
    parser.addoption(
        "--port",
        action="store",
        default=environ.get("DB_PORT", 1433),
        help="Database server port number",
    )
    parser.addoption(
        "--dbname",
        action="store",
        default=environ.get("DB_NAME", "test_integration_lms_toolkit"),
        help="Name of the test database",
    )
    parser.addoption(
        "--useintegratedsecurity",
        type=bool,
        action="store",
        default=environ.get("USE_INTEGRATED_SECURITY", True),
        help="Use Integrated Security for the database connection",
    )
    parser.addoption(
        "--username",
        action="store",
        default=environ.get("DB_USER", "sa"),
        help="Database username when not using integrated security",
    )
    parser.addoption(
        "--password",
        action="store",
        default=environ.get("DB_PASSWORD", ""),
        help="Database user password, when not using integrated security",
    )
    parser.addoption(
        "--skip-teardown",
        type=bool,
        action="store",
        default=environ.get("SKIP_TEARDOWN", False),
        help="Skip the teardown of the database. Potentially useful for debugging.",
    )


def _new_mssql_adapter(request) -> Adapter:
    use_integrated_security = request.config.getoption("--useintegratedsecurity")
    server = request.config.getoption("--server")
    port = request.config.getoption("--port")
    db_name = request.config.getoption("--dbname")
    username = request.config.getoption("--username")
    password = request.config.getoption("--password")

    if use_integrated_security is True:
        return create_mssql_adapter_with_integrated_security(
            server, db_name, port, False, False
        )

    return create_mssql_adapter(username, password, server, db_name, port)


@pytest.fixture(scope="session")
def mssql_connection(request) -> Iterable[Connection]:
    """
    Fixture that sets up a connection to use, and migrate the tables.
    Assumes existence of local SQLServer DB named 'test_integration_lms_toolkit'
    """
    adapter = _new_mssql_adapter(request)
    migrate(adapter)

    connection = adapter.engine.connect()
    yield connection
    connection.close()


@pytest.fixture(autouse=True)
def test_mssql_db(
    mssql_connection: Connection, request
) -> Tuple[SqlLmsOperations, Connection]:
    """
    Fixture that takes the set-up connection and wraps in a transaction. Transaction
    will be rolled-back automatically after each test.

    Returns both a plain transaction-wrapped Connection and a monkey-patched
    SqlLmsOperations that uses that Connection. They may be used interchangeably.
    """
    # Wrap connection in transaction
    transaction: Transaction = mssql_connection.begin()

    # Rollback transaction in finalizer when test is done
    request.addfinalizer(lambda: transaction.rollback())

    # New version of _exec using our transaction
    def replace_exec(self: SqlLmsOperations, statement: str) -> int:
        result = mssql_connection.execute(statement)
        if result:
            return int(result.rowcount)
        return 0

    # New version of insert_into_staging using our transaction
    def replace_insert_into_staging(self: SqlLmsOperations, df: DataFrame, table: str):
        df.to_sql(
            f"stg_{table}",
            con=mssql_connection,
            schema="lms",
            if_exists="append",
            index=False,
            method="multi",
            chunksize=120,
        )

    # Monkey-patch SqlLmsOperations to use our transaction
    SqlLmsOperations._exec = replace_exec  # type:ignore
    SqlLmsOperations.insert_into_staging = replace_insert_into_staging  # type:ignore

    # Initialize monkey-patched adapter with a dummy engine, doesn't need a real one now
    adapter: SqlLmsOperations = SqlLmsOperations(MagicMock())

    return (adapter, mssql_connection)
