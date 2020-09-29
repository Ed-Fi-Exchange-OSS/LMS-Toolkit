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


def request_courses(resource: Optional[Resource]) -> List[Dict[str, str]]:
    assert isinstance(resource, Resource) or resource is None

    if resource is None:
        return []

    return call_api(
        resource.courses().list,  # type: ignore - courses() is dynamic
        {"courseStates": ["ACTIVE"]},  # type: ignore - due to tail_recursive decorator
        "courses",
    )


def request_latest_courses_as_df(resource: Optional[Resource]) -> pd.DataFrame:
    assert isinstance(resource, Resource) or resource is None

    logging.info("Pulling course data")
    courses: List[Dict[str, str]] = request_courses(resource)
    return pd.json_normalize(courses)


def request_all_courses_as_df(
    resource: Optional[Resource], sync_db: sqlalchemy.engine.base.Engine
) -> pd.DataFrame:
    assert isinstance(resource, Resource) or resource is None
    assert isinstance(sync_db, sqlalchemy.engine.base.Engine)

    courses_df = request_latest_courses_as_df(resource)

    # append everything from API call
    courses_df.to_sql(
        "Courses", sync_db, if_exists="append", index=False, chunksize=500
    )
    # remove duplicates - leave only the most recent
    with sync_db.connect() as con:
        con.execute(
            "DELETE from Courses "
            "WHERE rowid not in (select max(rowid) "
            "FROM Courses "
            "GROUP BY id)"
        )

    return courses_df
