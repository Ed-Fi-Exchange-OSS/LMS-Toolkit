# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os

from dotenv import load_dotenv

from helpers import export_data
from api.request_client import RequestClient

load_dotenv()
schoology_key = os.getenv("SCHOOLOGY_KEY")
schoology_secret = os.getenv("SCHOOLOGY_SECRET")
schoology_output_path = os.getenv("SCHOOLOGY_OUTPUT_PATH")
schoology_grading_periods = os.getenv("SCHOOLOGY_GRADING_PERIODS")

assert schoology_key is not None, "A `SCHOOLOGY_KEY` must be present in the .env file and it was not found."
assert schoology_secret is not None, "A `SCHOOLOGY_SECRET` must be present in the .env file and it was not found."
assert schoology_output_path is not None, "A `SCHOOLOGY_OUTPUT_PATH` must be present in the .env file and it was not found."
assert schoology_grading_periods is not None, "A `SCHOOLOGY_GRADING_PERIODS` must be present in the .env file and it was not found."


grading_periods_array = schoology_grading_periods.split(',')

request_client = RequestClient(schoology_key, schoology_secret)

# export users
users_response = request_client.get_users()
users_list = []
while True:
    users_list = users_list + users_response.current_page_items
    if users_response.get_next_page() is None:
        break

export_data.to_csv(users_list, f"{schoology_output_path}/users.csv")

# export sections

# first we need to get a list of courses
courses_response = request_client.get_courses()
courses_list = []
while True:
    courses_list = courses_list + courses_response.current_page_items
    if courses_response.get_next_page() is None:
        break

# now we can get a list of sections
course_ids = map(lambda x: x["id"], courses_list)
sections_list = request_client.get_section_by_course_ids(list(course_ids))
export_data.to_csv(sections_list,
                   f"{schoology_output_path}/sections.csv")


# export assigments
section_ids = map(lambda x: x["id"], sections_list)

assignments = request_client.get_assignments_by_section_ids(list(section_ids))

filtered_assignments = [assignment for assignment in assignments if assignment["grading_period"] in grading_periods_array]

export_data.to_csv(filtered_assignments,
                   f"{schoology_output_path}/assignments.csv")


# export submissions
submissions_list = []

for assignment in assignments:
    submissions_response = request_client.get_submissions_by_section_id_and_grade_item_id(assignment["section_id"], str(assignment["grade_item_id"]))
    while True:
        submissions_list = submissions_list + submissions_response.current_page_items
        if submissions_response.get_next_page() is None:
            break

export_data.to_csv(submissions_list,
                   f"{schoology_output_path}/submissions.csv")
