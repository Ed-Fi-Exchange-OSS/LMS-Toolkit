# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import os
from typing import Callable, Dict
import sys

from dotenv import load_dotenv

from schoology_extractor.helpers import export_data
from schoology_extractor.api.request_client import RequestClient
from schoology_extractor.helpers import arg_parser
from schoology_extractor.schoology_request_service import SchoologyRequestService

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
service = SchoologyRequestService(logger, request_client, page_size)


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


# TODO: this method should disappear when we finish converting all of the output
# to use the official CSV formats.
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


def _get_users():
    return service.get_users()


# This variable facilitates temporary storage of output results from one GET
# request that need to be used for creating another GET request.
result_bucket: Dict[str, list] = {}


def _get_sections() -> list:
    sections = service.get_sections()
    result_bucket["sections"] = sections
    return sections


def _get_assignments() -> list:
    assignments = service.get_assignments(result_bucket["sections"], grading_periods)
    result_bucket["assignments"] = assignments
    return assignments


def _get_submissions() -> list:
    return service.get_submissions(result_bucket["assignments"])


def main():
    _create_file_from_dataframe(_get_users, "users.csv")
    _create_file_from_list(_get_sections, "sections.csv")
    _create_file_from_list(_get_assignments, "assignments.csv")
    _create_file_from_list(_get_submissions, "submissions.csv")


if __name__ == "__main__":
    logger.info("Starting Ed-Fi LMS Schoology Extractor")
    main()
