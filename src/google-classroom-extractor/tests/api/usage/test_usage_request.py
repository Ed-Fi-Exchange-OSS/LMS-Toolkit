# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import pytest
import pook
from pandas.core.frame import DataFrame
from google_classroom_extractor.api.usage import request_latest_usage_as_df
from tests.api.api_helper import setup_fake_reports_api

# unique value for each column in fixture
EMAIL = "em"
NUM_POSTS_CREATED = 1
LAST_INTERACTION_TIME = "1970-01-01T00:00:00.000Z"
LAST_LOGIN_TIME = "2020-08-17T20:31:00.000Z"


def describe_when_requesting_latest_usage():
    @pytest.fixture
    def usage_df() -> DataFrame:
        # arrange
        pook.activate()
        response_json = f"""
        {{
          "kind": "admin#reports#usageReports",
          "etag": "a",
          "usageReports": [
            {{
              "kind": "admin#reports#usageReport",
              "date": "2020-08-17",
              "etag": "b",
              "entity": {{
                "type": "USER",
                "customerId": "c",
                "userEmail": "{EMAIL}",
                "profileId": "e"
              }},
              "parameters": [
                {{
                  "name": "classroom:num_posts_created",
                  "intValue": "{NUM_POSTS_CREATED}"
                }},
                {{
                  "name": "classroom:last_interaction_time",
                  "datetimeValue": "{LAST_INTERACTION_TIME}"
                }},
                {{
                  "name": "accounts:last_login_time",
                  "datetimeValue": "{LAST_LOGIN_TIME}"
                }}
              ]
            }}
          ]
        }}
        """
        resource = setup_fake_reports_api(
            "usage/users/all/dates/2020-08-17", response_json
        )

        # act
        return request_latest_usage_as_df(resource, datetime(2020, 8, 17, 0, 0), datetime(2020, 8, 17, 12, 0))

    def it_should_have_correct_dataframe_shape(usage_df):
        row_count, column_count = usage_df.shape
        assert row_count == 1
        assert column_count == 9

    def it_should_map_dataframe_columns_correctly(usage_df):
        row_dict = usage_df.to_dict(orient="records")[0]
        assert row_dict["email"] == EMAIL
        assert row_dict["asOfDate"] == datetime(2020, 8, 17, 0, 0)
        assert row_dict["numberOfPosts"] == NUM_POSTS_CREATED
        assert row_dict["lastInteractionTime"] == datetime(1970, 1, 1, 0, 0)
        assert row_dict["lastLoginTime"] == datetime(2020, 8, 17, 20, 31)
        assert row_dict["name"] == EMAIL
        assert row_dict["monthDay"] == "08/17"
        assert row_dict["nameDate"] == f"{EMAIL} 08/17"
