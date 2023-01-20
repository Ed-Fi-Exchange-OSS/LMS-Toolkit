# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import json
import os
import pytest

from pathlib import Path
from sqlalchemy import create_engine

from edfi_canvas_extractor.graphql.extractor import GraphQLExtractor

MOCK_CANVAS_BASE_URL = "https://example.com"
MOCK_CANVAS_ACCESS_TOKEN = "1234567890"
DB_FILE = "tests/graphql/unit/test.db"
START_DATE = "2021-01-01"
END_DATE = "2030-01-01"


@pytest.fixture(scope="session")
def read_data():
    '''
    Returns the data converted from json file
    '''
    with open('tests/graphql/unit/sample-data.json', mode='r') as f:
        data = json.loads(f.read())

    return data


@pytest.fixture(scope="session")
def mock_gql(read_data):
    '''
    Returns the GraphQLExtractor object with the sample data.

    Parameters
    -----------
    read_data String with the query
    '''
    gql = GraphQLExtractor(
        MOCK_CANVAS_BASE_URL,
        MOCK_CANVAS_ACCESS_TOKEN,
        "1",
        START_DATE,
        END_DATE,
        )
    gql.extract(read_data)

    yield gql


@pytest.fixture(scope="class")
def gql():
    CANVAS_BASE_URL = os.environ['CANVAS_BASE_URL']
    CANVAS_ACCESS_TOKEN = os.environ['CANVAS_ACCESS_TOKEN']
    START_DATE = "2021-01-01"
    END_DATE = "2030-01-01"

    gql = GraphQLExtractor(
        CANVAS_BASE_URL,
        CANVAS_ACCESS_TOKEN,
        "1",
        START_DATE,
        END_DATE,
        )
    gql.run()

    yield gql


@pytest.fixture(scope="session")
def test_db_fixture():
    Path(DB_FILE).unlink(missing_ok=True)
    captureSqlAlchemyLogs = (os.getenv('LOG_LEVEL') or '').lower() == "debug"
    yield create_engine(f"sqlite:///{DB_FILE}", echo=captureSqlAlchemyLogs)
    # Path(DB_FILE).unlink(missing_ok=True)


def pytest_configure(config):
    # register your new marker to avoid warnings
    config.addinivalue_line(
        "markers",
        "unit: mark a test as a unit test.",
    )
    config.addinivalue_line(
        "markers",
        "integration: mark a test as a integration test.",
    )
