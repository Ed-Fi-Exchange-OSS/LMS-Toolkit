# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List
from pandas import DataFrame
import sqlalchemy

from canvasapi.section import Section
from canvasapi.enrollment import Enrollment
from edfi_lms_extractor_lib.api.resource_sync import (
    cleanup_after_sync,
    sync_to_db_without_cleanup,
)
from .canvas_helper import to_df
from .api_caller import call_with_retry

ENROLLMENTS_RESOURCE_NAME = "Enrollments"

logger = logging.getLogger(__name__)


def request_enrollments_for_section(section: Section) -> List[Enrollment]:
    """
    Fetch Enrollments API data for a section

    Parameters
    ----------
    canvas: Canvas
        a Canvas SDK object
    user: User
        a Canvas User object

    Returns
    -------
    List[Enrollment]
        a list of Enrollment API objects
    """
    return call_with_retry(section.get_enrollments)


def enrollments_synced_as_df(
    enrollments: List[Enrollment],
    sync_db: sqlalchemy.engine.base.Engine,
) -> DataFrame:
    """
    Fetch Enrollments API data for a range of students and return a Enrollments API DataFrame
    with current and previously fetched data

    Parameters
    ----------
    enrollments: List[Enrollment]
        a list of Canvas Enrollments objects
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a Enrollments API DataFrame with the current and previously fetched data
    """
    enrollments_df: DataFrame = _sync_without_cleanup(to_df(enrollments), sync_db)
    cleanup_after_sync(ENROLLMENTS_RESOURCE_NAME, sync_db)

    return enrollments_df


def _sync_without_cleanup(
    resource_df: DataFrame, sync_db: sqlalchemy.engine.base.Engine
) -> DataFrame:
    """
    Take fetched API data and sync with database. Creates tables when necessary,
    but ok if temporary tables are there to start. Doesn't delete temporary tables when finished.

    Parameters
    ----------
    resource_df: DataFrame
        a Enrollments API DataFrame with the current fetched data which
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
        resource_name=ENROLLMENTS_RESOURCE_NAME,
        sync_db=sync_db,
    )
