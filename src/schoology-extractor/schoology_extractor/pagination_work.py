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

request_client = RequestClient(schoology_key, schoology_secret)


# export users
response_object = request_client.get_users()
print(response_object.current_page_items)
print('--------divider--------')
response_object.get_next_page()
print(response_object.current_page_items)
