# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict
from unittest.mock import patch
from pandas import DataFrame, read_csv
from google_classroom_extractor.api.coursework import request_all_coursework_as_df
from tests.helper import merged_dict


def dataframe_row_count(dataframe) -> int:
    return dataframe.shape[0]


def db_row_count(test_db) -> int:
    return test_db.engine.execute("SELECT COUNT(rowid) from Coursework").scalar()


def db_ending_id(test_db) -> int:
    return test_db.engine.execute(
        "SELECT id from Coursework WHERE rowid = (SELECT MAX(rowid) from Coursework)"
    ).scalar()


def db_state_by_coursework_id(test_db, coursework_id) -> int:
    return test_db.engine.execute(
        f"SELECT state from Coursework WHERE id = '{coursework_id}'"
    ).scalar()


DUMMY_COURSE_IDS = ["1", "2"]


def describe_when_overlap_removal_is_needed():
    @patch("google_classroom_extractor.api.coursework.request_latest_coursework_as_df")
    def it_should_load_three_pulls_in_a_row_with_overlap_correctly(
        mock_latest_coursework_df, test_db_fixture
    ):
        # 1st pull: 17 rows, last row id is 87699559
        mock_latest_coursework_df.return_value = read_csv(
            "tests/api/coursework/coursework-1st.csv"
        )
        first_coursework_df = request_all_coursework_as_df(
            None, DUMMY_COURSE_IDS, test_db_fixture
        )
        assert dataframe_row_count(first_coursework_df) == 17
        assert db_row_count(test_db_fixture) == 17
        assert db_ending_id(test_db_fixture) == 87699559

        # 2nd pull: 39 rows, overlaps 7, last row id is 87025291
        mock_latest_coursework_df.return_value = read_csv(
            "tests/api/coursework/coursework-2nd-overlaps-1st.csv"
        )
        second_coursework_df = request_all_coursework_as_df(
            None, DUMMY_COURSE_IDS, test_db_fixture
        )
        assert dataframe_row_count(second_coursework_df) == 39
        assert (
            db_row_count(test_db_fixture) == 44
        )  # 39 new + 12 existing - 7 overlapping
        assert db_ending_id(test_db_fixture) == 87025291

        # 3rd pull: 98 rows, overlaps 43, last row id is 15461200
        mock_latest_coursework_df.return_value = read_csv(
            "tests/api/coursework/coursework-3rd-overlaps-1st-and-2nd.csv"
        )
        third_coursework_df = request_all_coursework_as_df(
            None, DUMMY_COURSE_IDS, test_db_fixture
        )
        assert dataframe_row_count(third_coursework_df) == 98
        assert (
            db_row_count(test_db_fixture) == 99
        )  # 98 new + 44 existing - 43 overlapping
        assert db_ending_id(test_db_fixture) == 15461200


def describe_when_two_pulls_of_same_coursework_data_differ_in_state():
    coursework_id = "123456"
    consistent_rows: Dict[str, str] = {
        "courseId": "1234",
        "id": coursework_id,
        "title": "Customer-focused eco-centric standardization",
        "description": "Herself PM out far really beautiful.",
        "creationTime": "2020-01-12 03:52:52",
        "updateTime": "2020-09-20 12:37:54",
        "dueDate": "2020-09-11",
        "dueTime": "22:47:58",
        "scheduledTime": "23:23:01",
        "maxPoints": "75",
        "workType": "ASSIGNMENT",
        "creatorUserId": "49165122",
        "topicId": "81859357",
    }
    initial_state = "CREATED"
    update_state = "PUBLISHED"

    @patch("google_classroom_extractor.api.coursework.request_latest_coursework_as_df")
    def it_should_replace_old_state_with_new(
        mock_latest_coursework_df, test_db_fixture
    ):
        # original coursework
        mock_latest_coursework_df.return_value = DataFrame.from_dict(
            [merged_dict(consistent_rows, {"state": initial_state})]
        )

        # initial pull
        first_coursework_df = request_all_coursework_as_df(
            None, DUMMY_COURSE_IDS, test_db_fixture
        )
        assert dataframe_row_count(first_coursework_df) == 1
        assert db_row_count(test_db_fixture) == 1
        assert (
            db_state_by_coursework_id(test_db_fixture, coursework_id) == initial_state
        )

        # same coursework, with state updated
        mock_latest_coursework_df.return_value = DataFrame.from_dict(
            [merged_dict(consistent_rows, {"state": update_state})]
        )

        # overwrite pull
        overwrite_coursework_df = request_all_coursework_as_df(
            None, DUMMY_COURSE_IDS, test_db_fixture
        )
        assert dataframe_row_count(overwrite_coursework_df) == 1
        assert db_row_count(test_db_fixture) == 1
        assert db_state_by_coursework_id(test_db_fixture, coursework_id) == update_state
