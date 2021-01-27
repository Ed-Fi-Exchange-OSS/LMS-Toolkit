# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Tuple
from unittest.mock import Mock
from canvasapi.canvas import Canvas

from pandas import DataFrame
import pytest
import sqlalchemy

from canvas_extractor import extract_facade
from canvas_extractor.api import (
    courses as coursesApi,
    sections as sectionsApi,
    students as studentsApi,
    assignments as assignmentsApi,
    authentication_events as authEventsApi,
)
from canvas_extractor.mapping import (
    sections as sectionsMap,
    users as usersMap,
    assignments as assignmentsMap,
    authentication_events as authEventsMap
)

TEST_START_DATE = "2021-01-01"
TEST_END_DATE = "2021-12-31"


@pytest.fixture
def canvas_mock():
    return Mock(spec=Canvas)


@pytest.fixture
def sync_db_mock():
    return Mock(spec=sqlalchemy.engine.base.Engine)


def describe_when_extract_courses_is_called():
    @pytest.fixture
    def system(canvas_mock, sync_db_mock):
        coursesApi.courses_synced_as_df = Mock(return_value=[])  # noqa: F811, F841
        coursesApi.request_courses = Mock(return_value=DataFrame())  # noqa: F811, F841
        extract_facade.extract_courses(
            canvas_mock, TEST_START_DATE, TEST_END_DATE, sync_db_mock
        )
        return (coursesApi.courses_synced_as_df, coursesApi.request_courses)

    def it_should_call_sync_method(system: Tuple[Mock, Mock]):
        (sync, _) = system
        assert sync.called

    def it_should_call_request_method(system: Tuple[Mock, Mock]):
        (_, request) = system
        assert request.called


def describe_when_extract_sections_is_called():
    @pytest.fixture
    def system(sync_db_mock):
        sectionsApi.sections_synced_as_df = Mock(return_value=[])
        sectionsApi.request_sections = Mock(return_value=DataFrame())
        sectionsMap.map_to_udm_sections = Mock(return_value=DataFrame())

        extract_facade.extract_sections([], sync_db_mock)
        return {
            "sync": sectionsApi.sections_synced_as_df,
            "request": sectionsApi.request_sections,
            "map": sectionsMap.map_to_udm_sections,
        }

    def it_should_call_sync_method(system: dict):
        assert system["sync"].called

    def it_should_call_request_method(system: dict):
        assert system["request"].called

    def it_should_call_map_method(system: dict):
        assert system["map"].called


def describe_when_extract_students_is_called():
    @pytest.fixture
    def system(sync_db_mock):
        studentsApi.students_synced_as_df = Mock(return_value=[])  # noqa: F811, F841
        studentsApi.request_students = Mock(
            return_value=DataFrame()
        )  # noqa: F811, F841
        usersMap.map_to_udm_users = Mock(return_value=DataFrame())
        extract_facade.extract_students([], sync_db_mock)
        return {
            "sync": studentsApi.students_synced_as_df,
            "request": studentsApi.request_students,
            "map": usersMap.map_to_udm_users,
        }

    def it_should_call_sync_method(system: dict):
        assert system["sync"].called

    def it_should_call_request_method(system: dict):
        assert system["request"].called

    def it_should_call_map_method(system: dict):
        assert system["map"].called


def describe_when_extract_assignments_is_called():
    @pytest.fixture
    def system(sync_db_mock):
        assignmentsApi.assignments_synced_as_df = Mock(
            return_value=[]
        )  # noqa: F811, F841
        assignmentsApi.request_assignments = Mock(
            return_value=DataFrame()
        )  # noqa: F811, F841
        assignmentsMap.map_to_udm_assignments = Mock(return_value=DataFrame())
        extract_facade.extract_assignments([], DataFrame(), sync_db_mock)
        return {
            "sync": assignmentsApi.assignments_synced_as_df,
            "request": assignmentsApi.request_assignments,
            "map": assignmentsMap.map_to_udm_assignments,
        }

    def it_should_call_sync_method(system: dict):
        assert system["sync"].called

    def it_should_call_request_method(system: dict):
        assert system["request"].called

    def it_should_call_map_method(system: dict):
        assert system["map"].called


def describe_when_extract_submissions_is_called():
    @pytest.fixture
    def system(sync_db_mock):
        assignmentsApi.assignments_synced_as_df = Mock(
            return_value=[]
        )  # noqa: F811, F841
        assignmentsApi.request_assignments = Mock(
            return_value=DataFrame()
        )  # noqa: F811, F841
        assignmentsMap.map_to_udm_assignments = Mock(return_value=DataFrame())
        extract_facade.extract_assignments([], DataFrame(), sync_db_mock)
        return {
            "sync": assignmentsApi.assignments_synced_as_df,
            "request": assignmentsApi.request_assignments,
            "map": assignmentsMap.map_to_udm_assignments,
        }

    def it_should_call_sync_method(system: dict):
        assert system["sync"].called

    def it_should_call_request_method(system: dict):
        assert system["request"].called

    def it_should_call_map_method(system: dict):
        assert system["map"].called


def describe_when_extract_system_activities_is_called():
    @pytest.fixture
    def system(sync_db_mock):
        authEventsApi.authentication_events_synced_as_df = Mock(
            return_value=[]
        )  # noqa: F811, F841
        authEventsApi.request_events = Mock(
            return_value=DataFrame()
        )  # noqa: F811, F841
        authEventsMap.map_to_udm_system_activities = Mock(return_value=DataFrame())
        extract_facade.extract_system_activities([], "", "", sync_db_mock)
        return {
            "sync": authEventsApi.authentication_events_synced_as_df,
            "request": authEventsApi.request_events,
            "map": authEventsMap.map_to_udm_system_activities,
        }

    def it_should_call_sync_method(system: dict):
        assert system["sync"].called

    def it_should_call_request_method(system: dict):
        assert system["request"].called

    def it_should_call_map_method(system: dict):
        assert system["map"].called
