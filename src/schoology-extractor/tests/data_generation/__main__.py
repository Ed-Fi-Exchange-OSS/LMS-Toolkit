# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from sys import stdout, argv

from dotenv import load_dotenv
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
from schoology_extractor.api.request_client import RequestClient
from schoology_extractor.helpers import arg_parser

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
enrollments = []
try:
    enrollments = generate_and_load_enrollments(
        request_client=request_client,
        users_per_section_count=NUMBER_OF_USERS_PER_SECTION,
        sections=sections,
        users=users,
    )
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
