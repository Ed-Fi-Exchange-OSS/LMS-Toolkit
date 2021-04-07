# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

# Developer note: this module is deliberately not unit tested. As a facade it is
# by definition complex. In this application, it contains the main application
# logic and is tested simply by running the application. Any branching or
# looping logic should go into other modules where they can be tested easily.

import logging
import os
from typing import Callable, Optional, Set
from functools import lru_cache

from pandas import DataFrame

from edfi_lms_ds_loader.helpers.constants import Table
from edfi_lms_ds_loader.helpers.argparser import MainArguments
from edfi_lms_ds_loader import migrator
from edfi_lms_file_utils import file_reader, file_repository
from edfi_lms_file_utils.constants import Resources
from edfi_lms_ds_loader import df_to_db
from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations

logger = logging.getLogger(__name__)


# This module deliberately has no exception handling. Due to the foreign key
# relationships between tables, there is little point to continuing after a
# failure. For example: users upload fails. Then section would work, but most of
# the child-objects of section have a dependency on users. If users succeeds,
# but section fails, then there's little value to having the users and nothing
# else. When we get that far down, better to keep the pattern of not catching
# exceptions throughout then to only catch exceptions on "lower value" targets
# like grades or attendance.

# TODO: consider refactoring for transaction management, so that operations can
# be rolled back. SQL Alchemy transactions can be used with DataFrame, so this
# should be feasible. https://tracker.ed-fi.org/browse/LMS-244


@lru_cache()
def _get_sections_df(csv_path: str) -> DataFrame:
    return file_reader.get_all_sections(csv_path)


@lru_cache()
def _get_assignments_df(csv_path: str) -> DataFrame:
    sections_df: DataFrame = _get_sections_df(csv_path)
    if sections_df.empty:
        return DataFrame()
    return file_reader.get_all_assignments(csv_path, sections_df)


def _get_unprocessed_file_paths(
    db_adapter: MssqlLmsOperations,
    resource_name: str,
    get_all_paths_callback: Callable,
) -> Set[str]:
    processed_files = db_adapter.get_processed_files(resource_name)
    all_paths = set(get_all_paths_callback())
    return all_paths - processed_files


def _upload_files_from_paths(
    db_adapter: MssqlLmsOperations,
    files: Set[str],
    table_name: str,
    resource_name: str,
    read_file_callback: Callable,
    custom_upload_function: Optional[Callable] = None,
) -> None:
    for path in files:
        data: DataFrame = read_file_callback(path)
        rows = data.shape[0]
        if rows != 0:
            if custom_upload_function is not None:
                custom_upload_function(db_adapter, data)
            else:
                df_to_db.upload_file(
                    db_adapter,
                    data,
                    table_name,
                    MssqlLmsOperations.insert_new_records_to_production,
                )
        db_adapter.add_processed_file(path, resource_name, rows)


def _load_users(csv_path: str, db_adapter: MssqlLmsOperations) -> None:
    def __get_all_file_paths_callback():
        formatted_path = os.path.abspath(csv_path)
        paths = file_repository.get_users_file_paths(formatted_path)
        return paths

    unprocessed_files = _get_unprocessed_file_paths(
        db_adapter, Resources.USERS, __get_all_file_paths_callback
    )
    _upload_files_from_paths(
        db_adapter,
        unprocessed_files,
        Table.USER,
        Resources.USERS,
        file_reader.read_users_file,
    )


def _load_sections(csv_path: str, db_adapter: MssqlLmsOperations) -> None:
    def __get_all_file_paths_callback():
        formatted_path = os.path.abspath(csv_path)
        paths = file_repository.get_sections_file_paths(formatted_path)
        return paths

    unprocessed_files = _get_unprocessed_file_paths(
        db_adapter, Resources.SECTIONS, __get_all_file_paths_callback
    )
    _upload_files_from_paths(
        db_adapter,
        unprocessed_files,
        Table.SECTION,
        Resources.SECTIONS,
        file_reader.read_sections_file,
    )


def _load_assignments(csv_path: str, db_adapter: MssqlLmsOperations) -> None:
    sections_df = _get_sections_df(csv_path)
    if sections_df.empty:
        logger.info("No sections loaded. Skipping assignments.")
        return
    sections = set(
        sections_df["SourceSystemIdentifier"]
    )  # we only need to access the last file

    def __get_all_file_paths_callback():
        formatted_path = os.path.abspath(csv_path)
        paths = []
        for section in sections:
            paths = paths + file_repository.get_assignments_file_paths(
                formatted_path, section
            )

        return paths

    unprocessed_files = _get_unprocessed_file_paths(
        db_adapter, Resources.ASSIGNMENTS, __get_all_file_paths_callback
    )
    _upload_files_from_paths(
        db_adapter,
        unprocessed_files,
        Table.ASSIGNMENT,
        Resources.ASSIGNMENTS,
        file_reader.read_assignments_file,
        df_to_db.upload_assignments,
    )


