# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import sqlalchemy
import sys

from datetime import datetime
from pandas import DataFrame
from typing import cast, Dict, Tuple

from canvasapi import Canvas
from canvasapi.paginated_list import PaginatedList

from edfi_canvas_extractor.config import get_canvas_api, get_sync_db_engine
from edfi_canvas_extractor.graphql.extractor import GraphQLExtractor
from edfi_lms_extractor_lib.csv_generation.write import (
    write_assignments,
    write_assignment_submissions,
    write_grades,
    write_sections,
    write_section_activities,
    write_section_associations,
    write_users,
)
from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions
from edfi_canvas_extractor.client_graphql import (
    extract_assignments,
    extract_grades,
    extract_courses,
    extract_enrollments,
    extract_sections,
    extract_submissions,
    extract_students,
)
from edfi_canvas_extractor.helpers.arg_parser import MainArguments
from edfi_canvas_extractor.graphql.canvas_helper import to_df


logger = logging.getLogger(__name__)
results_store: Dict[str, Tuple] = {}


def _break_execution(failing_extraction: str) -> None:
    logger.critical(
        f"Unable to continue file generation because the load of {failing_extraction} failed. "
        "Please review the log for more information."
    )
    sys.exit(1)


@catch_exceptions
def _get_courses(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine
) -> bool:
    logger.info("Extracting Courses from Canvas")

    (courses, courses_df) = extract_courses(
        gql, sync_db
    )

    results_store["courses"] = (courses, courses_df)

    return True


@catch_exceptions
def _get_sections(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine
) -> bool:
    logger.info("Extracting Sections from Canvas")
    sections, udm_sections_df, all_section_ids = extract_sections(gql, sync_db)

    if "sections" not in results_store:
        results_store["sections"] = (sections, udm_sections_df, all_section_ids)
    else:
        sections_temp, udm_sections_df_temp, all_section_ids_temp = results_store["sections"]

        sections_temp.extend(sections)
        udm_sections_df_temp = udm_sections_df_temp.append(udm_sections_df)
        all_section_ids_temp.extend(all_section_ids)

        results_store["sections"] = (sections_temp, udm_sections_df_temp, all_section_ids_temp)

    return True


@catch_exceptions
def _write_sections(
    arguments: MainArguments,
) -> None:
    _, udm_sections_df, _ = results_store["sections"]

    logger.info("Writing LMS UDM Sections to CSV file")
    write_sections(udm_sections_df, datetime.now(), arguments.output_directory)


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
def _get_students(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine
) -> bool:
    logger.info("Extracting Students from Canvas")
    (students, udm_students_df) = extract_students(gql, sync_db)
    results_store["students"] = (students, udm_students_df)

    return True


@catch_exceptions
def _write_students(arguments: MainArguments) -> None:
    (students, udm_students_df) = results_store["students"]

    logger.info("Writing LMS UDM Users to CSV file")
    write_users(udm_students_df, datetime.now(), arguments.output_directory)


@catch_exceptions
def _get_enrollments(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine
) -> bool:
    logger.info("Extracting Enrollments from Canvas")
    (_, _, all_section_ids) = results_store["sections"]
    (enrollments, udm_enrollments) = extract_enrollments(gql, all_section_ids, sync_db)
    results_store["enrollments"] = (enrollments, udm_enrollments)

    return True


@catch_exceptions
def _write_sections_associations(arguments: MainArguments) -> None:
    _, _, all_section_ids = results_store["sections"]
    _, udm_enrollments = results_store["enrollments"]

    logger.info("Writing LMS UDM UserSectionAssociations to CSV files")
    write_section_associations(
        udm_enrollments, all_section_ids, datetime.now(), arguments.output_directory
    )


@catch_exceptions
def _get_assignments(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine,
) -> bool:
    logger.info("Extracting Assignments from Canvas")
    (sections, _, _) = results_store["sections"]
    sections_df = to_df(sections)
    (assignments, udm_assignments_df) = extract_assignments(
        sections_df, gql, sync_db
    )
    results_store["assignments"] = (assignments, udm_assignments_df)

    return True


@catch_exceptions
def _write_assignments(
    arguments: MainArguments,
) -> None:
    logger.info("Writing LMS UDM Assignments to CSV files")
    (_, _, all_section_ids) = results_store["sections"]
    (_, udm_assignments_df) = results_store["assignments"]
    write_assignments(
        udm_assignments_df, all_section_ids, datetime.now(), arguments.output_directory
    )


@catch_exceptions
def _get_submissions(
    arguments: MainArguments,
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine,
) -> bool:
    logger.info("Extracting Submissions from Canvas")
    logger.info("Writing LMS UDM AssignmentSubmissions to CSV files")
    submissions = extract_submissions(gql, sync_db)
    if submissions:
        write_assignment_submissions(
            submissions,
            datetime.now(),
            arguments.output_directory,
        )

    return True


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


def run(arguments: MainArguments) -> None:
    logger.info("Starting Ed-Fi LMS Canvas Extractor")
    sync_db: sqlalchemy.engine.base.Engine = get_sync_db_engine(
        arguments.sync_database_directory
    )
    canvas: Canvas = get_canvas_api(arguments.base_url, arguments.access_token)

    accounts: PaginatedList = canvas.get_accounts()

    for account in accounts:
        _id = getattr(account, "id")

        logger.info(f"Getting data for account ID {_id}")

        gql = GraphQLExtractor(
            arguments.base_url,
            arguments.access_token,
            _id,
            arguments.start_date,
            arguments.end_date
            )
        gql.run()

        succeeded: bool = True

        succeeded = _get_courses(gql, sync_db)
        if not succeeded:
            _break_execution("Courses")

        succeeded = _get_sections(gql, sync_db)
        if not succeeded:
            _break_execution("Sections")

        succeeded = _get_students(gql, sync_db)
        if not succeeded:
            _break_execution("Students")

        succeeded = _get_enrollments(gql, sync_db)
        if not succeeded:
            _break_execution("Enrollments")

        _write_sections_associations(arguments)

        if arguments.extract_assignments:
            succeeded = _get_assignments(gql, sync_db)
            _write_assignments(arguments)
            if succeeded:
                _get_submissions(arguments, gql, sync_db)

        if arguments.extract_activities:
            _get_section_activities(
                arguments,
            )

        if arguments.extract_grades:  # Grades are not supported by all the extractors
            _get_grades(
                arguments,
            )  # Grades don't need sync process because they are part of enrollments

    _write_sections(arguments)
    _write_students(arguments)

    logger.info("Finishing Ed-Fi LMS Canvas Extractor")
