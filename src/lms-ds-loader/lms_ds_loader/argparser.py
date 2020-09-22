# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import argparse
from lms_ds_loader.constants import Constants
from lms_ds_loader.arguments import Arguments, DbConnection


def parse_arguments(args_in) -> Arguments:
    assert args_in is not None

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--csvpath", help="base path for input files", required=True
    )
    parser.add_argument(
        "-e",
        "--engine",
        help=f"database engine",
        choices=[Constants.MSSQL, Constants.POSTGRESQL],
        default=Constants.MSSQL,
    )
    parser.add_argument(
        "-s", "--server", help="database server name or IP address", required=True
    )
    parser.add_argument("--port", help="server port number", type=int)
    parser.add_argument("-d", "--dbname", help="database name", required=True)

    USE_INTEGRATED = "--useintegratedsecurity"
    parser.add_argument(
        "-i", USE_INTEGRATED, help="use Integrated Security", action="store_true"
    )

    user_name_required = USE_INTEGRATED not in args_in
    parser.add_argument("-u", "--username", required=user_name_required)
    parser.add_argument("-p", "--password", required=user_name_required)

    args_parsed = parser.parse_args(args_in)

    db_connection = None
    if args_parsed.engine == Constants.MSSQL:
        if args_parsed.useintegratedsecurity:
            db_connection = DbConnection.build_for_mssql_with_integrated_security(
                args_parsed.server, args_parsed.port, args_parsed.dbname
            )
        else:
            db_connection = DbConnection.build_for_mssql(
                args_parsed.server,
                args_parsed.port,
                args_parsed.dbname,
                args_parsed.username,
                args_parsed.password,
            )

    return Arguments(args_parsed.csvpath, args_parsed.engine, db_connection)
