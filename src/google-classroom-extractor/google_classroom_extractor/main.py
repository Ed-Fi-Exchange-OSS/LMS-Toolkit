# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import collections
import logging
import os
import sys
from typing import List

import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build, Resource
from google.oauth2 import service_account
import sqlalchemy

from google_classroom_extractor.config import get_credentials, get_sync_db_engine
from google_classroom_extractor.normalized import normalized_submissions

from google_classroom_extractor.api.courses import request_all_courses_as_df
from google_classroom_extractor.api.coursework import request_all_coursework_as_df
from google_classroom_extractor.api.students import request_all_students_as_df
from google_classroom_extractor.api.submissions import request_all_submissions_as_df
from google_classroom_extractor.api.usage import request_all_usage_as_df


def request():
    load_dotenv()
    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=os.environ.get("LOGLEVEL", "INFO"),
    )
    logging.getLogger("matplotlib").setLevel(logging.ERROR)
    logging.getLogger("opnieuw").setLevel(logging.DEBUG)

    credentials: service_account.Credentials = get_credentials()
    reports_resource: Resource = build(
        "admin", "reports_v1", credentials=credentials, cache_discovery=False
    )
    classroom_resource: Resource = build(
        "classroom", "v1", credentials=credentials, cache_discovery=False
    )

    sync_db: sqlalchemy.engine.base.Engine = get_sync_db_engine()

    courses_df: pd.DataFrame = request_all_courses_as_df(classroom_resource, sync_db)
    course_ids: List[str] = courses_df["id"].tolist()

    coursework_df: pd.DataFrame = request_all_coursework_as_df(
        classroom_resource, course_ids, sync_db
    )
    submissions_df: pd.DataFrame = request_all_submissions_as_df(
        classroom_resource, course_ids, sync_db
    )
    students_df: pd.DataFrame = request_all_students_as_df(
        classroom_resource, course_ids, sync_db
    )

    Result = collections.namedtuple(
        "Result",
        [
            "usage",
            "normalized_submissions",
            "courses",
            "coursework",
            "submissions",
            "students",
        ],
    )
    return Result(
        lambda: request_all_usage_as_df(reports_resource, sync_db),
        lambda: normalized_submissions(
            courses_df=courses_df,
            coursework_df=coursework_df,
            submissions_df=submissions_df,
            students_df=students_df,
        ),
        lambda: courses_df,
        lambda: coursework_df,
        lambda: submissions_df,
        lambda: students_df,
    )


if __name__ == "__main__":
    r = request()

    r.usage()
    r.courses()
    r.coursework()
    r.submissions()
    r.students()
    r.normalized_submissions()

    logging.info("Writing data to CSV files")
    with get_sync_db_engine().connect() as con:
        for table in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall():
            table_name = table[0]
            df = pd.read_sql(f"SELECT * FROM {table_name}", con)
            df.to_csv(f"{table_name.lower()}.csv", index=False)
