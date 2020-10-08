# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict
import os
from datetime import datetime
from pandas import DataFrame


USERS_ROOT_DIRECTORY = "data/ed-fi-udm-lms/users/"
SECTIONS_ROOT_DIRECTORY = "data/ed-fi-udm-lms/sections/"
ASSIGNMENT_ROOT_DIRECTORY = "data/ed-fi-udm-lms/section={id}/assignments/"


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
    assert isinstance(df_to_write, DataFrame)
    assert isinstance(output_date, datetime)
    assert isinstance(directory, str)

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
    assert isinstance(dfs_to_write, dict)
    assert isinstance(output_date, datetime)
    assert isinstance(directory_template, str)
    assert "{id}" in directory_template

    for id_placeholder, df_to_write in dfs_to_write.items():
        directory: str = directory_template.format(id=id_placeholder)
        write_csv(df_to_write, output_date, directory)
