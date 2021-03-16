# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from io import StringIO

import pandas as pd
import pytest

from edfi_lms_ds_loader.helpers.assignment_splitter import split


def describe_given_two_assignments_with_variable_number_submission_types():
    @pytest.fixture
    def when_splitting_the_assignments():
        # Arrange
        data = StringIO(
            """LMSSectionIdentifier,SourceSystemIdentifier,SubmissionType,SourceSystem
104,111,"['online_text_entry', 'online_upload']",Canvas
104,112,['online_upload'],Canvas"""
        )

        assignments_df = pd.read_csv(data)

        # Act
        assignments_df, submission_types_df = split(assignments_df)  # type: ignore

        return assignments_df, submission_types_df

    def it_should_remove_SubmissionType_from_the_assignments_DataFrame(
        when_splitting_the_assignments,
    ):
        df, _ = when_splitting_the_assignments

        assert "SubmissionType" not in list(df.columns)

    def it_should_preserve_other_columns_and_values_in_assignments_DataFrame(
        when_splitting_the_assignments,
    ):
        df, _ = when_splitting_the_assignments

        # Testing one row seems sufficient
        mask = (
            (df["SourceSystemIdentifier"] == 111)
            & (df["SourceSystem"] == "Canvas")
            & (df["LMSSectionIdentifier"] == 104)
        )

        assert df[mask].shape[0] == 1

    def it_should_map_111_online_text_entry_to_submission_types(
        when_splitting_the_assignments,
    ):
        _, df = when_splitting_the_assignments

        mask = (
            (df["SourceSystemIdentifier"] == 111)
            & (df["SourceSystem"] == "Canvas")
            & (df["SubmissionType"] == "online_text_entry")
        )

        assert df[mask].shape[0] == 1

    def it_should_map_111_online_upload_to_submission_types(
        when_splitting_the_assignments,
    ):
        _, df = when_splitting_the_assignments

        mask = (
            (df["SourceSystemIdentifier"] == 111)
            & (df["SourceSystem"] == "Canvas")
            & (df["SubmissionType"] == "online_upload")
        )

        assert df[mask].shape[0] == 1

    def it_should_map_112_online_upload_to_submission_types(
        when_splitting_the_assignments,
    ):
        _, df = when_splitting_the_assignments

        mask = (
            (df["SourceSystemIdentifier"] == 112)
            & (df["SourceSystem"] == "Canvas")
            & (df["SubmissionType"] == "online_upload")
        )

        assert df[mask].shape[0] == 1


def describe_given_one_assignment_with_one_submission_types():
    @pytest.fixture
    def when_splitting_the_assignments():
        # Arrange
        data = StringIO(
            """LMSSectionIdentifier,SourceSystemIdentifier,SubmissionType,SourceSystem
104,112,['online_upload'],Canvas"""
        )

        assignments_df = pd.read_csv(data)

        # Act
        assignments_df, submission_types_df = split(assignments_df)  # type: ignore

        return assignments_df, submission_types_df

    def it_should_map_112_online_upload_to_submission_types(
        when_splitting_the_assignments,
    ):
        _, df = when_splitting_the_assignments

        mask = (
            (df["SourceSystemIdentifier"] == 112)
            & (df["SourceSystem"] == "Canvas")
            & (df["SubmissionType"] == "online_upload")
        )

        assert df[mask].shape[0] == 1


def describe_given_there_are_no_assignments():
    @pytest.fixture
    def when_splitting_the_assignments():
        # Arrange
        assignments_df = pd.DataFrame()

        # Act
        assignments_df, submission_types_df = split(assignments_df)  # type: ignore

        return assignments_df, submission_types_df

    def it_should_create_empty_assignments_DataFrame(when_splitting_the_assignments):
        df, _ = when_splitting_the_assignments

        assert df.empty

    def it_should_create_empty_submission_types_DataFrame(
        when_splitting_the_assignments,
    ):
        _, df = when_splitting_the_assignments

        assert df.empty
