# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from edfi_lms_ds_loader.helpers.argparser import parse_main_arguments, MainArguments
from edfi_lms_ds_loader.helpers.constants import DbEngine, LOG_LEVELS
from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations


PATH = "./lms_udm_files"
SERVER = "localhost"
DB_NAME = "EdFi_ODS"
USERNAME = "my_user"
PASSWORD = "my_password"
PORT = 1234


def path_args():
    return ["--csvpath", PATH]


def engine_args(engine):
    return ["--engine", engine]


def server_args():
    return ["--server", SERVER]


def port_args():
    return ["--port", str(PORT)]


def db_name_args():
    return ["--dbname", DB_NAME]


def integrated_security_arg():
    return ["--useintegratedsecurity"]


def username_args():
    return ["--username", USERNAME]


def password_args():
    return ["--password", PASSWORD]


def assert_no_messages(capsys):
    out, err = capsys.readouterr()

    assert err == "", "There should be an error message"
    assert out == "", "There should not be an output message"


def assert_error_message(capsys):
    out, err = capsys.readouterr()

    assert err != "", "There should be an error message"
    assert out == "", "There should not be an output message"


def describe_when_parsing_system_arguments():
    def describe_given_arguments_is_an_empty_list():
        def it_should_show_help(capsys):
            with pytest.raises(SystemExit):
                parse_main_arguments(list())

                out, err = capsys.readouterr()

                assert err != "", "There should be an error message"
                assert out == "", "There should not be an output message"

    def describe_given_arguments_do_not_include_path():
        def it_should_show_help(capsys):
            with pytest.raises(SystemExit):
                args = [
                    *engine_args(DbEngine.MSSQL),
                    *server_args(),
                    *db_name_args(),
                    *integrated_security_arg(),
                ]

                parse_main_arguments(args)

                assert_error_message(capsys)

    def describe_given_arguments_do_not_include_engine():
        def it_should_default_to_mssql(capsys):
            args = [
                *path_args(),
                *server_args(),
                *db_name_args(),
                *integrated_security_arg(),
            ]

            parsed = parse_main_arguments(args)

            assert parsed is not None, "No arguments detected"

            assert parsed.engine == DbEngine.MSSQL

            assert_no_messages(capsys)

    def describe_given_arguments_do_not_include_server():
        def it_should_show_help(capsys):
            with pytest.raises(SystemExit):
                args = [
                    *engine_args(DbEngine.MSSQL),
                    *server_args(),
                    *integrated_security_arg(),
                ]

                parse_main_arguments(args)

                assert_error_message(capsys)

    def describe_given_integrated_security():
        def it_should_not_require_username_and_password(capsys):
            args = [
                *path_args(),
                *server_args(),
                *db_name_args(),
                *integrated_security_arg(),
            ]

            parsed = parse_main_arguments(args)

            assert parsed is not None, "No arguments detected"

            assert parsed.engine == DbEngine.MSSQL

            assert_no_messages(capsys)

    def describe_given_using_integrated_security_short_flag():
        def it_should_not_require_username_and_password(capsys):
            args = [
                *path_args(),
                *server_args(),
                *db_name_args(),
                "-i",
            ]

            parsed = parse_main_arguments(args)

            assert parsed is not None, "No arguments detected"

            assert parsed.engine == DbEngine.MSSQL

            assert_no_messages(capsys)

    def describe_given_not_using_integrated_security():
        def it_should_require_username(capsys):
            with pytest.raises(SystemExit):
                args = [
                    *path_args(),
                    *server_args(),
                    *db_name_args(),
                    *password_args(),
                ]

                parse_main_arguments(args)

                assert_error_message(capsys)

        def it_should_require_password(capsys):
            with pytest.raises(SystemExit):
                args = [
                    *path_args(),
                    *server_args(),
                    *db_name_args(),
                    *username_args(),
                ]

                parse_main_arguments(args)

                assert_error_message(capsys)

    def describe_given_optional_port_is_provided():
        def it_should_inject_port_into_connection_string(capsys):
            args = [
                *path_args(),
                *server_args(),
                *db_name_args(),
                *integrated_security_arg(),
                *port_args(),
            ]

            parsed = parse_main_arguments(args)

            assert_no_messages(capsys)

            assert parsed is not None, "No arguments detected"

            assert str(PORT) in parsed.connection_string

    def it_should_parse_csv_path(capsys):
        args = [
            *path_args(),
            *server_args(),
            *db_name_args(),
            *integrated_security_arg(),
        ]

        parsed = parse_main_arguments(args)

        assert parsed is not None, "No arguments detected"

        assert parsed.csv_path == PATH

        assert_no_messages(capsys)

    def describe_given_engine_mssql():
        def describe_given_using_integrated_security():
            def it_should_set_trusted_connection_in_the_connection_string(capsys):
                args = [
                    *path_args(),
                    *server_args(),
                    *db_name_args(),
                    *integrated_security_arg(),
                    *engine_args(DbEngine.MSSQL),
                ]

                parsed = parse_main_arguments(args)

                assert_no_messages(capsys)

                assert parsed is not None, "No arguments detected"

                # Test the details of the connection string in a more appropriate test
                # suite - test only enough here to prove the point
                assert "Trusted_Connection=yes" in parsed.connection_string

        @pytest.fixture
        def fixture(capsys):
            # Arrange
            args = [
                *path_args(),
                *server_args(),
                *db_name_args(),
                *engine_args(DbEngine.MSSQL),
                *username_args(),
                *password_args(),
                *port_args(),
            ]

            # Act
            parsed = parse_main_arguments(args)

            assert_no_messages(capsys)

            return parsed

        def it_should_set_server_name_in_the_connection_string(
             fixture
        ):
            # Test the details of the connection string in a more appropriate test
            # suite - test only enough here to prove the point
            assert SERVER in fixture.connection_string

        def it_should_set_port_in_the_connection_string(
            fixture
        ):
            # Test the details of the connection string in a more appropriate test
            # suite - test only enough here to prove the point
            assert str(PORT) in fixture.connection_string

        def it_should_set_database_name_in_the_connection_string(
            fixture
        ):
            # Test the details of the connection string in a more appropriate test
            # suite - test only enough here to prove the point
            assert DB_NAME in fixture.connection_string

        def it_should_set_username_in_the_connection_string(
            fixture
        ):
            # Test the details of the connection string in a more appropriate test
            # suite - test only enough here to prove the point
            assert USERNAME in fixture.connection_string

        def it_should_set_password_in_the_connection_string(
            fixture
        ):
            # Test the details of the connection string in a more appropriate test
            # suite - test only enough here to prove the point
            assert PASSWORD in fixture.connection_string

        def given_optional_non_default_log_level():
            def it_should_parse_the_log_level(capsys):
                args = [
                    *path_args(),
                    *server_args(),
                    *db_name_args(),
                    *integrated_security_arg(),
                    *engine_args(DbEngine.MSSQL),
                    "--log-level",
                    "DEBUG"
                ]

                parsed = parse_main_arguments(args)

                assert_no_messages(capsys)

                assert parsed is not None, "No arguments detected"
                assert parsed.log_level == "DEBUG"

    # NOT TESTING POSTGRESQL UNTIL STORY REQUIRES POSTGRESQL


