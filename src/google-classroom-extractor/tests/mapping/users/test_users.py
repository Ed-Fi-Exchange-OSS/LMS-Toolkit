# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
from pandas import DataFrame
from google_classroom_extractor.mapping.users import (
    students_and_teachers_to_users_df,
    STUDENT_USER_ROLE,
    TEACHER_USER_ROLE,
)
from google_classroom_extractor.mapping.constants import (
    SOURCE_SYSTEM,
    ENTITY_STATUS_ACTIVE,
)

# unique value for each column in fixture
STUDENT_COURSE_ID = "1"
STUDENT_USER_ID = "2"
STUDENT_PROFILE_ID = "3"
STUDENT_GIVEN_NAME = "4"
STUDENT_FAMILY_NAME = "5"
STUDENT_FULL_NAME = "6"
STUDENT_EMAIL_ADDRESS = "7"

TEACHER_COURSE_ID = "8"
TEACHER_USER_ID = "9"
TEACHER_PROFILE_ID = "10"
TEACHER_GIVEN_NAME = "11"
TEACHER_FAMILY_NAME = "12"
TEACHER_FULL_NAME = "13"
TEACHER_EMAIL_ADDRESS = "14"


def describe_when_a_single_student_and_single_teacher_with_unique_fields_is_mapped():
    @pytest.fixture
    def users_df() -> DataFrame:
        # arrange
        students_df = DataFrame(
            {
                "courseId": [STUDENT_COURSE_ID],
                "userId": [STUDENT_USER_ID],
                "profile.id": [STUDENT_PROFILE_ID],
                "profile.name.givenName": [STUDENT_GIVEN_NAME],
                "profile.name.familyName": [STUDENT_FAMILY_NAME],
                "profile.name.fullName": [STUDENT_FULL_NAME],
                "profile.emailAddress": [STUDENT_EMAIL_ADDRESS],
            }
        )

        teachers_df = DataFrame(
            {
                "courseId": [TEACHER_COURSE_ID],
                "userId": [TEACHER_USER_ID],
                "profile.id": [TEACHER_PROFILE_ID],
                "profile.name.givenName": [TEACHER_GIVEN_NAME],
                "profile.name.familyName": [TEACHER_FAMILY_NAME],
                "profile.name.fullName": [TEACHER_FULL_NAME],
                "profile.emailAddress": [TEACHER_EMAIL_ADDRESS],
            }
        )

        # act
        return students_and_teachers_to_users_df(students_df, teachers_df)

    def it_should_have_correct_shape(users_df):
        row_count, column_count = users_df.shape
        assert row_count == 2
        assert column_count == 10

    def it_should_have_complete_student_mapping_as_first_row(users_df):
        student_row_dict = users_df.to_dict(orient="records")[0]
        assert student_row_dict["SourceSystemIdentifier"] == STUDENT_USER_ID
        assert student_row_dict["Name"] == STUDENT_FULL_NAME
        assert student_row_dict["EmailAddress"] == STUDENT_EMAIL_ADDRESS
        assert student_row_dict["SourceSystem"] == SOURCE_SYSTEM
        assert student_row_dict["UserRole"] == STUDENT_USER_ROLE
        assert student_row_dict["EntityStatus"] == ENTITY_STATUS_ACTIVE
        assert student_row_dict["LocalUserIdentifier"] == ""
        assert student_row_dict["SISUserIdentifier"] == ""
        assert student_row_dict["SourceCreateDate"] == ""
        assert student_row_dict["SourceLastModifiedDate"] == ""

    def it_should_have_complete_teacher_mapping_as_second_row(users_df):
        teacher_row_dict = users_df.to_dict(orient="records")[1]
        assert teacher_row_dict["SourceSystemIdentifier"] == TEACHER_USER_ID
        assert teacher_row_dict["Name"] == TEACHER_FULL_NAME
        assert teacher_row_dict["EmailAddress"] == TEACHER_EMAIL_ADDRESS
        assert teacher_row_dict["SourceSystem"] == SOURCE_SYSTEM
        assert teacher_row_dict["UserRole"] == TEACHER_USER_ROLE
        assert teacher_row_dict["EntityStatus"] == ENTITY_STATUS_ACTIVE
        assert teacher_row_dict["LocalUserIdentifier"] == ""
        assert teacher_row_dict["SISUserIdentifier"] == ""
        assert teacher_row_dict["SourceCreateDate"] == ""
        assert teacher_row_dict["SourceLastModifiedDate"] == ""
