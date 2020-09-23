# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
import pytest

from lms_ds_loader.lms_filesystem_provider import LmsFilesystemProvider


class Test_lms_filesystem_provider:
    class Test_when_getting_all_files:
        def test_given_invalid_file_path_then_raise_error(self, mocker):

            csv_path = "does-not-exist"

            mocker.patch.object(os.path, "exists", return_value=False)

            with pytest.raises(OSError):
                LmsFilesystemProvider(csv_path).get_all_files()

        def test_given_valid_path_does_not_contain_user_directory_then_do_nothing(self, mocker):
            csv_path = "exists"

            # Arrange
            user_path = os.path.join(csv_path, "Users")

            def mock_os_path_exists(arg):
                switch = {
                    csv_path: True,
                    user_path: False
                }

                return switch.get(arg, f"Unexpected file path {arg}")

            mock = mocker.patch.object(os.path, "exists")
            mock.side_effect = mock_os_path_exists

            # Act
            fs = LmsFilesystemProvider(csv_path).get_all_files()

            # Assert
            assert len(fs.Users) == 0

        def test_given_valid_path_contains_empty_user_directory_then_do_nothing(self, mocker):
            csv_path = "exists"

            # Arrange
            user_path = os.path.join(csv_path, "Users")

            def mock_os_path_exists(arg):
                switch = {
                    csv_path: True,
                    user_path: True
                }

                return switch.get(arg, f"Unexpected file path {arg}")

            mock_path = mocker.patch.object(os.path, "exists")
            mock_path.side_effect = mock_os_path_exists

            def mock_os_scandir(arg):
                switch = {
                    user_path: []
                }

                return switch.get(arg, f"Unexpected file path {arg}")

            mock_scandir = mocker.patch.object(os, "scandir")
            mock_scandir.side_effect = mock_os_scandir

            # Act
            fs = LmsFilesystemProvider(csv_path).get_all_files()

            # Assert
            assert len(fs.Users) == 0

        def test_given_valid_path_contains_user_files_then_read_file_path(self, mocker):

            csv_path = "exists"
            user_path = os.path.join(csv_path, "Users")
            expected_1 = os.path.join(user_path, "2020-09-03-12-34-56.csv")
            expected_2 = os.path.join(user_path, "2020-09-04-12-34-36.csv")

            def mock_os_path_exists(arg):
                switch = {
                    csv_path: True,
                    user_path: True
                }

                return switch.get(arg, f"Unexpected file path {arg}")

            mock = mocker.patch.object(os.path, "exists")
            mock.side_effect = mock_os_path_exists

            def mock_os_scandir(arg):
                switch = {
                    user_path: [expected_1, expected_2]
                }

                return switch.get(arg, f"Unexpected file path {arg}")

            mock_scandir = mocker.patch.object(os, "scandir")
            mock_scandir.side_effect = mock_os_scandir

            # Act
            fs = LmsFilesystemProvider(csv_path).get_all_files()

            assert len(fs.Users) == 2, "did not find both files"
            assert fs.Users[0] == expected_1, "did not find file 1"
            assert fs.Users[1] == expected_2, "did not find file 2"
