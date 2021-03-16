# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from sys import stdout, argv

from dotenv import load_dotenv
from tests.data_generation.discussion_comments import (
    generate_and_load_discussion_comments,
    rollback_loaded_discussion_comments,
)
from tests.data_generation.discussions import (
    generate_and_load_discussions,
    rollback_loaded_discussions,
)
from tests.data_generation.assignments import (
    generate_and_load_assignments,
    generate_extra_assignments_without_enrollments,
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
from tests.data_generation.gradingperiods import get_gradingperiods
from tests.data_generation.courses import (
    generate_and_load_courses,
    rollback_loaded_courses,
)
from tests.data_generation.users import generate_and_load_users, rollback_loaded_users
from edfi_schoology_extractor.api.request_client import RequestClient
from edfi_schoology_extractor.helpers import arg_parser

load_dotenv()
arguments = arg_parser.parse_main_arguments(argv[1:])

logging.basicConfig(
    handlers=[
        logging.StreamHandler(stdout),
    ],
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level="INFO",
)
logger = logging.getLogger(__name__)

request_client: RequestClient = RequestClient(
    arguments.client_key, arguments.client_secret
)


grading_periods = []
try:
    grading_periods = get_gradingperiods(request_client)
except Exception as ex:
    logger.exception(ex)


NUMBER_OF_USERS = 5
users = []
try:
    users = generate_and_load_users(request_client, NUMBER_OF_USERS)
except Exception as ex:
    logger.exception(ex)


NUMBER_OF_COURSES = 5
courses = []
try:
    courses = generate_and_load_courses(request_client, NUMBER_OF_COURSES)
except Exception as ex:
    logger.exception(ex)


NUMBER_OF_SECTIONS_PER_COURSE = 3
sections = []
try:
    sections = generate_and_load_sections(
        request_client=request_client,
        record_count=NUMBER_OF_SECTIONS_PER_COURSE,
        courses=courses,
        grading_periods=grading_periods,
    )
except Exception as ex:
    logger.exception(ex)

NUMBER_OF_USERS_PER_SECTION = 3
enrollments = {}
try:
    enrollments = generate_and_load_enrollments(
        request_client=request_client,
        users_per_section_count=NUMBER_OF_USERS_PER_SECTION,
        sections=sections,
        users=users,
    )
except Exception as ex:
    logger.exception(ex)


NUMBER_OF_ASSIGNMENTS_PER_SECTION = 2
assignments = {}
try:
    assignments = generate_and_load_assignments(
        request_client=request_client,
        assignment_per_section_count=NUMBER_OF_ASSIGNMENTS_PER_SECTION,
        enrollments=enrollments,
    )
except Exception as ex:
    logger.exception(ex)


NUMBER_OF_DISCUSSIONS_PER_ASSIGNMENT = 2
discussions = {}
try:
    discussions = generate_and_load_discussions(
        request_client=request_client,
        discussions_per_assignment_count=NUMBER_OF_DISCUSSIONS_PER_ASSIGNMENT,
        assignments=assignments,
    )
except Exception as ex:
    logger.exception(ex)


NUMBER_OF_DISCUSSION_COMMENTS_PER_DISCUSSION = 3
discussion_comments = {}
try:
    discussion_comments = generate_and_load_discussion_comments(
        request_client=request_client,
        discussion_comments_per_discussion_count=NUMBER_OF_DISCUSSION_COMMENTS_PER_DISCUSSION,
        discussions=discussions,
        enrollments=enrollments,
    )
except Exception as ex:
    logger.exception(ex)


# **** Rollback section from here to end of file. Comment out to prevent rollbacks.

try:
    rollback_loaded_discussion_comments(request_client, discussion_comments)
except Exception as ex:
    logger.exception(ex)


try:
    rollback_loaded_discussions(request_client, discussions)
except Exception as ex:
    logger.exception(ex)


try:
    rollback_loaded_assignments(request_client, assignments)
except Exception as ex:
    logger.exception(ex)


try:
    rollback_loaded_enrollments(request_client, enrollments)
except Exception as ex:
    logger.exception(ex)


try:
    rollback_loaded_sections(request_client, sections)
except Exception as ex:
    logger.exception(ex)


try:
    rollback_loaded_courses(request_client, courses)
except Exception as ex:
    logger.exception(ex)


try:
    rollback_loaded_users(request_client, users)
except Exception as ex:
    logger.exception(ex)


"""
The following block of code was used to generate additional assignments for
every section.
"""
#
# courses = request_client.get_courses(200)
#
# sections = []
# for c in courses.get_all_pages():
#     section_page = request_client.get_section_by_course_id(c['id'], 200)
#     sections += section_page.get_all_pages()
#
# assignments = {}
# try:
#     assignments = generate_extra_assignments_without_enrollments(
#         request_client,
#         sections
#     )
# except Exception as ex:
#     logger.exception(ex)
"""
END
"""
