# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import List

import pytest

from edfi_lms_ds_loader.helpers.argparser import parse_main_arguments, MainArguments
from edfi_lms_ds_loader.helpers.constants import DbEngine, LOG_LEVELS
from edfi_lms_ds_loader.sql_lms_operations import SqlLmsOperations


PATH = "./lms_udm_files"
SERVER = "localhost"
DB_NAME = "EdFi_ODS"
USERNAME = "my_user"
PASSWORD = "my_password"
PORT = 1234


def _path_args() -> List[str]:
    return ["--csvpath", PATH]


def _engine_args(engine) -> List[str]:
    return ["--engine", engine]


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


def _encrypt_args() -> List[str]:
    return ["--encrypt"]


def _trust_certificate_args() -> List[str]:
    return ["--trust-certificate"]


def _assert_no_messages(capsys) -> None:
    out, err = capsys.readouterr()

    assert err == "", "There should be an error message"
    assert out == "", "There should not be an output message"


def _assert_error_message(capsys) -> None:
    out, err = capsys.readouterr()

    assert err != "", "There should be an error message"
    assert out == "", "There should not be an output message"


def describe_when_parsing_system_arguments() -> None:
    def describe_given_arguments_is_an_empty_list() -> None:
        def it_should_show_help(capsys) -> None:
            with pytest.raises(SystemExit):
                parse_main_arguments(list())

                out, err = capsys.readouterr()

                assert err != "", "There should be an error message"
                assert out == "", "There should not be an output message"

    def describe_given_arguments_do_not_include_path() -> None:
        def it_should_show_help(capsys) -> None:
            with pytest.raises(SystemExit):
                args = [
                    *_engine_args(DbEngine.MSSQL),
                    *_server_args(),
                    *_db_name_args(),
                    *_integrated_security_arg(),
                ]

                parse_main_arguments(args)

                _assert_error_message(capsys)

    def describe_given_arguments_do_not_include_engine() -> None:
        def it_should_default_to_mssql(capsys) -> None:
            args = [
                *_path_args(),
                *_server_args(),
                *_db_name_args(),
                *_integrated_security_arg(),
            ]

            parsed = parse_main_arguments(args)

            assert parsed is not None, "No arguments detected"

            assert parsed.engine == DbEngine.MSSQL

            _assert_no_messages(capsys)

    def describe_given_arguments_do_not_include_server() -> None:
        def it_should_show_help(capsys) -> None:
            with pytest.raises(SystemExit):
                args = [
                    *_engine_args(DbEngine.MSSQL),
                    *_server_args(),
                    *_integrated_security_arg(),
                ]

                parse_main_arguments(args)

                _assert_error_message(capsys)

    def describe_given_integrated_security() -> None:
        def describe_and_using_encryption() -> None:
            def it_should_add_Encrypt_to_connection_string() -> None:
                args = [
                    *_path_args(),
                    *_server_args(),
                    *_db_name_args(),
                    *_integrated_security_arg(),
                    *_encrypt_args(),
                ]

                parsed = parse_main_arguments(args)

                url = str(parsed.get_adapter().engine.url)
                assert "Encrypt=yes" in url
                assert "TrustServerCertificate=yes" not in url

            def describe_and_trusting_the_server_certificate() -> None:
                def it_should_set_trusted_connection_in_the_connection_string() -> None:
                    args = [
                        *_path_args(),
                        *_server_args(),
                        *_db_name_args(),
                        *_integrated_security_arg(),
                        *_encrypt_args(),
                        *_trust_certificate_args(),
                    ]

                    parsed = parse_main_arguments(args)

                    url = str(parsed.get_adapter().engine.url)
                    assert "Encrypt=yes" in url
                    assert "TrustServerCertificate=yes" in url

        def it_should_not_require_username_and_password(capsys) -> None:
            args = [
                *_path_args(),
                *_server_args(),
                *_db_name_args(),
                *_integrated_security_arg(),
            ]

            parsed = parse_main_arguments(args)

            assert parsed is not None, "No arguments detected"

            assert parsed.engine == DbEngine.MSSQL

            _assert_no_messages(capsys)

    def describe_given_using_integrated_security_short_flag() -> None:
        def it_should_not_require_username_and_password(capsys) -> None:
            args = [
                *_path_args(),
                *_server_args(),
                *_db_name_args(),
                "-i",
            ]

            parsed = parse_main_arguments(args)

            assert parsed is not None, "No arguments detected"

            assert parsed.engine == DbEngine.MSSQL

            _assert_no_messages(capsys)

    def describe_given_not_using_integrated_security() -> None:
        def it_should_require_username(capsys) -> None:
            with pytest.raises(SystemExit):
                args = [
                    *_path_args(),
                    *_server_args(),
                    *_db_name_args(),
                    *_password_args(),
                ]

                parse_main_arguments(args)

                _assert_error_message(capsys)

        def it_should_require_password(capsys) -> None:
            with pytest.raises(SystemExit):
                args = [
                    *_path_args(),
                    *_server_args(),
                    *_db_name_args(),
                    *_username_args(),
                ]

                parse_main_arguments(args)

                _assert_error_message(capsys)

    def describe_given_optional_port_is_provided() -> None:
        def it_should_inject_port_into_connection_string(capsys) -> None:
            args = [
                *_path_args(),
                *_server_args(),
                *_db_name_args(),
                *_integrated_security_arg(),
                *port_args(),
            ]

            parsed = parse_main_arguments(args)

            _assert_no_messages(capsys)

            assert parsed is not None, "No arguments detected"

            assert str(PORT) in str(parsed.get_adapter().engine.url)

    def it_should_parse_csv_path(capsys) -> None:
        args = [
            *_path_args(),
            *_server_args(),
            *_db_name_args(),
            *_integrated_security_arg(),
        ]

        parsed = parse_main_arguments(args)

        assert parsed is not None, "No arguments detected"

        assert parsed.csv_path == PATH

        _assert_no_messages(capsys)

    def describe_given_engine_mssql() -> None:
        def describe_given_using_integrated_security() -> None:
            def it_should_have_a_plain_connection_string(
                capsys,
            ) -> None:
                args = [
                    *_path_args(),
                    *_server_args(),
                    *_db_name_args(),
                    *_integrated_security_arg(),
                    *_engine_args(DbEngine.MSSQL),
                ]

                parsed = parse_main_arguments(args)

                _assert_no_messages(capsys)
                assert (
                    "mssql+pyodbc://localhost,1433/EdFi_ODS?driver=ODBC+Driver+17+for+SQL+Server"
                    == str(parsed.get_adapter().engine.url)
                )

        @pytest.fixture
        def fixture(capsys) -> MainArguments:
            # Arrange
            args = [
                *_path_args(),
                *_server_args(),
                *_db_name_args(),
                *_engine_args(DbEngine.MSSQL),
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
                    *_path_args(),
                    *_server_args(),
                    *_db_name_args(),
                    *_integrated_security_arg(),
                    *_engine_args(DbEngine.MSSQL),
                    "--log-level",
                    "DEBUG",
                ]

                parsed = parse_main_arguments(args)

                _assert_no_messages(capsys)

                assert parsed is not None, "No arguments detected"
                assert parsed.log_level == "DEBUG"

    # NOT TESTING POSTGRESQL UNTIL STORY REQUIRES POSTGRESQL


