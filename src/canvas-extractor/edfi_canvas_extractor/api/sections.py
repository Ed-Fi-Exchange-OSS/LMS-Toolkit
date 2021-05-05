# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List
from pandas import DataFrame
import sqlalchemy

from canvasapi.course import Course
from canvasapi.section import Section
from edfi_lms_extractor_lib.api.resource_sync import (
    cleanup_after_sync,
    sync_to_db_without_cleanup,
)
from .canvas_helper import to_df
from .api_caller import call_with_retry

SECTIONS_RESOURCE_NAME = "Sections"

logger = logging.getLogger(__name__)


def _request_sections_for_course(course: Course) -> List[Section]:
    """
    Fetch Sections API data for a course

    Parameters
    ----------
    canvas: Canvas
        a Canvas SDK object
    course: Course
        a Canvas Course object

    Returns
    -------
    List[Section]
        a list of Section API objects
    """
    return call_with_retry(course.get_sections)


def request_sections(courses: List[Course]) -> List[Section]:
    """
    Fetch Sections API data for a range of courses and return a list of sections as Section API objects

    Parameters
    ----------
    courses: List[Course]
        a list of Canvas Course objects

    Returns
    -------
    List[Section]
        a list of Section API objects
    """

    logger.info("Pulling section data")
    sections: List[Section] = []
    for course in courses:
        sections.extend(_request_sections_for_course(course))

    return sections


def sections_synced_as_df(
    sections: List[Section],
    sync_db: sqlalchemy.engine.base.Engine,
) -> DataFrame:
    """
    Fetch Sections API data for a range of courses and return a Sections API DataFrame
    with current and previously fetched data

    Parameters
    ----------
    sections: List[Section]
        a list of Canvas Sections objects
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a Sections API DataFrame with the current and previously fetched data
    """

    sections_df: DataFrame = _sync_without_cleanup(to_df(sections), sync_db)
    cleanup_after_sync(SECTIONS_RESOURCE_NAME, sync_db)

    return sections_df


def _sync_without_cleanup(
    resource_df: DataFrame, sync_db: sqlalchemy.engine.base.Engine
) -> DataFrame:
    """
    Take fetched API data and sync with database. Creates tables when necessary,
    but ok if temporary tables are there to start. Doesn't delete temporary tables when finished.

    Parameters
    ----------
    resource_df: DataFrame
        a Sections API DataFrame with the current fetched data which
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
        resource_name=SECTIONS_RESOURCE_NAME,
        sync_db=sync_db,
    )
