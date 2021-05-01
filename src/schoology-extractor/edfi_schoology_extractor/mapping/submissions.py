# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime

import pandas as pd

from . import constants


def map_to_udm(submissions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Maps a DataFrame containing Schoology submissions into the Ed-Fi LMS Unified Data
    Model (UDM) format.

    Parameters
    ----------
    submissions_df: DataFrame
        Pandas DataFrame containing Schoology submissions for a section

    Returns
    -------
    DataFrame
        A Submissions-formatted DataFrame .

    Notes
    -----
    DataFrame columns are:
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a
            submission by the source system
        SourceSystem: The system code or name providing the user data
        SubmissionStatus: The status of the submission
        SubmissionDateTime: Datetime of the submission
        EarnedPoints: Earned points for the submission
        Grade: Grade for the submission
        AssignmentSourceSystemIdentifier: Unique identifier for the assignment
        LMSUserSourceSystemIdentifier: Unique identifier of the LMSUser
        CreateDate: Created date
        LastModifiedDate: Last modified date
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
    """

    if submissions_df.empty:
        return submissions_df

    df = submissions_df[
        ["id", "created", "late", "draft", "uid", "CreateDate", "LastModifiedDate"]
    ].copy()

    df["SourceSystem"] = constants.SOURCE_SYSTEM
    df["SubmissionStatus"] = "on-time"

    def _get_status(row: pd.Series) -> str:
        if row["late"] == 1:
            return "late"
        if row["draft"] == 1:
            return "draft"
        return "on-time"

    df["SubmissionStatus"] = df.apply(_get_status, axis=1)

    df.drop(columns=["late", "draft"], inplace=True)

    df["AssignmentSourceSystemIdentifier"] = df["id"].apply(lambda x: x.split("#")[1])
    df["EarnedPoints"] = None
    df["Grade"] = None
    df["SourceCreateDate"] = ""
    df["SourceLastModifiedDate"] = ""

    df.rename(
        columns={
            "id": "SourceSystemIdentifier",
            "created": "SubmissionDateTime",
            "uid": "LMSUserSourceSystemIdentifier",
        },
        inplace=True,
    )

    df["SubmissionDateTime"] = df["SubmissionDateTime"].apply(
        lambda x: datetime.strftime(datetime.fromtimestamp(x), "%Y-%m-%d %H:%M:%S")
    )

    return df
