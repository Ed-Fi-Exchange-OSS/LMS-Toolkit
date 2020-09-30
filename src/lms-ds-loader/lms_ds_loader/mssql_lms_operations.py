# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass

import pandas as pd
import sqlalchemy as sal


@dataclass
class MssqlLmsOperations:
    connection_string: str

    def __post_init__(self):
        self.engine = None

    def _get_sql_engine(self):
        assert (
            type(self.connection_string) is str
        ), "Variable `connection_string` must ba string"
        assert (
            self.connection_string.strip() != ""
        ), "Variable `connection_string` cannot be whitespace"

        if not self.engine:
            self.engine = sal.create_engine(self.connection_string)

        return self.engine

    def _exec(self, statement):
        """This is a wrapper function that will not be unit tested."""

        assert type(statement) is str, "Argument `statement` must be a string"
        assert statement.strip() != "", "Argument `statement` cannot be whitespace"

        with self._get_sql_engine().connect() as connection:
            connection.execute(statement)

    def truncate_staging_table(self, table):
        assert type(table) is str, "Argument `table` must be a string"
        assert table.strip() != "", "Argument `table` cannot be whitespace"

        # TODO: for postgresql we'll want `TRUNCATE TABLE {staging} RESTART IDENTITY`
        self._exec(f"truncate table lms.[stg_{table}];")

    def disable_staging_natural_key_index(self, table):
        assert type(table) is str, "Argument `table` must be a string"
        assert table.strip() != "", "Argument `table` cannot be whitespace"

        self._exec(
            f"alter index [ix_stg_{table}_natural_key] on lms.[stg_{table}] disable;"
        )

    def enable_staging_natural_key_index(self, table):
        assert type(table) is str, "Argument `table` must be a string"
        assert table.strip() != "", "Argument `table` cannot be whitespace"

        self._exec(
            f"alter index [ix_stg_{table}_natural_key] on lms.[stg_{table}] rebuild;"
        )

    def insert_into_staging(self, df, table):
        assert isinstance(df, pd.DataFrame), "Argument `df` must be a DataFrame"
        assert type(table) is str, "Argument `table` must be a string"
        assert table.strip() != "", "Argument `table` cannot be whitespace"

        df.to_sql(
            f"stg_{table}",
            self._get_sql_engine(),
            schema="lms",
            if_exists="append",
            index=False,
            method="multi",
        )

    def insert_new_records_to_production(self, table, columns):
        assert type(table) is str, "Argument `table` must be a string"
        assert table.strip() != "", "Argument `table` cannot be whitespace"
        assert columns is not None, "Argument `columns` cannot be None"
        assert type(columns) is list, "Argument `columns` must be a list"
        assert len(columns) > 0, "Argument `columns` cannot be empty"

        column_string = ", ".join([f"[{c}]" for c in columns])

        statement = f"""
insert into lms.[{table}] ( {column_string} )
select {column_string}
from lms.stg_{table} as stg
where not exists (
  select 1 from lms.[{table}]
  where sourcesystemidentifier = stg.sourcesystemidentifier
  and sourcesystem = stg.sourcesystem
)
""".strip()

        self._exec(statement)

    def copy_updates_to_production(self, table, columns):
        assert type(table) is str, "Argument `table` must be a string"
        assert table.strip() != "", "Argument `table` cannot be whitespace"
        assert (
            type(columns) is list
        ), f"Argument `columns` must be a list, not a {type(columns)}"
        assert len(columns) > 0, "Argument `columns` cannot be empty"

        column_string = ", ".join([f"t.[{c}] = stg.[{c}]" for c in columns])

        statement = f"""
update t set {column_string}
from lms.[{table}] as t
inner join lms.stg_{table} as stg
on t.sourcesystem = stg.sourcesystem
and t.sourcesystemidentifier = stg.sourcesystemidentifier
and t.lastmodifieddate <> stg.lastmodifieddate
""".strip()

        self._exec(statement)

    def soft_delete_from_production(self, table):
        pass
