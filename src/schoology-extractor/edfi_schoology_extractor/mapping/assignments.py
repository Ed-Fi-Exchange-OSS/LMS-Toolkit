# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime

import pandas as pd

from . import constants


def map_to_udm(assignments_df: pd.DataFrame, section_id: int) -> pd.DataFrame:
    """
    Maps a DataFrame containing Schoology assignments into the Ed-Fi LMS Unified Data
    Model (UDM) format.

    Parameters
    ----------
    assignments_df: DataFrame
        Pandas DataFrame containing Schoology assignments for a section
    section_id: int
        The Section ID to which the assignments belong

    Returns
    -------
    DataFrame
        A LMSUsers-formatted DataFrame

    Notes
    -----
    DataFrame columns are:
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a user by the source system
        SourceSystem: The system code or name providing the user data
        Title: Assignment's title
        AssignmentCategory: Category/type of assignment
        AssignmentDescription: Full text description of the assignment
        StartDateTime: Date/time stamp when the assignment opens
        EndDateTime: Date/time stamp when the assignment closes
        DueDateTime: Date/time stamp when the assignment is due for full credit
        SubmissionType: Type of submission
        MaxPoints: Maximum points available for the submission
        LMSSectionSourceSystemIdentifier: Section identifier as recorded in the LMS
        CreateDate: datetime at which the record was first retrieved
        LastModifiedDate: datetime when the record was modified, or when first retrieved
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
    """

    if assignments_df.empty:
        return assignments_df

    df = assignments_df[
        [
            "id",
            "title",
            "description",
            "due",
            "max_points",
            "type",
            "CreateDate",
            "LastModifiedDate",
        ]
    ].copy()

    df["SourceSystem"] = constants.SOURCE_SYSTEM

    df.rename(
        columns={
            "id": "SourceSystemIdentifier",
            "title": "Title",
            "description": "AssignmentDescription",
            "max_points": "MaxPoints",
            "type": "AssignmentCategory",
            "due": "DueDateTime",
        },
        inplace=True,
    )

    df["DueDateTime"] = df["DueDateTime"].apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    )
    df["LMSSectionSourceSystemIdentifier"] = section_id

    df["SubmissionType"] = None
    df["SourceCreateDate"] = ""
    df["SourceLastModifiedDate"] = ""
    df["StartDateTime"] = ""
    df["EndDateTime"] = ""

    return df
