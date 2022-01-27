# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
# from os import path

from contextlib import contextmanager
from typing import Any, Dict, Iterator, List
import pyodbc
from tests_integration_pgsql.pgsql_server_config import PgsqlServerConfig


class PgsqlConnection(object):
    config: PgsqlServerConfig

    def __init__(self, config: PgsqlServerConfig):
        self.config = config

    @contextmanager
    def pyodbc_conn(self) -> Iterator[pyodbc.Connection]:
        c = (
            f"Driver={{PostgreSQL ANSI}};Server={self.config.server};Port={self.config.port};"
            f"Database={self.config.db_name};Uid={self.config.username};Pwd={{{self.config.password}}};"
        )
        connection: pyodbc.Connection = pyodbc.connect(c)

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
