# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


import pandas as pd
import pytest

from schoology_extractor.mapping.discussion_replies import map_to_udm

FAKE_SECTION_ID = 1


class Test_mapping_schoology_users_to_udm:
    @classmethod
    def setup_class(cls):

        # Arrange
        responses_csv = '''id,uid,comment,created,parent_id,status,likes,user_like_action,links,CreateDate,LastModifiedDate
824849694,100032890,Mary Archer's response to ""First Algebra Discussion Topic."",1604351930,0,1,0,False,{'self': 'https://api.schoology.com/v1/sections/2942191527/discussions/3278946222/comments/824849694'},2020-11-12 10:39:27,2020-11-12 10:39:27
824853919,100032891,Kyle Hughes's reply to Mary Archer's response to ""First Algebra Discussion Topic."",1604352056,824849694,1,0,False,{'self': 'https://api.schoology.com/v1/sections/2942191527/discussions/3278946222/comments/824853919'},2020-11-12 10:39:27,2020-11-12 10:39:27'''
        lines = responses_csv.split("\n")
        responses_df = pd.DataFrame(
            [x.split(",") for x in lines[1:]], columns=lines[0].split(",")
        )

        # Act
        cls.result = map_to_udm(responses_df, FAKE_SECTION_ID)

    # Each assertion is a separate method
    def test_then_output_has_two_rows(self):
        assert self.result.shape[0] == 2

    @pytest.mark.parametrize(
        "input",
        [
            "SourceSystemIdentifier",
            "SourceSystem",
            "LMSUserIdentifier",
            "LMSSectionIdentifier",
            "EntityStatus",
            "ActivityDateTime",
            "ActivityStatus",
            "ActivityType",
            "Content",
            "AssignmentIdentifier",
            "ActivityTimeInMinutes",
            "CreateDate",
            "LastModifiedDate",
        ],
    )
    def test_then_output_has_column(self, input):
        assert input in self.result.columns

    def test_then_source_system_identifier_is_mapped(self):
        assert self.result.at[0, "SourceSystemIdentifier"] == "824849694"

    def test_then_source_system_is_mapped(self):
        assert self.result.at[0, "SourceSystem"] == "Schoology"

    def test_then_user_identifier_is_mapped(self):
        assert self.result.at[0, "LMSUserIdentifier"] == "100032890"

    def test_then_section_identifier_is_mapped(self):
        assert self.result.at[0, "LMSSectionIdentifier"] == FAKE_SECTION_ID

    def test_then_entity_status_is_not_set(self):
        assert self.result.at[0, "EntityStatus"] == "active"

    def test_then_activity_date_time_is_mapped(self):
        assert self.result.at[0, "ActivityDateTime"] == "2020-11-02 15:18:50"

    def test_then_activity_status_is_mapped(self):
        assert self.result.at[0, "ActivityStatus"] == "active"

    def test_then_activity_type_is_mapped(self):
        assert self.result.at[0, "ActivityType"] == "Discussion Reply"

    def test_then_content_is_mapped(self):
        assert self.result.at[0, "Content"] == '''Mary Archer's response to ""First Algebra Discussion Topic.""'''
