# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Dict
import pytest
from pandas import DataFrame
from edfi_canvas_extractor.mapping.assignments import map_to_udm_assignments
from edfi_canvas_extractor.mapping.constants import SOURCE_SYSTEM


# unique value for each column in assignment
ID = "1"
DESCRIPTION = "2"
DUE_AT = "3"
UNLOCK_AT = "4"
LOCK_AT = "5"
POINTS_POSSIBLE = "6"
GRADING_TYPE = "7"
ASSIGNMENT_GROUP_ID = "8"
GRADING_STANDARD_ID = "9"
CREATED_AT = "10"
CREATED_AT_DATE = "11"
UPDATED_AT = "12"
UPDATED_AT_DATE = "13"
PEER_REVIEWS = "14"
AUTOMATIC_PEER_REVIEWS = "15"
POSITION = "16"
GRADE_GROUP_STUDENTS_INDIVIDUALLY = "17"
ANONYMOUS_PEER_REVIEWS = "18"
GROUP_CATEGORY_ID = "19"
POST_TO_SIS = "20"
MODERATED_GRADING = "21"
OMIT_FROM_FINAL_GRADE = "22"
INTRA_GROUP_PEER_REVIEWS = "23"
ANONYMOUS_INSTRUCTOR_ANNOTATIONS = "24"
ANONYMOUS_GRADING = "25"
GRADERS_ANONYMOUS_TO_GRADERS = "26"
GRADER_COUNT = "27"
GRADER_COMMENTS_VISIBLE_TO_GRADERS = "28"
FINAL_GRADER_ID = "29"
GRADER_NAMES_VISIBLE_TO_FINAL_GRADER = "30"
ALLOWED_ATTEMPTS = "31"
SECURE_PARAMS = "32"
COURSE_ID = "33"
NAME = "34"
SUBMISSION_TYPES = "35"
HAS_SUBMITTED_SUBMISSIONS = "36"
DUE_DATE_REQUIRED = "37"
MAX_NAME_LENGTH = "38"
IN_CLOSED_GRADING_PERIOD = "39"
IS_QUIZ_ASSIGNMENT = "40"
CAN_DUPLICATE = "41"
ORIGINAL_COURSE_ID = "42"
ORIGINAL_ASSIGNMENT_ID = "43"
ORIGINAL_ASSIGNMENT_NAME = "44"
ORIGINAL_QUIZ_ID = "45"
WORKFLOW_STATE = "46"
MUTED = "47"
HTML_URL = "48"
HAS_OVERRIDES = "49"
NEEDS_GRADING_COUNT = "50"
SIS_ASSIGNMENT_ID = "51"
INTEGRATION_ID = "52"
INTEGRATION_DATA = "53"
DISCUSSION_TOPIC = "54"
PUBLISHED = "55"
UNPUBLISHABLE = "56"
ONLY_VISIBLE_TO_OVERRIDES = "57"
LOCKED_FOR_USER = "58"
SUBMISSIONS_DOWNLOAD_URL = "59"
POST_MANUALLY = "60"
ANONYMIZE_STUDENTS = "61"
REQUIRE_LOCKDOWN_BROWSER = "62"
EXTERNAL_TOOL_TAG_ATTRIBUTES = "63"
URL = "64"
QUIZ_ID = "65"
ANONYMOUS_SUBMISSIONS = "66"
USE_RUBRIC_FOR_GRADING = "67"
FREE_FORM_CRITERION_COMMENTS = "68"
RUBRIC = "69"
RUBRIC_SETTINGS = "70"
DUE_AT_DATE = "71"
CREATE_DATE = "72"
LAST_MODIFIED_DATE = "73"

# unique value for each column in section
SECTION_ID = "101"
SECTION_NAME = "102"
SECTION_START_AT = "103"
SECTION_END_AT = "104"
SECTION_CREATED_AT = "105"
SECTION_CREATED_AT_DATE = "106"
SECTION_RESTRICT_ENROLLMENTS_TO_SECTION_DATES = "107"
SECTION_NONEXIST_COURSE_ID = "108"
SECTION_SIS_SECTION_ID = "109"
SECTION_SIS_COURSE_ID = "110"
SECTION_INTEGRATION_ID = "111"
SECTION_SIS_IMPORT_ID = "112"
SECTION_CREATE_DATE = "113"
SECTION_LAST_MODIFIED_DATE = "114"

