# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import List

import pytest

from edfi_lms_harmonizer.helpers.argparser import parse_main_arguments, MainArguments
from edfi_lms_harmonizer.helpers.constants import LOG_LEVELS


PATH = "./lms_udm_files"
SERVER = "localhost"
DB_NAME = "EdFi_ODS"
USERNAME = "my_user"
PASSWORD = "my_password"
PORT = 1234
REPORT_DIR = "./exceptions"


def _server_args() -> List[str]:
    return ["--server", SERVER]


def port_args() -> List[str]:
    return ["--port", str(PORT)]


def _db_name_args() -> List[str]:
    return ["--dbname", DB_NAME]


def _integrated_security_arg() -> List[str]:
    return ["--useintegratedsecurity"]


def _username_args() -> List[str]:
    return ["--username", USERNAME]


def _password_args() -> List[str]:
    return ["--password", PASSWORD]


def _exception_report_args() -> List[str]:
    return ["--exceptions-report-directory", REPORT_DIR]


def _assert_no_messages(capsys) -> None:
    out, err = capsys.readouterr()

    assert err == "", "There should be an error message"
    assert out == "", "There should not be an output message"


def _assert_error_message(capsys) -> None:
    out, err = capsys.readouterr()

    assert err != "", "There should be an error message"
    assert out == "", "There should not be an output message"


def describe_given_arguments_do_not_include_server() -> None:
    def it_should_show_help(capsys) -> None:
        with pytest.raises(SystemExit):
            args = [
                *_server_args(),
                *_integrated_security_arg(),
            ]

            parse_main_arguments(args)

            _assert_error_message(capsys)


def describe_given_integrated_security() -> None:
    def it_should_not_require_username_and_password(capsys) -> None:
        args = [
            *_server_args(),
            *_db_name_args(),
            *_integrated_security_arg(),
        ]

        parsed = parse_main_arguments(args)

        assert parsed is not None, "No arguments detected"

        _assert_no_messages(capsys)


def describe_given_using_integrated_security_short_flag() -> None:
    def it_should_not_require_username_and_password(capsys) -> None:
        args = [
            *_server_args(),
            *_db_name_args(),
            "-i",
        ]

        parsed = parse_main_arguments(args)

        assert parsed is not None, "No arguments detected"

        _assert_no_messages(capsys)


def describe_given_not_using_integrated_security() -> None:
    def it_should_require_username(capsys) -> None:
        with pytest.raises(SystemExit):
            args = [
                *_server_args(),
                *_db_name_args(),
                *_password_args(),
            ]

            parse_main_arguments(args)

            _assert_error_message(capsys)

    def it_should_require_password(capsys) -> None:
        with pytest.raises(SystemExit):
            args = [
                *_server_args(),
                *_db_name_args(),
                *_username_args(),
            ]

            parse_main_arguments(args)

            _assert_error_message(capsys)


def describe_given_optional_port_is_provided() -> None:
    def it_should_inject_port_into_connection_string(capsys) -> None:
        args = [
            *_server_args(),
            *_db_name_args(),
            *_integrated_security_arg(),
            *port_args(),
        ]

        parsed = parse_main_arguments(args)

        _assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        assert parsed.port == PORT


def describe_given_exception_report_arg() -> None:
    def it_should_store_the_file_path(capsys) -> None:
        args = [
            *_server_args(),
            *_db_name_args(),
            *_integrated_security_arg(),
            *_exception_report_args(),
        ]

        parsed = parse_main_arguments(args)

        assert parsed.exceptions_report_directory == REPORT_DIR


def describe_given_engine_mssql() -> None:
    def describe_given_using_integrated_security() -> None:
        def it_should_set_trusted_connection_in_the_connection_string(
            capsys,
        ) -> None:
            args = [*_server_args(), *_db_name_args(), *_integrated_security_arg()]

            parsed = parse_main_arguments(args)

            _assert_no_messages(capsys)

            assert parsed is not None, "No arguments detected"

            # Only need to confirm that the adapter was created
            assert parsed.get_adapter() is not None

    @pytest.fixture
    def fixture(capsys) -> MainArguments:
        # Arrange
        args = [
            *_server_args(),
            *_db_name_args(),
            *_username_args(),
            *_password_args(),
            *port_args(),
        ]

        # Act
        parsed = parse_main_arguments(args)

        _assert_no_messages(capsys)

        return parsed

    def it_should_set_server_name_in_the_connection_string(
        fixture: MainArguments,
    ) -> None:
        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert SERVER in str(fixture.get_adapter().engine.url)

    def it_should_set_port_in_the_connection_string(fixture: MainArguments) -> None:
        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert str(PORT) in str(fixture.get_adapter().engine.url)

    def it_should_set_database_name_in_the_connection_string(
        fixture: MainArguments,
    ) -> None:
        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert DB_NAME in str(fixture.get_adapter().engine.url)

    def it_should_set_username_in_the_connection_string(
        fixture: MainArguments,
    ) -> None:
        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert USERNAME in str(fixture.get_adapter().engine.url)

    def it_should_set_password_in_the_connection_string(
        fixture: MainArguments,
    ) -> None:
        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert PASSWORD in str(fixture.get_adapter().engine.url)

    def describe_given_optional_non_default_log_level() -> None:
        def it_should_parse_the_log_level(capsys) -> None:
            args = [
                *_server_args(),
                *_db_name_args(),
                *_integrated_security_arg(),
                "--log-level",
                "DEBUG",
            ]

            parsed = parse_main_arguments(args)

            _assert_no_messages(capsys)

            assert parsed is not None, "No arguments detected"
            assert parsed.log_level == "DEBUG"
