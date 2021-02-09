# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
from typing import List
from pathlib import Path
import pytest
from pandas import read_sql_query, DataFrame
from sqlalchemy import create_engine
from edfi_lms_extractor_lib.api.resource_sync import (
    SYNC_COLUMNS_SQL,
    SYNC_COLUMNS,
    add_hash_and_json_to,
    add_sourceid_to,
    sync_to_db_without_cleanup,
)

DB_FILE = "tests/api/test.db"

IDENTITY_COLUMNS = ["id"]

COLUMNS = [
    "id",
    "name",
    "descriptionHeading",
]

CHANGED_COURSE_BEFORE = [
    "1",
    "Changed Course",
    "descriptionHeading1",
]

CHANGED_COURSE_AFTER = [
    "1",
    "Changed Course",
    "*CHANGED*",
]

UNCHANGED_COURSE = [
    "2",
    "Unchanged Course",
    "descriptionHeading2",
]

OMITTED_FROM_SYNC_COURSE = [
    "3",
    "Omitted From Sync Course",
    "descriptionHeading3",
]

NEW_COURSE = [
    "4",
    "New Course",
    "descriptionHeading4",
]

SYNC_DATA = [CHANGED_COURSE_AFTER, UNCHANGED_COURSE, NEW_COURSE]


def prep_expected_sync_df(df: DataFrame, identity_columns: List[str]) -> DataFrame:
    result_df: DataFrame = add_hash_and_json_to(df)
    add_sourceid_to(result_df, identity_columns)
    result_df = result_df[["Json", "Hash", "SourceId"]]
    result_df.set_index("SourceId", inplace=True)
    return result_df


def prep_from_sync_db_df(df: DataFrame, identity_columns: List[str]) -> DataFrame:
    result_df: DataFrame = df[["Json", "Hash", "SourceId"]]
    result_df.set_index("SourceId", inplace=True)
    return result_df


@pytest.fixture
def test_db_fixture():
    Path(DB_FILE).unlink(missing_ok=True)
    yield create_engine(f"sqlite:///{DB_FILE}", echo=True)


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
        sync_to_db_without_cleanup(courses_sync_df, IDENTITY_COLUMNS, "Courses", test_db_fixture)

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
