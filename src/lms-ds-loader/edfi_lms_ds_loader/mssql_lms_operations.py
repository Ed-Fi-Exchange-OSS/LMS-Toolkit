# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
import logging

import pandas as pd
import sqlalchemy as sal
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

@dataclass
class MssqlLmsOperations:
    """
    An adapter providing Microsoft SQL Server operations for management and use
    of LMS staging and production tables.

    Parameters
    ----------
    connection_string: str
        Fully-formatted database connection string
    """

    connection_string: str

    def __post_init__(self):
        self.engine = None

    def _get_sql_engine(self):
        """This is a wrapper function that will not be unit tested."""

        assert (
            type(self.connection_string) is str
        ), "Variable `connection_string` must be a string"
        assert (
            self.connection_string.strip() != ""
        ), "Variable `connection_string` cannot be whitespace"

        if not self.engine:
            self.engine = sal.create_engine(self.connection_string)

        return self.engine

    def _exec(self, statement) -> int:
        """This is a wrapper function that will not be unit tested."""

        assert isinstance(statement, str), "Argument `statement` must be a string"
        assert statement.strip() != "", "Argument `statement` cannot be whitespace"

        Session = sessionmaker(bind=self._get_sql_engine())
        session = Session()
        result = session.execute(statement)
        session.commit()
        session.close()

        return result.rowcount

    def truncate_staging_table(self, table):
        """
        Executes a truncate command on the staging version of a table.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        """

        assert isinstance(table, str), "Argument `table` must be a string"
        assert table.strip() != "", "Argument `table` cannot be whitespace"

        # TODO: for postgresql we'll want `TRUNCATE TABLE {staging} RESTART IDENTITY`
        self._exec(f"truncate table lms.[stg_{table}];")

    def disable_staging_natural_key_index(self, table):
        """
        Disables the natural key index on the staging table, for optimizing
        inserts.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        """

        assert isinstance(table, str), "Argument `table` must be a string"
        assert table.strip() != "", "Argument `table` cannot be whitespace"

        self._exec(
            f"alter index [ix_stg_{table}_natural_key] on lms.[stg_{table}] disable;"
        )

    def enable_staging_natural_key_index(self, table):
        """
        Re-builds the natural key index on the staging table.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        """

        assert isinstance(table, str), "Argument `table` must be a string"
        assert table.strip() != "", "Argument `table` cannot be whitespace"

        self._exec(
            f"alter index [ix_stg_{table}_natural_key] on lms.[stg_{table}] rebuild;"
        )

    def insert_into_staging(self, df, table):
        """
        Inserts all records from a DataFrame into the staging table.

        Parameters
        ----------
        df: DataFrame
            A Pandas dataframe with column names that match the destination table
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        """

        assert isinstance(df, pd.DataFrame), "Argument `df` must be a DataFrame"
        assert isinstance(table, str), "Argument `table` must be a string"
        assert table.strip() != "", "Argument `table` cannot be whitespace"

        df.to_sql(
            f"stg_{table}",
            self._get_sql_engine(),
            schema="lms",
            if_exists="append",
            index=False,
            method="multi",
            # The ODBC driver complains and exits with chunksize > 190
            chunksize=190
        )
        logger.debug(f"All records have been loading into staging table 'stg_{table}'")


    def insert_new_records_to_production(self, table, columns):
        """
        Copies new records from the staging table to the production table.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        columns: List[str]
            A list of the column names in the table
        """

        assert isinstance(table, str), "Argument `table` must be a string"
        assert table.strip() != "", "Argument `table` cannot be whitespace"
        assert columns is not None, "Argument `columns` cannot be None"
        assert isinstance(columns, list), "Argument `columns` must be a list"
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

        rowcount = self._exec(statement)
        logger.debug(f"Inserted {rowcount} records into table `{table}`.")

    def copy_updates_to_production(self, table, columns):
        """
        Updates modified records in production based on the staging table, based
        on the LastModifiedDate.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        columns: List[str]
            A list of the column names in the table
        """

        assert isinstance(table, str), "Argument `table` must be a string"
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

        rowcount = self._exec(statement)
        logger.debug(f"Updated {rowcount} records in table `{table}`.")

    def soft_delete_from_production(self, table: str, sourceSystem: str):
        """
        Updates production records that do not have a match in the staging table
        by setting their `deletedat` value to the current timestamp.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_`.
        sourceSystem: str
            The SourceSystem currently being processed.
        """

        statement = f"""
update t set t.deletedat = getdate()
from lms.[{table}] as t
where not exists (
select 1 from lms.stg_{table} as stg
where t.sourcesystemidentifier = stg.sourcesystemidentifier
and t.sourcesystem = stg.sourcesystem
) and deletedat is null
and t.sourceSystem = '{sourceSystem}'
""".strip()

        rowcount = self._exec(statement)
        logger.debug(f"Soft-deleted {rowcount} records in table `{table}`")
