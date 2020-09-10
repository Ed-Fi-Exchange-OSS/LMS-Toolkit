import collections
import logging
import os
import sys
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from opnieuw import retry
from tail_recursive import tail_recursive
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


@retry(
    retry_on_exceptions=(Exception),
    max_calls_total=4,
    retry_window_after_first_call_in_seconds=60,
)
def execute(executable_resource):
    return executable_resource.execute()


# resource_method is the get/list SDK function to call,
# resource_parameters is the parameters for get/list
# response_property is the property in the response json we want
# results is the result accumulated across pages
@tail_recursive
def request_execution(
    resource_method, resource_parameters, response_property, results=None
):
    """Execute a Google Classroom/Admin SDK API request

    Parameters
    ----------
    resource_method: function
        is the get/list SDK function to call
    resource_parameters: dict
        is the parameters for get/list
    response_property: string
        is the property in the API response we want
    results: list
        is the list of dicts of the API response accumulated across pages

    Returns
    -------
    list
        a list of dicts of the API response property requested
    """
    if results is None:
        results = []
    response = execute(resource_method(**resource_parameters))
    results.extend(response.get(response_property, []))
    next_page_token = response.get("nextPageToken", None)
    if not next_page_token:
        return results
    resource_parameters["pageToken"] = next_page_token
    return request_execution.tail_call(
        resource_method, resource_parameters, response_property, results
    )


def request_usage(resource, date):
    return request_execution(
        resource.userUsageReport().get,
        {
            "userKey": "all",
            "date": date,
            "parameters": "classroom:timestamp_last_interaction,classroom:num_posts_created,accounts:timestamp_last_login",
        },
        "usageReports",
    )


def request_courses(resource):
    return request_execution(
        resource.courses().list,
        {"courseStates": ["ACTIVE"]},
        "courses",
    )


def request_coursework(resource, course_id):
    return request_execution(
        resource.courses().courseWork().list,
        {"courseId": course_id},
        "courseWork",
    )


def request_students(resource, course_id):
    return request_execution(
        resource.courses().students().list,
        {"courseId": course_id},
        "students",
    )


def request_submission(resource, course_id):
    return request_execution(
        resource.courses().courseWork().studentSubmissions().list,
        {"courseId": course_id, "courseWorkId": "-"},
        "studentSubmissions",
    )


def get_submissions(resource):
    logging.info("Pulling submissions data")

    courses = request_courses(resource)
    courses_df = pd.json_normalize(courses)[["id", "name"]]
    courses_df.rename(columns={"id": "courseId", "name": "courseName"}, inplace=True)
    courses_df = courses_df.astype("string")

    submissions = []
    students = []
    coursework = []
    for course_id in courses_df["courseId"]:
        submissions.extend(request_submission(resource, course_id))
        students.extend(request_students(resource, course_id))
        coursework.extend(request_coursework(resource, course_id))

    submissions_df = pd.json_normalize(submissions).astype("string")
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
        columns=["alternateLink", "assignmentSubmission.attachments", "submissionHistory"], inplace=True
    )

    course_submissions_df = pd.merge(
        submissions_df, courses_df, on="courseId", how="left"
    )
    submissions_df = submissions_df.iloc[0:0]
    courses_df = courses_df.iloc[0:0]

    coursework_df = pd.json_normalize(coursework).astype("string")
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
    coursework_df[
        "courseWorkDueDate"
    ] = coursework_df[["dueDate.year", "dueDate.month", "dueDate.day"]].agg('-'.join, axis=1)
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

    course_coursework_submissions_df = pd.merge(
        course_submissions_df, coursework_df, on="courseWorkId", how="left"
    )
    course_submissions_df = course_submissions_df.iloc[0:0]
    coursework_df = coursework_df.iloc[0:0]

    students_df = pd.json_normalize(students).astype("string")
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

    Result = collections.namedtuple("Result", ["usage", "submissions"])
    return Result(
        lambda: get_usage(reports_resource), lambda: get_submissions(classroom_resource)
    )


if __name__ == "__main__":
    r = request()

    # r.usage().to_csv("usage.csv")
    # logging.info("Usage data written to usage.csv")

    r.submissions().to_csv("submissions.csv")
    logging.info("Submissions data written to submissions.csv")
