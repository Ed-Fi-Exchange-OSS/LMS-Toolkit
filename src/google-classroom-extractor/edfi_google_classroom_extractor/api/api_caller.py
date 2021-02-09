# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from collections import namedtuple
import logging
import os
from typing import List, Dict, Optional, Callable, cast
from requests import RequestException
from opnieuw import retry
from tail_recursive import tail_recursive
from googleapiclient.errors import Error as GoogleApiError

ResourceType = namedtuple("ValidSdkFunction", ["courses", "userUsageReport"])

MAX_TOTAL_CALLS = int(os.getenv("REQUEST_RETRY_COUNT") or 4)
RETRY_WINDOW_AFTER_FIRST_CALL_IN_SECONDS = int(
    os.environ.get("REQUEST_RETRY_TIMEOUT_SECONDS") or 60
)

logger = logging.getLogger(__name__)


@retry(
    retry_on_exceptions=(IOError, RequestException, GoogleApiError),
    max_calls_total=MAX_TOTAL_CALLS,
    retry_window_after_first_call_in_seconds=RETRY_WINDOW_AFTER_FIRST_CALL_IN_SECONDS,
)
def _execute(executable_resource):
    """
    Invoke a get/list Google Classroom SDK function,
    retrying if there are errors.

    Parameters
    ----------
    executable_resource: function
        is the get/list Google Classroom SDK function to call

    Returns
    -------
    object
        a Google Classroom SDK response object

    Raises
    ------
    IOError
        if there is an IOError after retrying
    RequestException
        if there is a RequestException after retrying
    """
    assert hasattr(executable_resource, "execute")
    return executable_resource.execute()


@tail_recursive
def _call_api_recursive(
    resource_method: Callable,
    resource_parameters: Dict[str, str],
    response_property: str,
    results: Optional[List[Dict[str, str]]] = None,
) -> List[Dict[str, str]]:
    """
    Call a Google Classroom/Admin SDK API

    Parameters
    ----------
    resource_method: function
        is the get/list SDK function to call
    resource_parameters: dict
        is the parameters for get/list
    response_property: string
        is the property in the API response we want
    results: list
        is the list of dicts of the API response accumulated across pages

    Returns
    -------
    list
        a list of dicts of the API response property requested
    """

    current_results: List[Dict[str, str]] = [] if results is None else results
    response = _execute(resource_method(**resource_parameters))
    try:
        current_results.extend(response.get(response_property, []))
    except (IOError, RequestException, GoogleApiError):
        logger.exception("Error during API call after retries.  Will try to continue.")
        return current_results

    next_page_token = response.get("nextPageToken", None)
    if not next_page_token:
        return current_results
    resource_parameters["pageToken"] = next_page_token
    return cast(
        List[Dict[str, str]],
        _call_api_recursive.tail_call(
            resource_method, resource_parameters, response_property, current_results
        ),
    )


def call_api(
    resource_method: Callable,
    resource_parameters: Dict[str, str],
    response_property: str,
    results: Optional[List[Dict[str, str]]] = None,
) -> List[Dict[str, str]]:
    """
    Call a Google Classroom/Admin SDK API

    Parameters
    ----------
    resource_method: function
        is the get/list SDK function to call
    resource_parameters: dict
        is the parameters for get/list
    response_property: string
        is the property in the API response we want
    results: list
        is the list of dicts of the API response accumulated across pages

    Returns
    -------
    list
        a list of dicts of the API response property requested
    """

    return _call_api_recursive(resource_method, resource_parameters, response_property, results)  # type: ignore
