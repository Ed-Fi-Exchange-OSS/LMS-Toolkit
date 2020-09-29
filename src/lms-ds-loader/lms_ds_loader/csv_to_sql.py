# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
from typing import Type

import pandas as pd

from lms_ds_loader.mssql_lms_operations import MssqlLmsOperations


@dataclass
class CsvToSql:
    """
    Reads a CSV file and loads it into a table.

    Parameters
    ----------
    db_operations_adapter : object
        Database provider-specific adapter/wrapper for database operations.
    """

    db_operations_adapter: Type[MssqlLmsOperations]

    def __post_init__(self):
        self.engine = None

    def load_file(self, file, table, columns):
        """
        Executes the file read and database upload process.

        Parameters
        ----------
        file : str
            Full path to a file to read.
        table : str
            Name of the destination table, assumed to be in an "lms" schema.
        """
        df = pd.read_csv(file)

        adapter = self.db_operations_adapter
        adapter.disable_staging_natural_key_index(table)
        adapter.truncate_staging_table(table)
        adapter.insert_into_staging(df, table)

        adapter.insert_new_records_to_production(table, columns)

        adapter.enable_staging_natural_key_index(table)
