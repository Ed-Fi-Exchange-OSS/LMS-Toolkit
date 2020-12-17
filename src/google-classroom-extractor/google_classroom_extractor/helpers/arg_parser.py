
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
    log_level: str
        The log level for the tool. (optional)
    """
    log_level: str


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
        "-l",
        "--log-level",
        required=False,
        help="The log level for the tool.",
        choices=constants.LOG_LEVELS,
        type=str,
        default="INFO",
        env_var="SCHOOLOGY_LOG_LEVEL",
    )

    args_parsed = parser.parse_args(args_in)

    assert (
        args_parsed.log_level in constants.LOG_LEVELS
    ), "The specified `log-level` is not an allowed value."

    arguments = MainArguments(
        log_level=args_parsed.log_level,
    )

    return arguments
