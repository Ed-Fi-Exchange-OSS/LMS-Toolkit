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

SECTIONS_RESOURCE_NAME = "Sections"


def sections_synced_as_df(
    sections: List[Dict[str, str]],
    sync_db: sqlalchemy.engine.base.Engine,
) -> DataFrame:
    """
    Fetch Sections API data for a range of courses and return a Sections API DataFrame
    with current and previously fetched data

    Parameters
    ----------
    sections: List[Dict[str, str]]
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
    Take fetched data and sync with database. Creates tables when necessary,
    but ok if temporary tables are there to start. Doesn't delete temporary tables when finished.

    Parameters
    ----------
    resource_df: DataFrame
        a Sections DataFrame with the current fetched data which
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
