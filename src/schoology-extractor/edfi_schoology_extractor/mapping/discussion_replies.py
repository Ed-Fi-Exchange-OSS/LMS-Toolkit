# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import pandas as pd

from . import constants

DISCUSSION_REPLIES_TYPE = "discussion-reply"


def map_to_udm(
    discussion_replies_df: pd.DataFrame, section_id: int, discussion_id: int
) -> pd.DataFrame:
    """
    Maps a DataFrame containing Schoology discussion replies
    into the Ed-Fi LMS Unified Data Model (UDM) format.

    Parameters
    ----------
    discussion_replies_df: DataFrame
        Pandas DataFrame containing Schoology discussion replies for a section

    Returns
    -------
    DataFrame
        A LMSSectionActivities-formatted DataFrame

    Notes
    -----
    DataFrame columns are:
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a the discussion-reply by
            the source system
        SourceSystem: The system code or name providing the user data
        LMSUserSourceSystemIdentifier: A unique number or alphanumeric code assigned to a user by the source
            system
        LMSSectionSourceSystemIdentifier: A unique number or alphanumeric code assigned to a section by the
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

    if discussion_replies_df.empty:
        return discussion_replies_df

    df = discussion_replies_df[
        [
            "created",
            "status",
            "uid",
            "id",
            "CreateDate",
            "LastModifiedDate",
            "parent_id",
        ]
    ].copy()

    df["created"] = df["created"].apply(
        lambda x: datetime.fromtimestamp(int(x)).strftime("%Y-%m-%d %H:%M:%S")
    )
    df["status"] = df["status"].apply(lambda x: "active" if int(x) == 1 else "deleted")
    df["id"] = df["id"].apply(lambda x: f"sdr#{x}")
    df["ActivityType"] = DISCUSSION_REPLIES_TYPE
    df["LMSSectionSourceSystemIdentifier"] = section_id
    df["SourceSystem"] = constants.SOURCE_SYSTEM
    df["ParentSourceSystemIdentifier"] = df["parent_id"].apply(
        lambda x: f"sdr#{x}" if (x != 0) else f"sd{discussion_id}"
    )
    df["SourceSystemIdentifier"] = df[["ParentSourceSystemIdentifier", "id"]].agg(
        "-".join, axis=1
    )
    df.drop(columns=["id", "parent_id"], inplace=True)

    df["ActivityTimeInMinutes"] = None
    df["SourceCreateDate"] = ""
    df["SourceLastModifiedDate"] = ""

    df.rename(
        columns={
            "created": "ActivityDateTime",
            "status": "ActivityStatus",
            "uid": "LMSUserSourceSystemIdentifier",
        },
        inplace=True,
    )

    return df
