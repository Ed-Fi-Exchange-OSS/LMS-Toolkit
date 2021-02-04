# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


from datetime import datetime
import logging
import sys
from typing import Optional

from dotenv import load_dotenv
from googleapiclient.discovery import build, Resource
from google.oauth2 import service_account
import sqlalchemy
from errorhandler import ErrorHandler

from edfi_google_classroom_extractor.result import Result
from edfi_google_classroom_extractor.config import get_credentials, get_sync_db_engine
from edfi_google_classroom_extractor.request import request_all
from edfi_google_classroom_extractor.mapping.users import students_and_teachers_to_users_df
from edfi_google_classroom_extractor.mapping.user_section_associations import (
    students_and_teachers_to_user_section_associations_dfs,
)
from edfi_google_classroom_extractor.mapping.sections import courses_to_sections_df
from edfi_google_classroom_extractor.mapping.assignments import coursework_to_assignments_dfs
from edfi_google_classroom_extractor.mapping.assignment_submissions import (
    submissions_to_assignment_submissions_dfs,
)
from edfi_google_classroom_extractor.mapping.user_submission_activities import (
    submissions_to_user_submission_activities_dfs,
)
from edfi_lms_extractor_lib.csv_generation.write import (
    write_users,
    write_sections,
    write_section_associations,
    write_assignments,
    write_user_activities,
    write_assignment_submissions,
)
from edfi_google_classroom_extractor.helpers import arg_parser

logger: logging.Logger
error_tracker: ErrorHandler

classroom_account: str = ""
log_level: str = ""
output_directory: str = ""
usage_start_date: str = ""
usage_end_date: str = ""


def parse_args():
    arguments = arg_parser.parse_main_arguments(sys.argv[1:])
    global classroom_account
    global log_level
    global output_directory
    global usage_start_date
    global usage_end_date

    classroom_account = arguments.classroom_account
    log_level = arguments.log_level
    output_directory = arguments.output_directory
    usage_start_date = arguments.usage_start_date
    usage_end_date = arguments.usage_end_date


def configure_logging():
    global logger
    global error_tracker

    logger = logging.getLogger(__name__)

    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=log_level,
    )
    error_tracker = ErrorHandler()


def request() -> Optional[Result]:
    try:
        credentials: service_account.Credentials = get_credentials(classroom_account)
        reports_resource: Resource = build(
            "admin", "reports_v1", credentials=credentials, cache_discovery=False
        )
        classroom_resource: Resource = build(
            "classroom", "v1", credentials=credentials, cache_discovery=False
        )

        sync_db: sqlalchemy.engine.base.Engine = get_sync_db_engine()

        return request_all(
            classroom_resource,
            reports_resource,
            sync_db,
            usage_start_date,
            usage_end_date,
        )
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
    write_users(
        students_and_teachers_to_users_df(
            result_dfs.students_df, result_dfs.teachers_df
        ),
        datetime.now(),
        output_directory,
    )

    logger.info("Writing LMS UDM Sections to CSV file")
    write_sections(
        courses_to_sections_df(result_dfs.courses_df),
        datetime.now(),
        output_directory,
    )

    logger.info("Writing LMS UDM UserSectionAssociations to CSV files")
    write_section_associations(
        students_and_teachers_to_user_section_associations_dfs(
            result_dfs.students_df, result_dfs.teachers_df
        ),
        datetime.now(),
        output_directory,
    )

    logger.info("Writing LMS UDM Assignments to CSV files")
    write_assignments(
        coursework_to_assignments_dfs(result_dfs.coursework_df),
        datetime.now(),
        output_directory,
    )

    logger.info("Writing LMS UDM AssignmentSubmissions to CSV files")
    write_assignment_submissions(
        submissions_to_assignment_submissions_dfs(result_dfs.submissions_df),
        datetime.now(),
        output_directory,
    )

    logger.info("Writing LMS UDM User Activities to CSV files")
    write_user_activities(
        submissions_to_user_submission_activities_dfs(result_dfs.submissions_df),
        datetime.now(),
        output_directory,
    )

    logger.info("Finishing Ed-Fi LMS Google Classroom Extractor")

    if error_tracker.fired:
        print(
            "A fatal error occurred, please review the log output for more information.",
            file=sys.stderr,
        )
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    load_dotenv()
    parse_args()
    configure_logging()
    main()
