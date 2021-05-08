# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import logging
from typing import Any, Dict, List
import sys

from googleapiclient.discovery import build, Resource
from google.oauth2 import service_account
from pandas import DataFrame
import sqlalchemy


from edfi_google_classroom_extractor.api.courses import request_all_courses_as_df
from edfi_google_classroom_extractor.api.coursework import request_all_coursework_as_df
from edfi_google_classroom_extractor.api.students import request_all_students_as_df
from edfi_google_classroom_extractor.api.teachers import request_all_teachers_as_df
from edfi_google_classroom_extractor.api.submissions import (
    request_all_submissions_as_df,
)
from edfi_google_classroom_extractor.helpers.arg_parser import MainArguments
from edfi_google_classroom_extractor.config import get_credentials, get_sync_db_engine
from edfi_google_classroom_extractor.mapping.users import (
    students_and_teachers_to_users_df,
)
from edfi_google_classroom_extractor.mapping.user_section_associations import (
    students_and_teachers_to_user_section_associations_dfs,
)
from edfi_google_classroom_extractor.mapping.sections import courses_to_sections_df
from edfi_google_classroom_extractor.mapping.assignments import (
    coursework_to_assignments_dfs,
)
from edfi_google_classroom_extractor.mapping.assignment_submissions import (
    submissions_to_assignment_submissions_dfs,
)
from edfi_google_classroom_extractor.mapping.user_submission_activities import (
    submissions_to_user_submission_activities_dfs,
)
from edfi_lms_extractor_lib.csv_generation.write import (
    write_grades,
    write_users,
    write_sections,
    write_section_associations,
    write_section_activities,
    write_assignments,
    write_assignment_submissions,
    write_system_activities,
)
from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions


logger = logging.getLogger(__name__)
now = datetime.now()
# This variable facilitates temporary storage of output results from one GET
# request that need to be used for creating another GET request.
result_bucket: Dict[str, Any] = {}


def _break_execution(failing_extraction: str) -> None:
    logger.critical(
        f"Unable to continue file generation because the load of {failing_extraction} failed. Please review the log for more information."
    )
    sys.exit(1)


@catch_exceptions
def _get_courses(
    classroom_resource: Resource,
    sync_db: sqlalchemy.engine.base.Engine,
    output_directory: str,
):
    courses_df: DataFrame = request_all_courses_as_df(classroom_resource, sync_db)
    result_bucket["course_ids"] = courses_df["id"].tolist()

    logger.info("Writing LMS UDM Sections to CSV file")
    (sections_df, all_section_ids) = courses_to_sections_df(courses_df)
    result_bucket["section_ids"] = all_section_ids
    write_sections(
        sections_df,
        now,
        output_directory,
    )


@catch_exceptions
def _get_users(
    classroom_resource: Resource,
    sync_db: sqlalchemy.engine.base.Engine,
    output_directory: str,
):
    course_ids: List[str] = result_bucket["course_ids"]

    students = request_all_students_as_df(classroom_resource, course_ids, sync_db)
    teachers = request_all_teachers_as_df(classroom_resource, course_ids, sync_db)
    result_bucket["students_df"] = students
    result_bucket["teachers_df"] = teachers

    logger.info("Writing LMS UDM Users to CSV file")
    write_users(
        students_and_teachers_to_users_df(students, teachers),
        now,
        output_directory,
    )


@catch_exceptions
def _get_section_associations(classroom_resource: Resource, output_directory: str):
    logger.info("Writing LMS UDM UserSectionAssociations to CSV files")

    students_df = result_bucket["students_df"]
    teachers_df = result_bucket["teachers_df"]
    all_section_ids = result_bucket["section_ids"]

    write_section_associations(
        students_and_teachers_to_user_section_associations_dfs(
            students_df, teachers_df
        ),
        all_section_ids,
        now,
        output_directory,
    )


@catch_exceptions
def _get_assignments(
    classroom_resource: Resource,
    sync_db: sqlalchemy.engine.base.Engine,
    output_directory: str,
):
    logger.info("Writing LMS UDM Assignments to CSV files")

    course_ids: List[str] = result_bucket["course_ids"]
    all_section_ids = result_bucket["section_ids"]
    courseworks_df = request_all_coursework_as_df(
        classroom_resource, course_ids, sync_db
    )

    write_assignments(
        coursework_to_assignments_dfs(courseworks_df),
        all_section_ids,
        now,
        output_directory,
    )


@catch_exceptions
def _get_assignment_submissions(
    classroom_resource: Resource,
    sync_db: sqlalchemy.engine.base.Engine,
    output_directory: str,
):
    logger.info("Writing LMS UDM AssignmentSubmissions to CSV files")

    course_ids: List[str] = result_bucket["course_ids"]
    submissions_df = request_all_submissions_as_df(
        classroom_resource, course_ids, sync_db
    )
    result_bucket["submissions_df"] = submissions_df

    write_assignment_submissions(
        submissions_to_assignment_submissions_dfs(submissions_df),
        now,
        output_directory,
    )


@catch_exceptions
def _get_section_activities(output_directory: str):
    logger.info("Writing LMS UDM Section Activities to CSV files")

    submissions_df: DataFrame = result_bucket["submissions_df"]
    all_section_ids = result_bucket["section_ids"]
    write_section_activities(
        submissions_to_user_submission_activities_dfs(submissions_df),
        all_section_ids,
        now,
        output_directory,
    )


@catch_exceptions
def _get_system_activities(output_directory: str):
    logger.info("Writing empty LMS UDM SystemActivities to CSV file")

    write_system_activities(
        DataFrame(),
        now,
        output_directory,
    )


@catch_exceptions
def _get_grades(output_directory: str):
    logger.info("Writing empty LMS UDM Grades to CSV files")

    all_section_ids = result_bucket["section_ids"]
    write_grades(
        dict(),
        all_section_ids,
        now,
        output_directory,
    )


def run(arguments: MainArguments):
    logger.info("Starting Ed-Fi LMS Google Classroom Extractor")
    credentials: service_account.Credentials = get_credentials(
        arguments.classroom_account
    )
    classroom_resource: Resource = build(
        "classroom", "v1", credentials=credentials, cache_discovery=False
    )
    sync_db: sqlalchemy.engine.base.Engine = get_sync_db_engine(
        arguments.sync_database_directory
    )

    succeeded: bool = False

    succeeded = _get_courses(classroom_resource, sync_db, arguments.output_directory)
    if not succeeded:
        _break_execution("Sections")

    succeeded = _get_users(classroom_resource, sync_db, arguments.output_directory)
    if not succeeded:
        _break_execution("Users")

    succeeded = _get_section_associations(classroom_resource, arguments.output_directory)
    if not succeeded:
        _break_execution("Section Associations")

    if arguments.extract_assignments:
        succeeded = _get_assignments(
            classroom_resource, sync_db, arguments.output_directory
        )
        if not succeeded:
            _break_execution("Assignments")

        _get_assignment_submissions(
            classroom_resource, sync_db, arguments.output_directory
        )

    if arguments.extract_activities:
        _get_section_activities(arguments.output_directory)
        _get_system_activities(arguments.output_directory)

    if arguments.extract_grades:
        _get_grades(arguments.output_directory)

    logger.info("Finishing Ed-Fi LMS Google Classroom Extractor")
