# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List, Dict, Optional, cast
import pandas as pd  # type: ignore
from sqlalchemy.engine.base import Engine as saEngine  # type: ignore
from googleapiclient.discovery import Resource  # type: ignore
from .api_caller import call_api, ResourceType


def request_teachers(
    resource: Optional[Resource], course_id: str
) -> List[Dict[str, str]]:
    """
    Fetch Teachers API data for a course and return a list of teacher data

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource
    course_ids: str
        a Google Classroom course id as a string

    Returns
    -------
    List[Dict[str, str]]
        a list of Google Classroom Teacher resources,
            see https://developers.google.com/classroom/reference/rest/v1/courses.teachers

    DataFrame columns are:
        courseId: Identifier of the course
        userId: Identifier of the user
        profile.id: Identifier of the user
        profile.name.givenName: The user's first name
        profile.name.familyName: The user's last name
        profile.name.fullName: The user's full name formed by concatenating the first and last name values
        profile.emailAddress: Email address of the user
    """

    assert isinstance(resource, Resource) or resource is None
    assert isinstance(course_id, str)

    if resource is None:
        return []

    return call_api(
        cast(ResourceType, resource).courses().teachers().list,
        {"courseId": course_id},
        "teachers",
    )


def request_latest_teachers_as_df(
    resource: Optional[Resource], course_ids: List[str]
) -> pd.DataFrame:
    """
    Fetch Teachers API data for a range of courses and return a Teachers API DataFrame

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource or None
    course_ids: List[str]
        a list of Google Classroom course ids as a string array

    Returns
    -------
    DataFrame
        a Teachers API DataFrame with the fetched data

    DataFrame columns are:
        courseId: Identifier of the course
        userId: Identifier of the user
        profile.id: Identifier of the user
        profile.name.givenName: The user's first name
        profile.name.familyName: The user's last name
        profile.name.fullName: The user's full name formed by concatenating the first and last name values
        profile.emailAddress: Email address of the user
    """

    assert isinstance(resource, Resource) or resource is None
    assert isinstance(course_ids, list)

    logging.info("Pulling teacher data")
    teachers: List[Dict[str, str]] = []
    for course_id in course_ids:
        teachers.extend(request_teachers(resource, course_id))

    return pd.json_normalize(teachers).astype("string")


def request_all_teachers_as_df(
    resource: Optional[Resource],
    course_ids: List[str],
    sync_db: saEngine,
) -> pd.DataFrame:
    """
    Fetch Teachers API data for a range of courses and return a Teachers API DataFrame
    with current and previously fetched data

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource or None
    course_ids: List[str]
        a list of Google Classroom course ids as a string array
    sync_db: saEngine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a Teachers API DataFrame with the current and previously fetched data

    DataFrame columns are:
        courseId: Identifier of the course
        userId: Identifier of the user
        profile.id: Identifier of the user
        profile.name.givenName: The user's first name
        profile.name.familyName: The user's last name
        profile.name.fullName: The user's full name formed by concatenating the first and last name values
        profile.emailAddress: Email address of the user
    """

    assert isinstance(resource, Resource) or resource is None
    assert isinstance(course_ids, list)
    assert isinstance(sync_db, saEngine)

    teachers_df: pd.DataFrame = request_latest_teachers_as_df(resource, course_ids)

    # append everything from API call
    teachers_df.to_sql(
        "Teachers", sync_db, if_exists="append", index=False, chunksize=500
    )
    # remove duplicates - leave only the most recent
    with sync_db.connect() as con:
        con.execute(
            "DELETE from Teachers "
            "WHERE rowid not in (select max(rowid) "
            "FROM Teachers "
            "GROUP BY courseId, userId)"
        )

    return teachers_df
