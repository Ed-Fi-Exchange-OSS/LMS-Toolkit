# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
from typing import List, Optional


import edfi_lms_file_utils.directory_repository as dr


def _get_newest_file(directory: Optional[str]) -> Optional[str]:

    if directory is None or not os.path.exists(directory):
        return None

    files = [{"path": f.path, "name": f.name, "size": f.stat().st_size} for f in os.scandir(directory) if f.name.endswith(".csv")]
    files = sorted(files, key=lambda x: str(x["name"]), reverse=False)

    while files:
        f = files.pop()

        # Why 4? Because pandas.DataFrame.to_csv writes a file with two line
        # breaks "\n\n" when the DataFrame is empty. Want to ignore those files.
        if int(str(f["size"])) > 4:
            return str(f["path"])

    return None


def get_users_file(base_directory: str) -> Optional[str]:
    return _get_newest_file(dr.get_users_directory(base_directory))


def get_sections_file(base_directory: str) -> Optional[str]:
    return _get_newest_file(dr.get_sections_directory(base_directory))


def get_system_activities_files(base_directory: str) -> List[str]:
    files: List[str] = list()

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
