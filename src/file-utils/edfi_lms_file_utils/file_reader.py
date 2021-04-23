# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import Callable, Dict, List, Optional

import pandas as pd  # type: ignore

import edfi_lms_file_utils.file_repository as fr
from edfi_lms_file_utils.constants import DataTypes, Keys

logger = logging.getLogger(__name__)


def _default() -> pd.DataFrame:
    return pd.DataFrame()


def _read_csv(
    file: str,
    nrows: Optional[int] = None,
    data_types: Dict[str, str] = dict(),
    extra_date_columns: List[str] = list(),
) -> pd.DataFrame:
    """
    Loads a CSV file into a DataFrame.

    Parameters
    ----------
    file: str
        Full path to the file to read.
    nrows: int (optional)
        Number of rows to read. If not specified, reads all lines.
    data_types: dictionary (optional)
        A dictionary for forcing Pandas to use the correct data
        type. Do not use for DateTime columns - instead add those
        columns to the list in the `extra_date_columns` parameter.
    extra_date_columns: list (optional)
        A list of columns that should be treated as having DateTime
        data type.

    Returns
    -------
    pd.DataFrame
        The exact columns depend on the file being read.
    """

    logger.debug(f"Reading file: {file}")
    if file:

        dates = [
            "SourceCreateDate",
            "SourceLastModifiedDate",
            "CreateDate",
            "LastModifiedDate",
            *extra_date_columns,
        ]

        dtype = {
            "SourceSystemIdentifier": "string",
            "SourceSystem": "string",
            **data_types,
        }

        return pd.read_csv(
            file,
            engine="c",
            parse_dates=dates,
            infer_datetime_format=True,
            nrows=nrows,
            dtype=dtype,
        )

    return _default()


