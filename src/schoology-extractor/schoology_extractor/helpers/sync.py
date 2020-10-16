# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
import os
import logging
from typing import Optional

from pandas import DataFrame
import sqlalchemy

SYNC_DATABASE_LOCATION_SUFFIX = "data"


def get_sync_db_engine() -> sqlalchemy.engine.base.Engine:
    """
    Create a SQL Alchemy Engine for a SQLite file

    Returns
    -------
    sqlalchemy.engine.base.Engine
        a SQL Alchemy Engine
    """
    sync_database_directory = (os.path.join(SYNC_DATABASE_LOCATION_SUFFIX))
    logging.debug("Ensuring database directory at %s", os.path.abspath(sync_database_directory))
    os.makedirs(sync_database_directory, exist_ok=True)

    return sqlalchemy.create_engine(f"sqlite:///{sync_database_directory}/sync.sqlite")


def _write_resource_to_db(
    resource_name: str,
    db_engine: sqlalchemy.engine.base.Engine,
    data: DataFrame,
    column_mapping: Optional[dict] = None
):
    data.to_sql(
        resource_name, db_engine, if_exists="append", index=False, chunksize=500, dtype=column_mapping
    )
    pass


def sync_resource(
    resource_name: str,
    db_engine: sqlalchemy.engine.base.Engine,
    data: list,
    column_mapping: Optional[dict] = None
) -> DataFrame:
    df_data = DataFrame(data)
    _write_resource_to_db(resource_name, db_engine, df_data, column_mapping)

    return df_data
