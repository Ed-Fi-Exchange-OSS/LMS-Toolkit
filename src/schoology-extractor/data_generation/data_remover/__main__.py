# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from sys import stdout, argv

from dotenv import load_dotenv
from edfi_schoology_extractor.api.request_client import RequestClient
from edfi_schoology_extractor.helpers import arg_parser

from edfi_lms_file_utils import file_reader

# The purpose of this script is to remove ranges of sections and users from the
# Schoology sandbox that have been added by data generation, and that are causing
# slow sync times during manual testing

# Uses the output of a sync run to find section and user ids

load_dotenv()
arguments = arg_parser.parse_main_arguments(argv[1:])

logging.basicConfig(
    handlers=[
        logging.StreamHandler(stdout),
    ],
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level="INFO",
)
logger = logging.getLogger(__name__)

request_client: RequestClient = RequestClient(
    arguments.client_key, arguments.client_secret
)

# remove sections
sections_df = file_reader.get_all_sections(arguments.output_directory)
section_ids = sections_df["SourceSystemIdentifier"]
for section_id in section_ids:
    section_id_int: int = int(section_id)
    if section_id_int > 4680000000 and section_id_int < 4780000000:
        # delete
        request_client.delete("sections", str(section_id_int))
        logger.info("**** Deleted section with id %s", section_id_int)

# remove users
users_df = file_reader.get_all_users(arguments.output_directory)
user_ids = users_df["SourceSystemIdentifier"]
for user_id in user_ids:
    user_id_int: int = int(user_id)
    if user_id_int > 104281300 and user_id_int < 105000000:
        # delete
        request_client.delete("users", str(user_id_int))
        logger.info("**** Deleted user with id %s", user_id_int)
