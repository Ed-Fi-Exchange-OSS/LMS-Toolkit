# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List, Dict, Optional, cast
from pandas import DataFrame, json_normalize
import sqlalchemy
from googleapiclient.discovery import Resource
from google_classroom_extractor.api.api_caller import call_api, ResourceType
from google_classroom_extractor.api.resource_sync import (
    cleanup_after_sync,
    sync_to_db_without_cleanup,
)

logger = logging.getLogger(__name__)


def request_courses(resource: Optional[Resource]) -> List[Dict[str, str]]:
    """
    Fetch Course API data for all courses and return a list of course data

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource

    Returns
    -------
    List[Dict[str, str]]
        a list of Google Classroom Course resources,
            see https://developers.google.com/classroom/reference/rest/v1/courses
    """

    if resource is None:
        return []

    return call_api(
        cast(ResourceType, resource).courses().list,
        {},
        "courses",
    )


def request_latest_courses_as_df(resource: Optional[Resource]) -> DataFrame:
    """
    Fetch Course API data for all courses and return a Courses API DataFrame

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource

    Returns
    -------
    DataFrame
        a Courses API DataFrame with the fetched data

    Notes
    -----
    DataFrame columns are:
        id: Identifier for this course assigned by Classroom
        name: Name of the course
        section: Section of the course
        descriptionHeading: Optional heading for the description
        description: Optional description
        room: Optional room location
        ownerId: The identifier of the owner of a course
        creationTime: Creation time of the course
        updateTime: Time of the most recent update to this course
        enrollmentCode: Enrollment code to use when joining this course
        courseState: State of the course
        alternateLink: Absolute link to this course in the Classroom web UI
        teacherGroupEmail: The email address of a Google group containing all teachers of the course
        courseGroupEmail: The email address of a Google group containing all members of the course
        guardiansEnabled: Whether or not guardian notifications are enabled for this course
        calendarId: The Calendar ID for a calendar that all course members can see
    """

    logger.info("Pulling course data")
    courses: List[Dict[str, str]] = request_courses(resource)
    return json_normalize(courses)


def request_all_courses_as_df(
    resource: Optional[Resource], sync_db: sqlalchemy.engine.base.Engine
) -> DataFrame:
    """
    Fetch Course API data for all courses and return a Courses API DataFrame

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a Courses API DataFrame with the current and previously fetched data

    Notes
    -----
    DataFrame columns are:
        id: Identifier for this course assigned by Classroom
        name: Name of the course
        section: Section of the course
        descriptionHeading: Optional heading for the description
        description: Optional description
        room: Optional room location
        ownerId: The identifier of the owner of a course
        creationTime: Creation time of the course
        updateTime: Time of the most recent update to this course
        enrollmentCode: Enrollment code to use when joining this course
        courseState: State of the course
        alternateLink: Absolute link to this course in the Classroom web UI
        teacherGroupEmail: The email address of a Google group containing all teachers of the course
        courseGroupEmail: The email address of a Google group containing all members of the course
        teacherFolder.id: The identifier of the teacher folder
        teacherFolder.title: The identifier of the teacher folder,
        teacherFolder.alternateLink: Absolute link to the teacher folder in the Classroom web UI
        guardiansEnabled: Whether or not guardian notifications are enabled for this course
        calendarId: The Calendar ID for a calendar that all course members can see
        CreateDate: Date this record was created by the extractor
        LastModifiedDate: Date this record was last updated by the extractor
    """

    courses_df = request_latest_courses_as_df(resource)
    _sync_without_cleanup(courses_df, sync_db)
    cleanup_after_sync("Courses", sync_db)

    return courses_df


def _sync_without_cleanup(
    resource_df: DataFrame, sync_db: sqlalchemy.engine.base.Engine
):
    """
    Take fetched API data and sync with database. Creates tables when necessary,
    but ok if temporary tables are there to start. Doesn't delete temporary tables when finished.

    Parameters
    ----------
    resource_df: DataFrame
        a Courses API DataFrame with the current fetched data which
        will be mutated, adding Hash and CreateDate/LastModifiedDate
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections
    """
    sync_to_db_without_cleanup(
        resource_df=resource_df,
        resource_name="Courses",
        table_columns_sql="""
            id BIGINT,
            name TEXT,
            section BIGINT,
            descriptionHeading TEXT,
            room TEXT,
            ownerId BIGINT,
            creationTime TEXT,
            updateTime TEXT,
            enrollmentCode BIGINT,
            courseState TEXT,
            alternateLink TEXT,
            teacherGroupEmail TEXT,
            courseGroupEmail TEXT,
            "teacherFolder.id" TEXT,
            "teacherFolder.title" TEXT,
            "teacherFolder.alternateLink" TEXT,
            guardiansEnabled BOOLEAN,
            calendarId BIGINT,
            """,
        primary_keys="id",
        sync_db=sync_db,
    )
