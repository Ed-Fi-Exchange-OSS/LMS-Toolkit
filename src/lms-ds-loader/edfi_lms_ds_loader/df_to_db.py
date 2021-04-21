# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import Callable, List

import pandas as pd

from edfi_lms_ds_loader.helpers.constants import Table
from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations
from edfi_lms_ds_loader.helpers import assignment_splitter

logger = logging.getLogger(__name__)


def _prepare_staging_table(
    db_adapter: MssqlLmsOperations, df: pd.DataFrame, table: str
) -> None:
    logger.info(f"Uploading {table} file ...")

    db_adapter.disable_staging_natural_key_index(table)
    db_adapter.truncate_staging_table(table)
    db_adapter.insert_into_staging(df, table)
    db_adapter.enable_staging_natural_key_index(table)


def _get_source_system(df: pd.DataFrame) -> str:
    return str(df.iloc[0]["SourceSystem"])


def _upload_assignment_submission_types(
    db_adapter: MssqlLmsOperations, submission_types_df: pd.DataFrame
) -> None:
    TABLE = Table.ASSIGNMENT_SUBMISSION_TYPES

    _prepare_staging_table(db_adapter, submission_types_df, TABLE)

    db_adapter.insert_new_submission_types()

    source_system: str = _get_source_system(submission_types_df)
    db_adapter.unsoft_delete_returned_submission_types(source_system)
    db_adapter.soft_delete_removed_submission_types(source_system)

    logger.info(f"Done with {TABLE} file.")


def upload_file(
    db_adapter: MssqlLmsOperations,
    df: pd.DataFrame,
    table: str,
    db_adapter_insert_method: Callable[[MssqlLmsOperations, str, List[str]], None],
    db_adapter_delete_method: Callable[[MssqlLmsOperations, str, str], None],
) -> None:
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
    db_adapter_insert_method: Callable[[MssqlLmsOperations, str, List[str]], None]
        The MssqlLmsOperations insert method to use for the upload
    db_adapter_delete_method: Callable[[MssqlLmsOperations, str, str], None],
        The MssqlLmsOperations delete method to use for the upload
    """
    if df.empty:
        return

    _prepare_staging_table(db_adapter, df, table)

    columns = list(df.columns)

    db_adapter_insert_method(db_adapter, table, columns)
    db_adapter.copy_updates_to_production(table, columns)
    db_adapter_delete_method(db_adapter, table, _get_source_system(df))

    logger.info(f"Done with {table} file.")


def upload_users(db_adapter: MssqlLmsOperations, users_df: pd.DataFrame) -> None:
    """
    Uploads a User DataFrame to the User table.

    Parameters
    ----------
    db_adapter: MssqlLmsOperations
        Database engine-specific adapter/wrapper for database operations.
    users_df: pd.DataFrame
        A DataFrame to upload.
    """
    upload_file(
        db_adapter,
        users_df,
        Table.USER,
        MssqlLmsOperations.insert_new_records_to_production,
        MssqlLmsOperations.soft_delete_from_production,
    )


def upload_sections(db_adapter: MssqlLmsOperations, sections_df: pd.DataFrame) -> None:
    """
    Uploads a Section DataFrame to the Section table.

    Parameters
    ----------
    db_adapter: MssqlLmsOperations
        Database engine-specific adapter/wrapper for database operations.
    sections_df: pd.DataFrame
        A DataFrame to upload.
    """
    upload_file(
        db_adapter,
        sections_df,
        Table.SECTION,
        MssqlLmsOperations.insert_new_records_to_production,
        MssqlLmsOperations.soft_delete_from_production,
    )


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

    # Truncate AssignmentDescription to max 1024 characters, matching the database
    assignments_df["AssignmentDescription"] = assignments_df["AssignmentDescription"].astype("str").str[:1024]  # type: ignore
    upload_file(
        db_adapter,
        assignments_df,
        Table.ASSIGNMENT,
        MssqlLmsOperations.insert_new_records_to_production_for_section_relation,
        MssqlLmsOperations.soft_delete_from_production_for_section_relation,
    )

    if not submissions_type_df.empty:
        _upload_assignment_submission_types(db_adapter, submissions_type_df)


def upload_section_associations(
    db_adapter: MssqlLmsOperations, section_associations_df: pd.DataFrame
) -> None:
    """
    Uploads a Section Association DataFrame to the User-Section Association
    table.

    Parameters
    ----------
    db_adapter: MssqlLmsOperations
        Database engine-specific adapter/wrapper for database operations.
    section_associations_df: pd.DataFrame
        A DataFrame to upload.
    """
    upload_file(
        db_adapter,
        section_associations_df,
        Table.SECTION_ASSOCIATION,
        MssqlLmsOperations.insert_new_records_to_production_for_section_and_user_relation,
        MssqlLmsOperations.soft_delete_from_production_for_section_relation,
    )


def upload_assignment_submissions(
    db_adapter: MssqlLmsOperations, submissions_df: pd.DataFrame
) -> None:
    """
    Uploads an Assignment Submission DataFrame to the Assignment Submission
    table.

    Parameters
    ----------
    db_adapter: MssqlLmsOperations
        Database engine-specific adapter/wrapper for database operations.
    submissions_df: pd.DataFrame
        A DataFrame to upload.
    """
    upload_file(
        db_adapter,
        submissions_df,
        Table.ASSIGNMENT_SUBMISSION,
        MssqlLmsOperations.insert_new_records_to_production_for_assignment_and_user_relation,
        MssqlLmsOperations.soft_delete_from_production_for_assignment_relation,
    )


def upload_section_activities(
    db_adapter: MssqlLmsOperations, section_activities_df: pd.DataFrame
) -> None:
    """
    Uploads a Section Activity DataFrame to the Section Activity
    table.

    Parameters
    ----------
    db_adapter: MssqlLmsOperations
        Database engine-specific adapter/wrapper for database operations.
    section_activities_df: pd.DataFrame
        A DataFrame to upload.
    """
    upload_file(
        db_adapter,
        section_activities_df,
        Table.SECTION_ACTIVITY,
        MssqlLmsOperations.insert_new_records_to_production_for_section_and_user_relation,
        MssqlLmsOperations.soft_delete_from_production_for_section_relation,
    )


def upload_system_activities(
    db_adapter: MssqlLmsOperations, system_activities_df: pd.DataFrame
) -> None:
    """
    Uploads a System Activity DataFrame to the System Activity
    table.

    Parameters
    ----------
    db_adapter: MssqlLmsOperations
        Database engine-specific adapter/wrapper for database operations.
    system_activities_df: pd.DataFrame
        A DataFrame to upload.
    """
    upload_file(
        db_adapter,
        system_activities_df,
        Table.SYSTEM_ACTIVITY,
        MssqlLmsOperations.insert_new_records_to_production_for_user_relation,
        MssqlLmsOperations.soft_delete_from_production,
    )


def upload_attendance_events(
    db_adapter: MssqlLmsOperations, attendance_df: pd.DataFrame
) -> None:
    """
    Uploads a System Activity DataFrame to the System Activity
    table.

    Parameters
    ----------
    db_adapter: MssqlLmsOperations
        Database engine-specific adapter/wrapper for database operations.
    attendance_df: pd.DataFrame
        A DataFrame to upload.
    """
    upload_file(
        db_adapter,
        attendance_df,
        Table.ATTENDANCE,
        MssqlLmsOperations.insert_new_records_to_production_for_attendance_events,
        MssqlLmsOperations.soft_delete_from_production_for_section_relation,
    )
