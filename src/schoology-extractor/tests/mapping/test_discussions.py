# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


import pandas as pd
import pytest

from schoology_extractor.mapping.discussions import map_to_udm

FAKE_SECTION_ID = 1


def describe_mapping_schoology_discussions_to_udm():
    def describe_given_input_is_empty():
        def it_should_return_the_empty_DataFrame():
            input = pd.DataFrame()

            result = map_to_udm(input, FAKE_SECTION_ID)

            assert result.empty

    def describe_given_input_is_not_empty():
        @pytest.fixture
        def result():

            # Arrange
            responses_csv = """id,uid,title,body,weight,graded,require_initial_post,published,available,completed,display_weight,folder_id,due,comments_closed,completion_status,links/self,CreateDate,LastModifiedDate
3277613289,99785803,Test discussion,,10,0,,1,1,0,2,0,2021-01-26 23:59:00,0,,https://api.schoology.com/v1/sections/2941242697/discussions/3277613289,12/8/2020 7:58,12/8/2020 7:58"""
            lines = responses_csv.split("\n")
            responses_df = pd.DataFrame(
                [x.split(",") for x in lines[1:]], columns=lines[0].split(",")
            )

            # Act
            return map_to_udm(responses_df, FAKE_SECTION_ID)

        # Each assertion is a separate method
        def then_output_has_one_row(result: pd.DataFrame):
            assert result.shape[0] == 1

        def then_it_should_have_correct_number_of_columns(result):
            assert result.shape[1] == 13

        @pytest.mark.parametrize(
            "input",
            [
                "SourceSystemIdentifier",
                "SourceSystem",
                "ActivityType",
                "ActivityDateTime",
                "ActivityStatus",
                "ParentSourceSystemIdentifier",
                "ActivityTimeInMinutes",
                "LMSUserIdentifier",
                "LMSSectionIdentifier",
            ],
        )
        def then_output_has_column(result, input):
            assert input in result.columns

        def then_source_system_identifier_is_mapped(result):
            assert result.at[0, "SourceSystemIdentifier"] == "sd#3277613289"

        def then_source_system_is_mapped(result):
            assert result.at[0, "SourceSystem"] == "Schoology"

        def test_then_user_identifier_is_mapped(result):
            assert result.at[0, "LMSUserIdentifier"] == "99785803"

        def test_then_section_identifier_is_mapped(result):
            assert result.at[0, "LMSSectionIdentifier"] == FAKE_SECTION_ID

        def test_then_activity_date_time_is_mapped(result):
            assert result.at[0, "ActivityDateTime"] == "12/8/2020 7:58"

        def test_then_activity_type_is_mapped(result):
            assert result.at[0, "ActivityType"] == "Discussion"

        def test_then_it_should_have_empty_SourceCreateDate(result):
            assert result.at[0, "SourceCreateDate"] == ""

        def test_then_it_should_have_empty_SourceLastModifiedDate(result):
            assert result.at[0, "SourceLastModifiedDate"] == ""
