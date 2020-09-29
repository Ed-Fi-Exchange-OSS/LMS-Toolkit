# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os

from dotenv import load_dotenv

from lib import export_data
from lib.request_client import RequestClient

load_dotenv()
schoology_key = os.getenv("SCHOOLOGY_KEY")
schoology_secret = os.getenv("SCHOOLOGY_SECRET")
schoology_section_ids = os.getenv("SCHOOLOGY_SECTION_IDS")
schoology_output_path = os.getenv("SCHOOLOGY_OUTPUT_PATH")

sections_id_array = schoology_section_ids.split(',')
request_client = RequestClient(schoology_key, schoology_secret)


# export users
export_data.tocsv(request_client.get_users(), f"{schoology_output_path}/users.csv")


# export sections
sections_list = list()
for section_id in sections_id_array:
    sections_list.append(request_client.get_section_by_id(section_id))

export_data.tocsv(sections_list,
                  f"{schoology_output_path}/sections.csv")


# export assigments
export_data.tocsv(request_client.get_assignments_by_section_ids(sections_id_array),
                  f"{schoology_output_path}/assignments.csv")


# export submissions
submissions_list = list()
for section_id in sections_id_array:
    submissions_list.append(request_client.get_submissions_by_section_id(section_id))

export_data.tocsv(submissions_list,
                  f"{schoology_output_path}/submissions.csv")
