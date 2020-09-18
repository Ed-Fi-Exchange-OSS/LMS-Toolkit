from typing import List, Dict
import pandas as pd
from .api_caller import call_api


def request_submissions(resource, course_id: str) -> List[Dict[str, str]]:
    return call_api(
        resource.courses().courseWork().studentSubmissions().list,
        {"courseId": course_id, "courseWorkId": "-"},
        "studentSubmissions",
    )


def request_submissions_as_df(resource, course_ids: List[str]) -> pd.DataFrame:
    submissions: List[Dict[str, str]] = []
    for course_id in course_ids:
        submissions.extend(request_submissions(resource, course_id))

    submissions_df: pd.DataFrame = pd.json_normalize(submissions).astype("string")
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
