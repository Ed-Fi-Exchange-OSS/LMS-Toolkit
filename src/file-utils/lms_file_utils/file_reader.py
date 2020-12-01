# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import Callable, Union

import pandas as pd

import lms_file_utils.file_repository as fr


logger = logging.getLogger(__name__)


def _default() -> pd.DataFrame:
    return pd.DataFrame()


def _read_csv(file: str, nrows: Union[int, None] = None) -> pd.DataFrame:
    if file:
        return pd.read_csv(
            file, engine="c", parse_dates=True, infer_datetime_format=True, nrows=nrows
        )

    return _default()


def get_all_users(base_directory: str, nrows: Union[int, None] = None) -> pd.DataFrame:
    file = fr.get_users_file(base_directory)

    if file is not None:
        return _read_csv(file, nrows)

    return _default()


def get_all_system_activities(
    base_directory: str, nrows: Union[int, None] = None
) -> pd.DataFrame:
    files = fr.get_system_activities_files(base_directory)

    if files is None:
        return _default()

    df_list = list()
    for f in files:
        df_list.append(_read_csv(f, nrows))

    return pd.concat(df_list)


def get_all_sections(
    base_directory: str, nrows: Union[int, None] = None
) -> pd.DataFrame:
    file = fr.get_sections_file(base_directory)

    if file is not None:
        return _read_csv(file, nrows)

    return _default()


def get_section_associations(
    base_directory: str, section_id: int, nrows: Union[int, None] = None
) -> pd.DataFrame:
    file = fr.get_section_associations_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file, nrows)

    return _default()


def _get_data_for_section(
    base_directory: str,
    sections: pd.DataFrame,
    callback: Callable,
    nrows: Union[int, None] = None,
) -> pd.DataFrame:
    df = pd.DataFrame()

    if sections.empty:
        logger.info(
            "No sections have been loaded, therefore no section sub-files can be read."
        )
        return _default()

    for _, section_id in sections[["SourceSystemIdentifier"]].itertuples():
        sa = callback(base_directory, section_id, nrows)

        if not sa.empty:
            df = df.append(sa)

    return df


def get_all_section_associations(
    base_directory: str, sections: pd.DataFrame, nrows: Union[int, None] = None
) -> pd.DataFrame:
    return _get_data_for_section(
        base_directory, sections, get_section_associations, nrows
    )


def get_section_activities(
    base_directory: str, section_id: int, nrows: Union[int, None] = None
) -> pd.DataFrame:
    file = fr.get_section_activities_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file, nrows)

    return _default()


def get_all_section_activities(
    base_directory: str, sections: pd.DataFrame, nrows: Union[int, None] = None
) -> pd.DataFrame:
    return _get_data_for_section(
        base_directory, sections, get_section_activities, nrows
    )


def get_assignments(
    base_directory: str, section_id: int, nrows: Union[int, None] = None
) -> pd.DataFrame:
    file = fr.get_assignments_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file, nrows)

    return _default()


def get_all_assignments(
    base_directory: str, sections: pd.DataFrame, nrows: Union[int, None] = None
) -> pd.DataFrame:
    return _get_data_for_section(base_directory, sections, get_assignments, nrows)


def get_submissions(
    base_directory: str,
    section_id: int,
    assignment_id: int,
    nrows: Union[int, None] = None,
) -> pd.DataFrame:
    file = fr.get_submissions_file(base_directory, section_id, assignment_id)

    if file is not None:
        return _read_csv(file, nrows)

    return _default()


def get_all_submissions(
    base_directory: str, assignments: pd.DataFrame, nrows: Union[int, None] = None
) -> pd.DataFrame:

    if assignments.empty:
        logger.info(
            "No assignments have been loaded, therefore no submission files can be read."
        )
        return _default()

    df = pd.DataFrame()
    columns = ["SourceSystemIdentifier", "LMSSectionSourceSystemIdentifier"]
    for _, assignment_id, section_id in assignments[columns].itertuples():
        s = get_submissions(base_directory, section_id, assignment_id, nrows)

        if not s.empty:
            df = df.append(s)

    return df


def get_grades(
    base_directory: str, section_id: int, nrows: Union[int, None] = None
) -> pd.DataFrame:
    file = fr.get_grades_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file, nrows)

    return _default()


def get_all_grades(
    base_directory: str, sections: pd.DataFrame, nrows: Union[int, None] = None
) -> pd.DataFrame:
    return _get_data_for_section(base_directory, sections, get_grades, nrows)


def get_attendance_events(
    base_directory: str, section_id: int, nrows: Union[int, None] = None
) -> pd.DataFrame:
    file = fr.get_attendance_events_file(base_directory, section_id)

    if file is not None:
        return _read_csv(file, nrows)

    return _default()


def get_all_attendance_events(
    base_directory: str, sections: pd.DataFrame, nrows: Union[int, None] = None
) -> pd.DataFrame:
    return _get_data_for_section(base_directory, sections, get_attendance_events, nrows)
