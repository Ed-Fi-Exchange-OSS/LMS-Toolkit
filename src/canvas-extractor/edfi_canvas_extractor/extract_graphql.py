# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import sqlalchemy
import sys

from datetime import datetime
from typing import Dict, List, Tuple

from canvasapi import Canvas
from canvasapi.account import Account

from edfi_canvas_extractor.config import get_canvas_api, get_sync_db_engine
from edfi_canvas_extractor.graphql.extractor import GraphQLExtractor
from edfi_lms_extractor_lib.csv_generation.write import (
    write_sections,
    write_section_associations,
    write_users,
)
from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions
from edfi_canvas_extractor.client_graphql import (
    extract_courses,
    extract_enrollments,
    extract_sections,
    extract_students,
)
from edfi_canvas_extractor.helpers.arg_parser import MainArguments


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
) -> None:
    logger.info("Extracting Courses from Canvas")

    (courses, courses_df) = extract_courses(
        gql, sync_db
    )

    results_store["courses"] = (courses, courses_df)


@catch_exceptions
def _get_sections(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine
) -> None:
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


@catch_exceptions
def _write_sections(
    arguments: MainArguments,
) -> None:
    _, udm_sections_df, _ = results_store["sections"]

    logger.info("Writing LMS UDM Sections to CSV file")
    write_sections(udm_sections_df, datetime.now(), arguments.output_directory)


@catch_exceptions
def _get_students(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine
) -> None:
    logger.info("Extracting Students from Canvas")
    (students, udm_students_df) = extract_students(gql, sync_db)
    results_store["students"] = (students, udm_students_df)


@catch_exceptions
def _write_students(arguments: MainArguments) -> None:
    (students, udm_students_df) = results_store["students"]

    logger.info("Writing LMS UDM Users to CSV file")
    write_users(udm_students_df, datetime.now(), arguments.output_directory)


@catch_exceptions
def _get_enrollments(
    gql: GraphQLExtractor,
    sync_db: sqlalchemy.engine.base.Engine
) -> None:
    logger.info("Extracting Enrollments from Canvas")
    (_, _, all_section_ids) = results_store["sections"]
    (enrollments, udm_enrollments) = extract_enrollments(gql, all_section_ids, sync_db)
    results_store["enrollments"] = (enrollments, udm_enrollments)


@catch_exceptions
def _write_sections_associations(arguments: MainArguments) -> None:
    _, _, all_section_ids = results_store["sections"]
    _, udm_enrollments = results_store["enrollments"]

    logger.info("Writing LMS UDM UserSectionAssociations to CSV files")
    write_section_associations(
        udm_enrollments, all_section_ids, datetime.now(), arguments.output_directory
    )


def run(arguments: MainArguments) -> None:
    logger.info("Starting Ed-Fi LMS Canvas Extractor")
    sync_db: sqlalchemy.engine.base.Engine = get_sync_db_engine(
        arguments.sync_database_directory
    )
    canvas: Canvas = get_canvas_api(arguments.base_url, arguments.access_token)

    accounts: List[Account] = canvas.get_accounts()

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

    _write_sections(arguments)
    _write_students(arguments)

    logger.info("Finishing Ed-Fi LMS Canvas Extractor")
