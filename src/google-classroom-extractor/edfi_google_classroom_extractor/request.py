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
from edfi_google_classroom_extractor.helpers.arg_parser import MainArguments
from .result import Result


def request_all(
    classroom_resource: Resource,
    reports_resource: Resource,
    sync_db: sqlalchemy.engine.base.Engine,
    arguments: MainArguments
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
    students_df = request_all_students_as_df(classroom_resource, course_ids, sync_db)
    teachers_df = request_all_teachers_as_df(classroom_resource, course_ids, sync_db)
    usage_df = DataFrame()
    courseworks_df = DataFrame()
    submissions_df = DataFrame()

    if arguments.extract_activities:
        usage_df = request_all_usage_as_df(
            reports_resource, sync_db, arguments.usage_start_date, arguments.usage_end_date
        )

    if arguments.extract_assignments or arguments.extract_activities:
        courseworks_df = request_all_coursework_as_df(classroom_resource, course_ids, sync_db)
        submissions_df = request_all_submissions_as_df(classroom_resource, course_ids, sync_db)

    return Result(
        usage_df,
        courses_df,
        courseworks_df,
        submissions_df,
        students_df,
        teachers_df,
    )
