import collections
import logging
import os
import sys
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account


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


# TODO: handle 'PARTIAL_DATA_AVAILABLE' warning
# TODO: handle pagination
def request_usage(resource, date):
    return (
        resource.userUsageReport()
        .get(
            userKey="all",
            date=date,
            parameters="classroom:timestamp_last_interaction,classroom:num_posts_created,accounts:timestamp_last_login",
            pageToken=None,
        )
        .execute()
    )


# TODO: handle 'PARTIAL_DATA_AVAILABLE' warning
# TODO: handle pagination
def request_courses(resource):
    return resource.courses().list(courseStates=["ACTIVE"], pageToken=None).execute()


# TODO: handle 'PARTIAL_DATA_AVAILABLE' warning
# TODO: handle pagination
def request_students(resource, course_id):
    return (
        resource.courses().students().list(courseId=course_id, pageToken=None).execute()
    )


# TODO: handle 'PARTIAL_DATA_AVAILABLE' warning
# TODO: handle pagination
def request_submission(resource, course_id):
    return (
        resource.courses()
        .courseWork()
        .studentSubmissions()
        .list(courseId=course_id, courseWorkId="-", pageToken=None)
        .execute()
    )


def get_submissions(resource):
    logging.info("Pulling submissions data")

    courses = request_courses(resource)
    courses_df = pd.json_normalize(courses.get("courses", []))[["id", "name"]]
    courses_df.rename(columns={"id": "courseId", "name": "courseName"}, inplace=True)
    courses_df = courses_df.astype("string")

    submissions = []
    students = []
    for course_id in courses_df["courseId"]:
        submissions.extend(
            request_submission(resource, course_id).get("studentSubmissions", [])
        )
        students.extend(request_students(resource, course_id).get("students", []))

    submissions_df = pd.json_normalize(submissions).astype("string")

    course_submissions_df = pd.merge(
        submissions_df, courses_df, on="courseId", how="left"
    )

    students_df = pd.json_normalize(students).astype("string")

    # TODO - leave sub-json as objects to pluck out of - name in particular
    full_df = pd.merge(
        course_submissions_df, students_df, on=["userId", "courseId"], how="left"
    )
    full_df.rename(
        columns={"profile.name.fullName": "name", "profile.emailAddress": "email"},
        inplace=True,
    )
    full_df["importDate"] = datetime.today().strftime("%Y-%m-%d")
    full_df = full_df.astype(
        {
            "creationTime": "datetime64",
            "updateTime": "datetime64",
            "state": "string",
            "draftGrade": "string",
            "assignedGrade": "string",
            "courseName": "string",
            "name": "string",
            "email": "string",
            "importDate": "datetime64",
        }
    )
    return full_df[
        [
            "creationTime",
            "updateTime",
            "state",
            "draftGrade",
            "assignedGrade",
            "courseName",
            "name",
            "email",
            "importDate",
        ]
    ]


def get_usage(resource):
    logging.info("Pulling usage data")
    reports = []
    # pylint: disable=no-member
    for date in pd.date_range(
        start=os.getenv("START_DATE"), end=os.getenv("END_DATE")
    ).strftime("%Y-%m-%d"):
        single_result = request_usage(resource, date)
        reports.extend(single_result.get("usageReports", []))

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

    usage_df = pd.json_normalize(usage)
    usage_df = usage_df.astype(
        {
            "email": "string",
            "asOfDate": "datetime64",
            "importDate": "datetime64",
            "numberOfPosts": "int32",
            "lastInteractionTime": "datetime64",
            "lastLoginTime": "datetime64",
        }
    )

    # TODO: get this from join with student profile
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

    Result = collections.namedtuple("Result", ["usage", "submissions"])
    return Result(
        lambda: get_usage(reports_resource), lambda: get_submissions(classroom_resource)
    )


if __name__ == "__main__":
    r = request()

    r.usage().to_csv("usage.csv")
    logging.info("Usage data written to usage.csv")

    r.submissions().to_csv("submissions.csv")
    logging.info("Submissions data written to submissions.csv")
