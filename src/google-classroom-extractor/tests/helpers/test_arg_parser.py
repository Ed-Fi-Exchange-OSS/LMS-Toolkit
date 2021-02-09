# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from edfi_google_classroom_extractor.helpers.arg_parser import (
    parse_main_arguments,
    MainArguments
)


def assert_error_message(capsys):
    out, err = capsys.readouterr()

    assert err != "", "There should be an error message"
    assert out == "", "There should not be an output message"


def describe_when_parsing_arguments():
    def describe_given_minimum_parameters():
        @pytest.fixture
        def result() -> MainArguments:
            # Arrange
            parameters = ["-a", "test_account"]

            # Act
            return parse_main_arguments(parameters)

        def it_should_load_the_account(result: MainArguments):
            assert result.classroom_account == "test_account"

        def it_should_default_to_warn_level(result: MainArguments):
            assert result.log_level == "INFO"

        def it_should_default_to_current_directory(result: MainArguments):
            assert result.output_directory == "data/"

        def it_should_load_the_start_date(result: MainArguments):
            assert result.usage_start_date == ""

        def it_should_load_the_end_date(result: MainArguments):
            assert result.usage_end_date == ""

    def describe_given_optional_parameters():
        @pytest.fixture
        def result() -> MainArguments:
            # Arrange
            parameters = [
                "-a",
                "fake_account",
                "-l",
                "DEBUG",
                "-o",
                "output_directory",
                "-s",
                "fake_date",
                "-e",
                "fake_end_date"
            ]

            # Act
            return parse_main_arguments(parameters)

        def it_should_load_the_log_level(result: MainArguments):
            assert result.log_level == "DEBUG"

        def it_should_load_the_output_directory(result: MainArguments):
            assert result.output_directory == "output_directory"

        def it_should_load_the_start_date(result: MainArguments):
            assert result.usage_start_date == "fake_date"

        def it_should_load_the_end_date(result: MainArguments):
            assert result.usage_end_date == "fake_end_date"
