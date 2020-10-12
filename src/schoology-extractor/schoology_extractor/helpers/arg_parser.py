# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass

from configargparse import ArgParser

from schoology_extractor.helpers import constants


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
    grading_period: str
        CSV with the grading periods.
    output_directory: str
        The output directory for the generated csv files.
    log_level: str
        The log level for the tool.
    """
    client_key: str
    client_secret: str
    grading_period: str
    output_directory: str
    log_level: str


def parse_main_arguments(args_in: list) -> MainArguments:
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

    assert isinstance(args_in, list), "Argument `args_in` must be a list"
    parser = ArgParser()
    parser.add('-k', '--client-key', required=True, help='Schoology client key.', type=str)
    parser.add('-s', '--client_secret', required=True, help='Schoology client secret.', type=str)
    parser.add('-g', '--grading-period', required=True, help='CSV with the grading periods.', type=str)
    parser.add(
        '-o',
        '--output-directory',
        required=False,
        help='The output directory for the generated csv files.',
        type=str,
        default="")

    parser.add(
        '-l',
        '--log-level',
        required=False,
        help='The log level for the tool.',
        choices=constants.LOG_LEVELS,
        type=str,
        default="INFO")

    args_parsed = parser.parse_args(args_in)
    # Required
    assert isinstance(args_parsed.client_key, str), "Argument `client-key` must be a string."
    assert isinstance(args_parsed.client_secret, str), "Argument `client-secret` must be a string."
    assert isinstance(args_parsed.grading_period, str), "Argument `grading-period` must be a string."

    # Optional
    assert isinstance(args_parsed.output_directory, str), "The specified `output-directory` is not valid."
    assert args_parsed.log_level in constants.LOG_LEVELS, "The specified `log-level` is not an allowed value."

    arguments = MainArguments(
        client_key=args_parsed.client_key,
        client_secret=args_parsed.client_secret,
        grading_period=args_parsed.grading_period,
        output_directory=args_parsed.output_directory,
        log_level=args_parsed.log_level,
    )

    return arguments


@dataclass
class GradingPeriodsArguments:
    """
    Container for holding arguments parsed at the command line.

    Parameters
    ----------
    client_key : str
        Schoology client key.
    client_secret: str
        Schoology client secret.
    log_level: str
        The log level for the tool.
    """
    client_key: str
    client_secret: str
    log_level: str


def parse_grading_periods_arguments(args_in: list) -> GradingPeriodsArguments:
    """
    Configures the command-line interface.

    Parameters
    ----------
    args_in : list of str
        Full argument list from the command line.

    Returns
    -------
    arguments  : GradingPeriodsArguments
        A populated `GradingPeriodsArguments` object.
    """

    assert isinstance(args_in, list), "Argument `args_in` must be a list"

    parser = ArgParser()
    parser.add('-k', '--client-key', required=True, help='Schoology client key.', type=str)
    parser.add('-s', '--client_secret', required=True, help='Schoology client secret.', type=str)
    parser.add(
        '-l',
        '--log-level',
        required=False,
        help='The log level for the tool.',
        choices=constants.LOG_LEVELS,
        type=str,
        default="INFO")
    args_parsed = parser.parse_args(args_in)

    assert isinstance(args_parsed.client_key, str), "Argument `client-key` must be a string."
    assert isinstance(args_parsed.client_secret, str), "Argument `client-secret` must be a string."
    assert args_parsed.log_level in constants.LOG_LEVELS, "The specified `log-level` is not an allowed value."

    arguments = GradingPeriodsArguments(
        client_key=args_parsed.client_key,
        client_secret=args_parsed.client_secret,
        log_level=args_parsed.log_level
    )

    return arguments
