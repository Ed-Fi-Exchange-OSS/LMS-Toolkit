# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from edfi_canvas_extractor.graphql.schema import query_builder


@pytest.mark.skip(reason="This test connects graphql to API")
def test_graphql_request(gql_no_run):
    query = query_builder(1, "")
    body = gql_no_run.get_from_canvas(query)

    assert query is not None
    assert body is not None


@pytest.mark.skip(reason="This test connects graphql to API")
def test_gql_courses_not_empty(gql_run):
    assert gql_run.courses is not None
    assert isinstance(gql_run.courses, list)


@pytest.mark.skip(reason="This test connects graphql to API")
def test_gql_sections_not_empty(gql_run):
    assert gql_run.sections is not None
    assert isinstance(gql_run.sections, list)


@pytest.mark.skip(reason="This test connects graphql to API")
def test_gql_enrollments_not_empty(gql_run):
    assert gql_run.enrollments is not None
    assert isinstance(gql_run.enrollments, list)


@pytest.mark.skip(reason="This test connects graphql to API")
def test_gql_students_not_empty(gql_run):
    assert gql_run.students is not None
    assert isinstance(gql_run.students, list)
