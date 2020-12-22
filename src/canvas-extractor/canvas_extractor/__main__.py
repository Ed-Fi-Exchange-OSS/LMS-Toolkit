# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import List
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


from canvas_extractor.api.assignments import assignments_synced_as_df, request_assignments
from canvas_extractor.api.courses import courses_synced_as_df, request_courses
from canvas_extractor.api.enrollments import enrollments_synced_as_df, request_enrollments
from canvas_extractor.api.sections import sections_synced_as_df, request_sections
from canvas_extractor.api.students import request_students, students_synced_as_df
from canvas_extractor.api.submissions import request_submissions, submissions_synced_as_df
from canvas_extractor.config import get_canvas_api, get_sync_db_engine
from canvas_extractor.mapping import users as mapUsers
from canvas_extractor.mapping.sections import map_to_udm_sections

logger: logging.Logger
error_tracker: ErrorHandler


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


def extract_courses(canvas: Canvas, sync_db: sqlalchemy.engine.base.Engine) -> List[Course]:
    logger.info("Extracting Courses from Canvas API")
    courses: List[Course] = request_courses(canvas)
    courses_df: DataFrame = courses_synced_as_df(courses, sync_db)
    # Temporary - just for demonstration until UDM mapping
    courses_df.to_csv("data/courses.csv", index=False)
    return courses


def extract_sections(courses: List[Course], sync_db: sqlalchemy.engine.base.Engine) -> List[Section]:
    logger.info("Extracting Sections from Canvas API")
    sections: List[Section] = request_sections(courses)
    sections_df: DataFrame = sections_synced_as_df(sections, sync_db)
    udm_sections_df: DataFrame = map_to_udm_sections(sections_df)

    # Temporary - just for demonstration until UDM mapping
    udm_sections_df.to_csv("data/udm_sections.csv", index=False)
    return sections


def extract_students(courses: List[Course], sync_db: sqlalchemy.engine.base.Engine) -> List[User]:
    logger.info("Extracting Students from Canvas API")
    students: List[User] = request_students(courses)
    students_df: DataFrame = students_synced_as_df(students, sync_db)
    students_df = mapUsers.map_to_udm(students_df)
    # Temporary - just for demonstration until UDM mapping
    students_df.to_csv("data/students.csv", index=False)
    return students


def extract_assignments(courses: List[Course], sync_db: sqlalchemy.engine.base.Engine) -> List[Assignment]:
    logger.info("Extracting Assignments from Canvas API")
    assignments: List[Assignment] = request_assignments(courses)
    assignments_df: DataFrame = assignments_synced_as_df(assignments, sync_db)
    # Temporary - just for demonstration until UDM mapping
    assignments_df.to_csv("data/assignments.csv", index=False)
    return assignments


def extract_submissions(assignments: List[Assignment], sync_db: sqlalchemy.engine.base.Engine) -> List[Submission]:
    logger.info("Extracting Submissions from Canvas API")
    submissions: List[Submission] = request_submissions(assignments)
    submissions_df: DataFrame = submissions_synced_as_df(submissions, sync_db)
    # Temporary - just for demonstration until UDM mapping
    submissions_df.to_csv("data/submissions.csv", index=False)
    return submissions


def extract_enrollments(students: List[User], sync_db: sqlalchemy.engine.base.Engine) -> List[Enrollment]:
    logger.info("Extracting Enrollments from Canvas API")
    enrollments: List[Enrollment] = request_enrollments(students)
    enrollments_df: DataFrame = enrollments_synced_as_df(enrollments, sync_db)
    # Temporary - just for demonstration until UDM mapping
    enrollments_df.to_csv("data/enrollments.csv", index=False)
    return enrollments


def main():
    logger.info("Starting Ed-Fi LMS Canvas Extractor")
    sync_db: sqlalchemy.engine.base.Engine = get_sync_db_engine()

    courses: List[Course] = extract_courses(get_canvas_api(), sync_db)
    extract_sections(courses, sync_db)
    students: List[User] = extract_students(courses, sync_db)
    assignments: List[Assignment] = extract_assignments(courses, sync_db)
    extract_submissions(assignments, sync_db)
    extract_enrollments(students, sync_db)

    logger.info("Finishing Ed-Fi LMS Google Classroom Extractor")

    if error_tracker.fired:
        print("A fatal error occurred, please review the log output for more information.", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    load_dotenv()
    configure_logging()
    main()
