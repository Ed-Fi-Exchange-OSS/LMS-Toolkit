# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
from freezegun import freeze_time

from edfi_lms_file_utils import directory_repository as dr


OUTPUT_DIRECTORY = "./output"
DATE_TIME_INPUT_STRING = "2020-10-16 1:00:01 PM"


@pytest.fixture
def setup_filesystem(fs):
    # Fake as Linux so that all slashes in these test are forward
    fs.path_separator = "/"
    fs.is_windows_fs = False
    fs.is_macos = False
    fs.create_dir(OUTPUT_DIRECTORY)


def describe_when_getting_system_activities_directory_for_today():
    @freeze_time(DATE_TIME_INPUT_STRING)
    def it_should_use_correct_directory(setup_filesystem):
        # Act
        dir = dr.get_system_activities_directory_for_today(OUTPUT_DIRECTORY)

        # Assert
        assert dir == "./output/system-activities/date=2020-10-16"
