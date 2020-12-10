# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License,  Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest

from schoology_extractor.mapping.section_associations import map_to_udm


def describe_when_mapping_Schoology_DataFrame_to_EdFi_DataFrame():
    def describe_given_input_is_empty():
        def it_should_return_empty_DataFrame():
            input = pd.DataFrame()

            result = map_to_udm(input, 1)

            assert result.empty

    def describe_given_input_contains_data():
        # Note: The `EnrollmentStatus` column is tested in another test fixture

        @pytest.fixture
        def result() -> pd.DataFrame:

            section_associations = [
                {
                    "id": 43333,
                    "uid": 39303,
                    "status": 1,
                    "admin": 1,
                    "CreateDate": "a",
                    "LastModifiedDate": "b",
                },
                {
                    "id": 123355,
                    "uid": 588525,
                    "status": 1,
                    "admin": 0,
                    "CreateDate": "c",
                    "LastModifiedDate": "d",
                },
            ]

            # Arrange
            schoology_df = pd.DataFrame(section_associations)

            # Act
            return map_to_udm(schoology_df, 234234)

        def it_should_ignore_admin_users(result):
            assert result.shape[0] == 1

        def it_should_have_schoology_as_source_system(result):
            assert result["SourceSystem"].iloc[0] == "Schoology"

        def it_should_map_id_to_source_system_identifier(result):
            assert result["SourceSystemIdentifier"].iloc[0] == 123355

        def it_should_have_active_as_entity_status(result):
            assert result["EntityStatus"].iloc[0] == "active"

        def it_should_map_id_to_user_source_system_identifier(result):
            assert result["LMSUserSourceSystemIdentifier"].iloc[0] == 588525

        def it_should_map_input_section_id_to_lms_section_source_system_identifier(result):
            assert result["LMSSectionSourceSystemIdentifier"].iloc[0] == 234234

        def it_should_have_preserve_received_create_date(result):
            assert result["CreateDate"].iloc[0] == "c"

        def it_should_preserve_received_last_modified_date(result):
            assert result["LastModifiedDate"].iloc[0] == "d"

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
        section_association = {
            "id": 123355,
            "uid": 588525,
            "status": status_code,
            "admin": 0,
            "CreateDate": "a",
            "LastModifiedDate": "b"
        }

        # Arrange
        schoology_df = pd.DataFrame([section_association])

        # Act
        result = map_to_udm(schoology_df, 234234)

        # Assert
        assert result["EnrollmentStatus"].iloc[0] == status_string
