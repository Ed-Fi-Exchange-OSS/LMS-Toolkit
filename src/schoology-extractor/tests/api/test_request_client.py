# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from schoology_extractor.api.request_client import RequestClient
from schoology_extractor.api.paginated_result import PaginatedResult

FAKE_KEY = 'TEST_KEY'
FAKE_SECRET = 'TEST_SECRET'
FAKE_ENDPOINT_URL = 'FAKE_URL'
DEFAULT_URL = 'https://api.schoology.com/v1/'


@pytest.fixture
def default_request_client():
    return RequestClient(FAKE_KEY, FAKE_SECRET)


class TestRequestClient:

    class Test_when_constructing:
        def test_given_not_passing_in_a_url_then_use_the_DEFAULT_URL(self):
            request_client = RequestClient(FAKE_KEY, FAKE_SECRET)
            assert request_client.base_url == DEFAULT_URL

        def test_given_custom_url_then_use_it_for_the_base_url(self):

            # Arrange
            custom_url = "a_custom_url"

            # Act
            request_client = RequestClient(
                FAKE_KEY, FAKE_SECRET, custom_url)

            # Assert
            assert request_client.base_url == custom_url

        def test_given_None_as_parameters_then_assert_should_fail(self):
            # Assert
            with pytest.raises(AssertionError):
                RequestClient(None, None)   # type: ignore

    class Test_when_building_request_header:
        def test_then_consumer_key_is_present(self, default_request_client):
            assert self._present_in_header(
                default_request_client._request_header,
                header_key="Authorization",
                contained_value=FAKE_KEY
            )

        def test_then_oauth_word_is_present(self, default_request_client):
            assert self._present_in_header(
                default_request_client._request_header,
                header_key="Authorization",
                contained_value="OAuth"
            )

        def _present_in_header(self, request_header, header_key, contained_value):
            header_section = request_header[header_key]
            return header_section.find(contained_value) != -1

    class Test_when_get_method_is_called:
        def test_given_no_parameters_passed_then_throw_assert_exception(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client.get(None)

        def test_then_oauth_base_get_method_is_called(self, mocker, default_request_client):

            # Arrange
            mock_oauth_client = mocker.Mock()
            default_request_client.oauth = mock_oauth_client

            # Act
            default_request_client.get(FAKE_ENDPOINT_URL)

            # Assert
            mock_oauth_client.get.assert_called_once()

        def test_then_right_url_is_passed(self, mocker, default_request_client):

            # Arrange
            expected_url = DEFAULT_URL+FAKE_ENDPOINT_URL
            mock_oauth_client = mocker.Mock()
            default_request_client.oauth = mock_oauth_client

            # Act
            default_request_client.get(FAKE_ENDPOINT_URL)

            # Assert
            request_url = mock_oauth_client.get.call_args.kwargs['url']
            assert expected_url in request_url

    class Test_when_get_assignments_by_section_ids_method_is_called:
        def test_given_no_parameters_passed_then_throw_assert_exception(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client.get_assignments_by_section_ids(None)

        def test_given_an_array_of_ids_then_make_a_call_per_item_in_array(self, default_request_client, mocker):

            # Arrange
            array_of_ids = ['1', '2', '3', '4']
            get_mock = mocker.MagicMock(return_value={"assignment": [{}, {}]})
            default_request_client.get = get_mock

            # Act
            default_request_client.get_assignments_by_section_ids(array_of_ids)

            # Assert
            assert get_mock.call_count == len(array_of_ids)

        def test_given_an_empty_array_of_ids_then_make_a_call_per_item_in_array(self, default_request_client, mocker):

            # Arrange
            array_of_ids = []
            mock_get_client = mocker.MagicMock(return_value={"assignment": "test_assignment"})
            default_request_client.get = mock_get_client

            # Act
            default_request_client.get_assignments_by_section_ids(array_of_ids)

            # Assert
            assert mock_get_client.get.call_count == len(array_of_ids)

        def test_given_an_empty_array_of_ids_then_returns_empty_array(self, default_request_client, mocker):

            # Arrange
            array_of_ids = ['1', '2', '3', '4']
            get_mock = mocker.MagicMock(return_value={})
            default_request_client.get = get_mock

            # Act
            response = default_request_client.get_assignments_by_section_ids(array_of_ids)

            # Assert
            assert (isinstance(response, list) and len(response) == 0)

    class Test_when_get_section_by_course_ids_method_is_called:
        def test_given_no_parameters_passed_then_throw_assert_exception(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client.get_section_by_course_ids(None)

        def test_given_a_parameter_is_passed_then_shoud_make_the_get_calls(self, default_request_client, mocker):

            # Arrange
            get_mock = mocker.MagicMock(return_value=dict())
            default_request_client.get = get_mock
            section_ids = [1, 2, 3, 4]

            # Act
            default_request_client.get_section_by_course_ids(section_ids)

            # Assert
            assert get_mock.call_count == 4

    class Test_when_get_submissions_by_section_id_and_grade_item_id_method_is_called:
        def test_given_no_section_id_passed_then_throw_assert_exception(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client.get_submissions_by_section_id_and_grade_item_id(None, 'grade_item_id')

        def test_given_no_grade_item_id_passed_then_throw_assert_exception(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client.get_submissions_by_section_id_and_grade_item_id('2', None)

        def test_given_a_parameter_is_passed_then_shoud_make_the_get_call(self, default_request_client, mocker):

            # Arrange
            get_mock = mocker.MagicMock(return_value=dict())
            default_request_client.get = get_mock

            # Act
            default_request_client.get_submissions_by_section_id_and_grade_item_id('1', 'grade_item_id')

            # Assert
            assert get_mock.call_count == 1

    class Test_when_get_users_method_is_called:
        def test_given_a_parameter_is_passed_then_shoud_make_the_get_call(self, default_request_client, mocker):

            # Arrange
            get_mock = mocker.MagicMock(return_value={})
            default_request_client.get = get_mock

            # Act
            default_request_client.get_users()

            # Assert
            assert get_mock.call_count == 1

        def test_given_the_get_call_returns_empty_response_then_return_empty_PaginatedResult(self, default_request_client, mocker):

            # Arrange
            get_mock = mocker.MagicMock(return_value={})
            default_request_client.get = get_mock

            # Act
            response = default_request_client.get_users()

            # Assert
            assert isinstance(response, PaginatedResult) and len(response.current_page_items) == 0

        def test_given_the_get_call_returns_users_then_return_list_of_users(self, default_request_client, mocker):

            # Arrange
            fake_list_of_users = [{"test": "test"}, {"test": "test"}, {"test": "test"}]
            mock_oauth_client = mocker.Mock()
            response_json = mocker.Mock()
            response_json.json = mocker.MagicMock(return_value={"user": fake_list_of_users})
            mock_oauth_client.get = mocker.MagicMock(return_value=response_json)
            default_request_client.oauth = mock_oauth_client

            # Act
            response = default_request_client.get_users()

            # Assert
            assert len(response.current_page_items) == len(fake_list_of_users)

    class Test_when__build_pagination_params_method_is_called:
        def test_given_wrong_type_in_params_then_thrown_assertion_error(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client._build_pagination_params([])

        def test_given_correct_parameter_then_url_is_built_correctly(self, default_request_client):
            # Arrange
            items_per_page = 17
            expected_result = f'start=0&limit={items_per_page}'

            # Act
            result = default_request_client._build_pagination_params(items_per_page)

            # Assert
            assert result == expected_result

    class Test_when_get_grading_periods_method_is_called:
        def test_given_wrong_type_in_params_then_thrown_assertion_error(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client.get_grading_periods([])

        def test_given_correct_parameter_then_get_call_is_made(self, default_request_client, mocker):
            # Arrange
            get_mock = mocker.MagicMock(return_value={})
            default_request_client.get = get_mock

            # Act
            default_request_client.get_grading_periods()

            # Assert
            assert get_mock.call_count == 1

    class Test_when_get_courses_method_is_called:
        def test_given_wrong_type_in_params_then_thrown_assertion_error(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client.get_courses([])

        def test_given_correct_parameter_then_get_call_is_made(self, default_request_client, mocker):
            # Arrange
            get_mock = mocker.MagicMock(return_value={})
            default_request_client.get = get_mock

            # Act
            default_request_client.get_courses()

            # Assert
            assert get_mock.call_count == 1
