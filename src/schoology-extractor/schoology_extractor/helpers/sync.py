# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from datetime import datetime
import os
import logging
from typing import Optional, Union

from pandas import DataFrame
import sqlalchemy
from sqlalchemy.engine import ResultProxy

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


def _get_current_date_with_format() -> str:
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")


def _resource_has_changed(
    resource: dict,
    resource_name: str,
    db_engine:  sqlalchemy.engine.base.Engine,
    id_column: str = "id"
) -> bool:
    query = f"SELECT * FROM {resource_name} where {id_column} = {resource[id_column]} limit 1;"
    with db_engine.connect() as con:
        result: Union[ResultProxy, None] = con.execute(query)
        if result is None:
            return True
        for row in result:
            for column, value in row.items():
                if column != "CreateDate" and column != "LastModifiedDate":
                    if resource[column] != value:
                        return True

    return False


def _write_resource_to_db(
    resource_name: str,
    db_engine: sqlalchemy.engine.base.Engine,
    data: DataFrame,
    column_mapping: Optional[dict] = None
):
    data.to_sql(
        resource_name, db_engine, if_exists="append", index=False, chunksize=500, dtype=column_mapping
    )


def _table_exist(
    table_name: str,
    db_engine: sqlalchemy.engine.base.Engine,
) -> bool:
    with db_engine.connect() as con:
        result: Union[ResultProxy, None] = con.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name=?;
        """, (table_name, ))

        if result is None:
            return False
        if result.first() is None:
            return False
        return True


def _remove_duplicates(
    resource_name: str,
    db_engine: sqlalchemy.engine.base.Engine,
    unique_id_column: str
):
    with db_engine.connect() as con:
        con.execute(
            f"DELETE from {resource_name} "
            "WHERE rowid not in (select max(rowid) "
            f"FROM {resource_name} "
            f"GROUP BY {unique_id_column})"
        )


def _get_created_date(
    resource_name: str,
    db_engine: sqlalchemy.engine.base.Engine,
    unique_id_column: str,
    id: Union[str, int]
):
    with db_engine.connect() as con:
        result: Union[ResultProxy, None] = con.execute(
            f"SELECT CreateDate from {resource_name} "
            f"WHERE {unique_id_column} == {id}"
        )
        if result is not None:
            create_date = result.first()
            return create_date[0] if create_date is not None else _get_current_date_with_format()

        return _get_current_date_with_format()


def _get_last_modified_date(
    resource_name: str,
    db_engine: sqlalchemy.engine.base.Engine,
    unique_id_column: str,
    id: Union[str, int]
) -> str:
    with db_engine.connect() as con:
        result: Union[ResultProxy, None] = con.execute(
            f"SELECT LastModifiedDate from {resource_name} "
            f"WHERE {unique_id_column} == {id}"
        )
        last_modified = result.first()
        return last_modified[0]


def sync_resource(
    resource_name: str,
    db_engine: sqlalchemy.engine.base.Engine,
    data: list,
    column_mapping: Optional[dict] = None,
    id_column: str = "id"
) -> DataFrame:
    """
    Writes data to the local db and sets both CreateDate and LastModifiedDate.

    Parameters
    ----------
    resource_name: str
        Name of the resource that you want to sync
    db_engine: sqlalchemy.engine.base.Engine
        The dbEngine for the sync process.
    data: list,
        The data that you are going to sync.
    column_mapping: Optional[dict] = None
        Used for specifying column types when required for the syncDB.
    id_column: str = "id"
        The column where the id of the resource is contained.

    Returns
    -------
    df_data  : DataFrame
        A populated `DataFrame` with the elements from the original list.
    """
    table_exist = _table_exist(resource_name, db_engine)
    current_date_with_format = _get_current_date_with_format()

    if len(data) == 0:
        return DataFrame()

    for row in data:
        hasChanged = _resource_has_changed(row, resource_name, db_engine, id_column) if table_exist else True
        row["CreateDate"] = _get_created_date(resource_name, db_engine, id_column, row[id_column]) if table_exist else current_date_with_format
        row["LastModifiedDate"] = current_date_with_format if hasChanged else _get_last_modified_date(resource_name, db_engine, id_column, row[id_column])

    df_data = DataFrame(data)
    _write_resource_to_db(resource_name, db_engine, df_data, column_mapping)
    _remove_duplicates(resource_name, db_engine, id_column)

    return df_data