def _load_attendance_events(csv_path: str, db_adapter: MssqlLmsOperations) -> None:
    sections_df: DataFrame = _get_sections_df(csv_path)
    if sections_df.empty:
        logger.info("No sections loaded. Skipping section associations.")
        return
    sections = set(sections_df["SourceSystemIdentifier"])

    def __get_all_file_paths_callback():
        formatted_path = os.path.abspath(csv_path)
        paths = []
        for section in sections:
            paths = paths + file_repository.get_attendance_events_paths(
                formatted_path, section
            )

        return paths

    unprocessed_files = _get_unprocessed_file_paths(
        db_adapter, Resources.ATTENDANCE_EVENTS, __get_all_file_paths_callback
    )

    _upload_files_from_paths(
        db_adapter,
        unprocessed_files,
        Table.ATTENDANCE,
        Resources.ATTENDANCE_EVENTS,
        file_reader.read_attendance_events_file,
        df_to_db.upload_attendance_events
    )


def _load_section_associations(csv_path: str, db_adapter: MssqlLmsOperations) -> None:
    sections_df: DataFrame = _get_sections_df(csv_path)
    if sections_df.empty:
        logger.info("No sections loaded. Skipping section associations.")
        return
    sections = set(sections_df["SourceSystemIdentifier"])

    def __get_all_file_paths_callback():
        formatted_path = os.path.abspath(csv_path)
        paths = []
        for section in sections:
            paths = paths + file_repository.get_section_associations_file_paths(
                formatted_path, section
            )

        return paths

    unprocessed_files = _get_unprocessed_file_paths(
        db_adapter, Resources.SECTION_ASSOCIATIONS, __get_all_file_paths_callback
    )
    _upload_files_from_paths(
        db_adapter,
        unprocessed_files,
        Table.SECTION_ASSOCIATION,
        Resources.SECTION_ASSOCIATIONS,
        file_reader.read_section_associations_file,
        df_to_db.upload_section_associations,
    )


def _load_assignment_submissions(csv_path: str, db_adapter: MssqlLmsOperations) -> None:
    assignments_df: DataFrame = _get_assignments_df(csv_path)
    if assignments_df.empty:
        logger.info("No assignments loaded. Skipping assignment submissions.")
        return

    def __get_all_file_paths_callback():
        formatted_path = os.path.abspath(csv_path)
        paths = []
        for section_id, assignment_id in zip(
            assignments_df.LMSSectionSourceSystemIdentifier,
            assignments_df.SourceSystemIdentifier,
        ):
            paths = paths + file_repository.get_submissions_file_paths(
                formatted_path,
                section_id,
                assignment_id,
            )

        return paths

    unprocessed_files = _get_unprocessed_file_paths(
        db_adapter, Resources.SUBMISSIONS, __get_all_file_paths_callback
    )
    _upload_files_from_paths(
        db_adapter,
        unprocessed_files,
        Table.ASSIGNMENT_SUBMISSION,
        Resources.SUBMISSIONS,
        file_reader.read_submissions_file,
        df_to_db.upload_assignment_submissions,
    )


def _load_section_activities(csv_path: str, db_adapter: MssqlLmsOperations) -> None:
    sections_df: DataFrame = _get_sections_df(csv_path)
    if sections_df.empty:
        logger.info("No sections loaded. Skipping section associations.")
        return
    sections = set(sections_df["SourceSystemIdentifier"])

    def __get_all_file_paths_callback():
        formatted_path = os.path.abspath(csv_path)
        paths = []
        for section in sections:
            paths = paths + file_repository.get_section_activities_file_paths(
                formatted_path, section
            )

        return paths

    unprocessed_files = _get_unprocessed_file_paths(
        db_adapter, Resources.SECTION_ACTIVITIES, __get_all_file_paths_callback
    )
    _upload_files_from_paths(
        db_adapter,
        unprocessed_files,
        Table.SECTION_ACTIVITY,
        Resources.SECTION_ACTIVITIES,
        file_reader.read_section_activities_file,
        df_to_db.upload_section_activities,
    )


def _load_system_activities(csv_path: str, db_adapter: MssqlLmsOperations) -> None:
    def __get_all_file_paths_callback():
        formatted_path = os.path.abspath(csv_path)
        paths = file_repository.get_system_activities_file_paths(formatted_path)
        return paths

    unprocessed_files = _get_unprocessed_file_paths(
        db_adapter, Resources.SYSTEM_ACTIVITIES, __get_all_file_paths_callback
    )
    _upload_files_from_paths(
        db_adapter,
        unprocessed_files,
        Table.SYSTEM_ACTIVITY,
        Resources.SYSTEM_ACTIVITIES,
        file_reader.read_system_activities_file,
        df_to_db.upload_system_activities
    )


def run_loader(arguments: MainArguments) -> None:
    logger.info("Begin loading files into the LMS Data Store (DS)...")

    migrator.migrate(arguments.get_db_engine())

    csv_path = arguments.csv_path

    db_adapter = arguments.get_db_operations_adapter()

    _load_users(csv_path, db_adapter)
    _load_sections(csv_path, db_adapter)
    _load_assignments(csv_path, db_adapter)
    _load_assignment_submissions(csv_path, db_adapter)
    _load_attendance_events(csv_path, db_adapter)
    _load_section_associations(csv_path, db_adapter)
    _load_section_activities(csv_path, db_adapter)
    _load_system_activities(csv_path, db_adapter)

    logger.info("Done loading files into the LMS Data Store.")
