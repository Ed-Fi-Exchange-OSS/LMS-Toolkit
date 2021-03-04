# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd

from . import constants


def map_to_udm(sections_df: pd.DataFrame) -> pd.DataFrame:
    """
    Maps a DataFrame containing Schoology sections into the Ed-Fi LMS Unified Data
    Model (UDM) format.

    Parameters
    ----------
    sections_df: DataFrame
        Pandas DataFrame containing Schoology sections

    Returns
    -------
    DataFrame
        A LMS-Sections-formatted DataFrame

    Notes
    -----
    DataFrame columns are:
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a user by the source system
        SourceSystem: The system code or name providing the user data
        SISSectionIdentifier: Section identifier as recorded in the student information system (SIS)
        Title: Section title
        SectionDescription: Section long description
        Term: Calendar / grading period term
        LMSSectionStatus: Status of the section in the learning management system (LMS)
        CreateDate: datetime at which the record was first retrieved
        LastModifiedDate: datetime when the record was modified, or when first retrieved
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
    """

    if sections_df.empty:
        return sections_df

    df = sections_df[
        [
            "id",
            "section_title",
            "description",
            "section_school_code",
            "active",
            "CreateDate",
            "LastModifiedDate",
        ]
    ].copy()

    df["SourceSystem"] = constants.SOURCE_SYSTEM
    df["SourceCreateDate"] = ""
    df["SourceLastModifiedDate"] = ""

    df.rename(
        columns={
            "id": "SourceSystemIdentifier",
            "section_title": "Title",
            "description": "SectionDescription",
            "section_school_code": "SISSectionIdentifier",
        },
        inplace=True,
    )

    # Schoology does not have a concept matching to "term"
    df["Term"] = None
    df["LMSSectionStatus"] = df["active"].apply(
        lambda x: constants.ACTIVE if x == 1 else constants.INACTIVE
    )

    df.drop(columns=["active"], inplace=True)

    return df
