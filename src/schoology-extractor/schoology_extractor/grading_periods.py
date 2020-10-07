# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import os
from typing import Any, List
import sys

from dotenv import load_dotenv

from helpers import export_data
from api.request_client import RequestClient

load_dotenv()
# Configure logger
log_level = os.getenv("SCHOOLOGY_LOG_LEVEL", "INFO")
assert log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], "The specified `SCHOOLOGY_LOG_LEVEL` is not valid"
logFormatter = '%(asctime)s - %(levelname)s - %(message)s'

logging.basicConfig(
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
    format=logFormatter,
    level=log_level
)
logger = logging.getLogger(__name__)

logger.debug("Loading and processing .env variables")
schoology_key = os.getenv("SCHOOLOGY_KEY")
schoology_secret = os.getenv("SCHOOLOGY_SECRET")
schoology_section_ids = os.getenv("SCHOOLOGY_SECTION_IDS")
schoology_output_path = os.getenv("SCHOOLOGY_OUTPUT_PATH")

assert schoology_key is not None, "A `SCHOOLOGY_KEY` must be present in the .env file and it was not found."
assert schoology_secret is not None, "A `SCHOOLOGY_SECRET` must be present in the .env file and it was not found."

logger.debug("Finished loading and processing .env variables")

request_client = RequestClient(schoology_key, schoology_secret)

logger.info("Getting grading periods")
grading_periods_list: List[Any] = []
grading_periods_response = request_client.get_grading_periods()
while True:
    grading_periods_list = grading_periods_list + grading_periods_response.current_page_items
    if grading_periods_response.get_next_page() is None:
        break

print(export_data.to_string(grading_periods_list))
logger.info("Finished getting grading periods")
