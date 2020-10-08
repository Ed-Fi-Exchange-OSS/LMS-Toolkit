# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
from datetime import datetime
import pandas as pd  # type: ignore


USERS_ROOT_DIRECTORY = "data/ed-fi-udm-lms/users/"
SECTIONS_ROOT_DIRECTORY = "data/ed-fi-udm-lms/sections/"


def write_csv(df_to_write: pd.DataFrame, output_date: datetime, directory: str):
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
    assert isinstance(df_to_write, pd.DataFrame)
    assert isinstance(output_date, datetime)
    assert isinstance(directory, str)

    os.makedirs(directory, exist_ok=True)
    filename: str = output_date.strftime("%Y-%m-%d-%H-%M-%S")
    df_to_write.to_csv(os.path.join(directory, f"{filename}.csv"), index=False)
