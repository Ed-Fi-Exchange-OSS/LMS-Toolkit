# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from lms_ds_loader.arguments import DbConnection


class Test_DbConnection:
    class Test_when_using_mssql:
        class Test_when_using_integrated_security:
            def test_when_all_arguments_provided_then_return_pyodbc_connection_string(
                self,
            ):
                server = "my-server"
                database = "my-database"
                port = 1234
                expected = "mssql+pyodbc://my-server,1234/my-database?driver=SQL Server?Trusted_Connection=yes"

                connection_string = (
                    DbConnection.build_for_mssql_with_integrated_security(
                        server, port, database
                    )
                )

                assert connection_string == expected

            def test_when_server_is_None_then_expect_assertion_error(self):
                with pytest.raises(AssertionError):
                    DbConnection.build_for_mssql_with_integrated_security(
                        None, "a", "a"
                    )

            def test_when_server_is_whitepsace_then_expect_assertion_error(self):
                with pytest.raises(AssertionError):
                    DbConnection.build_for_mssql_with_integrated_security(
                        "   ", "a", "a"
                    )

            def test_when_port_is_None_then_override_with_1433(self):
                server = "my-server"
                database = "my-database"
                port = None
                expected = "mssql+pyodbc://my-server,1433/my-database?driver=SQL Server?Trusted_Connection=yes"

                connection_string = (
                    DbConnection.build_for_mssql_with_integrated_security(
                        server, port, database
                    )
                )

                assert connection_string == expected

            def test_when_port_is_whitepsace_then_override_with_1433(self):
                server = "my-server"
                database = "my-database"
                port = "   "
                expected = "mssql+pyodbc://my-server,1433/my-database?driver=SQL Server?Trusted_Connection=yes"

                connection_string = (
                    DbConnection.build_for_mssql_with_integrated_security(
                        server, port, database
                    )
                )

                assert connection_string == expected

            def test_when_database_name_is_None_then_expect_assertion_error(self):
                with pytest.raises(AssertionError):
                    DbConnection.build_for_mssql_with_integrated_security(
                        "a", "a", None
                    )

            def test_when_database_name_is_whitepsace_then_expect_assertion_error(self):
                with pytest.raises(AssertionError):
                    DbConnection.build_for_mssql_with_integrated_security(
                        "a", "a", "   "
                    )

            def test_when_all_arguments_provided_then_return_pyodbc_connection_string(
                self,
            ):
                server = "my-server"
                database = "my-database"
                port = 1234
                username = "me"
                password = "yo"
                expected = (
                    "mssql+pyodbc://me:yo@my-server,1234/my-database?driver=SQL Server"
                )

                connection_string = DbConnection.build_for_mssql(
                    server, port, database, username, password
                )

                assert connection_string == expected

            def test_when_server_is_None_then_expect_assertion_error(self):
                with pytest.raises(AssertionError):
                    server = None
                    database = "my-database"
                    port = 1234
                    username = "me"
                    password = "yo"

                    DbConnection.build_for_mssql(
                        server, port, database, username, password
                    )

            def test_when_server_is_whitepsace_then_expect_assertion_error(self):
                with pytest.raises(AssertionError):
                    server = "     "
                    database = "my-database"
                    port = 1234
                    username = "me"
                    password = "yo"

                    DbConnection.build_for_mssql(
                        server, port, database, username, password
                    )

            def test_when_port_is_None_then_override_with_1433(self):
                expected = (
                    "mssql+pyodbc://me:yo@my-server,1433/my-database?driver=SQL Server"
                )

                server = "my-server"
                database = "my-database"
                port = None
                username = "me"
                password = "yo"

                connection_string = DbConnection.build_for_mssql(
                    server, port, database, username, password
                )

                assert connection_string == expected

            def test_when_port_is_whitepsace_then_override_with_1433(self):
                expected = (
                    "mssql+pyodbc://me:yo@my-server,1433/my-database?driver=SQL Server"
                )

                server = "my-server"
                database = "my-database"
                port = "    "
                username = "me"
                password = "yo"

                connection_string = DbConnection.build_for_mssql(
                    server, port, database, username, password
                )

                assert connection_string == expected

            def test_when_database_name_is_None_then_expect_assertion_error(self):
                with pytest.raises(AssertionError):
                    server = "my-server"
                    database = None
                    port = 1234
                    username = "me"
                    password = "yo"

                    DbConnection.build_for_mssql(
                        server, port, database, username, password
                    )

            def test_when_database_name_is_whitepsace_then_expect_assertion_error(self):
                with pytest.raises(AssertionError):
                    server = "my-server"
                    database = "     "
                    port = 1234
                    username = "me"
                    password = "yo"

                    DbConnection.build_for_mssql(
                        server, port, database, username, password
                    )
