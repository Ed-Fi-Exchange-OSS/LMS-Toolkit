# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import pytest
from pandas import read_sql_query, DataFrame
from google_classroom_extractor.api.coursework import _sync_without_cleanup
from edfi_lms_extractor_lib.api.resource_sync import (
    SYNC_COLUMNS_SQL,
    SYNC_COLUMNS,
    add_hash_and_json_to,
    add_sourceid_to,
)
from tests.api.api_helper import prep_expected_sync_df, prep_from_sync_db_df

IDENTITY_COLUMNS = ["courseId", "id"]

COLUMNS = [
    "courseId",
    "id",
    "title",
    "description",
    "state",
    "alternateLink",
    "creationTime",
    "updateTime",
    "maxPoints",
    "workType",
    "submissionModificationMode",
    "assigneeMode",
    "creatorUserId",
    "dueDate.year",
    "dueDate.month",
    "dueDate.day",
    "dueTime.hours",
    "dueTime.minutes",
    "topicId",
    "scheduledTime",
]

CHANGED_COURSEWORK_BEFORE = [
    "1",
    "11",
    "title",
    "description",
    "state",
    "link",
    "2020-08-19T21:02:46.877Z",
    "2020-08-19T21:02:46.877Z",
    "100",
    "ASSIGNMENT",
    "2",
    "1",
    "111",
    "2020",
    "02",
    "01",
    "05",
    "25",
    "1111",
    "25",
]

CHANGED_COURSEWORK_AFTER = [
    "1",
    "11",
    "title",
    "CHANGED*",
    "state",
    "link",
    "2020-08-19T21:02:46.877Z",
    "2020-08-19T21:02:46.877Z",
    "100",
    "ASSIGNMENT",
    "2",
    "1",
    "111",
    "2020",
    "02",
    "01",
    "05",
    "25",
    "1111",
    "25",
]

UNCHANGED_COURSEWORK = [
    "2",
    "21",
    "title",
    "description*",
    "state",
    "link",
    "2020-08-19T21:02:46.877Z",
    "2020-08-19T21:02:46.877Z",
    "100",
    "ASSIGNMENT",
    "2",
    "1",
    "211",
    "2020",
    "02",
    "01",
    "05",
    "25",
    "2111",
    "25",
]

NEW_COURSEWORK = [
    "3",
    "31",
    "title",
    "description*",
    "state",
    "link",
    "2020-08-19T21:02:46.877Z",
    "2020-08-19T21:02:46.877Z",
    "100",
    "ASSIGNMENT",
    "3",
    "3",
    "311",
    "2020",
    "02",
    "01",
    "05",
    "25",
    "3111",
    "25",
]

SYNC_DATA = [CHANGED_COURSEWORK_AFTER, UNCHANGED_COURSEWORK, NEW_COURSEWORK]


def describe_when_testing_sync_with_new_and_missing_and_updated_rows():
    @pytest.fixture
    def test_db_after_sync(test_db_fixture):
        # arrange
        INITIAL_DATA = [
            CHANGED_COURSEWORK_BEFORE,
            UNCHANGED_COURSEWORK
        ]

        courseworks_initial_df = DataFrame(INITIAL_DATA, columns=COLUMNS)
        courseworks_initial_df = add_hash_and_json_to(courseworks_initial_df)
        add_sourceid_to(courseworks_initial_df, IDENTITY_COLUMNS)

        dateToUse = datetime(2020, 9, 14, 12, 0, 0)
        courseworks_initial_df["SyncNeeded"] = 0
        courseworks_initial_df["CreateDate"] = dateToUse
        courseworks_initial_df["LastModifiedDate"] = dateToUse
        courseworks_initial_df = courseworks_initial_df[SYNC_COLUMNS]

        courseworks_sync_df = DataFrame(SYNC_DATA, columns=COLUMNS)

        with test_db_fixture.connect() as con:
            con.execute("DROP TABLE IF EXISTS Assignmments")
            con.execute(
                f"""
                CREATE TABLE IF NOT EXISTS Assignmments (
                    {SYNC_COLUMNS_SQL}
                )
                """
            )

        courseworks_initial_df.to_sql(
            "Assignmments", test_db_fixture, if_exists="append", index=False, chunksize=1000
        )

        # act
        _sync_without_cleanup(courseworks_sync_df, test_db_fixture)

        return test_db_fixture

    def it_should_have_courseworks_table_with_updated_row_and_added_new_row(
        test_db_after_sync,
    ):
        EXPECTED_COURSEWORKS_DATA_AFTER_SYNC = [
            UNCHANGED_COURSEWORK,
            CHANGED_COURSEWORK_AFTER,
            NEW_COURSEWORK,
        ]
        with test_db_after_sync.connect() as con:
            expected_courseworks_df = prep_expected_sync_df(
                DataFrame(EXPECTED_COURSEWORKS_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            courseworks_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Assignmments", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_courseworks_df.to_csv() == courseworks_from_db_df.to_csv()
