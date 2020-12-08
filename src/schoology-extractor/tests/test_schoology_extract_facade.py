# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Tuple

import pandas as pd
from pandas.core.frame import DataFrame
import pytest
from unittest.mock import Mock
import sqlalchemy

from schoology_extractor.schoology_extract_facade import SchoologyExtractFacade
from schoology_extractor.api.request_client import RequestClient
from schoology_extractor.api.paginated_result import PaginatedResult
from schoology_extractor.mapping import users as usersMap
from schoology_extractor.mapping import sections as sectionsMap
from schoology_extractor.mapping import section_associations as sectionAssocMap
from schoology_extractor.mapping import assignments as assignmentsMap
from schoology_extractor.mapping import submissions as submissionsMap
from schoology_extractor.mapping import attendance as attendanceMap
from schoology_extractor.mapping import discussion_replies as discussionRepliesMap
from schoology_extractor.mapping import discussions as discussionsMap
from schoology_extractor.helpers import sync


def describe_when_getting_users():
    def describe_given_one_user():
        @pytest.fixture
        def result() -> pd.DataFrame:
            request_client = Mock(spec=RequestClient)
            db_engine = Mock(spec=sqlalchemy.engine.base.Engine)
            page_size = 22

            users = {
                "user": [{"uid": 1234, "role_id": 321}],
                "total": 1,
                "links": {"self": "ignore"},
            }
            users_page = PaginatedResult(
                request_client, page_size, users, "user", "ignore me"
            )

            roles = {"role": [{"id": 321, "title": "estudiante"}]}
            roles_page = PaginatedResult(
                request_client, page_size, roles, "role", "ignore me"
            )

            # Arrange
            request_client.get_users.return_value = users_page
            request_client.get_roles.return_value = roles_page

            # Also want to mock the UDM mapper function, since it is well-tested elsewhere
            usersMap.map_to_udm = Mock()
            usersMap.map_to_udm.return_value = pd.DataFrame()

            # This method will be tested in a different test
            sync.sync_resource = Mock(
                side_effect=lambda v, w, x, y="", z="": DataFrame(x)
            )

            service = SchoologyExtractFacade(request_client, page_size, db_engine)

            # Act
            result = service.get_users()

            return result

        def it_should_return_a_data_frame(result):
            assert isinstance(result, pd.DataFrame)

    def describe_given_two_pages_of_users():
        @pytest.fixture
        def system() -> Tuple[pd.DataFrame, Mock]:
            request_client = Mock(spec=RequestClient)
            db_engine = Mock(spec=sqlalchemy.engine.base.Engine)
            page_size = 1

            users = {
                "user": [{"uid": 1234, "role_id": 321}],
                "total": 1,
                "links": {"self": "ignore", "next": "url"},
            }
            users_2 = {
                "user": [{"uid": 1235, "role_id": 321}],
                "total": 1,
                "links": {"self": "ignore"},
            }
            users_page = PaginatedResult(
                request_client, page_size, users, "user", "ignore me"
            )

            roles = {"role": [{"id": 321, "title": "estudiante"}]}
            roles_page = PaginatedResult(
                request_client, page_size, roles, "role", "ignore me"
            )

            request_client.get_users.return_value = users_page
            request_client.get_roles.return_value = roles_page
            request_client.base_url = ""

            request_client.get.return_value = users_2

            # Also want to mock the UDM mapper function, since it is well-tested
            # elsewhere
            usersMap.map_to_udm = Mock()
            usersMap.map_to_udm.return_value = pd.DataFrame()

            # Arrange
            service = SchoologyExtractFacade(request_client, page_size, db_engine)

            # Act
            result = service.get_users()

            return result, usersMap.map_to_udm

        def it_should_return_the_user_in_a_data_frame(system):
            result, _ = system

            assert isinstance(result, pd.DataFrame)

        def it_should_use_first_users_page_when_mapping_to_udm(system):
            _, mock_map_to_udm = system

            args, _ = mock_map_to_udm.call_args
            assert args[0]["uid"][0] == 1234

        def it_should_use_second_users_page_when_mapping_to_udm(system):
            _, mock_map_to_udm = system

            args, _ = mock_map_to_udm.call_args
            assert args[0]["uid"][1] == 1235

        def it_should_use_the_given_roles_when_mapping_to_udm(system):
            _, mock_map_to_udm = system

            args, _ = mock_map_to_udm.call_args
            assert args[1]["id"][0] == 321


