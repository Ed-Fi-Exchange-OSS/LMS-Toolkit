# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from lms_ds_loader.arguments import Arguments
from lms_ds_loader.constants import Constants


class Test_Arguments:
    def test_initializer(self):
        csv_path = "some/path"
        engine = Constants.DbEngine.MSSQL

        a = Arguments(csv_path, engine)

        assert a.csv_path == csv_path
        assert a.engine == engine

    class Test_when_setting_connection_string:
        class Test_given_invalid_engine:
            def test_given_using_integrated_security(self):
                with pytest.raises(ValueError):
                    Arguments(
                        "bogus", "bogus"
                    ).set_connection_string_using_integrated_security(
                        "server", 20, "db_name"
                    )

            def test_given_username_and_password(self):
                with pytest.raises(ValueError):
                    Arguments("bogus", "bogus").set_connection_string(
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
                    expect = "mssql+pyodbc://my-server,1234/my-database?driver=SQL Server?Trusted_Connection=yes"

                    a = Arguments("some/path", Constants.DbEngine.MSSQL)
                    a.set_connection_string_using_integrated_security(
                        server, port, database,
                    )

                    assert a.connection_string == expect

                def test_given_server_is_None_then_expect_assertion_error(self):
                    with pytest.raises(AssertionError):
                        Arguments(
                            "some/path", Constants.DbEngine.MSSQL
                        ).set_connection_string_using_integrated_security(
                            None, "a", "a"
                        )

                def test_given_server_is_whitepsace_then_expect_assertion_error(self):
                    with pytest.raises(AssertionError):
                        Arguments(
                            "some/path", Constants.DbEngine.MSSQL
                        ).set_connection_string_using_integrated_security(
                            "    ", "a", "a"
                        )

                def test_given_port_is_None_then_override_with_1433(self):
                    server = "my-server"
                    database = "my-database"
                    port = None
                    expected = "mssql+pyodbc://my-server,1433/my-database?driver=SQL Server?Trusted_Connection=yes"

                    a = Arguments("some/path", Constants.DbEngine.MSSQL)
                    a.set_connection_string_using_integrated_security(
                        server, port, database,
                    )

                    assert a.connection_string == expected

                def test_given_port_is_whitepsace_then_override_with_1433(self):
                    server = "my-server"
                    database = "my-database"
                    port = "   "
                    expected = "mssql+pyodbc://my-server,1433/my-database?driver=SQL Server?Trusted_Connection=yes"

                    a = Arguments("some/path", Constants.DbEngine.MSSQL)
                    a.set_connection_string_using_integrated_security(
                        server, port, database,
                    )

                    assert a.connection_string == expected

                def test_given_database_name_is_None_then_expect_assertion_error(self):
                    with pytest.raises(AssertionError):
                        Arguments(
                            "some/path", Constants.DbEngine.MSSQL
                        ).set_connection_string_using_integrated_security(
                            "a", "a", None
                        )

                def test_given_database_name_is_whitepsace_then_expect_assertion_error(
                    self,
                ):
                    with pytest.raises(AssertionError):
                        Arguments(
                            "some/path", Constants.DbEngine.MSSQL
                        ).set_connection_string_using_integrated_security(
                            "a", "a", "   "
                        )

            class Test_given_not_using_integrated_security:
                def test_given_all_arguments_provided_then_return_pyodbc_connection_string(
                    self,
                ):
                    server = "my-server"
                    database = "my-database"
                    port = 1234
                    username = "me"
                    password = "yo"
                    expected = "mssql+pyodbc://me:yo@my-server,1234/my-database?driver=SQL Server"

                    a = Arguments("some/path", Constants.DbEngine.MSSQL)
                    a.set_connection_string(server, port, database, username, password)

                    assert a.connection_string == expected

                def test_given_server_is_None_then_expect_assertion_error(self):
                    with pytest.raises(AssertionError):
                        server = None
                        database = "my-database"
                        port = 1234
                        username = "me"
                        password = "yo"

                        Arguments(
                            "some/path", Constants.DbEngine.MSSQL
                        ).set_connection_string(
                            server, port, database, username, password
                        )

                def test_given_server_is_whitepsace_then_expect_assertion_error(self):
                    with pytest.raises(AssertionError):
                        server = "     "
                        database = "my-database"
                        port = 1234
                        username = "me"
                        password = "yo"

                        Arguments(
                            "some/path", Constants.DbEngine.MSSQL
                        ).set_connection_string(
                            server, port, database, username, password
                        )

                def test_given_port_is_None_then_override_with_1433(self):
                    expected = "mssql+pyodbc://me:yo@my-server,1433/my-database?driver=SQL Server"

                    server = "my-server"
                    database = "my-database"
                    port = None
                    username = "me"
                    password = "yo"

                    a = Arguments("some/path", Constants.DbEngine.MSSQL)
                    a.set_connection_string(server, port, database, username, password)

                    assert a.connection_string == expected

                def test_given_port_is_whitepsace_then_override_with_1433(self):
                    expected = "mssql+pyodbc://me:yo@my-server,1433/my-database?driver=SQL Server"

                    server = "my-server"
                    database = "my-database"
                    port = "    "
                    username = "me"
                    password = "yo"

                    a = Arguments("some/path", Constants.DbEngine.MSSQL)
                    a.set_connection_string(server, port, database, username, password)

                    assert a.connection_string == expected

                def test_given_database_name_is_None_then_expect_assertion_error(self):
                    with pytest.raises(AssertionError):
                        server = "my-server"
                        database = None
                        port = 1234
                        username = "me"
                        password = "yo"

                        Arguments(
                            "some/path", Constants.DbEngine.MSSQL
                        ).set_connection_string(
                            server, port, database, username, password
                        )

                def test_given_database_name_is_whitepsace_then_expect_assertion_error(
                    self,
                ):
                    with pytest.raises(AssertionError):
                        server = "my-server"
                        database = "     "
                        port = 1234
                        username = "me"
                        password = "yo"

                        Arguments(
                            "some/path", Constants.DbEngine.MSSQL
                        ).set_connection_string(
                            server, port, database, username, password
                        )
