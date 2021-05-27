# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import List
import re

from pandas import DataFrame
import sqlalchemy
from canvasapi.authentication_event import AuthenticationEvent
from canvasapi.user import User
from canvasapi.paginated_list import PaginatedList
from opnieuw import retry

from .canvas_helper import to_df
from edfi_lms_extractor_lib.api.resource_sync import (
    cleanup_after_sync,
    sync_to_db_without_cleanup,
)
from edfi_canvas_extractor.config import RETRY_CONFIG


AUTH_EVENTS_RESOURCE_NAME = "Authentication_Events"

logger = logging.getLogger(__name__)


def _authentication_event_get_next_page(self: PaginatedList):
    """
    This is a monkeypatched version of the CanvasAPI 2.2.0
    PaginatedList._get_next_page function, modified to handle
    the fact that authentication events are in the response
    under "events".
    """
    response = self._requester.request(
        self._request_method, self._next_url, **self._next_params
    )
    data = response.json()
    self._next_url = None

    next_link = response.links.get("next")
    regex = r"{}(.*)".format(re.escape(self._requester.base_url))

    self._next_url = (
        re.search(regex, next_link["url"]).group(1) if next_link else None  # type: ignore
    )

    self._next_params = {}

    content = []

    if self._root:
        try:
            data = data[self._root]
        except KeyError:
            raise ValueError("Invalid root value specified.")

    # This is the change to the code, added to get to the events object in the response
    if "events" in data:
        data = data["events"]

    for element in data:
        if element is not None:
            element.update(self._extra_attribs)
            content.append(self._content_class(self._requester, element))

    return content


@retry(**RETRY_CONFIG)  # type: ignore
def request_events(
    users: List[User], start_date: str, end_date: str
) -> List[AuthenticationEvent]:
    """
    Fetch AuthenticationEvent API data for a range of users and return a list of AuthenticationEvent API objects

    Parameters
    ----------
    users: List[User]
        a list of Canvas User objects

    Returns
    -------
    List[AuthenticationEvent]
        a list of AuthenticationEvent API objects
    """
    logger.info("Pulling authentication events data")

    # enable monkeypatch of CanvasApi's PaginatedList._get_next_page
    original_get_next_page = PaginatedList._get_next_page
    PaginatedList._get_next_page = _authentication_event_get_next_page

    events: List[AuthenticationEvent] = []
    for user in users:
        local_events = user.get_authentication_events(
            start_time=start_date, end_time=end_date
        )
        events.extend(local_events)

    # revert monkeypatch
    PaginatedList._get_next_page = original_get_next_page

    return events


def authentication_events_synced_as_df(
    auth_events: List[AuthenticationEvent],
    sync_db: sqlalchemy.engine.base.Engine,
) -> DataFrame:
    """
    Fetch AuthenticationEvent API data for a range of courses and return a AuthenticationEvent API DataFrame
    with current and previously fetched data

    Parameters
    ----------
    auth_events: List[AuthenticationEvent]
        a list of Canvas AuthenticationEvent objects
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        an AuthenticationEvent API DataFrame with the current and previously fetched data
    """
    auth_events_df: DataFrame = _sync_without_cleanup(to_df(auth_events), sync_db)
    cleanup_after_sync(AUTH_EVENTS_RESOURCE_NAME, sync_db)

    return auth_events_df


def _sync_without_cleanup(
    resource_df: DataFrame, sync_db: sqlalchemy.engine.base.Engine
) -> DataFrame:
    """
    Take fetched API data and sync with database. Creates tables when necessary,
    but ok if temporary tables are there to start. Doesn't delete temporary tables when finished.

    Parameters
    ----------
    resource_df: DataFrame
        an AuthenticationEvent API DataFrame with the current fetched data which
        will be mutated, adding Hash and CreateDate/LastModifiedDate
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a DataFrame with current fetched data and reconciled CreateDate/LastModifiedDate
    """
    return sync_to_db_without_cleanup(
        resource_df=resource_df,
        identity_columns=["id"],
        resource_name=AUTH_EVENTS_RESOURCE_NAME,
        sync_db=sync_db,
    )
