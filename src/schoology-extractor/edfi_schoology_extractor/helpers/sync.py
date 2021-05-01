# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
import os
import logging
from typing import Any, Dict, List, Union

from pandas import DataFrame
import sqlalchemy
from sqlalchemy.engine import ResultProxy
from edfi_lms_extractor_lib.api.resource_sync import (
    cleanup_after_sync,
    sync_to_db_without_cleanup,
)

USAGE_TABLE_NAME = "USAGE_PROCESSED_FILES"

logger = logging.getLogger(__name__)


def get_sync_db_engine(sync_database_directory: str) -> sqlalchemy.engine.base.Engine:
    """
    Create a SQL Alchemy Engine for a SQLite file

    Returns
    -------
    sqlalchemy.engine.base.Engine
        a SQL Alchemy Engine
    """
    logger.debug(
        "Ensuring database directory at %s", os.path.abspath(sync_database_directory)
    )
    os.makedirs(sync_database_directory, exist_ok=True)

    return sqlalchemy.create_engine(f"sqlite:///{sync_database_directory}/sync.sqlite")


def sync_resource(
    resource_name: str,
    db_engine: sqlalchemy.engine.base.Engine,
    data: List[Dict[str, Any]],
    id_column: str = "id",
) -> DataFrame:
    if len(data) == 0:
        return DataFrame()
    resource_df: DataFrame = DataFrame(data)

    synced_df = sync_to_db_without_cleanup(
        resource_df=resource_df,
        identity_columns=[id_column],
        resource_name=resource_name,
        sync_db=db_engine,
    )
    cleanup_after_sync(resource_name, db_engine)
    return synced_df


def _table_exist(
    table_name: str,
    db_engine: sqlalchemy.engine.base.Engine,
) -> bool:
    with db_engine.connect() as con:
        result: Union[ResultProxy, None] = con.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name=?;
        """,
            (table_name,),
        )

        if result is None:
            return False
        if result.first() is None:
            return False
        return True


def _create_usage_table_if_it_does_not_exist(db_engine: sqlalchemy.engine.base.Engine) -> None:
    if _table_exist(USAGE_TABLE_NAME, db_engine) is False:
        db_engine.execute(
            f"""CREATE TABLE {USAGE_TABLE_NAME} (
            FILE_NAME TEXT PRIMARY KEY
        );"""
        )


def _map_result_to_dicts_arr(result: Union[ResultProxy, None]) -> List[Dict[str, Any]]:
    if result is None:
        return list()

    return [dict(row.items()) for row in result]


def _map_single_result_to_dict(result: Union[ResultProxy, None]) -> Dict[str, Any]:
    mapped_result = _map_result_to_dicts_arr(result)
    return mapped_result[0] if len(mapped_result) > 0 else dict()


def usage_file_is_processed(
    file_name: str, db_engine: sqlalchemy.engine.base.Engine
) -> bool:
    """
    Verifies if the current file has been previously processed

    Parameters
    ----------
    file_name: str
        Name of the file
    db_engine: sqlalchemy.engine.base.Engine

    Returns
    -------
    bool
        True if the file has been processed, False if it has not.
    """

    _create_usage_table_if_it_does_not_exist(db_engine)

    query = f"select exists(select 1 from {USAGE_TABLE_NAME} where FILE_NAME='{file_name}') as 'exists'"

    db_item = {"exists": False}
    with db_engine.connect() as con:
        result: Union[ResultProxy, None] = con.execute(query)
        db_item = _map_single_result_to_dict(result)

    return db_item["exists"] == 1


def insert_usage_file_name(
    file_name: str, db_engine: sqlalchemy.engine.base.Engine
) -> None:
    """
    Inserts the name of the file in the table for processed files

    Parameters
    ----------
    file_name: str
        Name of the file
    db_engine: sqlalchemy.engine.base.Engine

    Returns
    -------
    None
    """

    _create_usage_table_if_it_does_not_exist(db_engine)
    db_engine.execute(f"INSERT INTO {USAGE_TABLE_NAME} VALUES('{file_name}')")
