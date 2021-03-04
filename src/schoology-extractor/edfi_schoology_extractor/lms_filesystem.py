# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import os

USERS = "users"
SECTION = "section"
ASSIGNMENT = "assignment"
ASSIGNMENTS = "assignments"
SECTION_ACTIVITY = "section-activities"
SECTIONS = "sections"
SECTION_ASSOCIATIONS = "section-associations"
ATTENDANCE = "attendance"
SUBMISSIONS = "submissions"
SYSTEM_ACTIVITIES = "system-activities"


def _get_file_name() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".csv"


def _create_directory_if_it_does_not_exist(dir: str):
    if not os.path.exists(dir):
        os.mkdir(dir)


def _get_section_directory(output_directory: str, section_id: int) -> str:
    base_dir = os.path.join(output_directory, f"{SECTION}={section_id}")
    _create_directory_if_it_does_not_exist(base_dir)

    return base_dir


def get_assignment_file_path(output_directory: str, section_id: int) -> str:
    """
    Builds the expected filesystem path (directory + file name) for a new
    Assignments file.

    Parameters
    ----------
    output_directory: str
        Base output directory
    section_id: int
        Identifier the section for which attendance will is being exported

    Returns
    -------
    full path with file name
    """
    base_dir = _get_section_directory(output_directory, section_id)
    base_dir = os.path.join(base_dir, ASSIGNMENTS)
    _create_directory_if_it_does_not_exist(base_dir)

    return os.path.join(base_dir, _get_file_name())


def get_section_activities_file_path(output_directory: str, section_id: int) -> str:
    """
    Builds the expected filesystem path (directory + file name) for a new
    section activity file.

    Parameters
    ----------
    output_directory: str
        Base output directory
    section_id: int
        Identifier the section for which attendance will is being exported

    Returns
    -------
    full path with file name
    """
    base_dir = _get_section_directory(output_directory, section_id)
    base_dir = os.path.join(base_dir, SECTION_ACTIVITY)
    _create_directory_if_it_does_not_exist(base_dir)

    return os.path.join(base_dir, _get_file_name())


def get_user_file_path(output_directory: str) -> str:
    """
    Builds the expected filesystem path (directory + file name) for a new
    Users file.

    Parameters
    ----------
    output_directory: str
        Base output directory

    Returns
    -------
    full path with file name
    """
    base_dir = os.path.join(output_directory, USERS)
    _create_directory_if_it_does_not_exist(base_dir)

    return os.path.join(base_dir, _get_file_name())


def get_section_file_path(output_directory: str) -> str:
    """
    Builds the expected filesystem path (directory + file name) for a new
    Sections file.

    Parameters
    ----------
    output_directory: str
        Base output directory

    Returns
    -------
    full path with file name
    """
    base_dir = os.path.join(output_directory, SECTIONS)
    _create_directory_if_it_does_not_exist(base_dir)

    return os.path.join(base_dir, _get_file_name())


def get_section_association_file_path(output_directory: str, section_id: int) -> str:
    """
    Builds the expected filesystem path (directory + file name) for a new
    Section Association file.

    Parameters
    ----------
    output_directory: str
        Base output directory
    section_id: int
        Identifier the section for which attendance will is being exported

    Returns
    -------
    full path with file name
    """
    base_dir = _get_section_directory(output_directory, section_id)
    base_dir = os.path.join(base_dir, SECTION_ASSOCIATIONS)
    _create_directory_if_it_does_not_exist(base_dir)

    return os.path.join(base_dir, _get_file_name())


def get_attendance_events_file_path(output_directory: str, section_id: int) -> str:
    """
    Builds the expected filesystem path (directory + file name) for a new
    Attendance Events file.

    Parameters
    ----------
    output_directory: str
        Base output directory
    section_id: int
        Identifier the section for which attendance will is being exported

    Returns
    -------
    full path with file name
    """
    base_dir = _get_section_directory(output_directory, section_id)
    base_dir = os.path.join(base_dir, ATTENDANCE)
    _create_directory_if_it_does_not_exist(base_dir)

    return os.path.join(base_dir, _get_file_name())


def get_submissions_file_path(
    output_directory: str, section_id: int, assignment_id: int
) -> str:
    """
    Builds the expected filesystem path (directory + file name) for a new
    Submissions file.

    Parameters
    ----------
    output_directory: str
        Base output directory
    section_id: int
        Identifier the section for which attendance will is being exported

    Returns
    -------
    full path with file name
    """
    # /ed-fi-udm-lms/section=<id>/assignment=<id>/submissions/<YYYY-mm-dd-HH-MM-SS>.csv
    base_dir = _get_section_directory(output_directory, section_id)
    base_dir = os.path.join(base_dir, f"{ASSIGNMENT}={str(assignment_id)}")
    _create_directory_if_it_does_not_exist(base_dir)
    base_dir = os.path.join(base_dir, SUBMISSIONS)
    _create_directory_if_it_does_not_exist(base_dir)

    return os.path.join(base_dir, _get_file_name())


def get_system_activities_file_path(output_directory: str) -> str:
    """
    Builds the expected filesystem path (directory + file name) for a new
    System Activities file.

    Parameters
    ----------
    output_directory: str
        Base output directory

    Returns
    -------
    full path with file name
    """

    base_dir = os.path.join(output_directory, SYSTEM_ACTIVITIES)
    _create_directory_if_it_does_not_exist(base_dir)

    base_dir = os.path.join(base_dir, "date=" + datetime.now().strftime("%Y-%m-%d"))
    _create_directory_if_it_does_not_exist(base_dir)

    return os.path.join(base_dir, _get_file_name())
