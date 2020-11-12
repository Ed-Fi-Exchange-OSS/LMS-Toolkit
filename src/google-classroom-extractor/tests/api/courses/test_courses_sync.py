# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
from google_classroom_extractor.api.courses import _sync_courses


def describe_when_testing_sync_with_new_missing_and_update():
    def it_should_work_correctly(test_db_fixture):
        # arrange
        courses_sync_df = pd.read_csv("tests/api/courses/courses-sync.csv")
        courses_initial_df = pd.read_csv("tests/api/courses/courses-initial.csv")

        with test_db_fixture.connect() as con:
            con.execute("DROP TABLE IF EXISTS Courses")
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

        courses_initial_df.to_sql(
            "Courses", test_db_fixture, if_exists="append", index=False, chunksize=1000
        )

        # act
        _sync_courses(courses_sync_df, test_db_fixture)

        # assert
        with test_db_fixture.connect() as con:
            courses_updated_df = pd.read_sql_query("SELECT * FROM Courses", con)
            row_count, column_count = courses_updated_df.shape
            assert row_count == 4
            assert column_count == 20
