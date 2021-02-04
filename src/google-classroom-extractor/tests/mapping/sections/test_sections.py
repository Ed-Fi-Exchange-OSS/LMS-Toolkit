# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
import pytest
from pandas import DataFrame
from edfi_google_classroom_extractor.mapping.sections import courses_to_sections_df
from edfi_google_classroom_extractor.mapping.constants import SOURCE_SYSTEM

# unique value for each column in fixture
COURSE_ID = "1"
NAME = "2"
SECTION = "3"
DESCRIPTION_HEADING = "4"
DESCRIPTION = "5"
ROOM = "6"
OWNER_ID = "7"
CREATION_TIME = "8"
UPDATE_TIME = "9"
ENROLLMENT_CODE = "10"
COURSE_STATE = "11"
ALTERNATE_LINK = "12"
TEACHER_GROUP_EMAIL = "13"
COURSE_GROUP_EMAIL = "14"
GUARDIANS_ENABLED = "15"
CALENDAR_ID = "16"
CREATE_DATE = "17"
LAST_MODIFIED_DATE = "18"


def describe_when_a_single_coursework_with_unique_fields_is_mapped():
    @pytest.fixture
    def sections_df() -> DataFrame:
        courses_df: DataFrame = DataFrame(
            {
                "id": [COURSE_ID],
                "name": [NAME],
                "section": [SECTION],
                "descriptionHeading": [DESCRIPTION_HEADING],
                "description": [DESCRIPTION],
                "room": [ROOM],
                "ownerId": [OWNER_ID],
                "creationTime": [CREATION_TIME],
                "updateTime": [UPDATE_TIME],
                "enrollmentCode": [ENROLLMENT_CODE],
                "courseState": [COURSE_STATE],
                "alternateLink": [ALTERNATE_LINK],
                "teacherGroupEmail": [TEACHER_GROUP_EMAIL],
                "courseGroupEmail": [COURSE_GROUP_EMAIL],
                "guardiansEnabled": [GUARDIANS_ENABLED],
                "calendarId": [CALENDAR_ID],
                "CreateDate": [CREATE_DATE],
                "LastModifiedDate": [LAST_MODIFIED_DATE],
            }
        )

        # act
        return courses_to_sections_df(courses_df)

    def it_should_have_correct_shape(sections_df):
        row_count, column_count = sections_df.shape
        assert row_count == 1
        assert column_count == 11

    def it_should_map_fields_correctly(sections_df):
        row_dict = sections_df.to_dict(orient="records")[0]
        assert row_dict["SourceSystemIdentifier"] == COURSE_ID
        assert row_dict["LMSSectionStatus"] == COURSE_STATE
        assert row_dict["SectionDescription"] == DESCRIPTION_HEADING
        assert row_dict["Title"] == NAME
        assert row_dict["SourceCreateDate"] == CREATION_TIME
        assert row_dict["SourceLastModifiedDate"] == UPDATE_TIME
        assert row_dict["SourceSystem"] == SOURCE_SYSTEM
        assert row_dict["SISSectionIdentifier"] == ""
        assert row_dict["Term"] == ""
        assert row_dict["CreateDate"] == CREATE_DATE
        assert row_dict["LastModifiedDate"] == LAST_MODIFIED_DATE
