# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
import os
from typing import List, Union, Optional

from configargparse import ArgParser  # type: ignore
from sqlalchemy.engine import Engine as sa_Engine
from sqlalchemy import create_engine as sa_create_engine

from .constants import LOG_LEVELS
from edfi_sql_adapter import sql_adapter


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
    exceptions_report_directory: Optional[str]
    server: str
    db_name: str
    port: int

    def __post_init__(self) -> None:
        self.adapter: sql_adapter.Adapter

    def build_mssql_adapter(self, username: str, password: str) -> sql_adapter.Adapter:
        self.adapter = sql_adapter.create_mssql_adapter(
            username, password, self.server, self.db_name, self.port
        )

    def build_mssql_adapter_with_integrated_security(self) -> sql_adapter.Adapter:
        self.adapter = sql_adapter.create_mssql_adapter_with_integrated_security(
            self.server, self.db_name, self.port
        )

    def get_adapter(self) -> sql_adapter.Adapter:
        return self.adapter


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
        default=1433
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

    parser.add(  # type: ignore
        "-e",
        "--exceptions-report-directory",
        required=False,
        help="File path for optional output of a CSV exception report.",
        type=str,
        env_var="EXCEPTIONs_REPORT_DIRECTORY",
    )

    args_parsed = parser.parse_args(args_in)
    args_parsed.useintegratedsecurity = (
        args_parsed.useintegratedsecurity or not user_name_required
    )

    arguments = MainArguments(
        args_parsed.log_level,
        args_parsed.exceptions_report_directory,
        args_parsed.server,
        args_parsed.dbname,
        args_parsed.port,
    )

    if args_parsed.useintegratedsecurity:
        arguments.build_mssql_adapter_with_integrated_security()
    else:
        arguments.build_mssql_adapter(
            args_parsed.username,
            args_parsed.password,
        )

    return arguments
