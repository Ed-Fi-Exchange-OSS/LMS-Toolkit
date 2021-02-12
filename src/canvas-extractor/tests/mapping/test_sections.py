# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
import pytest
from pandas import DataFrame
from edfi_canvas_extractor.mapping.sections import map_to_udm_sections
from edfi_canvas_extractor.mapping.constants import SOURCE_SYSTEM

# unique value for each column in fixture
ID = "1"
COURSE_ID = "2"
NAME = "3"
START_AT = "4"
END_AT = "5"
CREATED_AT = "6"
CREATED_AT_DATE = "7"
RESTRICT_ENROLLMENTS_TO_SECTION_DATES = "8"
NONXLIST_COURSE_ID = "9"
SIS_SECTION_ID = "10"
SIS_COURSE_ID = "11"
INTEGRATION_ID = "12"
SIS_IMPORT_ID = "13"
CREATE_DATE = "14"
LAST_MODIFIED_DATE = "15"


def describe_when_a_single_section_with_unique_fields_is_mapped():
    @pytest.fixture
    def sections_df() -> DataFrame:
        section_df: DataFrame = DataFrame(
            {
                "id": [ID],
                "course_id": [COURSE_ID],
                "name": [NAME],
                "start_at": [START_AT],
                "end_at": [END_AT],
                "created_at": [CREATED_AT],
                "created_at_date": [CREATED_AT_DATE],
                "restrict_enrollments_to_section_dates": [
                    RESTRICT_ENROLLMENTS_TO_SECTION_DATES
                ],
                "nonxlist_course_id": [NONXLIST_COURSE_ID],
                "sis_section_id": [SIS_SECTION_ID],
                "sis_course_id": [SIS_COURSE_ID],
                "integration_id": [INTEGRATION_ID],
                "sis_import_id": [SIS_IMPORT_ID],
                "CreateDate": [CREATE_DATE],
                "LastModifiedDate": [LAST_MODIFIED_DATE],
            }
        )

        # act
        return map_to_udm_sections(section_df)

    def it_should_have_correct_shape(sections_df):
        row_count, column_count = sections_df.shape
        assert row_count == 1
        assert column_count == 11

    def it_should_map_fields_correctly(sections_df):
        row_dict = sections_df.to_dict(orient="records")[0]
        assert row_dict["SourceSystemIdentifier"] == ID
        assert row_dict["LMSSectionStatus"] == ""
        assert row_dict["SectionDescription"] == ""
        assert row_dict["Title"] == NAME
        assert row_dict["SourceCreateDate"] == ""
        assert row_dict["SourceLastModifiedDate"] == ""
        assert row_dict["SourceSystem"] == SOURCE_SYSTEM
        assert row_dict["SISSectionIdentifier"] == SIS_SECTION_ID
        assert row_dict["Term"] == ""
        assert row_dict["CreateDate"] == CREATE_DATE
        assert row_dict["LastModifiedDate"] == LAST_MODIFIED_DATE
