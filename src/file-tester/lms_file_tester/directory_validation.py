# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
import sys
from typing import List, Optional, Union

# The following is a hack to load a local package above this package's base
# directory, so that this test utility does not need to rely on downloading a
# published version of the LMS file utils.
sys.path.append(os.path.join("..", "file-utils"))
from lms_file_utils import directory_repository as dr  # type: ignore # noqa: E402


def _check_for_directory(input_directory: str) -> Optional[str]:
    if not os.path.exists(input_directory):
        return f"Missing directory: {input_directory}"

    return None


def validate_base_directory_structure(input_directory: str) -> List[str]:

    is_missing = _check_for_directory(input_directory)
    if is_missing:
        return [is_missing]

    errors: List[str] = list()

    for d in [
        dr.get_users_directory(input_directory),
        dr.get_sections_directory(input_directory),
        dr.get_system_activities_directory(input_directory),
    ]:
        is_missing = _check_for_directory(d)
        if is_missing:
            errors.append(is_missing)

    return errors


def validate_section_directory_structure(
    input_directory: str, section_id: Union[str, int]
) -> List[str]:

    is_missing = _check_for_directory(input_directory)
    if is_missing:
        return [is_missing]

    errors: List[str] = list()

    for d in [
        dr.get_section_associations_directory(input_directory, section_id),
        dr.get_section_activities_directory(input_directory, section_id),
        dr.get_assignments_directory(input_directory, section_id),
        dr.get_grades_directory(input_directory, section_id),
        dr.get_attendance_events_directory(input_directory, section_id),
    ]:
        is_missing = _check_for_directory(d)
        if is_missing:
            errors.append(is_missing)

    return errors


def validate_assignment_directory_structure(
    input_directory: str, section_id: Union[str, int], assignment_id: Union[str, int]
) -> List[str]:

    base_dir = os.path.split(dr.get_assignments_directory(input_directory, section_id))[0]

    is_missing = _check_for_directory(base_dir)
    if is_missing:
        return [is_missing]

    is_missing = _check_for_directory(
        dr.get_submissions_directory(input_directory, section_id, assignment_id)
    )
    if is_missing:
        return [is_missing]

    return list()
