# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict
from pandas import DataFrame, concat
from edfi_google_classroom_extractor.mapping.constants import SOURCE_SYSTEM

ENROLLMENT_STATUS_ACTIVE = "Active"


def _students_or_teachers_to_user_section_associations_df(
    students_or_teachers_df: DataFrame,
) -> DataFrame:
    """
    Convert a Student or Teacher API DataFrame to a UserSectionAssociation DataFrame

    Parameters
    ----------
    students_or_teachers_df: DataFrame
        is a Students or Teachers API DataFrame

    Returns
    -------
    DataFrame
        a UserSectionAssociation DataFrame based on the given Students or Teachers API DataFrame

    Notes
    -----
    UserSectionAssociation DataFrame columns are:
        EndDate: Month, day, and year of the user's withdrawal or exit from the section
        EnrollmentStatus: The status of the user section association. E.g., Active,
            Inactive, Withdrawn
        LMSSectionIdentifier: A unique numeric identifier assigned to the section
        SourceSystem: The system code or name providing the user data
        SourceSystemIdentifier: A unique number or alphanumeric code
            assigned to a user by the source system
        StartDate: Month, day, and year of the user's entry or assignment to the section
        LMSUserIdentifier: A unique numeric identifier assigned to the user
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
        CreateDate: Date this record was created in the extractor
        LastModifiedDate: Date this record was last updated in the extractor
    """
    assert "userId" in students_or_teachers_df.columns
    assert "courseId" in students_or_teachers_df.columns

    user_section_associations_df: DataFrame = students_or_teachers_df[
        [
            "userId",
            "courseId",
            "CreateDate",
            "LastModifiedDate",
        ]
    ]

    user_section_associations_df = user_section_associations_df.rename(
        columns={
            "userId": "LMSUserIdentifier",
            "courseId": "LMSSectionIdentifier",
        }
    )

    user_section_associations_df[
        "SourceSystemIdentifier"
    ] = user_section_associations_df[["LMSUserIdentifier", "LMSSectionIdentifier"]].agg(
        "-".join, axis=1
    )

    user_section_associations_df["SourceSystem"] = SOURCE_SYSTEM
    user_section_associations_df["EnrollmentStatus"] = ENROLLMENT_STATUS_ACTIVE
    user_section_associations_df[
        "StartDate"
    ] = ""  # No enrollment start date available from API
    user_section_associations_df[
        "EndDate"
    ] = ""  # No enrollment end date available from API
    user_section_associations_df["SourceCreateDate"] = ""  # No create date available from API
    user_section_associations_df[
        "SourceLastModifiedDate"
    ] = ""  # No modified date available from API
    return user_section_associations_df


def students_and_teachers_to_user_section_associations_dfs(
    students_df: DataFrame, teachers_df: DataFrame
) -> Dict[str, DataFrame]:
    """
    Convert Student and Teacher API DataFrames to a Dict of
    UserSectionAssociation UDM DataFrames grouped by source system
    section id

    Parameters
    ----------
    students_df: DataFrame
        is a Students API DataFrame
    teachers_df: DataFrame
        is a Students API DataFrame

    Returns
    -------
    Dict[str, DataFrame]
        LMS UDM UserSectionAssociation DataFrames grouped by
            source system section id

    Notes
    -----
    UserSectionAssociation DataFrame columns are:
        EndDate: Month, day, and year of the user's withdrawal or exit from the section
        EnrollmentStatus: The status of the user section association. E.g., Active,
            Inactive, Withdrawn
        LMSSectionIdentifier: A unique numeric identifier assigned to the section
        SourceSystem: The system code or name providing the user data
        SourceSystemIdentifier: A unique number or alphanumeric code
            assigned to a user by the source system
        StartDate: Month, day, and year of the user's entry or assignment to the section
        LMSUserIdentifier: A unique numeric identifier assigned to the user
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
        CreateDate: Date this record was created in the extractor
        LastModifiedDate: Date this record was last updated in the extractor
    """
    assert "userId" in students_df.columns
    assert "courseId" in students_df.columns
    assert "userId" in teachers_df.columns
    assert "courseId" in teachers_df.columns

    associations_from_students_df: DataFrame = (
        _students_or_teachers_to_user_section_associations_df(
            students_df,
        )
    )
    associations_from_teachers_df: DataFrame = (
        _students_or_teachers_to_user_section_associations_df(
            teachers_df,
        )
    )

    user_section_associations_df = concat(
        [associations_from_students_df, associations_from_teachers_df],
        ignore_index=True,
        sort=False,
    )

    # group by section id as a Dict of DataFrames
    result: Dict[str, DataFrame] = dict(
        tuple(
            user_section_associations_df.groupby(
                [
                    "LMSSectionIdentifier",
                ]
            )
        )
    )

    return result
