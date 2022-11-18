# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging

from pandas import DataFrame
from typing import cast, Dict

from edfi_canvas_extractor.client_graphql import (
    extract_grades,
)
from edfi_canvas_extractor.extract_graphql import (
    _get_sections,
    _get_enrollments,
    results_store
)


def test_gql_grades_not_empty(
    mock_gql,
    test_db_fixture
):
    sections = _get_sections(mock_gql, test_db_fixture)

    assert sections is not None

    enrollments = _get_enrollments(mock_gql, test_db_fixture)

    assert enrollments is not None

    logging.info("Extracting Grades from Canvas API")
    (enrollments, udm_enrollments) = results_store["enrollments"]
    (sections, _, _) = results_store["sections"]
    udm_grades: Dict[str, DataFrame] = extract_grades(
        enrollments, cast(Dict[str, DataFrame], udm_enrollments), sections
    )

    assert udm_grades is not None
