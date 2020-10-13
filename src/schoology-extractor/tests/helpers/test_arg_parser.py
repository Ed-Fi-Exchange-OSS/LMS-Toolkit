# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from schoology_extractor.helpers.arg_parser import parse_main_arguments, MainArguments, parse_grading_periods_arguments, GradingPeriodsArguments


@pytest.fixture
def required_params_for_parse_main_arguments():
    return ['-s', 'fake_secret', '-g', 'fake_grading_periods', '-k', 'fake_key']


@pytest.fixture
def required_params_for_parse_grading_periods_arguments():
    return ['-s', 'fake_secret', '-k', 'fake_key']


def assert_error_message(capsys):
    out, err = capsys.readouterr()

    assert err != "", "There should be an error message"
    assert out == "", "There should not be an output message"


class Test_parse_main_argument:
    class Test_when_parameters_are_valid:
        def test_then_no_exception_is_thrown(self, required_params_for_parse_main_arguments):
            parse_main_arguments(required_params_for_parse_main_arguments)

        def test_then_return_correct_type(self, required_params_for_parse_main_arguments):
            parsed_arguments = parse_main_arguments(required_params_for_parse_main_arguments)
            assert isinstance(parsed_arguments, MainArguments)

    class Test_when_parameters_are_not_valid:
        def test_given_none_as_args_in_parameter_then_throw_assertion_error(self):
            with pytest.raises(AssertionError):
                parse_main_arguments(args_in=None)   # type: ignore

        def test_given_no_parameter_then_throw_type_error(self):
            with pytest.raises(TypeError):
                parse_main_arguments()   # type: ignore

        def test_given_client_key_parameter_is_missing_then_throw_error(self, capsys):
            args = ['-s', 'fake_secret', '-g', 'fake_grading_periods']
            with pytest.raises(SystemExit):
                parse_main_arguments(args)
                assert_error_message(capsys)

        def test_given_client_secret_parameter_is_missing_then_throw_error(self, capsys):
            args = ['-k', 'fake_key', '-g', 'fake_grading_periods']
            with pytest.raises(SystemExit):
                parse_main_arguments(args)
                assert_error_message(capsys)

        def test_given_grading_periods_parameter_is_missing_then_throw_error(self, capsys):
            args = ['-k', 'fake_key', '-s', 'fake_secret']
            with pytest.raises(SystemExit):
                parse_main_arguments(args)
                assert_error_message(capsys)

        def test_given_not_valid_log_level_parameter_is_missing_then_throw_system_exit_error(self, required_params_for_parse_main_arguments, capsys):
            args = ['-l', 'invalid_log_level'] + required_params_for_parse_main_arguments
            with pytest.raises(SystemExit):
                parse_main_arguments(args)
                assert_error_message(capsys)

        def test_given_not_valid_page_size_parameter_then_throw_system_exit_error(self, required_params_for_parse_main_arguments, capsys):
            args = ['-p', 'non_numeric_value'] + required_params_for_parse_main_arguments
            with pytest.raises(SystemExit):
                parse_main_arguments(args)
                assert_error_message(capsys)


class Test_parse_grading_periods_arguments:
    class Test_when_parameters_are_valid:
        def test_then_no_exception_is_thrown(self, required_params_for_parse_grading_periods_arguments):
            parse_grading_periods_arguments(required_params_for_parse_grading_periods_arguments)

        def test_then_return_correct_type(self, required_params_for_parse_grading_periods_arguments):
            parsed_arguments = parse_grading_periods_arguments(required_params_for_parse_grading_periods_arguments)
            assert isinstance(parsed_arguments, GradingPeriodsArguments)

    class Test_when_parameters_are_not_valid:
        def test_given_none_as_args_in_parameter_then_throw_assertion_error(self):
            with pytest.raises(AssertionError):
                parse_grading_periods_arguments(args_in=None)   # type: ignore

        def test_given_no_parameter_then_throw_type_error(self):
            with pytest.raises(TypeError):
                parse_grading_periods_arguments()   # type: ignore

        def test_given_client_key_parameter_is_missing_then_throw_error(self, capsys):
            args = ['-s', 'fake_secret']
            with pytest.raises(SystemExit):
                parse_grading_periods_arguments(args)
                assert_error_message(capsys)

        def test_given_client_secret_parameter_is_missing_then_throw_error(self, capsys):
            args = ['-k', 'fake_key']
            with pytest.raises(SystemExit):
                parse_grading_periods_arguments(args)
                assert_error_message(capsys)

        def test_given_not_valid_log_level_parameter_is_missing_then_throw_system_exit_error(self, required_params_for_parse_grading_periods_arguments, capsys):
            args = ['-l', 'invalid_log_level'] + required_params_for_parse_grading_periods_arguments
            with pytest.raises(SystemExit):
                parse_grading_periods_arguments(args)
                assert_error_message(capsys)

        def test_given_not_valid_page_size_parameter_then_throw_system_exit_error(self, required_params_for_parse_grading_periods_arguments, capsys):
            args = ['-p', 'non_numeric_value'] + required_params_for_parse_grading_periods_arguments
            with pytest.raises(SystemExit):
                parse_grading_periods_arguments(args)
                assert_error_message(capsys)
