# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import pytest
from pandas import read_sql_query, DataFrame
from canvas_extractor.api.enrollments import _sync_without_cleanup
from canvas_extractor.api.resource_sync import (
    SYNC_COLUMNS_SQL,
    SYNC_COLUMNS,
    add_hash_and_json_to,
    add_sourceid_to,
)
from tests.api.api_helper import prep_expected_sync_df, prep_from_sync_db_df

IDENTITY_COLUMNS = ["id"]

COLUMNS = [
    "id",
    "user_id",
    "course_id",
    "type",
    "created_at",
    "created_at_date",
    "updated_at",
    "updated_at_date",
    "associated_user_id",
    "start_at",
    "end_at",
    "course_section_id",
    "root_account_id",
    "limit_privileges_to_course_section",
    "enrollment_state",
    "role",
    "role_id",
    "last_activity_at",
    "last_attended_at",
    "total_activity_time",
    "sis_import_id",
    "grades",
    "sis_account_id",
    "sis_course_id",
    "course_integration_id",
    "sis_section_id",
    "section_integration_id",
    "sis_user_id",
    "html_url",
    "user",
    "last_activity_at_date",
]

CHANGED_ENROLLMENT_BEFORE = [
    "1",
    "Changed Enrollment Before",
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
    "11111111111",
    "111111111111",
    "1111111111111",
    "11111111111111",
    "111111111111111",
    "1111111111111111",
    "11111111111111111",
    "111111111111111111",
    "1111111111111111111",
    "11111111111111111111",
    "111111111111111111111",
    "1111111111111111111111",
    "11111111111111111111111",
    "111111111111111111111111",
    "1111111111111111111111111",
    "11111111111111111111111111",
    "111111111111111111111111111",
    "1111111111111111111111111111",
]

CHANGED_ENROLLMENT_AFTER = [
    "1",
    "*Changed Enrollment After*",
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
    "11111111111",
    "111111111111",
    "1111111111111",
    "11111111111111",
    "111111111111111",
    "1111111111111111",
    "11111111111111111",
    "111111111111111111",
    "1111111111111111111",
    "11111111111111111111",
    "111111111111111111111",
    "1111111111111111111111",
    "11111111111111111111111",
    "111111111111111111111111",
    "1111111111111111111111111",
    "11111111111111111111111111",
    "111111111111111111111111111",
    "1111111111111111111111111111",
]

UNCHANGED_ENROLLMENT = [
    "2",
    "Unchanged Enrollment",
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
    "22222222222",
    "222222222222",
    "2222222222222",
    "22222222222222",
    "222222222222222",
    "2222222222222222",
    "22222222222222222",
    "222222222222222222",
    "2222222222222222222",
    "22222222222222222222",
    "222222222222222222222",
    "2222222222222222222222",
    "22222222222222222222222",
    "222222222222222222222222",
    "2222222222222222222222222",
    "22222222222222222222222222",
    "222222222222222222222222222",
    "2222222222222222222222222222",
]

OMITTED_FROM_SYNC_ENROLLMENT = [
    "3",
    "Omitted From Sync Enrollment",
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
    "33333333333",
    "333333333333",
    "3333333333333",
    "33333333333333",
    "333333333333333",
    "3333333333333333",
    "33333333333333333",
    "333333333333333333",
    "3333333333333333333",
    "33333333333333333333",
    "333333333333333333333",
    "3333333333333333333333",
    "33333333333333333333333",
    "333333333333333333333333",
    "3333333333333333333333333",
    "33333333333333333333333333",
    "333333333333333333333333333",
    "3333333333333333333333333333",
]

NEW_ENROLLMENT = [
    "4",
    "New Enrollment",
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
    "44444444444",
    "444444444444",
    "4444444444444",
    "44444444444444",
    "444444444444444",
    "4444444444444444",
    "44444444444444444",
    "444444444444444444",
    "4444444444444444444",
    "44444444444444444444",
    "444444444444444444444",
    "4444444444444444444444",
    "44444444444444444444444",
    "444444444444444444444444",
    "4444444444444444444444444",
    "44444444444444444444444444",
    "444444444444444444444444444",
    "4444444444444444444444444444",
]

