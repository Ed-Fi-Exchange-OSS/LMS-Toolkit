# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Iterable
import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine, Connection, Transaction
from tests_integration_sql.migrator_helper_mssql import (
    migrate_lms_user_and_edfi_student,
)


def _new_mssql_engine() -> Engine:
    """
    Assumes existence of local SQLServer DB named 'test_harmonizer_lms_toolkit'
    """
    return create_engine(
        "mssql+pyodbc://localhost,1433/test_harmonizer_lms_toolkit?driver=ODBC+Driver+17+for+SQL+Server?Trusted_Connection=yes",
    )


def _migrate(connection: Connection):
    # something here to initialize db structure
    # both on the LMS and ODS sides

    migrate_lms_user_and_edfi_student(connection)


@pytest.fixture(scope="session")
def mssql_connection() -> Iterable[Connection]:
    """
    Fixture that sets up a connection to use, and migrate the tables.
    """
    engine = _new_mssql_engine()

    connection = engine.connect()
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
