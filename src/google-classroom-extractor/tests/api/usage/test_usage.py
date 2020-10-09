# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict
from unittest.mock import patch
import pandas as pd
from google_classroom_extractor.api.usage import request_all_usage_as_df
from tests.helper import merged_dict


def dataframe_row_count(dataframe) -> int:
    return dataframe.shape[0]


def db_row_count(test_db) -> int:
    return test_db.engine.execute("SELECT COUNT(rowid) from Usage").scalar()


def db_ending_email(test_db) -> int:
    return test_db.engine.execute(
        "SELECT email from Usage WHERE rowid = (SELECT MAX(rowid) from Usage)"
    ).scalar()


def db_posts_by_name_date(test_db, name_date) -> int:
    return test_db.engine.execute(
        f"SELECT numberOfPosts from Usage WHERE nameDate = '{name_date}'"
    ).scalar()


def describe_when_overlap_removal_is_needed():
    @patch("google_classroom_extractor.api.usage.request_latest_usage_as_df")
    def it_should_load_three_pulls_in_a_row_with_overlap_correctly(
        mock_latest_usage_df, test_db_fixture
    ):
        # 1st pull: 17 rows
        mock_latest_usage_df.return_value = pd.read_csv("tests/api/usage/usage-1st.csv")
        first_usage_df = request_all_usage_as_df(None, test_db_fixture)
        assert dataframe_row_count(first_usage_df) == 17
        assert db_row_count(test_db_fixture) == 17
        assert db_ending_email(test_db_fixture) == "luislopez@conrad-turner.com"

        # 2nd pull: 49 rows, overlaps 7
        mock_latest_usage_df.return_value = pd.read_csv(
            "tests/api/usage/usage-2nd-overlaps-1st.csv"
        )
        second_usage_df = request_all_usage_as_df(None, test_db_fixture)
        assert dataframe_row_count(second_usage_df) == 49
        assert (
            db_row_count(test_db_fixture) == 59
        )  # 49 new + 17 existing - 7 overlapping
        assert db_ending_email(test_db_fixture) == "xavierlopez@hotmail.com"

        # 3rd pull: 98 rows, overlaps 49
        mock_latest_usage_df.return_value = pd.read_csv(
            "tests/api/usage/usage-3rd-overlaps-1st-and-2nd.csv"
        )
        third_usage_df = request_all_usage_as_df(None, test_db_fixture)
        assert dataframe_row_count(third_usage_df) == 98
        assert (
            db_row_count(test_db_fixture) == 99
        )  # 98 new + 44 existing - 43 overlapping
        assert db_ending_email(test_db_fixture) == "petersstephen@yahoo.com"


def describe_when_pulls_of_same_usage_data_differ_in_number_of_posts():
    name_date = "april.vaughan 08/20"
    consistent_rows: Dict[str, str] = {
        "email": "april.vaughan@yahoo.com",
        "asOfDate": "2020-09-03 00:36:50",
        "importDate": "2020-09-15 18:58:05",
        "numberOfPosts": "3",
        "lastInteractionTime": "2020-09-07 22:05:37",
        "lastLoginTime": "2020-09-07 22:05:37",
        "name": "april.vaughan",
        "monthDay": "08/20",
        "nameDate": name_date,
    }
    initial_posts = "3"
    update_posts = "5"

    @patch("google_classroom_extractor.api.usage.request_latest_usage_as_df")
    def it_should_replace_old_post_count_with_new(
        mock_latest_usage_df, test_db_fixture
    ):
        mock_latest_usage_df.return_value = pd.DataFrame.from_dict(
            [merged_dict(consistent_rows, {"numberOfPosts": initial_posts})]
        )

        # initial pull
        first_usage_df = request_all_usage_as_df(None, test_db_fixture)
        assert dataframe_row_count(first_usage_df) == 1
        assert db_row_count(test_db_fixture) == 1
        assert db_posts_by_name_date(test_db_fixture, name_date) == initial_posts

        # same student, with email updated
        mock_latest_usage_df.return_value = pd.DataFrame.from_dict(
            [merged_dict(consistent_rows, {"numberOfPosts": update_posts})]
        )

        # overwrite pull
        overwrite_usage_df = request_all_usage_as_df(None, test_db_fixture)
        assert dataframe_row_count(overwrite_usage_df) == 1
        assert db_row_count(test_db_fixture) == 1
        assert db_posts_by_name_date(test_db_fixture, name_date) == update_posts
