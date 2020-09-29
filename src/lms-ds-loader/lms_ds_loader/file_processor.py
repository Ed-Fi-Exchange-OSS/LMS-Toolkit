# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from lms_ds_loader.csv_to_sql import CsvToSql
from lms_ds_loader.constants import Constants


class FileProcessor:
    """
    Processes all files in the LMS-UDM compatible file system and calls a
    program to read and load them into a database.

    Parameters
    ----------
    file_system : LmsFilesystemProvider
        A fully-prepared instance of `LmsFilesystemProvider`.
    connection_string : str
        Database connection string in PyODBC format.
    """

    def __init__(self, file_system, connection_string):
        assert file_system is not None, "file_system cannot be None"
        assert connection_string is not None, "connection_string cannot be None"
        assert (
            connection_string.strip() != ""
        ), "connection_string cannot be an empty string"

        self.file_system = file_system
        self.connection_string = connection_string

    def load_lms_files_into_database(self):
        """
        Orchestrates the discovery and loading of files.
        """
        csv_to_sql = CsvToSql(self.connection_string)

        for f in self.file_system.Users:
            csv_to_sql.load_file(f, Constants.Table.USER)
