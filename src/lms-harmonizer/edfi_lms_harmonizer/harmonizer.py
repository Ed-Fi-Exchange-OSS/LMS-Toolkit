# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging

from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions
from edfi_sql_adapter.sql_adapter import Adapter, Statement
from edfi_lms_harmonizer.helpers.constants import (
    SOURCE_SYSTEM,
    SOURCE_SYSTEM_NAMESPACE,
    DB_ENGINE,
)


logger = logging.getLogger(__name__)


def _generate_call_to_stored_procedure(
    engine: str, procedure: str, namespace: str = None, source_system: str = None
) -> str:
    if engine == DB_ENGINE.MSSQL:
        statement = f"EXEC lms.{procedure}"
        if namespace is not None or source_system is not None:
            statement += f" @Namespace='{namespace}', @SourceSystem='{source_system}'"
        return statement

    statement = f"call lms.{procedure}("
    if namespace is not None and source_system is not None:
        statement += f" _namespace => '{namespace}',  _sourcesystem => '{source_system}'"
    return statement + ")"


@catch_exceptions
def harmonize_users(engine: str, adapter: Adapter) -> None:

    statements = [
        Statement(
            _generate_call_to_stored_procedure(engine, "harmonize_lmsuser_canvas"),
            "Harmonizing Canvas LMS Users.",
        ),
        Statement(
            _generate_call_to_stored_procedure(
                engine, "harmonize_lmsuser_google_classroom"
            ),
            "Harmonizing Google Classroom LMS Users.",
        ),
        Statement(
            _generate_call_to_stored_procedure(engine, "harmonize_lmsuser_schoology"),
            "Harmonizing Schoology LMS Users.",
        ),
    ]

    adapter.execute(statements)


@catch_exceptions
def harmonize_sections(engine: str, adapter: Adapter) -> None:

    statements = [
        Statement(
            _generate_call_to_stored_procedure(engine, "harmonize_lmssection_canvas"),
            "Harmonizing Canvas LMS Sections.",
        ),
        Statement(
            _generate_call_to_stored_procedure(
                engine, "harmonize_lmssection_google_classroom"
            ),
            "Harmonizing Google Classroom LMS Sections.",
        ),
        Statement(
            _generate_call_to_stored_procedure(
                engine, "harmonize_lmssection_schoology"
            ),
            "Harmonizing Schoology LMS Sections.",
        ),
    ]

    adapter.execute(statements)


@catch_exceptions
def harmonize_assignments(engine: str, adapter: Adapter) -> None:

    statements = [
        Statement(
            _generate_call_to_stored_procedure(
                engine,
                "harmonize_assignment",
                SOURCE_SYSTEM_NAMESPACE.CANVAS,
                SOURCE_SYSTEM.CANVAS,
            ),
            "Harmonizing Canvas LMS Assignments.",
        ),
        Statement(
            _generate_call_to_stored_procedure(
                engine,
                "harmonize_assignment",
                SOURCE_SYSTEM_NAMESPACE.GOOGLE,
                SOURCE_SYSTEM.GOOGLE,
            ),
            "Harmonizing Google Classroom LMS Assignments.",
        ),
        Statement(
            _generate_call_to_stored_procedure(
                engine,
                "harmonize_assignment",
                SOURCE_SYSTEM_NAMESPACE.SCHOOLOGY,
                SOURCE_SYSTEM.SCHOOLOGY
            ),
            "Harmonizing Schoology LMS Assignments.",
        ),
    ]

    adapter.execute(statements)


@catch_exceptions
def harmonize_assignment_submissions(engine: str, adapter: Adapter) -> None:

    statements = [
        Statement(
            _generate_call_to_stored_procedure(
                engine,
                "harmonize_assignment_submissions",
                SOURCE_SYSTEM_NAMESPACE.CANVAS,
                SOURCE_SYSTEM.CANVAS,
            ),
            "Harmonizing Canvas LMS Assignment Submissions.",
        ),
        Statement(
            _generate_call_to_stored_procedure(
                engine,
                "harmonize_assignment_submissions",
                SOURCE_SYSTEM_NAMESPACE.GOOGLE,
                SOURCE_SYSTEM.GOOGLE,
            ),
            "Harmonizing Google Classroom LMS Assignment Submissions.",
        ),
        Statement(
            _generate_call_to_stored_procedure(
                engine,
                "harmonize_assignment_submissions",
                SOURCE_SYSTEM_NAMESPACE.SCHOOLOGY,
                SOURCE_SYSTEM.SCHOOLOGY,
            ),
            "Harmonizing Schoology LMS Assignment Submissions.",
        ),
    ]

    adapter.execute(statements)
