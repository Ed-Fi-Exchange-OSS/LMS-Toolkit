# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime

import pandas as pd

from . import constants


def _get_date_formated(date) -> str:
    if not isinstance(date, str) or date == "":
        return ""
    return datetime.strftime(
        datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z"), "%Y/%m/%d %H:%M:%S"
    )


def _get_status(row: pd.Series):
    if row["late"] == 1:
        return "late"
    if row["missing"] == 1:
        return "missing"
    if row["graded_at"] is not None:
        return "graded"
    return "on-time"


def map_to_udm_submissions(submissions_df: pd.DataFrame) -> pd.DataFrame:
    """
    Maps a DataFrame containing Canvas submissions into the Ed-Fi LMS Unified Data
    Model (UDM) format.

    Parameters
    ----------
    submissions_df: DataFrame
        Pandas DataFrame containing Canvas submissions for a section

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
        [
            "id",
            "late",
            "missing",
            "submitted_at",
            "grade",
            "assignment_id",
            "user_id",
            "CreateDate",
            "LastModifiedDate",
            "graded_at",
        ]
    ].copy()

    df["submitted_at"] = df["submitted_at"].apply(_get_date_formated)

    df.rename(
        columns={
            "id": "SourceSystemIdentifier",
            "submitted_at": "SubmissionDateTime",
            "assignment_id": "AssignmentSourceSystemIdentifier",
            "user_id": "LMSUserSourceSystemIdentifier",
            "grade": "Grade",
        },
        inplace=True,
    )

    df["SubmissionDateTime"] = pd.to_datetime(df["SubmissionDateTime"]).dt.strftime(
        constants.DATE_FORMAT
    )
    df["SourceSystem"] = constants.SOURCE_SYSTEM
    df["SubmissionStatus"] = df.apply(_get_status, axis=1)
    df["EarnedPoints"] = None
    df["SourceCreateDate"] = None
    df["SourceLastModifiedDate"] = None

    df.drop(columns=["late", "missing", "graded_at"], inplace=True)

    return df
