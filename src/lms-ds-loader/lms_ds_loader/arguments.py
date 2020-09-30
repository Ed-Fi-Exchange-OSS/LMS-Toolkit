# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass

from lms_ds_loader.constants import Constants
from lms_ds_loader.mssql_lms_operations import MssqlLmsOperations


@dataclass
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

    csv_path: str
    engine: str

    @staticmethod
    def _get_mssql_port(port):
        if not port:
            port = 1433
        if type(port) == str and port.strip() == "":
            port = 1433

        return port

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
        assert type(server) is str, "Argument `server` must be a string"
        assert server.strip() != "", "Argument `server` cannot be whitespace"

        assert type(db_name) is str, "Argument `db_name` must be a string"
        assert db_name.strip() != "", "Argument `db_name` cannot be whitespace"

        if self.engine == Constants.DbEngine.MSSQL:
            port = Arguments._get_mssql_port(port)
            self.connection_string = f"mssql+pyodbc://{server},{port}/{db_name}?driver=SQL Server?Trusted_Connection=yes"

        else:
            raise ValueError(f"Invalid `engine` parameter value: {self.engine}")

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

        assert type(server) is str, "Argument `server` must be a string`"
        assert server.strip() != "", "Argument `server` cannot be whitespace"

        assert type(db_name) is str, "Argument `db_name` must be a string`"
        assert db_name.strip() != "", "Argument `db_name` cannot be whitespace"

        assert type(username) is str, "Argument `username` must be a string`"
        assert username.strip() != "", "Argument `username` cannot be whitespace"

        assert type(password) is str, "Argument `password` must be a string`"
        assert password.strip() != "", "Argument `password` cannot be whitespace"

        if self.engine == Constants.DbEngine.MSSQL:
            port = Arguments._get_mssql_port(port)
            self.connection_string = f"mssql+pyodbc://{username}:{password}@{server},{port}/{db_name}?driver=SQL Server"

        else:
            raise ValueError(f"Invalid `engine` parameter value: {self.engine}")

        return self

    def get_db_operations_adapter(self):
        if self.engine == Constants.DbEngine.MSSQL:
            return MssqlLmsOperations(self.connection_string)

        raise NotImplementedError(
            f"Support for '{self.engine}' has not yet been implemented."
        )
