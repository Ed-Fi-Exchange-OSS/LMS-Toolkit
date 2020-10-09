# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import logging


def df_to_csv(df: pd.DataFrame, output_path: str):
    """
    Exports a DataFrame to CSV

    Parameters
    ----------
    df : DataFrame
        The data that will be exported to csv.
    output_path : str
        The path and name where you want your csv to be generated.

    """
    assert isinstance(df, pd.DataFrame), "Argument `df` should be a DataFrame"
    assert isinstance(output_path, str), "Argument `output_path` should be a string"
    assert len(output_path.strip()) > 0, "Argument `output_path` should not be whitespaces"

    df.to_csv(output_path, index=False)
    logging.info("The file has been generated => %s" % output_path)


def to_csv(data: list, output_path: str):
    """
        Exports the data to csv

        Parameters
        ----------
        data : list
            The data that will be exported to csv.
        output_path : str
            The path and name where you want your csv to be generated.

    """
    assert isinstance(data, list)
    assert isinstance(output_path, str)

    df = pd.DataFrame(data)
    df_to_csv(df, output_path)


def to_string(data: list) -> str:
    """
    Exports the data to string format

    Parameters
    ----------
    data : list
        The data that will be expoted to string.

    Returns
    -------
    str
        The information converted to string

    """
    assert isinstance(data, list)

    df = pd.DataFrame(data)
    return df.to_string()
