# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import os

from google.oauth2 import service_account
from sqlalchemy import create_engine
import sqlalchemy

SYNC_DATABASE_LOCATION_SUFFIX = "data"

logger = logging.getLogger(__name__)


def _is_running_in_notebook() -> bool:
    """
    Determine whether code is running in a Jupyter Notebook

    Returns
    -------
    bool
        True if code is running in a Jupyter Notebook
    """
    main = __import__("__main__", None, None, fromlist=["__file__"])
    return not hasattr(main, "__file__")


def get_sync_db_engine() -> sqlalchemy.engine.base.Engine:
    """
    Create a SQL Alchemy Engine for a SQLite file

    Returns
    -------
    sqlalchemy.engine.base.Engine
        a SQL Alchemy Engine
    """
    running_in_notebook: bool = _is_running_in_notebook()
    logger.debug("Running in Jupyter Notebook: %s", running_in_notebook)
    sync_database_directory = (
        os.path.join("..", SYNC_DATABASE_LOCATION_SUFFIX)
        if running_in_notebook
        else SYNC_DATABASE_LOCATION_SUFFIX
    )
    logger.debug("Ensuring database directory at %s", os.path.abspath(sync_database_directory))
    os.makedirs(sync_database_directory, exist_ok=True)
    return create_engine(f"sqlite:///{sync_database_directory}/sync.sqlite")


def get_credentials(classroom_account: str) -> service_account.Credentials:
    """
    Create a Google OAuth Credentials object from a service-account.json file

    Returns
    -------
    Credentials
        a Google OAuth Credentials object
    """
    scopes = [
        "https://www.googleapis.com/auth/admin.directory.orgunit",
        "https://www.googleapis.com/auth/admin.reports.usage.readonly",
        "https://www.googleapis.com/auth/classroom.courses",
        "https://www.googleapis.com/auth/classroom.coursework.students",
        "https://www.googleapis.com/auth/classroom.profile.emails",
        "https://www.googleapis.com/auth/classroom.rosters",
        "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
        "https://www.googleapis.com/auth/admin.reports.audit.readonly",
    ]

    filename = (
        "service-account.json"
        if os.path.exists("service-account.json")
        else "../service-account.json"
    )

    return service_account.Credentials.from_service_account_file(
        filename, scopes=scopes, subject=classroom_account
    )
