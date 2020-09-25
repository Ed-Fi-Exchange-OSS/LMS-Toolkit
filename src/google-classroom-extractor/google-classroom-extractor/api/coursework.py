# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import List, Dict
import pandas as pd
from .api_caller import call_api


def request_coursework(resource, course_id: str) -> List[Dict[str, str]]:
    return call_api(
        resource.courses().courseWork().list,
        {"courseId": course_id},
        "courseWork",
    )


def request_coursework_as_df(resource, course_ids: List[str]) -> pd.DataFrame:
    coursework: List[Dict[str, str]] = []
    for course_id in course_ids:
        coursework.extend(request_coursework(resource, course_id))

    coursework_df: pd.DataFrame = pd.json_normalize(coursework).astype("string")
    coursework_df.rename(
        columns={
            "id": "courseWorkId",
            "state": "courseWorkState",
            "title": "courseWorkTitle",
            "description": "courseWorkDescription",
            "creationTime": "courseWorkCreationTime",
            "updateTime": "courseWorkUpdateTime",
        },
        inplace=True,
    )
    coursework_df["courseWorkDueDate"] = coursework_df[
        ["dueDate.year", "dueDate.month", "dueDate.day"]
    ].agg("-".join, axis=1)
    coursework_df = coursework_df[
        [
            "courseWorkId",
            "courseWorkState",
            "courseWorkTitle",
            "courseWorkDescription",
            "courseWorkCreationTime",
            "courseWorkUpdateTime",
            "courseWorkDueDate",
        ]
    ]

    return coursework_df
