# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from dataclasses import dataclass
import logging
import os
from typing import List

import pandas as pd

from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations

logger = logging.getLogger(__name__)


@dataclass
class CsvToSql:
    """
    Reads a CSV file and loads it into a table.

    Parameters
    ----------
    db_operations_adapter : object
        Database provider-specific adapter/wrapper for database operations.
    """

    db_operations_adapter: MssqlLmsOperations

    def __post_init__(self) -> None:
        self.engine = None

    def load_file(self, file: str, table: str, columns: List[str]) -> None:
        """
        Executes the file read and database upload process.

        Parameters
        ----------
        file : str
            Full path to a file to read.
        table : str
            Name of the destination table, assumed to be in an "lms" schema.
        """

        if not os.path.exists(file):
            raise OSError(f"Path {file} does not exist.")
        assert table.strip() != "", "Argument `table` cannot be whitespace"
        assert len(columns) > 0, "Argument `columns` cannot be empty"

        logger.info(f"Processing file `{file}`...")
        df = pd.read_csv(file)
        logger.debug(f"... read {df.shape[0]} lines.")

        adapter = self.db_operations_adapter
        adapter.disable_staging_natural_key_index(table)
        adapter.truncate_staging_table(table)
        adapter.insert_into_staging(df, table)

        adapter.insert_new_records_to_production(table, columns)
        adapter.copy_updates_to_production(table, columns)

        sourceSystem = df.iloc[0]["SourceSystem"]
        adapter.soft_delete_from_production(table, sourceSystem)

        adapter.enable_staging_natural_key_index(table)
