import collections
import logging
import os
import sys

from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

from lib.courses import courses_dataframe
from lib.coursework import coursework_dataframe
from lib.students import students_dataframe
from lib.submissions import submissions_dataframe
from lib.usage import request_usage


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


def get_submissions(resource):
    logging.info("Pulling submissions data")

    courses_df = courses_dataframe(resource)
    course_ids = courses_df["courseId"]

    coursework_df = coursework_dataframe(resource, course_ids)
    submissions_df = submissions_dataframe(resource, course_ids)
    students_df = submissions_dataframe(resource, course_ids)

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


def get_usage(resource):
    logging.info("Pulling usage data")
    reports = []
    # pylint: disable=no-member
    for date in pd.date_range(
        start=os.getenv("START_DATE"), end=os.getenv("END_DATE")
    ).strftime("%Y-%m-%d"):
        reports.extend(request_usage(resource, date))

    usage = []
    for response in reports:
        row = {}
        row["email"] = response.get("entity").get("userEmail")
        row["asOfDate"] = response.get("date")
        row["importDate"] = datetime.today().strftime("%Y-%m-%d")

        for parameter in response.get("parameters"):
            if parameter.get("name") == "classroom:num_posts_created":
                row["numberOfPosts"] = parameter.get("intValue")

            if parameter.get("name") == "classroom:last_interaction_time":
                row["lastInteractionTime"] = parameter.get("datetimeValue")

            if parameter.get("name") == "accounts:last_login_time":
                row["lastLoginTime"] = parameter.get("datetimeValue")
        usage.append(row)

    usage_df = pd.json_normalize(usage).astype(
        {
            "email": "string",
            "asOfDate": "datetime64",
            "importDate": "datetime64",
            "numberOfPosts": "int32",
            "lastInteractionTime": "datetime64",
            "lastLoginTime": "datetime64",
        }
    )

    # TODO: get this from a join with student profile
    usage_df["name"] = usage_df["email"].str.split("@").str[0]

    usage_df["monthDay"] = usage_df["asOfDate"].dt.strftime("%m/%d")
    usage_df["nameDate"] = usage_df["name"] + " " + usage_df["monthDay"]
    return usage_df


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

    Result = collections.namedtuple(
        "Result", ["usage", "submissions"]
    )
    return Result(
        lambda: get_usage(reports_resource), lambda: get_submissions(classroom_resource)
    )


if __name__ == "__main__":
    r = request()

    r.usage().to_csv("usage.csv")
    logging.info("Usage data written to usage.csv")

    r.submissions().to_csv("submissions.csv")
    logging.info("Submissions data written to submissions.csv")
