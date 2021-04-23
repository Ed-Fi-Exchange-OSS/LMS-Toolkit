# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from os import path
from typing import List

from sqlalchemy.engine.base import Engine as sa_Engine
from sqlalchemy.exc import ProgrammingError
from sqlparse import split

from edfi_lms_ds_loader.sql_adapter import get_int, execute_statements


logger = logging.getLogger(__name__)

MIGRATION_SCRIPTS = [
    # CAUTION: these scripts will run in order from "top to bottom", so it is
    # critical to maintain the script order at all times.
    "initialize_lms_database",
    "create_processed_files_table",
    "create_user_tables",
    "create_section_tables",
    "create_assignment_tables",
    "create_section_association_tables",
    "create_assignment_submission_tables",
    "create_section_activity_tables",
    "create_system_activity_tables",
    "create_attendance_tables",
    "remove_startdate_enddate_from_sectionassociation"
]


def _get_script_path(engine: sa_Engine, script_name: str) -> str:
    script_dir = path.join(path.dirname(__file__), "scripts", engine.name)
    return path.join(script_dir, script_name)


def _read_statements_from_file(full_path: str) -> List[str]:
    raw_sql: str
    with open(full_path) as f:
        raw_sql = f.read()

    statements: List[str] = split(raw_sql)
    return statements


def _script_has_been_run(engine: sa_Engine, migration: str) -> bool:
    try:
        statement = f"SELECT 1 FROM lms.migrationjournal WHERE script = '{migration}';"
        response = get_int(engine, statement)

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


def _record_migration_in_journal(engine: sa_Engine, migration: str) -> None:
    statement = f"INSERT INTO lms.migrationjournal (script) values ('{migration}');"

    execute_statements(engine, [statement])


def _lms_schema_exists(engine: sa_Engine) -> bool:
    statement = """
select case when exists (
    select 1 from INFORMATION_SCHEMA.SCHEMATA where schema_name = 'lms'
) then 1 else 0 end
""".strip()

    return get_int(engine, statement) == 1


def _run_migration_script(engine: sa_Engine, migration: str) -> None:

    logger.debug(f"Running migration {migration}...")

    migration_script = _get_script_path(engine, f"{migration}.sql")

    statements = _read_statements_from_file(migration_script)
    execute_statements(engine, statements)

    _record_migration_in_journal(engine, migration)

    logger.debug(f"Done with migration {migration}.")


def migrate(engine: sa_Engine) -> None:
    """
    Runs database migration scripts for installing LMS table schema into the
    destination database.

    Parameters
    ----------
    engine: sa_Engine
        SQL Alchemy database engine object.
    """
    logger.info("Begin database auto-migration...")

    if not _lms_schema_exists(engine):
        _run_migration_script(engine, "initialize_lms_database")

    for migration in MIGRATION_SCRIPTS:
        # The following block of code does not belong in _run_migration_script
        # because it will throw an exception if the migration journal does not
        # exist, and therefore is not appropriate when initializing the LMS
        # database.
        if _script_has_been_run(engine, migration):
            logger.debug(
                f"Migration {migration} has already run and will not be re-run."
            )
            continue

        _run_migration_script(engine, migration)

    logger.info("Done with database auto-migration.")
