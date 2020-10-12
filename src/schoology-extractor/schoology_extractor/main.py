# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import os
from typing import Any, List
import sys

from dotenv import load_dotenv
import pandas as pd

from helpers import export_data
from api.request_client import RequestClient
from helpers import arg_parser
from mapping import users as usersMap

# Parse arguments
arguments = arg_parser.parse_main_arguments(sys.argv[1:])
# Parameters are validated in the parse_main_arguments function
schoology_key = arguments.client_key
schoology_secret = arguments.client_secret
schoology_output_path = arguments.output_directory
schoology_grading_periods = arguments.grading_period
log_level = arguments.log_level


# Configure logging
logFormatter = '%(asctime)s - %(levelname)s - %(message)s'

logging.basicConfig(
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
    format=logFormatter,
    level=log_level
)

logger = logging.getLogger(__name__)
logger.info("Starting Ed-Fi LMS Schoology Extractor")

# Init variables
grading_periods_array = schoology_grading_periods.split(",")
request_client = RequestClient(schoology_key, schoology_secret)


# Export users
logger.info("Exporting users")
try:
    users_response = request_client.get_users()
    users_list: List[Any] = []
    while True:
        users_list = users_list + users_response.current_page_items
        if users_response.get_next_page() is None:
            break

    roles_list: List[Any] = []
    roles_response = request_client.get_roles()
    while True:
        roles_list = roles_list + roles_response.current_page_items
        if roles_response.get_next_page() is None:
            break

    users_df = pd.DataFrame(users_list)
    roles_df = pd.DataFrame(roles_list)

    udm_users = usersMap.map_to_udm(users_df, roles_df)

    export_data.df_to_csv(udm_users, os.path.join(schoology_output_path, "users.csv"))
except Exception as ex:
    logger.error('An exception has occurred in the process of generating the users.csv file: %s', ex)


# Export sections
logger.info("Exporting sections")
sections_list = []
try:
    # first we need to get a list of courses
    logger.info("Exporting sections - Getting courses")
    courses_response = request_client.get_courses()
    courses_list: List[Any] = []
    while True:
        courses_list = courses_list + courses_response.current_page_items
        if courses_response.get_next_page() is None:
            break

    # now we can get a list of sections
    course_ids = map(lambda x: x["id"], courses_list)
    sections_list = request_client.get_section_by_course_ids(list(course_ids))
    export_data.to_csv(sections_list, os.path.join(schoology_output_path, "sections.csv"))
except Exception as ex:
    logger.error('An exception has occurred in the process of generating the sections.csv file: %s', ex)


# Export assigments
logger.info("Exporting assigments")
assignments = []
try:
    section_ids = map(lambda x: x["id"], sections_list)

    assignments = request_client.get_assignments_by_section_ids(list(section_ids))

    filtered_assignments = [
        assignment
        for assignment in assignments
        if assignment["grading_period"] in grading_periods_array
    ]

    export_data.to_csv(
        filtered_assignments, os.path.join(schoology_output_path, "assignments.csv")
    )
except Exception as ex:
    logger.error('An exception has occurred in the process of generating the assigments.csv file: %s', ex)


# Export submissions
logger.info("Exporting submissions")
try:
    submissions_list: List[Any] = []

    for assignment in assignments:
        submissions_response = (
            request_client.get_submissions_by_section_id_and_grade_item_id(
                assignment["section_id"], str(assignment["grade_item_id"])
            )
        )
        while True:
            submissions_list = submissions_list + submissions_response.current_page_items
            if submissions_response.get_next_page() is None:
                break

    export_data.to_csv(
        submissions_list, os.path.join(schoology_output_path, "submissions.csv")
    )
except Exception as ex:
    logger.error('An exception has occurred in the process of generating the submissions.csv file: %s', ex)
