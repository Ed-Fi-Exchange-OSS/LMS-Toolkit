# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import pytest
from pandas import read_sql_query, DataFrame
from edfi_google_classroom_extractor.api.submissions import _sync_without_cleanup
from edfi_lms_extractor_lib.api.resource_sync import (
    SYNC_COLUMNS_SQL,
    SYNC_COLUMNS,
    add_hash_and_json_to,
    add_sourceid_to,
)
from tests.api.api_helper import prep_expected_sync_df, prep_from_sync_db_df

IDENTITY_COLUMNS = ["id", "courseId", "courseWorkId"]

COLUMNS = [
    "courseId",
    "courseWorkId",
    "id",
    "userId",
    "creationTime",
    "updateTime",
    "state",
    "alternateLink",
    "courseWorkType",
    "submissionHistory",
    "late",
    "draftGrade",
    "assignedGrade",
    "associatedWithDeveloper",
]

CHANGED_SUBMISSION_BEFORE = [
    "1",
    "11",
    "111",
    "1111",
    "2020-08-19T21:02:46.877Z",
    "2020-08-19T21:02:46.877Z",
    "a",
    "http://test.test.test",
    "b",
    "a",
    "0",
    "100",
    "100",
    "0",
]

CHANGED_SUBMISSION_AFTER = [
    "1",
    "11",
    "111",
    "1111",
    "2020-08-19T21:02:46.877Z",
    "2020-08-19T21:02:46.877Z",
    "a",
    "http://test.test.test",
    "b",
    "***UPDATED***",
    "0",
    "100",
    "100",
    "0",
]

UNCHANGED_SUBMISSION = [
    "2",
    "21",
    "211",
    "2111",
    "2020-08-19T21:02:46.877Z",
    "2020-08-19T21:02:46.877Z",
    "a",
    "http://test.test.test",
    "b",
    "a",
    "0",
    "100",
    "100",
    "0",
]

NEW_SUBMISSION = [
    "3",
    "31",
    "311",
    "3111",
    "2020-08-19T21:02:46.877Z",
    "2020-08-19T21:02:46.877Z",
    "a",
    "http://test.test.test",
    "b",
    "a",
    "0",
    "100",
    "100",
    "0",
]

SYNC_DATA = [CHANGED_SUBMISSION_AFTER, UNCHANGED_SUBMISSION, NEW_SUBMISSION]


def describe_when_testing_sync_with_new_and_missing_and_updated_rows():
    @pytest.fixture
    def test_db_after_sync(test_db_fixture):
        # arrange
        INITIAL_DATA = [
            CHANGED_SUBMISSION_BEFORE,
            UNCHANGED_SUBMISSION
        ]

        submissions_initial_df = DataFrame(INITIAL_DATA, columns=COLUMNS)
        submissions_initial_df = add_hash_and_json_to(submissions_initial_df)
        add_sourceid_to(submissions_initial_df, IDENTITY_COLUMNS)

        dateToUse = datetime(2020, 9, 14, 12, 0, 0)
        submissions_initial_df["SyncNeeded"] = 0
        submissions_initial_df["CreateDate"] = dateToUse
        submissions_initial_df["LastModifiedDate"] = dateToUse
        submissions_initial_df = submissions_initial_df[SYNC_COLUMNS]

        submissions_sync_df = DataFrame(SYNC_DATA, columns=COLUMNS)

        with test_db_fixture.connect() as con:
            con.execute("DROP TABLE IF EXISTS StudentSubmissions")
            con.execute(
                f"""
                CREATE TABLE IF NOT EXISTS StudentSubmissions (
                    {SYNC_COLUMNS_SQL}
                )
                """
            )

        submissions_initial_df.to_sql(
            "StudentSubmissions", test_db_fixture, if_exists="append", index=False, chunksize=1000
        )

        # act
        _sync_without_cleanup(submissions_sync_df, test_db_fixture)

        return test_db_fixture

    def it_should_have_submissions_table_with_updated_row_and_added_new_row(
        test_db_after_sync,
    ):
        EXPECTED_SUBMISSIONS_DATA_AFTER_SYNC = [
            UNCHANGED_SUBMISSION,
            CHANGED_SUBMISSION_AFTER,
            NEW_SUBMISSION,
        ]
        with test_db_after_sync.connect() as con:
            expected_submissions_df = prep_expected_sync_df(
                DataFrame(EXPECTED_SUBMISSIONS_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            submissions_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from StudentSubmissions", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_submissions_df.to_csv() == submissions_from_db_df.to_csv()
