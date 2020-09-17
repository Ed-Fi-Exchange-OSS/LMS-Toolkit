import pandas as pd
from .api_caller import call_api


def request_coursework(resource, course_id):
    return call_api(
        resource.courses().courseWork().list,
        {"courseId": course_id},
        "courseWork",
    )


def coursework_dataframe(resource, course_ids):
    coursework = []
    for course_id in course_ids:
        coursework.extend(request_coursework(resource, course_id))

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

    return coursework_df
