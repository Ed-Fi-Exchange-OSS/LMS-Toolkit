from pathlib import Path
from unittest.mock import patch
import pandas as pd
from sqlalchemy import create_engine
from google_classroom_extractor.api.coursework import request_all_coursework_as_df

DB_FILE = "tests/coursework/test_coursework.db"


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


@patch("google_classroom_extractor.api.coursework.request_latest_coursework_as_df")
def test_overlap_removal(mock_latest_coursework_df):
    Path(DB_FILE).unlink(missing_ok=True)
    test_db = create_engine(f"sqlite:///{DB_FILE}", echo=True)

    # 1st pull: 17 rows, last row id is 87699559
    mock_latest_coursework_df.return_value = pd.read_csv(
        "tests/coursework/coursework-1st.csv"
    )
    first_coursework_df = request_all_coursework_as_df(None, DUMMY_COURSE_IDS, test_db)
    assert dataframe_row_count(first_coursework_df) == 17
    assert db_row_count(test_db) == 17
    assert db_ending_id(test_db) == 87699559

    # 2nd pull: 39 rows, overlaps 7, last row id is 87025291
    mock_latest_coursework_df.return_value = pd.read_csv(
        "tests/coursework/coursework-2nd-overlaps-1st.csv"
    )
    second_coursework_df = request_all_coursework_as_df(None, DUMMY_COURSE_IDS, test_db)
    assert dataframe_row_count(second_coursework_df) == 39
    assert db_row_count(test_db) == 44  # 39 new + 12 existing - 7 overlapping
    assert db_ending_id(test_db) == 87025291

    # 3rd pull: 98 rows, overlaps 43, last row id is 15461200
    mock_latest_coursework_df.return_value = pd.read_csv(
        "tests/coursework/coursework-3rd-overlaps-1st-and-2nd.csv"
    )
    third_coursework_df = request_all_coursework_as_df(None, DUMMY_COURSE_IDS, test_db)
    assert dataframe_row_count(third_coursework_df) == 98
    assert db_row_count(test_db) == 99  # 98 new + 44 existing - 43 overlapping
    assert db_ending_id(test_db) == 15461200


@patch("google_classroom_extractor.api.coursework.request_latest_coursework_as_df")
def test_value_replacement(mock_latest_coursework_df):
    Path(DB_FILE).unlink(missing_ok=True)
    test_db = create_engine(f"sqlite:///{DB_FILE}", echo=True)

    # original coursework
    coursework_id = "1234"
    mock_latest_coursework_df.return_value = pd.DataFrame(
        {
            "courseId": ["1234"],
            "id": [coursework_id],
            "title": ["Customer-focused eco-centric standardization"],
            "description": ["Herself PM out far really beautiful."],
            "state": ["CREATED"],
            "creationTime": ["2020-01-12 03:52:52"],
            "updateTime": ["2020-09-20 12:37:54"],
            "dueDate": ["2020-09-11"],
            "dueTime": ["22:47:58"],
            "scheduledTime": ["23:23:01"],
            "maxPoints": ["75"],
            "workType": ["ASSIGNMENT"],
            "creatorUserId": ["49165122"],
            "topicId": ["81859357"],
        }
    )

    # initial pull
    first_coursework_df = request_all_coursework_as_df(None, DUMMY_COURSE_IDS, test_db)
    assert dataframe_row_count(first_coursework_df) == 1
    assert db_row_count(test_db) == 1
    assert db_state_by_coursework_id(test_db, coursework_id) == "CREATED"

    # same coursework, with state updated
    mock_latest_coursework_df.return_value = pd.DataFrame(
        {
            "courseId": ["1234"],
            "id": [coursework_id],
            "title": ["Customer-focused eco-centric standardization"],
            "description": ["Herself PM out far really beautiful."],
            "state": ["PUBLISHED"],
            "creationTime": ["2020-01-12 03:52:52"],
            "updateTime": ["2020-09-20 12:37:54"],
            "dueDate": ["2020-09-11"],
            "dueTime": ["22:47:58"],
            "scheduledTime": ["23:23:01"],
            "maxPoints": ["75"],
            "workType": ["ASSIGNMENT"],
            "creatorUserId": ["49165122"],
            "topicId": ["81859357"],
        }
    )

    # overwrite pull
    overwrite_coursework_df = request_all_coursework_as_df(None, DUMMY_COURSE_IDS, test_db)
    assert dataframe_row_count(overwrite_coursework_df) == 1
    assert db_row_count(test_db) == 1
    assert db_state_by_coursework_id(test_db, coursework_id) == "PUBLISHED"
