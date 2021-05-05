# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List, Set

import pandas as pd
from sqlalchemy.engine.result import ResultProxy as sa_Result
from sqlalchemy.engine import Engine as sa_Engine
from sqlalchemy.exc import ProgrammingError
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
        self._exec(f"TRUNCATE TABLE lms.stg_{table};")

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
            f"ALTER INDEX IX_stg_{table}_Natural_Key on lms.stg_{table} DISABLE;"
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
            f"ALTER INDEX IX_stg_{table}_Natural_Key on lms.stg_{table} REBUILD;"
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
            chunksize=120,
        )
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

        statement = f"""
INSERT INTO
    lms.{table}
({column_string}
)
SELECT{column_string}
FROM
    lms.stg_{table} as stg
WHERE
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.{table}
        WHERE
            SourceSystemIdentifier = stg.SourceSystemIdentifier
        AND
            SourceSystem = stg.SourceSystem
    )
"""

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

        statement = f"""
INSERT INTO
    lms.{table}
(
    LMSUserIdentifier,{insert_columns}
)
SELECT
    LMSUser.LMSUserIdentifier,{select_columns}
FROM
    lms.stg_{table} as stg
INNER JOIN
    lms.LMSUser
ON
    stg.LMSUserSourceSystemIdentifier = LMSUser.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSUser.SourceSystem
WHERE NOT EXISTS (
  SELECT
    1
  FROM
    lms.{table}
  WHERE
    SourceSystemIdentifier = stg.SourceSystemIdentifier
  AND
    SourceSystem = stg.SourceSystem
)
"""

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

        statement = f"""
INSERT INTO
    lms.{table}
(
    LMSSectionIdentifier,{insert_columns}
)
SELECT
    LMSSection.LMSSectionIdentifier,{select_columns}
FROM
    lms.stg_{table} as stg
INNER JOIN
    lms.LMSSection
ON
    stg.LMSSectionSourceSystemIdentifier = LMSSection.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSSection.SourceSystem
WHERE NOT EXISTS (
  SELECT
    1
  FROM
    lms.{table}
  WHERE
    SourceSystemIdentifier = stg.SourceSystemIdentifier
  AND
    SourceSystem = stg.SourceSystem
)
"""

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

        statement = f"""
INSERT INTO
    lms.{table}
(
    LMSSectionIdentifier,
    LMSUserIdentifier,{insert_columns}
)
SELECT
    LMSSection.LMSSectionIdentifier,
    LMSUser.LMSUserIdentifier,{select_columns}
FROM
    lms.stg_{table} as stg
INNER JOIN
    lms.LMSSection
ON
    stg.LMSSectionSourceSystemIdentifier = LMSSection.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSSection.SourceSystem
INNER JOIN
    lms.LMSUser
ON
    stg.LMSUserSourceSystemIdentifier = LMSUser.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSUser.SourceSystem
WHERE NOT EXISTS (
  SELECT
    1
  FROM
    lms.{table}
  WHERE
    SourceSystemIdentifier = stg.SourceSystemIdentifier
  AND
    SourceSystem = stg.SourceSystem
)
"""

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

        statement = f"""
INSERT INTO
    lms.{table}
(
    AssignmentIdentifier,
    LMSUserIdentifier,{insert_columns}
)
SELECT
    Assignment.AssignmentIdentifier,
    LMSUser.LMSUserIdentifier,{select_columns}
FROM
    lms.stg_{table} as stg
INNER JOIN
    lms.Assignment
ON
    stg.AssignmentSourceSystemIdentifier = Assignment.SourceSystemIdentifier
AND
    stg.SourceSystem = Assignment.SourceSystem
INNER JOIN
    lms.LMSUser
ON
    stg.LMSUserSourceSystemIdentifier = LMSUser.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSUser.SourceSystem
WHERE NOT EXISTS (
  SELECT
    1
  FROM
    lms.{table}
  WHERE
    SourceSystemIdentifier = stg.SourceSystemIdentifier
  AND
    SourceSystem = stg.SourceSystem
)
"""

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

        statement = f"""
INSERT INTO
    lms.LMSUserAttendanceEvent
(
    LMSSectionIdentifier,
    LMSUserIdentifier,
    LMSUserLMSSectionAssociationIdentifier,{insert_columns}
)
SELECT
    LMSSection.LMSSectionIdentifier,
    LMSUser.LMSUserIdentifier,
    LMSUserLMSSectionAssociation.LMSUserLMSSectionAssociationIdentifier,{select_columns}
FROM
    lms.stg_LMSUserAttendanceEvent as stg
INNER JOIN
    lms.LMSSection
ON
    stg.LMSSectionSourceSystemIdentifier = LMSSection.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSSection.SourceSystem
INNER JOIN
    lms.LMSUser
ON
    stg.LMSUserSourceSystemIdentifier = LMSUser.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSUser.SourceSystem
INNER JOIN
    lms.LMSUserLMSSectionAssociation
ON
    LMSUser.LMSUserIdentifier = LMSUserLMSSectionAssociation.LMSUserIdentifier
AND
    LMSSection.LMSSectionIdentifier = LMSUserLMSSectionAssociation.LMSSectionIdentifier
WHERE NOT EXISTS (
  SELECT
    1
  FROM
    lms.LMSUserAttendanceEvent
  WHERE
    SourceSystemIdentifier = stg.SourceSystemIdentifier
  AND
    SourceSystem = stg.SourceSystem
)
"""

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

        statement = f"""
UPDATE
    t
SET{update_columns}
FROM
    lms.{table} as t
INNER JOIN
    lms.stg_{table} as stg
ON
    t.SourceSystem = stg.SourceSystem
AND
    t.SourceSystemIdentifier = stg.SourceSystemIdentifier
AND
    t.LastModifiedDate <> stg.LastModifiedDate
"""

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

        statement = f"""
UPDATE
    t
SET
    t.DeletedAt = getdate()
FROM
    lms.{table} as t
WHERE
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.stg_{table} as stg
        WHERE
            t.SourceSystemIdentifier = stg.SourceSystemIdentifier
        AND
            t.SourceSystem = stg.SourceSystem
    )
AND
    t.DeletedAt IS NULL
AND
    t.SourceSystem = '{source_system}'
"""

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

        statement = f"""
UPDATE
    t
SET
    t.DeletedAt = getdate()
FROM
    lms.{table} as t
WHERE
    t.LMSSectionIdentifier IN (
        SELECT
            s.LMSSectionIdentifier
        FROM
           lms.LMSSection as s
        INNER JOIN
            lms.stg_{table} as stg
        ON
            stg.LMSSectionSourceSystemIdentifier = s.SourceSystemIdentifier
        AND
            stg.SourceSystem = s.SourceSystem
    )
AND
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.stg_{table} as stg
        WHERE
            t.SourceSystemIdentifier = stg.SourceSystemIdentifier
        AND
            t.SourceSystem = stg.SourceSystem
    )
AND
    t.DeletedAt IS NULL
AND
    t.SourceSystem = '{source_system}'
"""

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

        statement = f"""
UPDATE
    t
SET
    t.DeletedAt = getdate()
FROM
    lms.{table} as t
WHERE
    t.AssignmentIdentifier IN (
        SELECT
            a.AssignmentIdentifier
        FROM
           lms.Assignment as a
        INNER JOIN
            lms.stg_{table} as stg
        ON
            stg.AssignmentSourceSystemIdentifier = a.SourceSystemIdentifier
        AND
            stg.SourceSystem = a.SourceSystem
    )
AND
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.stg_{table} as stg
        WHERE
            t.SourceSystemIdentifier = stg.SourceSystemIdentifier
        AND
            t.SourceSystem = stg.SourceSystem
    )
AND
    t.DeletedAt IS NULL
AND
    t.SourceSystem = '{source_system}'
"""

        row_count = self._exec(statement)
        logger.debug(f"Soft-deleted {row_count} records in table `{table}`")

    def insert_new_submission_types(self) -> None:
        """
        Inserts new Assignment Submission Type records from staging table
        into the production table.
        """

        statement = """
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

        statement = f"""
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
    SourceSystem = '{source_system}'
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

        statement = f"""
UPDATE
    AssignmentSubmissionType
SET
    DeletedAt = NULL
FROM
    lms.AssignmentSubmissionType
INNER JOIN
    lms.Assignment
ON
    AssignmentSubmissionType.AssignmentIdentifier = Assignment.AssignmentIdentifier
WHERE
    SourceSystem = '{source_system}'
AND
    EXISTS (
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
        row_count = self._exec(statement)
        logger.debug(
            f"Un-soft deleted {row_count} records in table `{Table.ASSIGNMENT_SUBMISSION_TYPES}`."
        )

    def get_processed_files(self, resource_name: str) -> Set[str]:
        try:
            query = f"""
SELECT
    FullPath
FROM
    lms.ProcessedFiles
WHERE
    ResourceName = '{resource_name}'
""".strip()
            result = pd.read_sql_query(query, self.engine)
            if "FullPath" in result:
                return set(result["FullPath"])
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

        statement = f"""
INSERT INTO
    lms.ProcessedFiles
(
    FullPath,
    ResourceName,
    NumberOfRows
)
VALUES
(
    '{path}',
    '{resource_name}',
    {rows}
)
""".strip()

        try:
            _ = self._exec(statement)
        except ProgrammingError as pe:
            logger.exception(pe)
            raise
