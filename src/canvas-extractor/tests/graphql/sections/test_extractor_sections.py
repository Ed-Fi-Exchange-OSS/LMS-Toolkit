# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


from pandas import DataFrame
from edfi_canvas_extractor.graphql.sections import sections_synced_as_df


def test_sections(gql_no_run, api):
    """
    Get from the sample data
    obtain the sections info
    Check and check the return type
    """
    gql_no_run.extract(api)
    sections = gql_no_run.get_sections()

    assert api is not None

    assert sections is not None
    assert isinstance(sections, list)


def test_sections_df(gql_no_run, api, test_db_fixture):
    """
    Get from the sample data
    obtain the sections info
    Check the DataFrame and columns
    """
    gql_no_run.extract(api)
    sections = gql_no_run.get_sections()

    sections_df = sections_synced_as_df(sections, test_db_fixture)

    assert sections_df is not None
    assert isinstance(sections_df, DataFrame)

    assert "id" in sections_df.columns
    assert "name" in sections_df.columns
    assert "sis_section_id" in sections_df.columns
    assert "course_id" in sections_df.columns
    assert "CreateDate" in sections_df.columns
    assert "LastModifiedDate" in sections_df.columns
