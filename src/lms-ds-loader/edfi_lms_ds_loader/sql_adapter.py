# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

# Developer note: this adapter module is deliberately not unit tested.

import logging
from typing import Any, Callable, List, TypeVar

from sqlalchemy.engine.base import Engine as sa_Engine
from sqlalchemy.orm import sessionmaker, Session as sa_Session
from sqlalchemy.exc import ProgrammingError


logger = logging.getLogger(__name__)

T = TypeVar('T')


def execute_transaction(
    engine: sa_Engine, function: Callable[[sa_Session], T]
) -> T:
    Session = sessionmaker(bind=engine)

    session = Session()
    response: Any
    try:
        response = function(session)

        session.commit()

        return response
    except ProgrammingError as pe:
        session.rollback()

        # Deliberately bubbling this error up to the stack - but need to make
        # sure it is handled in the standard error log messages as well.
        logger.exception(pe)
        raise
    finally:
        session.close()


def execute_statements(engine: sa_Engine, statements: List[str]) -> None:
    def __callback(session: sa_Session) -> None:
        for statement in statements:
            # Ignore MSSQL "GO" statements
            if statement == "GO":
                continue

            # Deliberately throwing away all results. Counting on exception handling
            # if there are any errors, and migration scripts should not be returning
            # any results.
            session.execute(statement)

    execute_transaction(engine, __callback)


def get_int(engine: sa_Engine, statement: str) -> int:
    def __callback(session: sa_Session) -> int:
        return session.execute(statement).scalar()

    result: int = execute_transaction(engine, __callback)

    if result:
        return result
    else:
        return 0
