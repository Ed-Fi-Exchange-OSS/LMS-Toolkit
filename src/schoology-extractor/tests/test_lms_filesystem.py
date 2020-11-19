# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
import re

import pytest
from freezegun import freeze_time

from schoology_extractor.lms_filesystem import (
    get_assignment_file_path,
    get_user_file_path,
    get_section_file_path,
    get_section_association_file_path,
    get_attendance_events_file_path,
    get_system_activities_file_path
)


SECTION_ID = 123
OUTPUT_DIRECTORY = "./output"
DATE_TIME_INPUT_STRING = "2020-10-16 1:00:01 PM"
FILE_NAME = "2020-10-16-13-00-01.csv"


def _setup_filesystem(fs):
    # Fake as Linux so that all slashes in these test are forward
    fs.path_separator = "/"
    fs.is_windows_fs = False
    fs.is_macos = False
    fs.create_dir(OUTPUT_DIRECTORY)


def describe_when_getting_the_assignment_file_name():
    @pytest.fixture
    @freeze_time(DATE_TIME_INPUT_STRING)
    def result(fs):
        _setup_filesystem(fs)

        return get_assignment_file_path(OUTPUT_DIRECTORY, SECTION_ID)

    def it_should_use_the_lms_filesystem_path_for_the_section(result, fs):
        assert (
            re.match(r"./output/section=123/assignments/[^/]+\.csv", result) is not None
        ), f"actual: {result}"

    def it_should_use_timestamp_for_file_name(result):
        assert result.endswith(FILE_NAME)

    def it_should_create_the_section_directory(result, fs):
        assert os.path.exists("./output/section=123/assignments")


def describe_when_getting_the_user_file_name():
    @pytest.fixture
    @freeze_time(DATE_TIME_INPUT_STRING)
    def result(fs):
        _setup_filesystem(fs)

        return get_user_file_path(OUTPUT_DIRECTORY)

    def it_should_use_the_lms_filesystem_path(result, fs):
        assert (
            re.match(r"./output/users/[^/]+\.csv", result) is not None
        ), f"actual: {result}"

    def it_should_use_timestamp_for_file_name(result):
        assert result.endswith(FILE_NAME)

    def it_should_create_the_users_directory(result, fs):
        assert os.path.exists("./output/users")


def describe_when_getting_the_section_file_name():
    @pytest.fixture
    @freeze_time(DATE_TIME_INPUT_STRING)
    def result(fs):
        _setup_filesystem(fs)

        return get_section_file_path(OUTPUT_DIRECTORY)

    def it_should_use_the_lms_filesystem_path(result, fs):
        assert (
            re.match(r"./output/sections/[^/]+\.csv", result) is not None
        ), f"actual: {result}"

    def it_should_use_timestamp_for_file_name(result):
        assert result.endswith(FILE_NAME)

    def it_should_create_the_sections_directory(result, fs):
        assert os.path.exists("./output/sections")


def describe_when_getting_the_section_associations_file_name():
    @pytest.fixture
    @freeze_time(DATE_TIME_INPUT_STRING)
    def result(fs):
        _setup_filesystem(fs)

        return get_section_association_file_path(OUTPUT_DIRECTORY, SECTION_ID)

    def it_should_use_the_lms_filesystem_path_for_the_section(result, fs):
        assert (
            re.match(r"./output/section=123/section-associations/[^/]+\.csv", result) is not None
        ), f"actual: {result}"

    def it_should_use_timestamp_for_file_name(result):
        assert result.endswith(FILE_NAME)

    def it_should_create_the_section_directory(result, fs):
        assert os.path.exists("./output/section=123/section-associations")


def describe_when_getting_the_attendance_events_file_name():
    @pytest.fixture
    @freeze_time(DATE_TIME_INPUT_STRING)
    def result(fs):
        _setup_filesystem(fs)

        return get_attendance_events_file_path(OUTPUT_DIRECTORY, SECTION_ID)

    def it_should_use_the_lms_filesystem_path_for_the_section(result, fs):
        assert (
            re.match(r"./output/section=123/attendance/[^/]+\.csv", result) is not None
        ), f"actual: {result}"

    def it_should_use_timestamp_for_file_name(result):
        assert result.endswith(FILE_NAME)

    def it_should_create_the_section_directory(result, fs):
        assert os.path.exists("./output/section=123/attendance")


def describe_when_getting_system_activities_file_path():
    @pytest.fixture
    @freeze_time(DATE_TIME_INPUT_STRING)
    def result(fs):
        _setup_filesystem(fs)

        return get_system_activities_file_path(OUTPUT_DIRECTORY)

    def it_should_use_the_current_date_in_the_directory_path(result, fs):
        assert (
            re.match(r"./output/system-activities/date=2020-10-16/[^/]+\.csv", result) is not None
        ), f"actual: {result}"

    def it_should_use_timestamp_for_file_name(result):
        assert result.endswith(FILE_NAME)

    def it_should_create_the_date_directory(result, fs):
        assert os.path.exists("./output/system-activities/date=2020-10-16")
