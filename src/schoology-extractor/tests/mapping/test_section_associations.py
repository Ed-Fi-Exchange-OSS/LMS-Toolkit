# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License,  Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest

from schoology_extractor.mapping.section_associations import map_to_udm

# TODO: it looks like "enrollments" includes the teacher. Confirm that and then
# make sure that teachers are filtered out.


def describe_when_mapping_Schoology_DataFrame_to_EdFi_DataFrame():
    # Note: The `EnrollmentStatus` column is tested in another test fixture

    @pytest.fixture
    def result() -> pd.DataFrame:

        section_association = {"id": 123355, "uid": 588525, "status": 1}

        # Arrange
        schoology_df = pd.DataFrame([section_association])

        # Act
        return map_to_udm(schoology_df, 234234)

    def it_should_have_schoology_as_source_system(result):
        assert result["SourceSystem"].iloc[0] == "Schoology"

    def it_should_map_id_to_source_system_identifier(result):
        assert result["SourceSystemIdentifier"].iloc[0] == 123355

    def it_should_have_active_as_entity_status(result):
        assert result["EntityStatus"].iloc[0] == "active"

    def it_should_map_id_to_user_source_system_identifier(result):
        assert result["UserSourceSystemIdentifier"].iloc[0] == 588525

    def it_should_map_input_section_id_to_lms_section_source_system_identifier(result):
        assert result["LMSSectionSourceSystemIdentifier"].iloc[0] == 234234

    # Can't add these next four until we have the sync process
    def it_should_have_empty_create_date(result):
        assert result["CreateDate"].iloc[0] is None

    def it_should_have_empty_last_modifie_date(result):
        assert result["LastModifiedDate"].iloc[0] is None

    def it_should_have_empty_start_date(result):
        assert result["StartDate"].iloc[0] is None

    def it_should_have_empty_end_date(result):
        assert result["EndDate"].iloc[0] is None


def describe_when_mapping_Schoology_enrollment_status_to_string_value():
    @pytest.mark.parametrize(
        "status_code,status_string",
        [
            (1, "Active"),
            (2, "Expired"),
            (3, "Invite pending"),
            (4, "Request pending"),
            (5, "Archived"),
        ],
    )
    def it_should_translate_status_code_to_string(status_code, status_string):
        section_association = {"id": 123355, "uid": 588525, "status": status_code}

        # Arrange
        schoology_df = pd.DataFrame([section_association])

        # Act
        result = map_to_udm(schoology_df, 234234)

        # Assert
        assert result["EnrollmentStatus"].iloc[0] == status_string
