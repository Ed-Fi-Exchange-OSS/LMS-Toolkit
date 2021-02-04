# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from pandas import DataFrame
from edfi_google_classroom_extractor.mapping.constants import SOURCE_SYSTEM


def courses_to_sections_df(courses_df: DataFrame) -> DataFrame:
    """
    Convert a Courses API DataFrame to an LMSSections UDM DataFrame

    Parameters
    ----------
    courses_df: DataFrame
        is a Courses API DataFrame

    Returns
    -------
    DataFrame
        a LMSSections DataFrame based on the given Courses API DataFrame

    Notes
    -----
    DataFrame columns are:
        LMSSectionStatus: The section status from the source system
        SISSectionIdentifier: The section identifier defined in the Student Information System
        SectionDescription: The section description
        SourceSystem: The system code or name providing the section data
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a user by the source system
        Term: The enrollment term for the section
        Title: The section title or name
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
        CreateDate: Date this record was created in the extractor
        LastModifiedDate: Date this record was last updated in the extractor
    """
    assert "id" in courses_df.columns
    assert "courseState" in courses_df.columns
    assert "descriptionHeading" in courses_df.columns
    assert "name" in courses_df.columns

    result: DataFrame = courses_df[
        [
            "id",
            "courseState",
            "descriptionHeading",
            "name",
            "creationTime",
            "updateTime",
            "CreateDate",
            "LastModifiedDate"
        ]
    ]
    result = result.rename(
        columns={
            "id": "SourceSystemIdentifier",
            "courseState": "LMSSectionStatus",
            "descriptionHeading": "SectionDescription",
            "name": "Title",
            "creationTime": "SourceCreateDate",
            "updateTime": "SourceLastModifiedDate",
        }
    )

    result["SourceSystem"] = SOURCE_SYSTEM
    result["SISSectionIdentifier"] = ""  # No SIS id available from API
    result["Term"] = ""  # No term available from API

    return result
