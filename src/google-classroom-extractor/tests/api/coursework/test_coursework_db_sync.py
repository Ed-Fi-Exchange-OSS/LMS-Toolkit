# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import pytest
import xxhash
from pandas import read_sql_query, DataFrame
from google_classroom_extractor.api.coursework import _sync_without_cleanup

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
        courseworks_initial_df["Hash"] = courseworks_initial_df.apply(
            lambda row: xxhash.xxh64_hexdigest(row.to_json().encode("utf-8")),
            axis=1,
        )
        dateToUse = datetime(2020, 9, 14, 12, 0, 0)
        courseworks_initial_df["SyncNeeded"] = 0
        courseworks_initial_df["CreateDate"] = dateToUse
        courseworks_initial_df["LastModifiedDate"] = dateToUse

        courseworks_sync_df = DataFrame(SYNC_DATA, columns=COLUMNS)

        with test_db_fixture.connect() as con:
            con.execute("DROP TABLE IF EXISTS Assignmments")
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS Assignmments (
                    courseId TEXT,
                    id TEXT,
                    title TEXT,
                    description TEXT,
                    materials TEXT,
                    state TEXT,
                    alternateLink TEXT,
                    creationTime TEXT,
                    updateTime TEXT,
                    maxPoints TEXT,
                    workType TEXT,
                    submissionModificationMode TEXT,
                    assigneeMode TEXT,
                    creatorUserId TEXT,
                    "dueDate.year" TEXT,
                    "dueDate.month" TEXT,
                    "dueDate.day" TEXT,
                    "dueTime.hours" TEXT,
                    "dueTime.minutes" TEXT,
                    "assignment.studentWorkFolder.id" TEXT,
                    "assignment.studentWorkFolder.title" TEXT,
                    "assignment.studentWorkFolder.alternateLink" TEXT,
                    topicId TEXT,
                    scheduledTime TEXT,
                    Hash TEXT,
                    CreateDate DATETIME,
                    LastModifiedDate DATETIME,
                    SyncNeeded BIGINT,
                    PRIMARY KEY (id,courseId)
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
            expected_courseworks_df = (
                DataFrame(EXPECTED_COURSEWORKS_DATA_AFTER_SYNC, columns=COLUMNS)
                .set_index(["id", "courseId"]).astype("string")  # ignore generated dataframe index
            )
            courseworks_from_db_df = (
                read_sql_query("SELECT * from Assignmments", con)
                .set_index(["id", "courseId"]).astype("string")  # ignore generated dataframe index
            )

            courseworks_from_db_df.drop(labels=[
                'materials',
                'assignment.studentWorkFolder.id',
                'assignment.studentWorkFolder.title',
                'assignment.studentWorkFolder.alternateLink',
                'Hash',
                'CreateDate',
                'LastModifiedDate',
                'SyncNeeded'], axis=1, inplace=True)  # deleting null columns not provided for the test

            assert expected_courseworks_df.to_csv() == courseworks_from_db_df.to_csv()
