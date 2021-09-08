# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict, List, Tuple, Any
import ast

from pandas import DataFrame, Series, isna
from edfi_google_classroom_extractor.mapping.constants import SOURCE_SYSTEM


# States returned by API
CREATED_STATE = "CREATED"
NEW_STATE = "NEW"
RECLAIMED_STATE = "RECLAIMED_BY_STUDENT"
TURNED_IN_STATE = "TURNED_IN"
RETURNED_STATE = "RETURNED"

# States derived from API "late" flag
LATE_STATE = "LATE"
MISSING_STATE = "MISSING"


def derive_state(submission_row: Series) -> str:
    """
    Takes a Pandas row of API assign submission data and returns the submission
    state for that row based on the API provided state and late flag.

    Parameters
    ----------
    pandas_row: Any
        is a row of assignment submission data

    Returns
    -------
    str
        Submission state for the row of data
    """
    api_state: str = submission_row["state"]
    if "late" not in submission_row:
        return api_state

    if isna(submission_row["late"]):
        return api_state

    if isinstance(submission_row["late"], bool) and submission_row["late"] is False:
        return api_state

    if (
        isinstance(submission_row["late"], str)
        and submission_row["late"].lower() != "true"
    ):
        return api_state

    if api_state == TURNED_IN_STATE:
        return LATE_STATE

    if (
        api_state == CREATED_STATE
        or api_state == NEW_STATE
        or api_state == RECLAIMED_STATE
    ):
        return MISSING_STATE

    return api_state


def _get_submission_datetime(submission_row: Series) -> str:
    if submission_row["state"] != TURNED_IN_STATE and submission_row["state"] != RETURNED_STATE:
        return ""

    status_history: List[dict] = ast.literal_eval(submission_row["submissionHistory"])
    # this submission history also has a history of grades, but for this purpose, we only care
    # about stateHistory so we filter by stateHistory
    status_history = [
        status_item["stateHistory"]
        for status_item in status_history
        if "stateHistory" in status_item.keys()
    ]
    status_history = sorted(
        status_history, key=lambda k: k["stateTimestamp"], reverse=True
    )

    for status_record in status_history:
        status_is_turned_in: bool = status_record["state"] == TURNED_IN_STATE

        if status_is_turned_in:
            return status_record["stateTimestamp"]

    return ""


def submissions_to_assignment_submissions_dfs(
    submissions_df: DataFrame,
) -> Dict[Tuple[str, str], DataFrame]:
    """
    Convert a Submission API DataFrame to a Dict of AssignmentSubmission UDM DataFrames
    grouped by source system section id/assignment id tuple pairs

    Parameters
    ----------
    submissions_df: DataFrame
        is a Submission API DataFrame

    Returns
    -------
    Dict[Tuple[str, str], DataFrame]
        LMS UDM AssignmentSubmission DataFrames grouped by
            source system section id/assignment id tuple pairs

    Notes
    -----
    AssignmentSubmission DataFrame columns are:
        AssignmentSourceSystemIdentifier: A unique numeric identifier assigned to the assignment
        EarnedPoints: The points earned for the submission
        Grade: The grade received for the submission
        SourceSystem: The system code or name providing the AssignmentSubmission data
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to
            an AssignmentSubmission by the source system
        SubmissionStatus: The status of the submission in relation to the late acceptance policy
        SubmissionDateTime: The date and time of the assignment submission
        LMSUserSourceSystemIdentifier: A unique numeric identifier assigned to the user
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
    """
    assert "courseId" in submissions_df.columns
    assert "courseWorkId" in submissions_df.columns
    assert "id" in submissions_df.columns
    assert "userId" in submissions_df.columns
    assert "creationTime" in submissions_df.columns
    assert "updateTime" in submissions_df.columns
    assert "state" in submissions_df.columns
    assert "assignedGrade" in submissions_df.columns

    submissions_df["SourceSystemIdentifier"] = submissions_df[
        ["courseId", "courseWorkId", "id"]
    ].agg("-".join, axis=1)

    submissions_df["AssignmentSourceSystemIdentifier"] = submissions_df[
        ["courseId", "courseWorkId"]
    ].agg("-".join, axis=1)

    submissions_df["Grade"] = submissions_df["assignedGrade"]
    submissions_df["SubmissionDateTime"] = submissions_df.apply(
        _get_submission_datetime,
        axis=1,
    )
    submissions_df["SubmissionStatus"] = submissions_df.apply(derive_state, axis=1)

    assignment_submissions_df: DataFrame = submissions_df[
        [
            "SourceSystemIdentifier",
            "AssignmentSourceSystemIdentifier",
            "Grade",
            "SubmissionDateTime",
            "assignedGrade",
            "userId",
            "courseId",
            "creationTime",
            "updateTime",
            "SubmissionStatus",
            "CreateDate",
            "LastModifiedDate",
        ]
    ]

    assignment_submissions_df = assignment_submissions_df.rename(
        columns={
            "assignedGrade": "EarnedPoints",
            "userId": "LMSUserSourceSystemIdentifier",
            "courseId": "SourceSystemSectionIdentifier",
            "creationTime": "SourceCreateDate",
            "updateTime": "SourceLastModifiedDate",
        }
    )

    assignment_submissions_df["SourceSystem"] = SOURCE_SYSTEM

    # group by section id and assignment id as a Dict of DataFrames
    result: Dict[
        Any, DataFrame
    ] = dict(  # Any because Pylance doesn't believe Tuple[str, str]
        tuple(
            assignment_submissions_df.groupby(
                [
                    "SourceSystemSectionIdentifier",
                    "AssignmentSourceSystemIdentifier",
                ]
            )
        )
    )

    # no longer need group by column
    for grouped_df in result.values():
        grouped_df.drop(columns=["SourceSystemSectionIdentifier"], inplace=True)

    return result
