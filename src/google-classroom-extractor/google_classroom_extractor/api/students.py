# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List, Dict, Optional, cast
import pandas as pd
import sqlalchemy
from googleapiclient.discovery import Resource
from .api_caller import call_api, ResourceType


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

    assert isinstance(resource, Resource) or resource is None
    assert isinstance(course_id, str)

    if resource is None:
        return []

    return call_api(
        cast(ResourceType, resource).courses().students().list,
        {"courseId": course_id},
        "students",
    )


def request_latest_students_as_df(
    resource: Optional[Resource], course_ids: List[str]
) -> pd.DataFrame:
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

    logging.info("Pulling student data")
    students: List[Dict[str, str]] = []
    for course_id in course_ids:
        students.extend(request_students(resource, course_id))

    return pd.json_normalize(students).astype("string")


def request_all_students_as_df(
    resource: Optional[Resource],
    course_ids: List[str],
    sync_db: sqlalchemy.engine.base.Engine,
) -> pd.DataFrame:
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
    assert isinstance(sync_db, sqlalchemy.engine.base.Engine)

    students_df: pd.DataFrame = request_latest_students_as_df(resource, course_ids)

    # append everything from API call
    students_df.to_sql(
        "Students", sync_db, if_exists="append", index=False, chunksize=500
    )
    # remove duplicates - leave only the most recent
    with sync_db.connect() as con:
        con.execute(
            "DELETE from Students "
            "WHERE rowid not in (select max(rowid) "
            "FROM Students "
            "GROUP BY courseId, userId)"
        )

    return students_df
