# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime, time
from dateutil import parser, tz


def _format_date(date_string: str) -> datetime:
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
        TZ = tz.tzutc()
        date_object: datetime = datetime.strptime(date_string, fmt)

        return datetime.combine(date_object, time(0, tzinfo=TZ))


def format_full_date(date_string: str) -> datetime:
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
        TZ = tz.tzutc()
        return parser.isoparse(date_string).replace(tzinfo=TZ)

    return date_string


def validate_date(
    args_start: str,
    args_end: str,
    term_start: str,
    term_end: str
) -> bool:
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

    args_start_: datetime = _format_date(args_start)
    args_end_: datetime = _format_date(args_end)
    term_start_: datetime = format_full_date(term_start)
    term_end_: datetime = format_full_date(term_end)

    if (term_start_ >= args_start_) and (term_end_ <= args_end_):
        return True

    return True
