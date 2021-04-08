# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import os
from typing import Union

from edfi_lms_file_utils.constants import Resources


def _get_directory_for_section(
    base_directory: str, section_id: Union[str, int], file_type: str
) -> str:
    return os.path.join(base_directory, f"{Resources.SECTION}={section_id}", file_type)


def get_users_directory(base_directory: str) -> str:
    """
    Gets the canonical directory for users files.

    Parameters
    ----------
    base_directory
        The base / parent directory for LMS extractor files.

    Returns
    -------
    str
        Full directory path for the resource.
    """
    return os.path.join(base_directory, Resources.USERS)


def get_sections_directory(base_directory: str) -> str:
    """
    Gets the canonical directory for sections files.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.

    Returns
    -------
    str
        Full directory path for the resource..
    """
    return os.path.join(base_directory, Resources.SECTIONS)


def get_system_activities_directory(base_directory: str) -> str:
    """
    Gets the canonical directory for system activities files.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.

    Returns
    -------
    str
        Full directory path for the resource.
    """
    return os.path.join(base_directory, Resources.SYSTEM_ACTIVITIES)


def get_system_activities_directory_for_today(base_directory: str) -> str:
    """
    Gets the canonical directory for system activities scoped to "today's" date.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.

    Returns
    -------
    str
        Full directory path for the resource.
    """
    return os.path.join(
        get_system_activities_directory(base_directory),
        f"date={datetime.now().strftime('%Y-%m-%d')}",
    )


def get_section_associations_directory(base_directory: str, section_id: int) -> str:
    """
    Gets the canonical directory for section associations files.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    section_id: int
        Section identifier.

    Returns
    -------
    str
        Full directory path for the resource.
    """
    return _get_directory_for_section(
        base_directory, section_id, Resources.SECTION_ASSOCIATIONS
    )


def get_section_activities_directory(base_directory: str, section_id: int) -> str:
    """
    Gets the canonical directory for section activities files.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    section_id: int
        Section identifier.

    Returns
    -------
    str
        Full directory path for the resource.
    """
    return _get_directory_for_section(
        base_directory, section_id, Resources.SECTION_ACTIVITIES
    )


def get_assignments_directory(base_directory: str, section_id: int) -> str:
    """
    Gets the canonical directory for assignments files.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    section_id: int
        Section identifier.

    Returns
    -------
    str
        Full directory path for the resource.
    """
    return _get_directory_for_section(base_directory, section_id, Resources.ASSIGNMENTS)


def get_grades_directory(base_directory: str, section_id: int) -> str:
    """
    Gets the canonical directory for grades files.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    section_id: int
        Section identifier.

    Returns
    -------
    str
        Full directory path for the resource.
    """
    return _get_directory_for_section(base_directory, section_id, Resources.GRADES)


def get_submissions_directory(
    base_directory: str, section_id: int, assignment_id: int
) -> str:
    """
    Gets the canonical directory for submissions files.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    section_id: int
        Section identifier.
    assignment_id: int
        Assignment identifier.

    Returns
    -------
    str
        Full directory path for the resource.
    """
    assignments = _get_directory_for_section(
        base_directory, section_id, f"{Resources.ASSIGNMENT}={assignment_id}"
    )

    return os.path.join(assignments, Resources.SUBMISSIONS)


def get_attendance_events_directory(base_directory: str, section_id: int) -> str:
    """
    Gets the canonical directory for attendance events files.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    section_id: int
        Section identifier.

    Returns
    -------
    str
        Full directory path for the resource.
    """
    return _get_directory_for_section(
        base_directory, section_id, Resources.ATTENDANCE_EVENTS
    )
