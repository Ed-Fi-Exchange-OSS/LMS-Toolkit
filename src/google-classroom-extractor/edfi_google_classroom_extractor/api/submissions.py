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
from edfi_lms_extractor_lib.api.resource_sync import (
    cleanup_after_sync,
    sync_to_db_without_cleanup,
)

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

SUBMISSIONS_RESOURCE_NAME = "StudentSubmissions"

logger = logging.getLogger(__name__)


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

    Notes
    -----
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

    logger.info("Pulling student submission data")
    submissions: List[Dict[str, str]] = []
    for course_id in course_ids:
        submissions.extend(request_submissions(resource, course_id))

    json_df: DataFrame = json_normalize(submissions).astype("string")
    return json_df.reindex(
        json_df.columns.union(REQUIRED_COLUMNS, sort=False), axis=1, fill_value=""  # type: ignore
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

    Notes
    -----
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
        CreateDate: Date this record was created by the extractor
        LastModifiedDate: Date this record was last updated by the extractor
    """

    submissions_df: DataFrame = request_latest_submissions_as_df(
        resource, course_ids
    )

    submissions_df = _sync_without_cleanup(submissions_df, sync_db)
    cleanup_after_sync(SUBMISSIONS_RESOURCE_NAME, sync_db)

    return submissions_df


def _sync_without_cleanup(
    resource_df: DataFrame, sync_db: sqlalchemy.engine.base.Engine
) -> DataFrame:
    """
    Take fetched API data and sync with database. Creates tables when necessary,
    but ok if temporary tables are there to start. Doesn't delete temporary tables when finished.

    Parameters
    ----------
    resource_df: DataFrame
        a courseworks API DataFrame with the current fetched data which
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
        identity_columns=["id", "courseId", "courseWorkId"],
        resource_name=SUBMISSIONS_RESOURCE_NAME,
        sync_db=sync_db,
    )
