# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from edfi_lms_ds_loader.helpers.argparser import parse_main_arguments, MainArguments
from edfi_lms_ds_loader.helpers.constants import DbEngine, LOG_LEVELS
from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations


class Test_parse_main_arguments:

    PATH = "./lms_udm_files"
    SERVER = "localhost"
    DB_NAME = "EdFi_ODS"
    USERNAME = "my_user"
    PASSWORD = "my_password"
    PORT = 1234

    def path_args(self):
        return ["--csvpath", self.PATH]

    def engine_args(self, engine):
        return ["--engine", engine]

    def server_args(self):
        return ["--server", self.SERVER]

    def port_args(self):
        return ["--port", str(self.PORT)]

    def db_name_args(self):
        return ["--dbname", self.DB_NAME]

    def integrated_security_arg(self):
        return ["--useintegratedsecurity"]

    def username_args(self):
        return ["--username", self.USERNAME]

    def password_args(self):
        return ["--password", self.PASSWORD]

    def assert_no_messages(self, capsys):
        out, err = capsys.readouterr()

        assert err == "", "There should be an error message"
        assert out == "", "There should not be an output message"

    def assert_error_message(self, capsys):
        out, err = capsys.readouterr()

        assert err != "", "There should be an error message"
        assert out == "", "There should not be an output message"

    def test_when_arguments_is_an_empty_list_then_show_help(self, capsys):

        with pytest.raises(SystemExit):
            parse_main_arguments(list())

            out, err = capsys.readouterr()

            assert err != "", "There should be an error message"
            assert out == "", "There should not be an output message"

    def test_when_arguments_do_not_include_path_then_show_help(self, capsys):

        with pytest.raises(SystemExit):
            args = [
                *self.engine_args(DbEngine.MSSQL),
                *self.server_args(),
                *self.db_name_args(),
                *self.integrated_security_arg(),
            ]

            parse_main_arguments(args)

            self.assert_error_message(capsys)

    def test_when_arguments_do_not_include_engine_then_default_to_mssql(self, capsys):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
        ]

        parsed = parse_main_arguments(args)

        assert parsed is not None, "No arguments detected"

        assert parsed.engine == DbEngine.MSSQL

        self.assert_no_messages(capsys)

    def test_when_arguments_do_not_include_server_then_show_help(self, capsys):

        with pytest.raises(SystemExit):
            args = [
                *self.engine_args(DbEngine.MSSQL),
                *self.server_args(),
                *self.integrated_security_arg(),
            ]

            parse_main_arguments(args)

            self.assert_error_message(capsys)

    def test_when_using_integrated_security_then_username_and_password_not_required(
        self, capsys
    ):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
        ]

        parsed = parse_main_arguments(args)

        assert parsed is not None, "No arguments detected"

        assert parsed.engine == DbEngine.MSSQL

        self.assert_no_messages(capsys)

    def test_when_using_integrated_security_short_flag_then_username_and_password_not_required(
        self, capsys
    ):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            "-i",
        ]

        parsed = parse_main_arguments(args)

        assert parsed is not None, "No arguments detected"

        assert parsed.engine == DbEngine.MSSQL

        self.assert_no_messages(capsys)

    def test_when_not_using_integrated_security_then_username_is_required(self, capsys):

        with pytest.raises(SystemExit):
            args = [
                *self.path_args(),
                *self.server_args(),
                *self.db_name_args(),
                *self.password_args(),
            ]

            parse_main_arguments(args)

            self.assert_error_message(capsys)

    def test_when_not_using_integrated_security_then_password_is_required(self, capsys):

        with pytest.raises(SystemExit):
            args = [
                *self.path_args(),
                *self.server_args(),
                *self.db_name_args(),
                *self.username_args(),
            ]

            parse_main_arguments(args)

            self.assert_error_message(capsys)

    def test_maps_port_into_response(self, capsys):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
            *self.port_args(),
        ]

        parsed = parse_main_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        assert str(self.PORT) in parsed.connection_string

    def test_maps_csv_path_into_response(self, capsys):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
        ]

        parsed = parse_main_arguments(args)

        assert parsed is not None, "No arguments detected"

        assert parsed.csv_path == self.PATH

        self.assert_no_messages(capsys)

    def test_when_using_security_with_engine_mssql_then_create_mssql_connection_with_trusted_connection(
        self, capsys
    ):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
            *self.engine_args(DbEngine.MSSQL),
        ]

        parsed = parse_main_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert "Trusted_Connection=yes" in parsed.connection_string

    def test_when_engine_mssql_then_create_mssql_connection_with_server_name(
        self, capsys
    ):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
            *self.engine_args(DbEngine.MSSQL),
        ]

        parsed = parse_main_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert self.SERVER in parsed.connection_string

    def test_when_engine_mssql_with_port_then_create_mssql_connection_with_port(
        self, capsys
    ):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
            *self.engine_args(DbEngine.MSSQL),
            *self.port_args(),
        ]

        parsed = parse_main_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert str(self.PORT) in parsed.connection_string

    def test_when_engine_mssql_then_create_mssql_connection_with_database_name(
        self, capsys
    ):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
            *self.engine_args(DbEngine.MSSQL),
        ]

        parsed = parse_main_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert self.DB_NAME in parsed.connection_string

    def test_when_using_sql_account_with_engine_mssql_then_create_mssql_connection_with_username(
        self, capsys
    ):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.engine_args(DbEngine.MSSQL),
            *self.username_args(),
            *self.password_args(),
        ]

        parsed = parse_main_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert self.USERNAME in parsed.connection_string

    def test_when_using_sql_account_with_engine_mssql_then_create_mssql_connection_with_password(
        self, capsys
    ):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.engine_args(DbEngine.MSSQL),
            *self.username_args(),
            *self.password_args(),
        ]

        parsed = parse_main_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert self.PASSWORD in parsed.connection_string

    def test_when_overriding_default_log_level(self, capsys):
        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
            *self.engine_args(DbEngine.MSSQL),
            "--log-level",
            "DEBUG"
        ]

        parsed = parse_main_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"
        assert parsed.log_level == "DEBUG"

    # NOT TESTING POSTGRESQL UNTIL STORY REQUIRES POSTGRESQL


