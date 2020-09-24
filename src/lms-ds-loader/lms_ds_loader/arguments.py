# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from lms_ds_loader.constants import Constants


class Arguments:
    """
    Container for holding arguments parsed at the command line.

    Parameters
    ----------
    csv_path : str
        Base path for finding CSV files.
    engine : str
        Database engine, either "mssql" or "postgresql"
    """

    def __init__(self, csv_path, engine):
        self.csv_path = csv_path
        self.engine = engine
        self.connection_string = ""

    @staticmethod
    def _build_for_mssql_integrated_security(server, port, db_name):
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
        """
        Creates a PyODBC connection string using integrated security.

        Parameters
        ----------
        server : str
            Database server name or IP address.
        port : int or None
            Database port number.
        db_name : str
            Database name.
        """

        if self.engine == Constants.DbEngine.MSSQL:
            self.connection_string = Arguments._build_for_mssql_integrated_security(server, port, db_name)

    def set_connection_string(self, server, port, db_name, username, password):
        """
        Creates a PyODBC connection string using username and password.

        Parameters
        ----------
        server : str
            Database server name or IP address.
        port : int or None
            Database port number.
        db_name : str
            Database name.
        username : str
            Database user name.
        password : str
            Database password.
        """

        if self.engine == Constants.DbEngine.MSSQL:
            self.connection_string = Arguments._build_for_mssql(server, port, db_name, username, password)
