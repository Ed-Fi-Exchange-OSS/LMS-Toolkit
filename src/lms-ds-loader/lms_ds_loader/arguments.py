# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from lms_ds_loader.constants import Constants


class Arguments:

    # TODO: are these static or instance?
    csv_path = ""
    engine = ""
    connection_string = ""

    def __init__(self, csv_path, engine):
        self.csv_path = csv_path
        self.engine = engine

    @staticmethod
    def _build_for_mssql_with_integrated_security(server, port, db_name):
        assert server is not None
        assert server.strip() != ""

        assert db_name is not None
        assert db_name.strip() != ""

        if not port:
            port = 1433
        if type(port) == str and port.strip() == "":
            port = 1433

        return f"mssql+pyodbc://{server},{port}/{db_name}?driver=SQL Server?Trusted_Connection=yes"

    @staticmethod
    def _build_for_mssql(server, port, db_name, username, password):
        assert server is not None
        assert server.strip() != ""

        assert db_name is not None
        assert db_name.strip() != ""

        if not port:
            port = 1433
        if type(port) == str and port.strip() == "":
            port = 1433

        return f"mssql+pyodbc://{username}:{password}@{server},{port}/{db_name}?driver=SQL Server"

    def set_connection_string_using_integrated_security(self, server, port, db_name):
        if self.engine == Constants.MSSQL:
            self.connection_string = Arguments._build_for_mssql_with_integrated_security(server, port, db_name)

    def set_connection_string(self, server, port, db_name, username, password):
        if self.engine == Constants.MSSQL:
            self.connection_string = Arguments._build_for_mssql(server, port, db_name, username, password)
