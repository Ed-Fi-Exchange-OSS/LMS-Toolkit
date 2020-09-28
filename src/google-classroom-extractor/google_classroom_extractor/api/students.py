# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List, Dict
import pandas as pd
from .api_caller import call_api


def request_students(resource, course_id: str) -> List[Dict[str, str]]:
    return call_api(
        resource.courses().students().list,
        {"courseId": course_id},  # type: ignore
        "students",
    )


def request_latest_students_as_df(resource, course_ids: List[str]) -> pd.DataFrame:
    logging.info("Pulling student data")
    students: List[Dict[str, str]] = []
    for course_id in course_ids:
        students.extend(request_students(resource, course_id))

    return pd.json_normalize(students).astype("string")


def request_all_students_as_df(resource, course_ids: List[str], sync_db) -> pd.DataFrame:
    students_df: pd.DataFrame = request_latest_students_as_df(resource, course_ids)

    # append everything from API call
    students_df.to_sql(
        "Students", sync_db, if_exists="append", index=False, chunksize=500
    )
    # remove duplicates - leave only the most recent
    with sync_db.connect() as con:
        con.execute(
            "DELETE from Students "
            "WHERE rowid not in (select max(rowid) "
            "FROM Students "
            "GROUP BY courseId, userId)"
        )

    return students_df
