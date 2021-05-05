# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List
from pandas import DataFrame
import sqlalchemy

from canvasapi.assignment import Assignment
from canvasapi.submission import Submission
from edfi_lms_extractor_lib.api.resource_sync import (
    cleanup_after_sync,
    sync_to_db_without_cleanup,
)
from .canvas_helper import to_df
from .api_caller import call_with_retry

SUBMISSIONS_RESOURCE_NAME = "Submissions"

logger = logging.getLogger(__name__)


def _request_submissions_for_assignment(assignment: Assignment) -> List[Submission]:
    """
    Fetch Submissions API data for a assignment

    Parameters
    ----------
    canvas: Canvas
        a Canvas SDK object
    assignment: Assignment
        a Canvas Assignment object

    Returns
    -------
    List[Submission]
        a list of Submission API objects
    """
    return call_with_retry(assignment.get_submissions)


def request_submissions(assignment: Assignment) -> List[Submission]:
    """
    Fetch Submissions API data for a range of assignments and return a list of submissions as Submission API objects

    Parameters
    ----------
    assignment: Assignment
        a Canvas Assignment object

    Returns
    -------
    List[Submission]
        a list of Submission API objects
    """
    return _request_submissions_for_assignment(assignment)


def submissions_synced_as_df(
    submissions: List[Submission],
    sync_db: sqlalchemy.engine.base.Engine,
) -> DataFrame:
    """
    Fetch Submissions API data for a range of assignments and return a Submissions API DataFrame
    with current and previously fetched data

    Parameters
    ----------
    submissions: List[Submission]
        a list of Canvas Submissions objects
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a Submissions API DataFrame with the current and previously fetched data
    """
    submissions_df: DataFrame = _sync_without_cleanup(to_df(submissions), sync_db)
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
        a Submissions API DataFrame with the current fetched data which
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
        resource_name=SUBMISSIONS_RESOURCE_NAME,
        sync_db=sync_db,
    )
