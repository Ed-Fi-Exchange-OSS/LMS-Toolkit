# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from pandas import DataFrame
from edfi_canvas_extractor.graphql.courses import courses_synced_as_df


def test_courses(gql):
    """
    Get from the sample data
    obtain the courses info
    Check and check the return type
    """
    courses = gql.get_courses()

    assert courses is not None
    assert isinstance(courses, list)


def test_courses_df(gql, test_db_fixture):
    """
    Get from the sample data
    obtain the courses info
    Check the DataFrame
    """
    courses = gql.get_courses()
    courses_df = courses_synced_as_df(courses, test_db_fixture)

    assert courses_df is not None
    assert isinstance(courses_df, DataFrame)
