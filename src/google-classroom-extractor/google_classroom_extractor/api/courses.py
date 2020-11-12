# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, cast
from pandas import DataFrame, json_normalize, read_sql_query
import sqlalchemy
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
    """

    courses_df = request_latest_courses_as_df(resource)
    _sync_courses(courses_df, sync_db)
    return courses_df


def _sync_courses(courses_df: DataFrame, sync_db: sqlalchemy.engine.base.Engine):
    """
    Take fetched API data and sync with database.

    Parameters
    ----------
    courses_df: DataFrame
        a Courses API DataFrame with the current fetched data which
        will be mutated, adding Hash and CreateDate/LastModifiedDate
    sync_db: sqlalchemy.engine.base.Engine
        an Engine instance for creating database connections
    """
    courses_df.set_index('id', inplace=True)

    # compute hash from API call data
    courses_df["Hash"] = courses_df.apply(
        lambda row: hashlib.sha256(
            row.to_csv(header=False, index=False).encode("utf-8")
        ).hexdigest(),
        axis=1,
    )

    # add initial Create/Update times and SyncNeeded flag
    now: datetime = datetime.now()
    courses_df["CreateDate"] = now
    courses_df["LastModifiedDate"] = now
    courses_df["SyncNeeded"] = 1

    # push to temporary sync table
    courses_df.to_sql(
        "Sync_Courses", sync_db, if_exists="replace", index=True, chunksize=1000
    )

    with sync_db.connect() as con:
        # ensure main table exists
        con.execute(
            "CREATE TABLE IF NOT EXISTS Courses ( "
            "id BIGINT, "
            "name TEXT, "
            "section BIGINT, "
            "descriptionHeading TEXT, "
            "description TEXT, "
            "room TEXT, "
            "ownerId BIGINT, "
            "creationTime TEXT, "
            "updateTime TEXT, "
            "enrollmentCode BIGINT, "
            "courseState TEXT, "
            "alternateLink TEXT, "
            "teacherGroupEmail TEXT, "
            "courseGroupEmail TEXT, "
            "guardiansEnabled BOOLEAN, "
            "calendarId BIGINT,  "
            "Hash TEXT, "
            "SyncNeeded BIGINT, "
            "CreateDate DATETIME, "
            "LastModifiedDate DATETIME, "
            "PRIMARY KEY (id) "
            ")"
        )
        con.execute("CREATE INDEX IF NOT EXISTS SYNCNEEDED_INDEX ON Courses(SyncNeeded)")

        # select unmatched records into temp table - differing by hash for same id
        # single entry in result set if id only exists in one table (meaning add or missing),
        #   so SyncNeeded flag will indicate which table it's from
        # double entry in result set if id exists in both (meaning update needed),
        #   so SyncNeeded will show which row is from which table
        con.execute(
            "CREATE TABLE Unmatched AS "
            "SELECT * FROM ( "
            "    SELECT * FROM Courses "
            "    UNION ALL "
            "    SELECT * FROM Sync_Courses "
            ") "
            "GROUP BY id, Hash "
            "HAVING COUNT(*) = 1"
        )
        con.execute("CREATE INDEX ID_INDEX ON Unmatched(id)")

        # all rows start with CreateDate and LastModifiedDate initialized to "now",
        #   but updated rows need the original CreateDate pulled from existing table
        # Note: UPDATE-FROM is not available in sqlite until v3.33.0, thus the
        #   double select goofiness
        con.execute(
            "UPDATE Unmatched "
            "    SET CreateDate = ( "
            "        SELECT c.CreateDate "
            "        FROM Courses c "
            "        WHERE c.id = Unmatched.id "
            "    ) "
            "    WHERE EXISTS ( "
            "        SELECT * "
            "        FROM Courses c "
            "        WHERE c.id = Unmatched.id "
            "    ) AND SyncNeeded = 1"
        )

        # fetch DataFrame with the changed record CreateDate updates
        create_date_query = ("SELECT id, CreateDate "
                             "FROM Unmatched "
                             "WHERE id IN ( "
                             "    SELECT id FROM Unmatched "
                             "    GROUP BY id "
                             "    HAVING COUNT(*) > 1 "
                             ") AND SyncNeeded = 1")
        create_date_df = read_sql_query(create_date_query, con)
        create_date_df.set_index('id', inplace=True)

        # update the CreateDates of updated rows
        courses_df.update(create_date_df)

        # now do deletes and inserts
        con.execute(
            "WITH "
            #    changed rows CTE (from SyncNeeded side only)
            "    changedRows AS ( "
            "        SELECT * FROM Unmatched "
            "        WHERE id IN ( "
            "            SELECT id FROM Unmatched "
            "            GROUP BY id "
            "            HAVING COUNT(*) > 1 "
            "        ) AND SyncNeeded = 1 "
            "    )"


            # delete the obsolete data
            "DELETE FROM Courses "
            "WHERE id IN ( "
            "    SELECT id from changedRows "
            ")"
        )

        con.execute(
            # insert new and changed data
            "WITH "
            #    changed rows CTE (from SyncNeeded side only)
            "    changedRows AS ( "
            "        SELECT * FROM Unmatched "
            "        WHERE id IN ( "
            "            SELECT id FROM Unmatched "
            "            GROUP BY id "
            "            HAVING COUNT(*) > 1 "
            "        ) AND SyncNeeded = 1 "
            "    ),"
            #    new rows CTE (also from SyncNeeded side)
            "    newRows AS ( "
            "        SELECT * FROM Unmatched "
            "        WHERE id IN ( "
            "            SELECT id FROM Unmatched "
            "            GROUP BY id "
            "            HAVING COUNT(*) = 1 AND SyncNeeded = 1 "
            "        ) "
            "    ) "

            "INSERT INTO Courses "
            "    SELECT * FROM Unmatched "
            "    WHERE id IN ( "
            "        SELECT id FROM changedRows "
            "        UNION ALL "
            "        SELECT id FROM newRows "
            "    ) AND SyncNeeded = 1"
        )

        con.execute(
            # reset SyncNeeded flag on main table
            "UPDATE Courses "
            "SET SyncNeeded = 0 "
            "WHERE SyncNeeded != 0"
        )

        # finally, remove sync table
        con.execute("DROP TABLE IF EXISTS Sync_Courses")
        con.execute("DROP TABLE IF EXISTS Unmatched")
