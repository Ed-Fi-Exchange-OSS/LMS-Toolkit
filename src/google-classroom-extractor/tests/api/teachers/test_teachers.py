# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict
from unittest.mock import patch
import pandas as pd
from google_classroom_extractor.api.teachers import request_all_teachers_as_df
from tests.helper import merged_dict


def dataframe_row_count(dataframe) -> int:
    return dataframe.shape[0]


def db_row_count(test_db) -> int:
    return test_db.engine.execute("SELECT COUNT(rowid) from Teachers").scalar()


def db_ending_user_id(test_db) -> int:
    return test_db.engine.execute(
        "SELECT userId from Teachers WHERE rowid = (SELECT MAX(rowid) from Teachers)"
    ).scalar()


def db_email_by_course_and_user_id(test_db, course_id, user_id) -> int:
    return test_db.engine.execute(
        f"SELECT [profile.emailAddress] from Teachers WHERE courseId = '{course_id}' AND userId = '{user_id}'"
    ).scalar()


DUMMY_COURSE_IDS = ["1", "2"]


def describe_when_overlap_removal_is_needed():
    @patch("google_classroom_extractor.api.teachers.request_latest_teachers_as_df")
    def it_should_load_three_pulls_in_a_row_with_overlap_correctly(
        mock_latest_teachers_df, test_db_fixture
    ):
        # 1st pull: 17 rows
        mock_latest_teachers_df.return_value = pd.read_csv(
            "tests/api/teachers/teachers-1st.csv"
        )
        first_teachers_df = request_all_teachers_as_df(
            None, DUMMY_COURSE_IDS, test_db_fixture
        )
        assert dataframe_row_count(first_teachers_df) == 17
        assert db_row_count(test_db_fixture) == 17
        assert db_ending_user_id(test_db_fixture) == 87275837

        # 2nd pull: 43 rows, overlaps 7
        mock_latest_teachers_df.return_value = pd.read_csv(
            "tests/api/teachers/teachers-2nd-overlaps-1st.csv"
        )
        second_teachers_df = request_all_teachers_as_df(
            None, DUMMY_COURSE_IDS, test_db_fixture
        )
        assert dataframe_row_count(second_teachers_df) == 43
        assert (
            db_row_count(test_db_fixture) == 50
        )  # 43 new + 14 existing - 7 overlapping
        assert db_ending_user_id(test_db_fixture) == 80099260

        # 3rd pull: 98 rows, overlaps 43
        mock_latest_teachers_df.return_value = pd.read_csv(
            "tests/api/teachers/teachers-3rd-overlaps-1st-and-2nd.csv"
        )
        third_teachers_df = request_all_teachers_as_df(
            None, DUMMY_COURSE_IDS, test_db_fixture
        )
        assert dataframe_row_count(third_teachers_df) == 98
        assert (
            db_row_count(test_db_fixture) == 99
        )  # 98 new + 44 existing - 43 overlapping
        assert db_ending_user_id(test_db_fixture) == 92311706


def describe_when_pulls_of_same_teacher_data_differ_in_email_address():
    course_id = "5583344"
    user_id = "79924907"
    consistent_rows: Dict[str, str] = {
        "courseId": course_id,
        "userId": user_id,
        "profile.id": "60436435",
        "profile.name.givenName": "Karen",
        "profile.name.familyName": "Owens",
        "profile.name.fullName": "Karen Owens",
        "profile.emailAddress": "karen21@hotmail.com",
    }
    initial_email = "kowens@gmail.com"
    update_email = "karens@hotmail.com"

    @patch("google_classroom_extractor.api.teachers.request_latest_teachers_as_df")
    def it_should_replace_old_email_with_new(mock_latest_teachers_df, test_db_fixture):
        mock_latest_teachers_df.return_value = pd.DataFrame.from_dict(
            [merged_dict(consistent_rows, {"profile.emailAddress": initial_email})]
        )

        # initial pull
        first_teachers_df = request_all_teachers_as_df(
            None, DUMMY_COURSE_IDS, test_db_fixture
        )
        assert dataframe_row_count(first_teachers_df) == 1
        assert db_row_count(test_db_fixture) == 1
        assert (
            db_email_by_course_and_user_id(test_db_fixture, course_id, user_id)
            == initial_email
        )

        # same teacher, with email updated
        mock_latest_teachers_df.return_value = pd.DataFrame.from_dict(
            [merged_dict(consistent_rows, {"profile.emailAddress": update_email})]
        )

        # overwrite pull
        overwrite_teachers_df = request_all_teachers_as_df(
            None, DUMMY_COURSE_IDS, test_db_fixture
        )
        assert dataframe_row_count(overwrite_teachers_df) == 1
        assert db_row_count(test_db_fixture) == 1
        assert (
            db_email_by_course_and_user_id(test_db_fixture, course_id, user_id)
            == update_email
        )
