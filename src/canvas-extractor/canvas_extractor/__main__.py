# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from datetime import datetime
from typing import Callable, Dict, Tuple, Union
import sys
import os
import logging

from dotenv import load_dotenv
from pandas import DataFrame
import sqlalchemy
from errorhandler import ErrorHandler

from canvasapi import Canvas

from canvas_extractor.config import get_canvas_api, get_sync_db_engine
from canvas_extractor.csv_generation.write import (
    GRADES_ROOT_DIRECTORY,
    SUBMISSION_ROOT_DIRECTORY,
    write_csv,
    write_multi_csv,
    write_multi_tuple_csv,
    SECTIONS_ROOT_DIRECTORY,
    USERS_ROOT_DIRECTORY,
    ASSIGNMENT_ROOT_DIRECTORY,
    SECTION_ASSOCIATIONS_ROOT_DIRECTORY,
)
from canvas_extractor.extract_facade import (
    extract_courses,
    extract_grades,
    extract_sections,
    extract_students,
    extract_assignments,
    extract_submissions,
    extract_enrollments,
)
from canvas_extractor.api.canvas_helper import to_df
from canvas_extractor.helpers import arg_parser

logger: logging.Logger
error_tracker: ErrorHandler


base_url: str = ""
access_token: str = ""
log_level: str = ""
output_directory: str = ""
start_date: str = ""
end_date: str = ""

results_store: Dict[str, Tuple[list, Union[DataFrame, Dict[str, DataFrame]]]] = {}


def _break_execution(failing_extraction: str) -> None:
    logger.critical(
        f"Unable to continue file generation because the load of {failing_extraction} failed. Please review the log for more information."
    )
    sys.exit(1)


def catch_exceptions(func: Callable) -> Callable:
    def callable_function(*args, **kwargs) -> bool:
        try:
            func(*args, **kwargs)
            return True
        except BaseException as e:
            logger.exception("An exception occurred", e)
            return False

    return callable_function


@catch_exceptions
def parse_args():
    arguments = arg_parser.parse_main_arguments(sys.argv[1:])
    global base_url
    global access_token
    global log_level
    global output_directory
    global start_date
    global end_date

    base_url = arguments.base_url
    access_token = arguments.access_token
    log_level = arguments.log_level
    output_directory = arguments.output_directory
    start_date = arguments.start_date
    end_date = arguments.end_date


@catch_exceptions
def configure_logging():
    global logger
    global error_tracker

    logger = logging.getLogger(__name__)

    # We only want to log requests information on DEBUG level
    if log_level == "INFO":
        canvasapi_logger = logging.getLogger("canvasapi.requester")
        canvasapi_logger.setLevel("WARNING")

    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=log_level,
    )
    error_tracker = ErrorHandler()


@catch_exceptions
def _get_courses(canvas: Canvas, sync_db: sqlalchemy.engine.base.Engine) -> None:
    logger.info("Extracting Courses from Canvas API")
    (courses, courses_df) = extract_courses(canvas, start_date, end_date, sync_db)
    # Temporary - just for demonstration until UDM mapping
    courses_df.to_csv("data/courses.csv", index=False)
    results_store["courses"] = (courses, courses_df)


@catch_exceptions
def _get_sections(sync_db: sqlalchemy.engine.base.Engine) -> None:
    logger.info("Extracting Sections from Canvas API")
    (courses, _) = results_store["courses"]
    (sections, udm_sections_df) = extract_sections(courses, sync_db)
    write_csv(
        udm_sections_df,
        datetime.now(),
        os.path.join(output_directory, SECTIONS_ROOT_DIRECTORY),
    )
    results_store["sections"] = (sections, udm_sections_df)


@catch_exceptions
def _get_assignments(
    sync_db: sqlalchemy.engine.base.Engine,
) -> None:
    logger.info("Extracting Assignments from Canvas API")
    (sections, _) = results_store["sections"]
    (courses, _) = results_store["courses"]
    sections_df = to_df(sections)
    (assignments, udm_assignments_df) = extract_assignments(
        courses, sections_df, sync_db
    )
    write_multi_csv(
        udm_assignments_df,
        datetime.now(),
        os.path.join(output_directory, ASSIGNMENT_ROOT_DIRECTORY),
    )
    results_store["assignments"] = (assignments, udm_assignments_df)


@catch_exceptions
def _get_students(sync_db: sqlalchemy.engine.base.Engine) -> None:
    logger.info("Extracting Students from Canvas API")
    (courses, _) = results_store["courses"]
    (_, udm_students_df) = extract_students(courses, sync_db)
    write_csv(
        udm_students_df,
        datetime.now(),
        os.path.join(output_directory, USERS_ROOT_DIRECTORY),
    )


@catch_exceptions
def _get_submissions(
    sync_db: sqlalchemy.engine.base.Engine,
) -> None:
    logger.info("Extracting Submissions from Canvas API")
    (assignments, _) = results_store["assignments"]
    (sections, _) = results_store["sections"]
    write_multi_tuple_csv(
        extract_submissions(assignments, sections, sync_db),
        datetime.now(),
        os.path.join(output_directory, SUBMISSION_ROOT_DIRECTORY),
    )


@catch_exceptions
def _get_enrollments(sync_db: sqlalchemy.engine.base.Engine) -> None:
    logger.info("Extracting Enrollments from Canvas API")
    (sections, _) = results_store["sections"]
    (enrollments, udm_enrollments) = extract_enrollments(sections, sync_db)
    write_multi_csv(
        udm_enrollments,
        datetime.now(),
        os.path.join(output_directory, SECTION_ASSOCIATIONS_ROOT_DIRECTORY),
    )
    results_store["enrollments"] = (enrollments, udm_enrollments)


@catch_exceptions
def _get_grades() -> None:
    logger.info("Extracting Grades from Canvas API")
    (enrollments, udm_enrollments) = results_store["enrollments"]
    (sections, _) = results_store["sections"]
    udm_grades = extract_grades(enrollments, udm_enrollments, sections)
    write_multi_csv(
        udm_grades,
        datetime.now(),
        os.path.join(output_directory, GRADES_ROOT_DIRECTORY),
    )


def main():
    logger.info("Starting Ed-Fi LMS Canvas Extractor")
    sync_db: sqlalchemy.engine.base.Engine = get_sync_db_engine()
    succeeded: bool = True

    succeeded = _get_courses(get_canvas_api(base_url, access_token), sync_db)
    if not succeeded:
        _break_execution("Courses")

    succeeded = _get_sections(sync_db)
    if not succeeded:
        _break_execution("Sections")

    succeeded = _get_assignments(sync_db)
    if not succeeded:
        _break_execution("Assignments")

    _get_students(sync_db)
    _get_submissions(sync_db)

    succeeded = _get_enrollments(sync_db)
    if not succeeded:
        _break_execution("Enrollments")

    _get_grades()  # Grades don't need sync process because they are part of enrollments

    logger.info("Finishing Ed-Fi LMS Canvas Extractor")

    if error_tracker.fired:
        print(
            "A fatal error occurred, please review the log output for more information.",
            file=sys.stderr,
        )
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    load_dotenv()
    parse_args()
    configure_logging()
    main()
