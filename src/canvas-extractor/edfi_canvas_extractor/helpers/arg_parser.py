# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
from typing import List

from configargparse import ArgParser

from . import constants


@dataclass
class MainArguments:
    """
    Container for holding arguments parsed at the command line.
    """

    base_url: str
    access_token: str
    log_level: str
    output_directory: str
    start_date: str
    end_date: str
    sync_database_directory: str
    extract_activities: bool = False
    extract_assignments: bool = False
    extract_attendance: bool = False
    extract_grades: bool = False


def parse_main_arguments(args_in: List[str]) -> MainArguments:
    """
    Configures the command-line interface.

    Parameters
    ----------
    args_in : list of str
        Full argument list from the command line.

    Returns
    -------
    arguments  : MainArguments
        A populated `MainArguments` object.
    """

    parser = ArgParser()

    parser.add(  # type: ignore
        "-b",
        "--base-url",
        required=True,
        help="The Canvas API base url.",
        type=str,
        default="",
        env_var="CANVAS_BASE_URL",
    )

    parser.add(  # type: ignore
        "-a",
        "--access-token",
        required=True,
        help="The Canvas API access token.",
        type=str,
        default="",
        env_var="CANVAS_ACCESS_TOKEN",
    )

    parser.add(  # type: ignore
        "-l",
        "--log-level",
        required=False,
        help="The log level for the tool.",
        choices=constants.LOG_LEVELS,
        type=str,
        default="INFO",
        env_var="LOG_LEVEL",
    )

    parser.add(  # type: ignore
        "-o",
        "--output-directory",
        required=False,
        help="The output directory for the generated csv files.",
        type=str,
        default="data/",
        env_var="OUTPUT_DIRECTORY",
    )

    parser.add(  # type: ignore
        "-s",
        "--start-date",
        required=True,
        help="Start date for the range of classes and events to include, in yyyy-mm-dd format.",
        type=str,
        default="",
        env_var="START_DATE",
    )

    parser.add(  # type: ignore
        "-e",
        "--end-date",
        required=True,
        help="End date for the range of classes and events to include, in yyyy-mm-dd format.",
        type=str,
        default="",
        env_var="END_DATE",
    )

    parser.add(  # type: ignore
        "-d",
        "--sync-database-directory",
        required=False,
        help="The directory for the sync database.",
        type=str,
        default="data",
        env_var="SYNC_DATABASE_DIRECTORY",
    )

    parser.add(  # type: ignore
        "-f",
        "--feature",
        required=False,
        help="Features to include.",
        type=str,
        nargs="*",
        choices=constants.VALID_FEATURES,
        default=[],
        env_var="FEATURE",
    )
    args_parsed = parser.parse_args(args_in)

    arguments = MainArguments(
        base_url=args_parsed.base_url,
        access_token=args_parsed.access_token,
        log_level=args_parsed.log_level,
        output_directory=args_parsed.output_directory,
        start_date=args_parsed.start_date,
        end_date=args_parsed.end_date,
        sync_database_directory=args_parsed.sync_database_directory,
        extract_activities=constants.Features.Activities in args_parsed.feature,
        extract_assignments=constants.Features.Assignments in args_parsed.feature,
        extract_attendance=constants.Features.Attendance in args_parsed.feature,
        extract_grades=constants.Features.Grades in args_parsed.feature,
    )

    return arguments
