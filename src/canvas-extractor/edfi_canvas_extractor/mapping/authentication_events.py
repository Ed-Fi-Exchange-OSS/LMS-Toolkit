# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
from pandas import DataFrame

from . import constants


def _map_type(lms_type: str):
    return "sign-in" if lms_type == "login" else "sign-out"


def map_to_udm_system_activities(authentication_events: pd.DataFrame) -> pd.DataFrame:
    """
    Maps a DataFrame containing Canvas authentication_events into the Ed-Fi LMS Unified Data
    Model (UDM) format.

    Parameters
    ----------
    authentication_events: DataFrame
        Pandas DataFrame containing authentication_events

    Returns
    -------
    DataFrame
        A LMSSystemActivities-formatted DataFrame

    Notes
    -----
    DataFrame columns are:
        SourceSystemIdentifier: a unique code for the record.
        SourceSystem: the system code or name providing the user data.
        LMSUserSourceSystemIdentifier: the source system identifier for the user.
        ActivityType: either "sign-in" or "sign-out".
        ActivityDateTime: the source system's event timestamp.
        ActivityStatus: will always be "active".
        ParentSourceSystemIdentifier: will always be None.
        ActivityTimeInMinutes: will always be None.
        CreateDate: Created date.
        LastModifiedDate: Last modified date (will always be the same as the CreateDate).
        SourceCreateDate: Date this record was created in the LMS.
    """

    if authentication_events.empty:
        return authentication_events

    assert "CreateDate" in authentication_events.columns
    assert "LastModifiedDate" in authentication_events.columns

    df: DataFrame = authentication_events[
        [
            "id",
            "event_type",
            "created_at",
            "CreateDate",
            "LastModifiedDate",
        ]
    ].copy()

    df["LMSUserSourceSystemIdentifier"] = df["id"].apply(lambda x: x.split("#")[1])

    df.rename(
        columns={
            "id": "SourceSystemIdentifier",
            "event_type": "ActivityType",
            "created_at": "ActivityDateTime",
        },
        inplace=True,
    )

    df["ActivityType"] = df["ActivityType"].apply(_map_type)
    df["SourceSystem"] = constants.SOURCE_SYSTEM
    df["ActivityStatus"] = "active"
    df["ParentSourceSystemIdentifier"] = ""
    df["ActivityTimeInMinutes"] = ""
    df["SourceCreateDate"] = df["ActivityDateTime"]
    df["SourceLastModifiedDate"] = ""
    df["ActivityDateTime"] = pd.to_datetime(df["ActivityDateTime"]).dt.strftime(
        constants.DATE_FORMAT
    )

    return df
