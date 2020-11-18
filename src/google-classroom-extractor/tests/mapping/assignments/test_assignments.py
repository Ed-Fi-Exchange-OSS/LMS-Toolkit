# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict
import pytest
from datetime import datetime
from pandas import DataFrame
from google_classroom_extractor.mapping.assignments import coursework_to_assignments_dfs
from google_classroom_extractor.mapping.constants import (
    SOURCE_SYSTEM,
    ENTITY_STATUS_ACTIVE,
)
from tests.helper import merged_dict

# unique value for each column in fixture
COURSE_ID = "1"
ID = "2"
TITLE = "3"
DESCRIPTION = "4"
STATE = "5"
ALTERNATE_LINK = "6"
CREATION_TIME = "7"
UPDATE_TIME = "8"
MAX_POINTS = "9"
DUEDATE_YEAR = "2000"
DUEDATE_MONTH = "10"
DUEDATE_DAY = "11"
DUETIME_HOURS = "12"
DUETIME_MINUTES = "13.0"  # API returns float strings
WORK_TYPE = "14"
SUBMISSION_MODIFICATION_MODE = "15"
ASSIGNEE_MODE = "16"
CREATOR_USER_ID = "17"
SCHEDULED_TIME = "18"
TOPIC_ID = "19"


def describe_when_a_single_coursework_with_unique_fields_is_mapped():
    @pytest.fixture
    def assignments_dicts() -> Dict[str, DataFrame]:
        # arrange
        coursework_df = DataFrame(
            {
                "courseId": [COURSE_ID],
                "id": [ID],
                "title": [TITLE],
                "description": [DESCRIPTION],
                "state": [STATE],
                "alternateLink": [ALTERNATE_LINK],
                "creationTime": [CREATION_TIME],
                "updateTime": [UPDATE_TIME],
                "maxPoints": [MAX_POINTS],
                "workType": [WORK_TYPE],
                "submissionModificationMode": [SUBMISSION_MODIFICATION_MODE],
                "assigneeMode": [ASSIGNEE_MODE],
                "creatorUserId": [CREATOR_USER_ID],
                "dueDate.year": [DUEDATE_YEAR],
                "dueDate.month": [DUEDATE_MONTH],
                "dueDate.day": [DUEDATE_DAY],
                "dueTime.hours": [DUETIME_HOURS],
                "dueTime.minutes": [DUETIME_MINUTES],
                "scheduledTime": [SCHEDULED_TIME],
                "topicId": [TOPIC_ID],
            }
        )

        # act
        return coursework_to_assignments_dfs(coursework_df)

    def it_should_have_correct_shape(assignments_dicts):
        assert len(assignments_dicts) == 1

        assignments_df: DataFrame = assignments_dicts[COURSE_ID]
        row_count, column_count = assignments_df.shape

        assert row_count == 1
        assert column_count == 13

    def it_should_map_fields_correctly(assignments_dicts):
        assignments_df: DataFrame = assignments_dicts[COURSE_ID]
        row_dict = assignments_df.to_dict(orient="records")[0]

        assert row_dict["AssignmentCategory"] == WORK_TYPE
        assert row_dict["AssignmentDescription"] == DESCRIPTION
        assert row_dict["DueDateTime"] == datetime(
            int(DUEDATE_YEAR),
            int(DUEDATE_MONTH),
            int(DUEDATE_DAY),
            int(DUETIME_HOURS),
            int(float(DUETIME_MINUTES)),
        )
        assert row_dict["EndDateTime"] == ""
        assert row_dict["EntityStatus"] == ENTITY_STATUS_ACTIVE
        assert row_dict["LMSSectionSourceSystemIdentifier"] == COURSE_ID
        assert row_dict["MaxPoints"] == MAX_POINTS
        assert row_dict["SourceSystem"] == SOURCE_SYSTEM
        assert row_dict["SourceSystemIdentifier"] == f"{COURSE_ID}-{ID}"
        assert row_dict["StartDateTime"] == SCHEDULED_TIME
        assert row_dict["Title"] == TITLE
        assert row_dict["SourceCreateDate"] == CREATION_TIME
        assert row_dict["SourceLastModifiedDate"] == UPDATE_TIME


def describe_when_a_single_coursework_without_due_date_info_is_mapped():
    @pytest.fixture
    def assignments_dicts() -> Dict[str, DataFrame]:
        # arrange
        coursework_df = DataFrame(
            {
                "courseId": [COURSE_ID],
                "id": [ID],
                "title": [TITLE],
                "description": [DESCRIPTION],
                "state": [STATE],
                "alternateLink": [ALTERNATE_LINK],
                "creationTime": [CREATION_TIME],
                "updateTime": [UPDATE_TIME],
                "maxPoints": [MAX_POINTS],
                "workType": [WORK_TYPE],
                "submissionModificationMode": [SUBMISSION_MODIFICATION_MODE],
                "assigneeMode": [ASSIGNEE_MODE],
                "creatorUserId": [CREATOR_USER_ID],
                "scheduledTime": [SCHEDULED_TIME],
                "topicId": [TOPIC_ID],
            }
        )

        # act
        return coursework_to_assignments_dfs(coursework_df)

    def it_should_have_correct_shape(assignments_dicts):
        assert len(assignments_dicts) == 1

        assignments_df: DataFrame = assignments_dicts[COURSE_ID]
        row_count, column_count = assignments_df.shape

        assert row_count == 1
        assert column_count == 13

    def it_should_map_fields_correctly_with_empty_duedate(assignments_dicts):
        assignments_df: DataFrame = assignments_dicts[COURSE_ID]
        row_dict = assignments_df.to_dict(orient="records")[0]

        assert row_dict["AssignmentCategory"] == WORK_TYPE
        assert row_dict["AssignmentDescription"] == DESCRIPTION
        assert row_dict["DueDateTime"] == ""
        assert row_dict["EndDateTime"] == ""
        assert row_dict["EntityStatus"] == ENTITY_STATUS_ACTIVE
        assert row_dict["LMSSectionSourceSystemIdentifier"] == COURSE_ID
        assert row_dict["MaxPoints"] == MAX_POINTS
        assert row_dict["SourceSystem"] == SOURCE_SYSTEM
        assert row_dict["SourceSystemIdentifier"] == f"{COURSE_ID}-{ID}"
        assert row_dict["StartDateTime"] == SCHEDULED_TIME
        assert row_dict["Title"] == TITLE
        assert row_dict["SourceCreateDate"] == CREATION_TIME
        assert row_dict["SourceLastModifiedDate"] == UPDATE_TIME


