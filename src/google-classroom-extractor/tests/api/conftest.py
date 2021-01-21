# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from pathlib import Path
import pytest
from sqlalchemy import create_engine

DB_FILE = "tests/api/test.db"


@pytest.fixture
def test_db_fixture():
    Path(DB_FILE).unlink(missing_ok=True)
    yield create_engine(f"sqlite:///{DB_FILE}", echo=True)
