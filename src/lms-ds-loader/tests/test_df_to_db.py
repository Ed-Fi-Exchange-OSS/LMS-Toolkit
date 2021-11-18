# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Tuple
from unittest.mock import MagicMock, patch, call

import pandas as pd
import pytest

from edfi_lms_ds_loader.helpers.constants import Table
from edfi_lms_ds_loader import df_to_db
from edfi_lms_ds_loader.Sql_lms_operations import SqlLmsOperations

SOURCE_SYSTEM = "google"


def describe_given_a_resource_that_is_not_a_child_of_section_or_user() -> None:
    @pytest.fixture
    def when_uploading_users() -> Tuple[MagicMock, pd.DataFrame, MagicMock, MagicMock]:
        # Arrange
        adapter_mock = MagicMock()
        db_adapter_insert_method_mock = MagicMock()
        db_adapter_delete_method_mock = MagicMock()
        df = pd.DataFrame([{"SourceSystem": SOURCE_SYSTEM}])

        # Act
        df_to_db.upload_file(
            adapter_mock,
            df,
            Table.USER,
            db_adapter_insert_method_mock,
            db_adapter_delete_method_mock,
        )

        return (
            adapter_mock,
            df,
            db_adapter_insert_method_mock,
            db_adapter_delete_method_mock,
        )

    def it_disables_the_natural_key_index(when_uploading_users) -> None:
        adapter_mock, _, _, _ = when_uploading_users
        assert adapter_mock.disable_staging_natural_key_index.call_args_list == [
            call(Table.USER)
        ]

    def it_truncates_the_staging_table(when_uploading_users) -> None:
        adapter_mock, _, _, _ = when_uploading_users
        assert adapter_mock.truncate_staging_table.call_args_list == [call(Table.USER)]

    def it_re_enables_natural_key_index(when_uploading_users) -> None:
        adapter_mock, _, _, _ = when_uploading_users
        assert adapter_mock.enable_staging_natural_key_index.call_args_list == [
            call(Table.USER)
        ]

    def it_inserts_into_staging_table(when_uploading_users) -> None:
        adapter_mock, df, _, _ = when_uploading_users
        assert adapter_mock.insert_into_staging.call_args_list == [call(df, Table.USER)]

    def it_inserts_into_production_table(when_uploading_users) -> None:
        adapter_mock, _, db_adapter_insert_method_mock, _ = when_uploading_users
        assert db_adapter_insert_method_mock.call_args_list == [
            call(adapter_mock, Table.USER, ["SourceSystem"])
        ]

    def it_updates_production_table(when_uploading_users) -> None:
        adapter_mock, _, _, _ = when_uploading_users
        assert adapter_mock.copy_updates_to_production.call_args_list == [
            call(Table.USER, ["SourceSystem"])
        ]

    def it_soft_deletes_from_production_table(when_uploading_users) -> None:
        adapter_mock, _, _, db_adapter_delete_method_mock = when_uploading_users
        assert db_adapter_delete_method_mock.call_args_list == [
            call(adapter_mock, Table.USER, SOURCE_SYSTEM)
        ]


def describe_given_assignments_description_too_long() -> None:
    @pytest.fixture
    def when_uploading_assignments_after_split(
        mocker,
    ) -> Tuple[MagicMock, pd.DataFrame]:
        # Arrange
        adapter_mock = MagicMock()

        assignments_df = pd.DataFrame(
            [
                {
                    "SourceSystem": SOURCE_SYSTEM,
                    "AssignmentDescription": "".join(["1"] * 1025),
                }
            ]
        )

        submissions_df = pd.DataFrame(
            [{"SubmissionType": "whatever", "SourceSystem": SOURCE_SYSTEM}]
        )
        response = (assignments_df, submissions_df)

        mocker.patch(
            "edfi_lms_ds_loader.df_to_db.assignment_splitter.split",
            return_value=response,
        )

        # Act
        df_to_db.upload_assignments(adapter_mock, assignments_df)

        return adapter_mock, assignments_df

    def it_trims_AssignmentDescription_to_1024_chars(
        when_uploading_assignments_after_split,
    ) -> None:
        _, assignment_df = when_uploading_assignments_after_split

        assert len(assignment_df.iloc[0]["AssignmentDescription"]) == 1024


