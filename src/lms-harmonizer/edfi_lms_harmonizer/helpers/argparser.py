# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
import os
from typing import List, Union

from configargparse import ArgParser  # type: ignore
from sqlalchemy.engine import Engine as sa_Engine
from sqlalchemy import create_engine as sa_create_engine

from .constants import LOG_LEVELS


@dataclass
class MainArguments:
    """
    Container for holding arguments parsed at the command line.

    Parameters
    ----------
    log_level : str
        The log level for the tool.
    """

    log_level: str

    @staticmethod
    def _get_mssql_port(port: Union[int, None]) -> int:
        if not port:
            port = 1433

        return port

    def set_connection_string_using_integrated_security(
        self, server: str, port: Union[int, None], db_name: str
    ) -> None:
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
        port = MainArguments._get_mssql_port(port)
        self.connection_string = f"mssql+pyodbc://{server},{port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server?Trusted_Connection=yes"

    def set_connection_string(
        self,
        server: str,
        port: Union[int, None],
        db_name: str,
        username: str,
        password: str,
    ) -> None:
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
        port = MainArguments._get_mssql_port(port)
        self.connection_string = f"mssql+pyodbc://{username}:{password}@{server},{port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"

    def get_db_engine(self) -> sa_Engine:
        return sa_create_engine(self.connection_string)


def parse_main_arguments(args_in: List[str]) -> MainArguments:
    """
    Configures the command-line interface.

    Parameters
    ----------
    args_in : list of str
        Full argument list from the command line.

    Returns
    -------
    arguments  : MainArguments
        A populated `MainArguments` object.
    """

    parser = ArgParser()

    parser.add(  # type: ignore
        "-s",
        "--server",
        help="Database server name or IP address",
        required=True,
        env_var="DB_SERVER",
    )
    parser.add(  # type: ignore
        "--port",
        help="Database server port number",
        type=int,
        env_var="DB_PORT",
    )
    parser.add(  # type: ignore
        "-d",
        "--dbname",
        help="Name of the database with the LMS tables.",
        env_var="DB_NAME",
        required=True,
    )

    USE_INTEGRATED = "--useintegratedsecurity"
    USE_INTEGRATED_SHORT = "-i"

    parser.add(  # type: ignore
        USE_INTEGRATED_SHORT,
        USE_INTEGRATED,
        help="Use Integrated Security for the database connection.",
        action="store_true",
    )
    user_name_required = (
        USE_INTEGRATED not in args_in and USE_INTEGRATED_SHORT not in args_in
    )
    # This parameter doesn't work right when used from a .env file,
    # so adding a manual override
    integrated_env_var = os.getenv("USE_INTEGRATED_SECURITY")
    if integrated_env_var and integrated_env_var.lower() in ("true", "yes", "t", "y"):
        user_name_required = False

    parser.add(  # type: ignore
        "-u",
        "--username",
        required=user_name_required,
        env_var="DB_USERNAME",
        help="Database username, when not using integrated security.",
    )
    parser.add(  # type: ignore
        "-p",
        "--password",
        required=user_name_required,
        env_var="DB_PASSWORD",
        help="Database user password, when not using integrated security.",
    )

    parser.add(  # type: ignore
        "-l",
        "--log-level",
        required=False,
        help="The log level for the tool.",
        choices=LOG_LEVELS,
        type=str,
        default="INFO",
        env_var="LOG_LEVEL",
    )

    args_parsed = parser.parse_args(args_in)
    args_parsed.useintegratedsecurity = (
        args_parsed.useintegratedsecurity or not user_name_required
    )

    arguments = MainArguments(args_parsed.log_level)

    if args_parsed.useintegratedsecurity:
        arguments.set_connection_string_using_integrated_security(
            args_parsed.server, args_parsed.port, args_parsed.dbname
        )
    else:
        arguments.set_connection_string(
            args_parsed.server,
            args_parsed.port,
            args_parsed.dbname,
            args_parsed.username,
            args_parsed.password,
        )

    return arguments
