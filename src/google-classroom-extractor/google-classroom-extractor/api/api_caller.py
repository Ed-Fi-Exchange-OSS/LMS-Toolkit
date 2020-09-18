import logging
from typing import List, Dict, Optional, Callable, cast
from requests import RequestException
from opnieuw import retry
from tail_recursive import tail_recursive


@retry(
    retry_on_exceptions=(IOError, RequestException),
    max_calls_total=4,
    retry_window_after_first_call_in_seconds=60,
)
def execute(executable_resource):
    return executable_resource.execute()


@tail_recursive
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
    current_results: List[Dict[str, str]] = [] if results is None else results
    response = execute(resource_method(**resource_parameters))
    try:
        current_results.extend(response.get(response_property, []))
    except (IOError, RequestException):
        logging.exception("Error during API call after retries.  Will try to continue.")
        return current_results

    next_page_token = response.get("nextPageToken", None)
    if not next_page_token:
        return current_results
    resource_parameters["pageToken"] = next_page_token
    return cast(
        List[Dict[str, str]],
        call_api.tail_call(
            resource_method, resource_parameters, response_property, current_results
        ),
    )
