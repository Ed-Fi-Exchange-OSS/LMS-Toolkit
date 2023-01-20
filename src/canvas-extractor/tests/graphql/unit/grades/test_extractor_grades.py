# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import pytest

from pandas import DataFrame
from typing import cast, Dict, Tuple

from edfi_canvas_extractor.client_graphql import (
    extract_grades,
)
from edfi_canvas_extractor.extract_graphql import (
    _get_sections,
    _get_enrollments,
    results_store
)


@pytest.fixture(autouse=True, scope="class")
def get_results(request, mock_gql, test_db_fixture):
    _get_sections(mock_gql, test_db_fixture)
    _get_enrollments(mock_gql, test_db_fixture)
    request.cls.results_store = results_store


def extracted_grades(results_store: Dict[str, Tuple]):
    logging.info("Extracting Grades from Canvas API")
    (enrollments, udm_enrollments) = results_store["enrollments"]
    (sections, _, _) = results_store["sections"]
    udm_grades: Dict[str, DataFrame] = extract_grades(
        enrollments, cast(Dict[str, DataFrame], udm_enrollments), sections
    )
    return udm_grades


@pytest.mark.unit
class TestExtractorGrades:

    def test_results_store(self):
        assert self.results_store["sections"] is not None  # type: ignore
        assert self.results_store["enrollments"] is not None  # type: ignore

    def test_gql_grades_not_empty(self):
        grades = extracted_grades(self.results_store)  # type: ignore
        assert grades is not None

    def test_gql_grades_duplicates(self):
        grades = extracted_grades(self.results_store)  # type: ignore
        duplicates_found = 0
        for _, grade_df in grades.items():
            if grade_df.duplicated().any():
                duplicates_found += 1
        assert duplicates_found == 0
