# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict, Tuple

import pandas as pd
import pytest
from unittest.mock import MagicMock, Mock

from edfi_lms_ds_loader import migrator
from edfi_lms_ds_loader.helpers.argparser import MainArguments
from edfi_lms_ds_loader.loader_facade import run_loader


def describe_when_uploading_extractor_files() -> None:
    def describe_given_no_errors_occur() -> None:
        @pytest.fixture
        def fixture(mocker) -> Tuple[Dict[str, MagicMock], Dict[str, pd.DataFrame]]:
            # Arrange
            args_mock = MagicMock(spec=MainArguments)
            db_engine_mock = MagicMock()
            args_mock.get_db_engine.return_value = db_engine_mock

            args_mock.csv_path = "/some/path"

            db_adapter_mock = Mock()
            db_adapter_mock.get_processed_files = Mock(
                return_value=set(["FullPathOne"])
            )

            args_mock.get_db_operations_adapter.return_value = db_adapter_mock

            migrator_mock = MagicMock(spec=migrator.migrate)
            mocker.patch("edfi_lms_ds_loader.migrator.migrate", migrator_mock)

            fake_df_users = pd.DataFrame({"generic_df": [1, 2, 3]})
            mocker.patch(
                "edfi_lms_file_utils.file_reader.read_users_file",
                return_value=fake_df_users,
            )

            fake_df_sections = pd.DataFrame([{"SourceSystemIdentifier": "a"}])
            mocker.patch(
                "edfi_lms_file_utils.file_reader.read_sections_file",
                return_value=fake_df_sections,
            )

            mocker.patch(
                "edfi_lms_ds_loader.loader_facade._get_sections_df",
                return_value=fake_df_sections,
            )

            fake_df_assignments = pd.DataFrame(
                [
                    {"LMSSectionSourceSystemIdentifier": "a"},
                    {"SourceSystemIdentifier": "b"},
                ]
            )
            mocker.patch(
                "edfi_lms_ds_loader.loader_facade._get_assignments_df",
                return_value=fake_df_assignments,
            )

            mocker.patch(
                "edfi_lms_file_utils.file_reader.read_assignments_file",
                return_value=fake_df_assignments,
            )

            fake_df_section_associations = pd.DataFrame([{"associations": "b"}])
            mocker.patch(
                "edfi_lms_file_utils.file_reader.read_section_associations_file",
                return_value=fake_df_section_associations,
            )

            fake_df_section_activities = pd.DataFrame([{"activities": "b"}])
            mocker.patch(
                "edfi_lms_file_utils.file_reader.read_section_activities_file",
                return_value=fake_df_section_activities,
            )

            fake_df_assignment_submissions = pd.DataFrame([{"submissions": "b"}])
            mocker.patch(
                "edfi_lms_file_utils.file_reader.read_submissions_file",
                return_value=fake_df_assignment_submissions,
            )

            mock_upload_file = mocker.patch("edfi_lms_ds_loader.df_to_db.upload_file")
            mock_upload_assignments_file = mocker.patch(
                "edfi_lms_ds_loader.df_to_db.upload_assignments"
            )
            mock_upload_section_associations_file = mocker.patch(
                "edfi_lms_ds_loader.df_to_db.upload_section_associations"
            )
            mock_upload_section_activities_file = mocker.patch(
                "edfi_lms_ds_loader.df_to_db.upload_section_activities"
            )
            mock_upload_assignment_submissions_file = mocker.patch(
                "edfi_lms_ds_loader.df_to_db.upload_assignment_submissions"
            )

            mocks = {
                "migrate": migrator_mock,
                "get_db_operations_adapter": db_adapter_mock,
                "get_db_engine": db_engine_mock,
                "upload_file": mock_upload_file,
                "upload_assignments_file": mock_upload_assignments_file,
                "upload_section_associations_file": mock_upload_section_associations_file,
                "upload_section_activities_file": mock_upload_section_activities_file,
                "upload_assignment_submissions_file": mock_upload_assignment_submissions_file,
            }

            dfs = {
                "users": fake_df_users,
                "sections": fake_df_sections,
                "assignments": fake_df_assignments,
                "section_associations": fake_df_section_associations,
                "section_activities": fake_df_section_activities,
                "assignment_submissions": fake_df_assignment_submissions,
            }

            file_repository_users_mock = Mock(return_value=["fileOne", "fileTwo"])
            mocker.patch(
                "edfi_lms_file_utils.file_repository.get_sections_file_paths",
                file_repository_users_mock,
            )

            file_repository_users_mock = Mock(return_value=["fileFour", "fileSix"])
            mocker.patch(
                "edfi_lms_file_utils.file_repository.get_users_file_paths",
                file_repository_users_mock,
            )

            file_repository_assignments_mock = Mock(
                return_value=["fileSeven", "fileEighth"]
            )
            mocker.patch(
                "edfi_lms_file_utils.file_repository.get_assignments_file_paths",
                file_repository_assignments_mock,
            )

            file_repository_section_associations_mock = Mock(
                return_value=["fileNine", "fileTen"]
            )
            mocker.patch(
                "edfi_lms_file_utils.file_repository.get_section_associations_file_paths",
                file_repository_section_associations_mock,
            )

            file_repository_assignment_submissions_mock = Mock(
                return_value=["fileEleven", "fileTwelve"]
            )
            mocker.patch(
                "edfi_lms_file_utils.file_repository.get_submissions_file_paths",
                file_repository_assignment_submissions_mock,
            )

            file_repository_section_activities_mock = Mock(
                return_value=["file13", "file14"]
            )
            mocker.patch(
                "edfi_lms_file_utils.file_repository.get_section_activities_file_paths",
                file_repository_section_activities_mock,
            )

            # Act
            run_loader(args_mock)

            # Return the mock objects for examination
            return (mocks, dfs)

        def it_runs_migrations(mocker, fixture) -> None:
            mocks, _ = fixture

            mocks["migrate"].assert_called_once_with(mocks["get_db_engine"])

        def it_uploads_users(mocker, fixture) -> None:
            mocks, dfs = fixture

            sections_call = mocks["upload_file"].call_args_list[0][0]
            assert sections_call[0] is mocks["get_db_operations_adapter"]
            assert sections_call[1] is dfs["users"]
            assert sections_call[2] == "LMSUser"

        def it_uploads_sections(mocker, fixture) -> None:
            mocks, dfs = fixture

            # call_args_list[1] means second call, the one for sections
            print(mocks["upload_file"].call_args_list)
            sections_call = mocks["upload_file"].call_args_list[2][0]
            assert sections_call[0] is mocks["get_db_operations_adapter"]
            assert sections_call[1] is dfs["sections"]
            assert sections_call[2] == "LMSSection"

        def it_uploads_assignments(mocker, fixture) -> None:
            mocks, dfs = fixture

            mocks["upload_assignments_file"].assert_called_with(
                mocks["get_db_operations_adapter"], dfs["assignments"]
            )

        def it_uploads_section_associations(mocker, fixture) -> None:
            mocks, dfs = fixture

            mocks["upload_section_associations_file"].assert_called_with(
                mocks["get_db_operations_adapter"], dfs["section_associations"]
            )

        def it_uploads_section_activities(mocker, fixture) -> None:
            mocks, dfs = fixture

            mocks["upload_section_activities_file"].assert_called_with(
                mocks["get_db_operations_adapter"], dfs["section_activities"]
            )

        def it_uploads_assignment_submissions(mocker, fixture) -> None:
            mocks, dfs = fixture

            mocks["upload_assignment_submissions_file"].assert_called_with(
                mocks["get_db_operations_adapter"], dfs["assignment_submissions"]
            )

    def describe_given_users_file_read_fails() -> None:
        def it_bubbles_up_the_error(mocker) -> None:
            # Arrange
            args_mock = MagicMock(spec=MainArguments)
            db_engine_mock = Mock()
            args_mock.get_db_engine.return_value = db_engine_mock

            args_mock.csv_path = "/some/path"

            db_adapter_mock = Mock()
            db_adapter_mock.get_processed_files = Mock(return_value=set(["fileOne"]))
            args_mock.get_db_operations_adapter.return_value = db_adapter_mock

            migrator_mock = MagicMock(spec=migrator.migrate)
            mocker.patch("edfi_lms_ds_loader.migrator.migrate", migrator_mock)

            def __raise(csv_path) -> None:
                raise Exception("bad things")

            mocker.patch(
                "edfi_lms_file_utils.file_reader.read_users_file", side_effect=__raise
            )

            file_repository_mock = Mock(return_value=["fileOne", "fileThree"])
            mocker.patch(
                "edfi_lms_file_utils.file_repository.get_users_file_paths",
                file_repository_mock,
            )

            # Act
            with pytest.raises(Exception):
                run_loader(args_mock)

    # Since we're not doing anything special to have that error bubble up,
    # additional tests for exceptions on other methods would not add much value
    # here.
