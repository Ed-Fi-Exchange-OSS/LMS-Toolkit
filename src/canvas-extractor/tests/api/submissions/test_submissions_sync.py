# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import pytest
from pandas import read_sql_query, DataFrame
from canvas_extractor.api.submissions import _sync_without_cleanup
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
    "body",
    "url",
    "grade",
    "score",
    "submitted_at",
    "assignment_id",
    "user_id",
    "submission_type",
    "workflow_state",
    "grade_matches_current_submission",
    "graded_at",
    "grader_id",
    "attempt",
    "cached_due_date",
    "excused",
    "late_policy_status",
    "points_deducted",
    "grading_period_id",
    "extra_attempts",
    "posted_at",
    "late",
    "missing",
    "seconds_late",
    "entered_grade",
    "entered_score",
    "preview_url",
    "discussion_entries",
    "anonymous_id",
    "course_id",
    "submitted_at_date",
    "graded_at_date",
    "cached_due_date_date",
    "posted_at_date",
    "attachments",
]

CHANGED_SUBMISSION_BEFORE = [
    "1",
    "Changed Submission Before",
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
    "11111111111111111111111111111",
    "11111111111111111111111111111",
    "11111111111111111111111111111",
    "11111111111111111111111111111",
]

CHANGED_SUBMISSION_AFTER = [
    "1",
    "*Changed Submission After*",
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
    "11111111111111111111111111111",
    "11111111111111111111111111111",
    "11111111111111111111111111111",
    "11111111111111111111111111111",
]

UNCHANGED_SUBMISSION = [
    "2",
    "Unchanged Submission",
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
    "22222222222222222222222222222",
    "22222222222222222222222222222",
    "22222222222222222222222222222",
    "22222222222222222222222222222",
]

OMITTED_FROM_SYNC_SUBMISSION = [
    "3",
    "Omitted From Sync Submission",
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
    "33333333333333333333333333333",
    "33333333333333333333333333333",
    "33333333333333333333333333333",
    "33333333333333333333333333333",
]

NEW_SUBMISSION = [
    "4",
    "New Submission",
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
    "44444444444444444444444444444",
    "44444444444444444444444444444",
    "44444444444444444444444444444",
    "44444444444444444444444444444",
]

SYNC_DATA = [CHANGED_SUBMISSION_AFTER, UNCHANGED_SUBMISSION, NEW_SUBMISSION]


def describe_when_testing_sync_with_new_and_missing_and_updated_rows():
    @pytest.fixture
    def test_db_after_sync(test_db_fixture):
        # arrange
        INITIAL_SUBMISSION_DATA = [
            CHANGED_SUBMISSION_BEFORE,
            UNCHANGED_SUBMISSION,
            OMITTED_FROM_SYNC_SUBMISSION,
        ]

        submissions_initial_df = DataFrame(INITIAL_SUBMISSION_DATA, columns=COLUMNS)
        submissions_initial_df = add_hash_and_json_to(submissions_initial_df)
        add_sourceid_to(submissions_initial_df, IDENTITY_COLUMNS)

        dateToUse = datetime(2020, 9, 14, 12, 0, 0)
        submissions_initial_df["SyncNeeded"] = 0
        submissions_initial_df["CreateDate"] = dateToUse
        submissions_initial_df["LastModifiedDate"] = dateToUse
        submissions_initial_df = submissions_initial_df[SYNC_COLUMNS]

        submissions_sync_df = DataFrame(SYNC_DATA, columns=COLUMNS)

        with test_db_fixture.connect() as con:
            con.execute("DROP TABLE IF EXISTS Submissions")
            con.execute(
                f"""
                CREATE TABLE IF NOT EXISTS Submissions (
                    {SYNC_COLUMNS_SQL}
                )
                """
            )

        submissions_initial_df.to_sql(
            "Submissions", test_db_fixture, if_exists="append", index=False, chunksize=1000
        )

        # act
        _sync_without_cleanup(submissions_sync_df, test_db_fixture)

        return test_db_fixture

    def it_should_have_submissions_table_with_updated_row_and_added_new_row(
        test_db_after_sync,
    ):
        EXPECTED_SUBMISSION_DATA_AFTER_SYNC = [
            UNCHANGED_SUBMISSION,
            OMITTED_FROM_SYNC_SUBMISSION,
            CHANGED_SUBMISSION_AFTER,
            NEW_SUBMISSION,
        ]
        with test_db_after_sync.connect() as con:
            expected_submissions_df = prep_expected_sync_df(
                DataFrame(EXPECTED_SUBMISSION_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            submissions_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Submissions", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_submissions_df.to_csv() == submissions_from_db_df.to_csv()

    def it_should_have_temporary_sync_table_unchanged(test_db_after_sync):
        EXPECTED_SYNC_DATA_AFTER_SYNC = SYNC_DATA
        with test_db_after_sync.connect() as con:
            expected_sync_submissions_df = prep_expected_sync_df(
                DataFrame(EXPECTED_SYNC_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            sync_submissions_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Sync_Submissions", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_sync_submissions_df.to_csv() == sync_submissions_from_db_df.to_csv()

    def it_should_have_temporary_unmatched_table_with_correct_intermediate_rows(
        test_db_after_sync,
    ):
        EXPECTED_UNMATCHED_DATA_AFTER_SYNC = [
            CHANGED_SUBMISSION_BEFORE,
            CHANGED_SUBMISSION_AFTER,
            OMITTED_FROM_SYNC_SUBMISSION,
            NEW_SUBMISSION,
        ]
        with test_db_after_sync.connect() as con:
            expected_unmatched_df = prep_expected_sync_df(
                DataFrame(EXPECTED_UNMATCHED_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            unmatched_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Unmatched_Submissions", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_unmatched_df.to_csv() == unmatched_from_db_df.to_csv()
