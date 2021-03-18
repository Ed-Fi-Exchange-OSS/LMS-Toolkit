# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Tuple
from unittest.mock import MagicMock

import pandas as pd
import pytest

from edfi_lms_ds_loader.helpers.constants import Table
from edfi_lms_ds_loader import df_to_db

SOURCE_SYSTEM = "google"


def describe_given_a_resource_that_is_not_a_child_of_section() -> None:
    @pytest.fixture
    def when_uploading_assignments() -> Tuple[MagicMock, pd.DataFrame]:
        # Arrange
        adapter_mock = MagicMock()

        df = pd.DataFrame([{"SourceSystem": SOURCE_SYSTEM}])

        # Act
        df_to_db.upload_file(adapter_mock, df, Table.USER)

        return adapter_mock, df

    def it_disables_the_natural_key_index(when_uploading_assignments) -> None:
        adapter_mock, _ = when_uploading_assignments
        adapter_mock.disable_staging_natural_key_index.assert_called_with(Table.USER)

    def it_truncates_the_staging_table(when_uploading_assignments) -> None:
        adapter_mock, _ = when_uploading_assignments
        adapter_mock.truncate_staging_table.assert_called_with(Table.USER)

    def it_re_enables_natural_key_index(when_uploading_assignments) -> None:
        adapter_mock, _ = when_uploading_assignments
        adapter_mock.enable_staging_natural_key_index.assert_called_with(Table.USER)

    def it_inserts_into_staging_table(when_uploading_assignments) -> None:
        adapter_mock, df = when_uploading_assignments
        adapter_mock.insert_into_staging.assert_called_with(df, Table.USER)

    def it_inserts_into_production_table(when_uploading_assignments) -> None:
        adapter_mock, _ = when_uploading_assignments
        adapter_mock.insert_new_records_to_production.assert_called_with(
            Table.USER, ["SourceSystem"]
        )

    def it_updates_production_table(when_uploading_assignments) -> None:
        adapter_mock, _ = when_uploading_assignments
        adapter_mock.copy_updates_to_production.assert_called_with(
            Table.USER, ["SourceSystem"]
        )

    def it_soft_deletes_from_production_table(when_uploading_assignments) -> None:
        adapter_mock, _ = when_uploading_assignments
        adapter_mock.soft_delete_from_production.assert_called_with(
            Table.USER, SOURCE_SYSTEM
        )


