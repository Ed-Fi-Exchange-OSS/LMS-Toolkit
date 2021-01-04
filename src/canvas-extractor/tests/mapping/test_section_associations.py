# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License,  Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest

from canvas_extractor.mapping.section_associations import map_to_udm_section_associations


def describe_when_mapping_Schoology_DataFrame_to_EdFi_DataFrame():
    def describe_given_input_is_empty():
        def it_should_return_empty_DataFrame():
            input = pd.DataFrame()

            result = map_to_udm_section_associations(input)

            assert result.empty

    def describe_given_input_contains_data():
        # Note: The `EnrollmentStatus` column is tested in another test fixture

        @pytest.fixture
        def result() -> pd.DataFrame:

            section_asociations_csv = """id,user_id,course_id,type,created_at,created_at_date,updated_at,updated_at_date,associated_user_id,start_at,end_at,course_section_id,root_account_id,limit_privileges_to_course_section,enrollment_state,role,role_id,last_activity_at,last_attended_at,total_activity_time,sis_import_id,grades,sis_account_id,sis_course_id,course_integration_id,sis_section_id,section_integration_id,sis_user_id,html_url,user,last_activity_at_date,CreateDate,LastModifiedDate
4,5,2,StudentEnrollment,2020-08-31T16:59:00Z,2020-08-31 16:59:00+00:00,2020-09-02T21:47:09Z,2020-09-02 21:47:09+00:00,,,,2,1,False,active,StudentEnrollment,3,,,0,,grade,,,,,,,https://edfialliance.instructure.com/courses/2/users/5,user,,22:07.3,22:07.3
106,113,104,StudentEnrollment,2020-09-14T17:06:21Z,2020-09-14 17:06:21+00:00,2020-09-14T17:18:34Z,2020-09-14 17:18:34+00:00,,,,103,1,False,active,StudentEnrollment,3,2020-09-14T17:37:57Z,,0,,grade,,ENG-1,,,,604863,https://edfialliance.instructure.com/courses/104/users/113,user,2020-09-14 17:37:57+00:00,22:07.3,22:07.3"""

            lines = section_asociations_csv.split("\n")
            section_associations = pd.DataFrame(
                [x.split(",") for x in lines[1:]], columns=lines[0].split(",")
            )

            # Arrange
            df = pd.DataFrame(section_associations)

            # Act
            return map_to_udm_section_associations(df)

        def it_should_have_correct_number_of_columns(result):
            assert result.shape[1] == 12

        def it_should_have_canvas_as_source_system(result):
            assert result["SourceSystem"].iloc[0] == "Canvas"

        def it_should_map_id_to_source_system_identifier(result):
            assert result["SourceSystemIdentifier"].iloc[0] == "4"

        def it_should_have_active_as_entity_status(result):
            assert result["EntityStatus"].iloc[0] == "active"

        def it_should_map_id_to_user_source_system_identifier(result):
            assert result["LMSUserSourceSystemIdentifier"].iloc[0] == "5"

        def it_should_map_input_section_id_to_lms_section_source_system_identifier(result):
            assert result["LMSSectionSourceSystemIdentifier"].iloc[0] == "2"

        def it_should_have_empty_start_date(result):
            assert result["StartDate"].iloc[0] == ""

        def it_should_have_empty_end_date(result):
            assert result["EndDate"].iloc[0] == ""
