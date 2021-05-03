# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
import os

from edfi_lms_file_utils import directory_repository as dr

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


def _create_directory_if_it_does_not_exist(dir: str) -> None:
    if not os.path.exists(dir):
        os.makedirs(dir)


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
    assignment_dir = dr.get_assignments_directory(output_directory, section_id)
    _create_directory_if_it_does_not_exist(assignment_dir)

    return os.path.join(assignment_dir, _get_file_name())


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
    section_activities_dir = dr.get_section_activities_directory(output_directory, section_id)
    _create_directory_if_it_does_not_exist(section_activities_dir)

    return os.path.join(section_activities_dir, _get_file_name())


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
    users_dir = dr.get_users_directory(output_directory)
    _create_directory_if_it_does_not_exist(users_dir)

    return os.path.join(users_dir, _get_file_name())


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
    sections_dir = dr.get_sections_directory(output_directory)
    _create_directory_if_it_does_not_exist(sections_dir)

    return os.path.join(sections_dir, _get_file_name())


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
    associations_dir = dr.get_section_associations_directory(output_directory, section_id)
    _create_directory_if_it_does_not_exist(associations_dir)

    return os.path.join(associations_dir, _get_file_name())


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
    attendance_dir = dr.get_attendance_events_directory(output_directory, section_id)
    _create_directory_if_it_does_not_exist(attendance_dir)

    return os.path.join(attendance_dir, _get_file_name())


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
    submissions_dir = dr.get_submissions_directory(output_directory, section_id, assignment_id)
    _create_directory_if_it_does_not_exist(submissions_dir)

    return os.path.join(submissions_dir, _get_file_name())


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
    system_activities_dir = dr.get_system_activities_directory_for_today(output_directory)
    _create_directory_if_it_does_not_exist(system_activities_dir)

    return os.path.join(system_activities_dir, _get_file_name())
