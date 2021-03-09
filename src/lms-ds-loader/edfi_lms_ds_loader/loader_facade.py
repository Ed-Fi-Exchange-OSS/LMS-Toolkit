# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

# Developer note: this module is deliberately not unit tested. As a facade it is
# by definition complex. In this application, it contains the main application
# logic and is tested simply by running the application. Any branching or
# looping logic should go into other modules where they can be tested easily.

import logging

from edfi_lms_ds_loader.helpers.constants import Table
from edfi_lms_ds_loader.helpers.argparser import MainArguments
from edfi_lms_ds_loader.migrator import migrate
from edfi_lms_file_utils import file_reader
from edfi_lms_ds_loader.df_to_db import upload_file
from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations

logger = logging.getLogger(__name__)


def _load_users(csv_path: str, db_adapter: MssqlLmsOperations) -> None:

    # TODO: enhance get_all_users to log name of the file
    users = file_reader.get_all_users(csv_path)
    upload_file(db_adapter, users, Table.USER)


# TODO: add more functions like _load_sections(...) here. And delete this
# comment once that pattern has been followed.


def run_loader(arguments: MainArguments) -> None:
    logger.info("Begin loading files into the LMS Data Store (DS)...")

    migrate(arguments.get_db_engine())

    csv_path = arguments.csv_path
    db_adapter = arguments.get_db_operations_adapter()

    _load_users(csv_path, db_adapter)

    # TODO: add more upload function calls here

    logger.info("Done loading files into the LMS Data Store.")
