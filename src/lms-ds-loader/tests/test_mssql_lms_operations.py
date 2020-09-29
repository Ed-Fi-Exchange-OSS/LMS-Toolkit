# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
from unittest.mock import Mock

import pandas as pd


from lms_ds_loader.mssql_lms_operations import MssqlLmsOperations


class Test_MssqlLmsOperations:
    class Test_when_executing_statement:
        def test_given_connection_string_is_none_then_raise_error(self):
            with pytest.raises(AssertionError):
                MssqlLmsOperations(None)._exec("a")

        def test_given_connection_string_is_whitespace_then_raise_error(self):
            with pytest.raises(AssertionError):
                MssqlLmsOperations("   ")._exec("a")

        def test_given_statement_is_none_then_raise_error(self):
            with pytest.raises(AssertionError):
                MssqlLmsOperations("a")._exec(None)

        def test_given_statement_is_whitespace_then_raise_error(self):
            with pytest.raises(AssertionError):
                MssqlLmsOperations("a")._exec("    ")

    class Test_when_truncating_staging_table:
        class Test_given_invalid_input:
            def test_and_table_name_is_none_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("a").truncate_staging_table(None)

            def test_and_table_name_is_whitespace_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("a").truncate_staging_table("   ")

        def test_given_valid_input_then_issue_truncate_statement(self, mocker):
            connection_string = "a connection string"
            table = "user"
            expected = "truncate table lms.[stg_user];"

            # Arrange

            # Explanation: the raw SQLAlchemy execution call is wrapped in
            # method `_exec`, which we can easily bypass here for unit testing.
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(connection_string).truncate_staging_table(table)

            # Assert
            exec_mock.assert_called_with(expected)

    class Test_when_disabling_natural_key_index:
        class Test_given_invalid_input:
            def test_and_table_name_is_none_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("a").disable_staging_natural_key_index(None)

            def test_and_table_name_is_whitespace_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("a").disable_staging_natural_key_index("   ")

        def test_given_valid_input_then_issue_truncate_statement(self, mocker):
            connection_string = "a connection string"
            table = "user"
            expected = (
                "alter index [ix_stg_user_natural_key] on lms.[stg_user] disable;"
            )

            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(connection_string).disable_staging_natural_key_index(
                table
            )

            # Assert
            exec_mock.assert_called_with(expected)

    class Test_when_enabling_natural_key_index:
        class Test_given_invalid_input:
            def test_table_name_is_none_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("a").enable_staging_natural_key_index(None)

            def test_table_name_is_whitespace_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("a").enable_staging_natural_key_index("   ")

        def test_given_valid_input_then_issue_truncate_statement(self, mocker):
            connection_string = "a connection string"
            table = "user"
            expected = (
                "alter index [ix_stg_user_natural_key] on lms.[stg_user] rebuild;"
            )

            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(connection_string).enable_staging_natural_key_index(
                table
            )

            # Assert
            exec_mock.assert_called_with(expected)

    class Test_when_inserting_new_records:
        class Test_given_invalid_input:
            def test_table_is_none_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("a").insert_new_records_to_production(None, "a")

            def test_table_is_whitespace_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("a").insert_new_records_to_production("   ", "a")

            def test_columns_is_none_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("a").insert_new_records_to_production(
                        "table", None
                    )

            def test_columns_is_not_an_array_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("a").insert_new_records_to_production(
                        "table", "not an array"
                    )

            def test_columns_is_an_empty_list_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("a").insert_new_records_to_production(
                        "table", list()
                    )

        def test_given_valid_input_then_issue_insert_where_not_exists_statement(
            self, mocker
        ):
            columns = ["a", "b"]
            table = "tbl"
            expected = """
insert into lms.[tbl] ( [a], [b] )
select [a], [b]
from lms.stg_tbl as stg
where not exists (
select 1 from lms.[tbl]
where sourcesystemidentifier = stg.sourcesystemidentifier
and sourcesystem = stg.sourcesystem)
"""
            expected = expected.strip().replace("\n", " ")

            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations("aaa").insert_new_records_to_production(table, columns)

            # Assert
            exec_mock.assert_called_with(expected)

    class Test_when_inserting_into_staging:
        class Test_given_invalid_arguments:
            def test_given_data_frame_is_none_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("aaa").insert_into_staging(None, "table")

            def test_given_table_is_none_then_raise_error(self):
                df = pd.DataFrame()

                with pytest.raises(AssertionError):
                    MssqlLmsOperations("aaa").insert_into_staging(df, None)

            def test_given_table_is_whitespace_then_raise_error(self):
                df = pd.DataFrame()

                with pytest.raises(AssertionError):
                    MssqlLmsOperations("aaa").insert_into_staging(df, "   ")

        def test_given_valid_arguments_then_use_pandas_to_load_into_the_db(self, mocker):
            connection_string = "connection string"
            table = "aaa"
            staging_table = "stg_aaa"
            df = Mock()

            # Arrange
            engine_mock = mocker.patch.object(MssqlLmsOperations, "_get_sql_engine")

            # Act
            MssqlLmsOperations(connection_string).insert_into_staging(df, table)

            # Assert
            engine_mock.assert_called()
            df.to_sql.assert_called_with(
                staging_table,
                engine_mock.return_value,
                schema="lms",
                if_exists="append",
                index=False,
                method="multi"
            )
