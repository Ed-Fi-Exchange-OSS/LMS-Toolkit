# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Callable

import pandas as pd


from .file_repository import (
    get_users_file,
    get_sections_file,
    get_section_associations_file,
    get_user_activities_file,
    get_assignments_file,
    get_grades_file,
    get_attendance_events_file,
    get_submissions_file
)


def _default() -> pd.DataFrame:
    return pd.DataFrame()

def _read_csv(file: str) -> pd.DataFrame:
    if file:
        return pd.read_csv(
            file, engine="c", parse_dates=True, infer_datetime_format=True
        )

    return _default()


def get_all_users(base_directory: str) -> pd.DataFrame:
    file = get_users_file(base_directory)

    if file is not None:
        return _read_csv(file)

    return _default()


def get_all_sections(base_directory: str) -> pd.DataFrame:
    file = get_sections_file(base_directory)

    if file is not None:
        return _read_csv(file)

    return _default()


def get_section_associations(base_directory: str, section_id: int) -> pd.DataFrame:
    file = get_section_associations_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file)

    return _default()


def _get_data_for_section(
    base_directory: str, sections: pd.DataFrame, callback: Callable
) -> pd.DataFrame:
    df = pd.DataFrame()

    if sections.empty:
        print(
            "No sections have been loaded, therefore no section sub-files can be read."
        )
        return _default()

    for _, section_id in sections[["SourceSystemIdentifier"]].itertuples():
        sa = callback(base_directory, section_id)

        if not sa.empty:
            df = df.append(sa)

    return df


def get_all_section_associations(
    base_directory: str, sections: pd.DataFrame
) -> pd.DataFrame:
    return _get_data_for_section(base_directory, sections, get_section_associations)


def get_user_activities(base_directory: str, section_id: int) -> pd.DataFrame:
    file = get_user_activities_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file)

    return _default()


def get_all_user_activities(
    base_directory: str, sections: pd.DataFrame
) -> pd.DataFrame:
    return _get_data_for_section(base_directory, sections, get_user_activities)


def get_assignments(base_directory: str, section_id: int) -> pd.DataFrame:
    file = get_assignments_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file)

    return _default()


def get_all_assignments(base_directory: str, sections: pd.DataFrame) -> pd.DataFrame:
    return _get_data_for_section(base_directory, sections, get_assignments)


def get_submissions(
    base_directory: str, section_id: int, assignment_id: int
) -> pd.DataFrame:
    file = get_submissions_file(base_directory, section_id, assignment_id)

    if file is not None:
        return _read_csv(file)

    return _default()


def get_all_submissions(base_directory: str, assignments: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    columns = ["SourceSystemIdentifier", "LMSSectionSourceSystemIdentifier"]
    for _, assignment_id, section_id in assignments[columns].itertuples():
        s = get_submissions(base_directory, section_id, assignment_id)

        if not s.empty:
            df = df.append(s)

    return df


def get_grades(base_directory: str, section_id: int) -> pd.DataFrame:
    file = get_grades_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file)

    return _default()


def get_all_grades(base_directory: str, sections: pd.DataFrame) -> pd.DataFrame:
    return _get_data_for_section(base_directory, sections, get_grades)


def get_attendance_events(base_directory: str, section_id: int) -> pd.DataFrame:
    file = get_attendance_events_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file)

    return _default()


def get_all_attendance_events(
    base_directory: str, sections: pd.DataFrame
) -> pd.DataFrame:
    return _get_data_for_section(base_directory, sections, get_attendance_events)
