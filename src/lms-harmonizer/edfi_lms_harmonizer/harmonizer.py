# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import Optional

from sqlalchemy.engine.base import Engine

from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions
from edfi_lms_harmonizer.helpers.argparser import MainArguments
from edfi_lms_harmonizer.exceptions_reports import (
    create_exception_reports,
    print_summary
)
from edfi_sql_adapter.sql_adapter import (
    Adapter,
    Statement
)


logger = logging.getLogger(__name__)


@catch_exceptions
def _harmonize_users(adapter: Adapter) -> None:

    statements = [
        Statement("EXEC lms.harmonize_lmsuser_canvas;",  "Harmonizing Canvas LMS Users."),
        Statement("EXEC lms.harmonize_lmsuser_google_classroom;",  "Harmonizing Google Classroom LMS Users."),
        Statement("EXEC lms.harmonize_lmsuser_schoology;", "Harmonizing Schoology LMS Users.")
    ]

    adapter.execute(statements)

# @catch_exceptions
# def _exception_reporting(adapter: Adapter, exceptions_report_directory: Optional[str]) -> None:
#     if exceptions_report_directory is not None:
#         create_exception_reports(adapter, exceptions_report_directory)

#     print_summary(adapter)


def run(arguments: MainArguments) -> None:
    adapter = arguments.get_adapter()
    # exceptions_report_directory = arguments.exceptions_report_directory

    _harmonize_users(adapter)
    # _exception_reporting(adapter, exceptions_report_directory)
