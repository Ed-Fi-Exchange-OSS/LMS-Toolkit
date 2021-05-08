# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
from pandas import DataFrame

from . import constants


def map_to_udm_grades(grades_df: pd.DataFrame) -> pd.DataFrame:
    """
    Maps a DataFrame containing Canvas grades into the Ed-Fi LMS Unified Data
    Model (UDM) format.

    Parameters
    ----------
    grades_df: DataFrame
        Pandas DataFrame containing grades

    Returns
    -------
    DataFrame
        A LMSGrades-formatted DataFrame

    Notes
    -----
    DataFrame columns are:
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a
        grade by the source system.
        LMSUserIdentifier: A unique numeric identifier assigned to the user.
        SourceSystem: The system code or name providing the section data
        LMSSectionIdentifier: A unique numeric identifier assigned to the section.
        LMSGradeIdentifier: A unique numeric identifier assigned to the grade.
        GradeType: The type of grade reported. E.g., Current, Final.
        Grade: The user's letter or numeric grade for the section.
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
        CreateDate: Date this record was created in the extractor
        LastModifiedDate: Date this record was last updated in the extractor
    """

    if grades_df.empty:
        return grades_df

    assert "SourceSystemIdentifier" in grades_df.columns
    assert "LMSUserLMSSectionAssociationSourceSystemIdentifier" in grades_df.columns
    assert "final_score" in grades_df.columns
    assert "CreateDate" in grades_df.columns
    assert "LastModifiedDate" in grades_df.columns

    df: DataFrame = grades_df[
        [
            "SourceSystemIdentifier",
            "LMSUserLMSSectionAssociationSourceSystemIdentifier",
            "final_score",
            "CreateDate",
            "LastModifiedDate",
        ]
    ].copy()

    df.rename(
        columns={"final_score": "Grade"},
        inplace=True,
    )

    df["SourceSystem"] = constants.SOURCE_SYSTEM
    df["GradeType"] = "Final"
    df["SourceCreateDate"] = ""
    df["SourceLastModifiedDate"] = ""

    return df
