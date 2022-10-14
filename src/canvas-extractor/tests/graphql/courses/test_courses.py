# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from pandas import DataFrame
from edfi_canvas_extractor.graphql.courses import courses_synced_as_df


def test_courses(gql_no_run, api):
    """
    Get from the sample data
    obtain the courses info
    Check and check the return type
    """
    gql_no_run.extract(api)
    courses = gql_no_run.courses

    assert api is not None

    assert courses is not None
    assert isinstance(courses, list)


def test_courses_df(gql_no_run, api, test_db_fixture):
    """
    Get from the sample data
    obtain the courses info
    Check the DataFrame
    """
    gql_no_run.extract(api)
    courses = gql_no_run.courses

    courses_df = courses_synced_as_df(courses, test_db_fixture)

    assert courses_df is not None
    assert isinstance(courses_df, DataFrame)
