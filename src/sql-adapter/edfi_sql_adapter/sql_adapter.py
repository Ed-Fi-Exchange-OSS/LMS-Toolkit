# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

# Developer note: this adapter module is deliberately not unit tested.

import logging
from typing import Any, Callable, List, TypeVar

from sqlalchemy.engine.base import Engine as sa_Engine
from sqlalchemy import create_engine as sa_create_engine
from sqlalchemy.orm import sessionmaker, Session as sa_Session
from sqlalchemy.exc import ProgrammingError


logger = logging.getLogger(__name__)

T = TypeVar("T")


def create_mssql_engine(
    username: str, password: str, server: str, port: int, db_name: str
) -> sa_Engine:
    """
    Creates a SQL Alchemy database engine for Microsoft SQL Server, using SQL
    credentials.
    """
    return sa_create_engine(
        f"mssql+pyodbc://{username}:{password}@{server},{port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"
    )


def create_mssql_engine_with_integrated_security(
    server: str, port: int, db_name: str
) -> sa_Engine:
    """
    Creates a SQL Alchemy database engine for Microsoft SQL Server, using
    integrated security (aka SSPI, aka Windows domain authentication).
    """
    return sa_create_engine(
        f"mssql+pyodbc://{server},{port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server?Trusted_Connection=yes"
    )


def create_postgresql_engine(
    username: str, password: str, server: str, port: int, db_name: str
) -> sa_Engine:
    """
    Creates a SQL Alchemy database engine for PostgreSQL, using database credentials.
    """
    return sa_create_engine(
        f"postgresql://{username}:{password}@{server}:{port}/{db_name}"
    )


def execute_transaction(engine: sa_Engine, function: Callable[[sa_Session], T]) -> T:
    """
    Runs the callback function, which presumably contains SQL statements, in a
    full database transaction, with rollback if an error occurs.

    Parameters
    ----------
    engine: sqlalchemy.engine.base.Engine
        An instance of a SQLAlchemy database engine.
    function: Callable[[sqlalchemy.orm.Session]]
        A function callback that returns accepts instance of sqlalchemy.orm.Session,
        and returns a generic value.

    Returns
    -------
    The (generic) object returned by the callback.
    """

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
    """
    Executes a series of SQL statements supplied in a list, in the natural
    order of the list.

    Parameters
    ----------
    engine: sqlalchemy.engine.base.Engine
        An instance of a SQLAlchemy database engine.
    statements: List[str]
        A collection of SQL statements to run, in order.
    """

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
    """
    Execute a query to get an integer result count.

    Parameters
    ----------
    engine: sqlalchemy.engine.base.Engine
        An instance of a SQLAlchemy database engine.
    statement: str
        The SQL query statement.

    Returns:
    --------
    Integer result count.
    """

    def __callback(session: sa_Session) -> int:
        return session.execute(statement).scalar()

    result: int = execute_transaction(engine, __callback)

    if result:
        return result
    else:
        return 0
