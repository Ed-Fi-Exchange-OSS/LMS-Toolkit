import pandas as pd
from .api_caller import call_api


def request_submissions(resource, course_id):
    return call_api(
        resource.courses().courseWork().studentSubmissions().list,
        {"courseId": course_id, "courseWorkId": "-"},
        "studentSubmissions",
    )


def submissions_dataframe(resource, course_ids):
    submissions = []
    for course_id in course_ids:
        submissions.extend(request_submissions(resource, course_id))

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
        columns=[
            "alternateLink",
            "assignmentSubmission.attachments",
            "submissionHistory",
        ],
        inplace=True,
    )

    return submissions_df
