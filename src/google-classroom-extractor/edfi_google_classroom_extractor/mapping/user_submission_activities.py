# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import json
from typing import Dict
from pandas import DataFrame, concat, Series
from edfi_google_classroom_extractor.mapping.constants import SOURCE_SYSTEM

ACTIVITY_TYPE_STATE = "Submission State Change"
ACTIVITY_TYPE_GRADE = "Submission Grade Change"


def submissions_to_user_submission_activities_dfs(
    submissions_df: DataFrame,
) -> Dict[str, DataFrame]:
    """
    Convert a Submission API DataFrame to a Dict of UserActivity
    UDM DataFrames grouped by source system section id.

    Parameters
    ----------
    submissions_df: DataFrame
        is a Submission API DataFrame

    Returns
    -------
    Dict[str, DataFrame] LMS UDM UserActivity DataFrames
        grouped by source system section id

    Notes
    -----
    UserActivity DataFrame columns are:
        ActivityDateTime: The date/time the activity occurred
        ActivityStatus: The activity status
        ActivityTimeInMinutes: The total activity time in minutes
        ActivityType: The type of activity, here "Submission" or "Grade"
        AssignmentIdentifier: A unique numeric identifier assigned to the assignment
        Content: Content associated with the activity
        LMSSectionIdentifier: A unique numeric identifier assigned to the section
        SourceSystem: The system code or name providing the user activity data
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a
            user activity by the source system
        LMSUserIdentifier: A unique numeric identifier assigned to the user
        CreateDate: Date this record was created in the extractor
        LastModifiedDate: Date this record was last updated in the extractor
    """
    assert "submissionHistory" in submissions_df.columns
    assert "id" in submissions_df.columns
    assert "courseId" in submissions_df.columns
    assert "courseWorkId" in submissions_df.columns

    # convert json-like submissionHistory string to list of dicts
    submissions_df["submissionHistory"] = submissions_df["submissionHistory"].apply(lambda json_like: json.loads(json_like.replace("'", '"')))
    submissions_df["AssignmentIdentifier"] = submissions_df[
        ["courseId", "courseWorkId"]
    ].agg("-".join, axis=1)

    submissions_df = submissions_df[["id", "courseId", "courseWorkId", "submissionHistory", "AssignmentIdentifier", "CreateDate", "LastModifiedDate"]]

    # explode submissionHistory lists into rows with other columns duplicated
    history_df = submissions_df.explode(column="submissionHistory")  # type: ignore

    # expand submissionHistory dicts (stateHistory and gradeHistory) into their own columns
    history_df = history_df["submissionHistory"].apply(Series).merge(history_df, left_index=True, right_index=True, how='outer')
    history_df.drop(columns=["submissionHistory"], inplace=True)

    # expand stateHistory (can assume exists, should always have at least one "CREATED" entry)
    user_submission_df = concat([history_df, history_df["stateHistory"].apply(Series)], axis=1)
    user_submission_df.dropna(subset=["stateHistory"], inplace=True)

    # enrich stateHistory
    user_submission_df["SourceSystemIdentifier"] = "S-" + user_submission_df[
        ["courseId", "courseWorkId", "id", "stateTimestamp"]
    ].agg("-".join, axis=1)

    user_submission_df = user_submission_df[
        [
            "SourceSystemIdentifier",
            "AssignmentIdentifier",
            "stateTimestamp",
            "state",
            "courseId",
            "actorUserId",
            "CreateDate",
            "LastModifiedDate"
        ]
    ]

    user_submission_df = user_submission_df.rename(
        columns={
            "stateTimestamp": "ActivityDateTime",
            "state": "ActivityStatus",
            "courseId": "LMSSectionIdentifier",
            "actorUserId": "LMSUserIdentifier",
        }
    )

    user_submission_df["ActivityType"] = ACTIVITY_TYPE_STATE

    # expand gradeHistory if exists
    if "gradeHistory" in history_df:
        grade_history_df = concat([history_df, history_df["gradeHistory"].apply(Series)], axis=1)
        grade_history_df.dropna(subset=["gradeHistory"], inplace=True)

        # enrich gradeHistory
        grade_history_df["SourceSystemIdentifier"] = "G-" + grade_history_df[
            ["courseId", "courseWorkId", "id", "gradeTimestamp"]
        ].agg("-".join, axis=1)

        grade_history_df = grade_history_df[
            [
                "SourceSystemIdentifier",
                "AssignmentIdentifier",
                "gradeTimestamp",
                "gradeChangeType",
                "courseId",
                "actorUserId",
                "CreateDate",
                "LastModifiedDate"
            ]
        ]

        grade_history_df = grade_history_df.rename(
            columns={
                "gradeTimestamp": "ActivityDateTime",
                "gradeChangeType": "ActivityStatus",
                "courseId": "LMSSectionIdentifier",
                "actorUserId": "LMSUserIdentifier",
            }
        )

        grade_history_df["ActivityType"] = ACTIVITY_TYPE_GRADE

        # combine with stateHistory
        user_submission_df = user_submission_df.append(grade_history_df)

    # teacher actions can show up on student histories and vice-versa
    user_submission_df.drop_duplicates(subset=["SourceSystemIdentifier"], inplace=True)

    # finish with common columns
    user_submission_df["ActivityTimeInMinutes"] = ""
    user_submission_df["Content"] = ""
    user_submission_df["SourceSystem"] = SOURCE_SYSTEM
    user_submission_df["SourceCreateDate"] = ""  # No create date available from API
    user_submission_df["SourceLastModifiedDate"] = ""  # No modified date available from API

    # group by section id as a Dict of DataFrames
    result: Dict[str, DataFrame] = dict(
        tuple(user_submission_df.groupby(["LMSSectionIdentifier"]))
    )

    return result
