# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict, Tuple, Any
from pandas import DataFrame
from google_classroom_extractor.mapping.constants import (
    SOURCE_SYSTEM,
    ENTITY_STATUS_ACTIVE,
)

TURNED_IN_STATE = "TURNED_IN"


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
        AssignmentIdentifier: A unique numeric identifier assigned to the assignment
        EarnedPoints: The points earned for the submission
        EntityStatus: The status of the record
        Grade: The grade received for the submission
        LMSGradeIdentifier: A unique numeric identifier assigned to the AssignmentSubmission
        SourceSystem: The system code or name providing the AssignmentSubmission data
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to
            an AssignmentSubmission by the source system
        Status: The status of the submission in relation to the late acceptance policy
        SubmissionDateTime: The date and time of the assignment submission
        LMSUserIdentifier: A unique numeric identifier assigned to the user
        CreateDate: Date this record was created
        LastModifiedDate: Date this record was last updated
    """
    assert "courseId" in submissions_df.columns
    assert "courseWorkId" in submissions_df.columns
    assert "id" in submissions_df.columns
    assert "userId" in submissions_df.columns
    assert "courseWorkType" in submissions_df.columns
    assert "creationTime" in submissions_df.columns
    assert "updateTime" in submissions_df.columns
    assert "state" in submissions_df.columns
    assert "assignedGrade" in submissions_df.columns

    submissions_df["SourceSystemIdentifier"] = submissions_df[
        ["courseId", "courseWorkId", "id"]
    ].agg("-".join, axis=1)

    submissions_df["AssignmentIdentifier"] = submissions_df[
        ["courseId", "courseWorkId"]
    ].agg("-".join, axis=1)

    submissions_df["Grade"] = submissions_df["assignedGrade"]
    submissions_df["LMSGradeIdentifier"] = submissions_df["SourceSystemIdentifier"]
    submissions_df["SubmissionDateTime"] = submissions_df.apply(
        lambda row: row["updateTime"] if row["state"] == TURNED_IN_STATE else "",
        axis=1,
    )

    assignment_submissions_df: DataFrame = submissions_df[
        [
            "SourceSystemIdentifier",
            "AssignmentIdentifier",
            "Grade",
            "LMSGradeIdentifier",
            "SubmissionDateTime",
            "assignedGrade",
            "userId",
            "courseId",
            "courseWorkType",
            "creationTime",
            "updateTime",
            "state",
        ]
    ]

    assignment_submissions_df = assignment_submissions_df.rename(
        columns={
            "assignedGrade": "EarnedPoints",
            "userId": "LMSUserIdentifier",
            "courseId": "SourceSystemSectionIdentifier",
            "courseWorkType": "SubmissionType",
            "creationTime": "CreateDate",
            "updateTime": "LastModifiedDate",
            "state": "Status",
        }
    )

    assignment_submissions_df["SourceSystem"] = SOURCE_SYSTEM
    assignment_submissions_df["EntityStatus"] = ENTITY_STATUS_ACTIVE

    # group by section id and assignment id as a Dict of DataFrames
    result: Dict[Any, DataFrame] = dict(  # Any because Pylance doesn't believe Tuple[str, str]
        tuple(
            assignment_submissions_df.groupby(
                [
                    "SourceSystemSectionIdentifier",
                    "AssignmentIdentifier",
                ]
            )
        )
    )

    # no longer need group by column
    for grouped_df in result.values():
        grouped_df.drop(columns=["SourceSystemSectionIdentifier"], inplace=True)

    return result
