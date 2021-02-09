# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict
import pytest
from pandas import DataFrame
from edfi_google_classroom_extractor.mapping.user_submission_activities import (
    submissions_to_user_submission_activities_dfs,
    ACTIVITY_TYPE_STATE,
    ACTIVITY_TYPE_GRADE,
)
from edfi_google_classroom_extractor.mapping.constants import SOURCE_SYSTEM

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
STATE = "14"
STATE_TIMESTAMP = "15"
GRADE_CHANGE_TYPE = "16"
GRADE_TIMESTAMP = "17"
ACTOR_USER_ID = "18"
LAST_MODIFIED_DATE = "02-01-2020"
CREATE_DATE = "01-01-2020"
STATE_SUBMISSION_HISTORY = f"{{'stateHistory': {{'state': '{STATE}', 'stateTimestamp': '{STATE_TIMESTAMP}', 'actorUserId': '{ACTOR_USER_ID}'}}}}"
GRADE_SUBMISSION_HISTORY = f"{{'gradeHistory': {{'pointsEarned': 0, 'maxPoints': 1, 'gradeTimestamp': '{GRADE_TIMESTAMP}', 'actorUserId': '{ACTOR_USER_ID}', 'gradeChangeType': '{GRADE_CHANGE_TYPE}'}}}}"


def describe_when_a_single_state_submission_with_unique_fields_is_mapped():
    @pytest.fixture
    def assignment_submissions_dicts() -> Dict[str, DataFrame]:
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
                "submissionHistory": [f"[{STATE_SUBMISSION_HISTORY}]"],
                "CreateDate": [CREATE_DATE],
                "LastModifiedDate": [LAST_MODIFIED_DATE],
            }
        )

        # act
        return submissions_to_user_submission_activities_dfs(submissions_df)

    def it_should_have_correct_shape(assignment_submissions_dicts):
        assert len(assignment_submissions_dicts) == 1

        submissions_df: DataFrame = assignment_submissions_dicts[COURSE_ID]
        row_count, column_count = submissions_df.shape

        assert row_count == 1
        assert column_count == 14

    def it_should_map_fields_correctly(assignment_submissions_dicts):
        submissions_df: DataFrame = assignment_submissions_dicts[COURSE_ID]
        state_row = submissions_df.to_dict(orient="records")[0]

        assert state_row["ActivityDateTime"] == STATE_TIMESTAMP
        assert state_row["ActivityStatus"] == STATE
        assert state_row["ActivityTimeInMinutes"] == ""
        assert state_row["ActivityType"] == ACTIVITY_TYPE_STATE
        assert state_row["AssignmentIdentifier"] == f"{COURSE_ID}-{COURSEWORK_ID}"
        assert state_row["SourceSystem"] == SOURCE_SYSTEM
        assert (
            state_row["SourceSystemIdentifier"]
            == f"S-{COURSE_ID}-{COURSEWORK_ID}-{ID}-{STATE_TIMESTAMP}"
        )
        assert state_row["Content"] == ""
        assert state_row["LMSSectionIdentifier"] == COURSE_ID
        assert state_row["LMSUserIdentifier"] == ACTOR_USER_ID


def describe_when_a_state_and_a_grade_submission_is_mapped():
    @pytest.fixture
    def assignment_submissions_dicts() -> Dict[str, DataFrame]:
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
                "submissionHistory": [
                    f"[{STATE_SUBMISSION_HISTORY},{GRADE_SUBMISSION_HISTORY}]"
                ],
                "CreateDate": CREATE_DATE,
                "LastModifiedDate": LAST_MODIFIED_DATE,
            }
        )

        # act
        return submissions_to_user_submission_activities_dfs(submissions_df)

    def it_should_have_correct_shape(assignment_submissions_dicts):
        assert len(assignment_submissions_dicts) == 1

        submissions_df: DataFrame = assignment_submissions_dicts[COURSE_ID]
        row_count, column_count = submissions_df.shape

        assert row_count == 2
        assert column_count == 14

    def it_should_map_state_fields_correctly(assignment_submissions_dicts):
        submissions_df: DataFrame = assignment_submissions_dicts[COURSE_ID]
        state_row = submissions_df.to_dict(orient="records")[0]

        assert state_row["ActivityDateTime"] == STATE_TIMESTAMP
        assert state_row["ActivityStatus"] == STATE
        assert state_row["ActivityTimeInMinutes"] == ""
        assert state_row["ActivityType"] == ACTIVITY_TYPE_STATE
        assert state_row["AssignmentIdentifier"] == f"{COURSE_ID}-{COURSEWORK_ID}"
        assert state_row["SourceSystem"] == SOURCE_SYSTEM
        assert (
            state_row["SourceSystemIdentifier"]
            == f"S-{COURSE_ID}-{COURSEWORK_ID}-{ID}-{STATE_TIMESTAMP}"
        )
        assert state_row["Content"] == ""
        assert state_row["LMSSectionIdentifier"] == COURSE_ID
        assert state_row["LMSUserIdentifier"] == ACTOR_USER_ID

    def it_should_map_grade_fields_correctly(assignment_submissions_dicts):
        submissions_df: DataFrame = assignment_submissions_dicts[COURSE_ID]
        grade_row = submissions_df.to_dict(orient="records")[1]

        assert grade_row["ActivityDateTime"] == GRADE_TIMESTAMP
        assert grade_row["ActivityStatus"] == GRADE_CHANGE_TYPE
        assert grade_row["ActivityTimeInMinutes"] == ""
        assert grade_row["ActivityType"] == ACTIVITY_TYPE_GRADE
        assert grade_row["AssignmentIdentifier"] == f"{COURSE_ID}-{COURSEWORK_ID}"
        assert grade_row["SourceSystem"] == SOURCE_SYSTEM
        assert (
            grade_row["SourceSystemIdentifier"]
            == f"G-{COURSE_ID}-{COURSEWORK_ID}-{ID}-{GRADE_TIMESTAMP}"
        )
        assert grade_row["Content"] == ""
        assert grade_row["LMSSectionIdentifier"] == COURSE_ID
        assert grade_row["LMSUserIdentifier"] == ACTOR_USER_ID
