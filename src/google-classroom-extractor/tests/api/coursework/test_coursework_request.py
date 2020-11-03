# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
import pook
from pandas.core.frame import DataFrame
from google_classroom_extractor.api.coursework import request_latest_coursework_as_df
from tests.api.api_helper import setup_fake_classroom_api

# unique value for each column in fixture
COURSE_ID = "1"
ID = "2"
TITLE = "3"
DESCRIPTION = "4"
MATERIALS_LINK_URL = "5"
MATERIALS_LINK_TITLE = "6"
MATERIALS_LINK_THUMBNAIL_URL = "7"
STATE = "8"
ALTERNATE_LINK = "9"
CREATION_TIME = "2020-09-02T20:25:17.399Z"
UPDATE_TIME = "2020-09-02T20:26:44.071Z"
DUEDATE_YEAR = "2000"
DUEDATE_MONTH = "10"
DUEDATE_DAY = "11"
DUETIME_HOURS = "12"
DUETIME_MINUTES = "13"
MAX_POINTS = "14"
WORK_TYPE = "15"
SUBMISSION_MODIFICATION_MODE = "16"
ASSIGNEE_MODE = "17"
CREATOR_USER_ID = "18"
SCHEDULED_TIME = "19"
TOPIC_ID = "20"


def describe_when_requesting_latest_coursework():
    @pytest.fixture
    def coursework_df() -> DataFrame:
        # arrange
        pook.activate()
        response_json = f"""
        {{
          "courseWork": [
            {{
              "courseId": "{COURSE_ID}",
              "id": "{ID}",
              "title": "{TITLE}",
              "description": "{DESCRIPTION}",
              "materials": [
                {{
                  "link": {{
                    "url": "{MATERIALS_LINK_URL}",
                    "title": "{MATERIALS_LINK_TITLE}",
                    "thumbnailUrl": "{MATERIALS_LINK_THUMBNAIL_URL}"
                  }}
                }}
              ],
              "state": "{STATE}",
              "alternateLink": "{ALTERNATE_LINK}",
              "creationTime": "{CREATION_TIME}",
              "updateTime": "{UPDATE_TIME}",
              "dueDate": {{
                "year": {DUEDATE_YEAR},
                "month": {DUEDATE_MONTH},
                "day": {DUEDATE_DAY}
              }},
              "dueTime": {{
                "hours": {DUETIME_HOURS},
                "minutes": {DUETIME_MINUTES}
              }},
              "maxPoints": {MAX_POINTS},
              "workType": "{WORK_TYPE}",
              "submissionModificationMode": "{SUBMISSION_MODIFICATION_MODE}",
              "assigneeMode": "{ASSIGNEE_MODE}",
              "creatorUserId": "{CREATOR_USER_ID}",
              "scheduledTime": "{SCHEDULED_TIME}",
              "topicId": "{TOPIC_ID}"
            }}
          ]
        }}
        """
        resource = setup_fake_classroom_api(
            f"courses/{COURSE_ID}/courseWork", response_json
        )

        # act
        return request_latest_coursework_as_df(resource, [COURSE_ID])

    def it_should_have_correct_dataframe_shape(coursework_df):
        row_count, column_count = coursework_df.shape
        assert row_count == 1
        assert column_count == 21

    def it_should_map_dataframe_columns_correctly(coursework_df):
        row_dict = coursework_df.to_dict(orient="records")[0]
        assert row_dict["courseId"] == COURSE_ID
        assert row_dict["id"] == ID
        assert row_dict["title"] == TITLE
        assert row_dict["description"] == DESCRIPTION
        assert (
            row_dict["materials"]
            == f"[{{'link': {{'url': '{MATERIALS_LINK_URL}', 'title': '{MATERIALS_LINK_TITLE}', 'thumbnailUrl': '{MATERIALS_LINK_THUMBNAIL_URL}'}}}}]"
        )
        assert row_dict["state"] == STATE
        assert row_dict["alternateLink"] == ALTERNATE_LINK
        assert row_dict["creationTime"] == CREATION_TIME
        assert row_dict["updateTime"] == UPDATE_TIME
        assert row_dict["maxPoints"] == MAX_POINTS
        assert row_dict["workType"] == WORK_TYPE
        assert row_dict["submissionModificationMode"] == SUBMISSION_MODIFICATION_MODE
        assert row_dict["assigneeMode"] == ASSIGNEE_MODE
        assert row_dict["creatorUserId"] == CREATOR_USER_ID
        assert row_dict["dueDate.year"] == DUEDATE_YEAR
        assert row_dict["dueDate.month"] == DUEDATE_MONTH
        assert row_dict["dueDate.day"] == DUEDATE_DAY
        assert row_dict["dueTime.hours"] == DUETIME_HOURS
        assert row_dict["dueTime.minutes"] == DUETIME_MINUTES
        assert row_dict["scheduledTime"] == SCHEDULED_TIME
        assert row_dict["topicId"] == TOPIC_ID