def describe_when_getting_sections():
    def describe_given_one_course_with_one_section():
        @pytest.fixture
        def system() -> Tuple[pd.DataFrame, Mock]:
            request_client = Mock(spec=RequestClient)
            db_engine = Mock(spec=sqlalchemy.engine.base.Engine)
            page_size = 22

            courses = {
                "course": [{"id": 3333}],
                "total": 1,
                "links": {"self": "ignore"},
            }
            courses_page = PaginatedResult(
                request_client, page_size, courses, "course", "ignore me"
            )
            request_client.get_courses.return_value = courses_page

            # Also want to mock the UDM mapper function, since it is well-tested
            # elsewhere
            sectionsMap.map_to_udm = Mock()
            sectionsMap.map_to_udm.return_value = pd.DataFrame()

            sections = {
                "section": [{"id": 1234}],
                "total": 1,
                "links": {"self": "ignore"},
            }
            sections_page = PaginatedResult(
                request_client, page_size, sections, "section", "ignore me"  # type: ignore
            )

            get_sections_mock = request_client.get_section_by_course_id
            get_sections_mock.return_value = sections_page

            # Arrange
            service = SchoologyExtractFacade(request_client, page_size, db_engine)

            # Act
            result = service.get_sections()

            return result, sectionsMap.map_to_udm

        def it_should_return_a_data_frame(system):
            result, _ = system

            assert isinstance(result, pd.DataFrame)

        def it_should_map_to_the_udm(system):
            _, map_to_udm = system

            map_to_udm.assert_called_once()

    def describe_given_two_pages_of_courses():
        @pytest.fixture
        def system() -> Tuple[pd.DataFrame, Mock]:
            request_client = Mock(spec=RequestClient)
            db_engine = Mock(spec=sqlalchemy.engine.base.Engine)
            page_size = 1

            courses = {
                "course": [{"id": 3333}],
                "total": 1,
                "links": {"self": "ignore"},
            }
            courses_page = PaginatedResult(
                request_client, page_size, courses, "course", "ignore me"
            )
            request_client.get_courses.return_value = courses_page

            # Also want to mock the UDM mapper function, since it is well-tested
            # elsewhere
            sectionsMap.map_to_udm = Mock()
            sectionsMap.map_to_udm.return_value = pd.DataFrame()

            sections = {
                "section": [{"id": 1234}],
                "total": 1,
                "links": {"self": "ignore"},
            }
            sections_page = PaginatedResult(
                request_client, page_size, sections, "section", "ignore me"
            )
            get_sections_mock = request_client.get_section_by_course_id
            get_sections_mock.return_value = sections_page

            # Arrange
            service = SchoologyExtractFacade(request_client, page_size, db_engine)

            # Act
            result = service.get_sections()

            return result, get_sections_mock

        def it_should_use_first_course_when_getting_sections(system):
            _, get_sections_mock = system

            args = get_sections_mock.call_args
            print(get_sections_mock.call_args[0][0])
            assert 3333 == args[0][0]


