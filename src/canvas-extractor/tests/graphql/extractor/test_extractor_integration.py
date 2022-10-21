# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
import pytest

from pandas import DataFrame
from pathlib import Path
from sqlalchemy import create_engine

from edfi_canvas_extractor.graphql.extractor import GraphQLExtractor
from edfi_canvas_extractor.graphql.schema import query_builder

from edfi_canvas_extractor.graphql.assignments import assignments_synced_as_df
from edfi_canvas_extractor.graphql.courses import courses_synced_as_df
from edfi_canvas_extractor.graphql.enrollments import enrollments_synced_as_df
from edfi_canvas_extractor.graphql.sections import sections_synced_as_df
from edfi_canvas_extractor.graphql.students import students_synced_as_df


CANVAS_BASE_URL = os.environ['POETRY_CANVAS_BASE_URL']
CANVAS_ACCESS_TOKEN = os.environ['POETRY_CANVAS_ACCESS_TOKEN']
START_DATE = "2021-01-01"
END_DATE = "2030-01-01"
DB_FILE = "tests/graphql/test.db"


@pytest.fixture(scope="class")
def gql_class():
    gql = GraphQLExtractor(
        CANVAS_BASE_URL,
        CANVAS_ACCESS_TOKEN,
        "1",
        START_DATE,
        END_DATE,
        )
    yield gql


@pytest.fixture(scope="class")
def graphql_class(gql_class):
    query = query_builder(account_id=1)
    data = gql_class.get_from_canvas(query)
    gql_class.extract(data)

    yield gql_class


@pytest.fixture(scope="class")
def test_db_fixture():
    Path(DB_FILE).unlink(missing_ok=True)
    yield create_engine(f"sqlite:///{DB_FILE}", echo=True)
    # Path(DB_FILE).unlink(missing_ok=True)


class TestExtractorIntegration:

    def test_extractor_request(self, gql_class):
        query = query_builder(account_id=1)
        data = gql_class.get_from_canvas(query)

        assert data is not None

    def test_extractor_courses(self, graphql_class):
        """
        Get from the sample data
        obtain the courses info
        Check and check the return type
        """
        courses = graphql_class.get_courses()

        assert courses is not None
        assert isinstance(courses, list)

    def test_extractor_courses_df(self, graphql_class, test_db_fixture):
        """
        Get from the sample data
        obtain the courses info
        Check the DataFrame
        """
        courses = graphql_class.get_courses()
        courses_df = courses_synced_as_df(courses, test_db_fixture)

        assert courses_df is not None
        assert isinstance(courses_df, DataFrame)

    def test_extractor_sections(self, graphql_class):
        """
        Get from the sample data
        obtain the sections info
        Check and check the return type
        """
        sections = graphql_class.get_sections()

        assert sections is not None
        assert isinstance(sections, list)

    def test_extractor_sections_df(self, graphql_class, test_db_fixture):
        """
        Get from the sample data
        obtain the sections info
        Check the DataFrame
        """
        sections = graphql_class.get_sections()
        sections_df = sections_synced_as_df(sections, test_db_fixture)

        assert sections_df is not None
        assert isinstance(sections_df, DataFrame)

    def test_extractor_students(self, graphql_class):
        """
        Get from the sample data
        obtain the students info
        Check and check the return type
        """
        students = graphql_class.get_students()

        assert students is not None
        assert isinstance(students, list)

    def test_students_df(self, graphql_class, test_db_fixture):
        """
        Get from the sample data
        obtain the students info
        Check the DataFrame
        """
        students = graphql_class.get_students()
        students_df = students_synced_as_df(students, test_db_fixture)

        assert students_df is not None
        assert isinstance(students_df, DataFrame)

    def test_extractor_enrollments(self, graphql_class):
        """
        Get from the sample data
        obtain the enrollments info
        Check and check the return type
        """
        enrollments = graphql_class.get_enrollments()

        assert enrollments is not None
        assert isinstance(enrollments, list)

    def test_enrollments_df(self, graphql_class, test_db_fixture):
        """
        Get from the sample data
        obtain the enrollments info
        Check the DataFrame
        """
        enrollments = graphql_class.get_enrollments()
        enrollments_df = enrollments_synced_as_df(enrollments, test_db_fixture)

        assert enrollments_df is not None
        assert isinstance(enrollments_df, DataFrame)

    def test_extractor_assignments(self, graphql_class):
        """
        Get from the sample data
        obtain the assignments info
        Check and check the return type
        """
        assignments = graphql_class.get_assignments()

        assert assignments is not None
        assert isinstance(assignments, list)

    def test_assignments_df(self, graphql_class, test_db_fixture):
        """
        Get from the sample data
        obtain the assignments info
        Check the DataFrame
        """
        assignments = graphql_class.get_assignments()
        assignments_df = assignments_synced_as_df(assignments, test_db_fixture)

        assert assignments_df is not None
        assert isinstance(assignments_df, DataFrame)
