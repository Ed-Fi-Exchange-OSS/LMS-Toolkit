# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


from datetime import datetime
import logging
import os
import sys

import pandas as pd  # type: ignore
from dotenv import load_dotenv
from googleapiclient.discovery import build, Resource  # type: ignore
from google.oauth2 import service_account  # type: ignore
from sqlalchemy.engine.base import Engine as saEngine  # type: ignore

from google_classroom_extractor.result import Result
from google_classroom_extractor.config import get_credentials, get_sync_db_engine
from google_classroom_extractor.request import request_all
from google_classroom_extractor.mapping.users import students_and_teachers_to_users_df
from google_classroom_extractor.mapping.sections import courses_to_sections_df
from google_classroom_extractor.csv_generation.write import (
    write_csv,
    USERS_ROOT_DIRECTORY,
    SECTIONS_ROOT_DIRECTORY,
)


def request():
    load_dotenv()
    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=os.environ.get("LOGLEVEL", "INFO"),
    )
    logging.getLogger("matplotlib").setLevel(logging.ERROR)
    logging.getLogger("opnieuw").setLevel(logging.DEBUG)

    credentials: service_account.Credentials = get_credentials()
    reports_resource: Resource = build(
        "admin", "reports_v1", credentials=credentials, cache_discovery=False
    )
    classroom_resource: Resource = build(
        "classroom", "v1", credentials=credentials, cache_discovery=False
    )

    sync_db: saEngine = get_sync_db_engine()

    return request_all(classroom_resource, reports_resource, sync_db)


if __name__ == "__main__":
    result_dfs: Result = request()

    logging.info("Writing API data to CSV files")
    with get_sync_db_engine().connect() as con:
        for table in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall():
            table_name = table[0]
            df = pd.read_sql(f"SELECT * FROM {table_name}", con)
            df.to_csv(f"{table_name.lower()}.csv", index=False)

    logging.info("Writing LMS UDM Users to CSV file")
    write_csv(
        students_and_teachers_to_users_df(
            result_dfs.students_df, result_dfs.teachers_df
        ),
        datetime.now(),
        USERS_ROOT_DIRECTORY,
    )

    logging.info("Writing LMS UDM Sections to CSV file")
    write_csv(
        courses_to_sections_df(result_dfs.courses_df),
        datetime.now(),
        SECTIONS_ROOT_DIRECTORY,
    )
