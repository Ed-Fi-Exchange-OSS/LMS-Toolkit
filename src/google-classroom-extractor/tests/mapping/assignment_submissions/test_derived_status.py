# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict, Tuple
import pytest
from pandas import DataFrame
from edfi_google_classroom_extractor.mapping.assignment_submissions import (
    submissions_to_assignment_submissions_dfs,
    CREATED_STATE,
    NEW_STATE,
    RECLAIMED_STATE,
    TURNED_IN_STATE,
    LATE_STATE,
    MISSING_STATE,
    RETURNED_STATE,
)
from tests.helper import merged_dict


# unique value for each column in fixture
COURSE_ID = "1"
COURSEWORK_ID = "2"
ID = "3"
USER_ID = "4"
CREATION_TIME = "2005-05-05 00:00:00"
UPDATE_TIME = "2006-06-06 00:00:00"
STATE = "7"
LATE = "8"
DRAFT_GRADE = "9"
ASSIGNED_GRADE = "10"
ALTERNATE_LINK = "11"
ASSOCIATED_WITH_DEVELOPER = "13"
SUBMISSION_HISTORY = """[
        {
          "stateHistory": {
            "state": "CREATED",
            "stateTimestamp": "2021-09-02T16:38:34.895Z",
            "actorUserId": "114946936387309047192"
          }
        },
        {
          "stateHistory": {
            "state": "TURNED_IN",
            "stateTimestamp": "2021-10-02T16:38:34.895Z",
            "actorUserId": "114946936387309047192"
          }
        }
      ]"""
CREATE_DATE = "2020-01-01"
LAST_MODIFIED_DATE = "2020-01-02"


BOILERPLATE: Dict[str, str] = {
    "courseId": COURSE_ID,
    "courseWorkId": COURSEWORK_ID,
    "id": ID,
    "userId": USER_ID,
    "creationTime": CREATION_TIME,
    "updateTime": UPDATE_TIME,
    "draftGrade": DRAFT_GRADE,
    "assignedGrade": ASSIGNED_GRADE,
    "alternateLink": ALTERNATE_LINK,
    "associatedWithDeveloper": ASSOCIATED_WITH_DEVELOPER,
    "submissionHistory": SUBMISSION_HISTORY,
    "CreateDate": CREATE_DATE,
    "LastModifiedDate": LAST_MODIFIED_DATE,
}


def describe_when_a_submission_is_created_and_late_as_true_string():
    @pytest.fixture
    def assignment_submission_dict() -> Dict[Tuple[str, str], DataFrame]:
        # arrange
        submission: Dict[str, str] = {
            "state": CREATED_STATE,
            "late": "true",
        }

        submissions_df = DataFrame.from_dict(
            [
                merged_dict(submission, BOILERPLATE),
            ]
        )
        # act
        return submissions_to_assignment_submissions_dfs(submissions_df)

    def it_should_change_to_missing_state(assignment_submission_dict):
        submissions_df: DataFrame = list(assignment_submission_dict.values())[0]
        row_dict = submissions_df.to_dict(orient="records")[0]
        assert row_dict["SubmissionStatus"] == MISSING_STATE


def describe_when_a_submission_is_created_and_late_as_false_string():
    @pytest.fixture
    def assignment_submission_dict() -> Dict[Tuple[str, str], DataFrame]:
        # arrange
        submission: Dict[str, str] = {
            "state": CREATED_STATE,
            "late": "false",
        }

        submissions_df = DataFrame.from_dict(
            [
                merged_dict(submission, BOILERPLATE),
            ]
        )
        # act
        return submissions_to_assignment_submissions_dfs(submissions_df)

    def it_should_stay_created_state(assignment_submission_dict):
        submissions_df: DataFrame = list(assignment_submission_dict.values())[0]
        row_dict = submissions_df.to_dict(orient="records")[0]
        assert row_dict["SubmissionStatus"] == CREATED_STATE


def describe_when_a_submission_is_created_and_late_as_true_bool():
    @pytest.fixture
    def assignment_submission_dict() -> Dict[Tuple[str, str], DataFrame]:
        # arrange
        submission: Dict[str, str] = {
            "state": CREATED_STATE,
            "late": True,
        }

        submissions_df = DataFrame.from_dict(
            [
                merged_dict(submission, BOILERPLATE),
            ]
        )
        # act
        return submissions_to_assignment_submissions_dfs(submissions_df)

    def it_should_change_to_missing_state(assignment_submission_dict):
        submissions_df: DataFrame = list(assignment_submission_dict.values())[0]
        row_dict = submissions_df.to_dict(orient="records")[0]
        assert row_dict["SubmissionStatus"] == MISSING_STATE


