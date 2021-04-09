# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging

import pytest
from unittest.mock import Mock
import pandas as pd
from sqlalchemy.exc import ProgrammingError

from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations


def describe_when_truncating_staging_table() -> None:
    def describe_given_invalid_input() -> None:
        def it_raises_an_error() -> None:
            with pytest.raises(AssertionError):
                MssqlLmsOperations(Mock()).truncate_staging_table("   ")

    def describe_given_valid_input() -> None:
        def it_should_issue_truncate_statement(mocker) -> None:
            table = "user"
            expected = "TRUNCATE TABLE lms.stg_user;"

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
            expected = "ALTER INDEX IX_stg_user_Natural_Key on lms.stg_user DISABLE;"

            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(Mock()).disable_staging_natural_key_index(table)

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
            expected = "ALTER INDEX IX_stg_user_Natural_Key on lms.stg_user REBUILD;"

            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(Mock()).enable_staging_natural_key_index(table)

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
                chunksize=120,
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
            columns = ["a", "b", "SourceSystem", "SourceSystemIdentifier"]
            table = "Fake"
            expected = """
UPDATE
    t
SET
    a = stg.a,
    b = stg.b
FROM
    lms.Fake as t
INNER JOIN
    lms.stg_Fake as stg
ON
    t.SourceSystem = stg.SourceSystem
AND
    t.SourceSystemIdentifier = stg.SourceSystemIdentifier
AND
    t.LastModifiedDate <> stg.LastModifiedDate
"""

            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(Mock()).copy_updates_to_production(table, columns)

            # Assert
            exec_mock.assert_called_with(expected)

    def describe_given_resource_is_child_of_section() -> None:
        def it_should_build_a_valid_insert_statement(mocker) -> None:
            columns = [
                "a",
                "b",
                "SourceSystem",
                "SourceSystemIdentifier",
                "LMSSectionSourceSystemIdentifier",
            ]
            table = "Fake"
            expected = """
UPDATE
    t
SET
    a = stg.a,
    b = stg.b
FROM
    lms.Fake as t
INNER JOIN
    lms.stg_Fake as stg
ON
    t.SourceSystem = stg.SourceSystem
AND
    t.SourceSystemIdentifier = stg.SourceSystemIdentifier
AND
    t.LastModifiedDate <> stg.LastModifiedDate
"""

            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(Mock()).copy_updates_to_production(table, columns)

            # Assert
            exec_mock.assert_called_with(expected)

    def describe_given_resource_is_child_of_section_and_user() -> None:
        def it_should_build_a_valid_update_statement(mocker) -> None:
            columns = [
                "a",
                "b",
                "SourceSystem",
                "SourceSystemIdentifier",
                "LMSSectionSourceSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
            ]
            table = "Fake"
            expected = """
UPDATE
    t
SET
    a = stg.a,
    b = stg.b
FROM
    lms.Fake as t
INNER JOIN
    lms.stg_Fake as stg
ON
    t.SourceSystem = stg.SourceSystem
AND
    t.SourceSystemIdentifier = stg.SourceSystemIdentifier
AND
    t.LastModifiedDate <> stg.LastModifiedDate
"""

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

            source_system = "Schoology"
            table = "Fake"
            expected = """
UPDATE
    t
SET
    t.DeletedAt = getdate()
FROM
    lms.Fake as t
WHERE
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.stg_Fake as stg
        WHERE
            t.SourceSystemIdentifier = stg.SourceSystemIdentifier
        AND
            t.SourceSystem = stg.SourceSystem
    )
AND
    t.DeletedAt IS NULL
AND
    t.SourceSystem = 'Schoology'
"""

            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(Mock()).soft_delete_from_production(table, source_system)

            # Assert
            exec_mock.assert_called_with(expected)


