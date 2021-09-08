# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict, Tuple
import pytest
from pandas import DataFrame
from edfi_google_classroom_extractor.mapping.assignment_submissions import (
    submissions_to_assignment_submissions_dfs, _get_submission_datetime
)
from edfi_google_classroom_extractor.mapping.constants import SOURCE_SYSTEM
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
                "associatedWithDeveloper": [ASSOCIATED_WITH_DEVELOPER],
                "submissionHistory": [SUBMISSION_HISTORY],
                "CreateDate": [CREATE_DATE],
                "LastModifiedDate": [LAST_MODIFIED_DATE],
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
        assert column_count == 12

    def it_should_map_fields_correctly(assignment_submissions_dicts):
        submissions_df: DataFrame = assignment_submissions_dicts[
            (COURSE_ID, f"{COURSE_ID}-{COURSEWORK_ID}")
        ]
        row_dict = submissions_df.to_dict(orient="records")[0]

        assert (
            row_dict["AssignmentSourceSystemIdentifier"]
            == f"{COURSE_ID}-{COURSEWORK_ID}"
        )
        assert row_dict["EarnedPoints"] == ASSIGNED_GRADE
        assert row_dict["Grade"] == ASSIGNED_GRADE
        assert row_dict["SourceSystem"] == SOURCE_SYSTEM
        assert row_dict["SourceSystemIdentifier"] == f"{COURSE_ID}-{COURSEWORK_ID}-{ID}"
        assert row_dict["SubmissionStatus"] == STATE
        assert row_dict["SubmissionDateTime"] == "2021-10-02T16:38:34.895Z"
        assert row_dict["LMSUserSourceSystemIdentifier"] == USER_ID
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
    "associatedWithDeveloper": ASSOCIATED_WITH_DEVELOPER,
    "submissionHistory": SUBMISSION_HISTORY,
    "CreateDate": CREATE_DATE,
    "LastModifiedDate": LAST_MODIFIED_DATE,
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


def describe_when_mapping_submission_datetime():
    def given_it_has_final_turned_in_status():
        SUBMISSION_HISTORY_TURNED_IN = """[
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
                "associatedWithDeveloper": [ASSOCIATED_WITH_DEVELOPER],
                "submissionHistory": SUBMISSION_HISTORY_TURNED_IN,
                "CreateDate": [CREATE_DATE],
                "LastModifiedDate": [LAST_MODIFIED_DATE],
            }
        )

        def it_should_return_a_submission_date_matching_turned_in_record():
            # act
            submissions_df["SubmissionDateTime"] = submissions_df.apply(
                _get_submission_datetime,
                axis=1,
            )

            # assert
            submission_dict = submissions_df.to_dict()[0]
            assert submission_dict["SubmissionDateTime"] == "2021-10-02T16:38:34.895Z"

    def given_it_has_final_reclaimed_by_student_status():
        SUBMISSION_HISTORY_RECLAIMED_BY_STUDENT = """[
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
                    "stateTimestamp": "2021-09-02T16:38:34.895Z",
                    "actorUserId": "114946936387309047192"
                }
                },
                {
                "stateHistory": {
                    "state": "RECLAIMED_BY_STUDENT",
                    "stateTimestamp": "2021-10-02T16:38:34.895Z",
                    "actorUserId": "114946936387309047192"
                }
                }
            ]"""

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
                "associatedWithDeveloper": [ASSOCIATED_WITH_DEVELOPER],
                "submissionHistory": SUBMISSION_HISTORY_RECLAIMED_BY_STUDENT,
                "CreateDate": [CREATE_DATE],
                "LastModifiedDate": [LAST_MODIFIED_DATE],
            }
        )

        def it_should_return_an_empty_submission_datetime_record():
            # act
            submissions_df["SubmissionDateTime"] = submissions_df.apply(
                _get_submission_datetime,
                axis=1,
            )

            # assert
            submission_dict = submissions_df.to_dict()[0]
            assert submission_dict["SubmissionDateTime"] == ""

    def given_it_has_not_been_sent():
        SUBMISSION_HISTORY_NOT_SENT = """[
                {
                "stateHistory": {
                    "state": "CREATED",
                    "stateTimestamp": "2021-09-02T16:38:34.895Z",
                    "actorUserId": "114946936387309047192"
                }
                }
            ]"""
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
                "associatedWithDeveloper": [ASSOCIATED_WITH_DEVELOPER],
                "submissionHistory": SUBMISSION_HISTORY_NOT_SENT,
                "CreateDate": [CREATE_DATE],
                "LastModifiedDate": [LAST_MODIFIED_DATE],
            }
        )

        def it_should_return_an_empty_submission_datetime_record():
            # act
            submissions_df["SubmissionDateTime"] = submissions_df.apply(
                _get_submission_datetime,
                axis=1,
            )

            # assert
            submission_dict = submissions_df.to_dict()[0]
            assert submission_dict["SubmissionDateTime"] == ""

    def given_it_has_been_graded():
        SUBMISSION_HISTORY_TURNED_IN = """[
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
                },
                {
                "stateHistory": {
                    "state": "RETURNED",
                    "stateTimestamp": "2021-11-02T16:38:34.895Z",
                    "actorUserId": "114946936387309047192"
                }
                }
            ]"""

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
                "associatedWithDeveloper": [ASSOCIATED_WITH_DEVELOPER],
                "submissionHistory": SUBMISSION_HISTORY_TURNED_IN,
                "CreateDate": [CREATE_DATE],
                "LastModifiedDate": [LAST_MODIFIED_DATE],
            }
        )

        def it_should_take_the_date_for_turned_in():
            # act
            submissions_df["SubmissionDateTime"] = submissions_df.apply(
                _get_submission_datetime,
                axis=1,
            )

            # assert
            submission_dict = submissions_df.to_dict()[0]
            assert submission_dict["SubmissionDateTime"] == "2021-10-02T16:38:34.895Z"

    def given_it_has_been_sent_then_reclaimed_by_the_student_then_resent():
        SUBMISSION_HISTORY_COMPLEX = """[
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
                },
                {
                "stateHistory": {
                    "state": "RECLAIMED_BY_STUDENT",
                    "stateTimestamp": "2021-11-02T16:38:34.895Z",
                    "actorUserId": "114946936387309047192"
                },
                {
                "stateHistory": {
                    "state": "TURNED_IN",
                    "stateTimestamp": "2021-12-02T16:38:34.895Z",
                    "actorUserId": "114946936387309047192"
                }
                }
            ]"""

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
                "associatedWithDeveloper": [ASSOCIATED_WITH_DEVELOPER],
                "submissionHistory": SUBMISSION_HISTORY_COMPLEX,
                "CreateDate": [CREATE_DATE],
                "LastModifiedDate": [LAST_MODIFIED_DATE],
            }
        )

        def it_should_take_the_last_date_of_turned_in_status():
            # act
            submissions_df["SubmissionDateTime"] = submissions_df.apply(
                _get_submission_datetime,
                axis=1,
            )

            # assert
            submission_dict = submissions_df.to_dict()[0]
            assert submission_dict["SubmissionDateTime"] == "2021-12-02T16:38:34.895Z"
