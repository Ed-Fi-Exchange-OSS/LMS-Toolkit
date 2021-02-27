# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from os import path
from typing import Any, Callable, List

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, session as sa_session
from sqlalchemy.exc import ProgrammingError
from sqlparse import split

logger = logging.getLogger(__name__)

MIGRATION_SCRIPTS = [
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

    return split(raw_sql)


def _execute_statements(engine: Engine, statements: List[str]):
    Session = sessionmaker(bind=engine)
    session = Session()

    for statement in statements:
        # Ignore MSSQL "GO" statements
        if statement == "GO":
            continue

        # Deliberately throwing away all results. Counting on exception handling
        # if there are any errors
        session.execute(statement)

    session.commit()
    session.close()


def _execute_transaction(engine: Engine, function: Callable[[object], Any]) -> Any:
    Session = sessionmaker(bind=engine)

    session = Session()
    response: Any
    try:
        response = function(session)

        session.commit()

        return response
    except ProgrammingError:
        session.rollback()
        raise
    finally:
        session.close()


def _script_has_been_run(engine: Engine, migration: str) -> bool:
    def __callback(session: sa_session):
        statement = f"SELECT 1 FROM lms.migrationjournal WHERE script = '{migration}';"
        return session.execute(statement).scalar()

    try:
        response = _execute_transaction(engine, __callback)

        return response == 1
    except ProgrammingError as error:
        # TODO: try this on SQL Server and find the appropriate error message
        logger.warn(type(error))
        logger.warn(error.args)
        if (
            "psycopg2.errors.UndefinedTable" in error.args[0] or
            "Invalid object name" in error.args[0]
           ):
            # This means it is a fresh database where the migrationjournal table
            # has not been installed yet.
            return False

        raise


def _record_migration_in_journal(engine: Engine, migration: str):
    statement = f"INSERT INTO lms.migrationjournal (script) values ('{migration}');"

    _execute_statements(engine, [statement])


def _run_file(engine: Engine, migration: str):
    if _script_has_been_run(engine, migration):
        logger.debug(f"Migration {migration} has already run and will not be re-run.")
        return

    logger.info(f"Running migration {migration}...")

    script_name = f"{migration}.sql"
    migration_script = _get_script_path(engine, script_name)

    statements = _read_statements_from_file(migration_script)
    _execute_statements(engine, statements)

    _record_migration_in_journal(engine, migration)

    logger.debug(f"Done with migration {migration}.")


def migrate(engine: Engine):
    logger.info("Begin database auto-migration...")
    for migration in MIGRATION_SCRIPTS:
        _run_file(engine, migration)

    logger.info("Done with database auto-migration.")