def describe_given_assignment_submission_types() -> None:
    def describe_when_inserting_new_records() -> None:
        def it_issues_insert_statement(mocker) -> None:
            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            expected = """
INSERT INTO lms.AssignmentSubmissionType (
    AssignmentIdentifier,
    SubmissionType
)
SELECT
    Assignment.AssignmentIdentifier,
    stg_AssignmentSubmissionType.SubmissionType
FROM
        lms.stg_AssignmentSubmissionType
    INNER JOIN
        lms.Assignment
    ON
        stg_AssignmentSubmissionType.SourceSystem = Assignment.SourceSystem
    AND
        stg_AssignmentSubmissionType.SourceSystemIdentifier = Assignment.SourceSystemIdentifier
WHERE
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.AssignmentSubmissionType
        WHERE
            AssignmentIdentifier = Assignment.AssignmentIdentifier
        AND
            SubmissionType = stg_AssignmentSubmissionType.SubmissionType
    )
"""

            # Act
            MssqlLmsOperations(Mock()).insert_new_submission_types()

            # Assert
            exec_mock.assert_called_with(expected)

    def describe_when_soft_deleting_records() -> None:
        def it_issues_update_statement(mocker) -> None:
            # Arrange
            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            source_system = "Canvas"
            expected = """
UPDATE
    AssignmentSubmissionType
SET
    DeletedAt = GETDATE()
FROM
    lms.AssignmentSubmissionType
INNER JOIN
    lms.Assignment
ON
    AssignmentSubmissionType.AssignmentIdentifier = Assignment.AssignmentIdentifier
WHERE
    SourceSystem = 'Canvas'
AND
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.stg_AssignmentSubmissionType
        WHERE
            stg_AssignmentSubmissionType.SourceSystem = Assignment.SourceSystem
        AND
            stg_AssignmentSubmissionType.SourceSystemIdentifier = Assignment.SourceSystemIdentifier
        AND
            stg_AssignmentSubmissionType.SubmissionType = AssignmentSubmissionType.SubmissionType
    )
"""

            # Act
            MssqlLmsOperations(Mock()).soft_delete_removed_submission_types(
                source_system
            )

            # Assert
            exec_mock.assert_called_with(expected)


