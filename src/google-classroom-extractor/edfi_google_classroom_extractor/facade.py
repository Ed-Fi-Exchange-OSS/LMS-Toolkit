# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import logging
from typing import Optional

from googleapiclient.discovery import build, Resource
from google.oauth2 import service_account
from pandas import DataFrame
import sqlalchemy


from edfi_google_classroom_extractor.helpers.arg_parser import MainArguments
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
    write_grades,
    write_users,
    write_sections,
    write_section_associations,
    write_section_activities,
    write_assignments,
    write_user_activities,
    write_assignment_submissions,
    write_system_activities,
)


logger = logging.getLogger(__name__)


def request(arguments: MainArguments) -> Optional[Result]:
    try:
        credentials: service_account.Credentials = get_credentials(arguments.classroom_account)
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
            arguments.usage_start_date,
            arguments.usage_end_date,
        )
    except Exception:
        logger.exception("An exception occurred while connecting to the API")
        return None


def run(arguments: MainArguments):

    logger.info("Starting Ed-Fi LMS Google Classroom Extractor")
    result_dfs: Optional[Result] = request(arguments)

    if not result_dfs:
        # Enrich this in LMS-150
        return

    now = datetime.now()

    logger.info("Writing LMS UDM Users to CSV file")
    write_users(
        students_and_teachers_to_users_df(
            result_dfs.students_df, result_dfs.teachers_df
        ),
        now,
        arguments.output_directory,
    )

    logger.info("Writing LMS UDM Sections to CSV file")
    (sections_df, all_section_ids) = courses_to_sections_df(result_dfs.courses_df)
    write_sections(
        sections_df,
        now,
        arguments.output_directory,
    )

    logger.info("Writing LMS UDM UserSectionAssociations to CSV files")
    write_section_associations(
        students_and_teachers_to_user_section_associations_dfs(
            result_dfs.students_df, result_dfs.teachers_df
        ),
        all_section_ids,
        now,
        arguments.output_directory,
    )

    logger.info("Writing LMS UDM Assignments to CSV files")
    write_assignments(
        coursework_to_assignments_dfs(result_dfs.coursework_df),
        all_section_ids,
        now,
        arguments.output_directory,
    )

    logger.info("Writing LMS UDM AssignmentSubmissions to CSV files")
    write_assignment_submissions(
        submissions_to_assignment_submissions_dfs(result_dfs.submissions_df),
        now,
        arguments.output_directory,
    )

    logger.info("Writing LMS UDM User Activities to CSV files")
    write_user_activities(
        submissions_to_user_submission_activities_dfs(result_dfs.submissions_df),
        all_section_ids,
        now,
        arguments.output_directory,
    )

    logger.info("Writing empty LMS UDM Grades to CSV files")
    write_grades(
        dict(),
        all_section_ids,
        now,
        arguments.output_directory,
    )

    logger.info("Writing empty LMS UDM SectionActivities to CSV files")
    write_section_activities(
        dict(),
        all_section_ids,
        now,
        arguments.output_directory,
    )

    logger.info("Writing empty LMS UDM SystemActivities to CSV file")
    write_system_activities(
        DataFrame(),
        now,
        arguments.output_directory,
    )

    logger.info("Finishing Ed-Fi LMS Google Classroom Extractor")
