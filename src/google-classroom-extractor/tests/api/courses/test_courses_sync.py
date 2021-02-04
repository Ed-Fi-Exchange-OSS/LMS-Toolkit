# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import pytest
from pandas import read_sql_query, DataFrame
from google_classroom_extractor.api.courses import _sync_without_cleanup
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
    "section",
    "descriptionHeading",
    "room",
    "ownerId",
    "creationTime",
    "updateTime",
    "enrollmentCode",
    "courseState",
    "alternateLink",
    "teacherGroupEmail",
    "courseGroupEmail",
    "teacherFolder.id",
    "teacherFolder.title",
    "teacherFolder.alternateLink",
    "guardiansEnabled",
    "calendarId",
]

CHANGED_COURSE_BEFORE = [
    "1",
    "Changed Course",
    "11",
    "descriptionHeading1",
    "a1",
    "111",
    "2020-03-01 12:00:00",
    "2020-03-01 12:00:00",
    "1111",
    "ACTIVE",
    "http://111",
    "111@gmail.com",
    "111@hotmail.com",
    "111111",
    "1111111",
    "11111111",
    "True",
    "11111",
]

CHANGED_COURSE_AFTER = [
    "1",
    "Changed Course",
    "11",
    "*CHANGED*",
    "a1",
    "111",
    "2020-03-01 12:00:00",
    "2020-03-01 12:00:00",
    "1111",
    "ACTIVE",
    "http://111",
    "111@gmail.com",
    "111@hotmail.com",
    "111111",
    "1111111",
    "11111111",
    "True",
    "11111",
]

UNCHANGED_COURSE = [
    "2",
    "Unchanged Course",
    "22",
    "descriptionHeading2",
    "b2",
    "222",
    "2020-03-02 12:00:00",
    "2020-03-02 12:00:00",
    "2222",
    "ACTIVE",
    "https://222",
    "222@gmail.com",
    "222@hotmail.com",
    "222222",
    "2222222",
    "22222222",
    "True",
    "22222",
]

OMITTED_FROM_SYNC_COURSE = [
    "3",
    "Omitted From Sync Course",
    "33",
    "descriptionHeading3",
    "c3",
    "333",
    "2020-03-03 12:00:00",
    "2020-03-03 12:00:00",
    "3333",
    "ACTIVE",
    "https://333",
    "333@gmail.com",
    "333@hotmail.com",
    "333333",
    "3333333",
    "33333333",
    "True",
    "33333",
]

NEW_COURSE = [
    "4",
    "New Course",
    "44",
    "descriptionHeading4",
    "c4",
    "444",
    "2020-04-04 12:00:00",
    "2020-04-04 12:00:00",
    "4444",
    "ACTIVE",
    "https://444",
    "444@gmail.com",
    "444@hotmail.com",
    "444444",
    "4444444",
    "44444444",
    "True",
    "44444",
]

SYNC_DATA = [CHANGED_COURSE_AFTER, UNCHANGED_COURSE, NEW_COURSE]


def describe_when_testing_sync_with_new_and_missing_and_updated_rows():
    @pytest.fixture
    def test_db_after_sync(test_db_fixture):
        # arrange
        INITIAL_COURSE_DATA = [
            CHANGED_COURSE_BEFORE,
            UNCHANGED_COURSE,
            OMITTED_FROM_SYNC_COURSE,
        ]

        courses_initial_df = DataFrame(INITIAL_COURSE_DATA, columns=COLUMNS)
        courses_initial_df = add_hash_and_json_to(courses_initial_df)
        add_sourceid_to(courses_initial_df, IDENTITY_COLUMNS)

        dateToUse = datetime(2020, 9, 14, 12, 0, 0)
        courses_initial_df["SyncNeeded"] = 0
        courses_initial_df["CreateDate"] = dateToUse
        courses_initial_df["LastModifiedDate"] = dateToUse
        courses_initial_df = courses_initial_df[SYNC_COLUMNS]

        courses_sync_df = DataFrame(SYNC_DATA, columns=COLUMNS)

        with test_db_fixture.connect() as con:
            con.execute("DROP TABLE IF EXISTS Courses")
            con.execute(
                f"""
                CREATE TABLE IF NOT EXISTS Courses (
                    {SYNC_COLUMNS_SQL}
                )
                """
            )

        courses_initial_df.to_sql(
            "Courses", test_db_fixture, if_exists="append", index=False, chunksize=1000
        )

        # act
        _sync_without_cleanup(courses_sync_df, test_db_fixture)

        return test_db_fixture

    def it_should_have_courses_table_with_updated_row_and_added_new_row(
        test_db_after_sync,
    ):
        EXPECTED_COURSE_DATA_AFTER_SYNC = [
            UNCHANGED_COURSE,
            OMITTED_FROM_SYNC_COURSE,
            CHANGED_COURSE_AFTER,
            NEW_COURSE,
        ]
        with test_db_after_sync.connect() as con:
            expected_courses_df = prep_expected_sync_df(
                DataFrame(EXPECTED_COURSE_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            courses_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Courses", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_courses_df.to_csv() == courses_from_db_df.to_csv()

    def it_should_have_temporary_sync_table_unchanged(test_db_after_sync):
        EXPECTED_SYNC_DATA_AFTER_SYNC = SYNC_DATA
        with test_db_after_sync.connect() as con:
            expected_sync_courses_df = prep_expected_sync_df(
                DataFrame(EXPECTED_SYNC_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            sync_courses_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Sync_Courses", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_sync_courses_df.to_csv() == sync_courses_from_db_df.to_csv()

    def it_should_have_temporary_unmatched_table_with_correct_intermediate_rows(
        test_db_after_sync,
    ):
        EXPECTED_UNMATCHED_DATA_AFTER_SYNC = [
            CHANGED_COURSE_BEFORE,
            CHANGED_COURSE_AFTER,
            OMITTED_FROM_SYNC_COURSE,
            NEW_COURSE,
        ]
        with test_db_after_sync.connect() as con:
            expected_unmatched_df = prep_expected_sync_df(
                DataFrame(EXPECTED_UNMATCHED_DATA_AFTER_SYNC, columns=COLUMNS).astype(
                    "string"
                ),
                IDENTITY_COLUMNS,
            )

            unmatched_from_db_df = prep_from_sync_db_df(
                read_sql_query("SELECT * from Unmatched_Courses", con).astype("string"),
                IDENTITY_COLUMNS,
            )

            assert expected_unmatched_df.to_csv() == unmatched_from_db_df.to_csv()
