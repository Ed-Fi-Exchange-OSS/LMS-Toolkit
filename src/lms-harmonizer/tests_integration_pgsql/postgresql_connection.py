# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
# from os import path

from contextlib import contextmanager
from typing import Any, Dict, Iterator, List
import pyodbc
from tests_integration_pgsql.server_config import ServerConfig


class PostgresqlConnection(object):
    config: ServerConfig

    def __init__(self, config: ServerConfig):
        self.config = config

    @contextmanager
    def pyodbc_conn(self) -> Iterator[pyodbc.Connection]:

        # TODO: change to postgresql connection string
        connection: pyodbc.Connection = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.config.server},{self.config.port};DATABASE={self.config.db_name};UID={self.config.username};PWD={self.config.password};"
            )

        connection.autocommit = True

        yield connection

        connection.close()


class _RowAsDict:
    def __init__(self, cursor):
        self._cursor = cursor

    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()
        return {
            description[0]: row[col]
            for col, description in enumerate(self._cursor.description)
        }


def query(connection: pyodbc.Connection, query: str) -> List[Dict[str, Any]]:
    cursor = connection.cursor().execute(query)
    return list(_RowAsDict(cursor))
