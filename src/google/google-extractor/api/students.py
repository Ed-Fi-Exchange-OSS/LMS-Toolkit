import pandas as pd
from .api_caller import call_api


def request_students(resource, course_id):
    return call_api(
        resource.courses().students().list,
        {"courseId": course_id},
        "students",
    )


def students_dataframe(resource, course_ids):
    students = []
    for course_id in course_ids:
        students.extend(request_students(resource, course_id))

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

    return students_df
