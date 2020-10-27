# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd

from . import constants


def _map_status_code_to_string(status_code: int) -> str:
    switcher = {
        1: "Active",
        2: "Expired",
        3: "Invite pending",
        4: "Request pending",
        5: "Archived",
    }
    return switcher.get(status_code, f"Unknown status: {status_code}")


def map_to_udm(enrollments_df: pd.DataFrame, section_id: int) -> pd.DataFrame:
    """
    Maps a DataFrame containing Schoology section associations (enrollments)
    into the Ed-Fi LMS Unified Data Model (UDM) format.

    Parameters
    ----------
    enrollments_df: DataFrame
        Pandas DataFrame containing Schoology assignments for a section

    Returns
    -------
    DataFrame
        A LMSUsers-formatted DataFrame

    Notes
    -----
    DataFrame columns are:
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a the section-association by
            the source system
        SourceSystem: The system code or name providing the user data
        EnrollmentStatus: Possible values are Active, Expired, Invite pending, Request Pending, Archived
        StartDate: Date when the section-association becomes Active
        EndDate: Date when the section-association changes from Active to another status
        UserSourceSystemIdentifier: A unique number or alphanumeric code assigned to a user by the source
            system
        LMSSectionSourceSystemIdentifier: A unique number or alphanumeric code assigned to a section by the
            source system
        EntityStatus: The status of the record
        CreateDate: Date/time at which the record was first retrieved
        LastModifieDate: Date/time when the record was modified, or when first retrieved
    """

    df = enrollments_df[["id", "uid", "status"]].copy()

    df["SourceSystem"] = constants.SOURCE_SYSTEM
    df["EntityStatus"] = constants.ACTIVE
    df["LMSSectionSourceSystemIdentifier"] = section_id

    df.rename(
        columns={
            "id": "SourceSystemIdentifier",
            "uid": "UserSourceSystemIdentifier",
            "status": "EnrollmentStatus",
        },
        inplace=True,
    )

    df["EnrollmentStatus"] = df["EnrollmentStatus"].apply(
        lambda x: _map_status_code_to_string(int(x))
    )

    # TODO: set these via the sync process
    df["StartDate"] = None
    df["EndDate"] = None
    df["CreateDate"] = None
    df["LastModifiedDate"] = None

    return df
