# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
from typing import Dict, Tuple, cast
import sys
import logging

from pandas import DataFrame
import sqlalchemy
from canvasapi import Canvas

from edfi_canvas_extractor.config import get_canvas_api, get_sync_db_engine
from edfi_lms_extractor_lib.csv_generation.write import (
    write_section_activities,
    write_users,
    write_sections,
    write_section_associations,
    write_assignments,
    write_grades,
    write_assignment_submissions,
    write_system_activities,
)
from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions

from edfi_canvas_extractor.client_facade import (
    extract_courses,
    extract_grades,
    extract_sections,
    extract_students,
    extract_assignments,
    extract_submissions,
    extract_enrollments,
    extract_system_activities,
)
from edfi_canvas_extractor.api.canvas_helper import to_df
from edfi_canvas_extractor.helpers.arg_parser import MainArguments


logger = logging.getLogger(__name__)


results_store: Dict[str, Tuple] = {}


def _break_execution(failing_extraction: str) -> None:
    logger.critical(
        f"Unable to continue file generation because the load of {failing_extraction} failed. Please review the log for more information."
    )
    sys.exit(1)


@catch_exceptions
def _get_courses(
    arguments: MainArguments, canvas: Canvas, sync_db: sqlalchemy.engine.base.Engine
) -> None:
    logger.info("Extracting Courses from Canvas API")
    (courses, courses_df) = extract_courses(
        canvas, arguments.start_date, arguments.end_date, sync_db
    )
    results_store["courses"] = (courses, courses_df)


@catch_exceptions
def _get_sections(
    arguments: MainArguments, sync_db: sqlalchemy.engine.base.Engine
) -> None:
    logger.info("Extracting Sections from Canvas API")
    (courses, _) = results_store["courses"]
    (sections, udm_sections_df, all_section_ids) = extract_sections(courses, sync_db)
    logger.info("Writing LMS UDM Sections to CSV file")
    write_sections(udm_sections_df, datetime.now(), arguments.output_directory)
    results_store["sections"] = (sections, udm_sections_df, all_section_ids)


@catch_exceptions
def _get_section_activities(
    arguments: MainArguments,
) -> None:
    (_, _, all_section_ids) = results_store["sections"]
    logger.info("Writing empty LMS UDM SectionActivities to CSV files")
    write_section_activities(
        dict(), all_section_ids, datetime.now(), arguments.output_directory
    )


@catch_exceptions
def _get_assignments(
    arguments: MainArguments,
    sync_db: sqlalchemy.engine.base.Engine,
) -> None:
    logger.info("Extracting Assignments from Canvas API")
    (sections, _, all_section_ids) = results_store["sections"]
    (courses, _) = results_store["courses"]
    sections_df = to_df(sections)
    (assignments, udm_assignments_df) = extract_assignments(
        courses, sections_df, sync_db
    )
    logger.info("Writing LMS UDM Assignments to CSV files")
    write_assignments(
        udm_assignments_df, all_section_ids, datetime.now(), arguments.output_directory
    )
    results_store["assignments"] = (assignments, udm_assignments_df)


@catch_exceptions
def _get_students(
    arguments: MainArguments, sync_db: sqlalchemy.engine.base.Engine
) -> None:
    logger.info("Extracting Students from Canvas API")
    (courses, _) = results_store["courses"]
    (students, udm_students_df) = extract_students(courses, sync_db)
    results_store["students"] = (students, udm_students_df)
    logger.info("Writing LMS UDM Users to CSV file")
    write_users(udm_students_df, datetime.now(), arguments.output_directory)


@catch_exceptions
def _get_submissions(
    arguments: MainArguments,
    sync_db: sqlalchemy.engine.base.Engine,
) -> None:
    logger.info("Extracting Submissions from Canvas API")
    (assignments, _) = results_store["assignments"]
    (sections, _, _) = results_store["sections"]
    logger.info("Writing LMS UDM AssignmentSubmissions to CSV files")
    write_assignment_submissions(
        extract_submissions(assignments, sections, sync_db),
        datetime.now(),
        arguments.output_directory,
    )


@catch_exceptions
def _get_enrollments(
    arguments: MainArguments, sync_db: sqlalchemy.engine.base.Engine
) -> None:
    logger.info("Extracting Enrollments from Canvas API")
    (sections, _, all_section_ids) = results_store["sections"]
    (enrollments, udm_enrollments) = extract_enrollments(sections, sync_db)
    logger.info("Writing LMS UDM UserSectionAssociations to CSV files")
    write_section_associations(
        udm_enrollments, all_section_ids, datetime.now(), arguments.output_directory
    )
    results_store["enrollments"] = (enrollments, udm_enrollments)


@catch_exceptions
def _get_grades(arguments: MainArguments) -> None:
    logger.info("Extracting Grades from Canvas API")
    (enrollments, udm_enrollments) = results_store["enrollments"]
    (sections, _, all_section_ids) = results_store["sections"]
    udm_grades: Dict[str, DataFrame] = extract_grades(
        enrollments, cast(Dict[str, DataFrame], udm_enrollments), sections
    )
    logger.info("Writing LMS UDM Grades to CSV files")
    write_grades(
        udm_grades, all_section_ids, datetime.now(), arguments.output_directory
    )


@catch_exceptions
def _get_system_activities(
    arguments: MainArguments, sync_db: sqlalchemy.engine.base.Engine
) -> None:
    logger.info("Extracting System Activities from Canvas API")
    (users, _) = results_store["students"]
    udm_system_activities = extract_system_activities(
        users, arguments.start_date, arguments.end_date, sync_db
    )
    write_system_activities(
        udm_system_activities, datetime.now(), arguments.output_directory
    )


def run(arguments: MainArguments) -> None:
    logger.info("Starting Ed-Fi LMS Canvas Extractor")
    sync_db: sqlalchemy.engine.base.Engine = get_sync_db_engine(
        arguments.sync_database_directory
    )
    succeeded: bool = True

    succeeded = _get_courses(
        arguments, get_canvas_api(arguments.base_url, arguments.access_token), sync_db
    )
    if not succeeded:
        _break_execution("Courses")

    succeeded = _get_sections(arguments, sync_db)
    if not succeeded:
        _break_execution("Sections")

    succeeded = _get_students(arguments, sync_db)
    if not succeeded:
        _break_execution("Students")

    succeeded = _get_enrollments(arguments, sync_db)
    if not succeeded:
        _break_execution("Enrollments")

    if arguments.extract_assignments:
        succeeded = _get_assignments(arguments, sync_db)
        if succeeded:
            _get_submissions(arguments, sync_db)

    if arguments.extract_activities:
        _get_system_activities(arguments, sync_db)
        _get_section_activities(
            arguments,
        )

    if arguments.extract_grades:  # Grades are not supported by all the extractors
        _get_grades(
            arguments,
        )  # Grades don't need sync process because they are part of enrollments

    logger.info("Finishing Ed-Fi LMS Canvas Extractor")
