# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List
from pandas import DataFrame
import sqlalchemy

from canvasapi.course import Course
from canvasapi.assignment import Assignment
from edfi_lms_extractor_lib.api.resource_sync import (
    cleanup_after_sync,
    sync_to_db_without_cleanup,
)
from .canvas_helper import to_df
from .api_caller import call_with_retry

ASSIGNMENTS_RESOURCE_NAME = "Assignments"

logger = logging.getLogger(__name__)


def _request_assignments_for_course(course: Course) -> List[Assignment]:
    """
    Fetch Assignments API data for a course

    Parameters
    ----------
    canvas: Canvas
        a Canvas SDK object
    course: Course
        a Canvas Course object

    Returns
    -------
    List[Assignment]
        a list of Assignment API objects
    """
    return call_with_retry(course.get_assignments)


def request_assignments(courses: List[Course]) -> List[Assignment]:
    """
    Fetch Assignments API data for a range of courses and return a list of assignments as Assignment API objects

    Parameters
    ----------
    courses: List[Course]
        a list of Canvas Course objects

    Returns
    -------
    List[Assignment]
        a list of Assignment API objects
    """

    logger.info("Pulling assignment data")
    assignments: List[Assignment] = []
    for course in courses:
        assignments.extend(_request_assignments_for_course(course))

    return assignments


def assignments_synced_as_df(
    assignments: List[Assignment],
    sync_db: sqlalchemy.engine.base.Engine,
) -> DataFrame:
    """
    Fetch Assignments API data for a range of courses and return a Assignments API DataFrame
    with current and previously fetched data

    Parameters
    ----------
    assignments: List[Assignment]
        a list of Canvas Assignments objects
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a Assignments API DataFrame with the current and previously fetched data
    """

    assignments_df: DataFrame = _sync_without_cleanup(to_df(assignments), sync_db)
    cleanup_after_sync(ASSIGNMENTS_RESOURCE_NAME, sync_db)

    return assignments_df


def _sync_without_cleanup(
    resource_df: DataFrame, sync_db: sqlalchemy.engine.base.Engine
) -> DataFrame:
    """
    Take fetched API data and sync with database. Creates tables when necessary,
    but ok if temporary tables are there to start. Doesn't delete temporary tables when finished.

    Parameters
    ----------
    resource_df: DataFrame
        a Assignments API DataFrame with the current fetched data which
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
        resource_name=ASSIGNMENTS_RESOURCE_NAME,
        sync_db=sync_db,
    )