def describe_given_uploading_assignments() -> None:
    # NB: having difficulty with mocks when `upload_assignments()` - I can't
    # detect the first mock call, to the Assignments table. The assertions only
    # pass on the `AssignmentSubmissionType` calls. Therefore only checking on
    # the submission types when directly running `upload_assignments()`. Will create a separate fixture
    # for testing the "private" method `_upload_assignments`.

    @pytest.fixture
    def when_uploading_assignments_after_split() -> Tuple[MagicMock, pd.DataFrame]:
        # Arrange
        adapter_mock = MagicMock()

        description = "".join(["1"] * 1025)

        assignments_df = pd.DataFrame(
            [{"SourceSystem": SOURCE_SYSTEM, "AssignmentDescription": description}]
        )

        # Act
        df_to_db._upload_assignments(adapter_mock, assignments_df)

        return adapter_mock, assignments_df

    def it_trims_AssignmentDescription_to_1024_chars(
        when_uploading_assignments_after_split
    ) -> None:
        _, assignment_df = when_uploading_assignments_after_split

        assert len(assignment_df.iloc[0]["AssignmentDescription"]) == 1024

    def it_disables_assignments_natural_key(when_uploading_assignments_after_split) -> None:
        adapter_mock, _ = when_uploading_assignments_after_split

        adapter_mock.disable_staging_natural_key_index.assert_called_with(
            Table.ASSIGNMENT
        )

    def it_truncates_assignments_staging_table(when_uploading_assignments_after_split) -> None:
        adapter_mock, _ = when_uploading_assignments_after_split

        adapter_mock.truncate_staging_table.assert_called_with(
            Table.ASSIGNMENT
        )

    def it_inserts_assignments_into_staging(when_uploading_assignments_after_split) -> None:
        adapter_mock, assignments_df = when_uploading_assignments_after_split

        adapter_mock.insert_into_staging.assert_called_with(
            assignments_df, Table.ASSIGNMENT
        )

    def it_inserts_assignments_into_production_table(
        when_uploading_assignments_after_split
    ) -> None:
        adapter_mock, assignments_df = when_uploading_assignments_after_split

        adapter_mock.insert_new_records_to_production_for_section.assert_called_with(
            Table.ASSIGNMENT, ["SourceSystem", "AssignmentDescription"]
        )

    def it_soft_deletes_assignments_in_production_table(
        when_uploading_assignments_after_split
    ) -> None:
        adapter_mock, _ = when_uploading_assignments_after_split

        adapter_mock.soft_delete_from_production.assert_called_with(Table.ASSIGNMENT, SOURCE_SYSTEM)

    def it_re_enables_assignments_natural_key(when_uploading_assignments_after_split) -> None:
        adapter_mock, _ = when_uploading_assignments_after_split

        adapter_mock.enable_staging_natural_key_index.assert_called_with(
            Table.ASSIGNMENT
        )

    # Assignment Submission Types
    @pytest.fixture
    def when_uploading_assignments(mocker) -> Tuple[MagicMock, pd.DataFrame]:
        # Arrange
        adapter_mock = MagicMock()

        # NB: this set of tests also handles the case where
        # AssignmentDescription has not been set, ensuring that we don't have an
        # error when we try to trim that field down to 1024 characters.

        assignments_df = pd.DataFrame(
            [{"SourceSystem": SOURCE_SYSTEM}], columns=["SourceSystem", "AssignmentDescription"]
        )
        submissions_df = pd.DataFrame(
            [{"SubmissionType": "whatever", "SourceSystem": SOURCE_SYSTEM}]
        )
        response = (assignments_df, submissions_df)

        mocker.patch(
            "edfi_lms_ds_loader.helpers.assignment_splitter.split",
            return_value=response,
        )

        # Act
        df_to_db.upload_assignments(adapter_mock, assignments_df)

        return adapter_mock, submissions_df

    def it_disables_submission_type_natural_key(mocker, when_uploading_assignments) -> None:
        adapter_mock, _ = when_uploading_assignments

        adapter_mock.disable_staging_natural_key_index.assert_called_with(
            Table.ASSIGNMENT_SUBMISSION_TYPES
        )

    def it_truncates_submission_types_staging_table(mocker, when_uploading_assignments) -> None:
        adapter_mock, submissions_df = when_uploading_assignments

        adapter_mock.truncate_staging_table.assert_called_with(
            Table.ASSIGNMENT_SUBMISSION_TYPES
        )

    def it_inserts_submission_types_into_staging(mocker, when_uploading_assignments) -> None:
        adapter_mock, submissions_df = when_uploading_assignments

        adapter_mock.insert_into_staging.assert_called_with(
            submissions_df, Table.ASSIGNMENT_SUBMISSION_TYPES
        )

    def it_inserts_submission_types_into_production_table(
        mocker, when_uploading_assignments
    ) -> None:
        adapter_mock, _ = when_uploading_assignments

        adapter_mock.insert_new_submission_types.assert_called_once()

    def it_soft_deletes_submission_types_in_production_table(
        mocker, when_uploading_assignments
    ) -> None:
        adapter_mock, _ = when_uploading_assignments

        adapter_mock.soft_delete_removed_submission_types.assert_called_once()

    def it_re_enables_submission_type_natural_key(mocker, when_uploading_assignments) -> None:
        adapter_mock, _ = when_uploading_assignments

        adapter_mock.enable_staging_natural_key_index.assert_called_with(
            Table.ASSIGNMENT_SUBMISSION_TYPES
        )
