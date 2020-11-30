# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
from typing import Optional, Union


def _get_directory_for_section(
    base_directory: str, section_id: Union[str, int], file_type: str
) -> Optional[str]:
    return os.path.join(base_directory, f"section={section_id}", file_type)


def get_users_directory(base_directory: str) -> Optional[str]:
    return os.path.join(base_directory, "users")


def get_sections_directory(base_directory: str) -> Optional[str]:
    return os.path.join(base_directory, "sections")


def get_system_activities_directory(base_directory: str) -> Optional[str]:
    return os.path.join(base_directory, "system-activities")


def get_section_associations_directory(
    base_directory: str, section_id: int
) -> Optional[str]:
    return _get_directory_for_section(
        base_directory, section_id, "section-associations"
    )


def get_section_activities_directory(
    base_directory: str, section_id: int
) -> Optional[str]:
    return _get_directory_for_section(base_directory, section_id, "section-activities")


def get_assignments_directory(base_directory: str, section_id: int) -> Optional[str]:
    return _get_directory_for_section(base_directory, section_id, "assignments")


def get_grades_directory(base_directory: str, section_id: int) -> Optional[str]:
    return _get_directory_for_section(base_directory, section_id, "grades")


def get_submissions_directory(
    base_directory: str, section_id: int, assignment_id: int
) -> Optional[str]:

    assignments = _get_directory_for_section(
        base_directory, section_id, f"assignment={assignment_id}"
    )

    if assignments is None:
        return None

    return os.path.join(assignments, "submissions")


def get_attendance_events_directory(
    base_directory: str, section_id: int
) -> Optional[str]:
    return _get_directory_for_section(base_directory, section_id, "attendance-events")
