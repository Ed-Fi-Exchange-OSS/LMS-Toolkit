# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict, List
from pandas import DataFrame


def to_df(canvas_objects: List) -> DataFrame:
    """
    Converts a list of canvas objects to a DataFrame

    Parameters
    ----------
    canvas_objects: List[CanvasObject]
        a list of CanvasObjects

    Returns
    -------
    DataFrame
        a DataFrame with the data from the canvas objects
    """
    return DataFrame.from_records(canvas_objects).astype("string")


def remove_duplicates(list: List, identity_property: str) -> List:
    """
    Remove duplicate objects from a list, using a property as the object identity

    Parameters
    ----------
    list: List
        a list of dicts
    identity_property: str
        the name of the index to use as the object identity

    Returns
    -------
    List
        a list of objects with duplicates removed
    """
    unique_dict: Dict = dict()
    for item in list:
        if item[identity_property] not in unique_dict:
            unique_dict[item[identity_property]] = item
    return [*unique_dict.values()]
