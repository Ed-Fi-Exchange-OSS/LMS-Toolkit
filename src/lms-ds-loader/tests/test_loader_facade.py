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


def describe_when_uploading_extractor_files():
    def describe_given_no_errors_occur():
        @pytest.fixture
        def fixture(mocker) -> Tuple[Dict[str, MagicMock], Dict[str, pd.DataFrame]]:
            # Arrange
            args_mock = MagicMock(spec=MainArguments)
            db_engine_mock = MagicMock()
            args_mock.get_db_engine.return_value = db_engine_mock

            args_mock.csv_path = "/some/path"

            db_adapter_mock = MagicMock()
            args_mock.get_db_operations_adapter.return_value = db_adapter_mock

            migrator_mock = MagicMock(spec=migrator.migrate)
            mocker.patch("edfi_lms_ds_loader.migrator.migrate", migrator_mock)

            df_users = pd.DataFrame({"users": [1]})
            mocker.patch(
                "edfi_lms_file_utils.file_reader.get_all_users", return_value=df_users
            )

            df_sections = pd.DataFrame([{"sections": "a"}])
            mocker.patch(
                "edfi_lms_file_utils.file_reader.get_all_sections",
                return_value=df_sections,
            )

            df_assignments = pd.DataFrame([{"assignments": "b"}])
            mocker.patch(
                "edfi_lms_file_utils.file_reader.get_all_assignments",
                return_value=df_assignments,
            )

            mock_upload_file = mocker.patch("edfi_lms_ds_loader.df_to_db.upload_file")
            mock_upload_assignments = mocker.patch(
                "edfi_lms_ds_loader.df_to_db.upload_assignments"
            )

            mocks = {
                "migrate": migrator_mock,
                "get_db_operations_adapter": db_adapter_mock,
                "get_db_engine": db_engine_mock,
                "upload_file": mock_upload_file,
                "upload_assignments": mock_upload_assignments,
            }

            dfs = {
                "users": df_users,
                "sections": df_sections,
                "assignments": df_assignments,
            }

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

            # twice - once for sections, once for users
            assert mocks["upload_file"].call_count == 2

            # call_args_list[1] means second call, the one for sections
            sections_call = mocks["upload_file"].call_args_list[1][0]
            assert sections_call[0] is mocks["get_db_operations_adapter"]
            assert sections_call[1] is dfs["sections"]
            assert sections_call[2] == "LMSSection"

        def it_uploads_assignments(mocker, fixture) -> None:
            mocks, dfs = fixture

            mocks["upload_assignments"].assert_called_with(
                mocks["get_db_operations_adapter"], dfs["assignments"]
            )

    def describe_given_users_file_read_fails():
        def it_bubbles_up_the_error(mocker):
            # Arrange
            args_mock = MagicMock(spec=MainArguments)
            db_engine_mock = Mock()
            args_mock.get_db_engine.return_value = db_engine_mock

            args_mock.csv_path = "/some/path"

            db_adapter_mock = Mock()
            args_mock.get_db_operations_adapter.return_value = db_adapter_mock

            migrator_mock = MagicMock(spec=migrator.migrate)
            mocker.patch("edfi_lms_ds_loader.migrator.migrate", migrator_mock)

            def __raise(csv_path):
                raise Exception("bad things")

            mocker.patch(
                "edfi_lms_file_utils.file_reader.get_all_users", side_effect=__raise
            )

            # Act
            with pytest.raises(Exception):
                run_loader(args_mock)

    # Since we're not doing anything special to have that error bubble up,
    # additional tests for exceptions on other methods would not add much value
    # here.
