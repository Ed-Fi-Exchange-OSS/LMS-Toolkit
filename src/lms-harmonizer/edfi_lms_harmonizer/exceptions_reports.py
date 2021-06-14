# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
from logging import getLogger
from os import path

import pandas as pd
from sqlalchemy.engine.base import Engine as sa_Engine

from edfi_sql_adapter import sql_adapter


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
    return path.join(
        output_directory, report_type, f"{datetime.now().strftime('%Y-%m-%d')}"
    )


def get_summary(engine: sa_Engine) -> None:
    sections_count = sql_adapter.get_int(engine, QUERY_FOR_SECTION_SUMMARY)
    users_count = sql_adapter.get_int(engine, QUERY_FOR_USERS_SUMMARY)

    if sections_count > 0 or users_count > 0:
        logger.warn(
            f"There are {sections_count} unmatched sections and {users_count} "
            f"unmatched users in the database."
        )
    else:
        logger.info("There are no unmatched sections or users in the database.")


def create_files(engine: sa_Engine, output_directory: str) -> None:
    sections = pd.read_sql(QUERY_FOR_SECTIONS, engine)
    sections.to_csv(_get_file_path(output_directory, SECTIONS))

    users = pd.read_sql(QUERY_FOR_USERS, engine)
    users.to_csv(_get_file_path(output_directory, USERS))
