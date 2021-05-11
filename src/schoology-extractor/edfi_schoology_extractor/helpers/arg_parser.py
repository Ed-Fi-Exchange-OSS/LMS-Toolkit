# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
from typing import List

from configargparse import ArgParser  # type: ignore

from . import constants


@dataclass
class MainArguments:
    """
    Container for holding arguments parsed at the command line.
    """
    client_key: str
    client_secret: str
    output_directory: str
    log_level: str
    page_size: int
    input_directory: str
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
        "-k",
        "--client-key",
        required=True,
        help="Schoology client key.",
        type=str,
        env_var="SCHOOLOGY_KEY",
    )

    parser.add(  # type: ignore
        "-s",
        "--client-secret",
        required=True,
        help="Schoology client secret.",
        type=str,
        env_var="SCHOOLOGY_SECRET",
    )

    parser.add(  # type: ignore
        "-o",
        "--output-directory",
        required=False,
        help="The output directory for the generated csv files.",
        type=str,
        default="",
        env_var="OUTPUT_DIRECTORY",
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
        "-p",
        "--page-size",
        required=False,
        help="Page size for the paginated requests.",
        type=int,
        default=200,
        env_var="PAGE_SIZE",
    )

    parser.add(  # type: ignore
        "-i",
        "--input-directory",
        required=False,
        help="Input directory for usage CSV files.",
        type=str,
        default=None,
        env_var="SCHOOLOGY_INPUT_DIRECTORY",
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
        nargs='*',
        choices=constants.VALID_FEATURES,
        default=[],
        env_var="FEATURE",
    )

    args_parsed = parser.parse_args(args_in)
    # Required
    assert isinstance(
        args_parsed.client_key, str
    ), "Argument `client-key` must be a string."
    assert isinstance(
        args_parsed.client_secret, str
    ), "Argument `client-secret` must be a string."

    # Optional
    assert isinstance(
        args_parsed.output_directory, str
    ), "The specified `output-directory` is not valid."
    assert (
        args_parsed.log_level in constants.LOG_LEVELS
    ), "The specified `log-level` is not an allowed value."
    assert isinstance(
        args_parsed.page_size, int
    ), "Argument `page-size` must be an int."

    arguments = MainArguments(
        client_key=args_parsed.client_key,
        client_secret=args_parsed.client_secret,
        output_directory=args_parsed.output_directory,
        log_level=args_parsed.log_level,
        page_size=args_parsed.page_size,
        input_directory=args_parsed.input_directory,
        sync_database_directory=args_parsed.sync_database_directory,
        extract_activities=constants.Features.Activities in args_parsed.feature,
        extract_assignments=constants.Features.Assignments in args_parsed.feature,
        extract_attendance=constants.Features.Attendance in args_parsed.feature,
        extract_grades=constants.Features.Grades in args_parsed.feature,
    )

    return arguments
