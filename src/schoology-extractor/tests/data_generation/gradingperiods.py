# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import Dict, List
from edfi_schoology_extractor.api.request_client import RequestClient


logger = logging.getLogger(__name__)


def get_gradingperiods(request_client: RequestClient) -> List[Dict]:
    """
    Get a list of grading periods via the Schoology API.

    Parameters
    ----------
    request_client : RequestClient
        A RequestClient initialized for access to the Schoology API

    Returns
    -------
    List[Dict]
        A list of JSON-like grading period objects from a GET all response
    """

    logger.info("Getting grading periods from Schoology API")
    get_response: List[Dict] = request_client.get("gradingperiods")["gradingperiods"]
    logger.info("Successfully retrieved %s grading periods", len(get_response))
    return get_response
