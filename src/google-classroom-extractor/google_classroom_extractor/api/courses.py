# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from datetime import datetime
from typing import List, Dict, Optional, cast
from pandas import DataFrame, json_normalize, read_sql_query
import sqlalchemy
import xxhash
from googleapiclient.discovery import Resource
from google_classroom_extractor.api.api_caller import call_api, ResourceType

logger = logging.getLogger(__name__)


def request_courses(resource: Optional[Resource]) -> List[Dict[str, str]]:
    """
    Fetch Course API data for all courses and return a list of course data

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource

    Returns
    -------
    List[Dict[str, str]]
        a list of Google Classroom Course resources,
            see https://developers.google.com/classroom/reference/rest/v1/courses
    """

    if resource is None:
        return []

    return call_api(
        cast(ResourceType, resource).courses().list,
        {},
        "courses",
    )


def request_latest_courses_as_df(resource: Optional[Resource]) -> DataFrame:
    """
    Fetch Course API data for all courses and return a Courses API DataFrame

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource

    Returns
    -------
    DataFrame
        a Courses API DataFrame with the fetched data

    Notes
    -----
    DataFrame columns are:
        id: Identifier for this course assigned by Classroom
        name: Name of the course
        section: Section of the course
        descriptionHeading: Optional heading for the description
        description: Optional description
        room: Optional room location
        ownerId: The identifier of the owner of a course
        creationTime: Creation time of the course
        updateTime: Time of the most recent update to this course
        enrollmentCode: Enrollment code to use when joining this course
        courseState: State of the course
        alternateLink: Absolute link to this course in the Classroom web UI
        teacherGroupEmail: The email address of a Google group containing all teachers of the course
        courseGroupEmail: The email address of a Google group containing all members of the course
        guardiansEnabled: Whether or not guardian notifications are enabled for this course
        calendarId: The Calendar ID for a calendar that all course members can see
    """

    logger.info("Pulling course data")
    courses: List[Dict[str, str]] = request_courses(resource)
    return json_normalize(courses)


def request_all_courses_as_df(
    resource: Optional[Resource], sync_db: sqlalchemy.engine.base.Engine
) -> DataFrame:
    """
    Fetch Course API data for all courses and return a Courses API DataFrame

    Parameters
    ----------
    resource: Optional[Resource]
        a Google Classroom SDK Resource
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections

    Returns
    -------
    DataFrame
        a Courses API DataFrame with the current and previously fetched data

    Notes
    -----
    DataFrame columns are:
        id: Identifier for this course assigned by Classroom
        name: Name of the course
        section: Section of the course
        descriptionHeading: Optional heading for the description
        description: Optional description
        room: Optional room location
        ownerId: The identifier of the owner of a course
        creationTime: Creation time of the course
        updateTime: Time of the most recent update to this course
        enrollmentCode: Enrollment code to use when joining this course
        courseState: State of the course
        alternateLink: Absolute link to this course in the Classroom web UI
        teacherGroupEmail: The email address of a Google group containing all teachers of the course
        courseGroupEmail: The email address of a Google group containing all members of the course
        guardiansEnabled: Whether or not guardian notifications are enabled for this course
        calendarId: The Calendar ID for a calendar that all course members can see
        CreateDate: Date this record was created by the extractor
        LastModifiedDate: Date this record was last updated by the extractor
    """

    courses_df = request_latest_courses_as_df(resource)
    _sync_courses_without_cleanup(courses_df, sync_db)

    # finally, remove temporary sync tables
    with sync_db.connect() as con:
        con.execute("DROP TABLE IF EXISTS Sync_Courses")
        con.execute("DROP TABLE IF EXISTS Unmatched")
    return courses_df


