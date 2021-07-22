# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
import pook
from pandas.core.frame import DataFrame
from edfi_google_classroom_extractor.api.courses import (
    request_latest_courses_as_df,
    EDFI_LMS_PREFIX,
)
from tests.api.api_helper import setup_fake_classroom_api

# unique value for each column in fixture
COURSE_ID = "1"
NAME = "2"
SECTION = "3"
DESCRIPTION_HEADING = "4"
DESCRIPTION = "5"
ROOM = "6"
OWNER_ID = "7"
CREATION_TIME = "2020-08-19T19:59:10.548Z"
UPDATE_TIME = "2020-08-21T15:11:15.181Z"
ENROLLMENT_CODE = "10"
COURSE_STATE = "11"
ALTERNATE_LINK = "12"
TEACHER_GROUP_EMAIL = "13"
COURSE_GROUP_EMAIL = "14"
TEACHER_FOLDER_ID = "15"
TEACHER_FOLDER_TITLE = "16"
TEACHER_FOLDER_ALTERNATE_LINK = "17"
GUARDIANS_ENABLED = "18"
CALENDAR_ID = "19"

COURSES_RESPONSE_JSON = f"""
{{
    "courses": [
    {{
        "id": "{COURSE_ID}",
        "name": "{NAME}",
        "section": "{SECTION}",
        "descriptionHeading": "{DESCRIPTION_HEADING}",
        "room": "{ROOM}",
        "ownerId": "{OWNER_ID}",
        "creationTime": "{CREATION_TIME}",
        "updateTime": "{UPDATE_TIME}",
        "enrollmentCode": "{ENROLLMENT_CODE}",
        "courseState": "{COURSE_STATE}",
        "alternateLink": "{ALTERNATE_LINK}",
        "teacherGroupEmail": "{TEACHER_GROUP_EMAIL}",
        "courseGroupEmail": "{COURSE_GROUP_EMAIL}",
        "teacherFolder": {{
        "id": "{TEACHER_FOLDER_ID}",
        "title": "{TEACHER_FOLDER_TITLE}",
        "alternateLink": "{TEACHER_FOLDER_ALTERNATE_LINK}"
        }},
        "guardiansEnabled": "{GUARDIANS_ENABLED}",
        "calendarId": "{CALENDAR_ID}"
    }}
    ]
}}
"""


def describe_when_requesting_courses_with_no_aliases():
    @pytest.fixture
    def courses_df() -> DataFrame:
        # arrange
        pook.activate()
        aliases_response_json = """
        {
          "aliases": []
        }
        """
        resource = setup_fake_classroom_api(
            [
                ("courses", COURSES_RESPONSE_JSON),
                (f"courses/{COURSE_ID}/aliases", aliases_response_json),
            ]
        )

        # act
        return request_latest_courses_as_df(resource)

    def it_should_have_correct_dataframe_shape(courses_df):
        row_count, column_count = courses_df.shape
        assert row_count == 1
        assert column_count == 19

    def it_should_map_dataframe_columns_correctly(courses_df):
        row_dict = courses_df.to_dict(orient="records")[0]
        assert row_dict["id"] == COURSE_ID
        assert row_dict["name"] == NAME
        assert row_dict["section"] == SECTION
        assert row_dict["descriptionHeading"] == DESCRIPTION_HEADING
        assert row_dict["room"] == ROOM
        assert row_dict["ownerId"] == OWNER_ID
        assert row_dict["creationTime"] == CREATION_TIME
        assert row_dict["updateTime"] == UPDATE_TIME
        assert row_dict["enrollmentCode"] == ENROLLMENT_CODE
        assert row_dict["courseState"] == COURSE_STATE
        assert row_dict["alternateLink"] == ALTERNATE_LINK
        assert row_dict["teacherGroupEmail"] == TEACHER_GROUP_EMAIL
        assert row_dict["courseGroupEmail"] == COURSE_GROUP_EMAIL
        assert row_dict["teacherFolder.id"] == TEACHER_FOLDER_ID
        assert row_dict["teacherFolder.title"] == TEACHER_FOLDER_TITLE
        assert row_dict["teacherFolder.alternateLink"] == TEACHER_FOLDER_ALTERNATE_LINK
        assert row_dict["guardiansEnabled"] == GUARDIANS_ENABLED
        assert row_dict["calendarId"] == CALENDAR_ID
        assert row_dict["alias"] == ""


def describe_when_requesting_courses_with_single_alias_without_scope_prefix():
    ALIASES = """
    {"alias": "unexpected_form"}
    """

    @pytest.fixture
    def courses_df() -> DataFrame:
        # arrange
        pook.activate()
        aliases_response_json = f"""
        {{
          "aliases": [{ALIASES}]
        }}
        """
        resource = setup_fake_classroom_api(
            [
                ("courses", COURSES_RESPONSE_JSON),
                (f"courses/{COURSE_ID}/aliases", aliases_response_json),
            ]
        )

        # act
        return request_latest_courses_as_df(resource)

    def it_should_ignore_alias_without_scope_prefix(courses_df):
        row_dict = courses_df.to_dict(orient="records")[0]
        assert row_dict["alias"] == ""


