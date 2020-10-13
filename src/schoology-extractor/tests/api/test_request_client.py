# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest

from schoology_extractor.api.request_client import RequestClient
from schoology_extractor.api.paginated_result import PaginatedResult

FAKE_KEY = "TEST_KEY"
FAKE_SECRET = "TEST_SECRET"
FAKE_ENDPOINT_URL = "FAKE_URL"
DEFAULT_URL = "https://api.schoology.com/v1/"


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
            request_client = RequestClient(FAKE_KEY, FAKE_SECRET, custom_url)

            # Assert
            assert request_client.base_url == custom_url

    class Test_when_building_request_header:
        def test_then_consumer_key_is_present(self, default_request_client):
            assert self._present_in_header(
                default_request_client._request_header,
                header_key="Authorization",
                contained_value=FAKE_KEY,
            )

        def test_then_oauth_word_is_present(self, default_request_client):
            assert self._present_in_header(
                default_request_client._request_header,
                header_key="Authorization",
                contained_value="OAuth",
            )

        def _present_in_header(self, request_header, header_key, contained_value):
            header_section = request_header[header_key]
            return header_section.find(contained_value) != -1

    class Test_when_get_method_is_called:
        def test_and_error_occurs_then_raise_an_HTTPError(
            self, requests_mock, default_request_client
        ):
            expected_url = DEFAULT_URL + FAKE_ENDPOINT_URL

            # Arrange
            requests_mock.get(expected_url, reason="BadRequest", status_code=400, text="no good")

            # Act
            try:
                default_request_client.get(FAKE_ENDPOINT_URL)

                raise RuntimeError("expected an error to occur")
            except RuntimeError as ex:
                assert str(ex) == "BadRequest (400): no good"

        def test_given_no_parameters_passed_then_throw_assert_exception(
            self, default_request_client
        ):
            with pytest.raises(AssertionError):
                default_request_client.get(None)

    class Test_when_get_assignments_by_section_ids_method_is_called:
        def test_given_no_parameters_passed_then_throw_assert_exception(
            self, default_request_client
        ):
            with pytest.raises(AssertionError):
                default_request_client.get_assignments_by_section_ids(None)

        def test_given_an_array_of_ids_then_make_a_call_per_item_in_array(
            self, default_request_client, requests_mock
        ):
            array_of_ids = ["1", "2", "3"]
            expected_url_1 = "https://api.schoology.com/v1/sections/1/assignments?start=0&limit=20"
            expected_url_2 = "https://api.schoology.com/v1/sections/2/assignments?start=0&limit=20"
            expected_url_3 = "https://api.schoology.com/v1/sections/3/assignments?start=0&limit=20"

            # Arrange
            text = '{"assignment": [{"a":"b"}]}'
            called = set()

            def callback(request, context):
                called.add(request.url)
                return text

            requests_mock.get(expected_url_1, reason="OK", status_code=200, text=callback)
            requests_mock.get(expected_url_2, reason="OK", status_code=200, text=callback)
            requests_mock.get(expected_url_3, reason="OK", status_code=200, text=callback)

            # Act
            response = default_request_client.get_assignments_by_section_ids(array_of_ids)

            # Assert
            assert len(called) == len(array_of_ids)
            assert expected_url_1 in called, "URL 1 not called"
            assert expected_url_2 in called, "URL 2 not called"
            assert expected_url_3 in called, "URL 3 not called"

            assert isinstance(response, list), "expected response to be a list"
            assert len(response) == 3, "expected three results"

        def test_given_an_empty_array_of_ids_then_do_not_make_any_calls(
            self, default_request_client
        ):
            # Act
            default_request_client.get_assignments_by_section_ids([])

            # If a request were made, then it would fail since the mock wasn't
            # setup.

    class Test_when_get_section_by_course_ids_method_is_called:
        def test_given_no_parameters_passed_then_throw_assert_exception(
            self, default_request_client
        ):
            with pytest.raises(AssertionError):
                default_request_client.get_section_by_course_ids(None)

        def test_given_a_parameter_is_passed_then_shoud_make_the_get_calls(
            self, default_request_client, requests_mock
        ):
            section_ids = [1, 2]
            expected_url_1 = "https://api.schoology.com/v1/courses/1/sections"
            expected_url_2 = "https://api.schoology.com/v1/courses/2/sections"

            # Arrange
            text = '{"section": [{"a":"b"}]}'
            called = set()

            def callback(request, context):
                called.add(request.url)
                return text

            requests_mock.get(expected_url_1, reason="OK", status_code=200, text=callback)
            requests_mock.get(expected_url_2, reason="OK", status_code=200, text=callback)

            # Act
            response = default_request_client.get_section_by_course_ids(section_ids)

            # Assert
            assert len(called) == len(section_ids)
            assert expected_url_1 in called, "URL 1 not called"
            assert expected_url_2 in called, "URL 2 not called"

            assert isinstance(response, list), "expected response to be a list"
            assert len(response) == 2, "expected three results"

    class Test_when_get_submissions_by_section_id_and_grade_item_id_method_is_called:
        def test_given_no_section_id_passed_then_throw_assert_exception(
            self, default_request_client
        ):
            with pytest.raises(AssertionError):
                default_request_client.get_submissions_by_section_id_and_grade_item_id(
                    None, "grade_item_id"
                )

        def test_given_no_grade_item_id_passed_then_throw_assert_exception(
            self, default_request_client
        ):
            with pytest.raises(AssertionError):
                default_request_client.get_submissions_by_section_id_and_grade_item_id(
                    "2", None
                )

        def test_given_a_parameter_is_passed_then_shoud_make_the_get_call(
            self, default_request_client, requests_mock
        ):
            expected_url_1 = "https://api.schoology.com/v1/sections/1/submissions/1234564"

            # Arrange
            text = '{"revision":[{"revision_id": 1,"uid": 100032890,"created": 1598631506,"num_items": 1,"late": 0,"draft": 0}]}'

            requests_mock.get(expected_url_1, reason="OK", status_code=200, text=text)

            # Act
            response = default_request_client.get_submissions_by_section_id_and_grade_item_id("1", "1234564")

            # Assert
            assert isinstance(response, PaginatedResult)
            assert len(response.current_page_items) == 1
            assert response.current_page_items[0]["uid"] == 100032890

    class Test_when_get_users_method_is_called:
        def test_given_the_get_call_returns_empty_response_then_return_empty_PaginatedResult(
            self, default_request_client, requests_mock
        ):
            expected_url_1 = "https://api.schoology.com/v1/users"

            # Arrange
            text = '{"user":[]}'

            requests_mock.get(expected_url_1, reason="OK", status_code=200, text=text)

            # Act
            response = default_request_client.get_users()

            # Assert
            assert isinstance(response, PaginatedResult)
            assert len(response.current_page_items) == 0

        def test_given_the_get_call_returns_users_then_return_list_of_users(
            self, default_request_client, requests_mock
        ):
            expected_url_1 = "https://api.schoology.com/v1/users"

            # Arrange
            text = '{"user":[{"uid": 100032890}]}'

            requests_mock.get(expected_url_1, reason="OK", status_code=200, text=text)

            # Act
            response = default_request_client.get_users()

            # Assert
            assert isinstance(response, PaginatedResult)
            assert len(response.current_page_items) == 1
            assert response.current_page_items[0]["uid"] == 100032890

    class Test_when_build_pagination_params_method_is_called:
        def test_given_wrong_type_in_params_then_thrown_assertion_error(
            self, default_request_client
        ):
            with pytest.raises(AssertionError):
                default_request_client._build_query_params_for_first_page([])

        def test_given_correct_parameter_then_url_is_built_correctly(
            self, default_request_client
        ):
            # Arrange
            items_per_page = 17
            expected_result = "start=0&limit=17"

            # Act
            result = default_request_client._build_query_params_for_first_page(
                items_per_page
            )

            # Assert
            assert result == expected_result

    class Test_when_get_grading_periods:
        def test_given_wrong_type_in_params_then_thrown_assertion_error(
            self, default_request_client
        ):
            with pytest.raises(AssertionError):
                default_request_client.get_grading_periods([])

        def test_given_correct_parameter_then_returns_expected_data(
            self, default_request_client, requests_mock
        ):
            expected_url_1 = "https://api.schoology.com/v1/gradingperiods"

            # Arrange
            text = '{"total":1,"gradingperiods":[{"id": 100032890}]}'

            requests_mock.get(expected_url_1, reason="OK", status_code=200, text=text)

            # Act
            response = default_request_client.get_grading_periods()

            # Assert
            assert isinstance(response, PaginatedResult)
            assert len(response.current_page_items) == 1
            assert response.current_page_items[0]["id"] == 100032890

    class Test_when_getting_all_courses:
        def test_given_wrong_type_in_params_then_thrown_assertion_error(
            self, default_request_client
        ):
            with pytest.raises(AssertionError):
                default_request_client.get_courses([])

        def test_given_correct_parameter_then_returns_expected_data(
            self, default_request_client, requests_mock
        ):
            expected_url_1 = "https://api.schoology.com/v1/courses"

            # Arrange
            text = '{"course":[{"id": 100032890, "title": "English I"}]}'

            requests_mock.get(expected_url_1, reason="OK", status_code=200, text=text)

            # Act
            response = default_request_client.get_courses()

            # Assert
            assert isinstance(response, PaginatedResult)
            assert len(response.current_page_items) == 1
            assert response.current_page_items[0]["id"] == 100032890
