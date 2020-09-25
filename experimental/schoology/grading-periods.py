# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

"""
Retrieves a list of school grading periods in the school.
"""

import os

from dotenv import load_dotenv
import pandas as pd
import schoolopy

# TODO: find a better way. This value is set for Ed-Fi/MSDF users
# because of an internal network issue. Necessary for running PIP. But
# it messes with the commands below, so needs to be unset.
os.environ["REQUESTS_CA_BUNDLE"] = ""

load_dotenv()
api_key = os.getenv("SCHOOLOGY_KEY")
api_secret = os.getenv("SCHOOLOGY_SECRET")

sc_client = schoolopy.Schoology(schoolopy.Auth(api_key, api_secret))

df = pd.DataFrame([
    { "grading_period_id": gp.id, "title": gp.title } for gp in sc_client.get_grading_periods()
])

print (df.to_string())
