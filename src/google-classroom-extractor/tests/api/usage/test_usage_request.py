# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from unittest.mock import patch, Mock
from google_classroom_extractor.api.usage import request_latest_usage_as_df
from datetime import datetime


def describe_when_requesting_latest_usage():
    @patch("google_classroom_extractor.api.usage.call_api")
    def it_should_use_user_usage_get_resource(mock_call_api):
        # arrange
        resource = Mock()
        now = datetime.now()
        # act
        request_latest_usage_as_df(resource, now, now)
        # assert
        assert isinstance(resource.userUsageReport.return_value.get, Mock)
