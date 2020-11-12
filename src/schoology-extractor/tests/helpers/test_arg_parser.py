# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from logging import WARNING
from typing import List

import pytest

from schoology_extractor.helpers.arg_parser import (
    parse_main_arguments,
    MainArguments,
    parse_grading_periods_arguments,
    GradingPeriodsArguments,
)


@pytest.fixture
def required_params_for_parse_grading_periods_arguments():
    return ["-s", "fake_secret", "-k", "fake_key"]


def assert_error_message(capsys):
    out, err = capsys.readouterr()

    assert err != "", "There should be an error message"
    assert out == "", "There should not be an output message"


def describe_when_parsing_arguments():
    def describe_given_minimum_parameters():
        @pytest.fixture
        def result() -> MainArguments:
            # Arrange
            parameters = ["-s", "fake_secret", "-g", "123,456", "-k", "fake_key"]

            # Act
            return parse_main_arguments(parameters)

        def it_should_load_the_secret(result: MainArguments):
            assert result.client_secret == "fake_secret"

        def it_should_load_the_grading_periods(result: MainArguments):
            assert result.grading_periods == "123,456"

        def it_should_load_the_key(result: MainArguments):
            assert result.client_key == "fake_key"

        def it_should_default_to_warn_level(result: MainArguments):
            assert result.log_level == "WARNING"

        def it_should_default_to_page_size_20(result: MainArguments):
            assert result.page_size == 20

        def it_should_default_to_current_directory(result: MainArguments):
            assert result.output_directory == ""

    def describe_given_optional_parameters():
        @pytest.fixture
        def result() -> MainArguments:
            # Arrange
            parameters = [
                "-s",
                "fake_secret",
                "-g",
                "123,456",
                "-k",
                "fake_key",
                "-o",
                "output_directory",
                "-l",
                "DEBUG",
                "-p",
                "30",
            ]

            # Act
            return parse_main_arguments(parameters)

        def it_should_load_the_output_directory(result: MainArguments):
            assert result.output_directory == "output_directory"

        def it_should_load_the_log_level(result: MainArguments):
            assert result.log_level == "DEBUG"

        def it_should_load_the_page_size(result: MainArguments):
            assert result.page_size == 30

    def describe_given_parameters_are_not_valid():
        @pytest.fixture
        def default_parameters() -> List[str]:
            return ["-s", "fake_secret", "-g", "123,456", "-k", "fake_key"]

        def given_client_key_parameter_is_missing_then_throw_error(capsys):
            args = ["-s", "fake_secret", "-g", "fake_grading_periods"]
            with pytest.raises(SystemExit):
                parse_main_arguments(args)
                assert_error_message(capsys)

        def given_client_secret_parameter_is_missing_then_throw_error(capsys):
            args = ["-k", "fake_key", "-g", "fake_grading_periods"]
            with pytest.raises(SystemExit):
                parse_main_arguments(args)
                assert_error_message(capsys)

        def given_grading_periods_parameter_is_missing_then_throw_error(capsys):
            args = ["-k", "fake_key", "-s", "fake_secret"]
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


def describe_when_parsing_grading_periods_arguments():
    def describe_given_parameters_are_valid():
        def it_should_not_throw_an_exception(
            required_params_for_parse_grading_periods_arguments,
        ):
            parse_grading_periods_arguments(
                required_params_for_parse_grading_periods_arguments
            )

        def it_should_return_correct_type(
            required_params_for_parse_grading_periods_arguments,
        ):
            parsed_arguments = parse_grading_periods_arguments(
                required_params_for_parse_grading_periods_arguments
            )
            assert isinstance(parsed_arguments, GradingPeriodsArguments)

    def describe_given_parameters_are_not_valid():
        def given_client_key_parameter_is_missing_then_throw_error(capsys):
            args = ["-s", "fake_secret"]
            with pytest.raises(SystemExit):
                parse_grading_periods_arguments(args)
                assert_error_message(capsys)

        def given_client_secret_parameter_is_missing_then_throw_error(capsys):
            args = ["-k", "fake_key"]
            with pytest.raises(SystemExit):
                parse_grading_periods_arguments(args)
                assert_error_message(capsys)

        def given_not_valid_log_level_parameter_is_missing_then_throw_system_exit_error(
            required_params_for_parse_grading_periods_arguments, capsys
        ):
            args = [
                "-l",
                "invalid_log_level",
            ] + required_params_for_parse_grading_periods_arguments
            with pytest.raises(SystemExit):
                parse_grading_periods_arguments(args)
                assert_error_message(capsys)

        def given_not_valid_page_size_parameter_then_throw_system_exit_error(
            required_params_for_parse_grading_periods_arguments, capsys
        ):
            args = [
                "-p",
                "non_numeric_value",
            ] + required_params_for_parse_grading_periods_arguments
            with pytest.raises(SystemExit):
                parse_grading_periods_arguments(args)
                assert_error_message(capsys)
