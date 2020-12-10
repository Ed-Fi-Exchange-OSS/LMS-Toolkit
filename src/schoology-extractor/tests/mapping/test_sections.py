# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


import pandas as pd
import pytest

from schoology_extractor.mapping.sections import map_to_udm


def describe_when_mapping_schoology_sections_to_udm():
    def describe_given_input_has_no_data():
        def it_should_return_an_empty_DataFrame():
            assert map_to_udm(pd.DataFrame()).empty

    def describe_given_input_has_data():
        @pytest.fixture
        def result():

            # Arrange
            sections_csv = """id,course_title,course_code,course_id,school_id,section_title,section_code,section_school_code,active,description,grading_periods,CreateDate,LastModifiedDate
2975852079,Algebra I,ALG-1,2942191514,2908525646,Section 2,ALG-1-2,123456,1,This is the section description,[825792],2020-10-30 11:40:50,2020-10-30 11:40:50
2942191527,Algebra I,ALG-1,2942191514,2908525646,Algebra I,ALG-1-1,,0,,[822639],2020-10-30 11:40:50,2020-10-30 11:40:50"""

            lines = sections_csv.split("\n")
            sections_df = pd.DataFrame(
                [x.split(",") for x in lines[1:]], columns=lines[0].split(",")
            )
            sections_df["active"] = sections_df["active"].apply(int)

            # Act
            return map_to_udm(sections_df)

        # Each assertion is a separate method
        def then_output_has_two_rows(result):
            assert result.shape[0] == 2

        def then_it_should_have_correct_number_of_columns(result):
            assert result.shape[1] == 11

        @pytest.mark.parametrize(
            "input",
            [
                "SourceSystemIdentifier",
                "SourceSystem",
                "Title",
                "SectionDescription",
                "Term",
                "LMSSectionStatus",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
            ],
        )
        def then_output_has_column(result, input):
            assert input in result.columns

        def then_source_system_identifier_is_mapped(result):
            assert result.at[0, "SourceSystemIdentifier"] == "2975852079"

        def then_source_system_is_mapped(result):
            assert result.at[0, "SourceSystem"] == "Schoology"

        def then_title_is_mapped(result):
            assert result.at[0, "Title"] == "Section 2"

        def then_section_description_is_mapped(result):
            assert (
                result.at[0, "SectionDescription"] == "This is the section description"
            )

        def then_term_is_mapped(result):
            # Schoology doesn't have a concept that we can translate into a term
            assert result.at[0, "Term"] is None

        def then_lms_section_status_is_mapped_active(result):
            assert result.at[0, "LMSSectionStatus"] == "active"

        def then_lms_section_status_is_mapped_inactive(result):
            # Note this is the second record
            assert result.at[1, "LMSSectionStatus"] == "inactive"

        def then_entity_status_is_mapped_inactive(result):
            assert result.at[0, "EntityStatus"] == "active"

        def then_create_date_is_mapped(result):
            assert result.at[0, "CreateDate"] == "2020-10-30 11:40:50"

        def then_last_modified_date_is_mapped(result):
            assert result.at[0, "LastModifiedDate"] == "2020-10-30 11:40:50"

        def then_it_should_have_empty_SourceCreateDate(result):
            assert result.at[0, "SourceCreateDate"] == ""

        def then_it_should_have_empty_SourceLastModifiedDate(result):
            assert result.at[0, "SourceLastModifiedDate"] == ""
