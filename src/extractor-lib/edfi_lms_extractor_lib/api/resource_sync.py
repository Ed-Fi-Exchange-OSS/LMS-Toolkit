# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from datetime import datetime
from typing import List
from pandas import DataFrame, Series, read_sql_query, to_datetime
import sqlalchemy
import xxhash

logger = logging.getLogger(__name__)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

SYNC_COLUMNS = [
    "SourceId",
    "Json",
    "Hash",
    "CreateDate",
    "LastModifiedDate",
    "SyncNeeded",
]

SYNC_COLUMNS_SQL = """
    SourceId TEXT,
    Json TEXT,
    Hash TEXT,
    CreateDate DATETIME,
    LastModifiedDate DATETIME,
    SyncNeeded BIGINT,
    PRIMARY KEY (SourceId)
    """


def _json_hash_encode(row: Series) -> Series:
    """
    Take a DataFrame row, add serialized JSON and hash

    Parameters
    ----------
    row: Series
        a DataFrame row

    Returns
    -------
    Series
        the row with the json and hash columns added
    """
    json = row.to_json()
    row["Json"] = json
    row["Hash"] = xxhash.xxh64_hexdigest(json.encode("utf-8"))
    return row


def add_hash_and_json_to(df: DataFrame) -> DataFrame:
    """
    Create Hash and Json columns for DataFrame.  Do this
    before adding any other columns e.g. SourceId

    Parameters
    ----------
    df: DataFrame
        a DataFrame with fetched data

    Returns
    -------
    DataFrame
        a new DataFrame with the json and hash columns added
    """
    return df.apply(_json_hash_encode, axis=1)


def add_sourceid_to(df: DataFrame, identity_columns: List[str]):
    """
    Create SourceId column for DataFrame with given identity columns.

    Parameters
    ----------
    df: DataFrame
        a DataFrame with fetched data
    identity_columns: List[str]
        a List of the identity columns for the resource dataframe
    """
    assert (
        Series(identity_columns).isin(df.columns).all()
    ), "Identity columns missing from dataframe"

    df[identity_columns] = df[identity_columns].astype("string")
    df["SourceId"] = df[sorted(identity_columns)].agg("-".join, axis=1)


def _create_sync_table_from_resource_df(
    resource_df: DataFrame,
    identity_columns: List[str],
    resource_name: str,
    sync_db: sqlalchemy.engine.base.Engine,
):
    """
    Take fetched data and push to a new temporary sync table.  Includes
    hash and tentative extractor CreateDate/LastModifiedDates.

    Parameters
    ----------
    resource_df: DataFrame
        a DataFrame with current fetched data.
    identity_columns: List[str]
        a List of the identity columns for the resource dataframe.
    resource_name: str
        the name of the API resource, e.g. "Courses", to be used in SQL
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections
    """
    with sync_db.connect() as con:
        # ensure sync table exists, need column ordering to be identical to regular table
        con.execute(f"DROP TABLE IF EXISTS Sync_{resource_name}")
        con.execute(
            f"""
            CREATE TABLE IF NOT EXISTS Sync_{resource_name} (
                {SYNC_COLUMNS_SQL}
            )
            """
        )

    sync_df: DataFrame = resource_df.copy()
    sync_df = add_hash_and_json_to(sync_df)

    # add (possibly composite) primary key, sorting for consistent ordering
    add_sourceid_to(sync_df, identity_columns)

    now: datetime = datetime.now()
    sync_df["CreateDate"] = now
    sync_df["LastModifiedDate"] = now
    sync_df["SyncNeeded"] = 1

    sync_df = sync_df[SYNC_COLUMNS]
    sync_df.set_index("SourceId", inplace=True)
    # push to temporary sync table
    sync_df.to_sql(
        f"Sync_{resource_name}", sync_db, if_exists="append", index=True, chunksize=1000
    )


