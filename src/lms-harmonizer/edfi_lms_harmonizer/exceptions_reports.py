# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
from logging import getLogger
from os import path, makedirs

import pandas as pd

from edfi_lms_extractor_lib.helpers.decorators import catch_exceptions
from edfi_sql_adapter.sql_adapter import Adapter


logger = getLogger(__name__)

QUERY_FOR_SECTIONS = "SELECT * FROM edfilms.exceptions_LMSSection"
QUERY_FOR_SECTION_SUMMARY = """
SELECT
    COUNT(1) as UnmatchedCount
FROM
    edfilms.exceptions_LMSSection
    """
QUERY_FOR_USERS = "SELECT * FROM edfilms.exceptions_LMSUser"
QUERY_FOR_USERS_SUMMARY = """
SELECT
    COUNT(1) as UnmatchedCount
FROM
    edfilms.exceptions_LMSUser
    """
SECTIONS = "sections"
USERS = "users"


def _get_file_path(output_directory: str, report_type: str) -> str:
    dir_path = path.join(
        output_directory, report_type
    )

    makedirs(dir_path, exist_ok=True)

    file_path = path.join(dir_path, f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv")

    return file_path


@catch_exceptions
def print_summary(adapter: Adapter) -> None:
    sections_count = adapter.get_int(QUERY_FOR_SECTION_SUMMARY)
    users_count = adapter.get_int(QUERY_FOR_USERS_SUMMARY)

    if sections_count > 0 or users_count > 0:
        logger.warning(
            f"There are {sections_count} unmatched sections and {users_count} "
            f"unmatched users in the database."
        )
    else:
        logger.info("There are no unmatched sections or users in the database.")


@catch_exceptions
def create_exception_reports(adapter: Adapter, output_directory: str) -> None:
    logger.info("Writing the Sections exception report")
    sections = pd.read_sql(QUERY_FOR_SECTIONS, adapter.engine)
    sections.to_csv(_get_file_path(output_directory, SECTIONS), index=False)

    logger.info("Writing the Users exception report")
    users = pd.read_sql(QUERY_FOR_USERS, adapter.engine)
    users.to_csv(_get_file_path(output_directory, USERS), index=False)
