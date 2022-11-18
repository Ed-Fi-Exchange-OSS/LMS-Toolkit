# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from pandas import DataFrame
from typing import cast, Dict

from edfi_canvas_extractor.graphql.assignments import assignments_synced_as_df
from edfi_canvas_extractor.graphql.courses import courses_synced_as_df
from edfi_canvas_extractor.graphql.enrollments import enrollments_synced_as_df
from edfi_canvas_extractor.graphql.sections import sections_synced_as_df
from edfi_canvas_extractor.graphql.students import students_synced_as_df
from edfi_canvas_extractor.client_graphql import (
    extract_grades,
)
from edfi_canvas_extractor.extract_graphql import (
    _get_sections,
    _get_enrollments,
    results_store
)


@pytest.fixture(autouse=True, scope="class")
def graphql(request, gql):
    request.cls.graphql_extractor = gql


@pytest.mark.usefixtures("graphql")
class TestExtractorIntegration:

    def test_gql_data_fetched(self):
        assert self.graphql_extractor.has_data is True  # type: ignore

    def test_gql_courses_not_empty(self):
        """
        Get from the sample data
        obtain the courses info
        Check and check the return type
        """
        courses = self.graphql_extractor.get_courses()  # type: ignore

        assert courses is not None
        assert isinstance(courses, list)

    def test_gql_courses_df_structure(self, test_db_fixture):
        """
        Get from the sample data
        obtain the courses info
        Check the DataFrame
        """
        courses = self.graphql_extractor.get_courses()  # type: ignore
        courses_df = courses_synced_as_df(courses, test_db_fixture)

        assert courses_df is not None
        assert isinstance(courses_df, DataFrame)

    def test_gql_sections_not_empty(self):
        """
        Get from the sample data
        obtain the sections info
        Check and check the return type
        """
        sections = self.graphql_extractor.get_sections()  # type: ignore

        assert sections is not None
        assert isinstance(sections, list)

    def test_gql_sections_df_structure(self, test_db_fixture):
        """
        Get from the sample data
        obtain the sections info
        Check the DataFrame
        """
        sections = self.graphql_extractor.get_sections()  # type: ignore
        sections_df = sections_synced_as_df(sections, test_db_fixture)

        assert sections_df is not None
        assert isinstance(sections_df, DataFrame)

    def test_gql_students_not_empty(self):
        """
        Get from the sample data
        obtain the students info
        Check and check the return type
        """
        students = self.graphql_extractor.get_students()  # type: ignore

        assert students is not None
        assert isinstance(students, list)

    def test_gql_students_df_structure(self, test_db_fixture):
        """
        Get from the sample data
        obtain the students info
        Check the DataFrame
        """
        students = self.graphql_extractor.get_students()  # type: ignore
        students_df = students_synced_as_df(students, test_db_fixture)

        assert students_df is not None
        assert isinstance(students_df, DataFrame)

    def test_gql_enrollments_not_empty(self):
        """
        Get from the sample data
        obtain the enrollments info
        Check and check the return type
        """
        enrollments = self.graphql_extractor.get_enrollments()  # type: ignore

        assert enrollments is not None
        assert isinstance(enrollments, list)

    def test_gql_enrollments_df_structure(self, test_db_fixture):
        """
        Get from the sample data
        obtain the enrollments info
        Check the DataFrame
        """
        enrollments = self.graphql_extractor.get_enrollments()  # type: ignore
        enrollments_df = enrollments_synced_as_df(enrollments, test_db_fixture)

        assert enrollments_df is not None
        assert isinstance(enrollments_df, DataFrame)

    def test_gql_assignments_not_empty(self):
        """
        Get from the sample data
        obtain the assignments info
        Check and check the return type
        """
        assignments = self.graphql_extractor.get_assignments()  # type: ignore

        assert assignments is not None
        assert isinstance(assignments, list)

    def test_gql_assignments_df_structure(self, test_db_fixture):
        """
        Get from the sample data
        obtain the assignments info
        Check the DataFrame
        """
        assignments = self.graphql_extractor.get_assignments()  # type: ignore
        assignments_df = assignments_synced_as_df(assignments, test_db_fixture)

        assert assignments_df is not None
        assert isinstance(assignments_df, DataFrame)

    def test_gql_grades_not_empty(
        self,
        gql,
        test_db_fixture
    ):
        sections = _get_sections(gql, test_db_fixture)

        assert sections is not None

        enrollments = _get_enrollments(gql, test_db_fixture)

        assert enrollments is not None

        (enrollments, udm_enrollments) = results_store["enrollments"]
        (sections, _, _) = results_store["sections"]
        udm_grades: Dict[str, DataFrame] = extract_grades(
            enrollments, cast(Dict[str, DataFrame], udm_enrollments), sections
        )

        assert udm_grades is not None