def _ensure_main_table_exists(
    resource_name: str,
    con: sqlalchemy.engine.base.Connection,
):
    """
    Ensure the main resource table exists, creating if necessary.

    Parameters
    ----------
    resource_name: str
        the name of the API resource, e.g. "Courses", to be used in SQL
    table_columns_sql: str
        the columns for the resource in the database, in SQL table creation form,
            with dangling commas
    con: sqlalchemy.engine.base.Connection
        an open database connection, which will not be closed by this function
    """
    con.execute(f"DROP INDEX IF EXISTS SYNCNEEDED_{resource_name}")
    con.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {resource_name} (
            {SYNC_COLUMNS_SQL}
        )
        """
    )
    con.execute(
        f"CREATE INDEX IF NOT EXISTS SYNCNEEDED_{resource_name} ON {resource_name}(SyncNeeded)"
    )


def _create_unmatched_records_temp_table(
    resource_name: str,
    con: sqlalchemy.engine.base.Connection,
):
    """
    Select unmatched records into new temp table - differing by hash for same identity.
    Single entry in result set if identity only exists in one table (meaning add or missing),
        so SyncNeeded flag will indicate which table it's from.
    Double entry in result set if identity exists in both (meaning update needed),
        so SyncNeeded will show which row is from which table.

    Parameters
    ----------
    resource_name: str
        the name of the API resource, e.g. "Courses", to be used in SQL
    con: sqlalchemy.engine.base.Connection
        an open database connection, which will not be closed by this function
    """
    con.execute(f"DROP INDEX IF EXISTS ID_{resource_name}")
    con.execute(f"DROP TABLE IF EXISTS Unmatched_{resource_name}")
    con.execute(
        f"""
        CREATE TABLE Unmatched_{resource_name} AS
        SELECT * FROM (
            SELECT * FROM {resource_name}
            UNION ALL
            SELECT * FROM Sync_{resource_name}
        )
        GROUP BY SourceId, Hash
        HAVING COUNT(*) = 1
        """
    )
    con.execute(
        f"CREATE INDEX IF NOT EXISTS ID_{resource_name} ON Unmatched_{resource_name}(SourceId)"
    )


def _get_true_create_dates_for_unmatched_records(
    resource_name: str,
    con: sqlalchemy.engine.base.Connection,
):
    """
    All rows start with CreateDate and LastModifiedDate initialized to "now",
        but updated rows need the original CreateDate pulled from existing table.

    Note: UPDATE-FROM is not available in sqlite until v3.33.0, thus the
        double select goofiness.

    Parameters
    ----------
    resource_name: str
        the name of the API resource, e.g. "Courses", to be used in SQL
    con: sqlalchemy.engine.base.Connection
        an open database connection, which will not be closed by this function
    """
    con.execute(
        f"""
        UPDATE Unmatched_{resource_name}
            SET CreateDate = (
                SELECT c.CreateDate
                FROM {resource_name} c
                WHERE c.SourceId = Unmatched_{resource_name}.SourceId
            )
            WHERE EXISTS (
                SELECT *
                FROM {resource_name} c
                WHERE c.SourceId = Unmatched_{resource_name}.SourceId
            ) AND SyncNeeded = 1
        """
    )


def _update_resource_table_with_changes(
    resource_name: str,
    con: sqlalchemy.engine.base.Connection,
):
    """
    Update main resource table with new and updated records

    Parameters
    ----------
    resource_name: str
        the name of the API resource, e.g. "Courses", to be used in SQL
    primary_keys: str
        a comma separated list of the primary key columns for the resource,
        e.g. "id,courseId"
    con: sqlalchemy.engine.base.Connection
        an open database connection, which will not be closed by this function
    """
    CHANGED_ROWS_CTE = f"""
                        changedRows AS (
                            SELECT * FROM Unmatched_{resource_name}
                            WHERE (SourceId) IN (
                                SELECT SourceId FROM Unmatched_{resource_name}
                                GROUP BY SourceId
                                HAVING COUNT(*) > 1
                            ) AND SyncNeeded = 1
                        )
                        """

    # delete obsolete data from regular table
    con.execute(
        # changed rows CTE (from SyncNeeded side only)
        f"""
        WITH
        {CHANGED_ROWS_CTE}
        DELETE FROM {resource_name}
        WHERE (SourceId) IN (
            SELECT SourceId from changedRows
        )
        """
    )

    # insert new and changed data into regular table
    con.execute(
        #    changed rows CTE (from SyncNeeded side only)
        #    new rows CTE (also from SyncNeeded side)
        f"""
        WITH
            {CHANGED_ROWS_CTE},
            newRows AS (
                SELECT * FROM Unmatched_{resource_name}
                WHERE (SourceId) IN (
                    SELECT SourceId FROM Unmatched_{resource_name}
                    GROUP BY SourceId
                    HAVING COUNT(*) = 1 AND SyncNeeded = 1
                )
            )
        INSERT INTO {resource_name}
            SELECT * FROM Unmatched_{resource_name}
            WHERE (SourceId) IN (
                SELECT SourceId FROM changedRows
                UNION ALL
                SELECT SourceId FROM newRows
            ) AND SyncNeeded = 1
        """
    )

    con.execute(
        # reset SyncNeeded flag on main table
        f"""
        UPDATE {resource_name}
        SET SyncNeeded = 0
        WHERE SyncNeeded != 0
        """
    )


def _update_dataframe_with_true_dates(
    resource_df: DataFrame,
    identity_columns: List[str],
    resource_name: str,
    con: sqlalchemy.engine.base.Connection,
) -> DataFrame:
    """
    Update main resource DataFrame with reconciled CreateDate/LastModifiedDates

    Parameters
    ----------
    resource_df: DataFrame
        an API DataFrame with current fetched data which
        will be mutated by updating CreateDate/LastModifiedDate
    identity_columns: List[str]
        a List of the identity columns for the resource dataframe.
    resource_name: str
        the name of the API resource, e.g. "Courses", to be used in SQL
    primary_keys: str
        a comma separated list of the primary key columns for the resource,
        e.g. "id,courseId"
    con: sqlalchemy.engine.base.Connection
        an open database connection, which will not be closed by this function

    Returns
    -------
    DataFrame
        a DataFrame with reconciled CreateDate/LastModifiedDate
    """
    assert (
        Series(identity_columns).isin(resource_df.columns).all()
    ), "Identity columns missing from dataframe"

    # fetch DataFrame with reconciled CreateDate/LastModifiedDate for sync records
    update_dates_query = f"""
                            SELECT SourceId, CreateDate, LastModifiedDate
                            FROM {resource_name}
                            WHERE (SourceId) IN (
                                SELECT SourceId FROM Sync_{resource_name}
                            )
                            """
    create_date_df = read_sql_query(update_dates_query, con)
    create_date_df["SourceId"] = create_date_df["SourceId"].astype("string")

    add_sourceid_to(resource_df, identity_columns)
    resource_df["SourceId"] = resource_df["SourceId"].astype("string")

    result_df = resource_df.join(create_date_df.set_index("SourceId"), on="SourceId")

    # reset index so no columns are hidden
    result_df.drop(["SourceId"], axis=1, inplace=True)

    # convert dates to string format
    result_df["CreateDate"] = to_datetime(result_df["CreateDate"]).dt.strftime(DATE_FORMAT)
    result_df["LastModifiedDate"] = to_datetime(result_df["LastModifiedDate"]).dt.strftime(DATE_FORMAT)

    return result_df


def sync_to_db_without_cleanup(
    resource_df: DataFrame,
    identity_columns: List[str],
    resource_name: str,
    sync_db: sqlalchemy.engine.base.Engine,
):
    """
    Take fetched data and sync with database. Creates tables when necessary,
    but ok if temporary tables are there to start. Does not delete temporary tables when finished.

    Parameters
    ----------
    resource_df: DataFrame
        a DataFrame with current fetched data
    identity_columns: List[str]
        a List of the identity columns for the resource dataframe.
    resource_name: str
        the name of the API resource, e.g. "Courses", to be used in SQL
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a DataFrame with current fetched data and reconciled CreateDate/LastModifiedDate
    """
    assert (
        Series(identity_columns).isin(resource_df.columns).all()
    ), "Identity columns missing from dataframe"

    # In certain cases we can end up with duplicate records, for example
    # in Canvas when a course belongs to a sub-account. De-duplicate the
    # DataFrame based on the identity_columns
    resource_df.drop_duplicates(subset=identity_columns, inplace=True)

    _create_sync_table_from_resource_df(
        resource_df, identity_columns, resource_name, sync_db
    )

    with sync_db.connect() as con:
        _ensure_main_table_exists(resource_name, con)
        _create_unmatched_records_temp_table(resource_name, con)
        _get_true_create_dates_for_unmatched_records(resource_name, con)
        _update_resource_table_with_changes(resource_name, con)
        result_df: DataFrame = _update_dataframe_with_true_dates(
            resource_df, identity_columns, resource_name, con
        )

    return result_df


def cleanup_after_sync(resource_name: str, sync_db: sqlalchemy.engine.base.Engine):
    """
    Delete sync temporary tables if they exist

    Parameters
    ----------
    resource_name: str
        the name of the API resource, e.g. "Courses", to be used in SQL
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections
    """
    with sync_db.connect() as con:
        con.execute(f"DROP TABLE IF EXISTS Sync_{resource_name}")
        con.execute(f"DROP TABLE IF EXISTS Unmatched_{resource_name}")
