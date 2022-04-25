# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


from typing import List
import pandas as pd
import pytest

from edfi_canvas_extractor.mapping.users import map_to_udm_users


def describe_when_mapping_schoology_users_to_udm():
    def describe_given_there_are_no_users():
        def it_should_return_an_empty_DataFrame():
            assert map_to_udm_users(pd.DataFrame()).empty

    def describe_given_input_has_data():
        @pytest.fixture
        def result():
            # Arrange
            users_csv = """id,name,created_at,sortable_name,short_name,sis_user_id,integration_id,sis_import_id,email,login_id,CreateDate,LastModifiedDate
114,Kyle Hughes,  2020-09-14T11:54:01-05:00,"Hughes Kyle",Kyle Hughes,604874,874,,Kyle.Hughes@studentgps.org,Kyle.Hughes@studentgps.org,45:38.5,45:38.5
116,Larry Mahoney,2021-03-10T14:19:17-06:00,"Mahoney Larry",Larry Mahoney,604927,927,,Larry.Mahoney@studentgps.org,Larry.Mahoney@studentgps.org,45:38.5,45:38.5"""

            lines = users_csv.split("\n")
            users_df = pd.DataFrame(
                [x.split(",") for x in lines[1:]], columns=lines[0].split(",")
            )

            # Act
            return map_to_udm_users(users_df)

        def test_then_output_has_two_rows(result):
            assert result.shape[0] == 2

        def test_then_it_should_have_correct_number_of_columns(result):
            assert result.shape[1] == 11

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
                "CreateDate",
                "LastModifiedDate",
            ],
        )
        def test_then_output_has_column(result, input):
            assert input in result.columns

        def test_then_source_system_identifier_is_mapped(result):
            assert result.at[0, "SourceSystemIdentifier"] == "114"

        def test_then_source_system_is_mapped(result):
            assert result.at[0, "SourceSystem"] == "Canvas"

        def test_then_user_role_is_mapped(result):
            assert result.at[0, "UserRole"] == "Student"

        def test_then_local_user_identifier_is_mapped(result):
            assert result.at[0, "LocalUserIdentifier"] == "Kyle.Hughes@studentgps.org"

        def test_then_sis_user_identifier_is_not_set(result):
            assert result.at[0, "SISUserIdentifier"] == "604874"

        def test_then_name_is_mapped(result):
            assert result.at[0, "Name"] == "Kyle Hughes"

        def test_then_email_address_is_mapped(result):
            assert result.at[0, "EmailAddress"] == "Kyle.Hughes@studentgps.org"

        def test_then_it_should_have_SourceCreateDate(result):
            assert result.at[0, "SourceCreateDate"] == "2020-09-14 16:54:01"

        def test_then_it_should_have_empty_SourceLastModifiedDate(result):
            assert result.at[0, "SourceLastModifiedDate"] == ""

        def then_output_to_csv_has_blanks_not_NaT_for_SourceLastModifiedDate(
            result: pd.DataFrame, fs
        ) -> None:

            # Fake as Linux so that all slashes in these test are forward
            fs.os = "linux"
            fs.path_separator = "/"
            fs.is_windows_fs = False
            fs.is_macos = False

            # Convert to CSV
            FILE = "/file.csv"
            result.to_csv(FILE, index=False)

            # Open as plain text and do some simple parsing to get the
            # SourceLastModifiedDate.
            lines: List[str] = []
            with open(FILE) as f:
                lines = f.readlines()

            lines = [line.replace("\n", "") for line in lines]

            # Find where "SourceLastModifiedDate" ended up
            column_names = lines[0].split(",")
            assert "SourceLastModifiedDate" in column_names, lines[0]
            position = column_names.index("SourceLastModifiedDate")

            def __look_for_nat(line: str, line_number: int) -> None:
                cells = line[line_number].split(",")
                assert cells[position] == "", line_number

            __look_for_nat(lines, 1)
            __look_for_nat(lines, 2)
