# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
import pytest

from lms_ds_loader.lms_filesystem_provider import LmsFilesystemProvider


class Test_when_getting_all_files:
    def test_given_invalid_file_path_then_raise_error(self, mocker):

        csv_path = "does-not-exist"

        mocker.patch.object(os.path, "exists", return_value=False)

        with pytest.raises(OSError):
            LmsFilesystemProvider(csv_path).get_all_files()

    def test_given_valid_path_does_not_contain_user_directory_then_do_nothing(self, fs):
        csv_path = "exists"

        # Arrange
        fs.create_dir(csv_path)

        # Act
        fs = LmsFilesystemProvider(csv_path).get_all_files()

        # Assert
        assert len(fs.Users) == 0

    def test_given_valid_path_contains_empty_user_directory_then_do_nothing(self, fs):
        csv_path = "exists"

        # Arrange
        user_path = os.path.join(csv_path, "Users")
        fs.create_dir(user_path)

        # Act
        fs = LmsFilesystemProvider(csv_path).get_all_files()

        # Assert
        assert len(fs.Users) == 0

    def test_given_valid_path_contains_user_files_then_load_their_file_paths(self, fs):

        csv_path = "exists"
        user_path = os.path.join(csv_path, "Users")
        expected_1 = os.path.join(user_path, "2020-09-03-12-34-56.csv")
        expected_2 = os.path.join(user_path, "2020-09-04-12-34-36.csv")

        fs.create_file(expected_1)
        fs.create_file(expected_2)

        # Act
        fs = LmsFilesystemProvider(csv_path).get_all_files()

        assert len(fs.Users) == 2, "did not find both files"
        assert fs.Users[0] == expected_1, "did not find file 1"
        assert fs.Users[1] == expected_2, "did not find file 2"

    def test_given_valid_path_contains_non_csv_files_then_ignore_them(self, fs):

        csv_path = "exists"
        user_path = os.path.join(csv_path, "Users")
        expected_1 = os.path.join(user_path, "2020-09-03-12-34-56.json")
        expected_2 = os.path.join(user_path, "2020-09-04-12-34-36.txt")

        fs.create_file(expected_1)
        fs.create_file(expected_2)

        # Act
        fs = LmsFilesystemProvider(csv_path).get_all_files()

        assert len(fs.Users) == 0, "Should not have found any files"
