# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
from subprocess import run, PIPE
from typing import List

from .ServerConfig import ServerConfig


def _sqlcmd_parameters_from(config: ServerConfig) -> List[str]:
    login: List[str] = (
        ["-E"]
        if config.useintegratedsecurity
        else ["-U", config.username, "-P", config.password]
    )

    ENABLE_QUOTED_IDENTIFIERS = "-I"
    TERMINATE_ON_ERROR = "-b"
    return [
        ENABLE_QUOTED_IDENTIFIERS,
        TERMINATE_ON_ERROR,
        "-d",
        config.db_name,
        "-S",
        f"{config.server},{config.port}",
        *login,
    ]


def _run_command(arg_list: List[str]) -> None:
    print(f"Command arguments: {arg_list}")
    result = run(arg_list, stdout=PIPE, stderr=PIPE)

    stdout = result.stdout.decode("UTF-8")

    if result.returncode != 0 or result.stderr or "SQL exception" in stdout:
        raise Exception(stdout)


def _run_sqlcmd(config: ServerConfig, command: str, use_msdb: bool = False) -> None:

    connection_params = _sqlcmd_parameters_from(config)

    if use_msdb:
        # In this situation, we need to connect to a system database instead of
        # the real database: thus replace the real database with "msdb".
        connection_params = [
            p if p != config.db_name else "msdb" for p in connection_params
        ]

    _run_command(["sqlcmd.exe", *connection_params, "-Q", command])


def _run_file_using_sqlcmd(config: ServerConfig, file_path: str) -> None:
    print(f"Attempting to run SQL file {file_path}")
    _run_command(["sqlcmd.exe", *_sqlcmd_parameters_from(config), "-i", file_path])


def drop_database(config: ServerConfig) -> None:
    command = f"""
IF DB_ID('{config.db_name}') IS NOT NULL
BEGIN
ALTER DATABASE {config.db_name} SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
DROP DATABASE {config.db_name};
END;
"""
    _run_sqlcmd(config, command, use_msdb=True)


def _get_parent_directory() -> str:
    pwd = os.path.dirname(__file__)

    return os.path.join(pwd, "..")


def _get_amt_path() -> str:
    parent = _get_parent_directory()
    amt_path = ""

    while os.path.exists(parent):
        test_path = os.path.join(parent, "Ed-Fi-Analytics-Middle-Tier")

        if os.path.exists(test_path):
            amt_path = test_path
            break

        parent = os.path.join(parent, "..")

    if not amt_path:
        raise RuntimeError(
            "Unable to find Ed-Fi-Analytics-Middle-Tier in a parent directory"
        )

    return os.path.join(amt_path, "src")


def _get_amt_console_path() -> str:
    return os.path.join(_get_amt_path(), "EdFi.AnalyticsMiddleTier.Console")


def _get_dacpac_path() -> str:
    return os.path.join(
        _get_amt_path(), "EdFi.AnalyticsMiddleTier.Tests", "EdFi_Ods_3.2.dacpac"
    )


def install_ds32_database(config: ServerConfig) -> None:
    args = [
        "sqlpackage.exe",
        f"/SourceFile:{_get_dacpac_path()}",
        "/Action:Publish",
        f"/TargetServerName:{config.server}",
        f"/TargetDatabaseName:{config.db_name}",
    ]

    if not config.useintegratedsecurity:
        args.append(f"/TargetUser:{config.username}")
        args.append(f"/TargetPassword:{config.password}")

    _run_command(args)


def run_ordered_sql_scripts(src_path: List[str], config: ServerConfig) -> None:
    parent = _get_parent_directory()
    structure_path = os.path.join(parent, "..", "..", *src_path)

    files = sorted(
        [
            os.path.join(structure_path, f)
            for f in os.listdir(structure_path)
            # avoid getting directory names
            if f.endswith(".sql")
        ]
    )

    for script in files:
        _run_file_using_sqlcmd(config, script)


def install_lms_datastore(config: ServerConfig) -> None:
    src_path = ["src", "lms-ds-loader", "edfi_lms_ds_loader", "scripts", "mssql"]

    print("----> Installing LMS Data Store")
    run_ordered_sql_scripts(src_path, config)


def install_lmsx_extension(config: ServerConfig) -> None:
    src_path = ["extension", "EdFi.Ods.Extensions.LMSX", "Artifacts", "MsSql", "Structure", "Ods"]

    print("----> Installing LMSX Extension")
    run_ordered_sql_scripts(src_path, config)


def install_lms_harmonizer(config: ServerConfig) -> None:
    src_path = ["src", "lms-harmonizer", "edfi_lms_harmonizer", "scripts", "MsSql"]

    print("----> Installing LMS Harmonizer")
    run_ordered_sql_scripts(src_path, config)


def install_analytics_middle_tier(config: ServerConfig) -> None:
    args = [
        "dotnet",
        "run",
        "--project",
        _get_amt_console_path(),
        "--connectionString",
        config.get_dotnet_connection_string(),
        "--options",
        "Engage",
    ]

    print("----> Installing Analytics Middle Tier")
    _run_command(args)