# Assignment Submission Types
def describe_when_uploading_assignments_with_no_submission_type() -> None:
    def it_should_only_upload_the_assignments(mocker) -> None:
        # Arrange
        adapter_mock = MagicMock()

        # NB: this set of tests also handles the case where
        # AssignmentDescription has not been set, ensuring that we don't have an
        # error when we try to trim that field down to 1024 characters.

        assignments_df = pd.DataFrame(
            [{"SourceSystem": SOURCE_SYSTEM}],
            columns=["SourceSystem", "AssignmentDescription"],
        )
        submissions_df = pd.DataFrame()
        response = (assignments_df, submissions_df)

        mocker.patch(
            "edfi_lms_ds_loader.helpers.assignment_splitter.split",
            return_value=response,
        )

        # Act
        df_to_db.upload_assignments(adapter_mock, assignments_df)

        # Assert

        # Just make sure no error occurs


def describe_when_uploading_assignments() -> None:
    @pytest.fixture
    def when_uploading_assignments(
        mocker,
    ) -> Tuple[MagicMock, pd.DataFrame, pd.DataFrame]:
        # Arrange
        adapter_mock = MagicMock()

        # NB: this set of tests also handles the case where
        # AssignmentDescription has not been set, ensuring that we don't have an
        # error when we try to trim that field down to 1024 characters.

        assignments_df = pd.DataFrame(
            [{"SourceSystem": SOURCE_SYSTEM}],
            columns=["SourceSystem", "AssignmentDescription"],
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

        return adapter_mock, submissions_df, assignments_df

    def it_disables_submission_type_natural_key(
        mocker, when_uploading_assignments
    ) -> None:
        adapter_mock, _, _ = when_uploading_assignments

        assert adapter_mock.disable_staging_natural_key_index.call_args_list == [
            call(Table.ASSIGNMENT),
            call(Table.ASSIGNMENT_SUBMISSION_TYPES),
        ]

    def it_truncates_submission_types_staging_table(
        mocker, when_uploading_assignments
    ) -> None:
        adapter_mock, _, _ = when_uploading_assignments

        assert adapter_mock.truncate_staging_table.call_args_list == [
            call(Table.ASSIGNMENT),
            call(Table.ASSIGNMENT_SUBMISSION_TYPES),
        ]

    def it_inserts_submission_types_into_staging(
        mocker, when_uploading_assignments
    ) -> None:
        adapter_mock, submissions_df, assignments_df = when_uploading_assignments

        assert adapter_mock.insert_into_staging.call_args_list == [
            call(assignments_df, Table.ASSIGNMENT),
            call(submissions_df, Table.ASSIGNMENT_SUBMISSION_TYPES),
        ]

    def it_inserts_submission_types_into_production_table(
        mocker, when_uploading_assignments
    ) -> None:
        adapter_mock, _, _ = when_uploading_assignments

        assert adapter_mock.insert_new_submission_types.call_args_list == [call()]

    def it_soft_deletes_submission_types_in_production_table(
        mocker, when_uploading_assignments
    ) -> None:
        adapter_mock, _, _ = when_uploading_assignments

        assert adapter_mock.soft_delete_removed_submission_types.call_args_list == [
            call(SOURCE_SYSTEM)
        ]

    def it_unsoft_deletes_submission_types_in_production_table(
        mocker, when_uploading_assignments
    ) -> None:
        adapter_mock, _, _ = when_uploading_assignments

        assert adapter_mock.unsoft_delete_returned_submission_types.call_args_list == [
            call(SOURCE_SYSTEM)
        ]

    def it_re_enables_submission_type_natural_key(
        mocker, when_uploading_assignments
    ) -> None:
        adapter_mock, _, _ = when_uploading_assignments

        assert adapter_mock.enable_staging_natural_key_index.call_args_list == [
            call(Table.ASSIGNMENT),
            call(Table.ASSIGNMENT_SUBMISSION_TYPES),
        ]


def describe_given_empty_DataFrame() -> None:
    def describe_when_uploading_assignments() -> None:
        def it_should_not_do_anything() -> None:
            df_to_db.upload_assignments(MagicMock(), pd.DataFrame())

            # if no errors occurred then this worked

    def describe_when_uploading_sections_file() -> None:
        def it_should_not_do_anything() -> None:
            df_to_db.upload_file(
                MagicMock(),
                pd.DataFrame(),
                "LMSection",
                SqlLmsOperations.insert_new_records_to_production,
                SqlLmsOperations.soft_delete_from_production,
            )

            # if no errors occurred then this worked


def describe_when_uploading_section_associations() -> None:
    @pytest.fixture
    @patch(
        "edfi_lms_ds_loader.df_to_db.SqlLmsOperations.soft_delete_from_production_for_section_relation"
    )
    @patch(
        "edfi_lms_ds_loader.df_to_db.SqlLmsOperations.insert_new_records_to_production_for_section_and_user_relation"
    )
    def when_uploading_section_associations(
        insert_mock,
        delete_mock,
    ) -> Tuple[MagicMock, pd.DataFrame, MagicMock, MagicMock]:
        # Arrange
        adapter_mock = MagicMock()

        df = pd.DataFrame([{"SourceSystem": SOURCE_SYSTEM}])

        # Act
        df_to_db.upload_section_associations(adapter_mock, df)

        return adapter_mock, df, insert_mock, delete_mock

    def it_disables_the_natural_key_index(when_uploading_section_associations) -> None:
        adapter_mock, _, _, _ = when_uploading_section_associations
        assert adapter_mock.disable_staging_natural_key_index.call_args_list == [
            call(Table.SECTION_ASSOCIATION)
        ]

    def it_truncates_the_staging_table(when_uploading_section_associations) -> None:
        adapter_mock, _, _, _ = when_uploading_section_associations
        assert adapter_mock.truncate_staging_table.call_args_list == [
            call(Table.SECTION_ASSOCIATION)
        ]

    def it_re_enables_natural_key_index(when_uploading_section_associations) -> None:
        adapter_mock, _, _, _ = when_uploading_section_associations
        assert adapter_mock.enable_staging_natural_key_index.call_args_list == [
            call(Table.SECTION_ASSOCIATION)
        ]

    def it_inserts_into_staging_table(when_uploading_section_associations) -> None:
        adapter_mock, df, _, _ = when_uploading_section_associations
        assert adapter_mock.insert_into_staging.call_args_list == [
            call(df, Table.SECTION_ASSOCIATION)
        ]

    def it_inserts_into_production_table(when_uploading_section_associations) -> None:
        adapter_mock, _, insert_mock, _ = when_uploading_section_associations
        assert insert_mock.call_args_list == [
            call(adapter_mock, Table.SECTION_ASSOCIATION, ["SourceSystem"])
        ]

    def it_updates_production_table(when_uploading_section_associations) -> None:
        adapter_mock, _, _, _ = when_uploading_section_associations
        assert adapter_mock.copy_updates_to_production.call_args_list == [
            call(Table.SECTION_ASSOCIATION, ["SourceSystem"])
        ]

    def it_soft_deletes_from_production_table(
        when_uploading_section_associations,
    ) -> None:
        adapter_mock, _, _, delete_mock = when_uploading_section_associations
        assert delete_mock.call_args_list == [
            call(adapter_mock, Table.SECTION_ASSOCIATION, SOURCE_SYSTEM)
        ]


def describe_when_uploading_assignment_submissions() -> None:
    @pytest.fixture
    @patch(
        "edfi_lms_ds_loader.df_to_db.SqlLmsOperations.soft_delete_from_production_for_assignment_relation"
    )
    @patch(
        "edfi_lms_ds_loader.df_to_db.SqlLmsOperations.insert_new_records_to_production_for_assignment_and_user_relation"
    )
    def when_uploading_assignment_submissions(
        insert_mock,
        delete_mock,
    ) -> Tuple[MagicMock, pd.DataFrame, MagicMock, MagicMock]:
        # Arrange
        adapter_mock = MagicMock()

        df = pd.DataFrame([{"SourceSystem": SOURCE_SYSTEM}])

        # Act
        df_to_db.upload_assignment_submissions(adapter_mock, df)

        return adapter_mock, df, insert_mock, delete_mock

    def it_disables_the_natural_key_index(
        when_uploading_assignment_submissions,
    ) -> None:
        adapter_mock, _, _, _ = when_uploading_assignment_submissions
        assert adapter_mock.disable_staging_natural_key_index.call_args_list == [
            call(Table.ASSIGNMENT_SUBMISSION)
        ]

    def it_truncates_the_staging_table(when_uploading_assignment_submissions) -> None:
        adapter_mock, _, _, _ = when_uploading_assignment_submissions
        assert adapter_mock.truncate_staging_table.call_args_list == [
            call(Table.ASSIGNMENT_SUBMISSION)
        ]

    def it_re_enables_natural_key_index(when_uploading_assignment_submissions) -> None:
        adapter_mock, _, _, _ = when_uploading_assignment_submissions
        assert adapter_mock.enable_staging_natural_key_index.call_args_list == [
            call(Table.ASSIGNMENT_SUBMISSION)
        ]

    def it_inserts_into_staging_table(when_uploading_assignment_submissions) -> None:
        adapter_mock, df, _, _ = when_uploading_assignment_submissions
        assert adapter_mock.insert_into_staging.call_args_list == [
            call(df, Table.ASSIGNMENT_SUBMISSION)
        ]

    def it_inserts_into_production_table(when_uploading_assignment_submissions) -> None:
        adapter_mock, _, insert_mock, _ = when_uploading_assignment_submissions
        assert insert_mock.call_args_list == [
            call(adapter_mock, Table.ASSIGNMENT_SUBMISSION, ["SourceSystem"])
        ]

    def it_updates_production_table(when_uploading_assignment_submissions) -> None:
        adapter_mock, _, _, _ = when_uploading_assignment_submissions
        assert adapter_mock.copy_updates_to_production.call_args_list == [
            call(Table.ASSIGNMENT_SUBMISSION, ["SourceSystem"])
        ]

    def it_soft_deletes_from_production_table(
        when_uploading_assignment_submissions,
    ) -> None:
        adapter_mock, _, _, delete_mock = when_uploading_assignment_submissions
        assert delete_mock.call_args_list == [
            call(adapter_mock, Table.ASSIGNMENT_SUBMISSION, SOURCE_SYSTEM)
        ]


def describe_when_uploading_section_activities() -> None:
    @pytest.fixture
    @patch(
        "edfi_lms_ds_loader.df_to_db.SqlLmsOperations.soft_delete_from_production_for_section_relation"
    )
    @patch(
        "edfi_lms_ds_loader.df_to_db.SqlLmsOperations.insert_new_records_to_production_for_section_and_user_relation"
    )
    def when_uploading_section_activities(
        insert_mock,
        delete_mock,
    ) -> Tuple[MagicMock, pd.DataFrame, MagicMock, MagicMock]:
        # Arrange
        adapter_mock = MagicMock()

        df = pd.DataFrame([{"SourceSystem": SOURCE_SYSTEM}])

        # Act
        df_to_db.upload_section_activities(adapter_mock, df)

        return adapter_mock, df, insert_mock, delete_mock

    def it_disables_the_natural_key_index(when_uploading_section_activities) -> None:
        adapter_mock, _, _, _ = when_uploading_section_activities
        assert adapter_mock.disable_staging_natural_key_index.call_args_list == [
            call(Table.SECTION_ACTIVITY)
        ]

    def it_truncates_the_staging_table(when_uploading_section_activities) -> None:
        adapter_mock, _, _, _ = when_uploading_section_activities
        assert adapter_mock.truncate_staging_table.call_args_list == [
            call(Table.SECTION_ACTIVITY)
        ]

    def it_re_enables_natural_key_index(when_uploading_section_activities) -> None:
        adapter_mock, _, _, _ = when_uploading_section_activities
        assert adapter_mock.enable_staging_natural_key_index.call_args_list == [
            call(Table.SECTION_ACTIVITY)
        ]

    def it_inserts_into_staging_table(when_uploading_section_activities) -> None:
        adapter_mock, df, _, _ = when_uploading_section_activities
        assert adapter_mock.insert_into_staging.call_args_list == [
            call(df, Table.SECTION_ACTIVITY)
        ]

    def it_inserts_into_production_table(when_uploading_section_activities) -> None:
        adapter_mock, _, insert_mock, _ = when_uploading_section_activities
        assert insert_mock.call_args_list == [
            call(adapter_mock, Table.SECTION_ACTIVITY, ["SourceSystem"])
        ]

    def it_updates_production_table(when_uploading_section_activities) -> None:
        adapter_mock, _, _, _ = when_uploading_section_activities
        assert adapter_mock.copy_updates_to_production.call_args_list == [
            call(Table.SECTION_ACTIVITY, ["SourceSystem"])
        ]

    def it_soft_deletes_from_production_table(
        when_uploading_section_activities,
    ) -> None:
        adapter_mock, _, _, delete_mock = when_uploading_section_activities
        assert delete_mock.call_args_list == [
            call(adapter_mock, Table.SECTION_ACTIVITY, SOURCE_SYSTEM)
        ]


def describe_when_uploading_system_activities() -> None:
    @pytest.fixture
    @patch(
        "edfi_lms_ds_loader.df_to_db.SqlLmsOperations.soft_delete_from_production"
    )
    @patch(
        "edfi_lms_ds_loader.df_to_db.SqlLmsOperations.insert_new_records_to_production_for_user_relation"
    )
    def when_uploading_system_activities(
        insert_mock,
        delete_mock,
    ) -> Tuple[MagicMock, pd.DataFrame, MagicMock, MagicMock]:
        # Arrange
        adapter_mock = MagicMock()

        df = pd.DataFrame([{"SourceSystem": SOURCE_SYSTEM}])

        # Act
        df_to_db.upload_system_activities(adapter_mock, df)

        return adapter_mock, df, insert_mock, delete_mock

    def it_disables_the_natural_key_index(when_uploading_system_activities) -> None:
        adapter_mock, _, _, _ = when_uploading_system_activities
        assert adapter_mock.disable_staging_natural_key_index.call_args_list == [
            call(Table.SYSTEM_ACTIVITY)
        ]

    def it_truncates_the_staging_table(when_uploading_system_activities) -> None:
        adapter_mock, _, _, _ = when_uploading_system_activities
        assert adapter_mock.truncate_staging_table.call_args_list == [
            call(Table.SYSTEM_ACTIVITY)
        ]

    def it_re_enables_natural_key_index(when_uploading_system_activities) -> None:
        adapter_mock, _, _, _ = when_uploading_system_activities
        assert adapter_mock.enable_staging_natural_key_index.call_args_list == [
            call(Table.SYSTEM_ACTIVITY)
        ]

    def it_inserts_into_staging_table(when_uploading_system_activities) -> None:
        adapter_mock, df, _, _ = when_uploading_system_activities
        assert adapter_mock.insert_into_staging.call_args_list == [
            call(df, Table.SYSTEM_ACTIVITY)
        ]

    def it_inserts_into_production_table(when_uploading_system_activities) -> None:
        adapter_mock, _, insert_mock, _ = when_uploading_system_activities
        assert insert_mock.call_args_list == [
            call(adapter_mock, Table.SYSTEM_ACTIVITY, ["SourceSystem"])
        ]

    def it_updates_production_table(when_uploading_system_activities) -> None:
        adapter_mock, _, _, _ = when_uploading_system_activities
        assert adapter_mock.copy_updates_to_production.call_args_list == [
            call(Table.SYSTEM_ACTIVITY, ["SourceSystem"])
        ]

    def it_soft_deletes_from_production_table(
        when_uploading_system_activities,
    ) -> None:
        adapter_mock, _, _, delete_mock = when_uploading_system_activities
        assert delete_mock.call_args_list == [
            call(adapter_mock, Table.SYSTEM_ACTIVITY, SOURCE_SYSTEM)
        ]


def describe_when_uploading_attendance_events() -> None:
    @pytest.fixture
    @patch(
        "edfi_lms_ds_loader.df_to_db.SqlLmsOperations.soft_delete_from_production_for_section_relation"
    )
    @patch(
        "edfi_lms_ds_loader.df_to_db.SqlLmsOperations.insert_new_records_to_production_for_attendance_events"
    )
    def when_uploading_attendance_events(
        insert_mock,
        delete_mock,
    ) -> Tuple[MagicMock, MagicMock, pd.DataFrame, MagicMock]:
        # Arrange
        adapter_mock = MagicMock()

        attendance_df = pd.DataFrame([{"SourceSystem": SOURCE_SYSTEM}])

        # Act
        df_to_db.upload_attendance_events(adapter_mock, attendance_df)

        return adapter_mock, insert_mock, attendance_df, delete_mock

    def it_disables_natural_key_index(when_uploading_attendance_events) -> None:
        adapter_mock, _, _, _ = when_uploading_attendance_events

        assert adapter_mock.disable_staging_natural_key_index.call_args_list == [
            call(Table.ATTENDANCE)
        ]

    def it_truncates_staging_table(when_uploading_attendance_events) -> None:
        adapter_mock, _, _, _ = when_uploading_attendance_events

        assert adapter_mock.truncate_staging_table.call_args_list == [
            call(Table.ATTENDANCE)
        ]

    def it_inserts_into_staging(when_uploading_attendance_events) -> None:
        adapter_mock, _, attendance_df, _ = when_uploading_attendance_events

        assert adapter_mock.insert_into_staging.call_args_list == [
            call(attendance_df, Table.ATTENDANCE),
        ]

    def it_inserts_into_production_table(when_uploading_attendance_events) -> None:
        adapter_mock, insert_mock, _, _ = when_uploading_attendance_events

        assert insert_mock.call_args_list == [
            call(adapter_mock, Table.ATTENDANCE, ["SourceSystem"])
        ]

    def it_updates_production_table(when_uploading_attendance_events) -> None:
        adapter_mock, _, _, _ = when_uploading_attendance_events

        assert adapter_mock.copy_updates_to_production.call_args_list == [
            call(Table.ATTENDANCE, ["SourceSystem"])
        ]

    def it_soft_deletes_from_production_table(when_uploading_attendance_events) -> None:
        adapter_mock, _, _, delete_mock = when_uploading_attendance_events

        assert delete_mock.call_args_list == [
            call(adapter_mock, Table.ATTENDANCE, SOURCE_SYSTEM)
        ]

    def it_re_enables_attendance_events_natural_key(
        when_uploading_attendance_events,
    ) -> None:
        adapter_mock, _, _, _ = when_uploading_attendance_events

        assert adapter_mock.enable_staging_natural_key_index.call_args_list == [
            call(Table.ATTENDANCE)
        ]
