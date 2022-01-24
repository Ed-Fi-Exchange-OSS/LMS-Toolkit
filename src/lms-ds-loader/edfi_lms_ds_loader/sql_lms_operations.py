# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List, Set

import pandas as pd
from sqlalchemy.engine.result import ResultProxy as sa_Result
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session as sa_Session

from edfi_lms_ds_loader.helpers.constants import DbEngine, Table
from edfi_sql_adapter.sql_adapter import Adapter
from edfi_lms_ds_loader.db_operations import MSSQL_sql_builder as MS_builder
from edfi_lms_ds_loader.db_operations import PGSQL_sql_builder as PG_builder

logger = logging.getLogger(__name__)
SUPPORTED_ENGINES = [DbEngine.POSTGRESQL, DbEngine.MSSQL]


class SqlLmsOperations:
    """
    An adapter providing SQL operations for management and use
    of LMS staging and production tables.

    Parameters
    ----------
    sql_adapter: Adapter
        The adapter to be used.
    engine: sqlalchemy.engine.Engine
        SQL Alchemy engine.
    """

    db_adapter: Adapter
    engine: str

    def __init__(self, sql_adapter: Adapter, engine: str = DbEngine.MSSQL) -> None:
        self.db_adapter = sql_adapter
        self.engine = engine
        if self.engine not in SUPPORTED_ENGINES:
            logger.error(f"The engine {self.engine} is not supported.")

    def _exec(self, statement: str) -> int:
        """This is a wrapper function that will not be unit tested."""

        assert statement.strip() != "", "Argument `statement` cannot be whitespace"

        def __callback(session: sa_Session) -> sa_Result:
            result: sa_Result = session.execute(statement)
            return result

        result = self.db_adapter.execute_transaction(__callback)

        if result:
            return int(result.rowcount)

        return 0

    def truncate_staging_table(self, table: str) -> None:
        """
        Executes a truncate command on the staging version of a table.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        """

        assert table.strip() != "", "Argument `table` cannot be whitespace"

        if self.engine == DbEngine.MSSQL:
            self._exec(MS_builder.truncate_stg_table(table))

        if self.engine == DbEngine.POSTGRESQL:
            self._exec(PG_builder.truncate_stg_table(table))

    def disable_staging_natural_key_index(self, table: str) -> None:
        """
        Disables the natural key index on the staging table, for optimizing
        inserts.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        """

        assert table.strip() != "", "Argument `table` cannot be whitespace"

        if self.engine == DbEngine.MSSQL:
            self._exec(MS_builder.disable_staging_natural_key_index(table))

        if self.engine == DbEngine.POSTGRESQL:
            self._exec(PG_builder.drop_staging_natural_key_index(table))

    def enable_staging_natural_key_index(self, table: str) -> None:
        """
        Re-builds the natural key index on the staging table.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        """

        assert table.strip() != "", "Argument `table` cannot be whitespace"

        if self.engine == DbEngine.MSSQL:
            self._exec(MS_builder.enable_staging_natural_key_index(table))

        if self.engine == DbEngine.POSTGRESQL:
            self._exec(PG_builder.recreate_staging_natural_key_index(table))

    def insert_into_staging(self, df: pd.DataFrame, table: str) -> None:
        """
        Inserts all records from a DataFrame into the staging table.

        Parameters
        ----------
        df: DataFrame
            A Pandas dataframe with column names that match the destination table
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        """

        assert table.strip() != "", "Argument `table` cannot be whitespace"

        # PostgreSQL requires lower case column names, but our
        # code uses upper case. Temporarily convert, then restore
        proper_names = df.columns

        df.columns = proper_names.str.lower()
        df.to_sql(
            f"stg_{table}".lower(),
            self.db_adapter.engine,
            schema="lms",
            if_exists="append",
            index=False,
            method="multi",
            chunksize=120,
        )
        df.columns = proper_names
        logger.debug(f"All records have been loaded into staging table 'stg_{table}'")

    def insert_new_records_to_production(self, table: str, columns: List[str]) -> None:
        """
        Copies new records from the staging table to the production table.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        columns: List[str]
            A list of the column names in the table
        """

        assert table.strip() != "", "Argument `table` cannot be whitespace"
        assert len(columns) > 0, "Argument `columns` cannot be empty"

        column_string = ",".join([f"\n    {c}" for c in columns])

        statement = ""
        if self.engine == DbEngine.MSSQL:
            statement = MS_builder.insert_new_records_to_production(
                table, column_string
            )

        if self.engine == DbEngine.POSTGRESQL:
            statement = PG_builder.insert_new_records_to_production(
                table, column_string
            )

        row_count = self._exec(statement)
        logger.debug(f"Inserted {row_count} records into table `{table}`.")

    def insert_new_records_to_production_for_user_relation(
        self, table: str, columns: List[str]
    ) -> None:
        """
        Copies new records from the staging table to the production table. Specialized
        for tables that have a foreign key to LMSUser.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        columns: List[str]
            A list of the column names in the table
        """

        assert table.strip() != "", "Argument `table` cannot be whitespace"
        assert len(columns) > 0, "Argument `columns` cannot be empty"

        insert_columns = ",".join(
            [f"\n    {c}" for c in columns if c != "LMSUserSourceSystemIdentifier"]
        )
        select_columns = ",".join(
            [f"\n    stg.{c}" for c in columns if c != "LMSUserSourceSystemIdentifier"]
        )

        statement = ""
        if self.engine == DbEngine.MSSQL:
            statement = MS_builder.insert_new_records_to_production_for_user_relation(
                table, insert_columns, select_columns
            )

        if self.engine == DbEngine.POSTGRESQL:
            statement = PG_builder.insert_new_records_to_production_for_user_relation(
                table, insert_columns, select_columns
            )

        row_count = self._exec(statement)
        logger.debug(f"Inserted {row_count} records into table `{table}`.")

    def insert_new_records_to_production_for_section_relation(
        self, table: str, columns: List[str]
    ) -> None:
        """
        Copies new records from the staging table to the production table. Specialized
        for tables that have a foreign key to LMSSection.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        columns: List[str]
            A list of the column names in the table
        """

        assert table.strip() != "", "Argument `table` cannot be whitespace"
        assert len(columns) > 0, "Argument `columns` cannot be empty"

        insert_columns = ",".join(
            [f"\n    {c}" for c in columns if c != "LMSSectionSourceSystemIdentifier"]
        )
        select_columns = ",".join(
            [
                f"\n    stg.{c}"
                for c in columns
                if c != "LMSSectionSourceSystemIdentifier"
            ]
        )

        statement = ""
        if self.engine == DbEngine.MSSQL:
            statement = (
                MS_builder.insert_new_records_to_production_for_section_relation(
                    table, insert_columns, select_columns
                )
            )

        if self.engine == DbEngine.POSTGRESQL:
            statement = (
                PG_builder.insert_new_records_to_production_for_section_relation(
                    table, insert_columns, select_columns
                )
            )

        row_count = self._exec(statement)
        logger.debug(f"Inserted {row_count} records into table `{table}`.")

    def insert_new_records_to_production_for_section_and_user_relation(
        self, table: str, columns: List[str]
    ) -> None:
        """
        Copies new records from the staging table to the production table. Specialized
        for tables that have a foreign key to both LMSSection and LMSUser.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        columns: List[str]
            A list of the column names in the table
        """

        assert table.strip() != "", "Argument `table` cannot be whitespace"
        assert len(columns) > 0, "Argument `columns` cannot be empty"

        insert_columns = ",".join(
            [
                f"\n    {c}"
                for c in columns
                if not (
                    c == "LMSSectionSourceSystemIdentifier"
                    or c == "LMSUserSourceSystemIdentifier"
                )
            ]
        )
        select_columns = ",".join(
            [
                f"\n    stg.{c}"
                for c in columns
                if not (
                    c == "LMSSectionSourceSystemIdentifier"
                    or c == "LMSUserSourceSystemIdentifier"
                )
            ]
        )

        statement = ""
        if self.engine == DbEngine.MSSQL:
            statement = MS_builder.insert_new_records_to_production_for_section_and_user_relation(
                table, insert_columns, select_columns
            )

        if self.engine == DbEngine.POSTGRESQL:
            statement = PG_builder.insert_new_records_to_production_for_section_and_user_relation(
                table, insert_columns, select_columns
            )

        row_count = self._exec(statement)
        logger.debug(f"Inserted {row_count} records into table `{table}`.")

    def insert_new_records_to_production_for_assignment_and_user_relation(
        self, table: str, columns: List[str]
    ) -> None:
        """
        Copies new records from the staging table to the production table. Specialized
        for tables that have a foreign key to both Assignment and LMSUser.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        columns: List[str]
            A list of the column names in the table
        """

        assert table.strip() != "", "Argument `table` cannot be whitespace"
        assert len(columns) > 0, "Argument `columns` cannot be empty"

        insert_columns = ",".join(
            [
                f"\n    {c}"
                for c in columns
                if not (
                    c == "AssignmentSourceSystemIdentifier"
                    or c == "LMSUserSourceSystemIdentifier"
                )
            ]
        )
        select_columns = ",".join(
            [
                f"\n    stg.{c}"
                for c in columns
                if not (
                    c == "AssignmentSourceSystemIdentifier"
                    or c == "LMSUserSourceSystemIdentifier"
                )
            ]
        )

        statement = ""
        if self.engine == DbEngine.MSSQL:
            statement = MS_builder.insert_new_records_to_production_for_assignment_and_user_relation(
                table, insert_columns, select_columns
            )

        if self.engine == DbEngine.POSTGRESQL:
            statement = PG_builder.insert_new_records_to_production_for_assignment_and_user_relation(
                table, insert_columns, select_columns
            )

        row_count = self._exec(statement)
        logger.debug(f"Inserted {row_count} records into table `{table}`.")

    def insert_new_records_to_production_for_attendance_events(
        self, table: str, columns: List[str]
    ) -> None:
        """
        Copies new records from the staging table to the production table. Specialized
        for the Attendance Events table.

        Parameters
        ----------
        table: str
            Not strictly necessary, but must be part of the signature
        columns: List[str]
            A list of the column names in the table
        """
        assert table.strip() != "", "Argument `table` cannot be whitespace"
        assert len(columns) > 0, "Argument `columns` cannot be empty"

        def __not_a_foreign_key(column: str) -> bool:
            return column not in [
                "LMSSectionSourceSystemIdentifier",
                "LMSUserSourceSystemIdentifier",
            ]

        insert_columns = ",".join(
            [f"\n    {c}" for c in columns if __not_a_foreign_key(c)]
        )
        select_columns = ",".join(
            [f"\n    stg.{c}" for c in columns if __not_a_foreign_key(c)]
        )

        statement = ""
        if self.engine == DbEngine.MSSQL:
            statement = (
                MS_builder.insert_new_records_to_production_for_attendance_events(
                    insert_columns, select_columns
                )
            )

        if self.engine == DbEngine.POSTGRESQL:
            statement = (
                PG_builder.insert_new_records_to_production_for_attendance_events(
                    insert_columns, select_columns
                )
            )

        row_count = self._exec(statement)
        logger.debug(f"Inserted {row_count} records into table `{table}`.")

    def copy_updates_to_production(self, table: str, columns: List[str]) -> None:
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

        assert table.strip() != "", "Argument `table` cannot be whitespace"
        assert len(columns) > 0, "Argument `columns` cannot be empty"

        update_columns = (
            ",".join(
                [
                    f"\n    {c} = stg.{c}"
                    for c in columns
                    if c
                    not in (
                        # These are natural key columns that should never be
                        # updated.
                        "SourceSystem",
                        "SourceSystemIdentifier",
                        "LMSSectionSourceSystemIdentifier",
                        "LMSUserSourceSystemIdentifier",
                        "AssignmentSourceSystemIdentifier",
                    )
                ]
            )
            + ",\n    DeletedAt = NULL"
        )

        statement = ""
        if self.engine == DbEngine.MSSQL:
            statement = MS_builder.copy_updates_to_production(table, update_columns)

        if self.engine == DbEngine.POSTGRESQL:
            statement = PG_builder.copy_updates_to_production(table, update_columns)

        row_count = self._exec(statement)
        logger.debug(f"Updated {row_count} records in table `{table}`.")

    def soft_delete_from_production(self, table: str, source_system: str) -> None:
        """
        Updates production records that do not have a match in the staging table
        by setting their `deletedat` value to the current timestamp.

        Parameters
        ----------
        table: str
            Name of the table to soft delete on, not including the `stg_`.
        source_system: str
            The SourceSystem currently being processed.
        """

        assert table.strip() != "", "Argument `table` cannot be whitespace"

        statement = ""
        if self.engine == DbEngine.MSSQL:
            statement = MS_builder.soft_delete_from_production(table, source_system)

        if self.engine == DbEngine.POSTGRESQL:
            statement = PG_builder.soft_delete_from_production(table, source_system)

        row_count = self._exec(statement)
        logger.debug(f"Soft-deleted {row_count} records in table `{table}`")

    def soft_delete_from_production_for_section_relation(
        self, table: str, source_system: str
    ) -> None:
        """
        Updates production records that do not have a match in the staging table
        by setting their `deletedat` value to the current timestamp, but
        only for the related sections in the staging table.

        Parameters
        ----------
        table: str
            Name of the table to soft delete on, not including the `stg_`.
        source_system: str
            The SourceSystem currently being processed.
        """

        assert table.strip() != "", "Argument `table` cannot be whitespace"

        statement = ""
        if self.engine == DbEngine.MSSQL:
            statement = MS_builder.soft_delete_from_production_for_section_relation(
                table, source_system
            )

        if self.engine == DbEngine.POSTGRESQL:
            statement = PG_builder.soft_delete_from_production_for_section_relation(
                table, source_system
            )

        row_count = self._exec(statement)
        logger.debug(f"Soft-deleted {row_count} records in table `{table}`")

    def soft_delete_from_production_for_assignment_relation(
        self, table: str, source_system: str
    ) -> None:
        """
        Updates production records that do not have a match in the staging table
        by setting their `deletedat` value to the current timestamp, but
        only for the related assignments in the staging table.

        Parameters
        ----------
        table: str
            Name of the table to soft delete on, not including the `stg_`.
        source_system: str
            The SourceSystem currently being processed.
        """

        assert table.strip() != "", "Argument `table` cannot be whitespace"

        statement = ""
        if self.engine == DbEngine.MSSQL:
            statement = MS_builder.soft_delete_from_production_for_assignment_relation(
                table, source_system
            )

        if self.engine == DbEngine.POSTGRESQL:
            statement = PG_builder.soft_delete_from_production_for_assignment_relation(
                table, source_system
            )

        row_count = self._exec(statement)
        logger.debug(f"Soft-deleted {row_count} records in table `{table}`")

    def insert_new_submission_types(self) -> None:
        """
        Inserts new Assignment Submission Type records from staging table
        into the production table.
        """

        statement = ""
        if self.engine == DbEngine.MSSQL:
            statement = MS_builder.insert_new_submission_types()

        if self.engine == DbEngine.POSTGRESQL:
            statement = PG_builder.insert_new_submission_types()

        row_count = self._exec(statement)
        logger.debug(
            f"Updated {row_count} records in table `{Table.ASSIGNMENT_SUBMISSION_TYPES}`."
        )

    def soft_delete_removed_submission_types(self, source_system: str) -> None:
        """
        Marks existing Assignment Submission Types as "deleted" when they are
        no longer present in the incoming data.

        Parameters
        ----------
        source_system: str
            The name of the source system for the current import process.
        """

        statement = ""
        if self.engine == DbEngine.MSSQL:
            statement = MS_builder.soft_delete_removed_submission_types(source_system)

        if self.engine == DbEngine.POSTGRESQL:
            statement = PG_builder.soft_delete_removed_submission_types(source_system)

        row_count = self._exec(statement)
        logger.debug(
            f"Soft deleted {row_count} records in table `{Table.ASSIGNMENT_SUBMISSION_TYPES}`."
        )

    def unsoft_delete_returned_submission_types(self, source_system: str) -> None:
        """
        Unmarks previously "deleted" Assignment Submission Types when they are
        present in the incoming data.

        Parameters
        ----------
        source_system: str
            The name of the source system for the current import process.
        """

        statement = ""
        if self.engine == DbEngine.MSSQL:
            statement = MS_builder.unsoft_delete_returned_submission_types(
                source_system
            )

        if self.engine == DbEngine.POSTGRESQL:
            statement = PG_builder.unsoft_delete_returned_submission_types(
                source_system
            )

        row_count = self._exec(statement)
        logger.debug(
            f"Un-soft deleted {row_count} records in table `{Table.ASSIGNMENT_SUBMISSION_TYPES}`."
        )

    def get_processed_files(self, resource_name: str) -> Set[str]:
        try:
            query = ""
            if self.engine == DbEngine.MSSQL:
                query = MS_builder.get_processed_files(resource_name)

            if self.engine == DbEngine.POSTGRESQL:
                query = PG_builder.get_processed_files(resource_name)

            query = query.strip()
            result = pd.read_sql_query(query, self.db_adapter.engine)

            result.columns = result.columns.str.lower()

            if "fullpath" in result:
                return set(result["fullpath"])

            return set()
        except ProgrammingError as pe:
            logger.exception(pe)
            raise

    def add_processed_file(self, path: str, resource_name: str, rows: int):
        """
        Records that a file has been processed and thus should not be processed
        a second time.

        Parameters
        ----------
        path: str
            Filesystem path for the file that was processed.
        resource_name: str
            Name of the resource covered by the file.
        rows: int
            Number of rows in the file.
        """
        statement = ""
        if self.engine == DbEngine.MSSQL:
            statement = MS_builder.add_processed_file(path, resource_name, rows)

        if self.engine == DbEngine.POSTGRESQL:
            statement = PG_builder.add_processed_file(path, resource_name, rows)

        statement = statement.strip()

        try:
            _ = self._exec(statement)
        except ProgrammingError as pe:
            logger.exception(pe)
            raise
