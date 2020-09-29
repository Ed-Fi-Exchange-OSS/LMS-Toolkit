# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import List, Tuple, Type

import pandas as pd
import sqlalchemy as sal

from lms_ds_loader.csv_to_sql import CsvToSql


class MockDbOperationsAdapter:
    def __init__(self):
        self.disable_staging_natural_key_index_called_with: str
        self.truncate_staging_table_called_with: str
        self.insert_into_staging_called_with: Tuple[Type[pd.DataFrame], str]
        self.insert_new_records_to_production_called_with: Tuple[str, List[str]]
        self.enable_staging_natural_key_index_called_with: str

    def truncate_staging_table(self, table):
        self.truncate_staging_table_called_with = table

    def disable_staging_natural_key_index(self, table):
        self.disable_staging_natural_key_index_called_with = table

    def enable_staging_natural_key_index(self, table):
        self.enable_staging_natural_key_index_called_with = table

    def insert_into_staging(self, df, table):
        self.insert_into_staging_called_with = (df, table)

    def insert_new_records_to_production(self, table, columns):
        self.insert_new_records_to_production_called_with = (table, columns)


class Test_when_reading_csv_and_loading_into_a_database:
    class Test_given_valid_arguments:
        def test_then_load_file_into_specified_table_using_pandas(self, mocker):
            adapter = MockDbOperationsAdapter()
            file = "a/b/c.csv"
            table = "c"
            columns = ["A"]

            # Arrange
            read_csv_mock = mocker.patch.object(pd, "read_csv")

            # Act
            csv_to_sql = CsvToSql(adapter)
            csv_to_sql.load_file(file, table, columns)

            # Assert
            read_csv_mock.assert_called_with(file)
            assert adapter.disable_staging_natural_key_index_called_with == table
            assert adapter.truncate_staging_table_called_with == table
            assert adapter.enable_staging_natural_key_index_called_with == table
            assert adapter.insert_into_staging_called_with == (read_csv_mock.return_value, table)
            assert adapter.insert_new_records_to_production_called_with == (table, columns)
