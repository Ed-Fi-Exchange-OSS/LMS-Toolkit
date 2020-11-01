# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List, Dict, Optional, cast
from pandas import DataFrame, json_normalize
import sqlalchemy
from googleapiclient.discovery import Resource
from .api_caller import call_api, ResourceType

REQUIRED_COLUMNS = [
    "courseId",
    "id",
    "title",
    "description",
    "state",
    "alternateLink",
    "creationTime",
    "updateTime",
    "maxPoints",
    "workType",
    "submissionModificationMode",
    "assigneeMode",
    "creatorUserId",
    "dueDate.year",
    "dueDate.month",
    "dueDate.day",
    "dueTime.hours",
    "dueTime.minutes",
    "scheduledTime",
    "topicId",
]


def request_coursework(
    resource: Optional[Resource], course_id: str
) -> List[Dict[str, str]]:
    """
    Fetch Coursework API data for all coursework for a course,
    and return a list of coursework data

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource

    Returns
    -------
    List[Dict[str, str]]
        a list of Google Classroom Coursework resources,
            see https://developers.google.com/classroom/reference/rest/v1/courses.courseWork
    """

    if resource is None:
        return []

    return call_api(
        cast(ResourceType, resource).courses().courseWork().list,
        {"courseId": course_id},
        "courseWork",
    )


def request_latest_coursework_as_df(
    resource: Optional[Resource], course_ids: List[str]
) -> DataFrame:
    """
    Fetch Coursework API data for the given courses
        and return a Coursework API DataFrame

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource
    course_ids: List[str]
        a list of course ids to retrieve coursework for

    Returns
    -------
    DataFrame
        a Coursework API DataFrame with the fetched data

    Notes
    -----
    DataFrame columns are:
        courseId: Identifier of the course
        id: Classroom-assigned identifier of this course work, unique per course
        title: Title of this course work
        description: Optional description of this course work
        state: Status of this course work
        alternateLink: Absolute link to this course work in the Classroom web UI
        creationTime: Timestamp when this course work was created
        updateTime: Timestamp of the most recent change to this course work
        maxPoints: Maximum grade for this course work
        workType: Type of this course work
        submissionModificationMode: Setting to determine when students are allowed
            to modify submissions
        assigneeMode: Assignee mode of the coursework
        creatorUserId: Identifier for the user that created the coursework
        dueDate.year: Optional year, in UTC, that submissions are due
        dueDate.month: Optional month, in UTC, that submissions are due
        dueDate.day: Optional day, in UTC, that submissions are due
        dueTime.hours: Optional hour, in UTC, that submissions are due
        dueTime.minutes: Optional minute, in UTC, that submissions are due
        scheduledTime: Optional timestamp when this course work is scheduled to be published
        topicId: Identifier for the topic that this coursework is associated with
    """

    logging.info("Pulling coursework data")
    coursework: List[Dict[str, str]] = []
    for course_id in course_ids:
        coursework.extend(request_coursework(resource, course_id))

    json_df: DataFrame = json_normalize(coursework).astype("string")
    return json_df.reindex(
        json_df.columns.union(REQUIRED_COLUMNS, sort=False), axis=1, fill_value=""
    )


def request_all_coursework_as_df(
    resource: Optional[Resource],
    course_ids: List[str],
    sync_db: sqlalchemy.engine.base.Engine,
) -> DataFrame:
    """
    Fetch Coursework API data for all courses and return a Coursework API DataFrame

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource
    course_ids: List[str]
        a list of course ids to retrieve coursework for
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a Coursework API DataFrame with the current and previously fetched data

    Notes
    -----
    DataFrame columns are:
        courseId: Identifier of the course
        id: Classroom-assigned identifier of this course work, unique per course
        title: Title of this course work
        description: Optional description of this course work
        state: Status of this course work
        alternateLink: Absolute link to this course work in the Classroom web UI
        creationTime: Timestamp when this course work was created
        updateTime: Timestamp of the most recent change to this course work
        maxPoints: Maximum grade for this course work
        workType: Type of this course work
        submissionModificationMode: Setting to determine when students are allowed
            to modify submissions
        assigneeMode: Assignee mode of the coursework
        creatorUserId: Identifier for the user that created the coursework
        dueDate.year: Optional year, in UTC, that submissions are due
        dueDate.month: Optional month, in UTC, that submissions are due
        dueDate.day: Optional day, in UTC, that submissions are due
        dueTime.hours: Optional hour, in UTC, that submissions are due
        dueTime.minutes: Optional minute, in UTC, that submissions are due
        scheduledTime: Optional timestamp when this course work is scheduled to be published
        topicId: Identifier for the topic that this coursework is associated with
    """

    coursework_df: DataFrame = request_latest_coursework_as_df(resource, course_ids)

    # append everything from API call
    coursework_df.to_sql(
        "Coursework", sync_db, if_exists="append", index=False, chunksize=500
    )
    # remove duplicates - leave only the most recent
    with sync_db.connect() as con:
        con.execute(
            "DELETE from Coursework "
            "WHERE rowid not in (select max(rowid) "
            "FROM Coursework "
            "GROUP BY id)"
        )

    return coursework_df
