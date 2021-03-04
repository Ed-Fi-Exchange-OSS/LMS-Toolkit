# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd

from . import constants


def map_to_udm(users_df: pd.DataFrame, roles_df: pd.DataFrame) -> pd.DataFrame:
    """
    Maps a DataFrame containing Schoology users into the Ed-Fi LMS Unified Data
    Model (UDM) format.

    Parameters
    ----------
    users_df: DataFrame
        Pandas DataFrame containing all Schoology users
    roles_df: DataFrame
        Pandas DataFrame containing all Schoology roles

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

    df = users_df[
        [
            "uid",
            "role_id",
            "school_uid",
            "name_first",
            "name_middle",
            "name_last",
            "username",
            "primary_email",
            "CreateDate",
            "LastModifiedDate",
        ]
    ].copy()
    df["role_id"] = df["role_id"].astype("string")
    df["SourceSystem"] = constants.SOURCE_SYSTEM

    df.rename(
        columns={
            "uid": "SourceSystemIdentifier",
            "school_uid": "SISUserIdentifier",
            "username": "LocalUserIdentifier",
            "primary_email": "EmailAddress",
        },
        inplace=True,
    )
    df = df.merge(roles_df[["id", "title"]], left_on="role_id", right_on="id")
    df.rename(columns={"title": "UserRole"}, inplace=True)

    df["Name"] = df[["name_first", "name_middle", "name_last"]].apply(" ".join, axis=1)
    df["Name"] = df["Name"].apply(lambda x: x.replace("  ", " "))
    df["SourceCreateDate"] = ""
    df["SourceLastModifiedDate"] = ""

    df.drop(
        columns=["name_first", "name_middle", "name_last", "role_id", "id"],
        inplace=True,
    )

    return df
