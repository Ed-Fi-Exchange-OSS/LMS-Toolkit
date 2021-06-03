# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from sys import stdout
import sys
from dotenv import load_dotenv
from canvasapi import Canvas
from canvasapi.account import Account
from edfi_canvas_extractor.helpers import arg_parser
from edfi_canvas_extractor.config import get_canvas_api
from edfi_lms_file_utils import file_reader

load_dotenv()

logging.basicConfig(
    handlers=[
        logging.StreamHandler(stdout),
    ],
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level="INFO",
)
logger = logging.getLogger(__name__)
arguments = arg_parser.parse_main_arguments(sys.argv[1:])


canvas: Canvas = get_canvas_api(arguments.base_url, arguments.access_token)
account: Account = canvas.get_accounts()[0]

sections_df = file_reader.get_all_sections(arguments.output_directory)
section_ids = sections_df["SourceSystemIdentifier"]

for section_id in section_ids:
    section_id_int: int = int(section_id)
    if section_id_int > 649 and section_id_int < 751:
        section_to_delete = canvas.get_section(section_id_int)
        # enrollments = section_to_delete.get_enrollments()

        # # delete enrollments
        # for enrollment in enrollments:
        #     enrollment.deactivate(task="delete")

        # delete section
        section_to_delete.delete()
        logger.info("**** Deleted section with id %s", section_id_int)

logger.info("**** Successfully deleted %s section", len(section_ids))

# remove users
# users_df = file_reader.get_all_users(arguments.output_directory)
# user_ids = users_df["SourceSystemIdentifier"]
# for user_id in user_ids:
#     user_id_int: int = int(user_id)
#     if user_id_int > 10000 and user_id_int < 50000:
#         # delete
#         account.delete_user(user_id_int)
#         logger.info("**** Deleted user with id %s", user_id_int)

# logger.info("**** Successfully deleted %s users", len(user_ids))
