# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest
from unittest.mock import MagicMock, Mock

from edfi_lms_ds_loader import migrator
from edfi_lms_ds_loader.helpers.argparser import MainArguments
from edfi_lms_ds_loader.loader_facade import run_loader
from edfi_lms_ds_loader import df_to_db


def describe_when_uploading_extractor_files():
    def describe_given_no_errors_occur():
        @pytest.fixture
        def fixture(mocker):
            # Arrange
            args_mock = MagicMock(spec=MainArguments)
            db_engine_mock = Mock()
            args_mock.get_db_engine.return_value = db_engine_mock

            args_mock.csv_path = "/some/path"

            db_adapter_mock = Mock()
            args_mock.get_db_operations_adapter.return_value = db_adapter_mock

            migrator_mock = MagicMock(spec=migrator.migrate)
            mocker.patch("edfi_lms_ds_loader.migrator.migrate", migrator_mock)

            df_users = pd.DataFrame({"users": [1]})
            mocker.patch("edfi_lms_file_utils.file_reader.get_all_users", return_value=df_users)

            df_sections = pd.DataFrame([{"sections": "a"}])
            mocker.patch("edfi_lms_file_utils.file_reader.get_all_sections", return_value=df_sections)

            upload_mock = MagicMock(spec=df_to_db.upload_file)
            mocker.patch("edfi_lms_ds_loader.df_to_db.upload_file", upload_mock)

            # Act
            run_loader(args_mock)

            # Return the mock objects for examination
            return (db_engine_mock, migrator_mock, db_adapter_mock, df_users, df_sections, upload_mock)

        def it_runs_migrations(mocker, fixture):
            db_engine_mock, migrator_mock, _, _, _, _ = fixture

            migrator_mock.assert_called_once_with(db_engine_mock)

        def it_uploads_users(mocker, fixture):
            _, _, db_adapter_mock, df_users, _, upload_mock = fixture

            sections_call = upload_mock.call_args_list[0][0]
            assert sections_call[0] is db_adapter_mock
            assert sections_call[1] is df_users
            assert sections_call[2] == "LMSUser"

        def it_uploads_sections(mocker, fixture):
            _, _, db_adapter_mock, _, df_sections, upload_mock = fixture

            assert upload_mock.call_count == 2

            sections_call = upload_mock.call_args_list[1][0]
            assert sections_call[0] is db_adapter_mock
            assert sections_call[1] is df_sections
            assert sections_call[2] == "LMSSection"

    def describe_given_users_file_read_fails():
        @pytest.fixture
        def fixture(mocker):
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

            mocker.patch("edfi_lms_file_utils.file_reader.get_all_users", side_effect=__raise)

            df_sections = pd.DataFrame([{"sections": "a"}])
            mocker.patch("edfi_lms_file_utils.file_reader.get_all_sections", return_value=df_sections)

            upload_mock = MagicMock(spec=df_to_db.upload_file)
            mocker.patch("edfi_lms_ds_loader.df_to_db.upload_file", upload_mock)

            # Act
            run_loader(args_mock)

            # Return the mock objects for examination
            return (db_engine_mock, migrator_mock, upload_mock)

        def it_runs_migrations(mocker, fixture):
            db_engine_mock, migrator_mock, _ = fixture

            migrator_mock.assert_called_once_with(db_engine_mock)

        def it_does_not_upload_users(mocker, fixture):
            _, _, upload_mock = fixture

            assert upload_mock.call_count == 1

            call = upload_mock.call_args_list[0][0]

            assert call[2] != "LMSUser"

        def it_does_upload_sections(mocker, fixture):
            _, _, upload_mock = fixture

            call = upload_mock.call_args_list[0][0]

            assert call[2] == "LMSSection"

    def describe_given_section_file_read_fails():
        @pytest.fixture
        def fixture(mocker):
            # Arrange
            args_mock = MagicMock(spec=MainArguments)
            db_engine_mock = Mock()
            args_mock.get_db_engine.return_value = db_engine_mock

            args_mock.csv_path = "/some/path"

            db_adapter_mock = Mock()
            args_mock.get_db_operations_adapter.return_value = db_adapter_mock

            migrator_mock = MagicMock(spec=migrator.migrate)
            mocker.patch("edfi_lms_ds_loader.migrator.migrate", migrator_mock)

            df_users = pd.DataFrame({"users": [1]})
            mocker.patch("edfi_lms_file_utils.file_reader.get_all_users", return_value=df_users)

            def __raise(csv_path):
                raise Exception("bad things")

            mocker.patch("edfi_lms_file_utils.file_reader.get_all_sections", side_effect=__raise)

            upload_mock = MagicMock(spec=df_to_db.upload_file)
            mocker.patch("edfi_lms_ds_loader.df_to_db.upload_file", upload_mock)

            # Act
            run_loader(args_mock)

            # Return the mock objects for examination
            return (db_engine_mock, migrator_mock, db_adapter_mock, df_users, upload_mock)

        def it_runs_migrations(mocker, fixture):
            db_engine_mock, migrator_mock, _, _, _ = fixture

            migrator_mock.assert_called_once_with(db_engine_mock)

        def it_uploads_users(mocker, fixture):
            _, _, db_adapter_mock, df_users, upload_mock = fixture

            sections_call = upload_mock.call_args_list[0][0]
            assert sections_call[0] is db_adapter_mock
            assert sections_call[1] is df_users
            assert sections_call[2] == "LMSUser"

        def it_does_not_upload_sections(mocker, fixture):
            _, _, db_adapter_mock, _, upload_mock = fixture

            assert upload_mock.call_count == 1
