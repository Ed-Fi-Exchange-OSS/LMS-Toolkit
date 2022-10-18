# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


from pandas import DataFrame
from edfi_canvas_extractor.graphql.students import students_synced_as_df


def test_students(gql):
    """
    Get from the sample data
    obtain the students info
    Check and check the return type
    """
    students = gql.get_students()

    assert students is not None
    assert isinstance(students, list)


def test_students_df(gql, test_db_fixture):
    """
    Get from the sample data
    obtain the students info
    Check the DataFrame and columns
    """
    students = gql.get_students()
    students_df = students_synced_as_df(students, test_db_fixture)

    assert students_df is not None
    assert isinstance(students_df, DataFrame)

    assert "id" in students_df.columns
    assert "sis_user_id" in students_df.columns
    assert "created_at" in students_df.columns
    assert "name" in students_df.columns
    assert "email" in students_df.columns
    assert "login_id" in students_df.columns
    assert "CreateDate" in students_df.columns
    assert "LastModifiedDate" in students_df.columns
