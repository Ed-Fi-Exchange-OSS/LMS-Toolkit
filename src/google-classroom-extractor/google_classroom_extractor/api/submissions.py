# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List, Dict, Optional
import pandas as pd
import sqlalchemy
from googleapiclient.discovery import Resource
from .api_caller import call_api


def request_submissions(
    resource: Optional[Resource], course_id: str
) -> List[Dict[str, str]]:
    assert isinstance(resource, Resource) or resource is None
    assert isinstance(course_id, str)

    if resource is None:
        return []

    return call_api(
        resource.courses().courseWork().studentSubmissions().list,  # type: ignore - courses() is dynamic
        {"courseId": course_id, "courseWorkId": "-"},  # type: ignore - due to tail_recursive decorator
        "studentSubmissions",
    )


def request_latest_submissions_as_df(
    resource: Optional[Resource], course_ids: List[str]
) -> pd.DataFrame:
    assert isinstance(resource, Resource) or resource is None
    assert isinstance(course_ids, list)

    logging.info("Pulling student submission data")
    submissions: List[Dict[str, str]] = []
    for course_id in course_ids:
        submissions.extend(request_submissions(resource, course_id))

    return pd.json_normalize(submissions).astype("string")


def request_all_submissions_as_df(
    resource: Optional[Resource],
    course_ids: List[str],
    sync_db: sqlalchemy.engine.base.Engine,
) -> pd.DataFrame:
    assert isinstance(resource, Resource) or resource is None
    assert isinstance(course_ids, list)
    assert isinstance(sync_db, sqlalchemy.engine.base.Engine)

    submissions_df: pd.DataFrame = request_latest_submissions_as_df(
        resource, course_ids
    )

    # append everything from API call
    submissions_df.to_sql(
        "StudentSubmissions", sync_db, if_exists="append", index=False, chunksize=500
    )
    # remove duplicates - leave only the most recent
    with sync_db.connect() as con:
        con.execute(
            "DELETE from StudentSubmissions "
            "WHERE rowid not in (select max(rowid) "
            "FROM StudentSubmissions "
            "GROUP BY id)"
        )

    return submissions_df
