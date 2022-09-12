# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import sqlalchemy
import sys

from canvasapi import Canvas
from canvasapi.account import Account
from datetime import datetime
from typing import List, Dict, Tuple

from edfi_canvas_extractor.config import get_canvas_api, get_sync_db_engine
from edfi_canvas_extractor.graphql.extract import Extract
from edfi_lms_extractor_lib.csv_generation.write import (
    write_sections,
)
from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions
from edfi_canvas_extractor.client_graphql import (
    extract_courses,
    extract_sections,
)
from edfi_canvas_extractor.helpers.arg_parser import MainArguments


logger = logging.getLogger(__name__)
results_store: Dict[str, Tuple] = {}


def _break_execution(failing_extraction: str) -> None:
    logger.critical(
        f"Unable to continue file generation because the load of {failing_extraction} failed. "
        "Please review the log for more information."
    )
    sys.exit(1)


@catch_exceptions
def _get_accounts(
    arguments: MainArguments,
    canvas: Canvas,
    sync_db: sqlalchemy.engine.base.Engine
) -> None:
    accounts: List[Account] = canvas.get_accounts()

    for account in accounts:
        _id = getattr(account, "id")
        gql = Extract()
        gql.set_account(_id)
        gql.set_dates(arguments.start_date, arguments.end_date)
        gql.run()

    succeeded: bool = True

    succeeded = _get_courses(gql, sync_db)

    if not succeeded:
        _break_execution("Courses")

    succeeded = _get_sections(arguments, gql, sync_db)

    if not succeeded:
        _break_execution("Sections")


@catch_exceptions
def _get_courses(
    gql: Extract,
    sync_db: sqlalchemy.engine.base.Engine
) -> None:
    logger.info("Extracting Courses from Canvas")

    (courses, courses_df) = extract_courses(
        gql, sync_db
    )

    results_store["courses"] = (courses, courses_df)


@catch_exceptions
def _get_sections(
    arguments: MainArguments,
    gql: Extract,
    sync_db: sqlalchemy.engine.base.Engine
) -> None:
    logger.info("Extracting Sections from Canvas")
    (sections, udm_sections_df, all_section_ids) = extract_sections(gql, sync_db)
    logger.info("Writing LMS UDM Sections to CSV file")
    write_sections(udm_sections_df, datetime.now(), arguments.output_directory)
    results_store["sections"] = (sections, udm_sections_df, all_section_ids)


def run(arguments: MainArguments) -> None:
    logger.info("Starting Ed-Fi LMS Canvas Extractor")
    sync_db: sqlalchemy.engine.base.Engine = get_sync_db_engine(
        arguments.sync_database_directory
    )
    canvas: Canvas = get_canvas_api(arguments.base_url, arguments.access_token)
    _get_accounts(arguments, canvas, sync_db)

    logger.info("Finishing Ed-Fi LMS Canvas Extractor")
