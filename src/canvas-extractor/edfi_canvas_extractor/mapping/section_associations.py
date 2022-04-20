# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from pandas import DataFrame

from edfi_canvas_extractor.mapping.constants import SOURCE_SYSTEM
from edfi_canvas_extractor.mapping.helpers import convert_to_standard_date_time_string


def _get_enrollment_status(status: str) -> str:
    if status == "active":
        return "Active"
    if status == "invited":
        return "Invite pending"
    if status == "inactive":
        return "Archived"
    return "Archived"


def map_to_udm_section_associations(enrollments_df: DataFrame) -> DataFrame:
    """
    Maps a DataFrame containing Canvas enrollments into the Ed-Fi LMS Unified Data
    Model (UDM) format.

    Parameters
    ----------
    enrollments_df: DataFrame
        Pandas DataFrame containing all Canvas enrollments

    Returns
    -------
    DataFrame
        A LMSSectionAssociations-formatted DataFrame

    DataFrame columns are:
        SourceSystemIdentifier: A unique number or alphanumeric code assigned to a the section-association by
            the source system
        SourceSystem: The system code or name providing the user data
        EnrollmentStatus: Possible values are Active, Expired, Invite pending, Request Pending, Archived
        LMSUserSourceSystemIdentifier: A unique number or alphanumeric code assigned to a user by the source
            system
        LMSSectionSourceSystemIdentifier: A unique number or alphanumeric code assigned to a section by the
            source system
        CreateDate: Date/time at which the record was first retrieved
        LastModifiedDate: Date/time when the record was modified, or when first retrieved
        SourceCreateDate: Date this record was created in the LMS
        SourceLastModifiedDate: Date this record was last updated in the LMS
    """

    if enrollments_df.empty:
        return enrollments_df

    assert "id" in enrollments_df.columns
    assert "enrollment_state" in enrollments_df.columns
    assert "user_id" in enrollments_df.columns
    assert "course_section_id" in enrollments_df.columns
    assert "created_at" in enrollments_df.columns
    assert "updated_at" in enrollments_df.columns

    enrollments_df = enrollments_df[
        [
            "id",
            "enrollment_state",
            "user_id",
            "course_section_id",
            "created_at",
            "updated_at",
            "CreateDate",
            "LastModifiedDate",
        ]
    ].copy()

    enrollments_df.rename(
        columns={
            "id": "SourceSystemIdentifier",
            "enrollment_state": "EnrollmentStatus",
            "user_id": "LMSUserSourceSystemIdentifier",
            "course_section_id": "LMSSectionSourceSystemIdentifier",
            "created_at": "SourceCreateDate",
            "updated_at": "SourceLastModifiedDate",
        },
        inplace=True,
    )

    convert_to_standard_date_time_string(enrollments_df, "SourceCreateDate")
    convert_to_standard_date_time_string(enrollments_df, "SourceLastModifiedDate")

    enrollments_df["EnrollmentStatus"] = enrollments_df["EnrollmentStatus"].apply(
        _get_enrollment_status
    )

    enrollments_df["SourceSystem"] = SOURCE_SYSTEM

    return enrollments_df
