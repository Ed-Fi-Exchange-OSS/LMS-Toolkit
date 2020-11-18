# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from datetime import datetime
from pandas import DataFrame, read_sql_query
import sqlalchemy
import xxhash

logger = logging.getLogger(__name__)


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


def sync_to_db_without_cleanup(
    resource_df: DataFrame,
    resource_name: str,
    table_columns_sql: str,
    primary_keys: str,
    sync_db: sqlalchemy.engine.base.Engine,
):
    """
    Take fetched API data and sync with database. Creates tables when necessary,
    but ok if temporary tables are there to start. Does not delete temporary tables when finished.

    Parameters
    ----------
    resource_df: DataFrame
        an API DataFrame with current fetched data which
        will be mutated, adding Hash and CreateDate/LastModifiedDate
    resource_name: str
        the name of the API resource, e.g. "Courses", to be used in SQL
    table_columns_sql: str
        the columns for the resource in the database, in SQL table creation form,
            with dangling commas
    primary_keys: str
        a comma separated list of the primary key columns for the resource,
        e.g. "id,courseId"
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections
    """
    SYNC_COLUMNS_SQL = """
        Hash TEXT,
        CreateDate DATETIME,
        LastModifiedDate DATETIME,
        SyncNeeded BIGINT,
        """
    with sync_db.connect() as con:
        # ensure sync table exists, need column ordering to be identical to regular table
        con.execute(f"DROP TABLE IF EXISTS Sync_{resource_name}")
        con.execute(
            f"""
            CREATE TABLE IF NOT EXISTS Sync_{resource_name} (
                {table_columns_sql}
                {SYNC_COLUMNS_SQL}
                PRIMARY KEY ({primary_keys})
            )
            """
        )

    # compute hash from API call data
    resource_df["Hash"] = resource_df.apply(
        lambda row: xxhash.xxh64_hexdigest(row.to_json().encode("utf-8")),
        axis=1,
    )

    primary_keys_as_array = primary_keys.split(",")

    # will need index set for DataFrame update below
    resource_df.set_index(primary_keys_as_array, inplace=True)

    # add initial Create/Update times and SyncNeeded flag
    now: datetime = datetime.now()
    resource_df["CreateDate"] = now
    resource_df["LastModifiedDate"] = now
    resource_df["SyncNeeded"] = 1

    # push to temporary sync table
    resource_df.to_sql(
        f"Sync_{resource_name}", sync_db, if_exists="append", index=True, chunksize=1000
    )

    with sync_db.connect() as con:
        # ensure main table exists
        con.execute(f"DROP INDEX IF EXISTS SYNCNEEDED_{resource_name}")
        con.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {resource_name} (
                {table_columns_sql}
                {SYNC_COLUMNS_SQL}
                PRIMARY KEY ({primary_keys})
            )
            """
        )
        con.execute(
            f"CREATE INDEX IF NOT EXISTS SYNCNEEDED_{resource_name} ON {resource_name}(SyncNeeded)"
        )

        # select unmatched records into temp table - differing by hash for same identity
        # single entry in result set if identity only exists in one table (meaning add or missing),
        #   so SyncNeeded flag will indicate which table it's from
        # double entry in result set if identity exists in both (meaning update needed),
        #   so SyncNeeded will show which row is from which table
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
            GROUP BY {primary_keys}, Hash
            HAVING COUNT(*) = 1
            """
        )
        con.execute(
            f"CREATE INDEX IF NOT EXISTS ID_{resource_name} ON Unmatched_{resource_name}({primary_keys})"
        )

        # all rows start with CreateDate and LastModifiedDate initialized to "now",
        #   but updated rows need the original CreateDate pulled from existing table
        # Note: UPDATE-FROM is not available in sqlite until v3.33.0, thus the
        #   double select goofiness
        create_date_where_clause = " AND ".join(
            map(
                lambda pk: f" c.{pk} = Unmatched_{resource_name}.{pk}",
                primary_keys_as_array,
            )
        )
        con.execute(
            f"""
            UPDATE Unmatched_{resource_name}
                SET CreateDate = (
                    SELECT c.CreateDate
                    FROM {resource_name} c
                    WHERE {create_date_where_clause}
                )
                WHERE EXISTS (
                    SELECT *
                    FROM {resource_name} c
                    WHERE {create_date_where_clause}
                ) AND SyncNeeded = 1
            """
        )

        CHANGED_ROWS_CTE = f"""
                           changedRows AS (
                               SELECT * FROM Unmatched_{resource_name}
                               WHERE ({primary_keys}) IN (
                                   SELECT {primary_keys} FROM Unmatched_{resource_name}
                                   GROUP BY {primary_keys}
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
            WHERE ({primary_keys}) IN (
                SELECT {primary_keys} from changedRows
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
                    WHERE ({primary_keys}) IN (
                        SELECT {primary_keys} FROM Unmatched_{resource_name}
                        GROUP BY {primary_keys}
                        HAVING COUNT(*) = 1 AND SyncNeeded = 1
                    )
                )
            INSERT INTO {resource_name}
                SELECT * FROM Unmatched_{resource_name}
                WHERE ({primary_keys}) IN (
                    SELECT {primary_keys} FROM changedRows
                    UNION ALL
                    SELECT {primary_keys} FROM newRows
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

        # fetch DataFrame with reconciled CreateDate/LastModifiedDate for sync records
        update_dates_query = f"""
                             SELECT {primary_keys}, CreateDate, LastModifiedDate
                             FROM {resource_name}
                             WHERE ({primary_keys}) IN (
                                 SELECT {primary_keys} FROM Sync_{resource_name}
                             )
                             """
        create_date_df = read_sql_query(update_dates_query, con)

        # set up index for update operation
        for pk in primary_keys_as_array:
            create_date_df[pk] = create_date_df[pk].astype("string")
        create_date_df.set_index(primary_keys_as_array, inplace=True)

        # update CreateDate/LastModifiedDate of sync records
        resource_df.update(create_date_df)

        # reset index so no columns are hidden
        resource_df.reset_index(inplace=True)
