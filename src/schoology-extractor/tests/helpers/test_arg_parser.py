# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

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
    @pytest.fixture
    def required_params_for_parse_main_arguments():
        return ["-s", "fake_secret", "-g", "fake_grading_periods", "-k", "fake_key"]

    def describe_given_parameters_are_valid():
        def it_should_not_throw_exception(required_params_for_parse_main_arguments):
            parse_main_arguments(required_params_for_parse_main_arguments)

        def it_should_return_correct_type(required_params_for_parse_main_arguments):
            parsed_arguments = parse_main_arguments(
                required_params_for_parse_main_arguments
            )
            assert isinstance(parsed_arguments, MainArguments)

    def describe_given_parameters_are_not_valid():
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

        def given_not_valid_log_level_parameter_is_missing_then_throw_system_exit_error(
            required_params_for_parse_main_arguments, capsys
        ):
            args = [
                "-l",
                "invalid_log_level",
            ] + required_params_for_parse_main_arguments
            with pytest.raises(SystemExit):
                parse_main_arguments(args)
                assert_error_message(capsys)

        def given_not_valid_page_size_parameter_then_throw_system_exit_error(
            required_params_for_parse_main_arguments, capsys
        ):
            args = [
                "-p",
                "non_numeric_value",
            ] + required_params_for_parse_main_arguments
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
