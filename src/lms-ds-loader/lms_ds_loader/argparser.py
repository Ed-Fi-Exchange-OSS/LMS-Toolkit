# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import configargparse
from lms_ds_loader.constants import Constants
from lms_ds_loader.arguments import Arguments


def parse_arguments(args_in) -> Arguments:
    assert args_in is not None

    parser = configargparse.ArgParser()
    parser.add("-c", "--csvpath", help="base path for input files", required=True)
    parser.add(
        "-e",
        "--engine",
        help="database engine",
        choices=[Constants.DbEngine.MSSQL, Constants.DbEngine.POSTGRESQL],
        default=Constants.DbEngine.MSSQL,
    )
    parser.add(
        "-s", "--server", help="database server name or IP address", required=True
    )
    parser.add("--port", help="server port number", type=int)
    parser.add("-d", "--dbname", help="database name", required=True)

    USE_INTEGRATED = "--useintegratedsecurity"
    USE_INTEGRATED_SHORT = "-i"
    parser.add(
        USE_INTEGRATED_SHORT,
        USE_INTEGRATED,
        help="use Integrated Security",
        action="store_true",
    )

    user_name_required = (
        USE_INTEGRATED not in args_in and USE_INTEGRATED_SHORT not in args_in
    )
    parser.add("-u", "--username", required=user_name_required)
    parser.add(
        "-p", "--password", required=user_name_required, env_var="MSSQL_PASSWORD"
    )

    args_parsed = parser.parse_args(args_in)

    arguments = Arguments(args_parsed.csvpath, args_parsed.engine)

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