def describe_when_getting_assignments():
    def describe_given_a_section_has_one_assignment():
        @pytest.fixture
        def system() -> Tuple[pd.DataFrame, Mock, Mock]:
            request_client = Mock(spec=RequestClient)
            db_engine = Mock(spec=sqlalchemy.engine.base.Engine)
            page_size = 22
            section_id = 1234

            assignments = [
                {
                    "id": 3333,
                    "due": "3456-1-2 01:23:45",
                    "description": "",
                    "max_points": 4,
                    "title": "1",
                    "type": "assignment",
                    "section_id": section_id,
                }
            ]
            assignments_response_mock = {
                "assignment": assignments,
                "total": 1,
                "links": {"self": "ignore"},
            }
            assignments_page = PaginatedResult(
                request_client,
                page_size,
                assignments_response_mock,
                "assignment",
                "ignore me",
            )

            # Arrange
            get_assignments_mock = request_client.get_assignments
            get_assignments_mock.return_value = assignments_page

            # Mock the UDM mapper
            assignmentsMap.map_to_udm = Mock()
            assignmentsMap.map_to_udm.return_value = pd.DataFrame()

            service = SchoologyExtractFacade(request_client, page_size, db_engine)

            # Act
            result = service.get_assignments(section_id)

            return result, get_assignments_mock, assignmentsMap.map_to_udm

        def it_should_return_a_DataFrame(system):
            result, _, _ = system
            assert isinstance(result, pd.DataFrame)

        def it_should_query_for_the_given_section(system):
            _, get_assignments_mock, _ = system

            args = get_assignments_mock.call_args
            assert 1234 == args[0][0]

        def it_should_map_results_to_the_udm(system):
            _, _, mapper = system

            mapper.assert_called_once()

        def it_should_map_first_assignment(system):
            _, _, mapper = system

            df = mapper.call_args[0][0]
            assert df["id"].iloc[0] == 3333


def describe_when_getting_submissions():
    def describe_given_one_assignment_and_one_submission():
        @pytest.fixture
        def result() -> DataFrame:
            request_client = Mock(spec=RequestClient)
            db_engine = Mock(spec=sqlalchemy.engine.base.Engine)
            # This method will be tested in a different test
            sync.sync_resource = Mock(
                side_effect=lambda v, w, x, y="", z="": DataFrame(x)
            )
            # Mock the UDM mapper
            submissionsMap.map_to_udm = Mock()
            submissionsMap.map_to_udm.side_effect = lambda x: x
            page_size = 22

            assignment_id = 345
            section_id = 123
            submissions = {
                "revision": [
                    {
                        "revision_id": 1,
                        "uid": 100032890,
                    }
                ],
                "total": 1,
                "links": {"self": "ignore"},
            }
            submissions_page = PaginatedResult(
                request_client, page_size, submissions, "revision", "ignore me"
            )

            # Arrange
            request_client.get_submissions_by_section_id_and_grade_item_id.return_value = (
                submissions_page
            )

            service = SchoologyExtractFacade(request_client, page_size, db_engine)

            # Act
            result = service.get_submissions(assignment_id, section_id)

            return result

        def it_should_return_the_submission(result: DataFrame):
            assert result["revision_id"][0] == 1


def describe_when_getting_section_associations():
    @pytest.fixture
    def system() -> Tuple[pd.DataFrame, Mock, Mock]:
        request_client = Mock(spec=RequestClient)
        page_size = 1

        # Also want to mock the UDM mapper function, since it is well-tested
        # elsewhere
        sectionAssocMap.map_to_udm = Mock()
        sectionAssocMap.map_to_udm.return_value = pd.DataFrame()

        # Mock the API calls
        section_id = 1234
        get_sections_mock = request_client.get_enrollments
        sections_response_mock = {
            "sections": [{"id": 1}, {"id": 2}],
            "total": 1,
            "links": {"self": "ignore"},
        }
        sections_page = PaginatedResult(
            request_client, page_size, sections_response_mock, "sections", "ignore me"
        )
        get_sections_mock.return_value = sections_page

        # Mock the Sync process
        sync.sync_resource = Mock(side_effect=lambda v, w, x, y="", z="": DataFrame(x))

        db_engine = Mock(spec=sqlalchemy.engine.base.Engine)

        # Arrange
        service = SchoologyExtractFacade(request_client, page_size, db_engine)

        # Act
        result = service.get_section_associations(section_id)

        return result, sectionAssocMap.map_to_udm, sync.sync_resource

    def it_should_return_a_data_frame(system):
        result, _, _ = system

        assert isinstance(result, pd.DataFrame)

    def it_should_map_to_the_udm(system):
        _, mapper, _ = system

        mapper.assert_called_once()

    def it_should_map_first_enrollment(system):
        _, mapper, _ = system

        df = mapper.call_args[0][0]
        assert df["id"].iloc[0] == 1

    def it_should_map_second_enrollment(system):
        _, mapper, _ = system

        df = mapper.call_args[0][0]
        assert df["id"].iloc[1] == 2

    def it_should_use_the_sync_process(system):
        _, _, sync_mock = system
        sync_mock.assert_called_once()


