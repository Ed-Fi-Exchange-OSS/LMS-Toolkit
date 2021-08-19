# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
from logging import getLogger
from os import path, makedirs

import pandas as pd

from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions
from edfi_sql_adapter.sql_adapter import Adapter
from edfi_lms_harmonizer.sql_for_exceptions_report import (
    QUERY_FOR_ASSIGNMENT_CAT_DESCRIPTORS,
    QUERY_FOR_ASSIGNMENT_CAT_DESCRIPTORS_SUMMARY,
    QUERY_FOR_ASSIGNMENT_SUBMISSION_EXCEPTIONS,
    QUERY_FOR_ASSIGNMENT_EXCEPTIONS,
    QUERY_FOR_SECTION_SUMMARY,
    QUERY_FOR_SECTIONS,
    QUERY_FOR_SUBMISSION_STATUS_DESCRIPTORS,
    QUERY_FOR_SUBMISSION_STATUS_DESCRIPTORS_SUMMARY,
    QUERY_FOR_USERS,
    QUERY_FOR_USERS_SUMMARY
)

SECTIONS = "sections"
USERS = "users"
DESCRIPTORS = "descriptors"

logger = getLogger(__name__)


def _get_file_path(output_directory: str, report_type: str) -> str:
    dir_path = path.join(output_directory, report_type)

    makedirs(dir_path, exist_ok=True)

    file_path = path.join(
        dir_path, f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    )

    return file_path


def _print_summary_for_sections_and_users(adapter: Adapter) -> None:
    users_count = adapter.get_int(QUERY_FOR_USERS_SUMMARY)
    sections_count = adapter.get_int(QUERY_FOR_SECTION_SUMMARY)
    if sections_count > 0 or users_count > 0:
        logger.warning(
            f"There are {sections_count} unmatched sections and {users_count} "
            f"unmatched users in the database."
        )
    else:
        logger.debug("There are no unmatched sections or users in the database.")


def _print_summary_for_assignments_and_submissions(adapter: Adapter) -> None:
    assignments_count = adapter.get_int(
        QUERY_FOR_ASSIGNMENT_EXCEPTIONS
    )
    submissions_count = adapter.get_int(
        QUERY_FOR_ASSIGNMENT_SUBMISSION_EXCEPTIONS
    )
    if assignments_count > 0 or submissions_count > 0:
        logger.warning(
            f"There are {assignments_count} unmatched Assignments and"
            f" {submissions_count} unmatched Submissions"
        )
    else:
        logger.debug(
            "There are no unmatched Assignments or Assignment submissions in the database."
        )


def _print_summary_for_descriptors(adapter: Adapter) -> None:
    assignment_descriptors_count = adapter.get_int(
        QUERY_FOR_ASSIGNMENT_CAT_DESCRIPTORS_SUMMARY
    )
    submission_descriptors_count = adapter.get_int(
        QUERY_FOR_SUBMISSION_STATUS_DESCRIPTORS_SUMMARY
    )
    if assignment_descriptors_count > 0 or submission_descriptors_count > 0:
        logger.warning(
            f"There are {assignment_descriptors_count} missing descriptors for Assignment Category "
            f"and {submission_descriptors_count} missing descriptors for Submission Status"
        )
    else:
        logger.debug(
            "There are no missing descriptors for Assignment Category or Submission Status in the database."
        )


@catch_exceptions
def print_summary(adapter: Adapter) -> None:
    _print_summary_for_sections_and_users(adapter)
    _print_summary_for_assignments_and_submissions(adapter)
    _print_summary_for_descriptors(adapter)


@catch_exceptions
def create_exception_reports(adapter: Adapter, output_directory: str) -> None:
    logger.info("Writing the Sections exception report")
    sections = pd.read_sql(QUERY_FOR_SECTIONS, adapter.engine)
    sections.to_csv(_get_file_path(output_directory, SECTIONS), index=False)

    logger.info("Writing the Users exception report")
    users = pd.read_sql(QUERY_FOR_USERS, adapter.engine)
    users.to_csv(_get_file_path(output_directory, USERS), index=False)

    logger.info(
        "Writing the Assignment Category and Submission Status missing descriptors report"
    )
    assignment_cat = pd.read_sql(QUERY_FOR_ASSIGNMENT_CAT_DESCRIPTORS, adapter.engine)
    submission_status = pd.read_sql(
        QUERY_FOR_SUBMISSION_STATUS_DESCRIPTORS, adapter.engine
    )
    descriptors_report = pd.concat([assignment_cat, submission_status])
    descriptors_report.to_csv(
        _get_file_path(output_directory, DESCRIPTORS), index=False
    )
