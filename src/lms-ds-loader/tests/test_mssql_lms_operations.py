# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
from unittest.mock import Mock

import pandas as pd


from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations


class Test_MssqlLmsOperations:
    class Test_when_executing_statement:
        def test_given_connection_string_is_whitespace_then_raise_error(self):
            with pytest.raises(AssertionError):
                MssqlLmsOperations("   ")._exec("a")

        def test_given_statement_is_whitespace_then_raise_error(self):
            with pytest.raises(AssertionError):
                MssqlLmsOperations("a")._exec("    ")

    class Test_when_truncating_staging_table:
        class Test_given_invalid_input:
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
            def test_table_is_whitespace_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("a").insert_new_records_to_production("   ", ["a"])

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
  and sourcesystem = stg.sourcesystem
)
"""
            expected = expected.strip()

            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations("aaa").insert_new_records_to_production(table, columns)

            # Assert
            exec_mock.assert_called_with(expected)

    class Test_when_inserting_into_staging:
        class Test_given_invalid_arguments:
            def test_given_table_is_whitespace_then_raise_error(self):
                df = pd.DataFrame()

                with pytest.raises(AssertionError):
                    MssqlLmsOperations("aaa").insert_into_staging(df, "   ")

        def test_given_valid_arguments_then_use_pandas_to_load_into_the_db(
            self, mocker
        ):
            connection_string = "connection string"
            table = "aaa"
            staging_table = "stg_aaa"
            df = Mock(spec=pd.DataFrame)

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
                method="multi",
                chunksize=190
            )

    class Test_when_updating_records:
        class Test_given_invalid_arguments:
            def test_given_table_is_whitespace_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("a").copy_updates_to_production("   ", ["a"])

            def test_give_columns_is_empty_list_then_raise_error(self):
                with pytest.raises(AssertionError):
                    MssqlLmsOperations("a").copy_updates_to_production("t", list())

        def test_given_valid_input_then_issue_insert_where_not_exists_statement(
            self, mocker
        ):
            columns = ["a", "b"]
            table = "tbl"
            expected = """
update t set t.[a] = stg.[a], t.[b] = stg.[b]
from lms.[tbl] as t
inner join lms.stg_tbl as stg
on t.sourcesystem = stg.sourcesystem
and t.sourcesystemidentifier = stg.sourcesystemidentifier
and t.lastmodifieddate <> stg.lastmodifieddate
"""
            expected = expected.strip()

            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations("aaa").copy_updates_to_production(table, columns)

            # Assert
            exec_mock.assert_called_with(expected)

    class Test_when_soft_deleting_a_record:
        class Test_given_valid_input:
            def test_then_update_records_that_are_not_in_the_staging_table(self, mocker):

                table = "tbl"
                expected = """
update t set t.deletedat = getdate()
from lms.[tbl] as t
where not exists (
select 1 from lms.stg_tbl as stg
where t.sourcesystemidentifier = stg.sourcesystemidentifier
and t.sourcesystem = stg.sourcesystem
) and deletedat is null
and t.sourceSystem = 'Schoology'"""
                expected = expected.strip()

                # Arrange
                exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

                # Act
                MssqlLmsOperations("aaa").soft_delete_from_production(table, "Schoology")

                # Assert
                exec_mock.assert_called_with(expected)
