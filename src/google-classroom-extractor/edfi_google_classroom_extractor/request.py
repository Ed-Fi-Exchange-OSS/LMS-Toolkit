# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import List
from pandas import DataFrame
from googleapiclient.discovery import Resource
import sqlalchemy

from edfi_google_classroom_extractor.api.courses import request_all_courses_as_df
from edfi_google_classroom_extractor.api.coursework import request_all_coursework_as_df
from edfi_google_classroom_extractor.api.students import request_all_students_as_df
from edfi_google_classroom_extractor.api.teachers import request_all_teachers_as_df
from edfi_google_classroom_extractor.api.submissions import request_all_submissions_as_df
from edfi_google_classroom_extractor.api.usage import request_all_usage_as_df
from .result import Result


def request_all(
    classroom_resource: Resource,
    reports_resource: Resource,
    sync_db: sqlalchemy.engine.base.Engine,
    env_usage_start_date: str,
    env_usage_end_date: str,
) -> Result:
    """
    Fetch from all API endpoints and return DataFrames for each

    Parameters
    ----------
    classroom_resource: Resource
        a Google Classroom SDK Resource
    reports_resource: Resource
        a Google Reports SDK Resource
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    Result
        a simple collection of all fetched API DataFrames
    """
    courses_df: DataFrame = request_all_courses_as_df(classroom_resource, sync_db)
    course_ids: List[str] = courses_df["id"].tolist()

    return Result(
        request_all_usage_as_df(
            reports_resource, sync_db, env_usage_start_date, env_usage_end_date
        ),
        courses_df,
        request_all_coursework_as_df(classroom_resource, course_ids, sync_db),
        request_all_submissions_as_df(classroom_resource, course_ids, sync_db),
        request_all_students_as_df(classroom_resource, course_ids, sync_db),
        request_all_teachers_as_df(classroom_resource, course_ids, sync_db),
    )
