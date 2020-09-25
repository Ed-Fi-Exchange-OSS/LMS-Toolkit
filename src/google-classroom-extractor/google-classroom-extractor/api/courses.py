# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import List, Dict
import pandas as pd
from .api_caller import call_api


def request_courses(resource) -> List[Dict[str, str]]:
    return call_api(
        resource.courses().list,
        {"courseStates": ["ACTIVE"]},
        "courses",
    )


def request_courses_as_df(resource) -> pd.DataFrame:
    courses: List[Dict[str, str]] = request_courses(resource)
    courses_df: pd.DataFrame = pd.json_normalize(courses)[["id", "name"]]
    courses_df.rename(columns={"id": "courseId", "name": "courseName"}, inplace=True)
    return courses_df.astype("string")
