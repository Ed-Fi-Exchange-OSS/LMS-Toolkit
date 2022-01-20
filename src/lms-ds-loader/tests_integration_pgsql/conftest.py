# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
from os import environ
import string

from typing import Iterable, Tuple, Optional
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
    Adapter,
    create_postgresql_adapter,
)


load_dotenv()


def _get_env_string(key: str, default: Optional[str] = None) -> str:
    value = environ.get(key)
    if value is None:
        if default is None:
            raise RuntimeError(
                f"Environment variable {key} is not set and there is no default value."
            )
        return default

    return value


def _get_env_int(key: str, default: Optional[int]) -> int:
    value = _get_env_string(key, str(default))

    if not value.isdigit():
        raise RuntimeError(
            f"Invalid value {value} for environment variable {key}, which should be a number."
        )

    return int(value)


@dataclass
class ConnectionSettings:
    host: str
    port: int
    user: str
    password: str
    db: str


Settings = ConnectionSettings(
    _get_env_string("PGSQL_HOST", "localhost"),
    _get_env_int("PGSQL_PORT", 5432),
    _get_env_string("PGSQL_USER", "postgres"),
    _get_env_string("PGSQL_PASSWORD"),
    _get_env_string("DB_NAME", "postgres"),
)


@pytest.fixture(scope="session")
def pgsql_connection() -> Iterable[Connection]:
    """
    Fixture that sets up a connection to use, and migrate the tables.
    Creates the test database if it does not yet exist.
    """
    adapter = create_postgresql_adapter(
        Settings.user, Settings.password, Settings.host, Settings.db, Settings.port
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
) -> Tuple[SqlLmsOperations, Connection]:
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
        df.to_sql(
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

    return (adapter, pgsql_connection)