class Test_MainArguments:
    def test_initializer(self):
        csv_path = "some/path"
        engine = DbEngine.MSSQL
        logging = LOG_LEVELS[0]

        a = MainArguments(csv_path, engine, logging)

        assert a.csv_path == csv_path
        assert a.engine == engine
        assert a.log_level == logging

    class Test_when_setting_connection_string:
        class Test_given_invalid_engine:
            def test_given_using_integrated_security(self):
                with pytest.raises(ValueError):
                    MainArguments(
                        "bogus", "bogus", LOG_LEVELS[0]
                    ).set_connection_string_using_integrated_security(
                        "server", 20, "db_name"
                    )

            def test_given_username_and_password(self):
                with pytest.raises(ValueError):
                    MainArguments("bogus", "bogus", LOG_LEVELS[0]).set_connection_string(
                        "server", 20, "db_name", "username", "password"
                    )

        class Test_given_engine_is_mssql:
            class Test_given_using_integrated_security:
                def test_given_all_arguments_provided_then_return_pyodbc_connection_string(
                    self,
                ):
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

                def test_given_port_is_None_then_override_with_1433(self):
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

            class Test_given_not_using_integrated_security:
                def test_given_all_arguments_provided_then_return_pyodbc_connection_string(
                    self,
                ):
                    server = "my-server"
                    database = "my-database"
                    port = 1234
                    username = "me"
                    password = "yo"
                    expected = "mssql+pyodbc://me:yo@my-server,1234/my-database?driver=ODBC+Driver+17+for+SQL+Server"

                    a = MainArguments("some/path", DbEngine.MSSQL, LOG_LEVELS[0])
                    a.set_connection_string(server, port, database, username, password)

                    assert a.connection_string == expected

                def test_given_port_is_None_then_override_with_1433(self):
                    expected = "mssql+pyodbc://me:yo@my-server,1433/my-database?driver=ODBC+Driver+17+for+SQL+Server"

                    server = "my-server"
                    database = "my-database"
                    port = None
                    username = "me"
                    password = "yo"

                    a = MainArguments("some/path", DbEngine.MSSQL, LOG_LEVELS[0])
                    a.set_connection_string(server, port, database, username, password)

                    assert a.connection_string == expected

        class Test_when_getting_db_operations_adapter:
            def test_given_engine_is_postgresql_then_raise_NotImplementedError(self):
                with pytest.raises(NotImplementedError):
                    a = MainArguments(
                        "some/path", DbEngine.MSSQL, LOG_LEVELS[0]
                    )
                    a.set_connection_string(
                        "server", None, "database", "username", "password"
                    )

                    a.engine = "PostgreSQL"
                    a.get_db_operations_adapter()

            def test_given_engine_is_mssql_then_return_proper_object(self):
                a = MainArguments("some/path", DbEngine.MSSQL, LOG_LEVELS[0])
                a.set_connection_string(
                    "server", None, "database", "username", "password"
                )
                actual = a.get_db_operations_adapter()

                assert type(actual) is MssqlLmsOperations
