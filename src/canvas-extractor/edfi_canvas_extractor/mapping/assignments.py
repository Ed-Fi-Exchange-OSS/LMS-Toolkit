# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict, cast
from pandas import DataFrame

from . import constants


def map_to_udm_assignments(
    assignments_df: DataFrame, sections_df: DataFrame
) -> Dict[str, DataFrame]:
    """
    Maps a DataFrame containing Canvas assignments into the Ed-Fi LMS Unified Data
    Model (UDM) format.

    Parameters
    ----------
    assignments_df: DataFrame
        Pandas DataFrame containing Canvas assignments
    sections_df: DataFrame
        Pandas DataFrame containing Canvas sections

    Returns
    -------
    DataFrame
        A LMS Assignments-formatted DataFrame

    Notes
    -----
    Assignment DataFrame columns are:
        AssignmentCategory: The category or type of assignment
        AssignmentDescription: The assignment description
        DueDateTime: The date and time the assignment is due
        EndDateTime: The end date and time for the assignment
        LMSSectionSourceSystemIdentifier: A unique numeric identifier assigned
            to the section
        MaxPoints: The maximum number of points a student may receive
        SourceSystem: The system code or name providing the assignment data
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to
            an assignment by the source system
        StartDateTime: The start date and time for the assignment
        Title: The assignment title or name
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
        CreateDate: Date this record was created in the extractor
        LastModifiedDate: Date this record was last updated in the extractor
    """

    if assignments_df.empty or sections_df.empty:
        return {}

    assert "id" in assignments_df.columns
    assert "name" in assignments_df.columns
    assert "description" in assignments_df.columns
    assert "created_at" in assignments_df.columns
    assert "updated_at" in assignments_df.columns
    assert "lock_at" in assignments_df.columns
    assert "unlock_at" in assignments_df.columns
    assert "due_at" in assignments_df.columns
    assert "submission_types" in assignments_df.columns
    assert "course_id" in assignments_df.columns
    assert "points_possible" in assignments_df.columns
    assert "CreateDate" in assignments_df.columns
    assert "LastModifiedDate" in assignments_df.columns

    assert "id" in sections_df.columns
    assert "course_id" in sections_df.columns

    assignments_df = assignments_df[
        [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
            "lock_at",
            "unlock_at",
            "course_id",
            "points_possible",
            "due_at",
            "submission_types",
            "CreateDate",
            "LastModifiedDate",
        ]
    ].copy()

    sections_df = sections_df[["id", "course_id"]].rename(
        columns={"id": "LMSSectionSourceSystemIdentifier"}
    )
    assignments_df = sections_df.merge(assignments_df, on="course_id").drop(
        columns=["course_id"]
    )

    assignments_df["SourceSystemIdentifier"] = assignments_df[
        ["LMSSectionSourceSystemIdentifier", "id"]
    ].agg("-".join, axis=1)

    assignments_df.drop(columns="id", inplace=True)

    assignments_df.rename(
        columns={
            "name": "Title",
            "description": "AssignmentDescription",
            "created_at": "SourceCreateDate",
            "updated_at": "SourceLastModifiedDate",
            "lock_at": "EndDateTime",
            "unlock_at": "StartDateTime",
            "points_possible": "MaxPoints",
            "due_at": "DueDateTime",
            "submission_types": "SubmissionType",
        },
        inplace=True,
    )

    assignments_df["AssignmentCategory"] = "assignment"
    assignments_df["SourceSystem"] = constants.SOURCE_SYSTEM

    assignments_df["LMSSectionSourceSystemIdentifier"] = assignments_df[
        "LMSSectionSourceSystemIdentifier"
    ].astype("string")

    assignments_df = assignments_df.drop_duplicates()

    # group by section id as a Dict of DataFrames
    result: Dict[str, DataFrame] = cast(
        Dict[str, DataFrame],
        dict(tuple(assignments_df.groupby(["LMSSectionSourceSystemIdentifier"]))),
    )

    return result
