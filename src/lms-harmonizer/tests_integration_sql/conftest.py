# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Iterable
import pytest
from sqlalchemy.engine.base import Engine, Connection, Transaction
from edfi_sql_adapter import sql_adapter
from tests_integration_sql.migrator_helper_mssql import (
    migrate_lms_user_and_edfi_student,
)


def pytest_addoption(parser):
    """
    Injects command line options mirroring the harmonizer itself
    """
    parser.addoption(
        "--server", action="store", default="localhost", help="Database server name or IP address"
    )
    parser.addoption(
        "--port", action="store", default="1433", help="Database server port number"
    )
    parser.addoption(
        "--dbname", action="store", default="test_harmonizer_lms_toolkit", help="Name of the test database"
    )
    parser.addoption(
        "--useintegratedsecurity", action="store", default="true", help="Use Integrated Security for the database connection"
    )
    parser.addoption(
        "--username", action="store", default="localuser", help="Database username when not using integrated security"
    )
    parser.addoption(
        "--password", action="store", default="localpassword", help="Database user password, when not using integrated security"
    )


@pytest.fixture(scope="session")
def mssql_engine(request) -> Engine:
    """
    Reads from injected command line options mirroring the harmonizer itself
    """
    useintegratedsecurity: str = request.config.getoption("--useintegratedsecurity")
    server: str = request.config.getoption("--server")
    port: str = request.config.getoption("--port")
    db_name: str = request.config.getoption("--dbname")

    if useintegratedsecurity == "true":
        return sql_adapter.create_mssql_adapter_with_integrated_security(
            server, db_name, int(port)
        ).engine
    else:
        username: str = request.config.getoption("--username")
        password: str = request.config.getoption("--password")
        return sql_adapter.create_mssql_adapter(
            username, password, server, db_name, int(port)
        ).engine


def _migrate(connection: Connection):
    migrate_lms_user_and_edfi_student(connection)


@pytest.fixture(scope="session")
def mssql_connection(mssql_engine) -> Iterable[Connection]:
    """
    Fixture that sets up a connection to use
    """
    connection = mssql_engine.connect()
    yield connection
    connection.close()


@pytest.fixture(autouse=True)
def test_mssql_db(mssql_connection: Connection, request) -> Connection:
    """
    Fixture that takes the set-up connection and wraps in a transaction. Transaction
    will be rolled-back automatically after each test.

    Returns both a plain transaction-wrapped Connection and a monkey-patched
    MssqlLmsOperations that uses that Connection. They may be used interchangeably.
    """
    # Wrap connection in transaction
    transaction: Transaction = mssql_connection.begin()

    _migrate(mssql_connection)

    # Rollback transaction in finalizer when test is done
    request.addfinalizer(lambda: transaction.rollback())

    return mssql_connection