SECOND_SECTION_ID = "201"
SECOND_SECTION_NAME = "202"
SECOND_SECTION_START_AT = "203"
SECOND_SECTION_END_AT = "204"
SECOND_SECTION_CREATED_AT = "205"
SECOND_SECTION_CREATED_AT_DATE = "206"
SECOND_SECTION_RESTRICT_ENROLLMENTS_TO_SECTION_DATES = "207"
SECOND_SECTION_NONEXIST_COURSE_ID = "208"
SECOND_SECTION_SIS_SECTION_ID = "209"
SECOND_SECTION_SIS_COURSE_ID = "210"
SECOND_SECTION_INTEGRATION_ID = "211"
SECOND_SECTION_SIS_IMPORT_ID = "212"
SECOND_SECTION_CREATE_DATE = "213"
SECOND_SECTION_LAST_MODIFIED_DATE = "214"


def describe_when_a_single_assignment_with_unique_fields_is_mapped():
    @pytest.fixture
    def assignment_dfs() -> Dict[str, DataFrame]:
        assignment_df: DataFrame = DataFrame(
            {
                "id": [ID],
                "description": [DESCRIPTION],
                "due_at": [DUE_AT],
                "unlock_at": [UNLOCK_AT],
                "lock_at": [LOCK_AT],
                "points_possible": [POINTS_POSSIBLE],
                "grading_type": [GRADING_TYPE],
                "ASSIGNMENT_GROUP_ID": [ASSIGNMENT_GROUP_ID],
                "grading_standard_id": [GRADING_STANDARD_ID],
                "created_at": [CREATED_AT],
                "created_at_date": [CREATED_AT_DATE],
                "updated_at": [UPDATED_AT],
                "updated_at_date": [UPDATED_AT_DATE],
                "peer_reviews": [PEER_REVIEWS],
                "automatic_peer_reviews": [AUTOMATIC_PEER_REVIEWS],
                "position": [POSITION],
                "grade_group_students_individually": [
                    GRADE_GROUP_STUDENTS_INDIVIDUALLY
                ],
                "anonymous_peer_reviews": [ANONYMOUS_PEER_REVIEWS],
                "group_category_id": [GROUP_CATEGORY_ID],
                "post_to_sis": [POST_TO_SIS],
                "moderated_grading": [MODERATED_GRADING],
                "omit_from_final_grade": [OMIT_FROM_FINAL_GRADE],
                "intra_group_peer_reviews": [INTRA_GROUP_PEER_REVIEWS],
                "anonymous_instructor_annotations": [ANONYMOUS_INSTRUCTOR_ANNOTATIONS],
                "anonymous_grading": [ANONYMOUS_GRADING],
                "graders_anonymous_to_graders": [GRADERS_ANONYMOUS_TO_GRADERS],
                "grader_count": [GRADER_COUNT],
                "grader_comments_visible_to_graders": [
                    GRADER_COMMENTS_VISIBLE_TO_GRADERS
                ],
                "final_grader_id": [FINAL_GRADER_ID],
                "grader_names_visible_to_final_grader": [
                    GRADER_NAMES_VISIBLE_TO_FINAL_GRADER
                ],
                "allowed_attempts": [ALLOWED_ATTEMPTS],
                "secure_params": [SECURE_PARAMS],
                "course_id": [COURSE_ID],
                "name": [NAME],
                "submission_types": [SUBMISSION_TYPES],
                "has_submitted_submissions": [HAS_SUBMITTED_SUBMISSIONS],
                "due_date_required": [DUE_DATE_REQUIRED],
                "max_name_length": [MAX_NAME_LENGTH],
                "in_closed_grading_period": [IN_CLOSED_GRADING_PERIOD],
                "is_quiz_assignment": [IS_QUIZ_ASSIGNMENT],
                "can_duplicate": [CAN_DUPLICATE],
                "original_course_id": [ORIGINAL_COURSE_ID],
                "original_assignment_id": [ORIGINAL_ASSIGNMENT_ID],
                "original_assignment_name": [ORIGINAL_ASSIGNMENT_NAME],
                "original_quiz_id": [ORIGINAL_QUIZ_ID],
                "workflow_state": [WORKFLOW_STATE],
                "muted": [MUTED],
                "html_url": [HTML_URL],
                "has_overrides": [HAS_OVERRIDES],
                "needs_grading_count": [NEEDS_GRADING_COUNT],
                "sis_assignment_id": [SIS_ASSIGNMENT_ID],
                "integration_id": [INTEGRATION_ID],
                "integration_data": [INTEGRATION_DATA],
                "discussion_topic": [DISCUSSION_TOPIC],
                "published": [PUBLISHED],
                "unpublishable": [UNPUBLISHABLE],
                "only_visible_to_overrides": [ONLY_VISIBLE_TO_OVERRIDES],
                "locked_for_user": [LOCKED_FOR_USER],
                "submissions_download_url": [SUBMISSIONS_DOWNLOAD_URL],
                "post_manually": [POST_MANUALLY],
                "anonymize_students": [ANONYMIZE_STUDENTS],
                "require_lockdown_browser": [REQUIRE_LOCKDOWN_BROWSER],
                "external_tool_tag_attributes": [EXTERNAL_TOOL_TAG_ATTRIBUTES],
                "url": [URL],
                "quiz_id": [QUIZ_ID],
                "anonymous_submissions": [ANONYMOUS_SUBMISSIONS],
                "use_rubric_for_grading": [USE_RUBRIC_FOR_GRADING],
                "free_form_criterion_comments": [FREE_FORM_CRITERION_COMMENTS],
                "rubric": [RUBRIC],
                "rubric_settings": [RUBRIC_SETTINGS],
                "due_at_date": [DUE_AT_DATE],
                "CreateDate": [CREATE_DATE],
                "LastModifiedDate": [LAST_MODIFIED_DATE],
            }
        )
        section_df: DataFrame = DataFrame(
            {
                "id": [SECTION_ID],
                # joins on COURSE_ID
                "course_id": [COURSE_ID],
                "name": [SECTION_NAME],
                "start_at": [SECTION_START_AT],
                "end_at": [SECTION_END_AT],
                "created_at": [SECTION_CREATED_AT],
                "created_at_date": [SECTION_CREATED_AT_DATE],
                "restrict_enrollments_to_section_dates": [
                    SECTION_RESTRICT_ENROLLMENTS_TO_SECTION_DATES
                ],
                "nonxlist_course_id": [SECTION_NONEXIST_COURSE_ID],
                "sis_section_id": [SECTION_SIS_SECTION_ID],
                "sis_course_id": [SECTION_SIS_COURSE_ID],
                "integration_id": [SECTION_INTEGRATION_ID],
                "sis_import_id": [SECTION_SIS_IMPORT_ID],
                "CreateDate": [SECTION_CREATE_DATE],
                "LastModifiedDate": [SECTION_LAST_MODIFIED_DATE],
            },
        )

        # act
        return map_to_udm_assignments(assignment_df, section_df)

    def it_should_have_correct_shape(assignment_dfs: Dict[str, DataFrame]) -> None:
        assert len(assignment_dfs) == 1
        # assignment_df: DataFrame = assignment_dfs[(SECTION_ID,)]
        assignment_df: DataFrame = assignment_dfs[SECTION_ID]
        row_count, column_count = assignment_df.shape
        assert row_count == 1
        assert column_count == 15

    def it_should_map_the_constant_assignment_to_property_AssignmentCategory(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "AssignmentCategory"] == "assignment"

    def it_should_map_the_assignment_description(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "AssignmentDescription"] == DESCRIPTION

    def it_should_map_the_due_date_time(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "DueDateTime"] == DUE_AT

    def it_should_map_the_end_date_time(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "EndDateTime"] == LOCK_AT

    def it_should_map_section_identifier(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "LMSSectionSourceSystemIdentifier"] == SECTION_ID

    def it_should_map_source_system(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "SourceSystem"] == SOURCE_SYSTEM

    def it_should_map_maxpoint(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "MaxPoints"] == POINTS_POSSIBLE

    def it_should_map_submission_type(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "SubmissionType"] == SUBMISSION_TYPES

    def it_should_map_source_system_identifier(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "SourceSystemIdentifier"] == f"{SECTION_ID}-{ID}"

    def it_should_map_start_date_time(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "StartDateTime"] == UNLOCK_AT

    def it_should_map_source_create_date(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "SourceCreateDate"] == CREATED_AT

    def it_should_map_source_last_modified_date(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "SourceLastModifiedDate"] == UPDATED_AT

    def it_should_map_title(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "Title"] == NAME

    def it_should_map_create_date(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "CreateDate"] == CREATE_DATE

    def it_should_map_last_modified_date(assignment_dfs: Dict[str, DataFrame]) -> None:
        assignment_df = assignment_dfs[SECTION_ID]
        assert assignment_df.loc[0, "LastModifiedDate"] == LAST_MODIFIED_DATE


