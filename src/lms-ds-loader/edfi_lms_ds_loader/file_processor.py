# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
import logging
from typing import Type


from edfi_lms_ds_loader.csv_to_sql import CsvToSql
from edfi_lms_ds_loader.helpers.constants import Table, Columns
from edfi_lms_ds_loader.lms_filesystem_provider import LmsFilesystemProvider
from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations

logger = logging.getLogger(__name__)


@dataclass
class FileProcessor:
    """
    Processes all files in the LMS-UDM compatible file system and calls a
    program to read and load them into a database.

    Parameters
    ----------
    file_system : LmsFilesystemProvider
        A fully-prepared instance of `LmsFilesystemProvider`.
    db_operations_adapter : object
        Database provider-specific adapter/wrapper for database operations.
    """

    file_system: LmsFilesystemProvider

    # TODO: replace `MssqlLmsOperations` once a base class is extracted for
    # support of both MSSQL and PostgreSQL.
    db_operations_adapter: Type[MssqlLmsOperations]

    def load_lms_files_into_database(self):
        """
        Orchestrates the discovery and loading of files.
        """

        assert (
            isinstance(self.file_system, LmsFilesystemProvider)
        ), "Property `file_system` must be a `LmsFilesystemProvider`"
        assert (
            isinstance(self.db_operations_adapter, MssqlLmsOperations)
        ), "Property `db_operations_adapter` must be a `MssqlLmsOperations`"

        csv_to_sql = CsvToSql(self.db_operations_adapter)

        logger.info("Begin processing User files...")
        for f in self.file_system.Users:
            csv_to_sql.load_file(f, Table.USER, Columns.USER)

        logger.info("Done processing User files.")
