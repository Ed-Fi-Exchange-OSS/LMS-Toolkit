# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import pytest
import xxhash
from pandas import read_sql_query, DataFrame
from google_classroom_extractor.api.teachers import _sync_without_cleanup

COLUMNS = [
    "courseId",
    "userId",
    "profile.id",
    "profile.name.givenName",
    "profile.name.familyName",
    "profile.name.fullName",
    "profile.emailAddress",
    "profile.permissions",
    "profile.photoUrl",
    "profile.verifiedTeacher",
]

CHANGED_TEACHER_BEFORE = [
    "1",
    "11",
    "111",
    "givenName1",
    "familyName1",
    "fullName1",
    "1@gmail.com",
    "1111",
    "http://111",
    "False",
]

CHANGED_TEACHER_AFTER = [
    "1",
    "11",
    "111",
    "*CHANGED*",
    "familyName1",
    "fullName1",
    "1@gmail.com",
    "1111",
    "http://111",
    "False",
]

UNCHANGED_TEACHER = [
    "2",
    "22",
    "222",
    "givenName2",
    "familyName2",
    "fullName2",
    "2@gmail.com",
    "2222",
    "http://222",
    "False",
]

OMITTED_FROM_SYNC_TEACHER = [
    "3",
    "33",
    "333",
    "givenName3",
    "familyName3",
    "fullName3",
    "3@gmail.com",
    "3333",
    "http://333",
    "False",
]

NEW_TEACHER = [
    "4",
    "44",
    "444",
    "givenName4",
    "familyName4",
    "fullName4",
    "4@gmail.com",
    "4444",
    "http://444",
    "False",
]

SYNC_DATA = [CHANGED_TEACHER_AFTER, UNCHANGED_TEACHER, NEW_TEACHER]


def describe_when_testing_sync_with_new_and_missing_and_updated_rows():
    @pytest.fixture
    def test_db_after_sync(test_db_fixture):
        # arrange
        INITIAL_TEACHER_DATA = [
            CHANGED_TEACHER_BEFORE,
            UNCHANGED_TEACHER,
            OMITTED_FROM_SYNC_TEACHER,
        ]

        teachers_initial_df = DataFrame(INITIAL_TEACHER_DATA, columns=COLUMNS)
        teachers_initial_df["Hash"] = teachers_initial_df.apply(
            lambda row: xxhash.xxh64_hexdigest(row.to_json().encode("utf-8")),
            axis=1,
        )
        dateToUse = datetime(2020, 9, 14, 12, 0, 0)
        teachers_initial_df["SyncNeeded"] = 0
        teachers_initial_df["CreateDate"] = dateToUse
        teachers_initial_df["LastModifiedDate"] = dateToUse

        teachers_sync_df = DataFrame(SYNC_DATA, columns=COLUMNS)

        with test_db_fixture.connect() as con:
            con.execute("DROP TABLE IF EXISTS Teachers")
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS Teachers (
                    courseId TEXT,
                    userId TEXT,
                    "profile.id" TEXT,
                    "profile.name.givenName" TEXT,
                    "profile.name.familyName" TEXT,
                    "profile.name.fullName" TEXT,
                    "profile.emailAddress" TEXT,
                    "profile.permissions" TEXT,
                    "profile.photoUrl" TEXT,
                    "profile.verifiedTeacher" TEXT,
                    Hash TEXT,
                    CreateDate DATETIME,
                    LastModifiedDate DATETIME,
                    SyncNeeded BIGINT,
                    PRIMARY KEY (courseId,userId)
                )
                """
            )

        teachers_initial_df.to_sql(
            "Teachers", test_db_fixture, if_exists="append", index=False, chunksize=1000
        )

        # act
        _sync_without_cleanup(teachers_sync_df, test_db_fixture)

        return test_db_fixture

    def it_should_have_teachers_table_with_updated_row_and_added_new_row(
        test_db_after_sync,
    ):
        EXPECTED_TEACHER_DATA_AFTER_SYNC = [
            UNCHANGED_TEACHER,
            OMITTED_FROM_SYNC_TEACHER,
            CHANGED_TEACHER_AFTER,
            NEW_TEACHER,
        ]
        with test_db_after_sync.connect() as con:
            expected_teachers_df = (
                DataFrame(EXPECTED_TEACHER_DATA_AFTER_SYNC, columns=COLUMNS)
                .set_index(["courseId", "userId"])  # ignore generated dataframe index
                .astype("string")
            )
            teachers_from_db_df = (
                read_sql_query("SELECT * from Teachers", con)
                .loc[:, "courseId":"profile.verifiedTeacher"]  # original columns only
                .set_index(["courseId", "userId"])  # ignore generated dataframe index
                .astype("string")
            )
            assert expected_teachers_df.to_csv() == teachers_from_db_df.to_csv()

    def it_should_have_temporary_sync_table_unchanged(test_db_after_sync):
        EXPECTED_SYNC_DATA_AFTER_SYNC = SYNC_DATA
        with test_db_after_sync.connect() as con:
            expected_sync_teachers_df = DataFrame(
                EXPECTED_SYNC_DATA_AFTER_SYNC, columns=COLUMNS
            ).astype("string")
            sync_teachers_from_db_df = (
                read_sql_query("SELECT * from Sync_Teachers", con)
                .loc[:, "courseId":"profile.verifiedTeacher"]  # original columns only
                .astype("string")
            )
            assert expected_sync_teachers_df.to_csv() == sync_teachers_from_db_df.to_csv()

    def it_should_have_temporary_unmatched_table_with_correct_intermediate_rows(
        test_db_after_sync,
    ):
        EXPECTED_UNMATCHED_DATA_AFTER_SYNC = [
            CHANGED_TEACHER_AFTER,
            CHANGED_TEACHER_BEFORE,
            OMITTED_FROM_SYNC_TEACHER,
            NEW_TEACHER,
        ]
        with test_db_after_sync.connect() as con:
            expected_unmatched_df = DataFrame(
                EXPECTED_UNMATCHED_DATA_AFTER_SYNC, columns=COLUMNS
            ).astype("string")
            unmatched_from_db_df = (
                read_sql_query("SELECT * from Unmatched_Teachers", con)
                .loc[:, "courseId":"profile.verifiedTeacher"]  # original columns only
                .astype("string")
            )
            assert expected_unmatched_df.to_csv() == unmatched_from_db_df.to_csv()
