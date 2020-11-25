# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import pytest
import xxhash
from pandas import read_sql_query, DataFrame
from google_classroom_extractor.api.submissions import _sync_without_cleanup

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
        submissions_initial_df["Hash"] = submissions_initial_df.apply(
            lambda row: xxhash.xxh64_hexdigest(row.to_json().encode("utf-8")),
            axis=1,
        )
        dateToUse = datetime(2020, 9, 14, 12, 0, 0)
        submissions_initial_df["SyncNeeded"] = 0
        submissions_initial_df["CreateDate"] = dateToUse
        submissions_initial_df["LastModifiedDate"] = dateToUse

        submissions_sync_df = DataFrame(SYNC_DATA, columns=COLUMNS)

        with test_db_fixture.connect() as con:
            con.execute("DROP TABLE IF EXISTS StudentSubmissions")
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS StudentSubmissions (
                    courseId TEXT,
                    courseWorkId TEXT,
                    id TEXT,
                    userId TEXT,
                    creationTime TEXT,
                    updateTime TEXT,
                    state TEXT,
                    alternateLink TEXT,
                    courseWorkType TEXT,
                    submissionHistory TEXT,
                    late TEXT,
                    draftGrade TEXT,
                    assignedGrade TEXT,
                    "assignmentSubmission.attachments" TEXT,
                    associatedWithDeveloper TEXT,
                    Hash TEXT,
                    CreateDate DATETIME,
                    LastModifiedDate DATETIME,
                    SyncNeeded BIGINT,
                    PRIMARY KEY (id,courseId,courseWorkId,userId)
                )
                """
            )

        submissions_sync_df.to_sql(
            "StudentSubmissions", test_db_fixture, if_exists="append", index=False, chunksize=1000
        )

        # act
        _sync_without_cleanup(submissions_sync_df, test_db_fixture)

        return test_db_fixture

    def it_should_have_submissionss_table_with_updated_row_and_added_new_row(
        test_db_after_sync,
    ):
        EXPECTED_SUBMISSIONS_DATA_AFTER_SYNC = [
            CHANGED_SUBMISSION_AFTER,
            UNCHANGED_SUBMISSION,
            NEW_SUBMISSION,
        ]
        with test_db_after_sync.connect() as con:
            expected_submissions_df = (
                DataFrame(EXPECTED_SUBMISSIONS_DATA_AFTER_SYNC, columns=COLUMNS)
                .set_index(["id", "courseId", "courseWorkId", "userId"]).astype("string")  # ignore generated dataframe index
            )
            submissions_from_db_df = (
                read_sql_query("SELECT * from StudentSubmissions", con)
                .set_index(["id", "courseId", "courseWorkId", "userId"]).astype("string")  # ignore generated dataframe index
            )

            submissions_from_db_df.drop(labels=[
                "assignmentSubmission.attachments",
                "Hash",
                "CreateDate",
                "LastModifiedDate",
                "SyncNeeded"], axis=1, inplace=True)

            assert expected_submissions_df.to_csv() == submissions_from_db_df.to_csv()
