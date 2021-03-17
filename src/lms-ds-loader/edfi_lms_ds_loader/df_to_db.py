# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging

import pandas as pd

from edfi_lms_ds_loader.helpers.constants import Table
from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations
from edfi_lms_ds_loader.helpers import assignment_splitter

logger = logging.getLogger(__name__)


def upload_file(db_adapter: MssqlLmsOperations, df: pd.DataFrame, table: str) -> None:
    """
    Uploads a DataFrame to the designated LMS table.

    Parameters
    ----------
    db_adapter: MssqlLmsOperations
        Database engine-specific adapter/wrapper for database operations.
    df: pd.DataFrame
        A DataFrame to upload.
    table: str
        The destination table.
    """

    logger.info(f"Uploading {table} file ...")

    db_adapter.disable_staging_natural_key_index(table)
    db_adapter.truncate_staging_table(table)
    db_adapter.insert_into_staging(df, table)

    columns = list(df.columns)

    db_adapter.insert_new_records_to_production(table, columns)
    db_adapter.copy_updates_to_production(table, columns)

    sourceSystem = df.iloc[0]["SourceSystem"]
    db_adapter.soft_delete_from_production(table, sourceSystem)

    db_adapter.enable_staging_natural_key_index(table)

    logger.info(f"Done with {table} file.")


def _upload_assignment_submission_types(
    db_adapter: MssqlLmsOperations, submission_types_df: pd.DataFrame
) -> None:
    table = Table.ASSIGNMENT_SUBMISSION_TYPES

    logger.info(f"Uploading {table} file ...")

    db_adapter.disable_staging_natural_key_index(table)
    db_adapter.truncate_staging_table(table)
    db_adapter.insert_into_staging(submission_types_df, table)

    db_adapter.insert_new_submission_types()

    sourceSystem = submission_types_df.iloc[0]["SourceSystem"]
    db_adapter.soft_delete_removed_submission_types(sourceSystem)

    db_adapter.enable_staging_natural_key_index(table)

    logger.info(f"Done with {table} file.")


def upload_assignments(
    db_adapter: MssqlLmsOperations, assignments_df: pd.DataFrame
) -> None:
    """
    Uploads an Assignments DataFrame to the Assignment and AssignmentSubmissionType
    tables. The specialized function is required in order to work with the
    collection table, AssignmentSubmissionType


    Parameters
    ----------
    db_adapter: MssqlLmsOperations
        Database engine-specific adapter/wrapper for database operations.
    df: pd.DataFrame
        A DataFrame to upload.
    """

    assignments_df, submissions_type_df = assignment_splitter.split(assignments_df)

    # Truncate AssignmentDescription to max 1024 characters, matching the database
    assignments_df["AssignmentDescription"] = assignments_df["AssignmentDescription"].str[:1024]  # type: ignore

    # Upload the Assignments without SubmissionType
    upload_file(db_adapter, assignments_df, Table.ASSIGNMENT)

    # Now run a specialized upload for Assignment Submission Types
    # Table.
    _upload_assignment_submission_types(db_adapter, submissions_type_df)
