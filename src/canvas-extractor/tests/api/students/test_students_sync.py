# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import pytest
from pandas import read_sql_query, DataFrame
from edfi_canvas_extractor.api.students import _sync_without_cleanup
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
    "name",
    "created_at",
    "sortable_name",
    "short_name",
    "sis_user_id",
    "integration_id",
    "sis_import_id",
    "email",
    "login_id",
]

CHANGED_STUDENT_BEFORE = [
    "1",
    "Changed Student Before",
    "11",
    "111",
    "1111",
    "2020-11-01",
    "11111",
    "111111",
    "1111111",
    "2020-11-01",
]

CHANGED_STUDENT_AFTER = [
    "1",
    "*Changed Student After*",
    "11",
    "111",
    "1111",
    "2020-11-01",
    "11111",
    "111111",
    "1111111",
    "2020-11-01",
]

UNCHANGED_STUDENT = [
    "2",
    "Unchanged Student",
    "22",
    "222",
    "2222",
    "2020-01-02",
    "22222",
    "222222",
    "2222222",
    "2020-02-02",
]

OMITTED_FROM_SYNC_STUDENT = [
    "3",
    "Omitted From Sync Student",
    "33",
    "333",
    "3333",
    "2020-01-03",
    "33333",
    "333333",
    "3333333",
    "2020-03-03",
]

NEW_STUDENT = [
    "4",
    "New Student",
    "44",
    "444",
    "4444",
    "2020-01-04",
    "44444",
    "444444",
    "4444444",
    "2020-04-04",
]

SYNC_DATA = [CHANGED_STUDENT_AFTER, UNCHANGED_STUDENT, NEW_STUDENT]


def describe_when_testing_sync_with_new_and_missing_and_updated_rows():
    @pytest.fixture
    def test_db_after_sync(test_db_fixture):
        # arrange
        INITIAL_STUDENT_DATA = [
            CHANGED_STUDENT_BEFORE,
            UNCHANGED_STUDENT,
            OMITTED_FROM_SYNC_STUDENT,
        ]

        students_initial_df = DataFrame(INITIAL_STUDENT_DATA, columns=COLUMNS)
        students_initial_df = add_hash_and_json_to(students_initial_df)
        add_sourceid_to(students_initial_df, IDENTITY_COLUMNS)

        dateToUse = datetime(2020, 9, 14, 12, 0, 0)
        students_initial_df["SyncNeeded"] = 0
        students_initial_df["CreateDate"] = dateToUse
        students_initial_df["LastModifiedDate"] = dateToUse
        students_initial_df = students_initial_df[SYNC_COLUMNS]

        students_sync_df = DataFrame(SYNC_DATA, columns=COLUMNS)

        with test_db_fixture.connect() as con:
            con.execute("DROP TABLE IF EXISTS Students")
            con.execute(
                f"""
                CREATE TABLE IF NOT EXISTS Students (
                    {SYNC_COLUMNS_SQL}
                )
                """
            )

        students_initial_df.to_sql(
            "Students", test_db_fixture, if_exists="append", index=False, chunksize=1000
        )

        # act
        _sync_without_cleanup(students_sync_df, test_db_fixture)

        return test_db_fixture

    def it_should_have_students_table_with_updated_row_and_added_new_row(
        test_db_after_sync,
    ):
        EXPECTED_STUDENT_DATA_AFTER_SYNC = [
            UNCHANGED_STUDENT,
            OMITTED_FROM_SYNC_STUDENT,
            CHANGED_STUDENT_AFTER,
            NEW_STUDENT,
        ]
        with test_db_after_sync.connect() as con:
            expected_students_df = prep_expected_sync_df(
                DataFrame(EXPECTED_STUDENT_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            students_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Students", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_students_df.to_csv() == students_from_db_df.to_csv()

    def it_should_have_temporary_sync_table_unchanged(test_db_after_sync):
        EXPECTED_SYNC_DATA_AFTER_SYNC = SYNC_DATA
        with test_db_after_sync.connect() as con:
            expected_sync_students_df = prep_expected_sync_df(
                DataFrame(EXPECTED_SYNC_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            sync_students_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Sync_Students", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_sync_students_df.to_csv() == sync_students_from_db_df.to_csv()

    def it_should_have_temporary_unmatched_table_with_correct_intermediate_rows(
        test_db_after_sync,
    ):
        EXPECTED_UNMATCHED_DATA_AFTER_SYNC = [
            CHANGED_STUDENT_AFTER,
            CHANGED_STUDENT_BEFORE,
            OMITTED_FROM_SYNC_STUDENT,
            NEW_STUDENT,
        ]
        with test_db_after_sync.connect() as con:
            expected_unmatched_df = prep_expected_sync_df(
                DataFrame(EXPECTED_UNMATCHED_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            unmatched_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Unmatched_Students", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_unmatched_df.to_csv() == unmatched_from_db_df.to_csv()
