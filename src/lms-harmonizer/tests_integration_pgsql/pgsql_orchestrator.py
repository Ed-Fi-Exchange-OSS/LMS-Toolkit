# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import subprocess
from os import environ, path, listdir
from platform import uname
import re
from tempfile import tempdir

from tests_integration_pgsql.pgsql_server_config import PgsqlServerConfig
from typing import List


SNAPSHOT_DATABASE = "temp_harmonizer_snapshot"


def _is_windows() -> bool:
    return uname().system == "Windows"


# TODO: consider unifying some of this code between this and mssql test library
def _run(config: PgsqlServerConfig, command: List[str]):

    command_as_string: str = " ".join(command)
    print(f"\033[95m{command_as_string}\033[0m")

    if command[0] == config.psql_cli and config.psql_cli != "psql":
        # Windows powershell command hack. When running a "psql" command,
        # PowerShell needs to get the command arguments in quotation marks,
        # otherwise the command processor will interpret some of the arguments.
        quoted_command = f"\"{' '.join(command[1:])}\""
        command = ["cmd", "/c", config.psql_cli, quoted_command]

    # TODO: make sure that .pgpass file can be used instead, since postgresql doesn't recommend
    # using an environment variable, and .pgpass is the only other option for unattended
    # execution of `psql`
    env = environ.copy()
    env["PGPASSWORD"] = config.password

    result = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, shell=True
    )
    stdout, stderr = result.communicate()

    if result.returncode != 0:
        raise Exception("Command failed %d %a %a. Offending command: <<%a>>" % (result.returncode, stdout, stderr, command_as_string))


def run_harmonizer(config: PgsqlServerConfig):
    harmonizer_path = path.abspath(path.join(
        path.dirname(__file__),
        "..",
        "edfi_lms_harmonizer"
    ))

    # The following command runs in Popen, which calls the OS shell (cmd.exe,
    # sh, bash, etc.). The password could have special characters in it that
    # would have meaning to the OS shell. Those characters need to be escaped
    # with the OS-specific escape character: ^ for Windows, and \ for Linux.
    # However, the command ends up being piped... and pipes end up requiring
    # triple escaping: ^^^ or \\\.
    pattern = r"([~`#$&*()\\|[\]{};'\"<>/?!])"
    escape_char = "^^^" if _is_windows() else "\\\\\\"
    replace = rf"{escape_char}\1"

    password = re.sub(pattern, replace, config.password)

    _run(
        config,
        [
            "poetry",
            "run",
            "python",
            harmonizer_path,
            "--server",
            config.server,
            "--port",
            config.port,
            "--dbname",
            config.db_name,
            "--username",
            config.username,
            "--password",
            password,
            "--engine",
            "postgresql",
        ],
    )


def _psql_parameters_from(config: PgsqlServerConfig) -> List[str]:
    return [
        "-b",  # Print failed SQL commands to standard error output.
        "-h",
        config.server,
        "-p",
        config.port,
        "-U",
        config.username,
    ]


# Only one SQL command can run at a time. psql does not return error codes to verify success
def _execute_sql_against_master(config: PgsqlServerConfig, sql: str):
    _run(
        config,
        [
            config.psql_cli,
            *_psql_parameters_from(config),
            "-d",
            "postgres",
            "-c",
            f"'{sql}'" if _is_windows() else sql,
        ],
    )


def _execute_sql_file_against_database(config: PgsqlServerConfig, filename: str):
    _run(
        config,
        [
            config.psql_cli,
            *_psql_parameters_from(config),
            "-d",
            config.db_name,
            "-f",
            filename,
        ],
    )


def _edfi_script_path(script_name: str) -> str:
    return path.normpath(
        path.join(
            path.dirname(__file__),
            "..",
            "..",
            "..",
            "utils",
            "ods-core-sql-5.2",
            "postgresql",
            script_name,
        )
    )


def _load_edfi_scripts(config: PgsqlServerConfig):
    _execute_sql_file_against_database(config, _edfi_script_path("0010-Schemas.sql"))
    _execute_sql_file_against_database(config, _edfi_script_path("0020-Tables.sql"))
    # Note - intentionally not running foreign key scripts


def _lms_extension_script_path(script_name: str) -> str:
    return path.normpath(
        path.join(
            path.dirname(__file__),
            "..",
            "..",
            "..",
            "extension",
            "EdFi.Ods.Extensions.LMSX",
            "Artifacts",
            "PgSql",
            "Structure",
            "Ods",
            script_name,
        )
    )


def _load_lms_extension_scripts(config: PgsqlServerConfig):
    _execute_sql_file_against_database(
        config,
        _lms_extension_script_path("0010-EXTENSION-LMSX-Schemas.sql"),
    )
    _execute_sql_file_against_database(
        config,
        _lms_extension_script_path("0020-EXTENSION-LMSX-Tables.sql"),
    )
    # Note - intentionally not running foreign key scripts


def _load_ordered_scripts(config: PgsqlServerConfig, script_path: str):
    files_in_path: List[str] = [
        f for f in listdir(script_path) if path.isfile(path.join(script_path, f))
    ]
    scripts: List[str] = list(
        map(lambda script: path.join(script_path, script), files_in_path)
    )
    for script in sorted(scripts):
        _execute_sql_file_against_database(config, script)


def _lms_migration_script_path() -> str:
    return path.normpath(
        path.join(
            path.dirname(__file__),
            "..",
            "..",
            "..",
            "src",
            "lms-ds-loader",
            "edfi_lms_ds_loader",
            "scripts",
            "postgresql",
        )
    )


def _load_lms_migration_scripts(config: PgsqlServerConfig):
    _load_ordered_scripts(config, _lms_migration_script_path())


def _drop_database(config: PgsqlServerConfig, db_name: str) -> None:
    sql = f"select pg_terminate_backend(pid) from pg_stat_activity where pid != pg_backend_pid() and datname = '{db_name}';"
    _execute_sql_against_master(config, sql)
    _execute_sql_against_master(config, f"drop database if exists {db_name};")


def _create_from_snapshot(config: PgsqlServerConfig):
    _drop_database(config, config.db_name)
    _execute_sql_against_master(
        config,
        f"create database {config.db_name} with template {SNAPSHOT_DATABASE};",
    )


def drop_snapshot(config: PgsqlServerConfig):
    _drop_database(config, SNAPSHOT_DATABASE)


def restore_snapshot(config: PgsqlServerConfig):
    _create_from_snapshot(config)


def initialize_database(config: PgsqlServerConfig):
    test_db = config.db_name

    drop_snapshot(config)

    _execute_sql_against_master(config, f"create database {SNAPSHOT_DATABASE};")
    config.db_name = SNAPSHOT_DATABASE
    _load_edfi_scripts(config)
    _load_lms_extension_scripts(config)
    _load_lms_migration_scripts(config)

    config.db_name = test_db
    _create_from_snapshot(config)
