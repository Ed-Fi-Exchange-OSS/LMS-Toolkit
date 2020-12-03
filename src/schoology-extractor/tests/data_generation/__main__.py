# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from sys import stdout, argv

from dotenv import load_dotenv
from tests.data_generation.users import generate_and_load_users
from schoology_extractor.api.request_client import RequestClient
from schoology_extractor.helpers import arg_parser

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

NUMBER_OF_USERS = 60

generate_and_load_users(RequestClient(arguments.client_key, arguments.client_secret), NUMBER_OF_USERS)
