# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import os

from google.oauth2 import service_account
from sqlalchemy import create_engine
import sqlalchemy

SYNC_DATABASE_LOCATION = "data/sync.sqlite"


def _is_running_in_notebook() -> bool:
    main = __import__("__main__", None, None, fromlist=["__file__"])
    return not hasattr(main, "__file__")


def get_sync_db_engine() -> sqlalchemy.engine.base.Engine:
    running_in_notebook: bool = _is_running_in_notebook()
    logging.debug(f"Running in Jupyter Notebook: {running_in_notebook}")
    sync_database_uri = (
        f"sqlite:///../{SYNC_DATABASE_LOCATION}"
        if running_in_notebook
        else f"sqlite:///{SYNC_DATABASE_LOCATION}"
    )
    return create_engine(sync_database_uri)


def get_credentials() -> service_account.Credentials:
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
        filename, scopes=scopes, subject=os.getenv("CLASSROOM_ACCOUNT")
    )
