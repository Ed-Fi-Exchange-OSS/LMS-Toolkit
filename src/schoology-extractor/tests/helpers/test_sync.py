# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from pandas.core.frame import DataFrame
import pytest
from unittest.mock import Mock
import sqlalchemy
from schoology_extractor.helpers import sync


@pytest.fixture
def db_engine_mock_returns_none():
    execute_mock = Mock()
    execute_mock.execute.return_value = None

    mock_connection = Mock()
    mock_connection.__enter__ = Mock(return_value=execute_mock)
    mock_connection.__exit__ = Mock()

    mock_db_engine = Mock()
    mock_db_engine.connect.return_value = mock_connection
    return mock_db_engine


@pytest.fixture
def db_engine_mock_returns_value():
    execute_mock = Mock()
    execute_mock.execute.return_value = Mock()

    mock_connection = Mock()
    mock_connection.__enter__ = Mock(return_value=execute_mock)
    mock_connection.__exit__ = Mock()

    mock_db_engine = Mock()
    mock_db_engine.connect.return_value = mock_connection
    return mock_db_engine


class Test_when_get_sync_db_engine_is_called:
    def test_then_engine_type_object_is_returned(self):
        engine = sync.get_sync_db_engine()
        assert isinstance(engine, sqlalchemy.engine.base.Engine)


class Test_when__table_exist_is_called:
    class Test_given_table_does_not_exist:
        def test_then_returns_false(self, db_engine_mock_returns_none):
            result = sync._table_exist("fake_table_name", db_engine_mock_returns_none)
            assert result is False

    class Test_given_table_exists:
        def test_then_returns_true(self, db_engine_mock_returns_value):
            result = sync._table_exist("fake_table_name", db_engine_mock_returns_value)
            assert result is True


@pytest.fixture
def db_engine_mock_returns_fake_resource():
    row = Mock()
    row.items.return_value = [
        (
            "JsonResponse",
            r"""{
                "id": 1,
                "name": "fake_name"
            }""",
        )
    ]
    execute_mock = Mock()
    execute_mock.execute.return_value = [row]

    mock_connection = Mock()
    mock_connection.__enter__ = Mock(return_value=execute_mock)
    mock_connection.__exit__ = Mock()

    mock_db_engine = Mock()
    mock_db_engine.connect.return_value = mock_connection
    return mock_db_engine


def mock_sync_internal_functions(sync):
    sync._table_exist = Mock(return_value=True)


class Test_given_sync_resource_is_called:
    def test_then_returns_dataframe(self, db_engine_mock_returns_none):
        mock_sync_internal_functions(sync)
        result = sync.sync_resource(
            "fake_resource_name",
            db_engine_mock_returns_none,
            [
                {"fake_column": "fake_value", "id": "fake_id"},
                {"fake_column": "fake_value", "id": "fake_id"},
            ],
        )
        assert isinstance(result, DataFrame)


@pytest.fixture
def db_engine_mock_returns_existing_file():
    execute_mock = Mock()
    execute_mock.execute.return_value = {"exists": 1}

    mock_connection = Mock()
    mock_connection.__enter__ = Mock(return_value=execute_mock)
    mock_connection.__exit__ = Mock()

    mock_db_engine = Mock()
    mock_db_engine.connect.return_value = mock_connection
    return mock_db_engine


class Test_given_usage_file_is_processed_is_called:
    def test_then_returns_boolean(self, db_engine_mock_returns_existing_file):
        mock_sync_internal_functions(sync)
        result = sync.usage_file_is_processed(
            "fake_resource_name", db_engine_mock_returns_existing_file
        )
        assert isinstance(result, bool)

    class Test_given_db_returns_false:
        def test_then_returns_false(self, db_engine_mock_returns_existing_file):
            mock_sync_internal_functions(sync)
            result = sync.usage_file_is_processed(
                "fake_resource_name", db_engine_mock_returns_existing_file
            )
            assert result is False
