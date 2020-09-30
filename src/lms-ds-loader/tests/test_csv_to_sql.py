# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
from unittest.mock import Mock

import pandas as pd
import sqlalchemy as sal

from lms_ds_loader.csv_to_sql import CsvToSql


class Test_when_reading_csv_and_loading_into_a_database:
    class Test_given_invalid_arguments:
        def test_given_file_is_none_then_raise_error(self):
            with pytest.raises(AssertionError):
                CsvToSql(Mock()).load_file(None, "a", ["a"])

        def test_given_file_does_not_exist_then_raise_error(self, fs):
            with pytest.raises(OSError):
                CsvToSql(Mock()).load_file("does/not/exist", "a", ["a"])

        def test_given_table_is_none_then_raise_error(self, fs):
            file = "d"
            fs.create_file(file)

            with pytest.raises(AssertionError):
                CsvToSql(Mock()).load_file(file, None, ["a"])

        def test_given_columns_is_none_then_raise_error(self, fs):
            file = "d"
            fs.create_file(file)

            with pytest.raises(AssertionError):
                CsvToSql(Mock()).load_file(file, "a", None)

        def test_given_columns_is_an_empty_list_then_raise_error(self, fs):
            file = "d"
            fs.create_file(file)

            with pytest.raises(AssertionError):
                CsvToSql(Mock()).load_file(file, "a", [])

    class Test_given_valid_arguments:
        def test_then_load_file_into_specified_table_using_pandas(self, mocker, fs):
            adapter = Mock()
            file = "a/b/c.csv"
            table = "c"
            columns = ["A"]

            # Arrange
            fs.create_file(file)
            read_csv_mock = mocker.patch.object(pd, "read_csv")

            # Act
            csv_to_sql = CsvToSql(adapter)
            csv_to_sql.load_file(file, table, columns)

            # Assert
            read_csv_mock.assert_called_with(file)
            adapter.disable_staging_natural_key_index.assert_called_with(table)
            adapter.truncate_staging_table.assert_called_with(table)
            adapter.enable_staging_natural_key_index.assert_called_with(table)
            adapter.insert_into_staging.assert_called_with(
                read_csv_mock.return_value, table
            )
            adapter.insert_new_records_to_production.assert_called_with(table, columns)
            adapter.copy_updates_to_production.assert_called_with(table, columns)
