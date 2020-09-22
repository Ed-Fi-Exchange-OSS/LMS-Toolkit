import logging
from typing import List, Dict
import pandas as pd
from .api_caller import call_api


def request_submissions(resource, course_id: str) -> List[Dict[str, str]]:
    return call_api(
        resource.courses().courseWork().studentSubmissions().list,
        {"courseId": course_id, "courseWorkId": "-"}, # type: ignore
        "studentSubmissions",
    )


def request_latest_submissions_as_df(resource, course_ids: List[str]) -> pd.DataFrame:
    logging.info("Pulling student submission data")
    submissions: List[Dict[str, str]] = []
    for course_id in course_ids:
        submissions.extend(request_submissions(resource, course_id))

    return pd.json_normalize(submissions).astype("string")


def request_all_submissions_as_df(resource, course_ids: List[str], sync_db) -> pd.DataFrame:
    submissions_df: pd.DataFrame = request_latest_submissions_as_df(resource, course_ids)

    # append everything from API call
    submissions_df.to_sql("StudentSubmissions", sync_db, if_exists="append", index=False, chunksize=500)
    # remove duplicates - leave only the most recent
    with sync_db.connect() as con:
        con.execute(
            "DELETE from StudentSubmissions "
            "WHERE rowid not in (select max(rowid) "
            "FROM StudentSubmissions "
            "GROUP BY id)")

    return submissions_df
