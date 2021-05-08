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
from edfi_schoology_extractor.client_facade import ClientFacade
from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions

logger = logging.getLogger(__name__)

# This variable facilitates temporary storage of output results from one GET
# request that need to be used for creating another GET request.
result_bucket: Dict[str, DataFrame] = {}


def _initialize(
    arguments: MainArguments,
) -> Tuple[ClientFacade, sqlalchemy.engine.base.Engine]:
    global logger

    try:
        request_client: RequestClient = RequestClient(
            arguments.client_key, arguments.client_secret
        )
        db_engine = get_sync_db_engine(arguments.sync_database_directory)

        facade = ClientFacade(request_client, arguments.page_size, db_engine)

        # Will generate an exception if directory is not valid
        os.lstat(arguments.output_directory)
        if arguments.input_directory:
            os.lstat(arguments.input_directory)

        return facade, db_engine
    except BaseException as e:
        logger.critical(e)
        print(
            "A fatal error occurred, please review the log output for more information.",
            file=sys.stderr,
        )
        sys.exit(1)


def _create_file_from_dataframe(df: Optional[DataFrame], file_name: str) -> None:
    normalized_file_name = os.path.normpath(file_name)
    logger.info(f"Exporting {normalized_file_name}")

    if df is not None:
        csv_writer.df_to_csv(df, normalized_file_name)
    else:
        csv_writer.df_to_csv(DataFrame(), normalized_file_name)


@catch_exceptions
def _get_users(client_facade: ClientFacade, output_directory: str) -> None:
    users = client_facade.get_users()

    _create_file_from_dataframe(users, lms.get_user_file_path(output_directory))


@catch_exceptions
def _get_sections(client_facade: ClientFacade, output_directory: str) -> None:

    sections = client_facade.get_sections()
    result_bucket["sections"] = sections

    _create_file_from_dataframe(
        sections, lms.get_section_file_path(output_directory)
    )


@catch_exceptions
def _get_assignments(
    client_facade: ClientFacade, output_directory: str, section_id: int
) -> None:

    assignment_file_path: str = lms.get_assignment_file_path(
        output_directory, section_id
    )

    assignments = client_facade.get_assignments(section_id)
    result_bucket["assignments"] = assignments

    _create_file_from_dataframe(assignments, assignment_file_path)


@catch_exceptions
def _get_section_activities(
    facade: ClientFacade, output_directory: str, section_id: int
) -> None:

    section_activities_file_path: str = lms.get_section_activities_file_path(
        output_directory, section_id
    )
    section_activities = facade.get_section_activities(section_id)

    _create_file_from_dataframe(section_activities, section_activities_file_path)


@catch_exceptions
def _get_submissions(
    client_facade: ClientFacade, output_directory: str, section_id: int
) -> None:
    assignments: DataFrame = result_bucket["assignments"]

    if not assignments.empty:
        for assignment in assignments["SourceSystemIdentifier"].tolist():

            assignment_id = int(assignment)
            submission_file_name = lms.get_submissions_file_path(
                output_directory, section_id, assignment_id
            )

            submissions = client_facade.get_submissions(assignment_id, section_id)
            _create_file_from_dataframe(
                submissions,
                submission_file_name,
            )


@catch_exceptions
def _get_section_associations(
    client_facade: ClientFacade, output_directory: str, section_id: int
) -> None:
    file_path = lms.get_section_association_file_path(output_directory, section_id)

    section_associations = client_facade.get_section_associations(section_id)
    result_bucket["section_associations"] = section_associations

    _create_file_from_dataframe(section_associations, file_path)


@catch_exceptions
def _get_attendance_events(
    client_facade: ClientFacade, output_directory: str, section_id: int
) -> None:
    file_path = lms.get_attendance_events_file_path(output_directory, section_id)

    section_associations: DataFrame = result_bucket["section_associations"]

    attendance_events: DataFrame = client_facade.get_attendance_events(
        section_id, section_associations
    )

    _create_file_from_dataframe(attendance_events, file_path)


@catch_exceptions
def _get_system_activities(
    arguments: MainArguments, db_engine: sqlalchemy.engine.base.Engine
) -> None:
    need_to_process_input_files = arguments.input_directory is not None

    if need_to_process_input_files:
        system_activities_output_dir: str = lms.get_system_activities_file_path(
            arguments.output_directory
        )

        system_activities = usage_analytics_facade.get_system_activities(
            arguments.input_directory, db_engine
        )

        _create_file_from_dataframe(system_activities, system_activities_output_dir)


def run(arguments: MainArguments) -> None:
    logger.info("Starting Ed-Fi LMS Schoology Extractor")
    facade, db_engine = _initialize(arguments)

    _get_users(facade, arguments.output_directory)
    _get_sections(facade, arguments.output_directory)
    succeeded = result_bucket.get("sections", None) is not None

    if not succeeded:
        logger.critical(
            "Unable to continue file generation because the load of Sections failed. Please review the log for more information."
        )
        sys.exit(1)

    for section_id in result_bucket["sections"]["SourceSystemIdentifier"].values:
        _get_section_associations(facade, arguments.output_directory, section_id)

        if arguments.extract_assignments:
            _get_assignments(facade, arguments.output_directory, section_id)
            succeeded = result_bucket.get("assignments", None) is not None
            if succeeded:
                _get_submissions(facade, arguments.output_directory, section_id)

        if arguments.extract_activities:
            _get_section_activities(facade, arguments.output_directory, section_id)

        if arguments.extract_attendance:
            _get_attendance_events(facade, arguments.output_directory, section_id)

    if arguments.extract_activities:
        _get_system_activities(arguments, db_engine)

    logger.info("Finishing Ed-Fi LMS Schoology Extractor")
