# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Dict, List
from http import HTTPStatus


def validate_multi_status(multi_response: List[Dict]):
    """
    Confirm response codes for all elements of a bulk response.

    Parameters
    ----------
    multi_response : List[Dict]
        A list of JSON-like responses to each individual request.

    Raises
    -------
    RuntimeError
        If any individual operation had a non-OK response code.
    """
    if any(response["response_code"] != HTTPStatus.OK for response in multi_response):
        raise RuntimeError(str(multi_response))
