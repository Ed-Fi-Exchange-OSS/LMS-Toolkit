# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest
import sqlalchemy as sal


from lms_ds_loader.csv_to_sql import CsvToSql


class Test_when_reading_csv_and_loading_into_a_database:
    class Test_given_valid_arguments:
        def test_then_load_file_into_specified_table_using_pandas(self, mocker):
            connection_string = "23456789"
            file = "a/b/c.csv"
            table = "c"

            # Arrange
            read_csv_mock = mocker.patch.object(pd, "read_csv")
            to_sql_mock = read_csv_mock.return_value.to_sql

            sal_mock = mocker.patch.object(sal, "create_engine")
            # sal_mock.return_value.connect.return_value = object()

            # Act
            csv_to_sql = CsvToSql(connection_string)
            csv_to_sql.load_file(file, table)

            # Assert
            sal_mock.assert_called_with(connection_string)
            read_csv_mock.assert_called_with(file)

            sal_mock.return_value.connect.return_value.__enter__.assert_called()

            """ The assertion below was gnarly to figure out - in paticular the second argument.
            The commented out print statement helped tremendously, displaying this message:
                [call('c', <MagicMock name='create_engine().connect().__enter__()' id='1760938768752'>, schema='lms', if_exists='append', index=False, method='multi')]
            To see that message, you must call pytest with argument `-s`. """
            # print(to_sql_mock.call_args_list)
            to_sql_mock.assert_called_with(
                table,
                sal_mock.return_value.connect.return_value.__enter__.return_value,
                schema="lms",
                if_exists="append",
                index=False,
                method="multi",
            )
