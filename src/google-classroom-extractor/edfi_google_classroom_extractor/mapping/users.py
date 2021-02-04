# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from pandas import DataFrame, concat
from edfi_google_classroom_extractor.mapping.constants import SOURCE_SYSTEM


STUDENT_USER_ROLE = "Student"
TEACHER_USER_ROLE = "Teacher"


def _students_or_teachers_to_users_df(
    students_or_teachers_df: DataFrame, lms_udm_user_role: str
) -> DataFrame:
    """
    Convert a Students or Teachers API DataFrame to a LMSUsers DataFrame

    Parameters
    ----------
    students_or_teachers_df: DataFrame
        is a Students or Teachers API DataFrame
    lms_udm_user_role
        is the LMS UDM user role as a string

    Returns
    -------
    DataFrame
        a LMSUsers DataFrame based on the given Students or Teachers API DataFrame

    Notes
    -----
    DataFrame columns are:
        EmailAddress: The primary e-mail address for the user
        LocalUserIdentifier: The user identifier assigned by a school or district
        Name: The full name of the user
        SISUserIdentifier: The user identifier defined in the Student Information System (SIS)
        SourceSystem: The system code or name providing the user data
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a user by the source system
        UserRole: The role assigned to the user
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
        CreateDate: Date this record was created in the extractor
        LastModifiedDate: Date this record was last updated in the extractor
    """
    assert "userId" in students_or_teachers_df.columns
    assert "profile.name.fullName" in students_or_teachers_df.columns
    assert "profile.emailAddress" in students_or_teachers_df.columns

    result: DataFrame = students_or_teachers_df[
        [
            "userId",
            "profile.name.fullName",
            "profile.emailAddress",
            "CreateDate",
            "LastModifiedDate",
        ]
    ]
    result = result.rename(
        columns={
            "userId": "SourceSystemIdentifier",
            "profile.name.fullName": "Name",
            "profile.emailAddress": "EmailAddress",
        }
    )

    # Student records are per-course, so there may be duplicates
    result.drop_duplicates(inplace=True)
    result["SourceSystem"] = SOURCE_SYSTEM
    result["UserRole"] = lms_udm_user_role

    result["LocalUserIdentifier"] = ""  # No local id available from API
    result["SISUserIdentifier"] = ""  # No SIS id available from API
    result["SourceCreateDate"] = ""  # No create date available from API
    result["SourceLastModifiedDate"] = ""  # No modified date available from API

    return result


def students_and_teachers_to_users_df(
    students_df: DataFrame, teachers_df: DataFrame
) -> DataFrame:
    """
    Convert Students and Teachers API DataFrames to an LMS UDM DataFrame

    Parameters
    ----------
    students_df: DataFrame
        is a Students API DataFrame
    teachers_df: DataFrame
        is a Teachers API DataFrame

    Returns
    -------
    DataFrame
        a LMSUsers DataFrame based on the given Students and Teachers API DataFrames

    Notes
    -----
    DataFrame columns are:
        EmailAddress: The primary e-mail address for the user
        LocalUserIdentifier: The user identifier assigned by a school or district
        Name: The full name of the user
        SISUserIdentifier: The user identifier defined in the Student Information System (SIS)
        SourceSystem: The system code or name providing the user data
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a user by the source system
        UserRole: The role assigned to the user
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
        CreateDate: Date this record was created in the extractor
        LastModifiedDate: Date this record was last updated in the extractor
    """
    assert "userId" in students_df.columns
    assert "profile.name.fullName" in students_df.columns
    assert "profile.emailAddress" in students_df.columns

    assert "userId" in teachers_df.columns
    assert "profile.name.fullName" in teachers_df.columns
    assert "profile.emailAddress" in teachers_df.columns

    users_from_students_df: DataFrame = _students_or_teachers_to_users_df(
        students_df, STUDENT_USER_ROLE
    )
    users_from_teachers_df: DataFrame = _students_or_teachers_to_users_df(
        teachers_df, TEACHER_USER_ROLE
    )

    return concat(
        [users_from_students_df, users_from_teachers_df], ignore_index=True, sort=False
    )
