import collections
import logging
import os
import sys
from datetime import datetime
from typing import List

import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build, Resource
from google.oauth2 import service_account
from sqlalchemy import create_engine

from google_classroom_extractor.api.courses import request_all_courses_as_df
from google_classroom_extractor.api.coursework import request_all_coursework_as_df
from google_classroom_extractor.api.students import request_all_students_as_df
from google_classroom_extractor.api.submissions import request_all_submissions_as_df
from google_classroom_extractor.api.usage import request_all_usage_as_df


def get_sync_db_engine():
    return create_engine(os.getenv("SYNC_DATABASE_URI"))


def get_credentials() -> service_account.Credentials:
    scopes = [
        "https://www.googleapis.com/auth/admin.directory.orgunit",
        "https://www.googleapis.com/auth/admin.reports.usage.readonly",
        "https://www.googleapis.com/auth/classroom.courses",
        "https://www.googleapis.com/auth/classroom.coursework.students",
        "https://www.googleapis.com/auth/classroom.profile.emails",
        "https://www.googleapis.com/auth/classroom.rosters",
        "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
        "https://www.googleapis.com/auth/admin.reports.audit.readonly",
    ]

    filename = (
        "service-account.json"
        if os.path.exists("service-account.json")
        else "../service-account.json"
    )

    return service_account.Credentials.from_service_account_file(
        filename, scopes=scopes, subject=os.getenv("CLASSROOM_ACCOUNT")
    )


def normalized_submissions(
    courses_df: pd.DataFrame,
    coursework_df: pd.DataFrame,
    submissions_df: pd.DataFrame,
    students_df: pd.DataFrame,
) -> pd.DataFrame:
    logging.info("Normalizing submissions data")

    courses_df.rename(columns={"id": "courseId", "name": "courseName"}, inplace=True)
    courses_df = courses_df.astype("string")

    submissions_df.rename(
        columns={
            "id": "submissionId",
            "userId": "studentUserId",
            "state": "submissionState",
            "creationTime": "submissionCreationTime",
            "updateTime": "submissionUpdateTime",
        },
        inplace=True,
    )
    submissions_df.drop(
        columns=[
            "alternateLink",
            "assignmentSubmission.attachments",
            "submissionHistory",
        ],
        inplace=True,
    )

    course_submissions_df: pd.DataFrame = pd.merge(
        submissions_df,
        courses_df[["courseId", "courseName"]],
        on="courseId",
        how="left",
    )

    coursework_df.rename(
        columns={
            "id": "courseWorkId",
            "state": "courseWorkState",
            "title": "courseWorkTitle",
            "description": "courseWorkDescription",
            "creationTime": "courseWorkCreationTime",
            "updateTime": "courseWorkUpdateTime",
        },
        inplace=True,
    )
    coursework_df["courseWorkDueDate"] = coursework_df[
        ["dueDate.year", "dueDate.month", "dueDate.day"]
    ].agg("-".join, axis=1)
    coursework_df = coursework_df[
        [
            "courseWorkId",
            "courseWorkState",
            "courseWorkTitle",
            "courseWorkDescription",
            "courseWorkCreationTime",
            "courseWorkUpdateTime",
            "courseWorkDueDate",
        ]
    ]

    course_coursework_submissions_df: pd.DataFrame = pd.merge(
        course_submissions_df, coursework_df, on="courseWorkId", how="left"
    )

    students_df.rename(
        columns={
            "profile.name.fullName": "studentName",
            "profile.emailAddress": "studentEmail",
            "userId": "studentUserId",
        },
        inplace=True,
    )
    students_df = students_df[
        ["studentUserId", "courseId", "studentName", "studentEmail"]
    ]

    full_df: pd.DataFrame = pd.merge(
        course_coursework_submissions_df,
        students_df,
        on=["studentUserId", "courseId"],
        how="left",
    )

    full_df["importDate"] = datetime.today().strftime("%Y-%m-%d")

    return full_df


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

    sync_db = get_sync_db_engine()

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