def describe_when_inserting_new_records() -> None:
    def describe_given_resource_is_not_child_of_section() -> None:
        def describe_given_table_is_whitespace() -> None:
            def it_raises_an_error() -> None:
                with pytest.raises(AssertionError):
                    MssqlLmsOperations(Mock()).insert_new_records_to_production(
                        "   ", ["a"]
                    )

        def describe_given_columns_is_an_empty_list() -> None:
            def it_raises_an_error() -> None:
                with pytest.raises(AssertionError):
                    MssqlLmsOperations(Mock()).insert_new_records_to_production(
                        "table", list()
                    )

        def describe_given_valid_input() -> None:
            def it_issues_insert_where_not_exists_statement(mocker) -> None:
                columns = ["a", "b"]
                table = "Fake"
                expected = """
INSERT INTO
    lms.Fake
(
    a,
    b
)
SELECT
    a,
    b
FROM
    lms.stg_Fake as stg
WHERE
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.Fake
        WHERE
            SourceSystemIdentifier = stg.SourceSystemIdentifier
        AND
            SourceSystem = stg.SourceSystem
    )
"""

                # Arrange
                exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

                # Act
                MssqlLmsOperations(Mock()).insert_new_records_to_production(
                    table, columns
                )

                # Assert
                exec_mock.assert_called_with(expected)

    def describe_given_resource_is_child_of_section() -> None:
        def it_should_build_a_valid_insert_statement(mocker) -> None:
            # Arrange
            expected = """
INSERT INTO
    lms.Fake
(
    LMSSectionIdentifier,
    SourceSystem,
    SourceSystemIdentifier
)
SELECT
    LMSSection.LMSSectionIdentifier,
    stg.SourceSystem,
    stg.SourceSystemIdentifier
FROM
    lms.stg_Fake as stg
INNER JOIN
    lms.LMSSection
ON
    stg.LMSSectionSourceSystemIdentifier = LMSSection.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSSection.SourceSystem
WHERE NOT EXISTS (
  SELECT
    1
  FROM
    lms.Fake
  WHERE
    SourceSystemIdentifier = stg.SourceSystemIdentifier
  AND
    SourceSystem = stg.SourceSystem
)
"""
            TABLE = "Fake"
            COLUMNS = [
                "LMSSectionSourceSystemIdentifier",
                "SourceSystem",
                "SourceSystemIdentifier",
            ]

            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(Mock()).insert_new_records_to_production_for_section(
                TABLE, COLUMNS
            )

            # Assert
            exec_mock.assert_called_with(expected)

    def describe_given_resource_is_child_of_user() -> None:
        def it_should_build_a_valid_insert_statement(mocker) -> None:
            # Arrange
            expected = """
INSERT INTO
    lms.Fake
(
    LMSUserIdentifier,
    SourceSystem,
    SourceSystemIdentifier
)
SELECT
    LMSUser.LMSUserIdentifier,
    stg.SourceSystem,
    stg.SourceSystemIdentifier
FROM
    lms.stg_Fake as stg
INNER JOIN
    lms.LMSUser
ON
    stg.LMSUserSourceSystemIdentifier = LMSUser.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSUser.SourceSystem
WHERE NOT EXISTS (
  SELECT
    1
  FROM
    lms.Fake
  WHERE
    SourceSystemIdentifier = stg.SourceSystemIdentifier
  AND
    SourceSystem = stg.SourceSystem
)
"""
            TABLE = "Fake"
            COLUMNS = [
                "LMSUserSourceSystemIdentifier",
                "SourceSystem",
                "SourceSystemIdentifier",
            ]

            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(Mock()).insert_new_records_to_production_for_user(
                TABLE, COLUMNS
            )

            # Assert
            exec_mock.assert_called_with(expected)

    def describe_given_resource_is_child_of_section_and_user() -> None:
        def it_should_build_a_valid_insert_statement(mocker) -> None:
            # Arrange
            expected = """
INSERT INTO
    lms.Fake
(
    LMSSectionIdentifier,
    LMSUserIdentifier,
    SourceSystem,
    SourceSystemIdentifier
)
SELECT
    LMSSection.LMSSectionIdentifier,
    LMSUser.LMSUserIdentifier,
    stg.SourceSystem,
    stg.SourceSystemIdentifier
FROM
    lms.stg_Fake as stg
INNER JOIN
    lms.LMSSection
ON
    stg.LMSSectionSourceSystemIdentifier = LMSSection.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSSection.SourceSystem
INNER JOIN
    lms.LMSUser
ON
    stg.LMSUserSourceSystemIdentifier = LMSUser.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSUser.SourceSystem
WHERE NOT EXISTS (
  SELECT
    1
  FROM
    lms.Fake
  WHERE
    SourceSystemIdentifier = stg.SourceSystemIdentifier
  AND
    SourceSystem = stg.SourceSystem
)
"""
            TABLE = "Fake"
            COLUMNS = [
                "LMSSectionSourceSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
                "SourceSystem",
                "SourceSystemIdentifier",
            ]

            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(
                Mock()
            ).insert_new_records_to_production_for_section_and_user(TABLE, COLUMNS)

            # Assert
            exec_mock.assert_called_with(expected)

    def describe_given_resource_is_child_of_assignment_and_user() -> None:
        def it_should_build_a_valid_insert_statement(mocker) -> None:
            # Arrange
            expected = """
INSERT INTO
    lms.Fake
(
    AssignmentIdentifier,
    LMSUserIdentifier,
    SourceSystem,
    SourceSystemIdentifier
)
SELECT
    Assignment.AssignmentIdentifier,
    LMSUser.LMSUserIdentifier,
    stg.SourceSystem,
    stg.SourceSystemIdentifier
FROM
    lms.stg_Fake as stg
INNER JOIN
    lms.Assignment
ON
    stg.AssignmentSourceSystemIdentifier = Assignment.SourceSystemIdentifier
AND
    stg.SourceSystem = Assignment.SourceSystem
INNER JOIN
    lms.LMSUser
ON
    stg.LMSUserSourceSystemIdentifier = LMSUser.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSUser.SourceSystem
WHERE NOT EXISTS (
  SELECT
    1
  FROM
    lms.Fake
  WHERE
    SourceSystemIdentifier = stg.SourceSystemIdentifier
  AND
    SourceSystem = stg.SourceSystem
)
"""
            TABLE = "Fake"
            COLUMNS = ["AssignmentSourceSystemIdentifier", "LMSUserSourceSystemIdentifier", "SourceSystem", "SourceSystemIdentifier"]

            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")

            # Act
            MssqlLmsOperations(Mock()).insert_new_records_to_production_for_assignment_and_user(TABLE, COLUMNS)

            # Assert
            exec_mock.assert_called_with(expected)

    def describe_given_attendance_events():
        def describe_and_no_table_name_provided():
            def it_raises_an_error():
                with pytest.raises(AssertionError):
                    MssqlLmsOperations(Mock()).insert_new_records_to_production_for_attendance_events("", ["a"])

        def describe_and_no_columns_provided():
            def it_raises_an_error():
                with pytest.raises(AssertionError):
                    MssqlLmsOperations(Mock()).insert_new_records_to_production_for_attendance_events("something", [])

        def describe_given_columns_including_both_foreign_keys():
            def it_should_build_the_correct_insert_statement(mocker):
                # Arrange
                row_count = 2
                table = "fake"
                columns = [
                    "LMSSectionSourceSystemIdentifier",
                    "LMSUserSourceSystemIdentifier",
                    "Another"
                ]

                expected = """
INSERT INTO
    lms.LMSUserAttendanceEvent
(
    LMSSectionIdentifier,
    LMSUserIdentifier,
    LMSUserLMSSectionAssociationIdentifier,
    Another
)
SELECT
    LMSSection.LMSSectionIdentifier,
    LMSUser.LMSUserIdentifier,
    LMSUserLMSSectionAssociation.LMSUserLMSSectionAssociationIdentifier,
    stg.Another
FROM
    lms.stg_LMSUserAttendanceEvent as stg
INNER JOIN
    lms.LMSSection
ON
    stg.LMSSectionSourceSystemIdentifier = LMSSection.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSSection.SourceSystem
INNER JOIN
    lms.LMSUser
ON
    stg.LMSUserSourceSystemIdentifier = LMSUser.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSUser.SourceSystem
INNER JOIN
    lms.LMSUserLMSSectionAssociation
ON
    LMSUser.LMSUserIdentifier = LMSUserLMSSectionAssociation.LMSUserIdentifier
AND
    LMSSection.LMSSectionIdentifier = LMSUserLMSSectionAssociation.LMSSectionIdentifier
WHERE NOT EXISTS (
  SELECT
    1
  FROM
    lms.LMSUserAttendanceEvent
  WHERE
    SourceSystemIdentifier = stg.SourceSystemIdentifier
  AND
    SourceSystem = stg.SourceSystem
)
"""
                system = MssqlLmsOperations(Mock())
                mock = mocker.patch.object(system, "_exec", return_value=row_count)

                # Act
                system.insert_new_records_to_production_for_attendance_events(table, columns)

                # Arrange
                mock.assert_called_with(expected)



