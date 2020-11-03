# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
import pook
from pandas.core.frame import DataFrame
from google_classroom_extractor.api.teachers import request_latest_teachers_as_df
from tests.api.api_helper import setup_fake_classroom_api

# unique value for each column in fixture
COURSE_ID = "1"
USER_ID = "2"
PROFILE_ID = "3"
GIVEN_NAME = "4"
FAMILY_NAME = "5"
FULL_NAME = "6"
EMAIL_ADDRESS = "7"


def describe_when_requesting_latest_teachers():
    @pytest.fixture
    def teachers_df() -> DataFrame:
        # arrange
        pook.activate()
        response_json = f"""
        {{
          "teachers": [
            {{
              "courseId": "{COURSE_ID}",
              "userId": "{USER_ID}",
              "profile": {{
                "id": "{PROFILE_ID}",
                "name": {{
                  "givenName": "{GIVEN_NAME}",
                  "familyName": "{FAMILY_NAME}",
                  "fullName": "{FULL_NAME}"
                }},
                "emailAddress": "{EMAIL_ADDRESS}"
              }}
            }}
          ]
        }}
        """
        resource = setup_fake_classroom_api(
            f"courses/{COURSE_ID}/teachers", response_json
        )

        # act
        return request_latest_teachers_as_df(resource, [COURSE_ID])

    def it_should_have_correct_dataframe_shape(teachers_df):
        row_count, column_count = teachers_df.shape
        assert row_count == 1
        assert column_count == 7

    def it_should_map_dataframe_columns_correctly(teachers_df):
        row_dict = teachers_df.to_dict(orient="records")[0]
        assert row_dict["courseId"] == COURSE_ID
        assert row_dict["userId"] == USER_ID
        assert row_dict["profile.id"] == PROFILE_ID
        assert row_dict["profile.name.givenName"] == GIVEN_NAME
        assert row_dict["profile.name.familyName"] == FAMILY_NAME
        assert row_dict["profile.name.fullName"] == FULL_NAME
        assert row_dict["profile.emailAddress"] == EMAIL_ADDRESS
