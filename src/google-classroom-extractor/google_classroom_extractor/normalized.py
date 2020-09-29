# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from datetime import datetime
import pandas as pd


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
