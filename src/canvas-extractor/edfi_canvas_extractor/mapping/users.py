# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from pandas import DataFrame

from edfi_canvas_extractor.mapping import constants
from edfi_canvas_extractor.mapping.helpers import convert_to_standard_date_time_string


def map_to_udm_users(users_df: DataFrame) -> DataFrame:
    """
    Maps a DataFrame containing Canvas users into the Ed-Fi LMS Unified Data
    Model (UDM) format.

    Parameters
    ----------
    users_df: DataFrame
        Pandas DataFrame containing all Canvas users

    Returns
    -------
    DataFrame
        A LMSUsers-formatted DataFrame

    DataFrame columns are:
        EmailAddress: The primary e-mail address for the user
        LocalUserIdentifier: The user identifier assigned by a school or district
        Name: The full name of the user
        SISUserIdentifier: The user identifier defined in the Student Information System (SIS)
        SourceSystem: The system code or name providing the user data
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a user by the source system
        CreateDate: datetime at which the record was first retrieved
        LastModifiedDate: datetime when the record was modified, or when first retrieved
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
    """

    if users_df.empty:
        return users_df

    df: DataFrame = users_df[
        [
            "id",
            "sis_user_id",
            "created_at",
            "name",
            "email",
            "login_id",
            "CreateDate",
            "LastModifiedDate",
        ]
    ].copy()

    df["SourceSystem"] = constants.SOURCE_SYSTEM

    df.rename(
        columns={
            "id": "SourceSystemIdentifier",
            "sis_user_id": "SISUserIdentifier",
            "login_id": "LocalUserIdentifier",
            "email": "EmailAddress",
            "name": "Name",
            "created_at": "SourceCreateDate",
        },
        inplace=True,
    )

    convert_to_standard_date_time_string(df, "SourceCreateDate")
    df["UserRole"] = constants.ROLES.STUDENT

    df["SourceLastModifiedDate"] = ""

    return df
