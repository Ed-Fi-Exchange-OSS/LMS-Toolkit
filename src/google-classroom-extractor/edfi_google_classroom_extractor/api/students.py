# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List, Dict, Optional, cast
from pandas import DataFrame, json_normalize
import sqlalchemy
from googleapiclient.discovery import Resource
from edfi_google_classroom_extractor.api.api_caller import call_api, ResourceType
from edfi_lms_extractor_lib.api.resource_sync import (
    cleanup_after_sync,
    sync_to_db_without_cleanup,
)

STUDENTS_RESOURCE_NAME = "Students"

logger = logging.getLogger(__name__)


def request_students(
    resource: Optional[Resource], course_id: str
) -> List[Dict[str, str]]:
    """
    Fetch Students API data for a course and return a list of student data

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource
    course_ids: str
        a Google Classroom course id as a string

    Returns
    -------
    List[Dict[str, str]]
        a list of Google Classroom Student resources,
            see https://developers.google.com/classroom/reference/rest/v1/courses.students
    """

    if resource is None:
        return []

    return call_api(
        cast(ResourceType, resource).courses().students().list,
        {"courseId": course_id},
        "students",
    )


def request_latest_students_as_df(
    resource: Optional[Resource], course_ids: List[str]
) -> DataFrame:
    """
    Fetch Students API data for a range of courses and return a Students API DataFrame

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource or None
    course_ids: List[str]
        a list of Google Classroom course ids as a string array

    Returns
    -------
    DataFrame
        a Students API DataFrame with the fetched data

    Notes
    -----
    DataFrame columns are:
        courseId: Identifier of the course
        userId: Identifier of the user
        profile.id: Identifier of the user
        profile.name.givenName: The user's first name
        profile.name.familyName: The user's last name
        profile.name.fullName: The user's full name formed by concatenating the first and last name values
        profile.emailAddress: Email address of the user
    """

    logger.info("Pulling student data")
    students: List[Dict[str, str]] = []
    for course_id in course_ids:
        students.extend(request_students(resource, course_id))

    return json_normalize(students).astype("string")


def request_all_students_as_df(
    resource: Optional[Resource],
    course_ids: List[str],
    sync_db: sqlalchemy.engine.base.Engine,
) -> DataFrame:
    """
    Fetch Students API data for a range of courses and return a Students API DataFrame
    with current and previously fetched data

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource or None
    course_ids: List[str]
        a list of Google Classroom course ids as a string array
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a Students API DataFrame with the current and previously fetched data

    Notes
    -----
    DataFrame columns are:
        courseId: Identifier of the course
        userId: Identifier of the user
        profile.id: Identifier of the user
        profile.name.givenName: The user's first name
        profile.name.familyName: The user's last name
        profile.name.fullName: The user's full name formed by concatenating the first and last name values
        profile.emailAddress: Email address of the user
    """

    students_df: DataFrame = request_latest_students_as_df(resource, course_ids)
    students_df = _sync_without_cleanup(students_df, sync_db)
    cleanup_after_sync(STUDENTS_RESOURCE_NAME, sync_db)

    return students_df


def _sync_without_cleanup(
    resource_df: DataFrame, sync_db: sqlalchemy.engine.base.Engine
) -> DataFrame:
    """
    Take fetched API data and sync with database. Creates tables when necessary,
    but ok if temporary tables are there to start. Doesn't delete temporary tables when finished.

    Parameters
    ----------
    resource_df: DataFrame
        a Students API DataFrame with the current fetched data which
        will be mutated, adding Hash and CreateDate/LastModifiedDate
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a DataFrame with current fetched data and reconciled CreateDate/LastModifiedDate
    """
    return sync_to_db_without_cleanup(
        resource_df=resource_df,
        identity_columns=["userId", "courseId"],
        resource_name=STUDENTS_RESOURCE_NAME,
        sync_db=sync_db,
    )
