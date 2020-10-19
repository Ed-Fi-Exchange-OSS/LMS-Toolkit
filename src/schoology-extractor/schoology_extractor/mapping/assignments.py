# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime

import pandas as pd

from . import constants


def map_to_udm(assignments_df: pd.DataFrame) -> pd.DataFrame:
    """
    Maps a DataFrame containing Schoology assignments into the Ed-Fi LMS Unified Data
    Model (UDM) format.

    Parameters
    ----------
    assignments_df: DataFrame
        Pandas DataFrame containing Schoology assignments for a section

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
        EntityStatus: The status of the record
        CreateDate: datetime at which the record was first retrieved
        LastModifieDate: datetime when the record was modified, or when first retrieved
    """

    df = assignments_df[
        [
            "id",
            "title",
            "description",
            "due",
            "max_points",
            "section_id",
            "type"
        ]
    ].copy()

    df["SourceSystem"] = constants.SOURCE_SYSTEM
    df["EntityStatus"] = constants.ACTIVE

    df.rename(
        columns={
            "id": "SourceSystemIdentifier",
            "title": "Title",
            "description": "AssignmentDescription",
            "max_points": "MaxPoints",
            "section_id": "LMSSectionSourceSystemIdentifier",
            "type": "AssignmentCategory"
        },
        inplace=True,
    )

    df["DueDateTime"] = df["due"].apply(lambda x: datetime.strptime(x, "%m/%d/%Y  %I:%M:%S %p").strftime("%Y-%m-%d %H:%M:%S"))
    df.drop(columns=["due"], inplace=True)

    df["SubmissionType"] = None
    df["CreateDate"] = None
    df["LastModifiedDate"] = None

    return df
