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


def _prepare_staging_table(db_adapter: MssqlLmsOperations, df: pd.DataFrame, table: str) -> None:
    logger.info(f"Uploading {table} file ...")

    db_adapter.disable_staging_natural_key_index(table)
    db_adapter.truncate_staging_table(table)
    db_adapter.insert_into_staging(df, table)
    db_adapter.enable_staging_natural_key_index(table)


def _get_source_system(df: pd.DataFrame) -> str:
    return str(df.iloc[0]["SourceSystem"])


def _upload_assignments(
    db_adapter: MssqlLmsOperations, assignments_df: pd.DataFrame
) -> None:

    TABLE = Table.ASSIGNMENT
    columns = list(assignments_df.columns)

    # Truncate AssignmentDescription to max 1024 characters, matching the database
    assignments_df["AssignmentDescription"] = assignments_df["AssignmentDescription"].astype("str").str[:1024]  # type: ignore

    _prepare_staging_table(db_adapter, assignments_df, TABLE)
    db_adapter.insert_new_records_to_production_for_section(
        TABLE,
        columns
    )
    db_adapter.copy_updates_to_production(TABLE, columns)
    db_adapter.soft_delete_from_production(TABLE, _get_source_system(assignments_df))

    logger.info(f"Done with {TABLE} file.")


def _upload_assignment_submission_types(
    db_adapter: MssqlLmsOperations, submission_types_df: pd.DataFrame
) -> None:
    TABLE = Table.ASSIGNMENT_SUBMISSION_TYPES

    _prepare_staging_table(db_adapter, submission_types_df, TABLE)

    db_adapter.insert_new_submission_types()

    db_adapter.soft_delete_removed_submission_types(_get_source_system(submission_types_df))

    logger.info(f"Done with {TABLE} file.")


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
    if df.empty:
        return

    _prepare_staging_table(db_adapter, df, table)

    columns = list(df.columns)

    db_adapter.insert_new_records_to_production(table, columns)
    db_adapter.copy_updates_to_production(table, columns)

    db_adapter.soft_delete_from_production(table, _get_source_system(df))

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
    if assignments_df.empty:
        return

    assignments_df, submissions_type_df = assignment_splitter.split(assignments_df)

    _upload_assignments(db_adapter, assignments_df)

    if not submissions_type_df.empty:
        _upload_assignment_submission_types(db_adapter, submissions_type_df)


def upload_section_associations(
    db_adapter: MssqlLmsOperations, section_associations_df: pd.DataFrame
) -> None:

    TABLE = Table.SECTION_ASSOCIATION
    columns = list(section_associations_df.columns)

    _prepare_staging_table(db_adapter, section_associations_df, TABLE)
    db_adapter.insert_new_records_to_production_for_section_and_user(
        TABLE,
        columns
    )
    db_adapter.copy_updates_to_production(TABLE, columns)
    db_adapter.soft_delete_from_production(TABLE, _get_source_system(section_associations_df))

    logger.info(f"Done with {TABLE} file.")
