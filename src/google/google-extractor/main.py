import collections
import logging
import os
import sys
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

from api.courses import courses_dataframe
from api.coursework import coursework_dataframe
from api.students import students_dataframe
from api.submissions import submissions_dataframe
from api.usage import usage_dataframe


# returns google.auth.service_account.Credentials
def get_credentials():
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


def denormalized_submissions(courses_df, coursework_df, submissions_df, students_df):
    logging.info("Pulling submissions data")

    course_submissions_df = pd.merge(
        submissions_df, courses_df, on="courseId", how="left"
    )
    submissions_df = submissions_df.iloc[0:0]
    courses_df = courses_df.iloc[0:0]

    course_coursework_submissions_df = pd.merge(
        course_submissions_df, coursework_df, on="courseWorkId", how="left"
    )
    course_submissions_df = course_submissions_df.iloc[0:0]
    coursework_df = coursework_df.iloc[0:0]

    # TODO - leave sub-json as objects to pluck out of - name in particular
    full_df = pd.merge(
        course_coursework_submissions_df,
        students_df,
        on=["studentUserId", "courseId"],
        how="left",
    )
    course_coursework_submissions_df = course_coursework_submissions_df.iloc[0:0]
    students_df = students_df.iloc[0:0]

    full_df["importDate"] = datetime.today().strftime("%Y-%m-%d")

    return full_df


def request():
    load_dotenv()
    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        level=os.environ.get("LOGLEVEL", "INFO"),
    )
    logging.getLogger("matplotlib").setLevel(logging.ERROR)

    credentials = get_credentials()
    reports_resource = build(
        "admin", "reports_v1", credentials=credentials, cache_discovery=False
    )
    classroom_resource = build(
        "classroom", "v1", credentials=credentials, cache_discovery=False
    )

    courses_df = courses_dataframe(classroom_resource)
    course_ids = courses_df["courseId"]

    coursework_df = coursework_dataframe(classroom_resource, course_ids)
    submissions_df = submissions_dataframe(classroom_resource, course_ids)
    students_df = students_dataframe(classroom_resource, course_ids)

    Result = collections.namedtuple(
        "Result",
        [
            "usage",
            "denormalized_submissions",
            "courses",
            "coursework",
            "submissions",
            "students",
        ],
    )
    return Result(
        lambda: usage_dataframe(reports_resource),
        lambda: denormalized_submissions(
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

    r.usage().to_csv("usage.csv")
    logging.info("Usage data written to usage.csv")

    r.courses().to_csv("courses.csv")
    logging.info("Courses data written to courses.csv")

    r.coursework().to_csv("coursework.csv")
    logging.info("Coursework data written to coursework.csv")

    r.submissions().to_csv("submissions.csv")
    logging.info("Submissions data written to submissions.csv")

    r.students().to_csv("students.csv")
    logging.info("Students data written to students.csv")

    r.denormalized_submissions().to_csv("denormalized_submissions.csv")
    logging.info("Denormalized submissions data written to denormalized_submissions.csv")
