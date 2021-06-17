# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import sys

from dotenv import load_dotenv
from errorhandler import ErrorHandler  # type: ignore

from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions
from edfi_lms_harmonizer.helpers.argparser import MainArguments, parse_main_arguments  # type: ignore
from edfi_lms_harmonizer.runner import run

logger: logging.Logger


@catch_exceptions
def _configure_logging(arguments: MainArguments) -> None:
    global logger

    logger = logging.getLogger(__name__)

    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=arguments.log_level,
    )


def main() -> None:
    load_dotenv()
    arguments = parse_main_arguments(sys.argv[1:])
    _configure_logging(arguments)
    error_tracker: ErrorHandler = ErrorHandler()

    run(arguments)

    if error_tracker.fired:
        print(
            "A fatal error occurred, please review the log output for more information.",
            file=sys.stderr,
        )
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
