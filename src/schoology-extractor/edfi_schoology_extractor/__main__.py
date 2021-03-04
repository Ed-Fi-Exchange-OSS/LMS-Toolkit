# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import os
import sys
from typing import Dict, Optional

from dotenv import load_dotenv
from errorhandler import ErrorHandler
from pandas import DataFrame
import sqlalchemy

from edfi_schoology_extractor.helpers import csv_writer
from edfi_schoology_extractor.api.request_client import RequestClient
from edfi_schoology_extractor.helpers import arg_parser
from edfi_schoology_extractor.schoology_extract_facade import SchoologyExtractFacade
from edfi_schoology_extractor import usage_analytics_facade
import edfi_schoology_extractor.lms_filesystem as lms

from edfi_schoology_extractor.helpers.sync import get_sync_db_engine


# Load configuration
load_dotenv()

arguments = arg_parser.parse_main_arguments(sys.argv[1:])
# Parameters are validated in the parse_main_arguments function
schoology_key = arguments.client_key
schoology_secret = arguments.client_secret
schoology_output_path = arguments.output_directory
log_level = arguments.log_level
page_size = arguments.page_size
input_directory = arguments.input_directory

db_engine: sqlalchemy.engine.base.Engine
extractorFacade: SchoologyExtractFacade

logger: logging.Logger
error_tracker: ErrorHandler


def _configure_logging():
    global logger
    global error_tracker

    logger = logging.getLogger(__name__)

    level = os.environ.get("LOGLEVEL", "INFO")
    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=level,
    )
    error_tracker = ErrorHandler()


def _initialize():
    global extractorFacade, db_engine

    try:
        request_client: RequestClient = RequestClient(schoology_key, schoology_secret)
        db_engine = get_sync_db_engine()
        extractorFacade = SchoologyExtractFacade(request_client, page_size, db_engine)
    except BaseException as e:
        logger.critical(e)
        print(
            "A fatal error occurred, please review the log output for more information.",
            file=sys.stderr,
        )
        sys.exit(1)


def _create_file_from_dataframe(df: Optional[DataFrame], file_name) -> bool:
    logger.info(f"Exporting {file_name}")
    try:
        if df is not None:
            csv_writer.df_to_csv(df, file_name)
        else:
            csv_writer.df_to_csv(DataFrame(), file_name)

        return True
    except BaseException:
        logger.exception("An exception occurred while generating %s", file_name)
        return False


def _get_users() -> DataFrame:
    return extractorFacade.get_users()


# This variable facilitates temporary storage of output results from one GET
# request that need to be used for creating another GET request.
result_bucket: Dict[str, DataFrame] = {}


def _get_sections() -> DataFrame:
    sections_df: DataFrame = extractorFacade.get_sections()
    result_bucket["sections"] = sections_df
    return sections_df


def _get_assignments(section_id: int) -> Optional[DataFrame]:
    assignments_df: DataFrame = extractorFacade.get_assignments(section_id)
    result_bucket["assignments"] = assignments_df
    return assignments_df


def _get_section_activities(section_id: int) -> Optional[DataFrame]:
    section_activities_df: DataFrame = extractorFacade.get_section_activities(
        section_id
    )
    result_bucket["section_activities"] = section_activities_df

    return section_activities_df


def _get_submissions(assignment_id: int, section_id: int) -> Optional[DataFrame]:
    return extractorFacade.get_submissions(assignment_id, section_id)


def _get_section_associations(section_id: int) -> DataFrame:
    section_associations_df: DataFrame = extractorFacade.get_section_associations(
        section_id
    )
    result_bucket["section_associations"] = section_associations_df

    return section_associations_df


def _get_attendance_events(section_id: int) -> DataFrame:
    section_associations_df: DataFrame = result_bucket["section_associations"]
    attendance_events_df: DataFrame = extractorFacade.get_attendance_events(
        section_id, section_associations_df
    )

    return attendance_events_df


def _get_system_activities() -> DataFrame:
    return usage_analytics_facade.get_system_activities(input_directory, db_engine)


def main():
    _configure_logging()

    logger.info("Starting Ed-Fi LMS Schoology Extractor")
    _initialize()

    _create_file_from_dataframe(
        _get_users(), lms.get_user_file_path(schoology_output_path)
    )
    succeeded = _create_file_from_dataframe(
        _get_sections(), lms.get_section_file_path(schoology_output_path)
    )

    # Cannot proceed with section-related files if the sections extract did not
    # succeed.
    if not succeeded:
        logger.critical(
            "Unable to continue file generation because the load of Sections failed. Please review the log for more information."
        )
        sys.exit(1)

    for section_id in result_bucket["sections"]["SourceSystemIdentifier"].values:

        assignment_file_path: str = lms.get_assignment_file_path(
            schoology_output_path, section_id
        )
        succeeded: bool = _create_file_from_dataframe(
            _get_assignments(section_id), assignment_file_path
        )

        if succeeded:
            assignments_df: DataFrame = result_bucket["assignments"]

            if not assignments_df.empty:
                for assignment in assignments_df["SourceSystemIdentifier"].tolist():

                    assignment_id: int = int(assignment)
                    submission_file_name: str = lms.get_submissions_file_path(
                        schoology_output_path, section_id, assignment_id
                    )
                    _create_file_from_dataframe(
                        _get_submissions(assignment_id, section_id),
                        submission_file_name,
                    )

        section_activities_file_path: str = lms.get_section_activities_file_path(
            schoology_output_path, section_id
        )
        _create_file_from_dataframe(
            _get_section_activities(section_id), section_activities_file_path
        )

        file_path: str = lms.get_section_association_file_path(
            schoology_output_path, section_id
        )
        succeeded: bool = _create_file_from_dataframe(
            _get_section_associations(section_id), file_path
        )

        file_path: str = lms.get_attendance_events_file_path(
            schoology_output_path, section_id
        )
        _create_file_from_dataframe(_get_attendance_events(section_id), file_path)

    need_to_process_input_files: bool = input_directory is not None
    if need_to_process_input_files:
        system_activities_output_dir: str = lms.get_system_activities_file_path(
            schoology_output_path
        )
        _create_file_from_dataframe(
            _get_system_activities(), system_activities_output_dir
        )

    logger.info("Finishing Ed-Fi LMS Schoology Extractor")

    if error_tracker.fired:
        print(
            "A fatal error occurred, please review the log output for more information.",
            file=sys.stderr,
        )
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
