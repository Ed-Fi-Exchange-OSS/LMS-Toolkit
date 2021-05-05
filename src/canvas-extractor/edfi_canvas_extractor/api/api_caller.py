# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Callable
from canvasapi.exceptions import CanvasException
from requests import RequestException
import socket
from opnieuw import retry

MAX_TOTAL_CALLS = 4
RETRY_WINDOW_AFTER_FIRST_CALL_IN_SECONDS = 60


@retry(
    retry_on_exceptions=(
        IOError,
        CanvasException,
        RequestException,
        socket.timeout,
        socket.error,
    ),
    max_calls_total=MAX_TOTAL_CALLS,
    retry_window_after_first_call_in_seconds=RETRY_WINDOW_AFTER_FIRST_CALL_IN_SECONDS,
)
def call_with_retry(canvas_api_function: Callable, **kwargs):
    """
    Invoke a get/list/etc Canvas SDK function that takes kwargs,
    retrying if there are errors.

    Parameters
    ----------
    executable_resource: Callable
        is the get/list/etc Canvas SDK function to call
    kwargs: Dict
        arguments to pass to the Canvas SDK function

    Returns
    -------
    object
        a Canvas SDK response object

    Raises
    ------
    IOError
        if there is an IOError after retrying
    CanvasException
        if there is a CanvasException after retrying
    """

    return canvas_api_function(**kwargs)