def _sync_courses_without_cleanup(courses_df: DataFrame, sync_db: sqlalchemy.engine.base.Engine):
    """
    Take fetched API data and sync with database. Creates tables when necessary,
    but ok if temporary tables are there to start. Doesn't delete temporary tables when finished.

    Parameters
    ----------
    courses_df: DataFrame
        a Courses API DataFrame with the current fetched data which
        will be mutated, adding Hash and CreateDate/LastModifiedDate
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections
    """
    with sync_db.connect() as con:
        # ensure sync table exists, need column ordering to be identical to regular table
        con.execute("DROP TABLE IF EXISTS Sync_Courses")
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS Sync_Courses (
                id BIGINT,
                name TEXT,
                section BIGINT,
                descriptionHeading TEXT,
                room TEXT,
                ownerId BIGINT,
                creationTime TEXT,
                updateTime TEXT,
                enrollmentCode BIGINT,
                courseState TEXT,
                alternateLink TEXT,
                teacherGroupEmail TEXT,
                courseGroupEmail TEXT,
                "teacherFolder.id" TEXT,
                "teacherFolder.title" TEXT,
                "teacherFolder.alternateLink" TEXT,
                guardiansEnabled BOOLEAN,
                calendarId BIGINT,
                Hash TEXT,
                CreateDate DATETIME,
                LastModifiedDate DATETIME,
                SyncNeeded BIGINT,
                PRIMARY KEY (id)
            )
            """
        )

    # compute hash from API call data
    courses_df["Hash"] = courses_df.apply(
        lambda row: xxhash.xxh64_hexdigest(
            row.to_json().encode("utf-8")
        ),
        axis=1,
    )

    # will need index set for DataFrame update below
    courses_df.set_index('id', inplace=True)

    # add initial Create/Update times and SyncNeeded flag
    now: datetime = datetime.now()
    courses_df["CreateDate"] = now
    courses_df["LastModifiedDate"] = now
    courses_df["SyncNeeded"] = 1

    # push to temporary sync table
    courses_df.to_sql(
        "Sync_Courses", sync_db, if_exists="append", index=True, chunksize=1000
    )

    with sync_db.connect() as con:
        # ensure main table exists
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS Courses (
                id BIGINT,
                name TEXT,
                section BIGINT,
                descriptionHeading TEXT,
                room TEXT,
                ownerId BIGINT,
                creationTime TEXT,
                updateTime TEXT,
                enrollmentCode BIGINT,
                courseState TEXT,
                alternateLink TEXT,
                teacherGroupEmail TEXT,
                courseGroupEmail TEXT,
                "teacherFolder.id" TEXT,
                "teacherFolder.title" TEXT,
                "teacherFolder.alternateLink" TEXT,
                guardiansEnabled BOOLEAN,
                calendarId BIGINT,
                Hash TEXT,
                CreateDate DATETIME,
                LastModifiedDate DATETIME,
                SyncNeeded BIGINT,
                PRIMARY KEY (id)
            )
            """
        )
        con.execute("CREATE INDEX IF NOT EXISTS SYNCNEEDED_INDEX ON Courses(SyncNeeded)")

        # select unmatched records into temp table - differing by hash for same id
        # single entry in result set if id only exists in one table (meaning add or missing),
        #   so SyncNeeded flag will indicate which table it's from
        # double entry in result set if id exists in both (meaning update needed),
        #   so SyncNeeded will show which row is from which table
        con.execute("DROP TABLE IF EXISTS Unmatched")
        con.execute(
            """
            CREATE TABLE Unmatched AS
            SELECT * FROM (
                SELECT * FROM Courses
                UNION ALL
                SELECT * FROM Sync_Courses
            )
            GROUP BY id, Hash
            HAVING COUNT(*) = 1
            """
        )
        con.execute("CREATE INDEX ID_INDEX ON Unmatched(id)")

        # all rows start with CreateDate and LastModifiedDate initialized to "now",
        #   but updated rows need the original CreateDate pulled from existing table
        # Note: UPDATE-FROM is not available in sqlite until v3.33.0, thus the
        #   double select goofiness
        con.execute(
            """
            UPDATE Unmatched
                SET CreateDate = (
                    SELECT c.CreateDate
                    FROM Courses c
                    WHERE c.id = Unmatched.id
                )
                WHERE EXISTS (
                    SELECT *
                    FROM Courses c
                    WHERE c.id = Unmatched.id
                ) AND SyncNeeded = 1
            """
        )

        # delete obsolete data from regular table
        con.execute(
            # changed rows CTE (from SyncNeeded side only)
            """
            WITH
                changedRows AS (
                    SELECT * FROM Unmatched
                    WHERE id IN (
                        SELECT id FROM Unmatched
                        GROUP BY id
                        HAVING COUNT(*) > 1
                    ) AND SyncNeeded = 1
                )
            DELETE FROM Courses
            WHERE id IN (
                SELECT id from changedRows
            )
            """
        )

        # insert new and changed data into regular table
        con.execute(
            #    changed rows CTE (from SyncNeeded side only)
            #    new rows CTE (also from SyncNeeded side)
            """
            WITH
                changedRows AS (
                    SELECT * FROM Unmatched
                    WHERE id IN (
                        SELECT id FROM Unmatched
                        GROUP BY id
                        HAVING COUNT(*) > 1
                    ) AND SyncNeeded = 1
                ),
                newRows AS (
                    SELECT * FROM Unmatched
                    WHERE id IN (
                        SELECT id FROM Unmatched
                        GROUP BY id
                        HAVING COUNT(*) = 1 AND SyncNeeded = 1
                    )
                )
            INSERT INTO Courses
                SELECT * FROM Unmatched
                WHERE id IN (
                    SELECT id FROM changedRows
                    UNION ALL
                    SELECT id FROM newRows
                ) AND SyncNeeded = 1
            """
        )

        con.execute(
            # reset SyncNeeded flag on main table
            """
            UPDATE Courses
            SET SyncNeeded = 0
            WHERE SyncNeeded != 0
            """
        )

        # fetch DataFrame with reconciled CreateDate/LastModifiedDate for sync records
        update_dates_query = """
                             SELECT id, CreateDate, LastModifiedDate
                             FROM Courses
                             WHERE id IN (
                                 SELECT id FROM Sync_Courses
                             )
                             """

        create_date_df = read_sql_query(update_dates_query, con)
        # set up index for update operation
        create_date_df["id"] = create_date_df["id"].astype('string')
        create_date_df.set_index('id', inplace=True)

        # update CreateDate/LastModifiedDate of sync records
        courses_df.update(create_date_df)

        # reset index so 'id' isn't a hidden column
        courses_df.reset_index(inplace=True)
