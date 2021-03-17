# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List

import pandas as pd
from sqlalchemy.engine.result import ResultProxy as sa_Result
from sqlalchemy.engine import Engine as sa_Engine
from sqlalchemy.orm import Session as sa_Session

from edfi_lms_ds_loader.helpers.constants import Table
from edfi_lms_ds_loader.sql_adapter import execute_transaction

logger = logging.getLogger(__name__)


class MssqlLmsOperations:
    """
    An adapter providing Microsoft SQL Server operations for management and use
    of LMS staging and production tables.

    Parameters
    ----------
    engine: sqlalchemy.engine.Engine
        SQL Alchemy engine.
    """

    engine: sa_Engine

    def __init__(self, engine: sa_Engine) -> None:
        self.engine = engine

    def _exec(self, statement: str) -> int:
        """This is a wrapper function that will not be unit tested."""

        assert statement.strip() != "", "Argument `statement` cannot be whitespace"

        def __callback(session: sa_Session) -> sa_Result:
            result: sa_Result = session.execute(statement)
            return result

        result = execute_transaction(self.engine, __callback)

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

        # Note: for postgresql we'll want `TRUNCATE TABLE {staging} RESTART IDENTITY`
        self._exec(f"truncate table lms.[stg_{table}];")

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

        self._exec(
            f"alter index [ix_stg_{table}_natural_key] on lms.[stg_{table}] disable;"
        )

    def enable_staging_natural_key_index(self, table: str) -> None:
        """
        Re-builds the natural key index on the staging table.

        Parameters
        ----------
        table: str
            Name of the table to truncate, not including the `stg_` prefix
        """

        assert table.strip() != "", "Argument `table` cannot be whitespace"

        self._exec(
            f"alter index [ix_stg_{table}_natural_key] on lms.[stg_{table}] rebuild;"
        )

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

        df.to_sql(
            f"stg_{table}",
            self.engine,
            schema="lms",
            if_exists="append",
            index=False,
            method="multi",
            # The ODBC driver complains and exits with chunksize > 190
            chunksize=190,
        )
        logger.debug(f"All records have been loading into staging table 'stg_{table}'")

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

        column_string = ", ".join([f"t.[{c}] = stg.[{c}]" for c in columns])

        statement = f"""
update t set {column_string}
from lms.[{table}] as t
inner join lms.stg_{table} as stg
on t.sourcesystem = stg.sourcesystem
and t.sourcesystemidentifier = stg.sourcesystemidentifier
and t.lastmodifieddate <> stg.lastmodifieddate
""".strip()

        row_count = self._exec(statement)
        logger.debug(f"Updated {row_count} records in table `{table}`.")

    def soft_delete_from_production(self, table: str, sourceSystem: str) -> None:
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

        assert table.strip() != "", "Argument `table` cannot be whitespace"

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

        row_count = self._exec(statement)
        logger.debug(f"Soft-deleted {row_count} records in table `{table}`")

    INSERT_SUBMISSION_TYPES = """
INSERT INTO lms.AssignmentSubmissionType (
    AssignmentIdentifier,
    SubmissionType
)
SELECT
    Assignment.AssignmentIdentifier,
    stg_AssignmentSubmissionType.SubmissionType
FROM
        lms.stg_AssignmentSubmissionType
    INNER JOIN
        lms.Assignment
    ON
        stg_AssignmentSubmissionType.SourceSystem = Assignment.SourceSystem
    AND
        stg_AssignmentSubmissionType.SourceSystemIdentifier = Assignment.SourceSystemIdentifier
WHERE
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.AssignmentSubmissionType
        WHERE
            AssignmentIdentifier = Assignment.AssignmentIdentifier
        AND
            SubmissionType = stg_AssignmentSubmissionType.SubmissionType
    )
"""

    def insert_new_submission_types(self) -> None:
        """
        Inserts new Assignment Submission Type records from staging table
        into the production table.
        """
        row_count = self._exec(MssqlLmsOperations.INSERT_SUBMISSION_TYPES)
        logger.debug(f"Updated {row_count} records in table `{Table.ASSIGNMENT_SUBMISSION_TYPES}`.")

    SOFT_DELETE_SUBMISSION_TYPES = """
UPDATE
    AssignmentSubmissionType
SET
    DeletedAt = GETDATE()
FROM
    lms.AssignmentSubmissionType
INNER JOIN
    lms.Assignment
ON
    AssignmentSubmissionType.AssignmentIdentifier = Assignment.AssignmentIdentifier
WHERE
    AssignmentSubmissionType.DeletedAt IS NULL
AND
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.stg_AssignmentSubmissionType
        WHERE
            stg_AssignmentSubmissionType.SourceSystem = Assignment.SourceSystem
        AND
            stg_AssignmentSubmissionType.SourceSystemIdentifier = Assignment.SourceSystemIdentifier
        AND
            stg_AssignmentSubmissionType.SubmissionType = AssignmentSubmissionType.SubmissionType
    )
"""

    def soft_delete_removed_submission_types(self) -> None:
        """
        Marks existing Assignment Submission Types as "deleted" when they are
        no longer present in the incoming data.
        """
        row_count = self._exec(MssqlLmsOperations.SOFT_DELETE_SUBMISSION_TYPES)
        logger.debug(f"Soft deleted {row_count} records in table `{Table.ASSIGNMENT_SUBMISSION_TYPES}`.")
