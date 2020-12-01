# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import os
import sys
from typing import List, Union

from validators.directory_validation import validate_assignment_directory_structure, validate_base_directory_structure, validate_section_directory_structure

# The following is a hack to load a local package above this package's base
# directory, so that this test utility does not need to rely on downloading a
# published version of the LMS file utils.
sys.path.append(os.path.join("..", "file-utils"))
from lms_file_utils import file_reader as fread  # type: ignore # noqa: E402

logger = logging.getLogger(__name__)


def _configure_logging():
    logFormatter = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        format=logFormatter,
        level="INFO",
    )


def _report(errors: List[str], happy: str):
    if len(errors) == 0:
        logger.info(happy)
    else:
        for e in errors:
            logger.warning(e)


def _validate_top_directories(input_directory: str):
    errors = validate_base_directory_structure(input_directory)
    _report(errors, "Basic directory structure is valid.")


def _validate_assignment_directories(input_directory: str, section_id: Union[int, str]):
    assignments = fread.get_assignments(input_directory, section_id)

    if assignments.empty:
        # This just means there is no file in the given directory
        return

    for _, assignment_id in assignments["SourceSystemIdentifier"].iteritems():
        errors = validate_assignment_directory_structure(input_directory, section_id, assignment_id)
        _report(errors, "Assignment directory structure is valid.")


def _validate_section_directories(input_directory: str):
    sections = fread.get_all_sections(input_directory)

    # then test all of those sections
    for _, section_id in sections["SourceSystemIdentifier"].iteritems():
        errors = validate_section_directory_structure(input_directory, section_id)
        _report(errors, "Section directory structure is valid.")

        _validate_assignment_directories(input_directory, section_id)


def _main():
    logger.info("Starting LMS File Tester")

    if (len(sys.argv) != 2):
        logger.critical("Must pass an input directory as the only argument to the script.")

    input_directory = sys.argv[1]

    _validate_top_directories(input_directory)
    _validate_section_directories(input_directory)

    # Also need to do some more testing on system activities


if __name__ == "__main__":
    _configure_logging()
    _main()
