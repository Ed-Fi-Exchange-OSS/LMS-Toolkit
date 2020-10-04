# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from pathlib import Path
from unittest.mock import patch
import pandas as pd
from sqlalchemy import create_engine
from google_classroom_extractor.api.usage import request_all_usage_as_df

DB_FILE = "tests/api/usage/test_usage.db"


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


@patch("google_classroom_extractor.api.usage.request_latest_usage_as_df")
def test_overlap_removal(mock_latest_usage_df):
    Path(DB_FILE).unlink(missing_ok=True)
    test_db = create_engine(f"sqlite:///{DB_FILE}", echo=True)

    # 1st pull: 17 rows
    mock_latest_usage_df.return_value = pd.read_csv(
        "tests/api/usage/usage-1st.csv"
    )
    first_usage_df = request_all_usage_as_df(None, test_db)
    assert dataframe_row_count(first_usage_df) == 17
    assert db_row_count(test_db) == 17
    assert db_ending_email(test_db) == "luislopez@conrad-turner.com"

    # 2nd pull: 49 rows, overlaps 7
    mock_latest_usage_df.return_value = pd.read_csv(
        "tests/api/usage/usage-2nd-overlaps-1st.csv"
    )
    second_usage_df = request_all_usage_as_df(None, test_db)
    assert dataframe_row_count(second_usage_df) == 49
    assert db_row_count(test_db) == 59  # 49 new + 17 existing - 7 overlapping
    assert db_ending_email(test_db) == "xavierlopez@hotmail.com"

    # 3rd pull: 98 rows, overlaps 49
    mock_latest_usage_df.return_value = pd.read_csv(
        "tests/api/usage/usage-3rd-overlaps-1st-and-2nd.csv"
    )
    third_usage_df = request_all_usage_as_df(None, test_db)
    assert dataframe_row_count(third_usage_df) == 98
    assert db_row_count(test_db) == 99  # 98 new + 44 existing - 43 overlapping
    assert db_ending_email(test_db) == "petersstephen@yahoo.com"


@patch("google_classroom_extractor.api.usage.request_latest_usage_as_df")
def test_value_replacement(mock_latest_usage_df):
    Path(DB_FILE).unlink(missing_ok=True)
    test_db = create_engine(f"sqlite:///{DB_FILE}", echo=True)

    name_date = "april.vaughan 08/20"

    # original usage
    mock_latest_usage_df.return_value = pd.DataFrame(
        {
            "email": ["april.vaughan@yahoo.com"],
            "asOfDate": ["2020-09-03 00:36:50"],
            "importDate": ["2020-09-15 18:58:05"],
            "numberOfPosts": ["3"],
            "lastInteractionTime": ["2020-09-07 22:05:37"],
            "lastLoginTime": ["2020-09-07 22:05:37"],
            "name": ["april.vaughan"],
            "monthDay": ["08/20"],
            "nameDate": [name_date],
        }
    )

    # initial pull
    first_usage_df = request_all_usage_as_df(None, test_db)
    assert dataframe_row_count(first_usage_df) == 1
    assert db_row_count(test_db) == 1
    assert db_posts_by_name_date(test_db, name_date) == "3"

    # same student, with email updated
    mock_latest_usage_df.return_value = pd.DataFrame(
        {
            "email": ["april.vaughan@yahoo.com"],
            "asOfDate": ["2020-09-03 00:36:50"],
            "importDate": ["2020-09-15 18:58:05"],
            "numberOfPosts": ["5"],
            "lastInteractionTime": ["2020-09-07 22:05:37"],
            "lastLoginTime": ["2020-09-07 22:05:37"],
            "name": ["april.vaughan"],
            "monthDay": ["08/20"],
            "nameDate": [name_date],
        }
    )

    # overwrite pull
    overwrite_usage_df = request_all_usage_as_df(None, test_db)
    assert dataframe_row_count(overwrite_usage_df) == 1
    assert db_row_count(test_db) == 1
    assert db_posts_by_name_date(test_db, name_date) == "5"
