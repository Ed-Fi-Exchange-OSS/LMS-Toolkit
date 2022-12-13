# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import json
import pytest

from pathlib import Path
from sqlalchemy import create_engine

from edfi_canvas_extractor.graphql.extractor import GraphQLExtractor

MOCK_CANVAS_BASE_URL = "https://example.com"
MOCK_CANVAS_ACCESS_TOKEN = "1234567890"
DB_FILE = "tests/graphql/test.db"
START_DATE = "2021-01-01"
END_DATE = "2030-01-01"


@pytest.fixture(scope="session")
def gql(api):
    gql = GraphQLExtractor(
        MOCK_CANVAS_BASE_URL,
        MOCK_CANVAS_ACCESS_TOKEN,
        "1",
        START_DATE,
        END_DATE,
        )
    gql.extract(api)
    yield gql


@pytest.fixture(scope="session")
def api():
    with open('tests/graphql/sample-data.json', mode='r') as f:
        data = json.loads(f.read())

    return data


@pytest.fixture(scope="session")
def test_db_fixture():
    Path(DB_FILE).unlink(missing_ok=True)
    yield create_engine(f"sqlite:///{DB_FILE}", echo=True)
    # Path(DB_FILE).unlink(missing_ok=True)
