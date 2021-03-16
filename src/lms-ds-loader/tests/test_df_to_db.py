# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Tuple
from unittest.mock import Mock

import pandas as pd
import pytest

from edfi_lms_ds_loader.helpers.constants import Table
from edfi_lms_ds_loader import df_to_db

SOURCE_SYSTEM = "google"


def describe_given_a_dataframe() -> None:
    @pytest.fixture
    def when_uploading_it() -> Tuple[Mock, pd.DataFrame]:
        # Arrange
        adapter_mock = Mock()

        df = pd.DataFrame([{"SourceSystem": SOURCE_SYSTEM}])

        # Act
        df_to_db.upload_file(adapter_mock, df, Table.USER)

        return adapter_mock, df

    def it_disables_the_natural_key_index(when_uploading_it) -> None:
        adapter_mock, _ = when_uploading_it
        adapter_mock.disable_staging_natural_key_index.assert_called_with(Table.USER)

    def it_truncates_the_staging_table(when_uploading_it) -> None:
        adapter_mock, _ = when_uploading_it
        adapter_mock.truncate_staging_table.assert_called_with(Table.USER)

    def it_reenables_natural_key_index(when_uploading_it) -> None:
        adapter_mock, _ = when_uploading_it
        adapter_mock.enable_staging_natural_key_index.assert_called_with(Table.USER)

    def it_inserts_into_staging_table(when_uploading_it) -> None:
        adapter_mock, df = when_uploading_it
        adapter_mock.insert_into_staging.assert_called_with(df, Table.USER)

    def it_inserts_into_production_table(when_uploading_it) -> None:
        adapter_mock, _ = when_uploading_it
        adapter_mock.insert_new_records_to_production.assert_called_with(
            Table.USER, ["SourceSystem"]
        )

    def it_updates_production_table(when_uploading_it) -> None:
        adapter_mock, _ = when_uploading_it
        adapter_mock.copy_updates_to_production.assert_called_with(
            Table.USER, ["SourceSystem"]
        )

    def it_soft_deletes_from_production_table(when_uploading_it) -> None:
        adapter_mock, _ = when_uploading_it
        adapter_mock.soft_delete_from_production.assert_called_with(
            Table.USER, SOURCE_SYSTEM
        )


def describe_given_assignment_submission_types() -> None:
    @pytest.fixture
    def when_uploading_it(mocker) -> Tuple[Mock, Mock, pd.DataFrame, pd.DataFrame]:
        # Arrange
        adapter_mock = Mock()

        description = "".join(["1"] * 1025)

        assignments_df = pd.DataFrame(
            [{"SourceSystem": SOURCE_SYSTEM, "AssignmentDescription": description}]
        )
        submissions_df = pd.DataFrame([{"SubmissionType": "whatever"}])
        response = (assignments_df, submissions_df)
        mocker.patch(
            "edfi_lms_ds_loader.helpers.assignment_splitter.split",
            return_value=response,
        )

        # Mock the regular upload process, since it was tested already up above
        assignment_upload_mock = mocker.patch("edfi_lms_ds_loader.df_to_db.upload_file")

        # Act
        df_to_db.upload_assignments(adapter_mock, assignments_df)

        return adapter_mock, assignment_upload_mock, assignments_df, submissions_df

    def it_uploads_assignments(mocker, when_uploading_it) -> None:
        adapter_mock, assignment_upload_mock, assignments_df, _ = when_uploading_it

        assignment_upload_mock.assert_called_with(
            adapter_mock, assignments_df, Table.ASSIGNMENT
        )

    def it_disables_submission_type_natural_key(mocker, when_uploading_it) -> None:
        adapter_mock, _, _, _ = when_uploading_it

        adapter_mock.disable_staging_natural_key_index.assert_called_with(
            Table.ASSIGNMENT_SUBMISSION_TYPES
        )

    def it_truncates_AssignmentDescription_to_1024_chars(
        mocker, when_uploading_it
    ) -> None:
        _, _, assignment_df, _ = when_uploading_it

        assert len(assignment_df.iloc[0]["AssignmentDescription"]) == 1024

    def it_truncates_submission_types_staging_table(mocker, when_uploading_it) -> None:
        adapter_mock, _, _, submissions_df = when_uploading_it

        adapter_mock.truncate_staging_table.assert_called_with(
            Table.ASSIGNMENT_SUBMISSION_TYPES
        )

    def it_inserts_submission_types_into_staging(mocker, when_uploading_it) -> None:
        adapter_mock, _, _, submissions_df = when_uploading_it

        adapter_mock.insert_into_staging.assert_called_with(
            submissions_df, Table.ASSIGNMENT_SUBMISSION_TYPES
        )

    def it_inserts_submission_types_into_production_table(
        mocker, when_uploading_it
    ) -> None:
        adapter_mock, _, _, _ = when_uploading_it

        adapter_mock.insert_new_submission_types.assert_called_once()

    def it_soft_deletes_submission_types_in_production_table(
        mocker, when_uploading_it
    ) -> None:
        adapter_mock, _, _, _ = when_uploading_it

        adapter_mock.soft_delete_removed_submission_types.assert_called_once()

    def it_reenables_submission_type_natural_key(mocker, when_uploading_it) -> None:
        adapter_mock, _, _, _ = when_uploading_it

        adapter_mock.enable_staging_natural_key_index.assert_called_with(
            Table.ASSIGNMENT_SUBMISSION_TYPES
        )
