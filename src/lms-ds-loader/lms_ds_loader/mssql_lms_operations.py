# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass

import sqlalchemy as sal


@dataclass
class MssqlLmsOperations:
    connection_string: str

    def __post_init__(self):
        self.engine = None

    def _get_sql_engine(self):
        assert self.connection_string is not None, "Variable `connection_string` cannot be None"
        assert self.connection_string.strip() != "", "Variable `connection_string` cannot be whitespace"

        if not self.engine:
            self.engine = sal.create_engine(self.connection_string)

        return self.engine

    def _exec(self, statement):
        """This is a wrapper function that will not be unit tested."""

        assert statement is not None, "Argument `statement` cannot be None"
        assert statement.strip() != "", "Argument `statement` cannot be whitespace"

        with self._get_sql_engine().connect() as connection:
            connection.execute(statement)

    def truncate_staging_table(self, table):
        assert table is not None, "Argument `table` cannot be None"
        assert table.strip() != "", "Argument `table` cannot be whitespace"

        # TODO: for postgresql we'll want `TRUNCATE TABLE {staging} RESTART IDENTITY`
        self._exec(f"truncate table lms.[stg_{table}];")

    def disable_staging_natural_key_index(self, table):
        assert table is not None, "Argument `table` cannot be None"
        assert table.strip() != "", "Argument `table` cannot be whitespace"

        self._exec(f"alter index [ix_stg_{table}_natural_key] on lms.[stg_{table}] disable;")

    def enable_staging_natural_key_index(self, table):
        assert table is not None, "Argument `table` cannot be None"
        assert table.strip() != "", "Argument `table` cannot be whitespace"

        self._exec(f"alter index [ix_stg_{table}_natural_key] on lms.[stg_{table}] rebuild;")

    def insert_into_staging(self, df, table):
        df.to_sql(
            f"stg_{table}",
            self._get_sql_engine(),
            schema="lms",
            if_exists="append",
            index=False,
            method="multi",
        )

    def insert_new_records_to_production(self, table, columns):
        assert table is not None, "Argument `table` cannot be None"
        assert table.strip() != "", "Argument `table` cannot be whitespace"
        assert columns is not None, "Argument `columns` cannot be None"
        assert isinstance(columns, list), "Argument `columns` must be a list"
        assert len(columns) > 0, "Argument `columns` cannot be empty"

        column_string = ", ".join([f"[{c}]" for c in columns])

        statement = [f"insert into lms.[{table}] ("]
        statement += [f"{column_string} ) select {column_string}"]
        statement += [f"from lms.stg_{table} as stg where not exists ("]
        statement += [f"select 1 from lms.[{table}]"]
        statement += ["where sourcesystemidentifier = stg.sourcesystemidentifier"]
        statement += ["and sourcesystem = stg.sourcesystem)"]

        self._exec(" ".join(statement))

    def copy_updates_to_production(self, table, columns):
        pass

    def soft_delete_from_production(self, table):
        pass

