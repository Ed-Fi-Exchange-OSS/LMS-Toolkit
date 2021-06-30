# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import subprocess
import os
from tests_integration_sql.server_config import ServerConfig
from typing import List


def _run(command: List[str]):

    command_as_string: str = " ".join(command)
    print(f"\033[95m{command_as_string}\033[0m")

    # Some system configurations on Windows-based CI servers have trouble
    # finding poetry, others do not. Explicitly calling "cmd /c" seems to help,
    # though unsure why.

    if os.name == "nt":
        # All versions of Windows are "nt"
        command = ["cmd", "/c", *command]

    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate()

    if result.returncode != 0:
        raise Exception("Command failed %d %a %a" % (result.returncode, stdout, stderr))


def run_harmonizer(config: ServerConfig):
    login: List[str] = (
        ["--useintegratedsecurity"]
        if config.useintegratedsecurity == "true"
        else ["--username", config.username, "--password", config.password]
    )
    _run(
        [
            "poetry",
            "run",
            "python",
            "edfi_lms_harmonizer",
            "--server",
            config.server,
            "--port",
            config.port,
            "--dbname",
            config.db_name,
            *login,
        ],
    )


def _sqlcmd_parameters_from(config: ServerConfig) -> List[str]:
    login: List[str] = (
        ["-E"]
        if config.useintegratedsecurity == "true"
        else ["-U", config.username, "-P", config.password]
    )

    return ["-S", f"{config.server},{config.port}", *login]


def _execute_sql_against_master(config: ServerConfig, sql: str):
    _run(["sqlcmd", "-b", *_sqlcmd_parameters_from(config), "-Q", sql])


def _execute_sql_file_against_database(config: ServerConfig, filename: str):
    _run(
        [
            "sqlcmd",
            "-b",
            "-I",
            *_sqlcmd_parameters_from(config),
            "-d",
            config.db_name,
            "-i",
            filename,
        ]
    )


def _edfi_script_path(script_name: str) -> str:
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "utils",
            "ods-core-sql-5.2",
            script_name,
        )
    )


def _load_edfi_scripts(config: ServerConfig):
    _execute_sql_file_against_database(config, _edfi_script_path("0010-Schemas.sql"))
    _execute_sql_file_against_database(config, _edfi_script_path("0020-Tables.sql"))
    # Note - intentionally not running foreign key scripts


def _lms_extension_script_path(script_name: str) -> str:
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "extension",
            "EdFi.Ods.Extensions.LMSX",
            "Artifacts",
            "MsSql",
            "Structure",
            "Ods",
            script_name,
        )
    )


def _load_lms_extension_scripts(config: ServerConfig):
    _execute_sql_file_against_database(
        config,
        _lms_extension_script_path("0010-EXTENSION-LMSX-Schemas.sql"),
    )
    _execute_sql_file_against_database(
        config,
        _lms_extension_script_path("0020-EXTENSION-LMSX-Tables.sql"),
    )
    # Note - intentionally not running foreign key scripts


def _load_ordered_scripts(config: ServerConfig, script_path: str):
    scripts: List[str] = list(
        map(lambda script: os.path.join(script_path, script), os.listdir(script_path))
    )
    for script in sorted(scripts):
        _execute_sql_file_against_database(config, script)


def _lms_migration_script_path() -> str:
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "src",
            "lms-ds-loader",
            "edfi_lms_ds_loader",
            "scripts",
            "mssql",
        )
    )


def _load_lms_migration_scripts(config: ServerConfig):
    _load_ordered_scripts(config, _lms_migration_script_path())


def _harmonizer_script_path() -> str:
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "extension",
            "EdFi.Ods.Extensions.LMSX",
            "LMS-Harmonizer",
        )
    )


def _load_harmonizer_scripts(config: ServerConfig):
    _load_ordered_scripts(config, _harmonizer_script_path())


def create_snapshot(config: ServerConfig):
    temp_filename: str = os.path.join(os.getcwd(), "temp_harmonizer_snapshot")
    _execute_sql_against_master(
        config,
        "DROP DATABASE IF EXISTS temp_harmonizer_snapshot;"
        "CREATE DATABASE temp_harmonizer_snapshot ON"
        f"    (NAME=[{config.db_name}], FILENAME='{temp_filename}')"
        f"    AS SNAPSHOT OF [{config.db_name}];",
    )


def delete_snapshot(config: ServerConfig):
    _execute_sql_against_master(
        config, "DROP DATABASE IF EXISTS temp_harmonizer_snapshot"
    )


def restore_snapshot(config: ServerConfig):
    _execute_sql_against_master(
        config,
        f"ALTER DATABASE {config.db_name} SET SINGLE_USER WITH ROLLBACK IMMEDIATE;"
        f"RESTORE DATABASE {config.db_name} "
        "FROM DATABASE_SNAPSHOT = 'temp_harmonizer_snapshot';"
        f"ALTER DATABASE {config.db_name} SET MULTI_USER;",
    )


def initialize_database(config: ServerConfig):
    _execute_sql_against_master(
        config,
        "DROP DATABASE IF EXISTS temp_harmonizer_snapshot;"
        f"DROP DATABASE IF EXISTS {config.db_name};"
        f"CREATE DATABASE {config.db_name};",
    )
    _load_edfi_scripts(config)
    _load_lms_extension_scripts(config)
    _load_lms_migration_scripts(config)
    _load_harmonizer_scripts(config)
