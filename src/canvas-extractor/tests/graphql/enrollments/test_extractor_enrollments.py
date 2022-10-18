# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


from pandas import DataFrame
from edfi_canvas_extractor.graphql.enrollments import enrollments_synced_as_df


def test_enrollments(gql):
    """
    Get from the sample data
    obtain the enrollments info
    Check and check the return type
    """
    enrollments = gql.get_enrollments()

    assert enrollments is not None
    assert isinstance(enrollments, list)


def test_enrollments_df(gql, test_db_fixture):
    """
    Get from the sample data
    obtain the enrollments info
    Check the DataFrame and columns
    """
    enrollments = gql.get_enrollments()
    enrollments_df = enrollments_synced_as_df(enrollments, test_db_fixture)

    assert enrollments_df is not None
    assert isinstance(enrollments_df, DataFrame)

    assert "id" in enrollments_df.columns
    assert "enrollment_state" in enrollments_df.columns
    assert "user_id" in enrollments_df.columns
    assert "course_section_id" in enrollments_df.columns
    assert "created_at" in enrollments_df.columns
    assert "updated_at" in enrollments_df.columns
