# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


import pandas as pd
import pytest

from schoology_extractor.mapping.users import map_to_udm


def describe_when_mapping_schoology_users_to_udm():
    def describe_given_there_are_no_users():
        def it_should_return_an_empty_DataFrame():
            assert map_to_udm(pd.DataFrame(), pd.DataFrame()).empty

    # Note: Schoology has no published controls around roles. Even if there were
    # a way to remove all roles, a User without a Role could not exist.
    # Therefore it is sufficient to test only for empty Users.

    def describe_given_input_has_data():
        @pytest.fixture
        def result():
            # Arrange
            users_csv = """uid,id,school_id,synced,school_uid,name_title,name_title_show,name_first,name_first_preferred,use_preferred_first_name,name_middle,name_middle_show,name_last,name_display,username,primary_email,picture_url,gender,position,grad_year,password,role_id,tz_offset,tz_name,parents,child_uids,language,additional_buildings,CreateDate,LastModifiedDate
100032890,100032890,2908525646,0,604863,,0,Mary,,1,Catherine,0,Archer,Mary Archer Display Name,mary.archer,mary.archer@studentgps.org,https://asset-cdn.schoology.com/system/files/imagecache/profile_reg/sites/all/themes/schoology_theme/images/user-default.gif,,,,,123456,-5,America/Chicago,,,,,2020-10-23 16:31:28,2020-10-23 16:31:28
99785799,99785799,2908525646,0,222222,,0,Brad,,1,,0,Banister,Brad Banister,brad.banister,brad@doublelinepartners.com,https://asset-cdn.schoology.com/system/files/imagecache/profile_reg/sites/all/themes/schoology_theme/images/user-default.gif,,,,,123457,-5,America/Chicago,,,,,2020-10-23 16:31:28,2020-10-23 16:31:28"""

            lines = users_csv.split("\n")
            users_df = pd.DataFrame(
                [x.split(",") for x in lines[1:]], columns=lines[0].split(",")
            )

            roles_csv = """id,title,faculty,role_type
123456,student,0,1
123457,teacher,0,1"""
            lines = roles_csv.split("\n")
            roles_df = pd.DataFrame(
                [x.split(",") for x in lines[1:]], columns=lines[0].split(",")
            )

            # Act
            return map_to_udm(users_df, roles_df)

        # Each assertion is a separate method
        def test_then_output_has_two_rows(result):
            assert result.shape[0] == 2

        def test_then_output_has_ten_columns(result):
            assert result.shape[1] == 10

        @pytest.mark.parametrize(
            "input",
            [
                "SourceSystemIdentifier",
                "SourceSystem",
                "UserRole",
                "LocalUserIdentifier",
                "SISUserIdentifier",
                "Name",
                "EmailAddress",
                "EntityStatus",
                "CreateDate",
                "LastModifiedDate",
            ],
        )
        def test_then_output_has_column(result, input):
            assert input in result.columns

        def test_then_source_system_identifier_is_mapped(result):
            assert result.at[0, "SourceSystemIdentifier"] == "100032890"

        def test_then_source_system_is_mapped(result):
            assert result.at[0, "SourceSystem"] == "Schoology"

        def test_then_user_role_is_mapped(result):
            assert result.at[0, "UserRole"] == "student"

        def test_then_local_user_identifier_is_mapped(result):
            assert result.at[0, "LocalUserIdentifier"] == "mary.archer"

        def test_then_sis_user_identifier_is_not_set(result):
            assert result.at[0, "SISUserIdentifier"] == "604863"

        def test_then_name_is_mapped(result):
            assert result.at[0, "Name"] == "Mary Catherine Archer"

        def test_name_does_not_have_two_spaces_when_middle_name_is_missing(result):
            assert result.at[1, "Name"] == "Brad Banister"

        def test_then_email_address_is_mapped(result):
            assert result.at[0, "EmailAddress"] == "mary.archer@studentgps.org"

        def test_then_entity_status_is_mapped_inactive(result):
            assert result.at[0, "EntityStatus"] == "active"
