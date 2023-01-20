# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict, List

from pandas import DataFrame
import sqlalchemy

from edfi_lms_extractor_lib.api.resource_sync import (
    cleanup_after_sync,
    sync_to_db_without_cleanup,
)
from .canvas_helper import to_df

COURSES_RESOURCE_NAME = "Courses"


def courses_synced_as_df(
    courses: List[Dict[str, str]], sync_db: sqlalchemy.engine.base.Engine
) -> DataFrame:
    """
    Using Course data, return a Courses API DataFrame

    Parameters
    ----------
    courses: List[Dict[str, str]]
        a list of Canvas Course SDK objects
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a Courses DataFrame with the current and previously fetched data
    """
    courses_df: DataFrame = _sync_without_cleanup(to_df(courses), sync_db)
    cleanup_after_sync(COURSES_RESOURCE_NAME, sync_db)

    return courses_df


def _sync_without_cleanup(
    resource_df: DataFrame, sync_db: sqlalchemy.engine.base.Engine
) -> DataFrame:
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

    Returns
    -------
    DataFrame
        a DataFrame with current fetched data and reconciled CreateDate/LastModifiedDate
    """
    return sync_to_db_without_cleanup(
        resource_df=resource_df,
        identity_columns=["id"],
        resource_name=COURSES_RESOURCE_NAME,
        sync_db=sync_db,
    )
