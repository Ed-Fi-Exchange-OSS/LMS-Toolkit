# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


import pandas as pd
import pytest

from schoology_extractor.mapping.discussions import map_to_udm

FAKE_SECTION_ID = 1


class Test_mapping_schoology_discussions_to_udm:
    @classmethod
    def setup_class(cls):

        # Arrange
        responses_csv = '''id,uid,title,body,weight,graded,require_initial_post,published,available,completed,display_weight,folder_id,due,comments_closed,completion_status,links/self,CreateDate,LastModifiedDate
3277613289,99785803,Test discussion,,10,0,,1,1,0,2,0,2021-01-26 23:59:00,0,,https://api.schoology.com/v1/sections/2941242697/discussions/3277613289,12/8/2020 7:58,12/8/2020 7:58'''
        lines = responses_csv.split("\n")
        responses_df = pd.DataFrame(
            [x.split(",") for x in lines[1:]], columns=lines[0].split(",")
        )

        # Act
        cls.result = map_to_udm(responses_df, FAKE_SECTION_ID)

    # Each assertion is a separate method
    def test_then_output_has_one_row(self):
        assert self.result.shape[0] == 1

    @pytest.mark.parametrize(
        "input",
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "ActivityType",
            "ActivityDateTime",
            "ActivityStatus",
            "ParentSourceSystemIdentifier",
            "ActivityTimeInMinutes",
            "EntityStatus",
            "LMSUserIdentifier",
            "LMSSectionIdentifier"
        ],
    )
    def test_then_output_has_column(self, input):
        assert input in self.result.columns

    def test_then_source_system_identifier_is_mapped(self):
        assert self.result.at[0, "SourceSystemIdentifier"] == "sd#3277613289"

    def test_then_source_system_is_mapped(self):
        assert self.result.at[0, "SourceSystem"] == "Schoology"

    def test_then_user_identifier_is_mapped(self):
        assert self.result.at[0, "LMSUserIdentifier"] == "99785803"

    def test_then_section_identifier_is_mapped(self):
        assert self.result.at[0, "LMSSectionIdentifier"] == FAKE_SECTION_ID

    def test_then_entity_status_is_not_set(self):
        assert self.result.at[0, "EntityStatus"] == "active"

    def test_then_activity_date_time_is_mapped(self):
        assert self.result.at[0, "ActivityDateTime"] == "12/8/2020 7:58"

    def test_then_activity_type_is_mapped(self):
        assert self.result.at[0, "ActivityType"] == "Discussion"
