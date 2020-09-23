# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from lms_ds_loader.argparser import parse_arguments
from lms_ds_loader.constants import Constants


class Test_parse_arguments:

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

    def test_when_arguments_object_is_None_then_throw_error(self):

        with pytest.raises(AssertionError):
            parse_arguments(None)

    def test_when_arguments_is_an_empty_list_then_show_help(self, capsys):

        with pytest.raises(SystemExit):
            parse_arguments(list())

            out, err = capsys.readouterr()

            assert err != "", "There should be an error message"
            assert out == "", "There should not be an output message"

    def test_when_arguments_do_not_include_path_then_show_help(self, capsys):

        with pytest.raises(SystemExit):
            args = [
                *self.engine_args(Constants.MSSQL),
                *self.server_args(),
                *self.db_name_args(),
                *self.integrated_security_arg(),
            ]

            parse_arguments(args)

            self.assert_error_message(capsys)

    def test_when_arguments_do_not_include_engine_then_default_to_mssql(self, capsys):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
        ]

        parsed = parse_arguments(args)

        assert parsed is not None, "No arguments detected"

        assert parsed.engine == Constants.MSSQL

        self.assert_no_messages(capsys)

    def test_when_arguments_do_not_include_server_then_show_help(self, capsys):

        with pytest.raises(SystemExit):
            args = [
                *self.engine_args(Constants.MSSQL),
                *self.server_args(),
                *self.integrated_security_arg(),
            ]

            parse_arguments(args)

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

        parsed = parse_arguments(args)

        assert parsed is not None, "No arguments detected"

        assert parsed.engine == Constants.MSSQL

        self.assert_no_messages(capsys)

    def test_when_not_using_integrated_security_then_username_is_required(self, capsys):

        with pytest.raises(SystemExit):
            args = [
                *self.path_args(),
                *self.server_args(),
                *self.db_name_args(),
                *self.password_args(),
            ]

            parse_arguments(args)

            self.assert_error_message(capsys)

    def test_when_not_using_integrated_security_then_password_is_required(self, capsys):

        with pytest.raises(SystemExit):
            args = [
                *self.path_args(),
                *self.server_args(),
                *self.db_name_args(),
                *self.username_args(),
            ]

            parse_arguments(args)

            self.assert_error_message(capsys)

    def test_maps_port_into_response(self, capsys):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
            *self.port_args(),
        ]

        parsed = parse_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        assert str(self.PORT) in parsed.db_connection

    def test_maps_csv_path_into_response(self, capsys):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
        ]

        parsed = parse_arguments(args)

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
            *self.engine_args(Constants.MSSQL),
        ]

        parsed = parse_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert "Trusted_Connection=yes" in parsed.db_connection

    def test_when_engine_mssql_then_create_mssql_connection_with_server_name(
        self, capsys
    ):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
            *self.engine_args(Constants.MSSQL),
        ]

        parsed = parse_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert self.SERVER in parsed.db_connection

    def test_when_engine_mssql_with_port_then_create_mssql_connection_with_port(
        self, capsys
    ):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
            *self.engine_args(Constants.MSSQL),
            *self.port_args(),
        ]

        parsed = parse_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert str(self.PORT) in parsed.db_connection

    def test_when_engine_mssql_then_create_mssql_connection_with_database_name(
        self, capsys
    ):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.integrated_security_arg(),
            *self.engine_args(Constants.MSSQL),
        ]

        parsed = parse_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert self.DB_NAME in parsed.db_connection

    def test_when_using_sql_account_with_engine_mssql_then_create_mssql_connection_with_username(
        self, capsys
    ):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.engine_args(Constants.MSSQL),
            *self.username_args(),
            *self.password_args(),
        ]

        parsed = parse_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert self.USERNAME in parsed.db_connection

    def test_when_using_sql_account_with_engine_mssql_then_create_mssql_connection_with_password(
        self, capsys
    ):

        args = [
            *self.path_args(),
            *self.server_args(),
            *self.db_name_args(),
            *self.engine_args(Constants.MSSQL),
            *self.username_args(),
            *self.password_args(),
        ]

        parsed = parse_arguments(args)

        self.assert_no_messages(capsys)

        assert parsed is not None, "No arguments detected"

        # Test the details of the connection string in a more appropriate test
        # suite - test only enough here to prove the point
        assert self.PASSWORD in parsed.db_connection

    # NOT TESTING POSTGRESQL UNTIL STORY REQUIRES POSTGRESQL
