# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
import pook
from pandas.core.frame import DataFrame
from google_classroom_extractor.api.submissions import request_latest_submissions_as_df
from tests.api.api_helper import setup_fake_classroom_api

# unique value for each column in fixture
COURSE_ID = "1"
COURSEWORK_ID = "2"
ID = "3"
USER_ID = "4"
CREATION_TIME = "2020-08-21T16:21:24.400Z"
UPDATE_TIME = "2020-08-21T16:37:02.606Z"
STATE = "7"
LATE = "8"
DRAFT_GRADE = "9"
ASSIGNED_GRADE = "10"
ALTERNATE_LINK = "11"
COURSEWORK_TYPE = "12"
ASSOCIATED_WITH_DEVELOPER = "13"


def describe_when_requesting_latest_submissions():
    @pytest.fixture
    def submissions_df() -> DataFrame:
        # arrange
        pook.activate()
        response_json = f"""
        {{
          "studentSubmissions": [
            {{
              "courseId": "{COURSE_ID}",
              "courseWorkId": "{COURSEWORK_ID}",
              "id": "{ID}",
              "userId": "{USER_ID}",
              "creationTime": "{CREATION_TIME}",
              "updateTime": "{UPDATE_TIME}",
              "state": "{STATE}",
              "late": "{LATE}",
              "draftGrade": "{DRAFT_GRADE}",
              "assignedGrade": "{ASSIGNED_GRADE}",
              "alternateLink": "{ALTERNATE_LINK}",
              "courseWorkType": "{COURSEWORK_TYPE}",
              "associatedWithDeveloper": "{ASSOCIATED_WITH_DEVELOPER}",
              "assignmentSubmission": {{
                "attachments": [
                  {{
                    "driveFile": {{
                      "id": "a",
                      "title": "b",
                      "alternateLink": "c",
                      "thumbnailUrl": "d"
                    }}
                  }}
                ]
              }},
              "submissionHistory": [
                {{
                  "stateHistory": {{
                    "state": "e",
                    "stateTimestamp": "f",
                    "actorUserId": "g"
                  }}
                }}
              ]
            }}
          ]
        }}
        """
        resource = setup_fake_classroom_api(
            f"courses/{COURSE_ID}/courseWork/-/studentSubmissions", response_json
        )

        # act
        return request_latest_submissions_as_df(resource, [COURSE_ID])

    def it_should_have_correct_dataframe_shape(submissions_df):
        row_count, column_count = submissions_df.shape
        assert row_count == 1
        assert column_count == 15

    def it_should_map_dataframe_columns_correctly(submissions_df):
        row_dict = submissions_df.to_dict(orient="records")[0]
        assert row_dict["courseId"] == COURSE_ID
        assert row_dict["courseWorkId"] == COURSEWORK_ID
        assert row_dict["id"] == ID
        assert row_dict["userId"] == USER_ID
        assert row_dict["creationTime"] == CREATION_TIME
        assert row_dict["updateTime"] == UPDATE_TIME
        assert row_dict["state"] == STATE
        assert row_dict["late"] == LATE
        assert row_dict["draftGrade"] == DRAFT_GRADE
        assert row_dict["assignedGrade"] == ASSIGNED_GRADE
        assert row_dict["alternateLink"] == ALTERNATE_LINK
        assert row_dict["courseWorkType"] == COURSEWORK_TYPE
        assert row_dict["associatedWithDeveloper"] == ASSOCIATED_WITH_DEVELOPER
        assert (
            row_dict["submissionHistory"]
            == "[{'stateHistory': {'state': 'e', 'stateTimestamp': 'f', 'actorUserId': 'g'}}]"
        )
        assert (
            row_dict["assignmentSubmission.attachments"]
            == "[{'driveFile': {'id': 'a', 'title': 'b', 'alternateLink': 'c', 'thumbnailUrl': 'd'}}]"
        )
