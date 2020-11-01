# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict
from unittest.mock import patch
from pandas import DataFrame, read_csv
from google_classroom_extractor.api.courses import request_all_courses_as_df
from tests.helper import merged_dict


def dataframe_row_count(dataframe) -> int:
    return dataframe.shape[0]


def db_row_count(test_db) -> int:
    return test_db.engine.execute("SELECT COUNT(rowid) from Courses").scalar()


def db_ending_name(test_db) -> int:
    return test_db.engine.execute(
        "SELECT name from Courses WHERE rowid = (SELECT MAX(rowid) from Courses)"
    ).scalar()


def db_room_by_course_id(test_db, course_id) -> int:
    return test_db.engine.execute(
        f"SELECT room from Courses WHERE id = '{course_id}'"
    ).scalar()


def describe_when_overlap_removal_is_needed():
    @patch("google_classroom_extractor.api.courses.request_latest_courses_as_df")
    def it_should_load_three_pulls_in_a_row_with_overlap_correctly(
        mock_latest_courses_df, test_db_fixture
    ):
        # 1st pull: courses-1st.csv is 17 rows ending with "Julia Harding"
        mock_latest_courses_df.return_value = read_csv(
            "tests/api/courses/courses-1st.csv"
        )
        first_courses_df = request_all_courses_as_df(None, test_db_fixture)
        assert dataframe_row_count(first_courses_df) == 17
        assert db_row_count(test_db_fixture) == 17
        assert db_ending_name(test_db_fixture) == "Julia Harding"

        # 2nd pull: courses-2nd-overlaps-1st is 59 rows with 5 overlapping ending with "Maurice Hatfield"
        mock_latest_courses_df.return_value = read_csv(
            "tests/api/courses/courses-2nd-overlaps-1st.csv"
        )
        second_courses_df = request_all_courses_as_df(None, test_db_fixture)
        assert dataframe_row_count(second_courses_df) == 59
        assert (
            db_row_count(test_db_fixture) == 71
        )  # 59 new + 17 existing - 5 overlapping
        assert db_ending_name(test_db_fixture) == "Maurice Hatfield"

        # 3rd pull: courses-3rd-overlaps-1st-and-2nd is 87 rows with 5 overlapping ending with "Troy Greene"
        mock_latest_courses_df.return_value = read_csv(
            "tests/api/courses/courses-3rd-overlaps-1st-and-2nd.csv"
        )
        third_courses_df = request_all_courses_as_df(None, test_db_fixture)
        assert dataframe_row_count(third_courses_df) == 87
        assert (
            db_row_count(test_db_fixture) == 99
        )  # 87 new + 71 existing - 59 overlapping
        assert db_ending_name(test_db_fixture) == "Troy Greene"


def describe_when_pulls_of_same_course_data_differ_in_room_id():
    course_id = "1234"
    consistent_rows: Dict[str, str] = {
        "id": course_id,
        "name": "Course1234",
        "section": "77",
        "descriptionHeading": "Universal analyzing firmware",
        "description": "Girl same long seat red fish.",
        "ownerId": "5904628",
        "creationTime": "2020-03-06 18:07:56",
        "updateTime": "2020-09-14 17:48:53",
        "enrollmentCode": "747450",
        "courseState": "ACTIVE",
        "alternateLink": "http://www.branch.com/register/",
        "teacherGroupEmail": "catherinedixon@gmail.com",
        "courseGroupEmail": "bwheeler@gmail.com",
        "guardiansEnabled": "True",
        "calendarId": "25816937",
    }
    initial_room_id = "Room1234"
    update_room_id = "room2345"

    @patch("google_classroom_extractor.api.courses.request_latest_courses_as_df")
    def it_should_replace_old_room_id_with_new(mock_latest_courses_df, test_db_fixture):
        mock_latest_courses_df.return_value = DataFrame.from_dict(
            [merged_dict(consistent_rows, {"room": initial_room_id})]
        )

        # initial pull
        first_courses_df = request_all_courses_as_df(None, test_db_fixture)
        assert dataframe_row_count(first_courses_df) == 1
        assert db_row_count(test_db_fixture) == 1
        assert db_room_by_course_id(test_db_fixture, course_id) == initial_room_id

        # same course, with room updated
        mock_latest_courses_df.return_value = DataFrame.from_dict(
            [merged_dict(consistent_rows, {"room": update_room_id})]
        )

        # overwrite pull
        overwrite_courses_df = request_all_courses_as_df(None, test_db_fixture)
        assert dataframe_row_count(overwrite_courses_df) == 1
        assert db_row_count(test_db_fixture) == 1
        assert db_room_by_course_id(test_db_fixture, course_id) == update_room_id
