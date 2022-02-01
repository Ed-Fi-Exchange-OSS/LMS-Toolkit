# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
from os import environ

from typing import Iterable, Tuple
import pytest
from unittest.mock import MagicMock
from pandas import DataFrame
from sqlalchemy.engine.base import Connection, Transaction
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv

from edfi_lms_ds_loader.migrator import migrate
from edfi_lms_ds_loader.sql_lms_operations import SqlLmsOperations
from edfi_lms_ds_loader.helpers.constants import DbEngine

from edfi_sql_adapter.sql_adapter import (
    create_postgresql_adapter,
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
    parser.addoption(
        "--psql_cli",
        help="This only exists for compatibility with the LMS Harmonizer"
    )


@dataclass
class ConnectionSettings:
    host: str
    port: int
    user: str
    password: str
    db: str


Settings = None


def GetSettings(request) -> ConnectionSettings:
    global Settings

    if Settings is None:
        Settings = ConnectionSettings(
            host=request.config.getoption("--server"),
            port=request.config.getoption("--port"),
            user=request.config.getoption("--username"),
            password=request.config.getoption("--password"),
            db=request.config.getoption("--dbname")
        )

    return Settings


@pytest.fixture(scope="session")
def pgsql_connection(request) -> Iterable[Connection]:
    """
    Fixture that sets up a connection to use, and migrate the tables.
    Creates the test database if it does not yet exist.
    """
    settings = GetSettings(request)

    adapter = create_postgresql_adapter(
        settings.user, settings.password, settings.host, settings.db, settings.port
    )

    if not database_exists(adapter.engine.url):
        create_database(adapter.engine.url)

    migrate(adapter, DbEngine.POSTGRESQL)

    connection = adapter.engine.connect()
    yield connection
    connection.close()


@pytest.fixture()
def test_pgsql_db(
    pgsql_connection: Connection, request
) -> Tuple[SqlLmsOperations, Connection, ConnectionSettings]:
    """
    Fixture that takes the set-up connection and wraps in a transaction. Transaction
    will be rolled-back automatically after each test.

    Returns both a plain transaction-wrapped Connection and a monkey-patched
    SqlLmsOperations that uses that Connection. They may be used interchangeably.
    """
    # Wrap connection in transaction
    transaction: Transaction = pgsql_connection.begin()

    # Rollback transaction in finalizer when test is done
    request.addfinalizer(lambda: transaction.rollback())

    # New version of _exec using our transaction
    def replace_exec(self: SqlLmsOperations, statement: str) -> int:
        result = pgsql_connection.execute(statement)
        if result:
            return int(result.rowcount)
        return 0

    # New version of insert_into_staging using our transaction
    def replace_insert_into_staging(self: SqlLmsOperations, df: DataFrame, table: str):
        copy = df.copy()
        copy.columns = copy.columns.str.lower()
        copy.to_sql(
            f"stg_{table}",
            con=pgsql_connection,
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
    adapter.engine = DbEngine.POSTGRESQL

    return (adapter, pgsql_connection, GetSettings(request))