def describe_when_getting_attendance_events():
    @pytest.fixture
    def system() -> Tuple[pd.DataFrame, Mock]:
        request_client = Mock(spec=RequestClient)
        page_size = 1

        # Also want to mock the UDM mapper function, since it is well-tested
        # elsewhere
        attendanceMap.map_to_udm = Mock()
        attendanceMap.map_to_udm.return_value = pd.DataFrame()

        section_id = 1234
        get_attendance_mock = request_client.get_attendance
        get_attendance_mock.return_value = [{"enrollment_id": 1}, {"enrollment_id": 2}]

        db_engine = Mock(spec=sqlalchemy.engine.base.Engine)

        # Actual section associations are irrelevant for these tests - just need
        # to ensure that the object is passed around correctly.
        section_associations = pd.DataFrame([{"id": 123}])

        # Arrange
        service = SchoologyExtractFacade(request_client, page_size, db_engine)

        # Act
        result = service.get_attendance_events(section_id, section_associations)

        return result, attendanceMap.map_to_udm

    def it_should_return_a_data_frame(system):
        result, _ = system

        assert isinstance(result, pd.DataFrame)

    def it_should_map_to_the_udm(system):
        _, mapper = system

        mapper.assert_called_once()

    def it_should_pass_the_api_response_into_the_mapper(system):
        _, mapper = system

        df = mapper.call_args[0][0]
        assert df[0]["enrollment_id"] == 1

    def it_should_pass_the_section_associations_into_the_mapper(system):
        _, mapper = system

        df = mapper.call_args[0][1]
        assert df["id"].iloc[0] == 123


def describe_when_getting_user_activities():
    @pytest.fixture
    def system() -> dict:
        request_client = Mock(spec=RequestClient)
        page_size = 1

        discussionRepliesMap.map_to_udm = Mock()
        discussionRepliesMap.map_to_udm.return_value = pd.DataFrame()
        discussionsMap.map_to_udm = Mock()
        discussionsMap.map_to_udm.return_value = pd.DataFrame()

        section_id = 1234
        get_discussions_mock = request_client.get_discussions
        get_discussions_mock.return_value = [{"id": 1}, {"id": 2}]

        get_discussion_replies_mock = request_client.get_discussion_replies
        get_discussion_replies_mock.return_value = [
            {"fake_dict_attrib": 1},
            {"fake_dict_attrib": 2},
        ]

        db_engine = Mock(spec=sqlalchemy.engine.base.Engine)

        # Arrange
        service = SchoologyExtractFacade(request_client, page_size, db_engine)

        # Act
        result = service.get_section_activities(section_id)

        return {
            "result": result,
            "replies_mock": discussionRepliesMap.map_to_udm,
            "discussions_mock": discussionsMap.map_to_udm,
        }

    def it_should_return_a_data_frame(system):

        assert isinstance(system["result"], pd.DataFrame)

    def it_should_map_replies_to_the_udm(system):
        assert system["replies_mock"].called

    def it_should_map_discussions_to_the_udm(system):
        assert system["discussions_mock"].called
