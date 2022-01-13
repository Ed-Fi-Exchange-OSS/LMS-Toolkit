# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import sys
from typing import List

# This next line *should* have
# `lms_file_tester.validators.directory_validation`, but the script does not run
# from the command line if you have `lms_file_tester` there - you get a module
# not found error. This does not make sense, and in fact mypy complains about
# it. But pylance does not. Headscratcher. Have tried renaming file to `main.py`
# and that did not solve it.
from validators.directory_validation import (  # type: ignore
    validate_assignment_directory_structure,
    validate_base_directory_structure,
    validate_section_directory_structure,
    validate_system_activities_directory_structure,
)
from validators.file_validation import (  # type: ignore
    validate_users_file,
    validate_sections_file,
    validate_system_activities_file,
    validate_section_associations_file,
    validate_section_activities_file,
    validate_assignments_file,
    validate_submissions_file,
    validate_grades_file,
    validate_attendance_events_file,
)

# The following is a hack to load a local package above this package's base
# directory, so that this test utility does not need to rely on downloading a
# published version of the LMS file utils.
from edfi_lms_file_utils import file_reader as fread  # type: ignore # noqa: E402

logger = logging.getLogger(__name__)


def _configure_logging(level="INFO"):
    logFormatter = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    logging.basicConfig(
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        format=logFormatter,
        level=level,
    )


def _report(errors: List[str], happy: str):
    if len(errors) == 0:
        logger.info(happy)
    else:
        for e in errors:
            logger.warning(e)


def _validate_users_and_sections(input_directory: str):
    errors = validate_base_directory_structure(input_directory)
    _report(errors, "Basic directory structure is valid.")

    errors = validate_users_file(input_directory)
    _report(errors, "Users file is valid.")

    errors = validate_sections_file(input_directory)
    _report(errors, "Sections file is valid.")


def _validate_assignment_directories(input_directory: str, section_id: int):
    assignments = fread.get_assignments(input_directory, section_id)

    if assignments.empty:
        # This just means there is no file in the given directory
        return

    for _, assignment_id in assignments["SourceSystemIdentifier"].iteritems():
        errors = validate_assignment_directory_structure(
            input_directory, section_id, assignment_id
        )
        _report(
            errors,
            f"Assignment directory structure is valid for section {section_id}, assignment {assignment_id}.",
        )

    errors = validate_submissions_file(input_directory, assignments)
    _report(errors, "Submissions file is valid.")


def _validate_section_directories(input_directory: str):
    sections = fread.get_all_sections(input_directory)

    for _, section_id in sections["SourceSystemIdentifier"].iteritems():
        errors = validate_section_directory_structure(input_directory, section_id)
        _report(
            errors, f"Section directory structure is valid for section {section_id}"
        )

        _validate_assignment_directories(input_directory, section_id)

    errors = validate_attendance_events_file(input_directory, sections)
    _report(errors, "Attendance Events file is valid.")

    errors = validate_grades_file(input_directory, sections)
    _report(errors, "Grades file is valid.")

    errors = validate_assignments_file(input_directory, sections)
    _report(errors, "Assignments file is valid.")

    errors = validate_section_associations_file(input_directory, sections)
    _report(errors, "Section Associations Events file is valid.")

    errors = validate_section_activities_file(input_directory, sections)
    _report(errors, "Section Activities Events file is valid.")


def _validate_system_activities_directories(input_directory: str):
    errors = validate_system_activities_directory_structure(input_directory)
    _report(errors, "System Activities directory structure is valid.")

    errors = validate_system_activities_file(input_directory)
    _report(errors, "System Activities file is valid.")


def _main():

    if len(sys.argv) < 2:
        logger.critical(
            "Must pass an input directory as an argument to the script. Optional log level as second argument."
        )

    input_directory = sys.argv[1]

    if len(sys.argv) == 3:
        _configure_logging(sys.argv[2])
    else:
        _configure_logging()

    logger.info("Starting LMS File Tester")

    _validate_users_and_sections(input_directory)
    _validate_section_directories(input_directory)
    _validate_system_activities_directories(input_directory)


if __name__ == "__main__":
    _main()
