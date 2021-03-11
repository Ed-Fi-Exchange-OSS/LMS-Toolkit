# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
from typing import Callable, List, Optional
from dataclasses import dataclass


import edfi_lms_file_utils.directory_repository as dr


@dataclass
class FileInfo:
    path: str
    name: str
    size: int

    def has_contents(self) -> bool:
        """
        Determines if a file has contents beyond a couple of line breaks; this situation occurs when
        `pandas.DataFrame.to_csv` writes a file with value "\n\n" for an empty DataFrame.

            Returns
            ---------
            bool
        """
        return self.size > 4


def _scan_files(directory: str) -> List[FileInfo]:
    if not os.path.exists(directory):
        return []

    files = [
        FileInfo(f.path, str(f.name), int(str(f.stat().st_size)))
        for f in os.scandir(directory)
        if f.name.endswith(".csv")
    ]
    return sorted(files, key=lambda x: x.name, reverse=False)


def _get_newest_file(directory: str) -> Optional[str]:
    files = _scan_files(directory)

    while files:
        f = files.pop()
        if f.has_contents():
            return f.path

    return None


def _get_file_paths(directory: str) -> List[str]:
    files = _scan_files(directory)
    return [f.path for f in files if f.has_contents()]


def get_users_file(base_directory: str) -> Optional[str]:
    directory = dr.get_users_directory(base_directory)
    if directory is None:
        return directory

    return _get_newest_file(directory)


def get_users_file_paths(base_directory: str) -> List[str]:
    directory = dr.get_users_directory(base_directory)
    if directory is None:
        return []
    return _get_file_paths(directory)


def get_sections_file(base_directory: str) -> Optional[str]:
    directory = dr.get_sections_directory(base_directory)
    if directory is None:
        return directory
    return _get_newest_file(directory)


def get_sections_file_paths(base_directory: str) -> List[str]:
    directory = dr.get_sections_directory(base_directory)
    if directory is None:
        return []
    return _get_file_paths(directory)


def _get_system_activities_base(base_directory: str, callback: Callable) -> List:
    files: List[str] = list()

    sys_activities = dr.get_system_activities_directory(base_directory)
    if sys_activities is None:
        return files

    if os.path.exists(sys_activities):
        for f in os.scandir(sys_activities):
            callback(f, files)
    return files


def get_system_activities_files(base_directory: str) -> List[str]:
    def _callback(f, files_to_return: List[str]):
        file = _get_newest_file(f.path)
        if file is not None:
            files_to_return.append(file)

    return _get_system_activities_base(base_directory, _callback)


def get_system_activities_file_paths(base_directory: str) -> List[str]:
    def _callback(f, files_to_return: List[str]):
        file = _get_file_paths(f.path)
        if file is not None:
            files_to_return.extend(file)

    return _get_system_activities_base(base_directory, _callback)


def get_section_associations_file(
    base_directory: str, section_id: int
) -> Optional[str]:
    directory = dr.get_section_associations_directory(base_directory, section_id)
    if directory is None:
        return directory
    return _get_newest_file(directory)


def get_section_associations_file_paths(
    base_directory: str, section_id: int
) -> List[str]:
    directory = dr.get_section_associations_directory(base_directory, section_id)
    if directory is None:
        return []
    return _get_file_paths(directory)


def get_section_activities_file(base_directory: str, section_id: int) -> Optional[str]:
    directory = dr.get_section_activities_directory(base_directory, section_id)
    if directory is None:
        return directory
    return _get_newest_file(directory)


def get_section_activities_file_paths(
    base_directory: str, section_id: int
) -> List[str]:
    directory = dr.get_section_activities_directory(base_directory, section_id)
    if directory is None:
        return []
    return _get_file_paths(directory)


def get_assignments_file(base_directory: str, section_id: int) -> Optional[str]:
    directory = dr.get_assignments_directory(base_directory, section_id)
    if directory is None:
        return directory
    return _get_newest_file(directory)


def get_assignments_file_paths(base_directory: str, section_id: int) -> List[str]:
    directory = dr.get_assignments_directory(base_directory, section_id)
    if directory is None:
        return []
    return _get_file_paths(directory)


def get_grades_file(base_directory: str, section_id: int) -> Optional[str]:
    directory = dr.get_grades_directory(base_directory, section_id)
    if directory is None:
        return directory
    return _get_newest_file(directory)


def get_grades_file_paths(base_directory: str, section_id: int) -> List[str]:
    directory = dr.get_grades_directory(base_directory, section_id)
    if directory is None:
        return []
    return _get_file_paths(directory)


def get_submissions_file(
    base_directory: str, section_id: int, assignment_id: int
) -> Optional[str]:
    directory = dr.get_submissions_directory(base_directory, section_id, assignment_id)
    if directory is None:
        return directory
    return _get_newest_file(directory)


def get_submissions_file_paths(
    base_directory: str, section_id: int, assignment_id: int
) -> List[str]:
    directory = dr.get_submissions_directory(base_directory, section_id, assignment_id)
    if directory is None:
        return []
    return _get_file_paths(directory)


def get_attendance_events_file(base_directory: str, section_id: int) -> Optional[str]:
    directory = dr.get_attendance_events_directory(base_directory, section_id)
    if directory is None:
        return directory
    return _get_newest_file(directory)


def get_attendance_events_paths(base_directory: str, section_id: int) -> List[str]:
    directory = dr.get_attendance_events_directory(base_directory, section_id)
    if directory is None:
        return []
    return _get_file_paths(directory)
