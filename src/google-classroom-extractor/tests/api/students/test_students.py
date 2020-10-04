# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from pathlib import Path
from unittest.mock import patch
import pandas as pd
from sqlalchemy import create_engine
from google_classroom_extractor.api.students import request_all_students_as_df

DB_FILE = "tests/api/students/test_students.db"


def dataframe_row_count(dataframe) -> int:
    return dataframe.shape[0]


def db_row_count(test_db) -> int:
    return test_db.engine.execute("SELECT COUNT(rowid) from Students").scalar()


def db_ending_user_id(test_db) -> int:
    return test_db.engine.execute(
        "SELECT userId from Students WHERE rowid = (SELECT MAX(rowid) from Students)"
    ).scalar()


def db_email_by_course_and_user_id(test_db, course_id, user_id) -> int:
    return test_db.engine.execute(
        f"SELECT [profile.emailAddress] from Students WHERE courseId = '{course_id}' AND userId = '{user_id}'"
    ).scalar()


DUMMY_COURSE_IDS = ["1", "2"]


@patch("google_classroom_extractor.api.students.request_latest_students_as_df")
def test_overlap_removal(mock_latest_students_df):
    Path(DB_FILE).unlink(missing_ok=True)
    test_db = create_engine(f"sqlite:///{DB_FILE}", echo=True)

    # 1st pull: 17 rows
    mock_latest_students_df.return_value = pd.read_csv(
        "tests/api/students/students-1st.csv"
    )
    first_students_df = request_all_students_as_df(None, DUMMY_COURSE_IDS, test_db)
    assert dataframe_row_count(first_students_df) == 17
    assert db_row_count(test_db) == 17
    assert db_ending_user_id(test_db) == 87275837

    # 2nd pull: 43 rows, overlaps 7
    mock_latest_students_df.return_value = pd.read_csv(
        "tests/api/students/students-2nd-overlaps-1st.csv"
    )
    second_students_df = request_all_students_as_df(None, DUMMY_COURSE_IDS, test_db)
    assert dataframe_row_count(second_students_df) == 43
    assert db_row_count(test_db) == 50  # 43 new + 14 existing - 7 overlapping
    assert db_ending_user_id(test_db) == 80099260

    # 3rd pull: 98 rows, overlaps 43
    mock_latest_students_df.return_value = pd.read_csv(
        "tests/api/students/students-3rd-overlaps-1st-and-2nd.csv"
    )
    third_students_df = request_all_students_as_df(None, DUMMY_COURSE_IDS, test_db)
    assert dataframe_row_count(third_students_df) == 98
    assert db_row_count(test_db) == 99  # 98 new + 44 existing - 43 overlapping
    assert db_ending_user_id(test_db) == 92311706


@patch("google_classroom_extractor.api.students.request_latest_students_as_df")
def test_value_replacement(mock_latest_students_df):
    Path(DB_FILE).unlink(missing_ok=True)
    test_db = create_engine(f"sqlite:///{DB_FILE}", echo=True)

    course_id = "5583344"
    user_id = "79924907"

    # original students
    mock_latest_students_df.return_value = pd.DataFrame(
        {
            "courseId": [course_id],
            "userId": [user_id],
            "profile.id": ["60436435"],
            "profile.name.givenName": ["Karen"],
            "profile.name.familyName": ["Owens"],
            "profile.name.fullName": ["Karen Owens"],
            "profile.emailAddress": ["karen21@hotmail.com"],
        }
    )

    # initial pull
    first_students_df = request_all_students_as_df(None, DUMMY_COURSE_IDS, test_db)
    assert dataframe_row_count(first_students_df) == 1
    assert db_row_count(test_db) == 1
    assert db_email_by_course_and_user_id(test_db, course_id, user_id) == "karen21@hotmail.com"

    # same student, with email updated
    mock_latest_students_df.return_value = pd.DataFrame(
        {
            "courseId": [course_id],
            "userId": [user_id],
            "profile.id": ["60436435"],
            "profile.name.givenName": ["Karen"],
            "profile.name.familyName": ["Owens"],
            "profile.name.fullName": ["Karen Owens"],
            "profile.emailAddress": ["kowens@gmail.com"],
        }
    )

    # overwrite pull
    overwrite_students_df = request_all_students_as_df(None, DUMMY_COURSE_IDS, test_db)
    assert dataframe_row_count(overwrite_students_df) == 1
    assert db_row_count(test_db) == 1
    assert db_email_by_course_and_user_id(test_db, course_id, user_id) == "kowens@gmail.com"
