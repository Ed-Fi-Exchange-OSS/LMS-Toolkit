# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict, List, cast
from canvasapi.canvas_object import CanvasObject
from pandas import DataFrame


def _to_dict(canvas_object: CanvasObject):
    """
    Converts a canvas object to a dict containing only the data values

    Parameters
    ----------
    canvas_object: CanvasObject
        a CanvasObject

    Returns
    -------
    Dict
        a Dict containing only the data value
    """
    dictionary = vars(canvas_object).copy()
    del dictionary["_requester"]
    return dictionary


def _to_dicts(canvas_objects: List[CanvasObject]) -> List[Dict]:
    """
    Converts a list of canvas objects to a list of dicts

    Parameters
    ----------
    canvas_objects: List[CanvasObject]
        a list of CanvasObjects

    Returns
    -------
    List[Dict]
        a list of Dicts
    """
    return list(map(_to_dict, canvas_objects))


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
    return DataFrame.from_records(
        _to_dicts(cast(List[CanvasObject], canvas_objects))
    ).astype("string")


def remove_duplicates(list: List, identity_property: str) -> List:
    """
    Remove duplicate objects from a list, using a property as the object identity

    Parameters
    ----------
    list: List
        a list of objects
    identity_property: str
        the name of the object property to use as the object identity

    Returns
    -------
    List
        a list of objects with duplicates removed
    """
    unique_dict: Dict = dict()
    for obj in list:
        if getattr(obj, identity_property) not in unique_dict:
            unique_dict[getattr(obj, identity_property)] = obj
    return [*unique_dict.values()]