def describe_when_requesting_courses_with_mutliple_alias_without_scope_prefix():
    ALIASES = """
    {"alias": "unexpected_form1"},
    {"alias": "unexpected_form2"},
    {"alias": "unexpected_form3"}
    """

    @pytest.fixture
    def courses_df() -> DataFrame:
        # arrange
        pook.activate()
        aliases_response_json = f"""
        {{
          "aliases": [{ALIASES}]
        }}
        """
        resource = setup_fake_classroom_api(
            [
                ("courses", COURSES_RESPONSE_JSON),
                (f"courses/{COURSE_ID}/aliases", aliases_response_json),
            ]
        )

        # act
        return request_latest_courses_as_df(resource)

    def it_should_ignore_aliases_without_scope_prefix(courses_df):
        row_dict = courses_df.to_dict(orient="records")[0]
        assert row_dict["alias"] == ""


def describe_when_requesting_courses_with_single_malformed_alias():
    ALIASES = """
    {"alias": "d:"}
    """

    @pytest.fixture
    def courses_df() -> DataFrame:
        # arrange
        pook.activate()
        aliases_response_json = f"""
        {{
          "aliases": [{ALIASES}]
        }}
        """
        resource = setup_fake_classroom_api(
            [
                ("courses", COURSES_RESPONSE_JSON),
                (f"courses/{COURSE_ID}/aliases", aliases_response_json),
            ]
        )

        # act
        return request_latest_courses_as_df(resource)

    def it_should_ignore_malformed_alias(courses_df):
        row_dict = courses_df.to_dict(orient="records")[0]
        assert row_dict["alias"] == ""


def describe_when_requesting_courses_with_multiple_malformed_aliases():
    ALIASES = """
    {"alias": "d:"},
    {"alias": "d:"}
    """

    @pytest.fixture
    def courses_df() -> DataFrame:
        # arrange
        pook.activate()
        aliases_response_json = f"""
        {{
          "aliases": [{ALIASES}]
        }}
        """
        resource = setup_fake_classroom_api(
            [
                ("courses", COURSES_RESPONSE_JSON),
                (f"courses/{COURSE_ID}/aliases", aliases_response_json),
            ]
        )

        # act
        return request_latest_courses_as_df(resource)

    def it_should_ignore_malformed_aliases(courses_df):
        row_dict = courses_df.to_dict(orient="records")[0]
        assert row_dict["alias"] == ""


def describe_when_requesting_courses_with_aliases_with_unknown_scopes():
    ALIASES = """
    {"alias": "q:unknown_scope1"},
    {"alias": "r:unknown_scope2"}
    """

    @pytest.fixture
    def courses_df() -> DataFrame:
        # arrange
        pook.activate()
        aliases_response_json = f"""
        {{
          "aliases": [{ALIASES}]
        }}
        """
        resource = setup_fake_classroom_api(
            [
                ("courses", COURSES_RESPONSE_JSON),
                (f"courses/{COURSE_ID}/aliases", aliases_response_json),
            ]
        )

        # act
        return request_latest_courses_as_df(resource)

    def it_should_ignore_malformed_aliases(courses_df):
        row_dict = courses_df.to_dict(orient="records")[0]
        assert row_dict["alias"] == ""


def describe_when_requesting_courses_with_single_alias_with_domain_prefix():
    ALIASES = """
    {"alias": "d:domain_alias"}
    """

    @pytest.fixture
    def courses_df() -> DataFrame:
        # arrange
        pook.activate()
        aliases_response_json = f"""
        {{
          "aliases": [{ALIASES}]
        }}
        """
        resource = setup_fake_classroom_api(
            [
                ("courses", COURSES_RESPONSE_JSON),
                (f"courses/{COURSE_ID}/aliases", aliases_response_json),
            ]
        )

        # act
        return request_latest_courses_as_df(resource)

    def it_should_map_to_alias_name(courses_df):
        row_dict = courses_df.to_dict(orient="records")[0]
        assert row_dict["alias"] == "domain_alias"


def describe_when_requesting_courses_with_multiple_domain_prefixes():
    ALIASES = """
    {"alias": "d:domain_alias1"},
    {"alias": "d:domain_alias2"},
    {"alias": "d:domain_alias3"}
    """

    @pytest.fixture
    def courses_df() -> DataFrame:
        # arrange
        pook.activate()
        aliases_response_json = f"""
        {{
          "aliases": [{ALIASES}]
        }}
        """
        resource = setup_fake_classroom_api(
            [
                ("courses", COURSES_RESPONSE_JSON),
                (f"courses/{COURSE_ID}/aliases", aliases_response_json),
            ]
        )

        # act
        return request_latest_courses_as_df(resource)

    def it_should_map_to_the_first_domain_alias(courses_df):
        row_dict = courses_df.to_dict(orient="records")[0]
        assert row_dict["alias"] == "domain_alias1"


def describe_when_requesting_courses_with_multiple_domain_prefixes_and_some_marked_edfilms():
    ALIASES = f"""
    {{"alias": "d:domain_alias1"}},
    {{"alias": "d:{EDFI_LMS_PREFIX}domain_alias2"}},
    {{"alias": "d:{EDFI_LMS_PREFIX}domain_alias3"}},
    {{"alias": "d:domain_alias4"}}
    """

    @pytest.fixture
    def courses_df() -> DataFrame:
        # arrange
        pook.activate()
        aliases_response_json = f"""
        {{
          "aliases": [{ALIASES}]
        }}
        """
        resource = setup_fake_classroom_api(
            [
                ("courses", COURSES_RESPONSE_JSON),
                (f"courses/{COURSE_ID}/aliases", aliases_response_json),
            ]
        )

        # act
        return request_latest_courses_as_df(resource)

    def it_should_map_to_first_edfi_domain_alias(courses_df):
        row_dict = courses_df.to_dict(orient="records")[0]
        assert row_dict["alias"] == "domain_alias2"
