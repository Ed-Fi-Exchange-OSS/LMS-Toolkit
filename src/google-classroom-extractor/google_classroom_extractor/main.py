# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


from datetime import datetime
import logging
import os
import sys

from dotenv import load_dotenv
from googleapiclient.discovery import build, Resource
from google.oauth2 import service_account
import sqlalchemy

from google_classroom_extractor.result import Result
from google_classroom_extractor.config import get_credentials, get_sync_db_engine
from google_classroom_extractor.request import request_all
from google_classroom_extractor.mapping.users import students_and_teachers_to_users_df
from google_classroom_extractor.mapping.user_section_associations import students_and_teachers_to_user_section_associations_dfs
from google_classroom_extractor.mapping.sections import courses_to_sections_df
from google_classroom_extractor.mapping.assignments import coursework_to_assignments_dfs
from google_classroom_extractor.mapping.assignment_submissions import submissions_to_assignment_submissions_dfs
from google_classroom_extractor.mapping.user_submission_activities import submissions_to_user_submission_activities_dfs
from google_classroom_extractor.csv_generation.write import (
    write_csv,
    write_multi_csv,
    write_multi_tuple_csv,
    USERS_ROOT_DIRECTORY,
    SECTIONS_ROOT_DIRECTORY,
    SECTION_ASSOCIATIONS_ROOT_DIRECTORY,
    ASSIGNMENT_ROOT_DIRECTORY,
    SUBMISSION_ROOT_DIRECTORY,
    USER_ACTIVITY_ROOT_DIRECTORY,
)


def request() -> Result:
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

    sync_db: sqlalchemy.engine.base.Engine = get_sync_db_engine()

    return request_all(classroom_resource, reports_resource, sync_db)


if __name__ == "__main__":
    result_dfs: Result = request()

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

    logging.info("Writing LMS UDM UserSectionAssociations to CSV files")
    write_multi_csv(
        students_and_teachers_to_user_section_associations_dfs(result_dfs.students_df, result_dfs.teachers_df),
        datetime.now(),
        SECTION_ASSOCIATIONS_ROOT_DIRECTORY,
    )

    logging.info("Writing LMS UDM Assignments to CSV files")
    write_multi_csv(
        coursework_to_assignments_dfs(result_dfs.coursework_df),
        datetime.now(),
        ASSIGNMENT_ROOT_DIRECTORY,
    )

    logging.info("Writing LMS UDM AssignmentSubmissions to CSV files")
    write_multi_tuple_csv(
        submissions_to_assignment_submissions_dfs(result_dfs.submissions_df),
        datetime.now(),
        SUBMISSION_ROOT_DIRECTORY,
    )

    logging.info("Writing LMS UDM User Activities to CSV files")
    write_multi_csv(
        submissions_to_user_submission_activities_dfs(result_dfs.submissions_df),
        datetime.now(),
        USER_ACTIVITY_ROOT_DIRECTORY,
    )
