# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from sys import stdout
import sys
from typing import Dict, List
from canvasapi import Canvas
from canvasapi.account import Account
from canvasapi.assignment import Assignment
from canvasapi.course import Course
from canvasapi.enrollment import Enrollment
from canvasapi.section import Section
from canvasapi.user import User
from dotenv import load_dotenv

from edfi_canvas_extractor.api.api_caller import call_with_retry
from edfi_canvas_extractor.helpers import arg_parser
from edfi_canvas_extractor.config import get_canvas_api
from tests.data_generation.helpers import flatten_dict_of_lists

from tests.data_generation.assignments import (
    generate_and_load_assignments,
    rollback_loaded_assignments,
)
from tests.data_generation.enrollments import (
    generate_and_load_enrollments,
    rollback_loaded_enrollments,
)
from tests.data_generation.sections import (
    generate_and_load_sections,
    rollback_loaded_sections,
)
from tests.data_generation.courses import (
    generate_and_load_courses,
    rollback_loaded_courses,
)

from tests.data_generation.users import generate_and_load_users, rollback_loaded_users

load_dotenv()

logging.basicConfig(
    handlers=[
        logging.StreamHandler(stdout),
    ],
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level="INFO",
)
logger = logging.getLogger(__name__)
arguments = arg_parser.parse_main_arguments(sys.argv[1:])

canvas: Canvas = get_canvas_api(arguments.base_url, arguments.access_token)
account: Account = call_with_retry(canvas.get_accounts)[0]


NUMBER_OF_USERS = 2
users: List[User] = []
try:
    users = generate_and_load_users(account, NUMBER_OF_USERS)
except Exception as ex:
    logger.exception(ex)


NUMBER_OF_COURSES = 2
courses: List[Course] = []
try:
    courses = generate_and_load_courses(account, NUMBER_OF_COURSES)
except Exception as ex:
    logger.exception(ex)


NUMBER_OF_SECTIONS_PER_COURSE = 2
sections_by_course: Dict[Course, List[Section]] = {}
try:
    sections_by_course = generate_and_load_sections(courses, NUMBER_OF_SECTIONS_PER_COURSE)
except Exception as ex:
    logger.exception(ex)


NUMBER_OF_USERS_PER_COURSE = 2
enrollments_by_course: Dict[Course, List[Enrollment]] = {}
try:
    enrollments_by_course = generate_and_load_enrollments(
        users,
        sections_by_course,
        NUMBER_OF_USERS_PER_COURSE,
    )
except Exception as ex:
    logger.exception(ex)


NUMBER_OF_ASSIGNMENTS_PER_COURSE = 2
assignments_by_course: Dict[Course, List[Assignment]] = {}
try:
    assignments_by_course = generate_and_load_assignments(courses, NUMBER_OF_ASSIGNMENTS_PER_COURSE)
except Exception as ex:
    logger.exception(ex)


# **** Rollback section from here to end of file. Comment out to prevent rollbacks.

try:
    rollback_loaded_assignments(flatten_dict_of_lists(assignments_by_course))
except Exception as ex:
    logger.exception(ex)


try:
    rollback_loaded_enrollments(flatten_dict_of_lists(enrollments_by_course))
except Exception as ex:
    logger.exception(ex)


try:
    rollback_loaded_sections(flatten_dict_of_lists(sections_by_course))
except Exception as ex:
    logger.exception(ex)


try:
    rollback_loaded_courses(courses)
except Exception as ex:
    logger.exception(ex)


try:
    rollback_loaded_users(account, users)
except Exception as ex:
    logger.exception(ex)
