# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
from unittest.mock import Mock
import pandas as pd


from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations


def describe_when_truncating_staging_table() -> None:
    def describe_given_invalid_input() -> None:
        def it_raises_an_error() -> None:
            with pytest.raises(AssertionError):
                MssqlLmsOperations(Mock()).truncate_staging_table("   ")

    def describe_given_valid_input() -> None:
        def it_should_issue_truncate_statement(mocker) -> None:
            table = "user"
            expected = "truncate table lms.[stg_user];"

            # Arrange

            # Explanation: the raw SQLAlchemy execution call is wrapped in
            # method `_exec`, which we can easily bypass here for unit testing.
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(Mock()).truncate_staging_table(table)

            # Assert
            exec_mock.assert_called_with(expected)


def describe_when_disabling_natural_key_index() -> None:
    def describe_given_table_name_is_whitespace() -> None:
        def it_raises_an_error() -> None:
            with pytest.raises(AssertionError):
                MssqlLmsOperations(Mock()).disable_staging_natural_key_index("   ")

    def describe_given_valid_input() -> None:
        def it_issues_truncate_statement(mocker) -> None:
            table = "user"
            expected = (
                "alter index [ix_stg_user_natural_key] on lms.[stg_user] disable;"
            )

            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(Mock()).disable_staging_natural_key_index(
                table
            )

            # Assert
            exec_mock.assert_called_with(expected)


def describe_when_enabling_natural_key_index() -> None:
    def describe_given_table_name_is_whitespace() -> None:
        def it_raises_an_error() -> None:
            with pytest.raises(AssertionError):
                MssqlLmsOperations(Mock()).enable_staging_natural_key_index("   ")

    def describe_given_valid_input() -> None:
        def it_issues_alter__index_statement(mocker) -> None:
            table = "user"
            expected = (
                "alter index [ix_stg_user_natural_key] on lms.[stg_user] rebuild;"
            )

            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(Mock()).enable_staging_natural_key_index(
                table
            )

            # Assert
            exec_mock.assert_called_with(expected)


def describe_when_inserting_new_records() -> None:
    def describe_given_table_is_whitespace() -> None:
        def it_raises_an_error() -> None:
            with pytest.raises(AssertionError):
                MssqlLmsOperations(Mock()).insert_new_records_to_production("   ", ["a"])

    def describe_given_columns_is_an_empty_list() -> None:
        def it_raises_an_error() -> None:
            with pytest.raises(AssertionError):
                MssqlLmsOperations(Mock()).insert_new_records_to_production(
                    "table", list()
                )

    def describe_given_valid_input() -> None:
        def it_issues_insert_where_not_exists_statement(mocker) -> None:
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
            MssqlLmsOperations(Mock()).insert_new_records_to_production(table, columns)

            # Assert
            exec_mock.assert_called_with(expected)


def describe_when_inserting_into_staging() -> None:
    def describe_given_table_is_whitespace() -> None:
        def it_raises_an_error() -> None:
            df = pd.DataFrame()

            with pytest.raises(AssertionError):
                MssqlLmsOperations(Mock()).insert_into_staging(df, "   ")

    def describe_given_valid_arguments() -> None:
        def it_then_use_pandas_to_load_into_the_db(mocker) -> None:
            table = "aaa"
            staging_table = "stg_aaa"
            df = Mock(spec=pd.DataFrame)
            engine_mock = Mock()

            # Act
            MssqlLmsOperations(engine_mock).insert_into_staging(df, table)

            # Assert
            # engine_mock.assert_called()
            df.to_sql.assert_called_with(
                staging_table,
                engine_mock,
                schema="lms",
                if_exists="append",
                index=False,
                method="multi",
                chunksize=190
            )


def describe_when_updating_records() -> None:
    def describe_given_table_is_whitespace() -> None:
        def it_raises_an_error() -> None:
            with pytest.raises(AssertionError):
                MssqlLmsOperations(Mock()).copy_updates_to_production("   ", ["a"])

    def describe_give_columns_is_empty_list() -> None:
        def it_raises_an_error() -> None:
            with pytest.raises(AssertionError):
                MssqlLmsOperations(Mock()).copy_updates_to_production("t", list())

    def describe_given_valid_input() -> None:
        def it_issues_insert_where_not_exists_statement(mocker) -> None:
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
            MssqlLmsOperations(Mock()).copy_updates_to_production(table, columns)

            # Assert
            exec_mock.assert_called_with(expected)


def describe_when_soft_deleting_a_record() -> None:
    def describe_given_table_is_whitespace() -> None:
        def it_raises_an_error() -> None:
            with pytest.raises(AssertionError):
                MssqlLmsOperations(Mock()).soft_delete_from_production("   ", "a")

    def describe_given_valid_input() -> None:
        def it_updates_records_that_are_not_in_the_staging_table(mocker) -> None:

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
            MssqlLmsOperations(Mock()).soft_delete_from_production(table, "Schoology")

            # Assert
            exec_mock.assert_called_with(expected)


def describe_given_assignment_submission_types() -> None:
    def describe_when_inserting_new_records() -> None:
        def it_issues_insert_statement(mocker) -> None:
            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(Mock()).insert_new_submission_types()

            # Assert
            exec_mock.assert_called_with(MssqlLmsOperations.INSERT_SUBMISSION_TYPES)

    def describe_when_soft_deleting_records() -> None:
        def it_issues_update_statement(mocker) -> None:
            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(Mock()).soft_delete_removed_submission_types()

            # Assert
            exec_mock.assert_called_with(MssqlLmsOperations.SOFT_DELETE_SUBMISSION_TYPES)
