# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os
from typing import Tuple

import pandas as pd
import pytest
from unittest.mock import Mock

import sqlalchemy

from schoology_extractor import usage_analytics_facade
from schoology_extractor.mapping import usage_analytics as usageMap
from schoology_extractor.helpers import csv_reader
from schoology_extractor.helpers import sync


def describe_when_getting_system_activities():
    def describe_given_no_usage_analytics_provided():
        def _mock_packages():
            os.scandir = Mock(return_value=[])
            csv_reader.load_data_frame = Mock(return_value=pd.DataFrame(["one"]))

        def it_should_return_empty_data_frame():
            _mock_packages()
            db_engine = Mock(spec=sqlalchemy.engine.base.Engine)
            result = usage_analytics_facade.get_system_activities('.', db_engine)
            assert result.empty

    def describe_given_usage_analytics():
        @pytest.fixture
        def system() -> Tuple[pd.DataFrame, Mock]:
            db_engine = Mock(spec=sqlalchemy.engine.base.Engine)

            mock_file_one = Mock()
            mock_file_one.name = "fake_name"
            mock_file_one.path = "fake_path"

            mock_file_two = Mock()
            mock_file_two.name = "fake_name"
            mock_file_two.path = "fake_path"

            fake_files = [mock_file_one, mock_file_two]

            os.scandir = Mock(return_value=fake_files)
            csv_reader.load_data_frame = Mock(return_value=pd.DataFrame(["one"]))
            # Arrange
            usageMap.map_to_udm = Mock()
            usageMap.map_to_udm.return_value = pd.DataFrame([{"one": 1}])
            sync.usage_file_is_processed = Mock(return_value=False)
            sync.insert_usage_file_name = Mock()

            # Act
            result = usage_analytics_facade.get_system_activities("fake_path", db_engine)

            return result, usageMap.map_to_udm

        def it_should_return_the_mapped_data_frame(system: Tuple[pd.DataFrame, Mock]):
            df, _ = system
            assert df.iloc[0]["one"] == 1

        def it_should_map_the_usage_data_frame(system: Tuple[pd.DataFrame, Mock]):
            _, mapper = system

            assert mapper.called
