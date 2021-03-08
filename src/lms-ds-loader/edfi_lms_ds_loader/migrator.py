# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from os import path
from typing import List

from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import ProgrammingError
from sqlparse import split

from edfi_lms_ds_loader.sql_adapter import get_int, execute_statements


logger = logging.getLogger(__name__)

MIGRATION_SCRIPTS = [
    # CAUTION: these scripts will run in order from "top to bottom", so it is
    # critical to maintain the script order at all times.
    "initialize_lms_database",
    "create_user_tables"
]


def _get_script_path(engine: Engine, script_name: str) -> str:
    script_dir = path.join(path.dirname(__file__), "scripts", engine.name)
    return path.join(script_dir, script_name)


def _read_statements_from_file(full_path: str) -> List[str]:
    raw_sql: str
    with open(full_path) as f:
        raw_sql = f.read()

    statements: List[str] = split(raw_sql)
    return statements


def _script_has_been_run(engine: Engine, migration: str) -> bool:
    try:
        statement = f"SELECT 1 FROM lms.migrationjournal WHERE script = '{migration}';"
        response = get_int(engine, statement)

        return bool(response == 1)
    except ProgrammingError as error:
        if (
            # PostgreSLQ error
            "psycopg2.errors.UndefinedTable" in error.args[0] or
            # SQL Server error
            "Invalid object name" in error.args[0]
           ):
            # This means it is a fresh database where the migrationjournal table
            # has not been installed yet.
            return False

        raise


def _record_migration_in_journal(engine: Engine, migration: str) -> None:
    statement = f"INSERT INTO lms.migrationjournal (script) values ('{migration}');"

    execute_statements(engine, [statement])


def migrate(engine: Engine) -> None:
    logger.info("Begin database auto-migration...")

    for migration in MIGRATION_SCRIPTS:
        if _script_has_been_run(engine, migration):
            logger.debug(f"Migration {migration} has already run and will not be re-run.")
            return

        logger.debug(f"Running migration {migration}...")

        script_name = f"{migration}.sql"
        migration_script = _get_script_path(engine, script_name)

        statements = _read_statements_from_file(migration_script)
        execute_statements(engine, statements)

        _record_migration_in_journal(engine, migration)

        logger.debug(f"Done with migration {migration}.")

    logger.info("Done with database auto-migration.")
