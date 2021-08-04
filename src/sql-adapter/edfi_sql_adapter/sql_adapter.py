# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

# Developer note: this adapter module is deliberately not unit tested.

from collections import namedtuple
import logging
from typing import Any, Callable, List, TypeVar

from sqlalchemy.engine.base import Engine as sa_Engine
from sqlalchemy import create_engine as sa_create_engine
from sqlalchemy.orm import sessionmaker, Session as sa_Session
from sqlalchemy.exc import ProgrammingError


logger = logging.getLogger(__name__)

T = TypeVar("T")
Statement = namedtuple("Statement", "sql, info_msg")


class Adapter:
    """
    This simple Adapter class supports basic decoupling of client code from SQL
    Alchemy, providing a set of common utility functions for interacting with a
    database.
    """

    engine: sa_Engine

    def __init__(self, engine: sa_Engine) -> None:
        """
        Class initializer.

        Parameters
        ----------
        engine: sqlalchemy.engine.base.Engine
            A SQL Alchemy engine.
        """
        self.engine = engine

    def execute_transaction(self, function: Callable[[sa_Session], T]) -> T:
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

        Session = sessionmaker(bind=self.engine)

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

    def execute_script(self, statements: List[str]) -> None:
        """
        Executes a series of SQL statements from a script, supplied in a list,
        in the natural order of the list.

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

        self.execute_transaction(__callback)

    def execute(self, statements: List[Statement]) -> None:
        """
        Executes a series of discrete statements, each with an accompanying
        message for logging.

        Parameters
        ----------
        statements: List[Statement]
            A list of Statements, where a Statement is a Named Tuple containing
            both the SQL statement and an informational message for logging.
        """
        with self.engine.connect().execution_options(autocommit=True) as connection:
            for s in statements:
                logger.info(s.info_msg)
                connection.execute(s.sql)

    def get_int(self, statement: str) -> int:
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

        result: int = self.execute_transaction(__callback)

        if result:
            return result
        else:
            return 0


# Below is a set of "static" functions for generating a new Adapter object


def create_mssql_adapter(
    username: str,
    password: str,
    server: str,
    db_name: str,
    port: int = 1433,
    encrypt: bool = False,
    trust_certificates: bool = False,
) -> Adapter:
    """
    Creates a SQL Alchemy database engine for Microsoft SQL Server, using SQL
    credentials.

    Parameters
    ----------
    username: str
        Database username.
    password: str
        Database password.
    server: str
        Database server name or IP Address.
    db_name: str
        Database name.
    port: int
        SQL Server's TCP port. Defaults to 1433.
    encrypt: bool
        Encrypt database connections. Defaults to false.
    trust_certificates: bool
        When encrypting the database connection, trust the server certificate.
        Helpful for localhost development. USE WITH CAUTION.

    Returns
    -------
    An instance of Adapter
    """

    url = f"mssql+pyodbc://{username}:{password}@{server},{port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"

    if encrypt:
        url += "&Encrypt=yes"

        if trust_certificates:
            url += "&TrustServerCertificate=yes"

    return Adapter(sa_create_engine(url))


def create_mssql_adapter_with_integrated_security(
    server: str,
    db_name: str,
    port: int = 1433,
    encrypt: bool = False,
    trust_certificates: bool = False,
) -> Adapter:
    """
    Creates a SQL Alchemy database engine for Microsoft SQL Server, using
    integrated security (aka SSPI, aka Windows domain authentication).

    Parameters
    ----------
    server: str
        Database server name or IP Address.
    db_name: str
        Database name.
    port: int
        SQL Server's TCP port. Defaults to 1433.
    encrypt: bool
        Encrypt database connections. Defaults to false.
    trust_certificates: bool
        When encrypting the database connection, trust the server certificate.
        Helpful for localhost development. USE WITH CAUTION.

    Returns
    -------
    An instance of Adapter
    """

    url = (
        f"mssql+pyodbc://{server},{port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"
    )

    if encrypt:
        url += "&Encrypt=yes"

        if trust_certificates:
            url += "&TrustServerCertificate=yes"

    return Adapter(sa_create_engine(url))


def create_postgresql_adapter(
    username: str, password: str, server: str, db_name: str, port: int = 5432
) -> Adapter:
    """
    Creates a SQL Alchemy database engine for PostgreSQL, using database credentials.

    Parameters
    ----------
    username: str
        Database username.
    password: str
        Database password.
    server: str
        Database server name or IP Address.
    db_name: str
        Database name.
    port: int
        PostgreSQL's TCP port. Defaults to 5432

    Returns
    -------
    An instance of Adapter
    """
    return Adapter(
        sa_create_engine(
            f"postgresql://{username}:{password}@{server}:{port}/{db_name}"
        )
    )
