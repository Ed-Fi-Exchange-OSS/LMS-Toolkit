# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


from pandas import DataFrame
from edfi_canvas_extractor.graphql.assignments import assignments_synced_as_df


def test_assignments(gql):
    """
    Get from the sample data
    obtain the assignments info
    Check and check the return type
    """
    assignments = gql.get_assignments()

    assert assignments is not None
    assert isinstance(assignments, list)


def test_assignments_df(gql, test_db_fixture):
    """
    Get from the sample data
    obtain the assignments info
    Check the DataFrame and columns
    """
    assignments = gql.get_assignments()
    assignments_df = assignments_synced_as_df(assignments, test_db_fixture)

    assert assignments_df is not None
    assert isinstance(assignments_df, DataFrame)

    assert "id" in assignments_df.columns
    assert "name" in assignments_df.columns
    assert "description" in assignments_df.columns
    assert "created_at" in assignments_df.columns
    assert "updated_at" in assignments_df.columns
    assert "lock_at" in assignments_df.columns
    assert "unlock_at" in assignments_df.columns
    assert "due_at" in assignments_df.columns
    assert "submission_types" in assignments_df.columns
    assert "course_id" in assignments_df.columns
    assert "points_possible" in assignments_df.columns
    assert "CreateDate" in assignments_df.columns
    assert "LastModifiedDate" in assignments_df.columns
