# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from os import path, scandir
from pathlib import Path
from typing import List
from collections import namedtuple

from sqlparse import split

from edfi_sql_adapter.sql_adapter import Adapter, Statement
from edfi_lms_ds_loader.helpers.constants import DbEngine


logger = logging.getLogger(__name__)
Migration = namedtuple("Migration", "path name")


def _get_migration_name(migration_file: str) -> str:
    # Extracts from full path and chops off the extension
    return Path(migration_file).stem


def _get_file_names(engine: str) -> List[Migration]:
    script_dir = path.join(path.dirname(__file__), "scripts", engine)
    files: List[Migration] = []

    with scandir(script_dir) as all_files:
        for file in all_files:
            if file.path.endswith(".sql"):
                files.append(Migration(file.path, _get_migration_name(file.name)))

    files.sort()

    return files


def _read_statements_from_file(full_path: str) -> List[str]:
    raw_sql: str
    with open(full_path) as f:
        raw_sql = f.read()

    statements: List[str] = split(raw_sql)
    return statements


def _migrationjournal_exists(adapter: Adapter) -> bool:
    statement = """
SELECT
    COUNT(table_name)
FROM
    information_schema.tables
WHERE
    table_schema LIKE 'lms' AND
    table_name = 'migrationjournal';
"""
    response = adapter.get_int(statement)
    return bool(response == 1)


def _script_has_been_run(adapter: Adapter, migration: str) -> bool:
    if (not _migrationjournal_exists(adapter)):
        return False

    statement = f"SELECT 1 FROM lms.migrationjournal WHERE script = '{migration}';"
    response = adapter.get_int(statement)
    return bool(response == 1)


def _record_migration_in_journal(adapter: Adapter, migration: str) -> None:
    statement = Statement(
        f"INSERT INTO lms.migrationjournal (script) values ('{migration}');",
        "Updating migration journal table",
    )

    adapter.execute([statement])


def _run_migration_script(adapter: Adapter, migration: Migration) -> None:

    logger.debug(f"Running migration {migration.name}...")

    statements = _read_statements_from_file(migration.path)
    adapter.execute_script(statements)

    _record_migration_in_journal(adapter, migration.name)

    logger.debug(f"Done with migration {migration.name}.")


def migrate(adapter: Adapter, engine: str = DbEngine.MSSQL) -> None:
    """
    Runs database migration scripts for installing LMS table schema into the
    destination database.

    Parameters
    ----------
    adapter: sql_adapter
        SQL Alchemy database engine object.
    """
    logger.info("Begin database auto-migration...")

    for migration in _get_file_names(engine):
        # The following block of code does not belong in _run_migration_script
        # because it will throw an exception if the migration journal does not
        # exist, and therefore is not appropriate when initializing the LMS
        # database.
        if _script_has_been_run(adapter, migration.name):
            logger.debug(
                f"Migration {migration.name} has already run and will not be re-run."
            )
            continue

        _run_migration_script(adapter, migration)

    logger.info("Done with database auto-migration.")
