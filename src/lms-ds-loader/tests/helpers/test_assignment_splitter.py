# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from io import StringIO
from typing import Tuple

import pandas as pd
import pytest

from edfi_lms_ds_loader.helpers.assignment_splitter import split


def describe_given_two_canvas_assignments_with_variable_number_submission_types() -> None:
    @pytest.fixture
    def when_splitting_the_assignments() -> Tuple[pd.DataFrame, pd.DataFrame]:
        # Arrange
        data = StringIO(
            """LMSSectionSourceSystemIdentifier,SourceSystemIdentifier,SubmissionType,SourceSystem,CreateDate,LastModifiedDate
104,111,"['online_text_entry', 'online_upload']",Canvas,2021-03-11,2021-03-12
104,112,['online_upload'],Canvas,2021-03-13,2021-03-14"""
        )

        assignments_df = pd.read_csv(data)

        # Act
        assignments_df, submission_types_df = split(assignments_df)  # type: ignore

        return assignments_df, submission_types_df

    def it_should_remove_SubmissionType_from_the_assignments_DataFrame(
        when_splitting_the_assignments,
    ) -> None:
        df, _ = when_splitting_the_assignments

        assert "SubmissionType" not in list(df.columns)

    def it_should_preserve_other_columns_and_values_in_assignments_DataFrame(
        when_splitting_the_assignments,
    ) -> None:
        df, _ = when_splitting_the_assignments

        # Testing one row seems sufficient
        row = df.iloc[0]

        assert row["SourceSystemIdentifier"] == 111
        assert row["SourceSystem"] == "Canvas"
        assert row["LMSSectionSourceSystemIdentifier"] == 104
        assert row["CreateDate"] == "2021-03-11"
        assert row["LastModifiedDate"] == "2021-03-12"

    def it_should_map_111_online_text_entry_to_submission_types(
        when_splitting_the_assignments,
    ) -> None:
        _, df = when_splitting_the_assignments

        row = df.iloc[0]

        assert row["SourceSystemIdentifier"] == 111
        assert row["SourceSystem"] == "Canvas"
        assert row["SubmissionType"] == "online_text_entry"
        assert row["CreateDate"] == "2021-03-11"

    def it_should_map_111_online_upload_to_submission_types(
        when_splitting_the_assignments,
    ) -> None:
        _, df = when_splitting_the_assignments

        # NOTE: keep an eye on this, not sure that the row numbers are actually
        # deterministic. If this fails then we'll need to change to lookup the
        # row with a filter, instead of assuming the row number.
        row = df.iloc[2]
        assert row["SourceSystemIdentifier"] == 111
        assert row["SourceSystem"] == "Canvas"
        assert row["SubmissionType"] == "online_upload"
        assert row["CreateDate"] == "2021-03-11"

    def it_should_map_112_online_upload_to_submission_types(
        when_splitting_the_assignments,
    ) -> None:
        _, df = when_splitting_the_assignments

        row = df.iloc[1]
        assert row["SourceSystemIdentifier"] == 112
        assert row["SourceSystem"] == "Canvas"
        assert row["SubmissionType"] == "online_upload"
        assert row["CreateDate"] == "2021-03-13"


def describe_given_one_canvas_assignment_with_one_submission_types() -> None:
    @pytest.fixture
    def when_splitting_the_assignments() -> Tuple[pd.DataFrame, pd.DataFrame]:
        # Arrange
        data = StringIO(
            """LMSSectionSourceSystemIdentifier,SourceSystemIdentifier,SubmissionType,SourceSystem,CreateDate,LastModifiedDate
104,112,['online_upload'],Canvas,2021-03-11,2021-03-12"""
        )

        assignments_df = pd.read_csv(data)

        # Act
        assignments_df, submission_types_df = split(assignments_df)  # type: ignore

        return assignments_df, submission_types_df

    def it_should_map_112_online_upload_to_submission_types(
        when_splitting_the_assignments,
    ) -> None:
        _, df = when_splitting_the_assignments

        row = df.iloc[0]

        assert row["SourceSystemIdentifier"] == 112
        assert row["SourceSystem"] == "Canvas"
        assert row["SubmissionType"] == "online_upload"
        assert row["CreateDate"] == "2021-03-11"


def describe_given_there_are_no_assignments() -> None:
    @pytest.fixture
    def when_splitting_the_assignments() -> Tuple[pd.DataFrame, pd.DataFrame]:
        # Arrange
        assignments_df = pd.DataFrame()

        # Act
        assignments_df, submission_types_df = split(assignments_df)  # type: ignore

        return assignments_df, submission_types_df

    def it_should_create_empty_assignments_DataFrame(
        when_splitting_the_assignments,
    ) -> None:
        df, _ = when_splitting_the_assignments

        assert df.empty

    def it_should_create_empty_submission_types_DataFrame(
        when_splitting_the_assignments,
    ) -> None:
        _, df = when_splitting_the_assignments

        assert df.empty


