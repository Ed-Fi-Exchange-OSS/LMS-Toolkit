
from dataclasses import dataclass
from typing import List

from configargparse import ArgParser

from . import constants


@dataclass
class MainArguments:
    """
    Container for holding arguments parsed at the command line.

    Parameters
    ----------
    log_level: str
        The log level for the tool. (optional)
    """
    classroom_account: str
    log_level: str
    output_directory: str
    usage_start_date: str
    usage_end_date: str


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
        "-a",
        "--classroom-account",
        required=True,
        help="The email address of the Google Classroom admin account.",
        type=str,
        default="",
        env_var="CLASSROOM_ACCOUNT",
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
        env_var="OUTPUT_PATH",
    )

    parser.add(  # type: ignore
        "-s",
        "--usage-start-date",
        required=False,
        help="Start date for usage data pull in yyyy-mm-dd format.",
        type=str,
        default="",
        env_var="START_DATE",
    )

    parser.add(  # type: ignore
        "-e",
        "--usage-end-date",
        required=False,
        help="End date for usage data pull in yyyy-mm-dd format.",
        type=str,
        default="",
        env_var="END_DATE",
    )

    args_parsed = parser.parse_args(args_in)

    assert isinstance(
        args_parsed.output_directory, str
    ), "The specified `classroom-account` is not valid."

    arguments = MainArguments(
        classroom_account=args_parsed.classroom_account,
        log_level=args_parsed.log_level,
        output_directory=args_parsed.output_directory,
        usage_start_date=args_parsed.usage_start_date,
        usage_end_date=args_parsed.usage_end_date,
    )

    return arguments
