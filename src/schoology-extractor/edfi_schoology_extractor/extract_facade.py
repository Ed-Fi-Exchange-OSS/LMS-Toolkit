# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import os
import sys
from typing import Dict, Optional, Tuple

from pandas import DataFrame
import sqlalchemy

from edfi_schoology_extractor.helpers.arg_parser import MainArguments
from edfi_schoology_extractor.api.request_client import RequestClient
from edfi_schoology_extractor.helpers import csv_writer
from edfi_schoology_extractor import usage_analytics_facade
import edfi_schoology_extractor.lms_filesystem as lms
from edfi_schoology_extractor.helpers.sync import get_sync_db_engine
from edfi_schoology_extractor.client_facade import SchoologyExtractFacade

logger = logging.getLogger(__name__)


def _initialize(arguments: MainArguments) -> Tuple[SchoologyExtractFacade, sqlalchemy.engine.base.Engine]:
    global logger

    try:
        request_client: RequestClient = RequestClient(arguments.client_key, arguments.client_secret)
        db_engine = get_sync_db_engine(arguments.sync_database_directory)

        facade = SchoologyExtractFacade(request_client, arguments.page_size, db_engine)

        return facade, db_engine
    except BaseException as e:
        logger.critical(e)
        print(
            "A fatal error occurred, please review the log output for more information.",
            file=sys.stderr,
        )
        sys.exit(1)


def _create_file_from_dataframe(df: Optional[DataFrame], file_name) -> bool:
    global logger

    normalized_file_name = os.path.normpath(file_name)
    logger.info(f"Exporting {normalized_file_name}")
    try:
        if df is not None:
            csv_writer.df_to_csv(df, normalized_file_name)
        else:
            csv_writer.df_to_csv(DataFrame(), normalized_file_name)

        return True
    except BaseException:
        logger.exception(
            "An exception occurred while generating %s", normalized_file_name
        )
        return False


def _get_users(extractorFacade: SchoologyExtractFacade) -> DataFrame:
    return extractorFacade.get_users()


# This variable facilitates temporary storage of output results from one GET
# request that need to be used for creating another GET request.
result_bucket: Dict[str, DataFrame] = {}


def _get_sections(extractorFacade: SchoologyExtractFacade) -> DataFrame:
    sections_df: DataFrame = extractorFacade.get_sections()
    result_bucket["sections"] = sections_df
    return sections_df


def _get_assignments(extractorFacade: SchoologyExtractFacade, section_id: int) -> Optional[DataFrame]:
    assignments_df: DataFrame = extractorFacade.get_assignments(section_id)
    result_bucket["assignments"] = assignments_df
    return assignments_df


def _get_section_activities(extractorFacade: SchoologyExtractFacade, section_id: int) -> Optional[DataFrame]:
    section_activities_df: DataFrame = extractorFacade.get_section_activities(
        section_id
    )
    result_bucket["section_activities"] = section_activities_df

    return section_activities_df


def _get_submissions(extractorFacade: SchoologyExtractFacade, assignment_id: int, section_id: int) -> Optional[DataFrame]:
    return extractorFacade.get_submissions(assignment_id, section_id)


def _get_section_associations(extractorFacade: SchoologyExtractFacade, section_id: int) -> DataFrame:
    section_associations_df: DataFrame = extractorFacade.get_section_associations(
        section_id
    )
    result_bucket["section_associations"] = section_associations_df

    return section_associations_df


def _get_attendance_events(extractorFacade: SchoologyExtractFacade, section_id: int) -> DataFrame:
    section_associations_df: DataFrame = result_bucket["section_associations"]
    attendance_events_df: DataFrame = extractorFacade.get_attendance_events(
        section_id, section_associations_df
    )

    return attendance_events_df


def _get_system_activities(input_directory: str, db_engine: sqlalchemy.engine.base.Engine) -> DataFrame:
    return usage_analytics_facade.get_system_activities(input_directory, db_engine)


def run(arguments: MainArguments) -> None:
    logger.info("Starting Ed-Fi LMS Schoology Extractor")
    facade, db_engine = _initialize(arguments)

    _create_file_from_dataframe(
        _get_users(facade), lms.get_user_file_path(arguments.output_directory)
    )
    succeeded = _create_file_from_dataframe(
        _get_sections(facade), lms.get_section_file_path(arguments.output_directory)
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
            arguments.output_directory, section_id
        )
        succeeded = _create_file_from_dataframe(
            _get_assignments(facade, section_id), assignment_file_path
        )

        if succeeded:
            assignments_df: DataFrame = result_bucket["assignments"]

            if not assignments_df.empty:
                for assignment in assignments_df["SourceSystemIdentifier"].tolist():

                    assignment_id: int = int(assignment)
                    submission_file_name: str = lms.get_submissions_file_path(
                        arguments.output_directory, section_id, assignment_id
                    )
                    _create_file_from_dataframe(
                        _get_submissions(facade, assignment_id, section_id),
                        submission_file_name,
                    )

        section_activities_file_path: str = lms.get_section_activities_file_path(
            arguments.output_directory, section_id
        )
        _create_file_from_dataframe(
            _get_section_activities(facade, section_id), section_activities_file_path
        )

        file_path = lms.get_section_association_file_path(
            arguments.output_directory, section_id
        )
        succeeded = _create_file_from_dataframe(
            _get_section_associations(facade, section_id), file_path
        )

        file_path = lms.get_attendance_events_file_path(
            arguments.output_directory, section_id
        )
        _create_file_from_dataframe(_get_attendance_events(facade, section_id), file_path)

    need_to_process_input_files = arguments.input_directory is not None
    if need_to_process_input_files:
        system_activities_output_dir: str = lms.get_system_activities_file_path(
            arguments.output_directory
        )
        _create_file_from_dataframe(
            _get_system_activities(arguments.input_directory, db_engine), system_activities_output_dir
        )

    logger.info("Finishing Ed-Fi LMS Schoology Extractor")
