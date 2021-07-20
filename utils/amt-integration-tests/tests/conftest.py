# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Iterator

from _pytest.config.argparsing import Parser
import pytest
from sqlalchemy import create_engine, engine

from .data_helpers import load_lms_descriptors

from .ServerConfig import ServerConfig
from .db_prep import (
    drop_database,
    install_ds32_database,
    install_analytics_middle_tier,
    install_lmsx_extension,
)


def pytest_addoption(parser: Parser) -> None:
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
        default="test_analytics_middle_tier_engage",
        help="Name of the test database",
    )
    parser.addoption(
        "--useintegratedsecurity",
        action="store",
        default=True,
        help="Use Integrated Security for the database connection",
    )
    parser.addoption(
        "--username",
        action="store",
        help="Database username when not using integrated security",
    )
    parser.addoption(
        "--password",
        action="store",
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
        skip_teardown=request.config.getoption("--skip-teardown"),
    )


@pytest.fixture(scope="session")
def mssql_fixture(request) -> Iterator[engine.base.Engine]:
    config = _server_config_from(request)

    # Warning - do not change the order of operations below
    drop_database(config)
    install_ds32_database(config)
    install_lmsx_extension(config)

    engine = create_engine(config.get_pyodbc_connection_string())
    load_lms_descriptors(engine)

    install_analytics_middle_tier(config)

    yield engine

    if config.teardown_enabled():
        drop_database(config)
