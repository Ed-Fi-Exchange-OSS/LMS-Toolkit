# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import dotenv
import json
import pytest

from pathlib import Path
from sqlalchemy import create_engine

from edfi_canvas_extractor.graphql.extractor import GraphQLExtractor


DB_FILE = "tests/graphql/test.db"


@pytest.fixture
def gql_run():
    config = dotenv.dotenv_values()

    gql = GraphQLExtractor(
        str(config["CANVAS_BASE_URL"]),
        str(config["CANVAS_ACCESS_TOKEN"]),
        "1",
        config["START_DATE"],
        config["END_DATE"],
        )
    gql.run()
    yield gql


@pytest.fixture
def gql_no_run():
    config = dotenv.dotenv_values()

    gql = GraphQLExtractor(
        str(config["CANVAS_BASE_URL"]),
        str(config["CANVAS_ACCESS_TOKEN"]),
        "1",
        config["START_DATE"],
        config["END_DATE"],
        )
    yield gql


@pytest.fixture
def api():
    with open('tests/graphql/sample.json', mode='r') as f:
        data = json.loads(f.read())

    return data


@pytest.fixture
def test_db_fixture():
    Path(DB_FILE).unlink(missing_ok=True)
    yield create_engine(f"sqlite:///{DB_FILE}", echo=True)
    # Path(DB_FILE).unlink(missing_ok=True)
