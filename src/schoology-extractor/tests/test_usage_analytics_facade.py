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


INPUT_DIRECTORY = './input'


def _setup_empty_filesystem(fs):
    fs.path_separator = "/"
    fs.is_windows_fs = False
    fs.is_macos = False
    fs.create_dir(INPUT_DIRECTORY)


def _setup_filesystem(fs):
    fs.path_separator = "/"
    fs.is_windows_fs = False
    fs.is_macos = False
    fs.create_dir(INPUT_DIRECTORY)
    contents = """role_name,user_building_id,user_building_name,username,email,schoology_user_id,unique_user_id,action_type,item_type,item_id,item_name,course_name,course_code,section_name,last_event_timestamp,event_count,role_id,user_building_code,last_name,first_name,device_type,item_building_id,item_building_name,item_building_code,item_parent_type,group_id,group_name,course_id,section_id,section_school_code,section_code,month,date,timestamp,time spent (seconds)
Student,2908525646,Ed-Fi Alliance - Grand Bend High school,kyle.hughes,kyle.hughes@studentgps.org,100032891,604874,CREATE,SESSION,,,,,,2020-11-04 17:28:43.097,1,796380,,Hughes,Kyle,WEB,2908525646,Ed-Fi Alliance - Grand Bend High school,,USER,,,,,,,11,11/04/2020,17:28,
"""
    fs.create_file(os.path.join(INPUT_DIRECTORY, "input.csv"), contents=contents)


def describe_when_getting_system_activities():
    def describe_given_no_usage_analytics_provided():
        @pytest.fixture
        def system(fs):
            _setup_empty_filesystem(fs)
            csv_reader.load_data_frame = Mock(return_value=pd.DataFrame(["one"]))
            db_engine = Mock(spec=sqlalchemy.engine.base.Engine)
            result = usage_analytics_facade.get_system_activities(INPUT_DIRECTORY, db_engine)

            return result

        def it_should_return_empty_data_frame(fs, system):
            assert system.empty

    def describe_given_usage_analytics():
        @pytest.fixture
        def given_usage_analytics(fs) -> Tuple[pd.DataFrame, Mock]:
            db_engine = Mock(spec=sqlalchemy.engine.base.Engine)

            _setup_filesystem(fs)
            csv_reader.load_data_frame = Mock(return_value=pd.DataFrame(["one"]))
            # Arrange
            usageMap.map_to_udm = Mock()
            usageMap.map_to_udm.return_value = pd.DataFrame([{"one": 1}])
            sync.usage_file_is_processed = Mock(return_value=False)
            sync.insert_usage_file_name = Mock()
            # Act
            result = usage_analytics_facade.get_system_activities(INPUT_DIRECTORY, db_engine)

            return result, usageMap.map_to_udm

        def it_should_map_the_usage_data_frame(given_usage_analytics: Tuple[pd.DataFrame, Mock]):
            _, mapper = given_usage_analytics

            assert mapper.called
