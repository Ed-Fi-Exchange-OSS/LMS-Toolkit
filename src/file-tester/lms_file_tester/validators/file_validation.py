# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
import sys
from typing import List

import pandas as pd

# The following is a hack to load a local package above this package's base
# directory, so that this test utility does not need to rely on downloading a
# published version of the LMS file utils.
sys.path.append(os.path.join("..", "file-utils"))
from lms_file_utils import file_reader as fread  # type: ignore # noqa: E402


def _validate_columns(expected: set, df: pd.DataFrame, file_type: str) -> List[str]:
    actual = set(df.columns)

    if actual == expected:
        return list()

    extra = actual.difference(expected)
    missing = expected.difference(extra)

    return [
        f"{file_type} file contains extra columns {extra} and is missing columns {missing}"
    ]


def validate_users_file(input_directory: str) -> List[str]:
    df = fread.get_all_users(input_directory, nrows=1)

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "UserRole",
            "LocalUserIdentifier",
            "SISUserIdentifier",
            "Name",
            "EmailAddress",
            "EntityStatus",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(expected, df, "Users")


def validate_sections_file(input_directory: str) -> List[str]:
    df = fread.get_all_sections(input_directory, nrows=1)

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "SISSectionIdentifier",
            "Title",
            "SectionDescription",
            "Term",
            "LMSSectionStatus",
            "EntityStatus",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(expected, df, "Sections")


def validate_system_activities_file(input_directory: str) -> List[str]:
    df = fread.get_all_system_activities(input_directory, nrows=1)

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "LMSUserSourceSystemIdentifier",
            "ActivityDateTime",
            "ActivityType",
            "ActivityStatus",
            "ParentSourceSystemIdentifier",
            "ActivityTimeInMinutes",
            "EntityStatus",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(expected, df, "System Activities")


def validate_section_associations_file(
    input_directory: str, sections: pd.DataFrame
) -> List[str]:
    df = fread.get_all_section_associations(input_directory, sections, nrows=1)

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "EnrollmentStatus",
            "StartDate",
            "EndDate",
            "LMSUserSourceSystemIdentifier",
            "LMSSectionSourceSystemIdentifier",
            "EntityStatus",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(expected, df, "Section Associations")


def validate_section_activities_file(
    input_directory: str, sections: pd.DataFrame
) -> List[str]:
    df = fread.get_all_section_activities(input_directory, sections, nrows=1)

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "ActivityType",
            "ActivityDateTime",
            "ActivityStatus",
            "MessagePost",
            "TotalActivityTimeInMinutes",
            "LMSSectionSourceSystemIdentifier",
            "UserSourceSystemIdentifier",
            "EntityStatus",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(expected, df, "Section Activities")


def validate_assignments_file(
    input_directory: str, sections: pd.DataFrame
) -> List[str]:
    df = fread.get_all_assignments(input_directory, sections, nrows=1)

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "Title",
            "AssignmentCategory",
            "AssignmentDescription",
            "StartDateTime",
            "EndDateTime",
            "DueDateTime",
            "SubmissionType",
            "MaxPoints",
            "LMSSectionSourceSystemIdentifier",
            "EntityStatus",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(expected, df, "Assignments")


def validate_submissions_file(
    input_directory: str, assignments: pd.DataFrame
) -> List[str]:
    df = fread.get_all_submissions(input_directory, assignments, nrows=1)

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "Title",
            "AssignmentCategory",
            "AssignmentDescription",
            "StartDateTime",
            "EndDateTime",
            "DueDateTime",
            "SubmissionType",
            "MaxPoints",
            "LMSSectionSourceSystemIdentifier",
            "EntityStatus",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(expected, df, "Submissions")


def validate_grades_file(input_directory: str, sections: pd.DataFrame) -> List[str]:
    df = fread.get_all_grades(input_directory, sections, nrows=1)

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "Grade",
            "GradeType",
            "LMSUserLMSSectionAssociationSourceSystemIdentifier",
            "EntityStatus",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(expected, df, "Grades")


def validate_attendance_events_file(
    input_directory: str, sections: pd.DataFrame
) -> List[str]:
    df = fread.get_all_attendance_events(input_directory, sections, nrows=1)

    expected = set(
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "Date",
            "AttendanceStatus",
            "SectionAssociationSystemIdentifier",
            "UserSourceSystemIdentifier",
            "UserLMSSectionAssociationSourceSystemIdentifier",
            "EntityStatus",
            "CreateDate",
            "LastModifiedDate",
            "SourceCreateDate",
            "SourceLastModifiedDate",
        ]
    )

    return _validate_columns(expected, df, "Grades")
