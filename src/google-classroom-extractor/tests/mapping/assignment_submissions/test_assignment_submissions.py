# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict, Tuple
import pytest
from pandas import DataFrame
from google_classroom_extractor.mapping.assignment_submissions import (
    submissions_to_assignment_submissions_dfs,
)
from google_classroom_extractor.mapping.constants import (
    SOURCE_SYSTEM,
    ENTITY_STATUS_ACTIVE,
)
from tests.helper import merged_dict

# unique value for each column in fixture
COURSE_ID = "1"
COURSEWORK_ID = "2"
ID = "3"
USER_ID = "4"
CREATION_TIME = "5"
UPDATE_TIME = "6"
STATE = "7"
LATE = "8"
DRAFT_GRADE = "9"
ASSIGNED_GRADE = "10"
ALTERNATE_LINK = "11"
COURSEWORK_TYPE = "12"
ASSOCIATED_WITH_DEVELOPER = "13"
SUBMISSION_HISTORY = "14"
CREATE_DATE = "2020-01-01"
LAST_MODIFIED_DATE = "2020-01-02"


def describe_when_a_single_submission_with_unique_fields_is_mapped():
    @pytest.fixture
    def assignment_submissions_dicts() -> Dict[Tuple[str, str], DataFrame]:
        # arrange
        submissions_df = DataFrame(
            {
                "courseId": [COURSE_ID],
                "courseWorkId": [COURSEWORK_ID],
                "id": [ID],
                "userId": [USER_ID],
                "creationTime": [CREATION_TIME],
                "updateTime": [UPDATE_TIME],
                "state": [STATE],
                "late": [LATE],
                "draftGrade": [DRAFT_GRADE],
                "assignedGrade": [ASSIGNED_GRADE],
                "alternateLink": [ALTERNATE_LINK],
                "courseWorkType": [COURSEWORK_TYPE],
                "associatedWithDeveloper": [ASSOCIATED_WITH_DEVELOPER],
                "submissionHistory": [SUBMISSION_HISTORY],
                "CreateDate": [CREATE_DATE],
                "LastModifiedDate": [LAST_MODIFIED_DATE]
            }
        )

        # act
        return submissions_to_assignment_submissions_dfs(submissions_df)

    def it_should_have_correct_shape(assignment_submissions_dicts):
        assert len(assignment_submissions_dicts) == 1

        submissions_df: DataFrame = assignment_submissions_dicts[
            (COURSE_ID, f"{COURSE_ID}-{COURSEWORK_ID}")
        ]
        row_count, column_count = submissions_df.shape

        assert row_count == 1
        assert column_count == 14

    def it_should_map_fields_correctly(assignment_submissions_dicts):
        submissions_df: DataFrame = assignment_submissions_dicts[
            (COURSE_ID, f"{COURSE_ID}-{COURSEWORK_ID}")
        ]
        row_dict = submissions_df.to_dict(orient="records")[0]

        assert row_dict["AssignmentIdentifier"] == f"{COURSE_ID}-{COURSEWORK_ID}"
        assert row_dict["EarnedPoints"] == ASSIGNED_GRADE
        assert row_dict["EntityStatus"] == ENTITY_STATUS_ACTIVE
        assert row_dict["Grade"] == ASSIGNED_GRADE
        assert row_dict["SourceSystem"] == SOURCE_SYSTEM
        assert row_dict["SourceSystemIdentifier"] == f"{COURSE_ID}-{COURSEWORK_ID}-{ID}"
        assert row_dict["Status"] == STATE
        assert row_dict["SubmissionDateTime"] == ""
        assert row_dict["LMSUserIdentifier"] == USER_ID
        assert row_dict["SourceCreateDate"] == CREATION_TIME
        assert row_dict["SourceLastModifiedDate"] == UPDATE_TIME
        assert row_dict["CreateDate"] == CREATE_DATE
        assert row_dict["LastModifiedDate"] == LAST_MODIFIED_DATE


BOILERPLATE: Dict[str, str] = {
    "userId": USER_ID,
    "creationTime": CREATION_TIME,
    "updateTime": UPDATE_TIME,
    "state": STATE,
    "late": LATE,
    "draftGrade": DRAFT_GRADE,
    "assignedGrade": ASSIGNED_GRADE,
    "alternateLink": ALTERNATE_LINK,
    "courseWorkType": COURSEWORK_TYPE,
    "associatedWithDeveloper": ASSOCIATED_WITH_DEVELOPER,
    "submissionHistory": SUBMISSION_HISTORY,
    "CreateDate": CREATE_DATE,
    "LastModifiedDate": LAST_MODIFIED_DATE
}


