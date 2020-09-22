import logging
from typing import List, Dict
import pandas as pd
from .api_caller import call_api


def request_courses(resource) -> List[Dict[str, str]]:
    # type: ignore
    return call_api(
        resource.courses().list,
        {"courseStates": ["ACTIVE"]}, # type: ignore
        "courses",
    )


def request_latest_courses_as_df(resource) -> pd.DataFrame:
    logging.info("Pulling course data")
    courses: List[Dict[str, str]] = request_courses(resource)
    return pd.json_normalize(courses)


def request_all_courses_as_df(resource, sync_db) -> pd.DataFrame:
    courses_df = request_latest_courses_as_df(resource)

    # append everything from API call
    courses_df.to_sql("Courses", sync_db, if_exists="append", index=False, chunksize=500)
    # remove duplicates - leave only the most recent
    with sync_db.connect() as con:
        con.execute(
            "DELETE from Courses "
            "WHERE rowid not in (select max(rowid) "
            "FROM Courses "
            "GROUP BY id)")

    return courses_df
