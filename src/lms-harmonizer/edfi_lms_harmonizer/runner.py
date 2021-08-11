# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from edfi_lms_harmonizer.migrator import migrate
from edfi_lms_harmonizer.helpers.argparser import MainArguments
from edfi_lms_harmonizer.exceptions_reports import (
    create_exception_reports,
    print_summary,
)
from edfi_lms_harmonizer.harmonizer import (
    harmonize_users,
    harmonize_sections,
    harmonize_assignments,
    harmonize_assignment_submissions
)


logger = logging.getLogger(__name__)

#
# Developer note: this class will not be unit tested
#


def run(arguments: MainArguments) -> None:
    """
    Orchestrates the primary business functions of LMS Harmonizer

    Parameters
    ----------
    arguments: MainArguments
        An object containing the system arguments
    """

    logger.info("Starting the Ed-Fi LMS Harmonizer")

    adapter = arguments.get_adapter()
    migrate(adapter)

    exceptions_report_directory = arguments.exceptions_report_directory

    harmonize_users(adapter)
    harmonize_sections(adapter)
    harmonize_assignments(adapter)
    harmonize_assignment_submissions(adapter)

    if exceptions_report_directory is not None:
        create_exception_reports(adapter, exceptions_report_directory)

    print_summary(adapter)

    logger.info("Finishing the Ed-Fi LMS Harmonizer")
