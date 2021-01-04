# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from datetime import datetime
from typing import Dict, List, Tuple
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
from canvasapi.enrollment import Enrollment
from canvasapi.section import Section
from canvasapi.submission import Submission
from canvasapi.user import User


from canvas_extractor.api.assignments import (
    assignments_synced_as_df,
    request_assignments,
)
from canvas_extractor.api.courses import courses_synced_as_df, request_courses
from canvas_extractor.api.enrollments import (
    enrollments_synced_as_df,
    request_enrollments_for_section,
)
from canvas_extractor.api.sections import sections_synced_as_df, request_sections
from canvas_extractor.api.students import request_students, students_synced_as_df
from canvas_extractor.api.submissions import (
    request_submissions,
    submissions_synced_as_df,
)
from canvas_extractor.config import get_canvas_api, get_sync_db_engine
from canvas_extractor.mapping.assignments import map_to_udm_assignments
from canvas_extractor.mapping.users import map_to_udm_users
from canvas_extractor.mapping.sections import map_to_udm_sections
from canvas_extractor.mapping.section_associations import map_to_udm_section_associations
from canvas_extractor.mapping.submissions import map_to_udm_submissions
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


def extract_courses(
    canvas: Canvas, sync_db: sqlalchemy.engine.base.Engine
) -> List[Course]:
    logger.info("Extracting Courses from Canvas API")
    courses: List[Course] = request_courses(canvas)
    courses_df: DataFrame = courses_synced_as_df(courses, sync_db)
    # Temporary - just for demonstration until UDM mapping
    courses_df.to_csv("data/courses.csv", index=False)
    return courses


def extract_sections(
    courses: List[Course], sync_db: sqlalchemy.engine.base.Engine
) -> Tuple[List[Section], DataFrame]:
    logger.info("Extracting Sections from Canvas API")
    sections: List[Section] = request_sections(courses)
    sections_df: DataFrame = sections_synced_as_df(sections, sync_db)
    udm_sections_df: DataFrame = map_to_udm_sections(sections_df)

    sections_output_directory = os.path.join(BASE_OUTPUT_DIRECTORY, SECTIONS_ROOT_DIRECTORY)
    write_csv(udm_sections_df, datetime.now(), sections_output_directory)
    return (sections, sections_df)


def extract_students(
    courses: List[Course], sync_db: sqlalchemy.engine.base.Engine
) -> List[User]:
    logger.info("Extracting Students from Canvas API")
    students: List[User] = request_students(courses)
    students_df: DataFrame = students_synced_as_df(students, sync_db)
    udm_students_df: DataFrame = map_to_udm_users(students_df)

    users_output_directory = os.path.join(BASE_OUTPUT_DIRECTORY, USERS_ROOT_DIRECTORY)
    write_csv(udm_students_df, datetime.now(), users_output_directory)
    return students


def extract_assignments(
    courses: List[Course],
    sections_df: DataFrame,
    sync_db: sqlalchemy.engine.base.Engine,
) -> List[Assignment]:
    logger.info("Extracting Assignments from Canvas API")
    assignments: List[Assignment] = request_assignments(courses)
    assignments_df: DataFrame = assignments_synced_as_df(assignments, sync_db)
    udm_assignments_dfs: Dict[str, DataFrame] = map_to_udm_assignments(
        assignments_df, sections_df
    )

    assignments_output_directory = os.path.join(
        BASE_OUTPUT_DIRECTORY, ASSIGNMENT_ROOT_DIRECTORY
    )
    write_multi_csv(udm_assignments_dfs, datetime.now(), assignments_output_directory)
    return assignments


def extract_submissions(
    assignments: List[Assignment],
    sections: List[Section],
    sync_db: sqlalchemy.engine.base.Engine,
):
    logger.info("Extracting Submissions from Canvas API")
    export: Dict[Tuple[str, str], DataFrame] = {}
    for section in sections:
        for assignment in [
            assignment
            for assignment in assignments
            if assignment.course_id == section.course_id
        ]:
            submissions: List[Submission] = request_submissions(assignment)
            submissions_df: DataFrame = submissions_synced_as_df(submissions, sync_db)
            submissions_df = map_to_udm_submissions(submissions_df)
            export[(section.id, assignment.id)] = submissions_df

    submissions_output_directory = os.path.join(
        BASE_OUTPUT_DIRECTORY, SUBMISSION_ROOT_DIRECTORY
    )
    write_multi_tuple_csv(export, datetime.now(), submissions_output_directory)


def extract_enrollments(
    sections: List[Section], sync_db: sqlalchemy.engine.base.Engine
):
    logger.info("Extracting Enrollments from Canvas API")
    output: Dict[str, DataFrame] = dict()
    SECTION_ASSOCIATIONS_OUTPUT = os.path.join(
        BASE_OUTPUT_DIRECTORY, SECTION_ASSOCIATIONS_ROOT_DIRECTORY
    )
    for section in sections:
        enrollments: List[Enrollment] = request_enrollments_for_section(section)
        enrollments_df: DataFrame = enrollments_synced_as_df(enrollments, sync_db)
        enrollments_df = map_to_udm_section_associations(enrollments_df)
        output[section.id] = enrollments_df

    write_multi_csv(output, datetime.now(), SECTION_ASSOCIATIONS_OUTPUT)


def main():
    logger.info("Starting Ed-Fi LMS Canvas Extractor")
    sync_db: sqlalchemy.engine.base.Engine = get_sync_db_engine()

    courses: List[Course] = extract_courses(get_canvas_api(), sync_db)
    sections_df: DataFrame
    sections: Section
    (sections, sections_df) = extract_sections(courses, sync_db)
    assignments: List[Assignment] = extract_assignments(courses, sections_df, sync_db)

    extract_students(courses, sync_db)
    extract_submissions(assignments, sync_db)
    extract_enrollments(sections, sync_db)

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
