# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Iterator
import pytest
from tests_integration_sql.orchestrator import (
    create_snapshot,
    delete_snapshot,
    initialize_database,
    restore_snapshot,
)
from tests_integration_sql.server_config import ServerConfig


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
        "--port", action="store", default="1433", help="Database server port number"
    )
    parser.addoption(
        "--dbname",
        action="store",
        default="test_harmonizer_lms_toolkit",
        help="Name of the test database",
    )
    parser.addoption(
        "--useintegratedsecurity",
        action="store",
        default="true",
        help="Use Integrated Security for the database connection",
    )
    parser.addoption(
        "--username",
        action="store",
        default="localuser",
        help="Database username when not using integrated security",
    )
    parser.addoption(
        "--password",
        action="store",
        default="localpassword",
        help="Database user password, when not using integrated security",
    )
    parser.addoption(
        "--skip-teardown",
        type=bool,
        action="store",
        default=False,
        help="Skip the teardown of the database. Potentially useful for debugging.",
    )


def _server_config_from(request) -> ServerConfig:
    return ServerConfig(
        useintegratedsecurity=request.config.getoption("--useintegratedsecurity"),
        server=request.config.getoption("--server"),
        port=request.config.getoption("--port"),
        db_name=request.config.getoption("--dbname"),
        username=request.config.getoption("--username"),
        password=request.config.getoption("--password"),
        skip_teardown=request.config.getoption("--skip-teardown")
    )


@pytest.fixture(scope="session")
def mssql_db_config(request) -> Iterator[ServerConfig]:
    """
    Fixture that wraps an engine to use with snapshot
    creation and deletion
    """
    config: ServerConfig = _server_config_from(request)
    initialize_database(config)
    create_snapshot(config)

    yield config

    delete_snapshot(config)


@pytest.fixture(autouse=True)
def test_db_config(mssql_db_config: ServerConfig, request) -> ServerConfig:
    """
    Fixture that takes the wrapped engine and passes it along, while
    providing a finalizer hook to rollback via snapshotting after each test.
    """

    # Rollback via snapshotting in finalizer when test is done
    def finalizer():
        restore_snapshot(mssql_db_config)

    if not mssql_db_config.skip_teardown:
        request.addfinalizer(finalizer)

    return mssql_db_config
