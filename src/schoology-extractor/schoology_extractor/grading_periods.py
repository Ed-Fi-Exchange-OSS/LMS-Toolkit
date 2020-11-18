# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import Any, List
import sys

from schoology_extractor.helpers import csv_writer, arg_parser
from schoology_extractor.api.request_client import RequestClient

# Parse arguments
arguments = arg_parser.parse_grading_periods_arguments(sys.argv[1:])
# Parameters are validated in the parse_grading_periods_arguments function
schoology_key = arguments.client_key
schoology_secret = arguments.client_secret
log_level = arguments.log_level

# Configure logging
logFormatter = '%(asctime)s - %(levelname)s - %(message)s'

logging.basicConfig(
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
    format=logFormatter,
    level=log_level,
)
logger = logging.getLogger(__name__)

logger.info("Ed-Fi LMS Schoology Extractor - Grading Periods")
request_client = RequestClient(schoology_key, schoology_secret)

logger.info("Getting grading periods")

try:

    grading_periods_list: List[Any] = []
    grading_periods_response = request_client.get_grading_periods()
    while True:
        grading_periods_list = (
            grading_periods_list + grading_periods_response.current_page_items
        )
        if grading_periods_response.get_next_page() is None:
            break
    print(csv_writer.to_string(grading_periods_list))

except Exception as ex:
    logger.error("An exception occurred while getting the Grading Periods: %s", ex)
