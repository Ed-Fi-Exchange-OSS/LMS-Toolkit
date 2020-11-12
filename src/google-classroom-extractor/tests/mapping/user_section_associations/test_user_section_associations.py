# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict
import pytest
from pandas import DataFrame
from google_classroom_extractor.mapping.user_section_associations import (
    students_and_teachers_to_user_section_associations_dfs,
    ENROLLMENT_STATUS_ACTIVE,
)
from google_classroom_extractor.mapping.constants import (
    SOURCE_SYSTEM,
    ENTITY_STATUS_ACTIVE,
)

# unique value for each column in fixture
COURSE_ID = "1"
STUDENT_USER_ID = "2"
TEACHER_USER_ID = "3"


def describe_when_a_single_student_and_single_teacher_with_unique_fields_is_mapped():
    @pytest.fixture
    def associations_dicts() -> Dict[str, DataFrame]:
        # arrange
        students_df = DataFrame(
            {
                "courseId": [COURSE_ID],
                "userId": [STUDENT_USER_ID],
            }
        )

        teachers_df = DataFrame(
            {
                "courseId": [COURSE_ID],
                "userId": [TEACHER_USER_ID],
            }
        )

        # act
        return students_and_teachers_to_user_section_associations_dfs(
            students_df, teachers_df
        )

    def it_should_have_correct_shape(associations_dicts):
        assert len(associations_dicts) == 1

        association_df: DataFrame = associations_dicts[COURSE_ID]
        row_count, column_count = association_df.shape

        assert row_count == 2
        assert column_count == 10

    def it_should_map_student_fields_correctly(associations_dicts):
        association_df: DataFrame = associations_dicts[COURSE_ID]
        row_dict = association_df.to_dict(orient="records")[0]

        assert row_dict["LMSUserIdentifier"] == STUDENT_USER_ID
        assert row_dict["LMSSectionIdentifier"] == COURSE_ID
        assert row_dict["SourceSystem"] == SOURCE_SYSTEM
        assert row_dict["SourceSystemIdentifier"] == f"{STUDENT_USER_ID}-{COURSE_ID}"
        assert row_dict["EntityStatus"] == ENTITY_STATUS_ACTIVE
        assert row_dict["EnrollmentStatus"] == ENROLLMENT_STATUS_ACTIVE
        assert row_dict["StartDate"] == ""
        assert row_dict["EndDate"] == ""
        assert row_dict["SourceCreateDate"] == ""
        assert row_dict["SourceLastModifiedDate"] == ""

    def it_should_map_teacher_fields_correctly(associations_dicts):
        association_df: DataFrame = associations_dicts[COURSE_ID]
        row_dict = association_df.to_dict(orient="records")[1]

        assert row_dict["LMSUserIdentifier"] == TEACHER_USER_ID
        assert row_dict["LMSSectionIdentifier"] == COURSE_ID
        assert row_dict["SourceSystem"] == SOURCE_SYSTEM
        assert row_dict["SourceSystemIdentifier"] == f"{TEACHER_USER_ID}-{COURSE_ID}"
        assert row_dict["EntityStatus"] == ENTITY_STATUS_ACTIVE
        assert row_dict["EnrollmentStatus"] == ENROLLMENT_STATUS_ACTIVE
        assert row_dict["StartDate"] == ""
        assert row_dict["EndDate"] == ""
        assert row_dict["SourceCreateDate"] == ""
        assert row_dict["SourceLastModifiedDate"] == ""


def describe_when_users_in_different_courses_are_mapped():
    course2_id = "course2_id"

    @pytest.fixture
    def associations_dicts() -> Dict[str, DataFrame]:
        # arrange
        students_df = DataFrame(
            {
                "courseId": [COURSE_ID],
                "userId": [STUDENT_USER_ID],
            }
        )

        teachers_df = DataFrame(
            {
                "courseId": [course2_id],
                "userId": [TEACHER_USER_ID],
            }
        )

        # act
        return students_and_teachers_to_user_section_associations_dfs(
            students_df, teachers_df
        )

    def it_should_have_two_courses(associations_dicts):
        assert len(associations_dicts) == 2

    def it_should_have_one_association_for_first_course(
        associations_dicts,
    ):
        association_df: DataFrame = associations_dicts[COURSE_ID]
        row_count, _ = association_df.shape

        assert row_count == 1

    def it_should_have_one_association_for_second_course(
        associations_dicts,
    ):
        association_df: DataFrame = associations_dicts[course2_id]
        row_count, _ = association_df.shape

        assert row_count == 1

    def it_should_have_correct_user_id_in_first_course(
        associations_dicts,
    ):
        association_df: DataFrame = associations_dicts[COURSE_ID]
        course1_dict = association_df.to_dict(orient="records")[0]

        assert course1_dict["LMSUserIdentifier"] == STUDENT_USER_ID

    def it_should_have_correct_user_id_in_second_course(
        associations_dicts,
    ):
        association_df: DataFrame = associations_dicts[course2_id]
        course2_dict = association_df.to_dict(orient="records")[0]

        assert course2_dict["LMSUserIdentifier"] == TEACHER_USER_ID