def describe_when_a_submission_is_created_and_late_as_false_bool():
    @pytest.fixture
    def assignment_submission_dict() -> Dict[Tuple[str, str], DataFrame]:
        # arrange
        submission: Dict[str, str] = {
            "state": CREATED_STATE,
            "late": False,
        }

        submissions_df = DataFrame.from_dict(
            [
                merged_dict(submission, BOILERPLATE),
            ]
        )
        # act
        return submissions_to_assignment_submissions_dfs(submissions_df)

    def it_should_stay_created_state(assignment_submission_dict):
        submissions_df: DataFrame = list(assignment_submission_dict.values())[0]
        row_dict = submissions_df.to_dict(orient="records")[0]
        assert row_dict["SubmissionStatus"] == CREATED_STATE


def describe_when_a_submission_is_created_and_late_not_there():
    @pytest.fixture
    def assignment_submission_dict() -> Dict[Tuple[str, str], DataFrame]:
        # arrange
        submission: Dict[str, str] = {
            "state": CREATED_STATE,
        }

        submissions_df = DataFrame.from_dict(
            [
                merged_dict(submission, BOILERPLATE),
            ]
        )
        # act
        return submissions_to_assignment_submissions_dfs(submissions_df)

    def it_should_stay_created_state(assignment_submission_dict):
        submissions_df: DataFrame = list(assignment_submission_dict.values())[0]
        row_dict = submissions_df.to_dict(orient="records")[0]
        assert row_dict["SubmissionStatus"] == CREATED_STATE


def describe_when_a_submission_is_created_and_late_is_none():
    @pytest.fixture
    def assignment_submission_dict() -> Dict[Tuple[str, str], DataFrame]:
        # arrange
        submission: Dict[str, str] = {
            "state": CREATED_STATE,
            "late": None,
        }

        submissions_df = DataFrame.from_dict(
            [
                merged_dict(submission, BOILERPLATE),
            ]
        )
        # act
        return submissions_to_assignment_submissions_dfs(submissions_df)

    def it_should_stay_created_state(assignment_submission_dict):
        submissions_df: DataFrame = list(assignment_submission_dict.values())[0]
        row_dict = submissions_df.to_dict(orient="records")[0]
        assert row_dict["SubmissionStatus"] == CREATED_STATE


def describe_when_a_submission_is_turned_in_and_late_is_true():
    @pytest.fixture
    def assignment_submission_dict() -> Dict[Tuple[str, str], DataFrame]:
        # arrange
        submission: Dict[str, str] = {
            "state": TURNED_IN_STATE,
            "late": "true",
        }

        submissions_df = DataFrame.from_dict(
            [
                merged_dict(submission, BOILERPLATE),
            ]
        )
        # act
        return submissions_to_assignment_submissions_dfs(submissions_df)

    def it_should_change_to_late_state(assignment_submission_dict):
        submissions_df: DataFrame = list(assignment_submission_dict.values())[0]
        row_dict = submissions_df.to_dict(orient="records")[0]
        assert row_dict["SubmissionStatus"] == LATE_STATE


def describe_when_a_submission_is_new_and_late_is_true():
    @pytest.fixture
    def assignment_submission_dict() -> Dict[Tuple[str, str], DataFrame]:
        # arrange
        submission: Dict[str, str] = {
            "state": NEW_STATE,
            "late": "true",
        }

        submissions_df = DataFrame.from_dict(
            [
                merged_dict(submission, BOILERPLATE),
            ]
        )
        # act
        return submissions_to_assignment_submissions_dfs(submissions_df)

    def it_should_change_to_missing_state(assignment_submission_dict):
        submissions_df: DataFrame = list(assignment_submission_dict.values())[0]
        row_dict = submissions_df.to_dict(orient="records")[0]
        assert row_dict["SubmissionStatus"] == MISSING_STATE


def describe_when_a_submission_is_reclaimed_and_late_is_true():
    @pytest.fixture
    def assignment_submission_dict() -> Dict[Tuple[str, str], DataFrame]:
        # arrange
        submission: Dict[str, str] = {
            "state": RECLAIMED_STATE,
            "late": "true",
        }

        submissions_df = DataFrame.from_dict(
            [
                merged_dict(submission, BOILERPLATE),
            ]
        )
        # act
        return submissions_to_assignment_submissions_dfs(submissions_df)

    def it_should_change_to_missing_state(assignment_submission_dict):
        submissions_df: DataFrame = list(assignment_submission_dict.values())[0]
        row_dict = submissions_df.to_dict(orient="records")[0]
        assert row_dict["SubmissionStatus"] == MISSING_STATE


def describe_when_a_submission_is_returned_and_late_is_true():
    @pytest.fixture
    def assignment_submission_dict() -> Dict[Tuple[str, str], DataFrame]:
        # arrange
        submission: Dict[str, str] = {
            "state": RETURNED_STATE,
            "late": "true",
        }

        submissions_df = DataFrame.from_dict(
            [
                merged_dict(submission, BOILERPLATE),
            ]
        )
        # act
        return submissions_to_assignment_submissions_dfs(submissions_df)

    def it_should_stay_returned_state(assignment_submission_dict):
        submissions_df: DataFrame = list(assignment_submission_dict.values())[0]
        row_dict = submissions_df.to_dict(orient="records")[0]
        assert row_dict["SubmissionStatus"] == RETURNED_STATE
