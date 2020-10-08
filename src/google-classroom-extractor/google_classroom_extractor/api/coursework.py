# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List, Dict, Optional, cast
import pandas as pd  # type: ignore
from sqlalchemy.engine.base import Engine as saEngine  # type: ignore
from googleapiclient.discovery import Resource  # type: ignore
from .api_caller import call_api, ResourceType


def request_coursework(
    resource: Optional[Resource], course_id: str
) -> List[Dict[str, str]]:
    assert isinstance(resource, Resource) or resource is None
    assert isinstance(course_id, str)

    if resource is None:
        return []

    return call_api(
        cast(ResourceType, resource).courses().courseWork().list,
        {"courseId": course_id},
        "courseWork",
    )


def request_latest_coursework_as_df(
    resource: Optional[Resource], course_ids: List[str]
) -> pd.DataFrame:
    assert isinstance(resource, Resource) or resource is None
    assert isinstance(course_ids, list)

    logging.info("Pulling coursework data")
    coursework: List[Dict[str, str]] = []
    for course_id in course_ids:
        coursework.extend(request_coursework(resource, course_id))
    return pd.json_normalize(coursework).astype("string")


def request_all_coursework_as_df(
    resource: Optional[Resource],
    course_ids: List[str],
    sync_db: saEngine,
) -> pd.DataFrame:
    assert isinstance(resource, Resource) or resource is None
    assert isinstance(course_ids, list)
    assert isinstance(sync_db, saEngine)

    coursework_df: pd.DataFrame = request_latest_coursework_as_df(resource, course_ids)

    # append everything from API call
    coursework_df.to_sql(
        "Coursework", sync_db, if_exists="append", index=False, chunksize=500
    )
    # remove duplicates - leave only the most recent
    with sync_db.connect() as con:
        con.execute(
            "DELETE from Coursework "
            "WHERE rowid not in (select max(rowid) "
            "FROM Coursework "
            "GROUP BY id)"
        )

    return coursework_df