SYNC_DATA = [CHANGED_ENROLLMENT_AFTER, UNCHANGED_ENROLLMENT, NEW_ENROLLMENT]


def describe_when_testing_sync_with_new_and_missing_and_updated_rows():
    @pytest.fixture
    def test_db_after_sync(test_db_fixture):
        # arrange
        INITIAL_ENROLLMENT_DATA = [
            CHANGED_ENROLLMENT_BEFORE,
            UNCHANGED_ENROLLMENT,
            OMITTED_FROM_SYNC_ENROLLMENT,
        ]

        enrollments_initial_df = DataFrame(INITIAL_ENROLLMENT_DATA, columns=COLUMNS)
        enrollments_initial_df = add_hash_and_json_to(enrollments_initial_df)
        add_sourceid_to(enrollments_initial_df, IDENTITY_COLUMNS)

        dateToUse = datetime(2020, 9, 14, 12, 0, 0)
        enrollments_initial_df["SyncNeeded"] = 0
        enrollments_initial_df["CreateDate"] = dateToUse
        enrollments_initial_df["LastModifiedDate"] = dateToUse
        enrollments_initial_df = enrollments_initial_df[SYNC_COLUMNS]

        enrollments_sync_df = DataFrame(SYNC_DATA, columns=COLUMNS)

        with test_db_fixture.connect() as con:
            con.execute("DROP TABLE IF EXISTS Enrollments")
            con.execute(
                f"""
                CREATE TABLE IF NOT EXISTS Enrollments (
                    {SYNC_COLUMNS_SQL}
                )
                """
            )

        enrollments_initial_df.to_sql(
            "Enrollments", test_db_fixture, if_exists="append", index=False, chunksize=1000
        )

        # act
        _sync_without_cleanup(enrollments_sync_df, test_db_fixture)

        return test_db_fixture

    def it_should_have_enrollments_table_with_updated_row_and_added_new_row(
        test_db_after_sync,
    ):
        EXPECTED_ENROLLMENT_DATA_AFTER_SYNC = [
            UNCHANGED_ENROLLMENT,
            OMITTED_FROM_SYNC_ENROLLMENT,
            CHANGED_ENROLLMENT_AFTER,
            NEW_ENROLLMENT,
        ]
        with test_db_after_sync.connect() as con:
            expected_enrollments_df = prep_expected_sync_df(
                DataFrame(EXPECTED_ENROLLMENT_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            enrollments_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Enrollments", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_enrollments_df.to_csv() == enrollments_from_db_df.to_csv()

    def it_should_have_temporary_sync_table_unchanged(test_db_after_sync):
        EXPECTED_SYNC_DATA_AFTER_SYNC = SYNC_DATA
        with test_db_after_sync.connect() as con:
            expected_sync_enrollments_df = prep_expected_sync_df(
                DataFrame(EXPECTED_SYNC_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            sync_enrollments_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Sync_Enrollments", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_sync_enrollments_df.to_csv() == sync_enrollments_from_db_df.to_csv()

    def it_should_have_temporary_unmatched_table_with_correct_intermediate_rows(
        test_db_after_sync,
    ):
        EXPECTED_UNMATCHED_DATA_AFTER_SYNC = [
            CHANGED_ENROLLMENT_BEFORE,
            CHANGED_ENROLLMENT_AFTER,
            OMITTED_FROM_SYNC_ENROLLMENT,
            NEW_ENROLLMENT,
        ]
        with test_db_after_sync.connect() as con:
            expected_unmatched_df = prep_expected_sync_df(
                DataFrame(EXPECTED_UNMATCHED_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            unmatched_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Unmatched_Enrollments", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_unmatched_df.to_csv() == unmatched_from_db_df.to_csv()