def describe_when_multiple_submissions_for_the_same_assignment_are_mapped():
    submission2_id = "submission2_id"

    @pytest.fixture
    def assignment_submissions_dicts() -> Dict[Tuple[str, str], DataFrame]:
        # arrange
        submission1: Dict[str, str] = {
            "id": ID,
            "courseId": COURSE_ID,
            "courseWorkId": COURSEWORK_ID,
        }

        submission2: Dict[str, str] = {
            "id": submission2_id,
            "courseId": COURSE_ID,
            "courseWorkId": COURSEWORK_ID,
        }

        submissions_df = DataFrame.from_dict(
            [
                merged_dict(submission1, BOILERPLATE),
                merged_dict(submission2, BOILERPLATE),
            ]
        )
        # act
        return submissions_to_assignment_submissions_dfs(submissions_df)

    def it_should_have_one_assignment(assignment_submissions_dicts):
        assert len(assignment_submissions_dicts) == 1

    def it_should_have_first_row_in_same_assignment(assignment_submissions_dicts):
        assignment_submissions_df: DataFrame = assignment_submissions_dicts[
            (COURSE_ID, f"{COURSE_ID}-{COURSEWORK_ID}")
        ]
        coursework1_dict = assignment_submissions_df.to_dict(orient="records")[0]

        assert (
            coursework1_dict["SourceSystemIdentifier"]
            == f"{COURSE_ID}-{COURSEWORK_ID}-{ID}"
        )

    def it_should_have_second_row_in_same_assignment(assignment_submissions_dicts):
        assignment_submissions_df: DataFrame = assignment_submissions_dicts[
            (COURSE_ID, f"{COURSE_ID}-{COURSEWORK_ID}")
        ]
        coursework2_dict = assignment_submissions_df.to_dict(orient="records")[1]

        assert (
            coursework2_dict["SourceSystemIdentifier"]
            == f"{COURSE_ID}-{COURSEWORK_ID}-{submission2_id}"
        )


def describe_when_submissions_in_different_assignments_are_mapped():
    submission2_id = "submission2_id"
    coursework2_id = "coursework2_id"

    @pytest.fixture
    def assignment_submissions_dicts() -> Dict[Tuple[str, str], DataFrame]:
        # arrange
        submission1: Dict[str, str] = {
            "id": ID,
            "courseId": COURSE_ID,
            "courseWorkId": COURSEWORK_ID,
        }

        submission2: Dict[str, str] = {
            "id": submission2_id,
            "courseId": COURSE_ID,
            "courseWorkId": coursework2_id,
        }

        submissions_df = DataFrame.from_dict(
            [
                merged_dict(submission1, BOILERPLATE),
                merged_dict(submission2, BOILERPLATE),
            ]
        )
        # act
        return submissions_to_assignment_submissions_dfs(submissions_df)

    def it_should_have_two_assignments(assignment_submissions_dicts):
        assert len(assignment_submissions_dicts) == 2

    def it_should_have_one_submission_for_first_assignment(
        assignment_submissions_dicts,
    ):
        submissions_df: DataFrame = assignment_submissions_dicts[
            (COURSE_ID, f"{COURSE_ID}-{COURSEWORK_ID}")
        ]
        row_count, _ = submissions_df.shape

        assert row_count == 1

    def it_should_have_one_submission_for_second_assignment(
        assignment_submissions_dicts,
    ):
        submissions_df: DataFrame = assignment_submissions_dicts[
            (COURSE_ID, f"{COURSE_ID}-{coursework2_id}")
        ]
        row_count, _ = submissions_df.shape

        assert row_count == 1

    def it_should_have_correct_submission_id_in_first_assignment(
        assignment_submissions_dicts,
    ):
        assignment_submissions_df: DataFrame = assignment_submissions_dicts[
            (COURSE_ID, f"{COURSE_ID}-{COURSEWORK_ID}")
        ]
        coursework1_dict = assignment_submissions_df.to_dict(orient="records")[0]

        assert (
            coursework1_dict["SourceSystemIdentifier"]
            == f"{COURSE_ID}-{COURSEWORK_ID}-{ID}"
        )

    def it_should_have_correct_submission_id_in_second_assignment(
        assignment_submissions_dicts,
    ):
        assignment_submissions_df: DataFrame = assignment_submissions_dicts[
            (COURSE_ID, f"{COURSE_ID}-{coursework2_id}")
        ]
        coursework2_dict = assignment_submissions_df.to_dict(orient="records")[0]

        assert (
            coursework2_dict["SourceSystemIdentifier"]
            == f"{COURSE_ID}-{coursework2_id}-{submission2_id}"
        )
