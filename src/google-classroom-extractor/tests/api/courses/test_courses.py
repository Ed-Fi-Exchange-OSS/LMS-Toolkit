# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from pathlib import Path
from unittest.mock import patch
import pandas as pd
from sqlalchemy import create_engine
from google_classroom_extractor.api.courses import request_all_courses_as_df

DB_FILE = "tests/api/courses/test_courses.db"


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


@patch("google_classroom_extractor.api.courses.request_latest_courses_as_df")
def test_overlap_removal(mock_latest_courses_df):
    Path(DB_FILE).unlink(missing_ok=True)
    test_db = create_engine(f"sqlite:///{DB_FILE}", echo=True)

    # 1st pull: courses-1st.csv is 17 rows ending with "Julia Harding"
    mock_latest_courses_df.return_value = pd.read_csv("tests/api/courses/courses-1st.csv")
    first_courses_df = request_all_courses_as_df(None, test_db)
    assert dataframe_row_count(first_courses_df) == 17
    assert db_row_count(test_db) == 17
    assert db_ending_name(test_db) == "Julia Harding"

    # 2nd pull: courses-2nd-overlaps-1st is 59 rows with 5 overlapping ending with "Maurice Hatfield"
    mock_latest_courses_df.return_value = pd.read_csv(
        "tests/api/courses/courses-2nd-overlaps-1st.csv"
    )
    second_courses_df = request_all_courses_as_df(None, test_db)
    assert dataframe_row_count(second_courses_df) == 59
    assert db_row_count(test_db) == 71  # 59 new + 17 existing - 5 overlapping
    assert db_ending_name(test_db) == "Maurice Hatfield"

    # 3rd pull: courses-3rd-overlaps-1st-and-2nd is 87 rows with 5 overlapping ending with "Troy Greene"
    mock_latest_courses_df.return_value = pd.read_csv(
        "tests/api/courses/courses-3rd-overlaps-1st-and-2nd.csv"
    )
    third_courses_df = request_all_courses_as_df(None, test_db)
    assert dataframe_row_count(third_courses_df) == 87
    assert db_row_count(test_db) == 99  # 87 new + 71 existing - 59 overlapping
    assert db_ending_name(test_db) == "Troy Greene"


@patch("google_classroom_extractor.api.courses.request_latest_courses_as_df")
def test_value_replacement(mock_latest_courses_df):
    Path(DB_FILE).unlink(missing_ok=True)
    test_db = create_engine(f"sqlite:///{DB_FILE}", echo=True)

    # original course
    course_id = "1234"
    initial_room_id = "Room1234"
    mock_latest_courses_df.return_value = pd.DataFrame(
        {
            "id": [course_id],
            "name": ["Course1234"],
            "section": ["77"],
            "descriptionHeading": ["Universal analyzing firmware"],
            "description": ["Girl same long seat red fish."],
            "room": [initial_room_id],
            "ownerId": ["5904628"],
            "creationTime": ["2020-03-06 18:07:56"],
            "updateTime": ["2020-09-14 17:48:53"],
            "enrollmentCode": ["747450"],
            "courseState": ["ACTIVE"],
            "alternateLink": ["http://www.branch.com/register/"],
            "teacherGroupEmail": ["catherinedixon@gmail.com"],
            "courseGroupEmail": ["bwheeler@gmail.com"],
            "guardiansEnabled": ["True"],
            "calendarId": ["25816937"],
        }
    )

    # initial pull
    first_courses_df = request_all_courses_as_df(None, test_db)
    assert dataframe_row_count(first_courses_df) == 1
    assert db_row_count(test_db) == 1
    assert db_room_by_course_id(test_db, course_id) == initial_room_id

    # same course, with room updated
    update_room_id = "room2345"
    mock_latest_courses_df.return_value = pd.DataFrame(
        {
            "id": [course_id],
            "name": ["Course1234"],
            "section": ["77"],
            "descriptionHeading": ["Universal analyzing firmware"],
            "description": ["Girl same long seat red fish."],
            "room": [update_room_id],
            "ownerId": ["5904628"],
            "creationTime": ["2020-03-06 18:07:56"],
            "updateTime": ["2020-09-20 17:48:53"],
            "enrollmentCode": ["747450"],
            "courseState": ["ACTIVE"],
            "alternateLink": ["http://www.branch.com/register/"],
            "teacherGroupEmail": ["catherinedixon@gmail.com"],
            "courseGroupEmail": ["bwheeler@gmail.com"],
            "guardiansEnabled": ["True"],
            "calendarId": ["25816937"],
        }
    )

    # overwrite pull
    overwrite_courses_df = request_all_courses_as_df(None, test_db)
    assert dataframe_row_count(overwrite_courses_df) == 1
    assert db_row_count(test_db) == 1
    assert db_room_by_course_id(test_db, course_id) == update_room_id
