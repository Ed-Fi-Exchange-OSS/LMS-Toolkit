# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from unittest.mock import patch, Mock
from google_classroom_extractor.api.teachers import request_latest_teachers_as_df


def describe_when_requesting_latest_teachers():
    @patch("google_classroom_extractor.api.teachers.call_api")
    def it_should_use_teachers_list_resource(mock_call_api):
        # arrange
        resource = Mock()
        # act
        request_latest_teachers_as_df(resource, [""])
        # assert
        assert isinstance(resource.courses.return_value.teachers.return_value.list, Mock)