def describe_given_one_canvas_assignment_with_no_submission_types() -> None:
    @pytest.fixture
    def when_splitting_the_assignments() -> Tuple[pd.DataFrame, pd.DataFrame]:
        # Arrange
        data = StringIO(
            """LMSSectionSourceSystemIdentifier,SourceSystemIdentifier,SubmissionType,SourceSystem,CreateDate,LastModifiedDate
104,112,,Canvas,2021-03-11,2021-03-12"""
        )

        assignments_df = pd.read_csv(data)

        # Act
        assignments_df, submission_types_df = split(assignments_df)  # type: ignore

        return assignments_df, submission_types_df

    def it_should_preserve_rows_in_Assignment_DataFrame(
        when_splitting_the_assignments,
    ) -> None:
        df, _ = when_splitting_the_assignments

        row = df.iloc[0]

        assert row["SourceSystemIdentifier"] == 112
        assert row["SourceSystem"] == "Canvas"
        assert row["LMSSectionSourceSystemIdentifier"] == 104
        assert row["CreateDate"] == "2021-03-11"
        assert row["LastModifiedDate"] == "2021-03-12"

    def it_should_return_an_empty_submission_type_DataFrame(
        when_splitting_the_assignments,
    ) -> None:
        _, df = when_splitting_the_assignments

        assert df.empty


def describe_given_one_google_assignment() -> None:
    @pytest.fixture
    def when_splitting_the_assignments() -> Tuple[pd.DataFrame, pd.DataFrame]:
        # Arrange
        data = StringIO(
            """LMSSectionSourceSystemIdentifier,SourceSystemIdentifier,SubmissionType,SourceSystem,CreateDate,LastModifiedDate
104,112,ASSIGNMENT,Google Classroom,2021-03-11,2021-03-12"""
        )

        assignments_df = pd.read_csv(data)

        # Act
        assignments_df, submission_types_df = split(assignments_df)  # type: ignore

        return assignments_df, submission_types_df

    def it_should_remove_SubmissionType_from_the_assignments_DataFrame(
        when_splitting_the_assignments,
    ) -> None:
        df, _ = when_splitting_the_assignments

        assert "SubmissionType" not in list(df.columns)

    def it_should_preserve_other_columns_and_values_in_assignments_DataFrame(
        when_splitting_the_assignments,
    ) -> None:
        df, _ = when_splitting_the_assignments

        row = df.iloc[0]

        assert row["SourceSystemIdentifier"] == 112
        assert row["SourceSystem"] == "Google Classroom"
        assert row["LMSSectionSourceSystemIdentifier"] == 104
        assert row["CreateDate"] == "2021-03-11"

    def it_should_map_Assignment_to_submission_types(
        when_splitting_the_assignments,
    ) -> None:
        _, df = when_splitting_the_assignments

        row = df.iloc[0]

        assert row["SourceSystemIdentifier"] == 112
        assert row["SourceSystem"] == "Google Classroom"
        assert row["SubmissionType"] == "ASSIGNMENT"
        assert row["CreateDate"] == "2021-03-11"


def describe_given_one_schoology_assignment() -> None:
    @pytest.fixture
    def when_splitting_the_assignments() -> Tuple[pd.DataFrame, pd.DataFrame]:
        # Arrange
        data = StringIO(
            """SourceSystemIdentifier,Title,AssignmentDescription,DueDateTime,MaxPoints,AssignmentCategory,CreateDate,LastModifiedDate,SourceSystem,LMSSectionSourceSystemIdentifier,SubmissionType,SourceCreateDate,SourceLastModifiedDate,StartDateTime,EndDateTime
2942251001,Algebra foundations,,2020-08-28 23:59:00,100,assignment,2021-03-04 09:25:43,2021-03-04 09:25:43,Schoology,2942191527,,,,,"""
        )

        assignments_df = pd.read_csv(data)

        # Act
        assignments_df, submission_types_df = split(assignments_df)  # type: ignore

        return assignments_df, submission_types_df

    def it_should_remove_SubmissionType_from_the_assignments_DataFrame_abc(
        when_splitting_the_assignments,
    ) -> None:
        df, _ = when_splitting_the_assignments

        assert "SubmissionType" not in list(df.columns)

    def it_should_preserve_other_columns_and_values_in_assignments_DataFrame(
        when_splitting_the_assignments,
    ) -> None:
        df, _ = when_splitting_the_assignments

        row = df.iloc[0]

        assert row["SourceSystemIdentifier"] == 2942251001
        assert row["SourceSystem"] == "Schoology"
        assert row["LMSSectionSourceSystemIdentifier"] == 2942191527
        # That's good enough. Don't need to test that the fixture's call to
        # `pd.read_csv` is working properly ;-). Just confirming that the
        # row is still there.

    def it_should_create_empty_submission_types_DataFrame(
        when_splitting_the_assignments,
    ) -> None:
        _, df = when_splitting_the_assignments

        assert df.empty
