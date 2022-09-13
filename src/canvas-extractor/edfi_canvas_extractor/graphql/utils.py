# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
from dateutil import parser


def _format_date(date_string: str) -> object:
    """
    Convert string to date object
    format "2021-02-22"

    Parameters
    ----------
    date_string: String

    Returns
    -------
    DateTime Object
    """

    if isinstance(date_string, str):
        fmt = "%Y-%m-%d"

        return datetime.strptime(date_string, fmt).replace(tzinfo=None)


def _format_full_date(date_string: str) -> object:
    """
    Convert string to date object from isoformats

    Parameters
    ----------
    date_string: String

    Returns
    -------
    DateTime Object
    """
    if isinstance(date_string, str):
        return parser.isoparse(date_string).replace(tzinfo=None)


def validate_date(args_start, args_end, term_start, term_end) -> bool:
    """
    Determine the courses between the range of
    date from the arguments

    Parameters
    ----------
    args_start: DateTime Object
    args_end: DateTime Object
    term_start: DateTime Object
    term_end: DateTime Object

    Returns
    -------
    True/False bool
    """

    args = list(map(_format_date, [args_start, args_end]))
    term = list(map(_format_full_date, [term_start, term_end]))

    if term[0] >= args[0] and term[1] <= args[1]:
        return True
