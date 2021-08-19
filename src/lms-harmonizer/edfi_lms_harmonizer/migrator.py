# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from os import path
from typing import List

from sqlalchemy.exc import ProgrammingError
from sqlparse import split

from edfi_sql_adapter.sql_adapter import Adapter, Statement


logger = logging.getLogger(__name__)

MIGRATION_SCRIPTS = [
    # CAUTION: these scripts will run in order from "top to bottom", so it is
    # critical to maintain the script order at all times.
    "0001_initialize_lms_database",
    "0002_harmonize_lmsuser_canvas",
    "0003_harmonize_lmsuser_schoology",
    "0004_harmonize_lmsuser_google-classroom",
    "0005_harmonize_lmssection_canvas",
    "0006_harmonize_lmssection_google_classroom",
    "0007_harmonize_lmssection_schoology",
    "0008_view_exceptions_LMSSection",
    "0009_view_exceptions_LMSUser",
    "0010_harmonize_assignment",
    "0011_harmonize_assignment_submissions",
    "0012_view_missing_assignment_category_descriptors",
    "0013_view_missing_assignmentsubmission_status_descriptors",
    "0014_view_assignment_submissions_exceptions",
    "0015_view_assignments_exceptions",
]


def _get_script_path(adapter: Adapter, script_name: str) -> str:
    script_dir = path.join(path.dirname(__file__), "scripts", adapter.engine.name)
    return path.join(script_dir, script_name)


def _read_statements_from_file(full_path: str) -> List[str]:
    raw_sql: str
    with open(full_path) as f:
        raw_sql = f.read()

    statements: List[str] = split(raw_sql)
    return statements


def _script_has_been_run(adapter: Adapter, migration: str) -> bool:
    try:
        statement = f"SELECT 1 FROM lms.MigrationJournal_Harmonizer WHERE script = '{migration}';"
        response = adapter.get_int(statement)

        return bool(response == 1)
    except ProgrammingError as error:
        if (
            # PostgreSLQ error
            "psycopg2.errors.UndefinedTable" in error.args[0]
            or
            # SQL Server error
            "Invalid object name" in error.args[0]
        ):
            # This means it is a fresh database where the migrationjournal table
            # has not been installed yet.
            return False

        raise


def _record_migration_in_journal(adapter: Adapter, migration: str) -> None:
    statement = Statement(
        f"INSERT INTO lms.MigrationJournal_Harmonizer (script) values ('{migration}');",
        "Updating migration journal table"
    )

    adapter.execute([statement])


def _lms_migration_journal_exists(adapter: Adapter) -> bool:
    statement = """
SELECT CASE WHEN EXISTS
    (SELECT *
     FROM INFORMATION_SCHEMA.TABLES
     WHERE TABLE_SCHEMA = 'lms'
     AND TABLE_NAME = 'MigrationJournal_Harmonizer')
THEN 1 ELSE 0 END
""".strip()

    return adapter.get_int(statement) == 1


def _run_migration_script(adapter: Adapter, migration: str) -> None:

    logger.debug(f"Running migration {migration}...")

    migration_script = _get_script_path(adapter, f"{migration}.sql")

    statements = _read_statements_from_file(migration_script)
    adapter.execute_script(statements)

    _record_migration_in_journal(adapter, migration)

    logger.debug(f"Done with migration {migration}.")


def migrate(adapter: Adapter) -> None:
    """
    Runs database migration scripts for installing LMS table schema into the
    destination database.

    Parameters
    ----------
    adapter: sql_adapter
        SQL Alchemy database engine object.
    """
    logger.info("Begin database auto-migration...")

    if not _lms_migration_journal_exists(adapter):
        _run_migration_script(adapter, "0001_initialize_lms_database")

    for migration in MIGRATION_SCRIPTS:
        # The following block of code does not belong in _run_migration_script
        # because it will throw an exception if the migration journal does not
        # exist, and therefore is not appropriate when initializing the LMS
        # database.
        if _script_has_been_run(adapter, migration):
            logger.debug(
                f"Migration {migration} has already run and will not be re-run."
            )
            continue

        _run_migration_script(adapter, migration)

    logger.info("Done with database auto-migration.")
