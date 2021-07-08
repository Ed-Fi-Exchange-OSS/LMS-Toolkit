# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging

from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions
from edfi_sql_adapter.sql_adapter import Adapter, Statement


logger = logging.getLogger(__name__)


@catch_exceptions
def harmonize_users(adapter: Adapter) -> None:

    statements = [
        Statement(
            "EXEC lms.harmonize_lmsuser_canvas;", "Harmonizing Canvas LMS Users."
        ),
        Statement(
            "EXEC lms.harmonize_lmsuser_google_classroom;",
            "Harmonizing Google Classroom LMS Users.",
        ),
        Statement(
            "EXEC lms.harmonize_lmsuser_schoology;", "Harmonizing Schoology LMS Users."
        ),
    ]

    adapter.execute(statements)


@catch_exceptions
def harmonize_sections(adapter: Adapter) -> None:

    statements = [
        Statement(
            "EXEC lms.harmonize_lmssection_canvas;", "Harmonizing Canvas LMS Sections."
        ),
        Statement(
            "EXEC lms.harmonize_lmssection_google_classroom;",
            "Harmonizing Google Classroom LMS Sections.",
        ),
        Statement(
            "EXEC lms.harmonize_lmssection_schoology;",
            "Harmonizing Schoology LMS Sections.",
        ),
    ]

    adapter.execute(statements)


@catch_exceptions
def harmonize_assignments(adapter: Adapter) -> None:

    statements = [
        Statement("EXEC lms.harmonize_assignment;", "Harmonizing LMS Assignments."),
    ]

    adapter.execute(statements)


@catch_exceptions
def harmonize_assignment_submissions(adapter: Adapter) -> None:

    statements = [
        Statement("EXEC lms.harmonize_assignment_submissions;", "Harmonizing LMS Assignment Submissions."),
    ]

    adapter.execute(statements)
