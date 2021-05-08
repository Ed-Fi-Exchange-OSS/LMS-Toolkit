# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from edfi_canvas_extractor.helpers.arg_parser import parse_main_arguments, MainArguments


def assert_error_message(capsys):
    out, err = capsys.readouterr()

    assert err != "", "There should be an error message"
    assert out == "", "There should not be an output message"


TEST_BASE_URL = "1"
TEST_ACCESS_TOKEN = "2"
TEST_START_DATE = "3"
TEST_END_DATE = "3"
TEST_LOG_LEVEL = "DEBUG"
TEST_OUTPUT_DIRECTORY = "5"
TEST_SYNC_DATABASE_DIRECTORY = "test_sync_database_directory"
TEST_FEATURES = "activities attendance assignments grades"


def describe_when_parsing_arguments():
    def describe_given_minimum_parameters():
        @pytest.fixture
        def result() -> MainArguments:
            # Arrange
            parameters = [
                "-b",
                TEST_BASE_URL,
                "-a",
                TEST_ACCESS_TOKEN,
                "-s",
                TEST_START_DATE,
                "-e",
                TEST_END_DATE,
            ]

            # Act
            return parse_main_arguments(parameters)

        def it_should_load_the_base_url(result: MainArguments):
            assert result.base_url == TEST_BASE_URL

        def it_should_load_the_access_token(result: MainArguments):
            assert result.access_token == TEST_ACCESS_TOKEN

        def it_should_default_to_warn_level(result: MainArguments):
            assert result.log_level == "INFO"

        def it_should_default_to_data_directory(result: MainArguments):
            assert result.output_directory == "data/"

        def it_should_load_the_start_date(result: MainArguments):
            assert result.start_date == TEST_START_DATE

        def it_should_load_the_end_date(result: MainArguments):
            assert result.end_date == TEST_END_DATE

    def describe_given_optional_parameters():
        @pytest.fixture
        def result() -> MainArguments:
            # Arrange
            parameters = [
                "-b",
                TEST_BASE_URL,
                "-a",
                TEST_ACCESS_TOKEN,
                "-s",
                TEST_START_DATE,
                "-e",
                TEST_END_DATE,
                "-l",
                TEST_LOG_LEVEL,
                "-o",
                TEST_OUTPUT_DIRECTORY,
                "-d",
                TEST_SYNC_DATABASE_DIRECTORY,
                "-f",
                *TEST_FEATURES.split(),  # Split to convert it into a list and use * to unpack the list into separated values
            ]

            # Act
            return parse_main_arguments(parameters)

        def it_should_load_the_base_url(result: MainArguments):
            assert result.base_url == TEST_BASE_URL

        def it_should_load_the_access_token(result: MainArguments):
            assert result.access_token == TEST_ACCESS_TOKEN

        def it_should_load_the_log_level(result: MainArguments):
            assert result.log_level == TEST_LOG_LEVEL

        def it_should_load_the_output_directory(result: MainArguments):
            assert result.output_directory == TEST_OUTPUT_DIRECTORY

        def it_should_load_the_start_date(result: MainArguments):
            assert result.start_date == TEST_START_DATE

        def it_should_load_the_end_date(result: MainArguments):
            assert result.end_date == TEST_END_DATE

        def it_should_load_the_sync_database_directory(result: MainArguments):
            assert result.sync_database_directory == TEST_SYNC_DATABASE_DIRECTORY

        def it_should_load_the_features(result: MainArguments):
            assert result.extract_grades
            assert result.extract_activities
            assert result.extract_assignments
            assert result.extract_attendance
