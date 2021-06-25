# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from subprocess import run
import os
import sys


def _lms_script_path(script_name: str) -> str:
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "docs",
            "supporting-artifacts",
            script_name,
        )
    )


def _edfi_script_path(script_name: str) -> str:
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "docs",
            "metaed-project",
            "MetaEdOutput",
            "EdFi",
            "Database",
            "SQLServer",
            "ODS",
            "Structure",
            script_name,
        )
    )


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


def _run(command: str):

    print(f"\033[95m{command}\033[0m")

    # Some system configurations on Windows-based CI servers have trouble
    # finding poetry, others do not. Explicitly calling "cmd /c" seems to help,
    # though unsure why.

    if os.name == "nt":
        # All versions of Windows are "nt"
        command = f"cmd /c {command}"

    result = run(command)

    if result.returncode != 0:
        # Only exits the script for non-zero return code
        exit(result.returncode)


def _execute_sql_against_master(sql: str):
    _run(f"sqlcmd -Q \"{sql}\"")


def _execute_sql_against_database(dbname: str, sql: str):
    _run(f"sqlcmd -d {dbname} -Q \"{sql}\"")


def _execute_sql_file_against_database(dbname: str, filename: str):
    _run(f"sqlcmd -d {dbname} -i \"{filename}\"")


def main() -> None:
    _execute_sql_against_master("DROP DATABASE IF EXISTS test_harmonizer_lms_toolkit_e2e; CREATE DATABASE test_harmonizer_lms_toolkit_e2e")

    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _edfi_script_path("0010-Schemas.sql"))
    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _edfi_script_path("0020-Tables.sql"))
    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _edfi_script_path("0030-ForeignKeys.sql"))
    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _edfi_script_path("0040-IdColumnUniqueIndexes.sql"))
    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _edfi_script_path("0050-ExtendedProperties.sql"))

    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _lms_script_path("0010-LMS-Schemas.sql"))
    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _lms_script_path("0020-LMS-Tables.sql"))
    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _lms_script_path("0030-LMS-ForeignKeys.sql"))
    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _lms_script_path("0040-LMS-IdColumnUniqueIndexes.sql"))
    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _lms_script_path("0050-LMS-ExtendedProperties.sql"))

    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _lms_extension_script_path("0010-EXTENSION-LMSX-Schemas.sql"))
    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _lms_extension_script_path("0020-EXTENSION-LMSX-Tables.sql"))
    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _lms_extension_script_path("0030-EXTENSION-LMSX-ForeignKeys.sql"))
    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _lms_extension_script_path("0040-EXTENSION-LMSX-IdColumnUniqueIndexes.sql"))
    _execute_sql_file_against_database("test_harmonizer_lms_toolkit_e2e", _lms_extension_script_path("0050-EXTENSION-LMSX-ExtendedProperties.sql"))

    sys.exit(0)


main()
