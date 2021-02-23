# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License,  Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest

from edfi_canvas_extractor.mapping.authentication_events import map_to_udm_system_activities


def describe_when_mapping_Schoology_DataFrame_to_EdFi_DataFrame():
    def describe_given_input_is_empty():
        def it_should_return_empty_DataFrame():
            input = pd.DataFrame()

            result = map_to_udm_system_activities(input)

            assert result.empty

    def describe_given_input_contains_data():

        @pytest.fixture
        def result() -> pd.DataFrame:

            csv = """id,created_at,created_at_date,event_type,links,CreateDate,LastModifiedDate
in#111#2021-01-20T21:12:16Z,2021-01-20T21:12:16Z,2021-01-20 21:12:16+00:00,login,"test",2021-01-25 09:24:05.978277,2021-01-25 09:24:05.978277"""

            lines = csv.split("\n")
            df = pd.DataFrame(
                [x.split(",") for x in lines[1:]], columns=lines[0].split(",")
            )

            # Arrange
            df = pd.DataFrame(df)

            # Act
            return map_to_udm_system_activities(df)

        def it_should_have_correct_number_of_columns(result):
            assert result.shape[1] == 12

        def it_should_have_canvas_as_source_system(result):
            assert result["SourceSystem"].iloc[0] == "Canvas"

        def it_should_map_id_to_source_system_identifier(result):
            assert result["SourceSystemIdentifier"].iloc[0] == "in#111#2021-01-20T21:12:16Z"

        def it_should_map_id_to_user_source_system_identifier(result):
            assert result["LMSUserSourceSystemIdentifier"].iloc[0] == "111"

        def it_should_have_CreateDate(result):
            assert result["CreateDate"].iloc[0] == "2021-01-25 09:24:05.978277"

        def it_should_have_LastModifiedDate(result):
            assert result["LastModifiedDate"].iloc[0] == "2021-01-25 09:24:05.978277"
