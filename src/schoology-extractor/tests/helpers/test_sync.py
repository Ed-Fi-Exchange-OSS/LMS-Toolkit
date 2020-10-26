# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
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
        assert isinstance(
            engine,
            sqlalchemy.engine.base.Engine
        )


class Test_when__get_current_date_with_format_is_called:
    def test_then_date_is_returned_in_right_format(self):
        date_with_format = sync._get_current_date_with_format()

        # If wrong format is returned, exception is thrown
        datetime.strptime(date_with_format, "%Y-%m-%d %H:%M:%S")


class Test_when__table_exist_is_called:
    class Test_given_table_does_not_exist():
        def test_then_returns_false(self, db_engine_mock_returns_none):
            result = sync._table_exist("fake_table_name", db_engine_mock_returns_none)
            assert result is False

    class Test_given_table_exists():
        def test_then_returns_true(self, db_engine_mock_returns_value):
            result = sync._table_exist("fake_table_name", db_engine_mock_returns_value)
            assert result is True


class Test_when__remove_duplicates_is_called:
    class Test_given_db_execute_method_is_called():
        def test_then_query_is_built_correctly(self, db_engine_mock_returns_value):
            sync._remove_duplicates(
                "fake_table_name",
                db_engine_mock_returns_value,
                "fake_column_id")

            query = "DELETE from fake_table_name WHERE rowid not in (select max(rowid) FROM fake_table_name GROUP BY fake_column_id)"

            db_engine_mock_returns_value.connect().__enter__().execute.assert_called_with(query)


class Test_when__get_created_date_is_called:
    class Test_given_db_execute_method_is_called():
        def test_then_query_is_built_correctly(self, db_engine_mock_returns_value):
            sync._remove_duplicates(
                "fake_table_name",
                db_engine_mock_returns_value,
                "fake_column_id")

            query = "DELETE from fake_table_name WHERE rowid not in (select max(rowid) FROM fake_table_name GROUP BY fake_column_id)"

            db_engine_mock_returns_value.connect().__enter__().execute.assert_called_with(query)