def get_all_users(base_directory: str, nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Reads the most recent users file into a Pandas DataFrame.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    file = fr.get_users_file(base_directory)

    if file is None:
        return _default()

    return read_users_file(file, nrows)


def read_users_file(full_path: str, nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Reads the CSV file for the given path into a Pandas DataFrame.

    Parameters
    ----------
    full_path: str
        The full path of the file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    return _read_csv(full_path, nrows, DataTypes.USERS)


def get_all_system_activities(
    base_directory: str, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the most recent system activities files into a Pandas DataFrame.
    Combines data from the latest file in all existing directories and
    removes duplicates.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    files = fr.get_system_activities_files(base_directory)

    if files is None or len(files) == 0:
        return _default()

    df_list = list()
    for f in files:
        df_list.append(read_system_activities_file(f, nrows))

    df = pd.concat(df_list)
    df.drop_duplicates(inplace=True)

    return df  # type: ignore


def read_system_activities_file(
    full_path: str, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the CSV file for the given path into a Pandas DataFrame.

    Parameters
    ----------
    full_path: str
        The full path of the file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    data_types = {
        "LMSUserSourceSystemIdentifier": "string",
        "ActivityType": "string",
        "ActivityStatus": "string",
        "ParentSourceSystemIdentifier": "string",
        "ActivityTimeInMinutes": "Int64",
    }

    extra_date_columns = ["ActivityDateTime"]

    return _read_csv(
        full_path,
        nrows,
        data_types=data_types,
        extra_date_columns=extra_date_columns,
    )


def get_all_sections(base_directory: str, nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Reads the most recent sections file into a Pandas DataFrame.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    file = fr.get_sections_file(base_directory)

    if file is None:
        return _default()

    return read_sections_file(file, nrows=nrows)


def read_sections_file(full_path: str, nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Reads the CSV file for the given path into a Pandas DataFrame.

    Parameters
    ----------
    full_path: str
        The full path of the file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    return _read_csv(full_path, nrows, DataTypes.SECTIONS)


def get_section_associations(
    base_directory: str, section_id: int, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the most recent section associations file for the given section into
    a Pandas DataFrame.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    section_id: int
        Section identifier.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    file = fr.get_section_associations_file(base_directory, section_id)

    if file is None:
        return _default()

    return read_section_associations_file(file, nrows)


def read_section_associations_file(
    full_path: str, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the CSV file for the given path into a Pandas DataFrame.

    Parameters
    ----------
    full_path: str
        The full path of the file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    data_types = {
        "EnrollmentStatus": "string",
        "LMSSectionSourceSystemIdentifier": "string",
        "LMSUserSourceSystemIdentifier": "string",
    }

    return _read_csv(full_path, nrows, data_types=data_types)


def _get_data_for_section(
    base_directory: str,
    sections: pd.DataFrame,
    callback: Callable[[str, int, Optional[int]], pd.DataFrame],
    nrows: Optional[int] = None,
) -> pd.DataFrame:
    df = pd.DataFrame()

    if sections.empty:
        logger.info(
            "No sections have been loaded, therefore no section sub-files can be read."
        )
        return _default()

    for _, section_id in sections[[Keys.SOURCE_SYSTEM_IDENTIFIER]].itertuples():
        sa = callback(base_directory, section_id, nrows)

        if not sa.empty:
            df = df.append(sa)

    return df


def get_all_section_associations(
    base_directory: str, sections: pd.DataFrame, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the most recent section associations files for all given sections into
    a Pandas DataFrame.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    sections: pd.DataFrame
        DataFrame containing sections read from a sections file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    return _get_data_for_section(
        base_directory, sections, get_section_associations, nrows
    )


def get_section_activities(
    base_directory: str, section_id: int, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the most recent section activities file for the given section into
    a Pandas DataFrame.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    section_id: int
        Section identifier.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    file = fr.get_section_activities_file(base_directory, section_id)

    if file is None:
        return _default()

    return read_section_activities_file(file, nrows)


def read_section_activities_file(
    full_path: str, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the CSV file for the given path into a Pandas DataFrame.

    Parameters
    ----------
    full_path: str
        The full path of the file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    data_types = {
        "LMSSectionSourceSystemIdentifier": "string",
        "LMSUserSourceSystemIdentifier": "string",
        "ActivityType": "string",
        "ActivityStatus": "string",
        "ParentSourceSystemIdentifier": "string",
        "ActivityTimeInMinutes": "Int64",
    }

    extra_date_columns = ["ActivityDateTime"]

    return _read_csv(
        full_path,
        nrows,
        data_types=data_types,
        extra_date_columns=extra_date_columns,
    )


def get_all_section_activities(
    base_directory: str, sections: pd.DataFrame, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the most recent section activities files for all given sections into
    a Pandas DataFrame.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    sections: pd.DataFrame
        DataFrame containing sections read from a sections file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    return _get_data_for_section(
        base_directory, sections, get_section_activities, nrows
    )


def get_assignments(
    base_directory: str, section_id: int, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the most recent assignments file for the given section into
    a Pandas DataFrame.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    section_id: int
        Section identifier.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    file = fr.get_assignments_file(base_directory, section_id)

    if file is None:
        return _default()

    return read_assignments_file(file, nrows)


def read_assignments_file(full_path: str, nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Reads the CSV file for the given path into a Pandas DataFrame.

    Parameters
    ----------
    full_path: str
        The full path of the file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    return _read_csv(full_path, nrows)


def get_all_assignments(
    base_directory: str, sections: pd.DataFrame, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the most recent assignments files for all given sections into
    a Pandas DataFrame.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    sections: pd.DataFrame
        DataFrame containing sections read from a sections file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    return _get_data_for_section(base_directory, sections, get_assignments, nrows)


def get_submissions(
    base_directory: str,
    section_id: int,
    assignment_id: int,
    nrows: Optional[int] = None,
) -> pd.DataFrame:
    """
    Reads the most recent submissions file for the given section into
    a Pandas DataFrame.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    section_id: int
        Section identifier.
    assignment_id: int
        Assignment identifier.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    file = fr.get_submissions_file(base_directory, section_id, assignment_id)

    if file is None:
        return _default()

    return read_submissions_file(file, nrows)


def read_submissions_file(full_path: str, nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Reads the CSV file for the given path into a Pandas DataFrame.

    Parameters
    ----------
    full_path: str
        The full path of the file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    data_types = {
        "Grade": "string",
        "AssignmentSourceSystemIdentifier": "string",
        "LMSUserSourceSystemIdentifier": "string",
        "SubmissionStatus": "string",
        "EarnedPoints": "Int64",
    }

    extra_date_columns = ["SubmissionDateTime"]

    return _read_csv(
        full_path,
        nrows,
        data_types=data_types,
        extra_date_columns=extra_date_columns,
    )


def get_all_submissions(
    base_directory: str, assignments: pd.DataFrame, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the most recent section associations files for all given sections into
    a Pandas DataFrame.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    assignments: pd.DataFrame
        DataFrame containing assignments read from an assignments file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """

    if assignments.empty:
        logger.info(
            "No assignments have been loaded, therefore no submission files can be read."
        )
        return _default()

    df = pd.DataFrame()
    columns = [Keys.SOURCE_SYSTEM_IDENTIFIER, Keys.LMS_SECTION_SOURCE_SYSTEM_IDENTIFIER]
    for _, assignment_id, section_id in assignments[columns].itertuples():
        s = get_submissions(base_directory, section_id, assignment_id, nrows)

        if not s.empty:
            df = df.append(s)

    return df


def get_grades(
    base_directory: str, section_id: int, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the most recent grades file for the given section into
    a Pandas DataFrame.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    section_id: int
        Section identifier.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    file = fr.get_grades_file(base_directory, section_id)

    if file is None:
        return _default()

    return read_grades_file(file, nrows)


def read_grades_file(full_path: str, nrows: Optional[int] = None) -> pd.DataFrame:
    """
    Reads the CSV file for the given path into a Pandas DataFrame.

    Parameters
    ----------
    full_path: str
        The full path of the file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    return _read_csv(full_path, nrows)


def get_all_grades(
    base_directory: str, sections: pd.DataFrame, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the most recent grades files for all given sections into
    a Pandas DataFrame.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    sections: pd.DataFrame
        DataFrame containing sections read from a sections file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    return _get_data_for_section(base_directory, sections, get_grades, nrows)


def get_attendance_events(
    base_directory: str, section_id: int, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the most recent attendance events file for the given section into
    a Pandas DataFrame.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    section_id: int
        Section identifier.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    file = fr.get_attendance_events_file(base_directory, section_id)

    if file is None:
        return _default()

    return read_attendance_events_file(file, nrows)


def read_attendance_events_file(
    full_path: str, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the CSV file for the given path into a Pandas DataFrame.

    Parameters
    ----------
    full_path: str
        The full path of the file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """

    data_types = {
        "LMSUserSourceSystemIdentifier": "string",
        "LMSSectionSourceSystemIdentifier": "string",
        "AttendanceStatus": "string",
    }

    extra_date_columns = ["EventDate"]

    return _read_csv(full_path, nrows, data_types, extra_date_columns)


def get_all_attendance_events(
    base_directory: str, sections: pd.DataFrame, nrows: Optional[int] = None
) -> pd.DataFrame:
    """
    Reads the most recent attendance events files for all given sections into
    a Pandas DataFrame.

    Parameters
    ----------
    base_directory: str
        The base / parent directory for LMS extractor files.
    sections: pd.DataFrame
        DataFrame containing sections read from a sections file.
    nrows: int or None
        (Optional) number of rows to read from the file - useful for testing
        without reading the entirety of a large file.

    Returns
    -------
    Pandas DataFrame with columns matching the model definition / CSV file.
    """
    return _get_data_for_section(base_directory, sections, get_attendance_events, nrows)
