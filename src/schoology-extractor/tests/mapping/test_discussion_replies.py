# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime

import pandas as pd
import pytest

from edfi_schoology_extractor.mapping.discussion_replies import map_to_udm

FAKE_SECTION_ID = 1
FAKE_DISCUSSION_ID = 12


def describe_mapping_schoology_users_to_udm():
    def describe_given_input_is_empty():
        def it_should_return_the_empty_DataFrame():
            input = pd.DataFrame()

            result = map_to_udm(input, FAKE_SECTION_ID, FAKE_DISCUSSION_ID)

            assert result.empty

    def describe_given_input_is_not_empty():
        @pytest.fixture
        def result() -> pd.DataFrame:

            # Arrange
            responses_csv = """id,uid,comment,created,parent_id,status,likes,user_like_action,links,CreateDate,LastModifiedDate
824849694,100032890,Mary Archer's response to ""First Algebra Discussion Topic."",1604351930,0,1,0,False,{'self': 'https://api.schoology.com/v1/sections/2942191527/discussions/3278946222/comments/824849694'},2020-11-12 10:39:27,2020-11-12 10:39:27
824853919,100032891,Kyle Hughes's reply to Mary Archer's response to ""First Algebra Discussion Topic."",1604352056,824849694,1,0,False,{'self': 'https://api.schoology.com/v1/sections/2942191527/discussions/3278946222/comments/824853919'},2020-11-12 10:39:27,2020-11-12 10:39:27"""
            lines = responses_csv.split("\n")
            responses_df = pd.DataFrame(
                [x.split(",") for x in lines[1:]], columns=lines[0].split(",")
            )

            # Act
            return map_to_udm(responses_df, FAKE_SECTION_ID, FAKE_DISCUSSION_ID)

        # Each assertion is a separate method
        def test_then_output_has_two_rows(result):
            assert result.shape[0] == 2

        def test_then_it_should_have_correct_number_of_columns(result):
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
        def test_then_output_has_column(result, input):
            assert input in result.columns

        def test_then_source_system_identifier_is_mapped(result):
            assert result.at[0, "SourceSystemIdentifier"] == "sdr#824849694"

        def test_then_source_system_is_mapped(result):
            assert result.at[0, "SourceSystem"] == "Schoology"

        def test_then_user_identifier_is_mapped(result):
            assert result.at[0, "LMSUserIdentifier"] == "100032890"

        def test_then_section_identifier_is_mapped(result):
            assert result.at[0, "LMSSectionIdentifier"] == FAKE_SECTION_ID

        def test_then_activity_date_time_is_mapped(result):
            # This is a timezone-safe test
            expected = datetime.fromtimestamp(1604351930)
            actual = datetime.fromisoformat(result.at[0, "ActivityDateTime"])
            assert actual == expected

        def test_then_activity_status_is_mapped(result):
            assert result.at[0, "ActivityStatus"] == "active"

        def test_then_activity_type_is_mapped(result):
            assert result.at[0, "ActivityType"] == "discussion-reply"

        def test_then_it_should_have_empty_SourceCreateDate(result):
            assert result.at[0, "SourceCreateDate"] == ""

        def test_then_it_should_have_empty_SourceLastModifiedDate(result):
            assert result.at[0, "SourceLastModifiedDate"] == ""
