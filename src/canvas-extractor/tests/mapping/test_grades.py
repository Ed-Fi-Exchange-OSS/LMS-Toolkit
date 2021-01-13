# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License,  Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest

from canvas_extractor.mapping.grades import map_to_udm_grades


def describe_when_mapping_Schoology_DataFrame_to_EdFi_DataFrame():
    def describe_given_input_is_empty():
        def it_should_return_empty_DataFrame():
            input = pd.DataFrame()

            result = map_to_udm_grades(input)

            assert result.empty

    def describe_given_input_contains_data():

        @pytest.fixture
        def result() -> pd.DataFrame:

            grades_csv = """html_url,current_grade,current_score,final_grade,final_score,unposted_current_score,unposted_current_grade,unposted_final_score,unposted_final_grade,SourceSystemIdentifier,LMSUserIdentifier,LMSSectionIdentifier,LMSGradeIdentifier,CreateDate,LastModifiedDate
https://edfialliance.instructure.com/courses/103/grades/113,,89.5,,89.5,89.5,,89.5,,g#111,113,104,g#111,2021-01-12 15:29:34.999238,2021-01-12 16:13:40.212388"""

            lines = grades_csv.split("\n")
            grades = pd.DataFrame(
                [x.split(",") for x in lines[1:]], columns=lines[0].split(",")
            )

            # Arrange
            df = pd.DataFrame(grades)

            # Act
            return map_to_udm_grades(df)

        def it_should_have_correct_number_of_columns(result):
            assert result.shape[1] == 11

        def it_should_have_canvas_as_source_system(result):
            assert result["SourceSystem"].iloc[0] == "Canvas"

        def it_should_map_id_to_source_system_identifier(result):
            assert result["SourceSystemIdentifier"].iloc[0] == "g#111"

        def it_should_map_id_to_user_source_system_identifier(result):
            assert result["LMSUserIdentifier"].iloc[0] == "113"

        def it_should_map_input_section_id_to_lms_section_identifier(result):
            assert result["LMSSectionIdentifier"].iloc[0] == "104"

        def it_should_have_grade_identifier(result):
            assert result["LMSGradeIdentifier"].iloc[0] == "g#111"

        def it_should_have_grade(result):
            assert result["Grade"].iloc[0] == "89.5"

        def it_should_have_CreateDate(result):
            assert result["CreateDate"].iloc[0] == "2021-01-12 15:29:34.999238"

        def it_should_have_LastModifiedDate(result):
            assert result["LastModifiedDate"].iloc[0] == "2021-01-12 16:13:40.212388"

        def it_should_have_GradeType(result):
            assert result["GradeType"].iloc[0] == "Final"

        def it_should_have_SourceCreateDate(result):
            assert result["SourceCreateDate"].iloc[0] == ""

        def it_should_have_SourceLastModifiedDate(result):
            assert result["SourceLastModifiedDate"].iloc[0] == ""
