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

    Parameters
    ----------
    client_key : str
        Schoology client key.
    client_secret: str
        Schoology client secret.
    output_directory: str
        The output directory for the generated csv files. (optional)
    log_level: str
        The log level for the tool. (optional)
    page_size: int
        The size of the page for paginated requests. (optional)
    input_directory: str
        The input directory containing usage CSV files exported from the
        Schoology site. (optional)
    """

    client_key: str
    client_secret: str
    output_directory: str
    log_level: str
    page_size: int
    input_directory: str


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
        env_var="SCHOOLOGY_OUTPUT_PATH",
    )

    parser.add(  # type: ignore
        "-l",
        "--log-level",
        required=False,
        help="The log level for the tool.",
        choices=constants.LOG_LEVELS,
        type=str,
        default="INFO",
        env_var="SCHOOLOGY_LOG_LEVEL",
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
    )

    return arguments
