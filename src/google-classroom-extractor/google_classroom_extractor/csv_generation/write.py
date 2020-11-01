# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict, Tuple
import os
from datetime import datetime
from pandas import DataFrame


USERS_ROOT_DIRECTORY = "data/ed-fi-udm-lms/users/"
SECTIONS_ROOT_DIRECTORY = "data/ed-fi-udm-lms/sections/"
SECTION_ASSOCIATIONS_ROOT_DIRECTORY = "data/ed-fi-udm-lms/section={id}/section-associations/"
ASSIGNMENT_ROOT_DIRECTORY = "data/ed-fi-udm-lms/section={id}/assignments/"
SUBMISSION_ROOT_DIRECTORY = "data/ed-fi-udm-lms/section={id1}/assignment={id2}/submissions/"
USER_ACTIVITY_ROOT_DIRECTORY = "data/ed-fi-udm-lms/section={id}/user-activities/"


def write_csv(df_to_write: DataFrame, output_date: datetime, directory: str):
    """
    Write a LMS UDM DataFrame to a CSV file

    Parameters
    ----------
    df_to_write: DataFrame
        is a LMS UDM DataFrame
    output_date: datetime
        is the timestamp for the filename
    directory: str
        is the directory the file will go in
    """
    os.makedirs(directory, exist_ok=True)
    filename: str = output_date.strftime("%Y-%m-%d-%H-%M-%S")
    df_to_write.to_csv(os.path.join(directory, f"{filename}.csv"), index=False)


def write_multi_csv(
    dfs_to_write: Dict[str, DataFrame], output_date: datetime, directory_template: str
):
    """
    Write a series of LMS UDM DataFrames to CSV files

    Parameters
    ----------
    dfs_to_write: Dict[str, DataFrame]
        is a Dict of id/LMS UDM DataFrame pairs
    output_date: datetime
        is the timestamp for the filename
    directory_template: str
        is the directory the file will go in, with an {id} placeholder
    """
    assert "{id}" in directory_template

    for id_placeholder, df_to_write in dfs_to_write.items():
        directory: str = directory_template.format(id=id_placeholder)
        write_csv(df_to_write, output_date, directory)


def write_multi_tuple_csv(
    dfs_to_write: Dict[Tuple[str, str], DataFrame], output_date: datetime, directory_template: str
):
    """
    Write a series of LMS UDM DataFrames to CSV files

    Parameters
    ----------
    dfs_to_write: Dict[Tuple[str, str], DataFrame]
        is a Dict of 2 id tuples/LMS UDM DataFrame pairs
    output_date: datetime
        is the timestamp for the filename
    directory_template: str
        is the directory the file will go in, with an {id1} and an {id2} placeholder
    """
    assert "{id1}" in directory_template
    assert "{id2}" in directory_template

    for id_tuple, df_to_write in dfs_to_write.items():
        (id1, id2) = id_tuple
        directory: str = directory_template.format(id1=id1, id2=id2)
        write_csv(df_to_write, output_date, directory)
