# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from os import path, scandir
from typing import List

from sqlparse import split

from edfi_sql_adapter.sql_adapter import Adapter, Statement


logger = logging.getLogger(__name__)


SCHEMA_SCRIPT_NAME = "0001_initialize_lms_database.sql"


def _get_scripts_dir(engine: str) -> str:
    return path.join(path.dirname(__file__), "scripts", engine)


def _get_scripts(scripts_dir: str) -> List[str]:
    with scandir(scripts_dir) as entries:
        return sorted(
            [
                entry.path
                for entry in entries
                if entry.is_file() and entry.name.endswith(".sql") and not entry.name == SCHEMA_SCRIPT_NAME
            ]
        )


def _read_statements_from_file(full_path: str) -> List[str]:
    raw_sql: str
    with open(full_path) as f:
        raw_sql = f.read()

    statements: List[str] = split(raw_sql)
    return statements


def _migration_name(migration: str) -> str:
    return path.split(migration)[-1].split(".")[0].lower()


def _script_has_been_run(adapter: Adapter, migration: str) -> bool:
    migration_name = _migration_name(migration)
    statement = f"select 1 from lms.migrationjournal_harmonizer where script = '{migration_name}';"
    response = adapter.get_int(statement)

    return bool(response == 1)


def _record_migration_in_journal(adapter: Adapter, migration: str) -> None:
    migration_name = _migration_name(migration)

    statement = Statement(
        f"insert into lms.migrationjournal_harmonizer (script) values ('{migration_name}');",
        "Updating migration journal table",
    )

    adapter.execute([statement])


def _lms_migration_journal_exists(adapter: Adapter) -> bool:
    statement = """
select
    count(table_name)
from
    information_schema.tables
where
    table_schema like 'lms' and
    -- First option covers SQL Server if set to case sensitive mode,
    -- second option covers PostgreSQL
    table_name in ('MigrationJournal_Harmonizer', 'migrationjournal_harmonizer');
"""
    response = adapter.get_int(statement)
    return bool(response == 1)


def _run_migration_script(adapter: Adapter, migration: str) -> None:

    logger.debug(f"Running migration {migration}...")

    statements = _read_statements_from_file(migration)
    adapter.execute_script(statements)

    _record_migration_in_journal(adapter, migration)

    logger.debug(f"Done with migration {migration}.")


def _initialize_migrations(scripts_dir: str, adapter: Adapter):
    logger.debug("Creating schema and migration table...")

    migration = path.join(scripts_dir, SCHEMA_SCRIPT_NAME)
    _run_migration_script(adapter, migration)


def migrate(engine: str, adapter: Adapter) -> None:
    """
    Runs database migration scripts for installing LMS table schema into the
    destination database.

    Parameters
    ----------
    adapter: sql_adapter
        SQL Alchemy database engine object.
    """
    logger.info("Begin database auto-migration...")

    scripts_dir = _get_scripts_dir(engine)

    if not _lms_migration_journal_exists(adapter):
        _initialize_migrations(scripts_dir, adapter)

    for migration in _get_scripts(scripts_dir):
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
