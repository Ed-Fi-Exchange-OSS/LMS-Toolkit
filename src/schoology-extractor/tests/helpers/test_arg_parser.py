# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import List

import pytest

from edfi_schoology_extractor.helpers.arg_parser import (
    parse_main_arguments,
    MainArguments,
)


FAKE_SECRET = "fake_secret"
FAKE_KEY = "fake_key"
FAKE_OUTPUT_DIRECTORY = "output_directory"
FAKE_INPUT_DIRECTORY = "output_input"
LOG_LEVEL = "DEBUG"
TEST_SYNC_DATABASE_DIRECTORY = "test_sync_database_directory"
TEST_FEATURES = "activities attendance assignments grades"


def assert_error_message(capsys):
    out, err = capsys.readouterr()

    assert err != "", "There should be an error message"
    assert out == "", "There should not be an output message"


def describe_when_parsing_arguments():
    def describe_given_minimum_parameters():
        @pytest.fixture
        def result() -> MainArguments:
            # Arrange
            parameters = ["-s", FAKE_SECRET, "-k", FAKE_KEY]

            # Act
            return parse_main_arguments(parameters)

        def it_should_load_the_secret(result: MainArguments):
            assert result.client_secret == FAKE_SECRET

        def it_should_load_the_key(result: MainArguments):
            assert result.client_key == FAKE_KEY

        def it_should_default_to_warn_level(result: MainArguments):
            assert result.log_level == "INFO"

        def it_should_default_to_page_size_200(result: MainArguments):
            assert result.page_size == 200

        def it_should_default_to_current_directory(result: MainArguments):
            assert result.output_directory == ""

    def describe_given_optional_parameters():
        @pytest.fixture
        def result() -> MainArguments:
            # Arrange
            parameters = [
                "-s",
                FAKE_SECRET,
                "-k",
                FAKE_KEY,
                "-o",
                FAKE_OUTPUT_DIRECTORY,
                "-l",
                LOG_LEVEL,
                "-p",
                "30",
                "-i",
                FAKE_INPUT_DIRECTORY,
                "-d",
                TEST_SYNC_DATABASE_DIRECTORY,
                "-f",
                *TEST_FEATURES.split(),  # Split to convert it into a list and use * to unpack the list into separated values
            ]

            # Act
            return parse_main_arguments(parameters)

        def it_should_load_the_input_directory(result: MainArguments):
            assert result.input_directory == FAKE_INPUT_DIRECTORY

        def it_should_load_the_output_directory(result: MainArguments):
            assert result.output_directory == FAKE_OUTPUT_DIRECTORY

        def it_should_load_the_log_level(result: MainArguments):
            assert result.log_level == LOG_LEVEL

        def it_should_load_the_page_size(result: MainArguments):
            assert result.page_size == 30

        def it_should_load_the_sync_database_directory(result: MainArguments):
            assert result.sync_database_directory == TEST_SYNC_DATABASE_DIRECTORY

        def it_should_load_the_features_array(result: MainArguments):
            assert result.extract_attendance
            assert result.extract_activities
            assert result.extract_assignments
            assert result.extract_grades

    def describe_given_parameters_are_not_valid():
        @pytest.fixture
        def default_parameters() -> List[str]:
            return ["-s", FAKE_SECRET, "-k", FAKE_KEY]

        def given_client_key_parameter_is_missing_then_throw_error(capsys):
            args = ["-s", FAKE_SECRET]
            with pytest.raises(SystemExit):
                parse_main_arguments(args)
                assert_error_message(capsys)

        def given_client_secret_parameter_is_missing_then_throw_error(capsys):
            args = ["-k", FAKE_KEY]
            with pytest.raises(SystemExit):
                parse_main_arguments(args)
                assert_error_message(capsys)

        def given_invalid_log_level_parameter_then_throw_system_exit_error(
            default_parameters, capsys
        ):
            args = [
                "-l",
                "invalid_log_level",
            ] + default_parameters
            with pytest.raises(SystemExit):
                parse_main_arguments(args)
                assert_error_message(capsys)

        def given_invalid_page_size_parameter_then_throw_system_exit_error(
            default_parameters, capsys
        ):
            args = [
                "-p",
                "non_numeric_value",
            ] + default_parameters
            with pytest.raises(SystemExit):
                parse_main_arguments(args)
                assert_error_message(capsys)
