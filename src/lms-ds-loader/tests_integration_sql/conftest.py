# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Tuple
import pytest
from unittest.mock import MagicMock
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine, Connection, Transaction

from edfi_lms_ds_loader.migrator import migrate
from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations


def _new_engine() -> Engine:
    return create_engine(
        "mssql+pyodbc://localhost,1433/test_integration_lms_toolkit?driver=ODBC+Driver+17+for+SQL+Server?Trusted_Connection=yes",
    )


@pytest.fixture(scope="session")
def connection() -> Connection:
    """
    Fixture that sets up a connection to use, and migrate the tables.
    Assumes existence of local SQLServer DB named 'test_integration_lms_toolkit'
    """
    engine = _new_engine()
    migrate(engine)

    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(autouse=True)
def test_db(connection: Connection, request) -> Tuple[MssqlLmsOperations, Connection]:
    """
    Fixture that takes the set-up connection and wraps in a transaction. Transaction
    will be rolled-back automatically after each test.

    Returns both a plain transaction-wrapped Connection and a monkey-patched
    MssqlLmsOperations that uses that Connection. They may be used interchangeably.
    """
    # Wrap connection in transaction
    transaction: Transaction = connection.begin()

    # Rollback transaction in finalizer when test is done
    request.addfinalizer(lambda: transaction.rollback())

    # New version of _exec using our transaction
    def replace_exec(self: MssqlLmsOperations, statement: str) -> int:
        result = connection.execute(statement)
        if result:
            return int(result.rowcount)
        return 0

    # New version of insert_into_staging using our transaction
    def replace_insert_into_staging(self: MssqlLmsOperations, df: DataFrame, table: str):
        df.to_sql(
            f"stg_{table}",
            con=connection,
            schema="lms",
            if_exists="append",
            index=False,
            method="multi",
            chunksize=120,
        )

    # Monkey-patch MssqlLmsOperations to use our transaction
    MssqlLmsOperations._exec = replace_exec
    MssqlLmsOperations.insert_into_staging = replace_insert_into_staging

    # Initialize monkey-patched adapter with a dummy engine, doesn't need a real one now
    adapter: MssqlLmsOperations = MssqlLmsOperations(MagicMock())

    return (adapter, connection)
