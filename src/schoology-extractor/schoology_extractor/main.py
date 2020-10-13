# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import os
from typing import Callable
import sys

from dotenv import load_dotenv

from helpers import export_data
from api.request_client import RequestClient
from helpers import arg_parser
from facade import Facade

# Load configuration
load_dotenv()

arguments = arg_parser.parse_main_arguments(sys.argv[1:])
# Parameters are validated in the parse_main_arguments function
schoology_key = arguments.client_key
schoology_secret = arguments.client_secret
schoology_output_path = arguments.output_directory
schoology_grading_periods = arguments.grading_period
log_level = arguments.log_level
page_size = arguments.page_size

# Configure logging
logFormatter = "%(asctime)s - %(levelname)s - %(message)s"

logging.basicConfig(
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
    format=logFormatter,
    level=log_level,
)

logger = logging.getLogger(__name__)

grading_periods = schoology_grading_periods.split(",")
request_client = RequestClient(schoology_key, schoology_secret)
facade = Facade(logger, request_client, page_size)
closure = {}


def _create_file_from_dataframe(action: Callable, file_name):
    logger.info(f"Exporting {file_name}")
    try:
        data = action()
        export_data.df_to_csv(data, os.path.join(schoology_output_path, file_name))
    except Exception as ex:
        logger.error(
            f"An exception occurred while generating {file_name} : %s",
            ex,
        )


def _create_file_from_list(action: Callable, file_name):
    logger.info(f"Exporting {file_name}")
    try:
        data = action()
        export_data.to_csv(data, os.path.join(schoology_output_path, file_name))
    except Exception as ex:
        logger.error(
            f"An exception occurred while generating {file_name} : %s",
            ex,
        )


def _export_sections():
    sections = facade.get_sections()
    closure["sections"] = sections
    return sections


def _export_assignments():
    assignments = facade.get_assignments(closure["sections"], grading_periods)
    closure["assignments"] = assignments
    return assignments


def _export_submissions():
    return facade.get_submissions(closure["assignments"])


def main():
    _create_file_from_dataframe(facade.get_users, "users.csv")
    _create_file_from_list(_export_sections, "sections.csv")
    _create_file_from_list(_export_assignments, "assignments.csv")
    _create_file_from_list(_export_submissions, "submissions.csv")


if __name__ == "__main__":
    logger.info("Starting Ed-Fi LMS Schoology Extractor")
    main()
