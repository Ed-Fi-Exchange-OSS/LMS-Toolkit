# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime

import pandas as pd
import pytest

from edfi_schoology_extractor.mapping.section_updates import map_to_udm

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
            responses_csv = """id,body,uid,created,last_updated,likes,user_like_action,realm,section_id,num_comments,LastModifiedDate,CreateDate
3278973032,Mary Archer can post an update here.,100032890,1604351963,1604351963,1,false,section,2942191527,2,,"""
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
                "LMSUserSourceSystemIdentifier",
                "LMSSectionSourceSystemIdentifier",
            ],
        )
        def then_output_has_column(result, input):
            assert input in result.columns

        def then_source_system_identifier_is_mapped(result):
            assert result.at[0, "SourceSystemIdentifier"] == "su#3278973032"

        def then_source_system_is_mapped(result):
            assert result.at[0, "SourceSystem"] == "Schoology"

        def test_then_user_identifier_is_mapped(result):
            assert result.at[0, "LMSUserSourceSystemIdentifier"] == "100032890"

        def test_then_section_identifier_is_mapped(result):
            assert result.at[0, "LMSSectionSourceSystemIdentifier"] == FAKE_SECTION_ID

        def test_then_activity_date_time_is_mapped(result):
            # This is a timezone-safe test
            expected = datetime.fromtimestamp(1604351963)
            actual = datetime.fromisoformat(result.at[0, "ActivityDateTime"])
            assert actual == expected

        def test_then_activity_type_is_mapped(result):
            assert result.at[0, "ActivityType"] == "section-update"

        def test_then_it_should_have_empty_SourceCreateDate(result):
            assert result.at[0, "SourceCreateDate"] == ""

        def test_then_it_should_have_empty_SourceLastModifiedDate(result):
            assert result.at[0, "SourceLastModifiedDate"] == ""
