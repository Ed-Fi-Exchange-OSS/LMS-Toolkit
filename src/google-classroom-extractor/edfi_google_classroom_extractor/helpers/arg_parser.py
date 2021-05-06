
from dataclasses import dataclass
from typing import List

from configargparse import ArgParser

from . import constants


@dataclass
class MainArguments:
    """
    Container for holding arguments parsed at the command line.
    """
    classroom_account: str
    log_level: str
    output_directory: str
    usage_start_date: str
    usage_end_date: str
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
        env_var="OUTPUT_DIRECTORY",
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

    assert isinstance(
        args_parsed.output_directory, str
    ), "The specified `classroom-account` is not valid."

    arguments = MainArguments(
        classroom_account=args_parsed.classroom_account,
        log_level=args_parsed.log_level,
        output_directory=args_parsed.output_directory,
        usage_start_date=args_parsed.usage_start_date,
        usage_end_date=args_parsed.usage_end_date,
        sync_database_directory=args_parsed.sync_database_directory,
        extract_activities=constants.Features.Activities in args_parsed.feature,
        extract_assignments=constants.Features.Assignments in args_parsed.feature,
        extract_attendance=constants.Features.Attendance in args_parsed.feature,
        extract_grades=constants.Features.Grades in args_parsed.feature,
    )

    return arguments
