# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
import os
from typing import List

from configargparse import ArgParser  # type: ignore

from edfi_lms_ds_loader.helpers.constants import DbEngine, LOG_LEVELS
from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations
from edfi_sql_adapter.sql_adapter import (
    Adapter,
    create_mssql_adapter_with_integrated_security,
    create_mssql_adapter,
)


@dataclass
class MainArguments:
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
    log_level: str
    server: str
    db_name: str
    port: int
    encrypt: bool = False
    trust_certificate: bool = False

    def __post_init__(self) -> None:
        self.db_adapter: Adapter

    def _get_sql_server_port(self) -> int:
        return 1433 if not self.port or self.port == 0 else self.port

    # For future use
    # def _get_pgsql_server_port(self) -> int:
    #     return 5432 if not self.port or self.port == 0 else self.port

    def build_mssql_adapter(self, username: str, password: str) -> None:
        self.db_adapter = create_mssql_adapter(
            username,
            password,
            self.server,
            self.db_name,
            self._get_sql_server_port(),
            self.encrypt,
            self.trust_certificate,
        )

    def build_mssql_adapter_with_integrated_security(self) -> None:
        self.db_adapter = create_mssql_adapter_with_integrated_security(
            self.server,
            self.db_name,
            self._get_sql_server_port(),
            self.encrypt,
            self.trust_certificate,
        )

    def get_adapter(self) -> Adapter:
        if self.engine != DbEngine.MSSQL:
            raise NotImplementedError(
                f"Support for '{self.engine}' has not yet been implemented."
            )

        if not hasattr(self, "db_adapter"):
            raise RuntimeError("The SQL Adapter has not been initialized yet.")

        return self.db_adapter

    def get_db_operations_adapter(self) -> MssqlLmsOperations:
        return MssqlLmsOperations(self.get_adapter())


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
        "-c",
        "--csvpath",
        help="Base path for input files.",
        required=True,
        env_var="CSV_PATH",
    )
    parser.add(  # type: ignore
        "-e",
        "--engine",
        help="Database engine.",
        choices=[DbEngine.MSSQL, DbEngine.POSTGRESQL],
        default=DbEngine.MSSQL,
        env_var="DB_ENGINE",
    )
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

    # Retrieve this value because we need it in order to determine
    # if username and password are required
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
        "-n",
        "--encrypt",
        help="Encrypt the connection to the database.",
        action="store_true",
        env_var="ENCRYPT_SQL_CONNECTION",
    )
    parser.add(  # type: ignore
        "-t",
        "--trust-certificate",
        help="When encrypting connections, trust the server certificate. Useful for localhost debuggin with a self-signed certificate. USE WITH CAUTION.",
        action="store_true",
        env_var="TRUST_SERVER_CERTIFICATE",
    )

    args_parsed = parser.parse_args(args_in)

    # Need to add this back in because reading it manually earlier
    # seems to cause it to be misread by the parser.
    args_parsed.useintegratedsecurity = (
        args_parsed.useintegratedsecurity or not user_name_required
    )

    arguments = MainArguments(
        args_parsed.csvpath,
        args_parsed.engine,
        args_parsed.log_level,
        args_parsed.server,
        args_parsed.dbname,
        args_parsed.port,
        args_parsed.encrypt,
        args_parsed.trust_certificate,
    )

    if args_parsed.useintegratedsecurity:
        arguments.build_mssql_adapter_with_integrated_security()
    else:
        arguments.build_mssql_adapter(
            args_parsed.username,
            args_parsed.password,
        )

    return arguments
