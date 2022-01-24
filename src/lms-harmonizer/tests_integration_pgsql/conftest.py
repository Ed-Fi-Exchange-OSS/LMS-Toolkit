# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Iterator
from os import environ
import pytest
from tests_integration_pgsql.orchestrator import (
    delete_snapshot,
    initialize_database,
    TEMPORARY_DATABASE,
)
from tests_integration_pgsql.server_config import ServerConfig


def pytest_addoption(parser):
    """
    Injects command line options mirroring the harmonizer itself
    """
    parser.addoption(
        "--server",
        action="store",
        default=environ.get("DB_SERVER", "localhost"),
        help="Database server name or IP address",
    )
    parser.addoption(
        "--port",
        action="store",
        default=environ.get("DB_PORT", "5432"),
        help="Database server port number",
    )
    parser.addoption(
        "--dbname",
        action="store",
        default=environ.get("DB_NAME", "test_harmonizer_lms_toolkit"),
        help="Name of the test database",
    )
    parser.addoption(
        "--username",
        action="store",
        default=environ.get("DB_USER", "postgres"),
        help="Database username when not using integrated security",
    )
    parser.addoption(
        "--password",
        action="store",
        default=environ.get("PGPASSWORD", ""),
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
        type=str,
        action="store",
        default=environ.get("PSQL_CLI", "psql"),
        help="Full path to the psql command (or a shell script that invokes psql)",
    )


def _server_config_from(request) -> ServerConfig:
    return ServerConfig(
        server=request.config.getoption("--server"),
        port=request.config.getoption("--port"),
        db_name=request.config.getoption("--dbname"),
        username=request.config.getoption("--username"),
        password=request.config.getoption("--password"),
        skip_teardown=request.config.getoption("--skip-teardown"),
        psql_cli=request.config.getoption("--psql"),
    )


@pytest.fixture(scope="session")
def postgresql_db_config(request) -> Iterator[ServerConfig]:
    """
    Fixture that wraps an engine to use with snapshot
    creation and deletion
    """
    config: ServerConfig = _server_config_from(request)
    initialize_database(config)

    yield config

    delete_snapshot(config)


@pytest.fixture(autouse=True)
def test_db_config(mssql_db_config: ServerConfig, request) -> ServerConfig:
    """
    Fixture that takes the wrapped engine and passes it along, while
    providing a finalizer hook to rollback via snapshotting after each test.
    """

    # Rollback via snapshotting in finalizer when test is done
    # def finalizer():
    #     restore_snapshot(mssql_db_config)

    # if not mssql_db_config.skip_teardown:
    #     request.addfinalizer(finalizer)

    return mssql_db_config
