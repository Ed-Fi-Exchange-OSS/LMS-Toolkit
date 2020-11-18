# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


from datetime import datetime
import logging
import os
import sys
from typing import Optional

from dotenv import load_dotenv
from googleapiclient.discovery import build, Resource
from google.oauth2 import service_account
import sqlalchemy

from google_classroom_extractor.result import Result
from google_classroom_extractor.config import get_credentials, get_sync_db_engine
from google_classroom_extractor.request import request_all
from google_classroom_extractor.mapping.users import students_and_teachers_to_users_df
from google_classroom_extractor.mapping.user_section_associations import (
    students_and_teachers_to_user_section_associations_dfs,
)
from google_classroom_extractor.mapping.sections import courses_to_sections_df
from google_classroom_extractor.mapping.assignments import coursework_to_assignments_dfs
from google_classroom_extractor.mapping.assignment_submissions import (
    submissions_to_assignment_submissions_dfs,
)
from google_classroom_extractor.mapping.user_submission_activities import (
    submissions_to_user_submission_activities_dfs,
)
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

logger: logging.Logger


def configure_logging():
    global logger

    logger = logging.getLogger(__name__)

    level = os.environ.get("LOGLEVEL", "INFO")
    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=level,
    )


def request() -> Optional[Result]:
    try:
        credentials: service_account.Credentials = get_credentials()
        reports_resource: Resource = build(
            "admin", "reports_v1", credentials=credentials, cache_discovery=False
        )
        classroom_resource: Resource = build(
            "classroom", "v1", credentials=credentials, cache_discovery=False
        )

        sync_db: sqlalchemy.engine.base.Engine = get_sync_db_engine()

        return request_all(classroom_resource, reports_resource, sync_db)
    except Exception:
        logger.exception("An exception occurred while connecting to the API")
        return None


def main():
    logger.info("Starting Ed-Fi LMS Google Classroom Extractor")
    result_dfs: Optional[Result] = request()

    if not result_dfs:
        # Enrich this in FIZZ-150
        return

    logger.info("Writing LMS UDM Users to CSV file")
    write_csv(
        students_and_teachers_to_users_df(
            result_dfs.students_df, result_dfs.teachers_df
        ),
        datetime.now(),
        USERS_ROOT_DIRECTORY,
    )

    logger.info("Writing LMS UDM Sections to CSV file")
    write_csv(
        courses_to_sections_df(result_dfs.courses_df),
        datetime.now(),
        SECTIONS_ROOT_DIRECTORY,
    )

    logger.info("Writing LMS UDM UserSectionAssociations to CSV files")
    write_multi_csv(
        students_and_teachers_to_user_section_associations_dfs(
            result_dfs.students_df, result_dfs.teachers_df
        ),
        datetime.now(),
        SECTION_ASSOCIATIONS_ROOT_DIRECTORY,
    )

    logger.info("Writing LMS UDM Assignments to CSV files")
    write_multi_csv(
        coursework_to_assignments_dfs(result_dfs.coursework_df),
        datetime.now(),
        ASSIGNMENT_ROOT_DIRECTORY,
    )

    logger.info("Writing LMS UDM AssignmentSubmissions to CSV files")
    write_multi_tuple_csv(
        submissions_to_assignment_submissions_dfs(result_dfs.submissions_df),
        datetime.now(),
        SUBMISSION_ROOT_DIRECTORY,
    )

    logger.info("Writing LMS UDM User Activities to CSV files")
    write_multi_csv(
        submissions_to_user_submission_activities_dfs(result_dfs.submissions_df),
        datetime.now(),
        USER_ACTIVITY_ROOT_DIRECTORY,
    )

    logger.info("Finishing Ed-Fi LMS Google Classroom Extractor")


if __name__ == "__main__":
    load_dotenv()
    configure_logging()
    main()
