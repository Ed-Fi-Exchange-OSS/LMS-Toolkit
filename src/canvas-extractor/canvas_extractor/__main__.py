# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from datetime import datetime
from typing import List, Tuple
import sys
import os
import logging

from dotenv import load_dotenv
from pandas import DataFrame
import sqlalchemy
from errorhandler import ErrorHandler

from canvasapi import Canvas
from canvasapi.assignment import Assignment
from canvasapi.course import Course
from canvasapi.section import Section
from canvasapi.user import User

from canvas_extractor.config import get_canvas_api, get_sync_db_engine
from canvas_extractor.csv_generation.write import (
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
    extract_sections,
    extract_students,
    extract_assignments,
    extract_submissions,
    extract_enrollments,
)

logger: logging.Logger
error_tracker: ErrorHandler
BASE_OUTPUT_DIRECTORY = "data"


def load_dotenv_values():
    load_dotenv()
    global BASE_OUTPUT_DIRECTORY
    BASE_OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIRECTORY", "data")


def configure_logging():
    global logger
    global error_tracker

    logger = logging.getLogger(__name__)

    level = os.environ.get("LOGLEVEL", "INFO")
    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=level,
    )
    error_tracker = ErrorHandler()


def _get_courses(
    canvas: Canvas, sync_db: sqlalchemy.engine.base.Engine
) -> Tuple[List[Course], DataFrame]:
    logger.info("Extracting Courses from Canvas API")
    (courses, courses_df) = extract_courses(canvas, sync_db)
    # Temporary - just for demonstration until UDM mapping
    courses_df.to_csv("data/courses.csv", index=False)
    return (courses, courses_df)


def _get_sections(
    courses: List[Course], sync_db: sqlalchemy.engine.base.Engine
) -> Tuple[List[Section], DataFrame]:
    logger.info("Extracting Sections from Canvas API")
    (sections, udm_sections_df) = extract_sections(courses, sync_db)
    write_csv(
        udm_sections_df,
        datetime.now(),
        os.path.join(BASE_OUTPUT_DIRECTORY, SECTIONS_ROOT_DIRECTORY),
    )
    return (sections, udm_sections_df)


def _get_students(
    courses: List[Course], sync_db: sqlalchemy.engine.base.Engine
) -> List[User]:
    logger.info("Extracting Students from Canvas API")
    (students, udm_students_df) = extract_students(courses, sync_db)
    write_csv(
        udm_students_df,
        datetime.now(),
        os.path.join(BASE_OUTPUT_DIRECTORY, USERS_ROOT_DIRECTORY),
    )
    return students


def _get_assignments(
    courses: List[Course],
    sections_df: DataFrame,
    sync_db: sqlalchemy.engine.base.Engine,
) -> Tuple[List[Assignment], DataFrame]:
    logger.info("Extracting Assignments from Canvas API")
    (assignments, udm_assignments_df) = extract_assignments(
        courses, sections_df, sync_db
    )
    write_multi_csv(
        udm_assignments_df,
        datetime.now(),
        os.path.join(BASE_OUTPUT_DIRECTORY, ASSIGNMENT_ROOT_DIRECTORY),
    )
    return (assignments, udm_assignments_df)


def _get_submissions(
    assignments: List[Assignment],
    sections: List[Section],
    sync_db: sqlalchemy.engine.base.Engine,
):
    logger.info("Extracting Submissions from Canvas API")
    write_multi_tuple_csv(
        extract_submissions(assignments, sections, sync_db),
        datetime.now(),
        os.path.join(BASE_OUTPUT_DIRECTORY, SUBMISSION_ROOT_DIRECTORY),
    )


def _get_enrollments(sections: List[Section], sync_db: sqlalchemy.engine.base.Engine):
    logger.info("Extracting Enrollments from Canvas API")
    write_multi_csv(
        extract_enrollments(sections, sync_db),
        datetime.now(),
        os.path.join(BASE_OUTPUT_DIRECTORY, SECTION_ASSOCIATIONS_ROOT_DIRECTORY),
    )


def main():
    logger.info("Starting Ed-Fi LMS Canvas Extractor")
    sync_db: sqlalchemy.engine.base.Engine = get_sync_db_engine()

    (courses, _) = _get_courses(get_canvas_api(), sync_db)
    (sections, sections_df) = _get_sections(courses, sync_db)
    assignments: List[Assignment] = _get_assignments(courses, DataFrame(sections), sync_db)

    _get_students(courses, sync_db)
    _get_submissions(assignments, sync_db)
    _get_enrollments(sections, sync_db)

    logger.info("Finishing Ed-Fi LMS Canvas Extractor")

    if error_tracker.fired:
        print(
            "A fatal error occurred, please review the log output for more information.",
            file=sys.stderr,
        )
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    load_dotenv_values()
    configure_logging()
    main()
