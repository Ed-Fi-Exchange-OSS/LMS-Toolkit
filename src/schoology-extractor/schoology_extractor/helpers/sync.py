# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
import json
from datetime import datetime
import os
import logging
from typing import Union

from pandas import DataFrame
import sqlalchemy
from sqlalchemy.engine import ResultProxy

SYNC_DATABASE_LOCATION_SUFFIX = "data"
COLUMN_MAPPING = {
    'SourceId': sqlalchemy.types.String
}
USAGE_TABLE_NAME = 'USAGE_PROCESSED_FILES'

logger = logging.getLogger(__name__)


def get_sync_db_engine() -> sqlalchemy.engine.base.Engine:
    """
    Create a SQL Alchemy Engine for a SQLite file

    Returns
    -------
    sqlalchemy.engine.base.Engine
        a SQL Alchemy Engine
    """
    sync_database_directory = (os.path.join(SYNC_DATABASE_LOCATION_SUFFIX))
    logger.debug("Ensuring database directory at %s", os.path.abspath(sync_database_directory))
    os.makedirs(sync_database_directory, exist_ok=True)

    return sqlalchemy.create_engine(f"sqlite:///{sync_database_directory}/sync.sqlite")


def _get_current_date_with_format() -> str:
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")


def _map_result_to_dicts_arr(result: Union[list, None]) -> list:
    if result is None:
        return list()

    return [dict(row.items()) for row in result]  # type: ignore


def _map_single_result_to_dict(result: Union[list, None]) -> dict:
    mapped_result = _map_result_to_dicts_arr(result)
    return mapped_result[0] if len(mapped_result) > 0 else dict()


def _resource_has_changed(
    resource: dict,
    resource_name: str,
    db_engine:  sqlalchemy.engine.base.Engine,
    id_column: str = "id"
) -> bool:
    query = f"SELECT * FROM {resource_name} where SourceId = '{resource[id_column]}' limit 1;"
    with db_engine.connect() as con:
        result: Union[ResultProxy, None] = con.execute(query)
        db_item = _map_single_result_to_dict(result)

    if "JsonResponse" not in db_item:
        # Implies this is a new record that is not yet in the database.
        return False

    json_response = r"%s" % db_item["JsonResponse"]
    db_parsed_item = json.loads(json_response)

    for key in db_parsed_item:
        api_value = resource[key]
        db_value = db_parsed_item[key]

        if isinstance(api_value, dict) or isinstance(api_value, list):
            api_value = str(api_value).replace("'", '"')
            db_value = str(db_value).replace("'", '"')

        if str(db_value) != str(api_value):
            return True

    return False


def _write_resource_to_db(
    resource_name: str,
    db_engine: sqlalchemy.engine.base.Engine,
    data: DataFrame
):
    data.to_sql(resource_name, db_engine, if_exists="append", index=False, chunksize=500, dtype=COLUMN_MAPPING)


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
    db_engine: sqlalchemy.engine.base.Engine
):
    with db_engine.connect() as con:
        con.execute(
            f"DELETE from {resource_name} "
            "WHERE rowid not in (select max(rowid) "
            f"FROM {resource_name} "
            f"GROUP BY SourceId)"
        )


def _get_created_date(
    resource_name: str,
    db_engine: sqlalchemy.engine.base.Engine,
    id: Union[str, int]
):
    with db_engine.connect() as con:
        result: Union[ResultProxy, None] = con.execute(
            f"SELECT CreateDate from {resource_name} "
            f"WHERE SourceId == '{id}'"
        )
        if result is not None:
            create_date = result.first()
            return create_date[0] if create_date is not None else _get_current_date_with_format()

        return _get_current_date_with_format()


def _get_last_modified_date(
    resource_name: str,
    db_engine: sqlalchemy.engine.base.Engine,
    id: Union[str, int]
) -> str:
    with db_engine.connect() as con:
        result: Union[ResultProxy, None] = con.execute(
            f"SELECT LastModifiedDate from {resource_name} "
            f"WHERE SourceId == '{id}'"
        )
        if result is not None:
            modified_date = result.first()
            return modified_date[0] if modified_date is not None else _get_current_date_with_format()

    return _get_current_date_with_format()


def sync_resource(
    resource_name: str,
    db_engine: sqlalchemy.engine.base.Engine,
    data: list,
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

    data_to_write = []
    table_exist = _table_exist(resource_name, db_engine)
    current_date_with_format = _get_current_date_with_format()

    if len(data) == 0:
        return DataFrame()

    for row in data:
        hasChanged = _resource_has_changed(row, resource_name, db_engine, id_column) if table_exist else True
        create_date = _get_created_date(resource_name, db_engine, row[id_column]) if table_exist else current_date_with_format
        last_modified_date = current_date_with_format if hasChanged else _get_last_modified_date(resource_name, db_engine, row[id_column])
        record = dict(
            CreateDate=create_date,
            LastModifiedDate=last_modified_date,
            SourceId=row[id_column],
            JsonResponse=json.dumps(row)
        )
        data_to_write.append(record)
        row["CreateDate"] = create_date
        row["LastModifiedDate"] = last_modified_date

    df_data = DataFrame(data_to_write)
    _write_resource_to_db(resource_name, db_engine, df_data)
    _remove_duplicates(resource_name, db_engine)

    return DataFrame(data)


def _create_usage_table_if_it_does_not_exist(
        db_engine: sqlalchemy.engine.base.Engine
        ):
    if _table_exist(USAGE_TABLE_NAME, db_engine) is False:
        db_engine.execute(f"""CREATE TABLE {USAGE_TABLE_NAME} (
            FILE_NAME TEXT PRIMARY KEY
        );""")


def usage_file_is_processed(
        file_name: str,
        db_engine: sqlalchemy.engine.base.Engine
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

    query = F"select exists(select 1 from {USAGE_TABLE_NAME} where FILE_NAME='{file_name}') as 'exists'"

    db_item = {'exists': False}
    with db_engine.connect() as con:
        result: Union[ResultProxy, None] = con.execute(query)
        db_item = _map_single_result_to_dict(result)

    return db_item['exists'] == 1


def insert_usage_file_name(
        file_name: str,
        db_engine: sqlalchemy.engine.base.Engine) -> None:
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
