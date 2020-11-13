# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Tuple

import pandas as pd
import pytest
from unittest.mock import Mock

from schoology_extractor.usage_analytics_facade import get_system_activities
from schoology_extractor.mapping import usage_analytics as usageMap
# Will need this soon
# from schoology_extractor.helpers.csv_reader import load_data_frame


def describe_when_getting_system_activities():
    def describe_given_no_usage_analytics_provided():
        def it_should_return_empty_data_frame():
            result = get_system_activities(pd.DataFrame())

            assert result.empty

    def describe_given_usage_analytics():
        @pytest.fixture
        def system() -> Tuple[pd.DataFrame, Mock]:

            # Arrange
            usageMap.map_to_udm = Mock()
            usageMap.map_to_udm.return_value = pd.DataFrame([{"one": 1}])

            usage = pd.DataFrame([{"two": 2}])

            # Act
            result = get_system_activities(usage)

            return result, usageMap.map_to_udm

        def it_should_return_the_mapped_data_frame(system):
            df, _ = system
            assert df.iloc[0]["one"] == 1

        def it_should_map_the_usage_data_frame(system):
            _, mapper = system

            input = mapper.call_args[0][0]
            assert input.iloc[0]["two"] == 2
