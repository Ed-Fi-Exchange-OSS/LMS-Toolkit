# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from google_classroom_extractor.helpers.arg_parser import (
    parse_main_arguments,
    MainArguments
)


def assert_error_message(capsys):
    out, err = capsys.readouterr()

    assert err != "", "There should be an error message"
    assert out == "", "There should not be an output message"


def describe_when_parsing_arguments():
    def describe_given_log_level_parameter():
        @pytest.fixture
        def result() -> MainArguments:
            # Arrange
            parameters = ["-l", "log_level"]

            # Act
            return parse_main_arguments(parameters)

        def it_should_load_the_secret(result: MainArguments):
            assert result.log_level == "log_level"

    def describe_given_no_log_level_parameter():
        @pytest.fixture
        def result() -> MainArguments:
            # Arrange
            parameters = []

            # Act
            return parse_main_arguments(parameters)

        def it_should_load_the_default_log_level(result: MainArguments):
            assert result.log_level == "INFO"
