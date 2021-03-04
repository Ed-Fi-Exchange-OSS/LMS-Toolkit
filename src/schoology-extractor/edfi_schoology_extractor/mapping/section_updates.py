# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import pandas as pd

from . import constants

SECTION_UPDATE_TYPE = "section-update"


def map_to_udm(section_updates_df: pd.DataFrame, section_id: int) -> pd.DataFrame:
    """
    Maps a DataFrame containing Schoology section updates
    into the Ed-Fi LMS Unified Data Model (UDM) format.

    Parameters
    ----------
    section_updates_df: DataFrame
        Pandas DataFrame containing Schoology assignments for a section

    Returns
    -------
    DataFrame
        A LMSSectionActivities-formatted DataFrame

    Notes
    -----
    DataFrame columns are:
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a the section-update by
            the source system
        SourceSystem: The system code or name providing the user data
        LMSUserIdentifier: A unique number or alphanumeric code assigned to a user by the source
            system
        LMSSectionIdentifier: A unique number or alphanumeric code assigned to a section by the
            source system
        ActivityDateTime: The date/time the replied was created.
        ActivityStatus: The status for the update
        ActivityType: The type of activity: `section-update`
        Content: The comment text.
        AssignmentIdentifier: A unique numeric identifier assigned to the assignment.
        ActivityTimeInMinutes: The total activity time in minutes.
        CreateDate: Date/time at which the record was first retrieved
        LastModifiedDate: Date/time when the record was modified, or when first retrieved
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
    """
    if section_updates_df.empty:
        return section_updates_df

    df = section_updates_df[
        ["id", "uid", "created", "LastModifiedDate", "CreateDate"]
    ].copy()

    df["created"] = df["created"].apply(
        lambda x: datetime.strftime(datetime.fromtimestamp(int(x)), "%Y-%m-%d %H:%M:%S")
    )
    df["status"] = None

    df["id"] = df["id"].apply(lambda x: f"su#{x}")
    df["ActivityType"] = SECTION_UPDATE_TYPE
    df["LMSSectionIdentifier"] = section_id
    df["SourceSystem"] = constants.SOURCE_SYSTEM

    df["ActivityTimeInMinutes"] = None
    df["ParentSourceSystemIdentifier"] = None
    df["SourceCreateDate"] = ""
    df["SourceLastModifiedDate"] = ""

    df.rename(
        columns={
            "created": "ActivityDateTime",
            "id": "SourceSystemIdentifier",
            "uid": "LMSUserIdentifier",
            "status": "ActivityStatus",
        },
        inplace=True,
    )

    return df
