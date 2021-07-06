# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
from subprocess import run
from typing import List

from .ServerConfig import ServerConfig


def test_path(directory: str, additional_message: str = "") -> None:
    """
    Tests that a directory path exists, throwing an error if not.

    Parameters
    ----------
    directory: str
        The path to test.

    additional_message: str
        Optional message to append to the standard message.
    """
    if not os.path.exists(directory):
        raise RuntimeError(f"Path `{directory}` does not exist. {additional_message}")


def _sqlcmd_parameters_from(config: ServerConfig) -> List[str]:
    login: List[str] = (
        ["-E"]
        if config.useintegratedsecurity
        else ["-U", config.username, "-P", config.password]
    )

    return ["-S", f"{config.server},{config.port}", *login]


def _run_command(arg_list: List[str]) -> None:
    run(arg_list, check=True)


def run_sqlcmd(config: ServerConfig, command: str) -> None:
    _run_command(["sqlcmd.exe", "-b", *_sqlcmd_parameters_from(config), "-Q", command])


def drop_database(config: ServerConfig) -> None:
    command = f"""
IF DB_ID('{config.db_name}') IS NOT NULL
BEGIN
ALTER DATABASE {config.db_name} SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
DROP DATABASE {config.db_name};
END;
"""
    run_sqlcmd(config, command)


def _get_amt_path() -> str:
    pwd = os.path.dirname(__file__)

    parent = os.path.join(pwd, "..")
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


def install_database(config: ServerConfig) -> None:
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


def install_analytics_middle_tier(config: ServerConfig) -> None:
    args = [
        "dotnet",
        "run",
        "--project",
        _get_amt_console_path(),
        "--connectionString",
        config.get_dotnet_connection_string(),
        "--options",
        "Engage"
    ]

    _run_command(args)
