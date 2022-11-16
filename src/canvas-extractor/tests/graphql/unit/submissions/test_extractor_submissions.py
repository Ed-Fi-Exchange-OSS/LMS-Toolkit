# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


from pandas import DataFrame
from edfi_canvas_extractor.graphql.submissions import submissions_synced_as_df


def test_gql_submissions_not_empty(mock_gql):
    """
    Get from the sample data
    obtain the submissions info
    Check and check the return type
    """
    submissions = mock_gql.get_submissions()

    assert submissions is not None
    assert isinstance(submissions, list)


def test_submissions_df_structure(mock_gql, test_db_fixture):
    """
    Get from the sample data
    obtain the submissions info
    Check the DataFrame and columns
    """
    submissions = mock_gql.get_submissions()

    if submissions:
        submissions_df = submissions_synced_as_df(submissions, test_db_fixture)

        assert submissions_df is not None
        assert isinstance(submissions_df, DataFrame)

        assert "id" in submissions_df.columns
        assert "late" in submissions_df.columns
        assert "missing" in submissions_df.columns
        assert "submitted_at" in submissions_df.columns
        assert "grade" in submissions_df.columns
        assert "assignment_id" in submissions_df.columns
        assert "user_id" in submissions_df.columns
        assert "CreateDate" in submissions_df.columns
        assert "LastModifiedDate" in submissions_df.columns
        assert "graded_at" in submissions_df.columns
