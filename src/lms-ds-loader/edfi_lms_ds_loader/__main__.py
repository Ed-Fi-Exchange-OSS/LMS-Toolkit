# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

"""
A utility for loading CSV files in the Learning Management System Unified Data
Model (LMS-UDM) into a Learning Management System Data Store (LMS-DS) database.

call `python . -h` for a detailed listing of command arguments.
"""

import logging
import sys

from dotenv import load_dotenv
from errorhandler import ErrorHandler  # type: ignore

from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions
from edfi_lms_ds_loader.helpers.argparser import MainArguments, parse_main_arguments
from edfi_lms_ds_loader.loader_facade import runLoader


logger: logging.Logger
error_tracker: ErrorHandler


def _parse_args():
    # catching exceptions is unnecessary here
    return parse_main_arguments(sys.argv[1:])


@catch_exceptions
def _configure_logging(arguments: MainArguments):
    global logger
    global error_tracker

    logger = logging.getLogger(__name__)

    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=arguments.log_level,
    )
    error_tracker = ErrorHandler()


@catch_exceptions
def main(arguments: MainArguments):
    logger.info("Begin loading files into the LMS Data Store (DS)...")
    runLoader(arguments)
    logger.info("Done loading files into the LMS Data Store.")


if __name__ == "__main__":
    load_dotenv()
    arguments = _parse_args()
    _configure_logging(arguments)
    main(arguments)

    if error_tracker.fired:
        print(
            "A fatal error occurred, please review the log output for more information.",
            file=sys.stderr,
        )
        sys.exit(1)
    sys.exit(0)