BOILERPLATE: Dict[str, str] = {
    "description": DESCRIPTION,
    "state": STATE,
    "alternateLink": ALTERNATE_LINK,
    "creationTime": CREATION_TIME,
    "updateTime": UPDATE_TIME,
    "maxPoints": MAX_POINTS,
    "workType": WORK_TYPE,
    "submissionModificationMode": SUBMISSION_MODIFICATION_MODE,
    "assigneeMode": ASSIGNEE_MODE,
    "creatorUserId": CREATOR_USER_ID,
    "dueDate.year": DUEDATE_YEAR,
    "dueDate.month": DUEDATE_MONTH,
    "dueDate.day": DUEDATE_DAY,
    "dueTime.hours": DUETIME_HOURS,
    "dueTime.minutes": DUETIME_MINUTES,
    "scheduledTime": SCHEDULED_TIME,
    "topicId": TOPIC_ID,
}


def describe_when_multiple_assignments_are_in_same_section():
    coursework2_id = "coursework2_id"
    coursework2_title = "coursework2_title"

    @pytest.fixture
    def assignments_dict() -> Dict[str, DataFrame]:
        # arrange
        coursework1: Dict[str, str] = {
            "courseId": COURSE_ID,
            "id": ID,
            "title": TITLE,
        }

        coursework2: Dict[str, str] = {
            "courseId": COURSE_ID,
            "id": coursework2_id,
            "title": coursework2_title,
        }

        coursework_df = DataFrame.from_dict(
            [
                merged_dict(coursework1, BOILERPLATE),
                merged_dict(coursework2, BOILERPLATE),
            ]
        )

        # act
        return coursework_to_assignments_dfs(coursework_df)

    def it_should_have_one_assignment(assignments_dict):
        assert len(assignments_dict) == 1

    def it_should_have_two_rows_in_same_assignment(assignments_dict):
        assignments_df: DataFrame = assignments_dict[COURSE_ID]
        row_count, _ = assignments_df.shape

        assert row_count == 2

    def it_should_have_first_row_with_correct_data(assignments_dict):
        coursework1_dict = assignments_dict[COURSE_ID].to_dict(orient="records")[0]

        assert coursework1_dict["SourceSystemIdentifier"] == f"{COURSE_ID}-{ID}"
        assert coursework1_dict["Title"] == TITLE

    def it_should_have_second_row_with_correct_data(assignments_dict):
        coursework2_dict = assignments_dict[COURSE_ID].to_dict(orient="records")[1]
        assert (
            coursework2_dict["SourceSystemIdentifier"]
            == f"{COURSE_ID}-{coursework2_id}"
        )
        assert coursework2_dict["Title"] == coursework2_title


def describe_when_multiple_assignments_are_in_different_sections():
    coursework2_course_id = "coursework2_course_id"
    coursework2_title = "coursework2_title"

    @pytest.fixture
    def assignments_dict() -> Dict[str, DataFrame]:
        # arrange
        coursework1: Dict[str, str] = {
            "courseId": COURSE_ID,
            "id": ID,
            "title": TITLE,
        }

        coursework2: Dict[str, str] = {
            "courseId": coursework2_course_id,
            "id": ID,
            "title": coursework2_title,
        }

        coursework_df = DataFrame.from_dict(
            [
                merged_dict(coursework1, BOILERPLATE),
                merged_dict(coursework2, BOILERPLATE),
            ]
        )

        # act
        return coursework_to_assignments_dfs(coursework_df)

    def it_should_have_two_assignments(assignments_dict):
        assert len(assignments_dict) == 2

    def it_should_have_one_row_in_first_assignment(assignments_dict):
        assignments_df: DataFrame = assignments_dict[COURSE_ID]
        row_count, _ = assignments_df.shape
        assert row_count == 1

    def it_should_have_first_assignment_with_correct_data(assignments_dict):
        coursework_dict = assignments_dict[COURSE_ID].to_dict(orient="records")[0]
        assert coursework_dict["SourceSystemIdentifier"] == f"{COURSE_ID}-{ID}"
        assert coursework_dict["Title"] == TITLE

    def it_should_have_one_row_in_second_assignment(assignments_dict):
        assignments_df: DataFrame = assignments_dict[coursework2_course_id]
        row_count, _ = assignments_df.shape
        assert row_count == 1

    def it_should_have_second_assignment_with_correct_data(assignments_dict):
        coursework_dict = assignments_dict[coursework2_course_id].to_dict(
            orient="records"
        )[0]
        assert (
            coursework_dict["SourceSystemIdentifier"] == f"{coursework2_course_id}-{ID}"
        )
        assert coursework_dict["Title"] == coursework2_title