def describe_when_initializing_MainArguments() -> None:
    def it_passes_initializer_arguments_into_instance_properties() -> None:
        csv_path = "some/path"
        engine = DbEngine.MSSQL
        logging = LOG_LEVELS[0]
        db_name = "whatever"
        server = "somwehere"
        port = 2343
        encrypt = True
        trust_certificate = True

        a = MainArguments(
            csv_path,
            engine,
            logging,
            server,
            db_name,
            port,
            encrypt,
            trust_certificate,
        )

        assert a.csv_path == csv_path
        assert a.engine == engine
        assert a.log_level == logging
        assert a.server == server
        assert a.port == port
        assert a.engine == engine
        assert a.encrypt == encrypt
        assert a.trust_certificate == trust_certificate
        assert a.db_name == db_name


def describe_when_getting_db_operations_adapter() -> None:
    def describe_engine_is_postgresql() -> None:
        def it_should_raise_NotImplementedError() -> None:
            with pytest.raises(NotImplementedError):
                a = MainArguments(
                    "some/path", DbEngine.MSSQL, LOG_LEVELS[0], "server", "database", 0
                )

                a.engine = "PostgreSQL"
                a.build_mssql_adapter_with_integrated_security()
                a.get_db_operations_adapter()

    def describe_engine_is_mssql() -> None:
        def it_should_create_the_requested_adapter() -> None:
            a = MainArguments(
                "some/path", DbEngine.MSSQL, LOG_LEVELS[0], "server", "database", 0
            )
            a.build_mssql_adapter_with_integrated_security()
            actual = a.get_db_operations_adapter()

            assert type(actual) is SqlLmsOperations
