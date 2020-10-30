# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


import pandas as pd
import pytest

from schoology_extractor.mapping.sections import map_to_udm


class Test_mapping_schoology_sections_to_udm:
    @classmethod
    def setup_class(cls):

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
        cls.result = map_to_udm(sections_df)

    # Each assertion is a separate method
    def test_then_output_has_two_rows(self):
        assert self.result.shape[0] == 2

    def test_then_output_has_ten_columns(self):
        assert self.result.shape[1] == 9

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
    def test_then_output_has_column(self, input):
        assert input in self.result.columns

    def test_then_source_system_identifier_is_mapped(self):
        assert self.result.at[0, "SourceSystemIdentifier"] == "2975852079"

    def test_then_source_system_is_mapped(self):
        assert self.result.at[0, "SourceSystem"] == "Schoology"

    def test_then_title_is_mapped(self):
        assert self.result.at[0, "Title"] == "Section 2"

    def test_then_section_description_is_mapped(self):
        assert (
            self.result.at[0, "SectionDescription"] == "This is the section description"
        )

    def test_then_term_is_mapped(self):
        # Schoology doesn't have a concept that we can translate into a term
        assert self.result.at[0, "Term"] is None

    def test_then_lms_section_status_is_mapped_active(self):
        assert self.result.at[0, "LMSSectionStatus"] == "active"

    def test_then_lms_section_status_is_mapped_inactive(self):
        # Note this is the second record
        assert self.result.at[1, "LMSSectionStatus"] == "inactive"

    def test_then_entity_status_is_mapped_inactive(self):
        assert self.result.at[0, "EntityStatus"] == "active"

    # TODO: FIZZ-125
    def test_then_create_date_is_mapped(self):
        assert self.result.at[0, "CreateDate"] == "2020-10-30 11:40:50"

    # TODO: FIZZ-125
    def test_then_last_modified_date_is_mapped(self):
        assert self.result.at[0, "LastModifiedDate"] == "2020-10-30 11:40:50"
