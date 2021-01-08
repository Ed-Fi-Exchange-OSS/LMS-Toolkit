# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime

import pandas as pd


def map_to_udm(usage: pd.DataFrame) -> pd.DataFrame:
    """
    Maps a DataFrame containing Schoology usage analytics into the Ed-Fi LMS
    Unified Data Model (UDM) format for system activities

    Parameters
    ----------
    usage: DataFrame
        Pandas DataFrame containing Schoology usage analytics

    Returns
    -------
    DataFrame
        A System Activities-formatted DataFrame

    Notes
    -----
    DataFrame columns are:
        SourceSystemIdentifier: a unique code for the record
        SourceSystem: the system code or name providing the user data
        LMSUserSourceSystemIdentifier: the source system identifier for the user
        ActivityType: either "sign-in" or "sign-out"
        ActivityDateTime: the source system's event timestamp
        ActivityStatus: will always be "active"
        ParentSourceSystemIdentifier: will always be None
        ActivityTimeInMinutes: will always be None
        CreateDate: Created date
        LastModifiedDate: Last modified date (will always be the same as the CreateDate)
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
    """

    if usage.empty:
        return usage

    filter = (usage["action_type"].isin(["CREATE", "DELETE"])) & (
        usage["item_type"] == "SESSION"
    )
    keep = ["schoology_user_id", "action_type", "last_event_timestamp"]
    df = usage[filter][keep].copy()

    if df.empty:
        return pd.DataFrame()

    df["SourceSystem"] = "Schoology"

    def _get_source_system_identifier(row: pd.Series) -> str:
        id = "in" if row["action_type"] == "CREATE" else "out"
        timestamp = pd.Timestamp(row["last_event_timestamp"]).timestamp()
        id = f"{id}#{row['schoology_user_id']}#{timestamp}"
        return id

    df["SourceSystemIdentifier"] = df.apply(_get_source_system_identifier, axis=1)

    df["ActivityType"] = df.apply(
        lambda row: "sign-in" if row["action_type"] == "CREATE" else "sign-out", axis=1
    )

    df.rename(
        columns={
            "last_event_timestamp": "ActivityDateTime",
            "schoology_user_id": "LMSUserSourceSystemIdentifier",
        },
        inplace=True,
    )
    df = df.astype({"LMSUserSourceSystemIdentifier": "int64"})

    df["ActivityStatus"] = "active"
    df["ParentSourceSystemIdentifier"] = df["ActivityTimeInMinutes"] = None
    df["CreateDate"] = df["LastModifiedDate"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    df["SourceCreateDate"] = ""
    df["SourceLastModifiedDate"] = ""

    df.drop(columns=["action_type"], inplace=True)

    return df
