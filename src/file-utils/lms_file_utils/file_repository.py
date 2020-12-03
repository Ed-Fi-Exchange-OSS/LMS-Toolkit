# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
from typing import List, Optional


import lms_file_utils.directory_repository as dr


def _get_newest_file(directory: Optional[str]) -> Optional[str]:

    if directory is None or not os.path.exists(directory):
        return None

    files = [(f.path, f.name) for f in os.scandir(directory) if f.name.endswith(".csv")]
    files = sorted(files, key=lambda x: x[1], reverse=True)

    if len(files) > 0:
        return files[0][0]

    return None


def get_users_file(base_directory: str) -> Optional[str]:
    return _get_newest_file(dr.get_users_directory(base_directory))


def get_sections_file(base_directory: str) -> Optional[str]:
    return _get_newest_file(dr.get_sections_directory(base_directory))


def get_system_activities_files(base_directory: str) -> List[str]:
    files = list()

    sys_activities = dr.get_system_activities_directory(base_directory)

    if sys_activities is None:
        return files

    if os.path.exists(sys_activities):
        for f in os.scandir(sys_activities):
            file = _get_newest_file(f.path)

            if file is not None:
                files.append(file)

    return files


def get_section_associations_file(
    base_directory: str, section_id: int
) -> Optional[str]:
    return _get_newest_file(dr.get_section_associations_directory(base_directory, section_id))


def get_section_activities_file(base_directory: str, section_id: int) -> Optional[str]:
    return _get_newest_file(dr.get_section_activities_directory(base_directory, section_id))


def get_assignments_file(base_directory: str, section_id: int) -> Optional[str]:
    return _get_newest_file(dr.get_assignments_directory(base_directory, section_id))


def get_grades_file(base_directory: str, section_id: int) -> Optional[str]:
    return _get_newest_file(dr.get_grades_directory(base_directory, section_id))


def get_submissions_file(
    base_directory: str, section_id: int, assignment_id: int
) -> Optional[str]:
    return _get_newest_file(dr.get_submissions_directory(base_directory, section_id, assignment_id))


def get_attendance_events_file(base_directory: str, section_id: int) -> Optional[str]:
    return _get_newest_file(dr.get_attendance_events_directory(base_directory, section_id))
