# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from logging import Logger
from typing import Tuple

import pandas as pd
import pytest
from unittest.mock import Mock

from schoology_extractor.schoology_request_service import SchoologyRequestService
from schoology_extractor.api.request_client import RequestClient
from schoology_extractor.api.paginated_result import PaginatedResult
from schoology_extractor.mapping import users as usersMap


def describe_when_getting_users():
    def describe_given_one_user():
        @pytest.fixture
        def result() -> pd.DataFrame:
            logger = Mock(spec=Logger)
            request_client = Mock(spec=RequestClient)
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

            request_client.get_users.return_value = users_page
            request_client.get_roles.return_value = roles_page

            # Also want to mock the UDM mapper function, since it is well-tested elsewhere
            usersMap.map_to_udm = Mock()
            usersMap.map_to_udm.return_value = pd.DataFrame()

            # Arrange
            service = SchoologyRequestService(logger, request_client, page_size)

            # Act
            result = service.get_users()

            return result

        def it_should_return_a_data_frame(result):
            assert isinstance(result, pd.DataFrame)

    def describe_given_two_pages_of_users():
        @pytest.fixture
        def system() -> Tuple[pd.DataFrame, Mock]:
            logger = Mock(spec=Logger)
            request_client = Mock(spec=RequestClient)
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
            service = SchoologyRequestService(logger, request_client, page_size)

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
        def system() -> Tuple[list, Mock]:
            logger = Mock(spec=Logger)
            request_client = Mock(spec=RequestClient)
            page_size = 22

            courses = {
                "course": [{"id": 3333}],
                "total": 1,
                "links": {"self": "ignore"}
            }
            courses_page = PaginatedResult(
                request_client, page_size, courses, "course", "ignore me"
            )
            request_client.get_courses.return_value = courses_page

            sections = [{"id": 1234}]
            get_sections_mock = request_client.get_section_by_course_ids
            get_sections_mock.return_value = sections

            # Arrange
            service = SchoologyRequestService(logger, request_client, page_size)

            # Act
            result = service.get_sections()

            return result, get_sections_mock

        def it_should_return_the_sections_list(system):
            result, _ = system

            assert result[0]["id"] == 1234

    def describe_given_two_pages_of_courses():
        @pytest.fixture
        def system() -> Tuple[list, Mock]:
            logger = Mock(spec=Logger)
            request_client = Mock(spec=RequestClient)
            page_size = 1

            courses = {
                "course": [{"id": 3333}],
                "total": 1,
                "links": {"self": "ignore", "next": "next"}
            }
            courses_page = PaginatedResult(
                request_client, page_size, courses, "course", "ignore me"
            )
            request_client.get_courses.return_value = courses_page

            courses_2 = {
                "course": [{"id": 3334}],
                "total": 1,
                "links": {"self": "ignore"}
            }
            request_client.base_url = ""
            request_client.get.return_value = courses_2

            sections = [{"id": 1234}]
            get_sections_mock = request_client.get_section_by_course_ids
            get_sections_mock.return_value = sections

            # Arrange
            service = SchoologyRequestService(logger, request_client, page_size)

            # Act
            result = service.get_sections()

            return result, get_sections_mock

        def it_should_return_the_sections_list(system):
            result, _ = system

            assert result[0]["id"] == 1234

        def it_should_use_first_course_when_getting_sections(system):
            _, get_sections_mock = system

            args = get_sections_mock.call_args
            assert 3333 in args[0][0]

        def it_should_use_second_course_when_getting_sections(system):
            _, get_sections_mock = system

            args = get_sections_mock.call_args
            assert 3334 in args[0][0]
