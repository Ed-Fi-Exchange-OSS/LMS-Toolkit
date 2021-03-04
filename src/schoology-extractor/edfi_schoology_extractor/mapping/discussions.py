# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Union
import pandas as pd

from . import constants

DISCUSSION_TYPE = "Discussion"


def map_to_udm(discussions_df: pd.DataFrame, section_id: int) -> pd.DataFrame:
    """
    Maps a DataFrame containing Schoology Discussion threads
    into the Ed-Fi LMS Unified Data Model (UDM) format.

    Parameters
    ----------
    discussions_df: DataFrame
        Pandas DataFrame containing Schoology discussions

    Returns
    -------
    DataFrame
        A LMSUsers-formatted DataFrame

    Notes
    -----
    DataFrame columns are:
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a the discussion-reply by
            the source system
        SourceSystem: The system code or name providing the user data
        LMSUserIdentifier: A unique number or alphanumeric code assigned to a user by the source
            system
        LMSSectionIdentifier: A unique number or alphanumeric code assigned to a section by the
            source system
        ActivityDateTime: The date/time the replied was created.
        ActivityStatus: The status for the reply
        ActivityType: The type of activity: `Discussion reply`
        Content: The comment text.
        AssignmentIdentifier: A unique numeric identifier assigned to the assignment.
        ActivityTimeInMinutes: The total activity time in minutes.
        CreateDate: Date/time at which the record was first retrieved
        LastModifiedDate: Date/time when the record was modified, or when first retrieved
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
    """

    if discussions_df.empty:
        return discussions_df

    df = discussions_df[
        [
            "completed",
            "graded",
            "available",
            "published",
            "uid",
            "id",
            "CreateDate",
            "LastModifiedDate",
        ]
    ].copy()

    df["created"] = df["CreateDate"]

    def _get_status(row: pd.Series) -> Union[str, None]:
        completed = row["completed"]
        if completed == 1:
            return "completed"
        graded = row["graded"]
        if graded == 1:
            return "graded"
        available = row["available"]
        if available == 1:
            return "available"
        published = row["published"]
        if published == 1:
            return "published"
        return None

    df["status"] = df.apply(_get_status, axis=1)

    df["id"] = df["id"].apply(lambda x: f"sd#{x}")
    df["ActivityType"] = DISCUSSION_TYPE
    df["LMSSectionIdentifier"] = section_id
    df["SourceSystem"] = constants.SOURCE_SYSTEM

    df["ActivityTimeInMinutes"] = None
    df["ParentSourceSystemIdentifier"] = None
    df["SourceCreateDate"] = ""
    df["SourceLastModifiedDate"] = ""

    df.drop(["completed", "graded", "available", "published"], axis=1, inplace=True)

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
