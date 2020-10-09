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
    "courseWorkId",
    "id",
    "userId",
    "creationTime",
    "updateTime",
    "state",
    "late",
    "draftGrade",
    "assignedGrade",
    "alternateLink",
    "courseWorkType",
    "associatedWithDeveloper",
    "submissionHistory",
]


def request_submissions(
    resource: Optional[Resource], course_id: str
) -> List[Dict[str, str]]:
    """
    Fetch Student Submissions API data for all submissions for a coursework,
    and return a list of submissions data

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource

    Returns
    -------
    List[Dict[str, str]]
        a list of Google Classroom StudentSubmissions resources,
            see https://developers.google.com/classroom/reference/rest/v1/courses.courseWork.studentSubmissions
    """
    assert isinstance(resource, Resource) or resource is None
    assert isinstance(course_id, str)

    if resource is None:
        return []

    return call_api(
        cast(ResourceType, resource).courses().courseWork().studentSubmissions().list,
        {"courseId": course_id, "courseWorkId": "-"},
        "studentSubmissions",
    )


def request_latest_submissions_as_df(
    resource: Optional[Resource], course_ids: List[str]
) -> DataFrame:
    """
    Fetch StudentSubmissions API data for the given coursework
        and return a StudentSubmissions API DataFrame

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

    DataFrame columns are:
        courseId: Identifier of the course
        courseWorkId: Identifier for the course work this corresponds to
        id: Classroom-assigned Identifier for the student submission, unique
        per coursework
        userId: Identifier for the student that owns this submission
        creationTime: Creation time of this submission
        updateTime: Last update time of this submission
        title: Title of this course work
        description: Optional description of this course work
        state: Status of this submission
        late: Whether this submission is late
        draftGrade: Optional pending grade. If unset, no grade was set. Decimal
            values are allowed.
        assignedGrade: Optional grade. If unset, no grade was set. Decimal
            values are allowed.
        alternateLink: Absolute link to this course work in the Classroom web UI
        courseWorkType: Type of course work this submission is for
        associatedWithDeveloper: Whether this student submission is associated with the
            Developer Console project making the request
        submissionHistory: The history of the submission as JSON
    """
    assert isinstance(resource, Resource) or resource is None
    assert isinstance(course_ids, list)

    logging.info("Pulling student submission data")
    submissions: List[Dict[str, str]] = []
    for course_id in course_ids:
        submissions.extend(request_submissions(resource, course_id))

    json_df: DataFrame = json_normalize(submissions).astype("string")
    return json_df.reindex(
        json_df.columns.union(REQUIRED_COLUMNS, sort=False), axis=1, fill_value=""
    )


def request_all_submissions_as_df(
    resource: Optional[Resource],
    course_ids: List[str],
    sync_db: sqlalchemy.engine.base.Engine,
) -> DataFrame:
    """
    Fetch StudentSubmissions API data for the given coursework
        and return a StudentSubmissions API DataFrame

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

    DataFrame columns are:
        courseId: Identifier of the course
        courseWorkId: Identifier for the course work this corresponds to
        id: Classroom-assigned Identifier for the student submission, unique
        per coursework
        userId: Identifier for the student that owns this submission
        creationTime: Creation time of this submission
        updateTime: Last update time of this submission
        state: Status of this submission
        late: Whether this submission is late
        draftGrade: Optional pending grade. If unset, no grade was set. Decimal
            values are allowed.
        assignedGrade: Optional grade. If unset, no grade was set. Decimal
            values are allowed.
        alternateLink: Absolute link to this course work in the Classroom web UI
        courseWorkType: Type of course work this submission is for
        associatedWithDeveloper: Whether this student submission is associated with the
            Developer Console project making the request
        submissionHistory: The history of the submission as JSON
    """
    assert isinstance(resource, Resource) or resource is None
    assert isinstance(course_ids, list)
    assert isinstance(sync_db, sqlalchemy.engine.base.Engine)

    submissions_df: DataFrame = request_latest_submissions_as_df(
        resource, course_ids
    )

    # append everything from API call
    submissions_df.to_sql(
        "StudentSubmissions", sync_db, if_exists="append", index=False, chunksize=500
    )
    # remove duplicates - leave only the most recent
    with sync_db.connect() as con:
        con.execute(
            "DELETE from StudentSubmissions "
            "WHERE rowid not in (select max(rowid) "
            "FROM StudentSubmissions "
            "GROUP BY id)"
        )

    return submissions_df
