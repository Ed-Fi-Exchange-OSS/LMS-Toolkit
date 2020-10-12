# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict, Optional
from datetime import datetime
import pandas as pd
from google_classroom_extractor.mapping.constants import (
    SOURCE_SYSTEM,
    ENTITY_STATUS_ACTIVE,
)


def coursework_to_assignments_dfs(
    coursework_df: pd.DataFrame,
) -> Dict[str, pd.DataFrame]:
    """
    Convert a Coursework API DataFrame to a Dict of Assignment UDM DataFrames
    grouped by source system section id pairs

    Parameters
    ----------
    coursework_df: DataFrame
        is a Coursework API DataFrame

    Returns
    -------
    Dict[str, DataFrame]
        LMS UDM Assignment DataFrames grouped by source system section id

    Assignment DataFrame columns are:
        AssignmentCategory: The category or type of assignment
        AssignmentDescription: The assignment description
        DueDateTime: The date and time the assignment is due
        EndDateTime: The end date and time for the assignment
        EntityStatus: The status of the record
        MaxPoints: The maximum number of points a student may receive
        SourceSystem: The system code or name providing the assignment data
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to
            an assignment by the source system
        StartDateTime: The start date and time for the assignment
        Title: The assignment title or name
        CreateDate: Date this record was created
        LastModifiedDate: Date this record was last updated
    """
    assert isinstance(coursework_df, pd.DataFrame)
    assert "courseId" in coursework_df.columns
    assert "id" in coursework_df.columns
    assert "workType" in coursework_df.columns
    assert "description" in coursework_df.columns
    assert "scheduledTime" in coursework_df.columns
    assert "maxPoints" in coursework_df.columns
    assert "title" in coursework_df.columns
    assert "dueDate.year" in coursework_df.columns
    assert "dueDate.month" in coursework_df.columns
    assert "dueDate.day" in coursework_df.columns
    assert "dueTime.hours" in coursework_df.columns
    assert "dueTime.minutes" in coursework_df.columns

    if {
        "dueDate.year",
        "dueDate.month",
        "dueDate.day",
        "dueTime.hours",
        "dueTime.minutes",
    }.issubset(coursework_df.columns):
        due_date_df: pd.DataFrame = coursework_df[
            [
                "dueDate.year",
                "dueDate.month",
                "dueDate.day",
                "dueTime.hours",
                "dueTime.minutes",
            ]
        ]
        filled_df: Optional[pd.DataFrame] = due_date_df.fillna("0")
        if filled_df is None:
            raise ValueError  # fillna will never return None in this usage
        coursework_df["DueDateTime"] = filled_df.apply(
            lambda date_element: datetime(*pd.to_numeric(date_element, downcast="integer")),
            axis=1,
        )
    else:
        coursework_df["DueDateTime"] = ""

    coursework_df["SourceSystemIdentifier"] = coursework_df[["courseId", "id"]].agg(
        ":".join, axis=1
    )

    assignments_df: pd.DataFrame = coursework_df[
        [
            "courseId",
            "workType",
            "description",
            "scheduledTime",
            "maxPoints",
            "title",
            "creationTime",
            "updateTime",
            "DueDateTime",
            "SourceSystemIdentifier",
        ]
    ]

    assignments_df = assignments_df.rename(
        columns={
            "courseId": "SourceSystemSectionIdentifier",
            "workType": "AssignmentCategory",
            "description": "AssignmentDescription",
            "scheduledTime": "StartDateTime",
            "maxPoints": "MaxPoints",
            "title": "Title",
            "creationTime": "CreateDate",
            "updateTime": "LastModifiedDate",
        }
    )

    assignments_df["SourceSystem"] = SOURCE_SYSTEM
    assignments_df["EntityStatus"] = ENTITY_STATUS_ACTIVE
    assignments_df["EndDateTime"] = ""  # No EndDateTime available from API

    # group by section id as a Dict of DataFrames
    result: Dict[str, pd.DataFrame] = dict(
        tuple(assignments_df.groupby(["SourceSystemSectionIdentifier"]))
    )

    # no longer need group by column
    for grouped_df in result.values():
        grouped_df.drop(columns=["SourceSystemSectionIdentifier"], inplace=True)

    return result