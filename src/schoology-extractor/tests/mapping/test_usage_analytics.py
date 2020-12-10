# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest
from freezegun import freeze_time

from schoology_extractor.mapping.usage_analytics import map_to_udm

DATE_TIME_INPUT_STRING = "2020-10-16 1:00:01 PM"
EXPECTED_DATE_TIME = "2020-10-16 13:00:01"


def describe_when_converting_usage_analytics_to_udm():
    def describe_given_item_type_assignment_then_ignore_the_record():
        # Arrange
        df = pd.DataFrame(
            [{
                "action_type": "CREATE",
                "item_type": "ASSIGNMENT",
                "schoology_user_id": "100032891",
                "unique_user_id": 604874,
                "last_event_timestamp": "2020-11-04 17:28:43.097"
            }]
        )

        # Act
        result = map_to_udm(df)

        # Assert
        assert result.empty

    def describe_given_item_type_discussion_then_ignore_the_record():
        # Arrange
        df = pd.DataFrame(
            [{
                "action_type": "CREATE",
                "item_type": "DISCUSSION",
                "schoology_user_id": "100032891",
                "unique_user_id": 604874,
                "last_event_timestamp": "2020-11-04 17:28:43.097"
            }]
        )

        # Act
        result = map_to_udm(df)

        # Assert
        assert result.empty

    def describe_given_item_type_session():
        def describe_given_action_type_update():
            def it_should_ignore_the_record():
                # Arrange
                df = pd.DataFrame(
                    [{
                        "action_type": "UPDATE",
                        "item_type": "SESSION",
                        "schoology_user_id": "100032891",
                        "unique_user_id": 604874,
                        "last_event_timestamp": "2020-11-04 17:28:43.097"
                    }]
                )

                # Act
                result = map_to_udm(df)

                # Assert
                assert result.empty

        def describe_given_action_type_create():
            @pytest.fixture
            @freeze_time(DATE_TIME_INPUT_STRING)
            def result() -> pd.DataFrame:
                # Arrange
                df = pd.DataFrame(
                    [{
                        "action_type": "CREATE",
                        "item_type": "SESSION",
                        "schoology_user_id": "100032891",
                        "unique_user_id": 604874,
                        "last_event_timestamp": "2020-11-04 17:28:43.097"
                    }]
                )

                # Act
                return map_to_udm(df)

            def it_should_have_correct_number_of_columns(result):
                assert result.shape[1] == 13

            def it_should_have_one_row(result):
                assert result.shape[0] == 1

            @pytest.mark.parametrize(
                "field,expected", [
                    ("SourceSystemIdentifier", "in#100032891#1604510923.097"),
                    ("SourceSystem", "Schoology"),
                    ("LMSUserSourceSystemIdentifier", 100032891),
                    ("ActivityType", "sign-in"),
                    ("ActivityDateTime", "2020-11-04 17:28:43.097"),
                    ("ActivityStatus", "active"),
                    ("ParentSourceSystemIdentifier", None),
                    ("ActivityTimeInMinutes", None),
                    ("EntityStatus", "active"),
                    ("CreateDate", EXPECTED_DATE_TIME),
                    ("LastModifiedDate", EXPECTED_DATE_TIME),
                    ("SourceCreateDate", ""),
                    ("SourceLastModifiedDate", ""),
                ]
            )
            def it_should_map_fields(result, field, expected):
                assert result.iloc[0][field] == expected

        def describe_given_action_type_delete():
            @pytest.fixture
            @freeze_time(DATE_TIME_INPUT_STRING)
            def result() -> pd.DataFrame:
                # Arrange
                df = pd.DataFrame(
                    [{
                        "action_type": "DELETE",
                        "item_type": "SESSION",
                        "schoology_user_id": "100032891",
                        "unique_user_id": 604874,
                        "last_event_timestamp": "2020-11-04 17:28:43.097"
                    }]
                )

                # Act
                return map_to_udm(df)

            def it_should_have_correct_number_of_columns(result):
                assert result.shape[1] == 13

            def it_should_have_one_row(result):
                assert result.shape[0] == 1

            @pytest.mark.parametrize(
                "field,expected", [
                    ("SourceSystemIdentifier", "out#100032891#1604510923.097"),
                    ("SourceSystem", "Schoology"),
                    ("LMSUserSourceSystemIdentifier", 100032891),
                    ("ActivityType", "sign-out"),
                    ("ActivityDateTime", "2020-11-04 17:28:43.097"),
                    ("ActivityStatus", "active"),
                    ("ParentSourceSystemIdentifier", None),
                    ("ActivityTimeInMinutes", None),
                    ("EntityStatus", "active"),
                    ("CreateDate", EXPECTED_DATE_TIME),
                    ("LastModifiedDate", EXPECTED_DATE_TIME),
                    ("SourceCreateDate", ""),
                    ("SourceLastModifiedDate", ""),
                ]
            )
            def it_should_map_fields(result, field, expected):
                assert result.iloc[0][field] == expected