def describe_when_a_single_assignment_in_two_sections_is_mapped():
    @pytest.fixture
    def assignment_dfs() -> Dict[str, DataFrame]:
        assignment_df: DataFrame = DataFrame(
            {
                "id": [ID],
                "description": [DESCRIPTION],
                "due_at": [DUE_AT],
                "unlock_at": [UNLOCK_AT],
                "lock_at": [LOCK_AT],
                "points_possible": [POINTS_POSSIBLE],
                "grading_type": [GRADING_TYPE],
                "ASSIGNMENT_GROUP_ID": [ASSIGNMENT_GROUP_ID],
                "grading_standard_id": [GRADING_STANDARD_ID],
                "created_at": [CREATED_AT],
                "created_at_date": [CREATED_AT_DATE],
                "updated_at": [UPDATED_AT],
                "updated_at_date": [UPDATED_AT_DATE],
                "peer_reviews": [PEER_REVIEWS],
                "automatic_peer_reviews": [AUTOMATIC_PEER_REVIEWS],
                "position": [POSITION],
                "grade_group_students_individually": [
                    GRADE_GROUP_STUDENTS_INDIVIDUALLY
                ],
                "anonymous_peer_reviews": [ANONYMOUS_PEER_REVIEWS],
                "group_category_id": [GROUP_CATEGORY_ID],
                "post_to_sis": [POST_TO_SIS],
                "moderated_grading": [MODERATED_GRADING],
                "omit_from_final_grade": [OMIT_FROM_FINAL_GRADE],
                "intra_group_peer_reviews": [INTRA_GROUP_PEER_REVIEWS],
                "anonymous_instructor_annotations": [ANONYMOUS_INSTRUCTOR_ANNOTATIONS],
                "anonymous_grading": [ANONYMOUS_GRADING],
                "graders_anonymous_to_graders": [GRADERS_ANONYMOUS_TO_GRADERS],
                "grader_count": [GRADER_COUNT],
                "grader_comments_visible_to_graders": [
                    GRADER_COMMENTS_VISIBLE_TO_GRADERS
                ],
                "final_grader_id": [FINAL_GRADER_ID],
                "grader_names_visible_to_final_grader": [
                    GRADER_NAMES_VISIBLE_TO_FINAL_GRADER
                ],
                "allowed_attempts": [ALLOWED_ATTEMPTS],
                "secure_params": [SECURE_PARAMS],
                "course_id": [COURSE_ID],
                "name": [NAME],
                "submission_types": [SUBMISSION_TYPES],
                "has_submitted_submissions": [HAS_SUBMITTED_SUBMISSIONS],
                "due_date_required": [DUE_DATE_REQUIRED],
                "max_name_length": [MAX_NAME_LENGTH],
                "in_closed_grading_period": [IN_CLOSED_GRADING_PERIOD],
                "is_quiz_assignment": [IS_QUIZ_ASSIGNMENT],
                "can_duplicate": [CAN_DUPLICATE],
                "original_course_id": [ORIGINAL_COURSE_ID],
                "original_assignment_id": [ORIGINAL_ASSIGNMENT_ID],
                "original_assignment_name": [ORIGINAL_ASSIGNMENT_NAME],
                "original_quiz_id": [ORIGINAL_QUIZ_ID],
                "workflow_state": [WORKFLOW_STATE],
                "muted": [MUTED],
                "html_url": [HTML_URL],
                "has_overrides": [HAS_OVERRIDES],
                "needs_grading_count": [NEEDS_GRADING_COUNT],
                "sis_assignment_id": [SIS_ASSIGNMENT_ID],
                "integration_id": [INTEGRATION_ID],
                "integration_data": [INTEGRATION_DATA],
                "discussion_topic": [DISCUSSION_TOPIC],
                "published": [PUBLISHED],
                "unpublishable": [UNPUBLISHABLE],
                "only_visible_to_overrides": [ONLY_VISIBLE_TO_OVERRIDES],
                "locked_for_user": [LOCKED_FOR_USER],
                "submissions_download_url": [SUBMISSIONS_DOWNLOAD_URL],
                "post_manually": [POST_MANUALLY],
                "anonymize_students": [ANONYMIZE_STUDENTS],
                "require_lockdown_browser": [REQUIRE_LOCKDOWN_BROWSER],
                "external_tool_tag_attributes": [EXTERNAL_TOOL_TAG_ATTRIBUTES],
                "url": [URL],
                "quiz_id": [QUIZ_ID],
                "anonymous_submissions": [ANONYMOUS_SUBMISSIONS],
                "use_rubric_for_grading": [USE_RUBRIC_FOR_GRADING],
                "free_form_criterion_comments": [FREE_FORM_CRITERION_COMMENTS],
                "rubric": [RUBRIC],
                "rubric_settings": [RUBRIC_SETTINGS],
                "due_at_date": [DUE_AT_DATE],
                "CreateDate": [CREATE_DATE],
                "LastModifiedDate": [LAST_MODIFIED_DATE],
            }
        )
        section_df: DataFrame = DataFrame(
            {
                "id": [SECTION_ID, SECOND_SECTION_ID],
                # joins on COURSE_ID
                "course_id": [COURSE_ID, COURSE_ID],
                "name": [SECTION_NAME, SECOND_SECTION_NAME],
                "start_at": [SECTION_START_AT, SECOND_SECTION_START_AT],
                "end_at": [SECTION_END_AT, SECOND_SECTION_END_AT],
                "created_at": [SECTION_CREATED_AT, SECOND_SECTION_CREATED_AT],
                "created_at_date": [
                    SECTION_CREATED_AT_DATE,
                    SECOND_SECTION_CREATED_AT_DATE,
                ],
                "restrict_enrollments_to_section_dates": [
                    SECTION_RESTRICT_ENROLLMENTS_TO_SECTION_DATES,
                    SECOND_SECTION_RESTRICT_ENROLLMENTS_TO_SECTION_DATES,
                ],
                "nonxlist_course_id": [
                    SECTION_NONEXIST_COURSE_ID,
                    SECOND_SECTION_NONEXIST_COURSE_ID,
                ],
                "sis_section_id": [
                    SECTION_SIS_SECTION_ID,
                    SECOND_SECTION_SIS_SECTION_ID,
                ],
                "sis_course_id": [SECTION_SIS_COURSE_ID, SECOND_SECTION_SIS_COURSE_ID],
                "integration_id": [
                    SECTION_INTEGRATION_ID,
                    SECOND_SECTION_INTEGRATION_ID,
                ],
                "sis_import_id": [SECTION_SIS_IMPORT_ID, SECOND_SECTION_SIS_IMPORT_ID],
                "CreateDate": [SECTION_CREATE_DATE, CREATE_DATE],
                "LastModifiedDate": [
                    SECTION_LAST_MODIFIED_DATE,
                    SECOND_SECTION_LAST_MODIFIED_DATE,
                ],
            }
        )

        # act
        return map_to_udm_assignments(assignment_df, section_df)

    def it_should_have_correct_number_of_dfs(assignment_dfs: Dict[str, DataFrame]):
        assert len(assignment_dfs) == 2

    def it_should_have_correct_shape_for_first_df(assignment_dfs: Dict[str, DataFrame]):
        assignment_df: DataFrame = assignment_dfs[SECTION_ID]
        row_count, column_count = assignment_df.shape
        assert row_count == 1
        assert column_count == 15

    def it_should_have_correct_shape_for_second_df(
        assignment_dfs: Dict[str, DataFrame]
    ):
        second_assignment_df: DataFrame = assignment_dfs[SECOND_SECTION_ID]
        second_row_count, second_column_count = second_assignment_df.shape
        assert second_row_count == 1
        assert second_column_count == 15

    def it_should_map_fields_correctly_for_first_df(assignment_dfs):
        assignment_df: DataFrame = assignment_dfs[SECTION_ID]
        row_dict = assignment_df.to_dict(orient="records")[0]

        # Just test the identifier - don't need to look at every column
        assert row_dict["SourceSystemIdentifier"] == f"{SECTION_ID}-{ID}"

    def it_should_map_fields_correctly_for_second_df(assignment_dfs):
        assignment_df: DataFrame = assignment_dfs[SECOND_SECTION_ID]
        row_dict = assignment_df.to_dict(orient="records")[0]
        assert row_dict["SourceSystemIdentifier"] == f"{SECOND_SECTION_ID}-{ID}"
