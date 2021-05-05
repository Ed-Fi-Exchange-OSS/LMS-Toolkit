# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List
from pandas import DataFrame
import sqlalchemy

from canvasapi.course import Course
from canvasapi.user import User
from edfi_lms_extractor_lib.api.resource_sync import (
    cleanup_after_sync,
    sync_to_db_without_cleanup,
)
from .canvas_helper import remove_duplicates, to_df
from .api_caller import call_with_retry

STUDENTS_RESOURCE_NAME = "Students"

logger = logging.getLogger(__name__)


def _request_students_for_course(course: Course) -> List[User]:
    """
    Fetch Students API data for a course

    Parameters
    ----------
    canvas: Canvas
        a Canvas SDK object
    course: Course
        a Canvas Course object

    Returns
    -------
    List[User]
        a list of User API objects
    """
    return call_with_retry(course.get_users, enrollment_type=["student"])


def request_students(courses: List[Course]) -> List[User]:
    """
    Fetch Students API data for a range of courses and return a list of students as User API objects

    Parameters
    ----------
    courses: List[Course]
        a list of Canvas Course objects

    Returns
    -------
    List[User]
        a list of User API objects
    """

    logger.info("Pulling student data")
    students: List[User] = []
    for course in courses:
        students.extend(_request_students_for_course(course))

    return remove_duplicates(students, "id")


def students_synced_as_df(
    students: List[User],
    sync_db: sqlalchemy.engine.base.Engine,
) -> DataFrame:
    """
    Fetch Students API data for a range of courses and return a Students API DataFrame
    with current and previously fetched data

    Parameters
    ----------
    students: List[User]
        a list of Canvas Users objects
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a Students API DataFrame with the current and previously fetched data
    """
    students_df: DataFrame = _sync_without_cleanup(to_df(students), sync_db)
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
        identity_columns=["id"],
        resource_name=STUDENTS_RESOURCE_NAME,
        sync_db=sync_db,
    )
