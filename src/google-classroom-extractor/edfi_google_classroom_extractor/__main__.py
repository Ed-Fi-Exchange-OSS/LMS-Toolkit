# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import sys

from dotenv import load_dotenv
from errorhandler import ErrorHandler

from edfi_google_classroom_extractor.helpers import arg_parser
from edfi_google_classroom_extractor import facade

logger: logging.Logger
error_tracker: ErrorHandler


def _parse_args() -> arg_parser.MainArguments:
    return arg_parser.parse_main_arguments(sys.argv[1:])


def _configure_logging(arguments: arg_parser.MainArguments):
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


def _main(arguments):
    facade.run(arguments)

    if error_tracker.fired:
        print(
            "A fatal error occurred, please review the log output for more information.",
            file=sys.stderr,
        )
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    load_dotenv()
    arguments = _parse_args()
    _configure_logging(arguments)
    _main(arguments)
