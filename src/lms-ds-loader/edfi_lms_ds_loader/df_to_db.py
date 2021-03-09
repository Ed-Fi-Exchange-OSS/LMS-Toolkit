# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging

import pandas as pd

from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations

logger = logging.getLogger(__name__)


def upload_file(db_adapter: MssqlLmsOperations, df: pd.DataFrame, table: str) -> None:
    """
    Uploads a DataFrame to the designated LMS table

    Parameters
    ----------
    db_adapter: MssqlLmsOperations
        Database engine-specific adapter/wrapper for database operations.
    df: pd.DataFrame
        A DataFrame to upload.
    table: str
        The destination table.
    """

    logger.info(f"Uploading {table} file ...")

    db_adapter.disable_staging_natural_key_index(table)
    db_adapter.truncate_staging_table(table)
    db_adapter.insert_into_staging(df, table)

    columns = list(df.columns)

    db_adapter.insert_new_records_to_production(table, columns)
    db_adapter.copy_updates_to_production(table, columns)

    sourceSystem = df.iloc[0]["SourceSystem"]
    db_adapter.soft_delete_from_production(table, sourceSystem)

    db_adapter.enable_staging_natural_key_index(table)

    logger.info(f"Done with {table} file.")