def describe_when_getting_processed_files():
    def describe_given_parameters_are_correct():
        def it_should_build_the_correct_sql_query(mocker):
            resource_name = "fake_resource_name"
            expected_query = """
SELECT
    FullPath
FROM
    lms.ProcessedFiles
WHERE
    ResourceName = 'fake_resource_name'
""".strip()

            query_mock = mocker.patch.object(
                pd, "read_sql_query", return_value=pd.DataFrame(columns=["FullPath"])
            )

            MssqlLmsOperations(Mock()).get_processed_files(resource_name)

            call_args = query_mock.call_args
            assert len(call_args) == 2
            assert call_args[0][0] == expected_query

    def describe_given_the_processed_file_table_does_not_exist():
        def it_should_log_an_error_and_re_raise_the_exception(mocker):
            def __raise(query, engine) -> None:
                raise ProgrammingError("statement", [], "none", False)

            mocker.patch.object(pd, "read_sql_query", side_effect=__raise)

            # Typically we do not test the logging. In this case and another
            # below, logging was a core business requirement for a task, and
            # thus it makes sense to test that requirement.
            logger = logging.getLogger("edfi_lms_ds_loader.mssql_lms_operations")
            mock_exc_logger = mocker.patch.object(logger, "exception")

            with pytest.raises(ProgrammingError):
                MssqlLmsOperations(Mock()).get_processed_files("fake_resource_name")

            mock_exc_logger.assert_called_once()


def describe_when_adding_processed_files():
    def describe_given_parameters_are_correct():
        def it_should_build_the_correct_sql_statement(mocker):
            resource_name = "fake_resource_name"
            path = "fake_path/"
            rows = 3
            expected_statement = """
INSERT INTO
    lms.ProcessedFiles
(
    FullPath,
    ResourceName,
    NumberOfRows
)
VALUES
(
    'fake_path/',
    'fake_resource_name',
    3
)
""".strip()

            exec_mock = mocker.patch.object(MssqlLmsOperations, "_exec")
            MssqlLmsOperations(Mock()).add_processed_file(path, resource_name, rows)

            exec_mock.assert_called_with(expected_statement)

    def describe_given_the_processed_file_table_does_not_exist():
        def it_should_log_an_error_and_re_raise_the_exception(mocker):
            def __raise(_) -> None:
                raise ProgrammingError("statement", [], "none", False)

            resource_name = "fake_resource_name"
            path = "fake_path/"
            rows = 3

            mocker.patch.object(MssqlLmsOperations, "_exec", side_effect=__raise)

            logger = logging.getLogger("edfi_lms_ds_loader.mssql_lms_operations")
            mock_exc_logger = mocker.patch.object(logger, "exception")

            with pytest.raises(ProgrammingError):
                MssqlLmsOperations(Mock()).add_processed_file(path, resource_name, rows)

            mock_exc_logger.assert_called_once()

# insert_new_records_to_production_for_attendance_events