def describe_when_initializing_MainArguments():
    def it_passes_initializer_arguments_into_instance_properties():
        csv_path = "some/path"
        engine = DbEngine.MSSQL
        logging = LOG_LEVELS[0]

        a = MainArguments(csv_path, engine, logging)

        assert a.csv_path == csv_path
        assert a.engine == engine
        assert a.log_level == logging


def describe_when_setting_connection_string():
    def describe_given_invalid_engine():
        with pytest.raises(ValueError):
            MainArguments(
                "bogus", "bogus", LOG_LEVELS[0]
            ).set_connection_string_using_integrated_security(
                "server", 20, "db_name"
            )

    def describe_given_engine_is_mssql():
        def describe_given_using_integrated_security():
            def describe_given_port_is_provided():
                def it_should_return_a_pyodbc_connection_string_with_trusted_connection():
                    server = "my-server"
                    database = "my-database"
                    port = 1234
                    expect = "mssql+pyodbc://my-server,1234/my-database?driver=ODBC+Driver+17+for+SQL+Server?Trusted_Connection=yes"

                    a = MainArguments("some/path", DbEngine.MSSQL, LOG_LEVELS[0])
                    a.set_connection_string_using_integrated_security(
                        server,
                        port,
                        database,
                    )

                    assert a.connection_string == expect

            def describe_given_port_is_not_provided():
                def it_should_use_default_value_of_1433():
                    server = "my-server"
                    database = "my-database"
                    port = None
                    expected = "mssql+pyodbc://my-server,1433/my-database?driver=ODBC+Driver+17+for+SQL+Server?Trusted_Connection=yes"

                    a = MainArguments("some/path", DbEngine.MSSQL, LOG_LEVELS[0])
                    a.set_connection_string_using_integrated_security(
                        server,
                        port,
                        database,
                    )

                    assert a.connection_string == expected

        def describe_given_using_username_and_password():
            def describe_given_port_is_provided():
                def it_should_return_a_pyodbc_connection_string_with_trusted_connection():
                    server = "my-server"
                    database = "my-database"
                    port = 1234
                    username = "me"
                    password = "yo"
                    expected = "mssql+pyodbc://me:yo@my-server,1234/my-database?driver=ODBC+Driver+17+for+SQL+Server"

                    a = MainArguments("some/path", DbEngine.MSSQL, LOG_LEVELS[0])
                    a.set_connection_string(server, port, database, username, password)

                    assert a.connection_string == expected

            def describe_given_port_is_not_provided():
                def it_should_use_default_value_of_1433():
                    expected = "mssql+pyodbc://me:yo@my-server,1433/my-database?driver=ODBC+Driver+17+for+SQL+Server"

                    server = "my-server"
                    database = "my-database"
                    port = None
                    username = "me"
                    password = "yo"

                    a = MainArguments("some/path", DbEngine.MSSQL, LOG_LEVELS[0])
                    a.set_connection_string(server, port, database, username, password)

                    assert a.connection_string == expected


def describe_when_getting_db_operations_adapter():
    def describe_engine_is_postgresql():
        def it_should_raise_NotImplementedError():
            with pytest.raises(NotImplementedError):
                a = MainArguments(
                    "some/path", DbEngine.MSSQL, LOG_LEVELS[0]
                )
                a.set_connection_string(
                    "server", None, "database", "username", "password"
                )

                a.engine = "PostgreSQL"
                a.get_db_operations_adapter()

    def describe_engine_is_mssql():
        def it_should_create_the_requested_adapter():
            a = MainArguments("some/path", DbEngine.MSSQL, LOG_LEVELS[0])
            a.set_connection_string(
                "server", None, "database", "username", "password"
            )
            actual = a.get_db_operations_adapter()

            assert type(actual) is MssqlLmsOperations
