import pandas as pd
from .api_caller import call_api


def request_courses(resource):
    return call_api(
        resource.courses().list,
        {"courseStates": ["ACTIVE"]},
        "courses",
    )


def courses_dataframe(resource):
    courses = request_courses(resource)
    courses_df = pd.json_normalize(courses)[["id", "name"]]
    courses_df.rename(columns={"id": "courseId", "name": "courseName"}, inplace=True)
    courses_df = courses_df.astype("string")

    return courses_df