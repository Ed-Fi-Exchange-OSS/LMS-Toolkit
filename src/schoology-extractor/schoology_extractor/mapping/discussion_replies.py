# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import pandas as pd

from . import constants

DISCUSSION_REPLIES_TYPE = "Discussion Reply"


def map_to_udm(discussion_replies_df: pd.DataFrame, section_id: int) -> pd.DataFrame:
    """
    Maps a DataFrame containing Schoology section associations (enrollments)
    into the Ed-Fi LMS Unified Data Model (UDM) format.

    Parameters
    ----------
    enrollments_df: DataFrame
        Pandas DataFrame containing Schoology assignments for a section

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
        LMSUserSourceSystemIdentifier: A unique number or alphanumeric code assigned to a user by the source
            system
        LMSSectionSourceSystemIdentifier: A unique number or alphanumeric code assigned to a section by the
            source system
        EntityStatus: The status of the record
        ActivityDateTime - The date/time the replied was created.
        ActivityStatus - The status for the reply
        ActivityType - The type of activity: `Discussion reply`
        Content - The comment text.
        LMSUserActivityIdentifier - A unique numeric identifier assigned to the user activity:
            `discussion_id`.
        AssignmentIdentifier - 	A unique numeric identifier assigned to the assignment.
        ActivityTimeInMinutes - The total activity time in minutes.
        EntityStatus - The status of the record.
        CreateDate: Date/time at which the record was first retrieved
        LastModifieDate: Date/time when the record was modified, or when first retrieved
    """
    df = discussion_replies_df[[
        "created",
        "status",
        "comment",
        "uid",
        "id",
        "discussion_id"
        ]].copy()

    df["created"] = df["created"].apply(lambda x: datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S"))
    df["status"] = df["status"].apply(lambda x: 'active' if x == 1 else 'deleted')
    df["ActivityType"] = DISCUSSION_REPLIES_TYPE
    df["LMSSectionIdentifier"] = section_id
    df["SourceSystem"] = constants.SOURCE_SYSTEM
    df["EntityStatus"] = constants.ACTIVE

    df["AssignmentIdentifier"] = None
    df["ActivityTimeInMinutes"] = None
    df["EntityStatus"] = constants.ACTIVE

    df.rename(
        columns={
            "created": "ActivityDateTime",
            "status": "ActivityStatus ",
            "comment": "Content",
            "id": "SourceSystemIdentifier",
            "uid": "LMSUserIdentifier",
            "discussion_id": "LMSUserActivityIdentifier"
        },
        inplace=True,
    )

    df["CreateDate"] = None
    df["LastModifiedDate"] = None

    return df
