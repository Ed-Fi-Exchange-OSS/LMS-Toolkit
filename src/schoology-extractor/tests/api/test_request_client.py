# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from schoology_extractor.api.request_client import RequestClient
from schoology_extractor.api.paginated_result import PaginatedResult

fake_key = 'TEST_KEY'
fake_secret = 'TEST_SECRET'
fake_endpoint_url = 'FAKE_URL'
default_url = 'https://api.schoology.com/v1/'


@pytest.fixture
def default_request_client():
    return RequestClient(fake_key, fake_secret)


class TestRequestClient:

    class Test_when_constructing:
        def test_given_not_passing_in_a_url_then_use_the_default_url(self):
            request_client = RequestClient(fake_key, fake_secret)
            assert request_client.base_url == default_url

        def test_given_custom_url_then_use_it_for_the_base_url(self):

            # Arrange
            custom_url = "a_custom_url"

            # Act
            request_client = RequestClient(
                fake_key, fake_secret, custom_url)

            # Assert
            assert request_client.base_url == custom_url

        def test_given_None_as_parameters_then_assert_should_fail(self):
            # Assert
            with pytest.raises(AssertionError):
                RequestClient(None, None)

    class Test_when_get_assignments_by_section_ids_method_is_called:
        def test_given_no_parameters_passed_then_throw_assert_exception(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client.get_assignments_by_section_ids(None)

        def test_given_an_array_of_ids_then_make_a_call_per_item_in_array(self, default_request_client, mocker):

            # Arrange
            array_of_ids = ['1', '2', '3', '4']
            get_mock = mocker.MagicMock(return_value=dict())
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

    class Test_when_get_section_by_id_method_is_called:
        def test_given_no_parameters_passed_then_throw_assert_exception(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client.get_section_by_id(None)

        def test_given_a_parameter_is_passed_then_shoud_make_the_get_call(self, default_request_client, mocker):

            # Arrange
            get_mock = mocker.MagicMock(return_value=dict())
            default_request_client.get = get_mock

            # Act
            default_request_client.get_section_by_id('1')

            # Assert
            assert get_mock.call_count == 1

    class Test_when_get_submissions_by_section_id_method_is_called:
        def test_given_no_parameters_passed_then_throw_assert_exception(self, default_request_client):
            with pytest.raises(AssertionError):
                default_request_client.get_submissions_by_section_id(None)

        def test_given_a_parameter_is_passed_then_shoud_make_the_get_call(self, default_request_client, mocker):

            # Arrange
            get_mock = mocker.MagicMock(return_value=dict())
            default_request_client.get = get_mock

            # Act
            default_request_client.get_submissions_by_section_id('1')

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
