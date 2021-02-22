# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import pytest
from pandas import read_sql_query, DataFrame
from edfi_canvas_extractor.api.sections import _sync_without_cleanup
from edfi_lms_extractor_lib.api.resource_sync import (
    SYNC_COLUMNS_SQL,
    SYNC_COLUMNS,
    add_hash_and_json_to,
    add_sourceid_to,
)
from tests.api.api_helper import prep_expected_sync_df, prep_from_sync_db_df

IDENTITY_COLUMNS = ["id"]

COLUMNS = [
    "id",
    "course_id",
    "name",
    "start_at",
    "end_at",
    "created_at",
    "created_at_date",
    "restrict_enrollments_to_section_dates",
    "nonxlist_course_id",
    "sis_section_id",
    "sis_course_id",
    "integration_id",
    "sis_import_id",
]

CHANGED_SECTION_BEFORE = [
    "1",
    "Changed Section Before",
    "11",
    "111",
    "1111",
    "2020-11-01",
    "11111",
    "111111",
    "1111111",
    "2020-11-01",
    "11111111",
    "111111111",
    "1111111111",
]

CHANGED_SECTION_AFTER = [
    "1",
    "*Changed Section After*",
    "11",
    "111",
    "1111",
    "2020-11-01",
    "11111",
    "111111",
    "1111111",
    "2020-11-01",
    "11111111",
    "111111111",
    "1111111111",
]

UNCHANGED_SECTION = [
    "2",
    "Unchanged Section",
    "22",
    "222",
    "2222",
    "2020-01-02",
    "22222",
    "222222",
    "2222222",
    "2020-02-02",
    "22222222",
    "222222222",
    "2222222222",
]

OMITTED_FROM_SYNC_SECTION = [
    "3",
    "Omitted From Sync Section",
    "33",
    "333",
    "3333",
    "2020-01-03",
    "33333",
    "333333",
    "3333333",
    "2020-03-03",
    "33333333",
    "333333333",
    "3333333333",
]

NEW_SECTION = [
    "4",
    "New Section",
    "44",
    "444",
    "4444",
    "2020-01-04",
    "44444",
    "444444",
    "4444444",
    "2020-04-04",
    "44444444",
    "444444444",
    "4444444444",
]

SYNC_DATA = [CHANGED_SECTION_AFTER, UNCHANGED_SECTION, NEW_SECTION]


def describe_when_testing_sync_with_new_and_missing_and_updated_rows():
    @pytest.fixture
    def test_db_after_sync(test_db_fixture):
        # arrange
        INITIAL_SECTION_DATA = [
            CHANGED_SECTION_BEFORE,
            UNCHANGED_SECTION,
            OMITTED_FROM_SYNC_SECTION,
        ]

        sections_initial_df = DataFrame(INITIAL_SECTION_DATA, columns=COLUMNS)
        sections_initial_df = add_hash_and_json_to(sections_initial_df)
        add_sourceid_to(sections_initial_df, IDENTITY_COLUMNS)

        dateToUse = datetime(2020, 9, 14, 12, 0, 0)
        sections_initial_df["SyncNeeded"] = 0
        sections_initial_df["CreateDate"] = dateToUse
        sections_initial_df["LastModifiedDate"] = dateToUse
        sections_initial_df = sections_initial_df[SYNC_COLUMNS]

        sections_sync_df = DataFrame(SYNC_DATA, columns=COLUMNS)

        with test_db_fixture.connect() as con:
            con.execute("DROP TABLE IF EXISTS Sections")
            con.execute(
                f"""
                CREATE TABLE IF NOT EXISTS Sections (
                    {SYNC_COLUMNS_SQL}
                )
                """
            )

        sections_initial_df.to_sql(
            "Sections", test_db_fixture, if_exists="append", index=False, chunksize=1000
        )

        # act
        _sync_without_cleanup(sections_sync_df, test_db_fixture)

        return test_db_fixture

    def it_should_have_sections_table_with_updated_row_and_added_new_row(
        test_db_after_sync,
    ):
        EXPECTED_SECTION_DATA_AFTER_SYNC = [
            UNCHANGED_SECTION,
            OMITTED_FROM_SYNC_SECTION,
            CHANGED_SECTION_AFTER,
            NEW_SECTION,
        ]
        with test_db_after_sync.connect() as con:
            expected_sections_df = prep_expected_sync_df(
                DataFrame(EXPECTED_SECTION_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            sections_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Sections", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_sections_df.to_csv() == sections_from_db_df.to_csv()

    def it_should_have_temporary_sync_table_unchanged(test_db_after_sync):
        EXPECTED_SYNC_DATA_AFTER_SYNC = SYNC_DATA
        with test_db_after_sync.connect() as con:
            expected_sync_sections_df = prep_expected_sync_df(
                DataFrame(EXPECTED_SYNC_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            sync_sections_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Sync_Sections", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert (
                expected_sync_sections_df.to_csv() == sync_sections_from_db_df.to_csv()
            )

    def it_should_have_temporary_unmatched_table_with_correct_intermediate_rows(
        test_db_after_sync,
    ):
        EXPECTED_UNMATCHED_DATA_AFTER_SYNC = [
            CHANGED_SECTION_AFTER,
            CHANGED_SECTION_BEFORE,
            OMITTED_FROM_SYNC_SECTION,
            NEW_SECTION,
        ]
        with test_db_after_sync.connect() as con:
            expected_unmatched_df = prep_expected_sync_df(
                DataFrame(EXPECTED_UNMATCHED_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            unmatched_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Unmatched_Sections", con).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            assert expected_unmatched_df.to_csv() == unmatched_from_db_df.to_csv()
