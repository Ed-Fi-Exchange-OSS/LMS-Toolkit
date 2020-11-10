# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License,  Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest

from schoology_extractor.mapping.submissions import map_to_udm


def describe_when_mapping_empty_DataFrame():
    def it_should_return_empty_DataFrame():
        df = map_to_udm(pd.DataFrame())
        assert (df == pd.DataFrame()).all().all()


def describe_when_mapping_Schoology_DataFrame_to_EdFi_DataFrame():
    @pytest.fixture
    def result() -> pd.DataFrame:

        submission = {
            "id": "2942191527#2942251001#100032890",
            "revision_id": 1,
            "uid": 100032890,
            "created": 1604510984,
            "num_items": 1,
            "late": 0,
            "draft": 0,
            "CreateDate": "2020-11-04 09:46:45",
            "LastModifiedDate": "2020-11-04 09:46:45",
        }

        # Arrange
        schoology_df = pd.DataFrame([submission])

        # Act
        return map_to_udm(schoology_df)

    def it_should_have_schoology_as_SourceSystem(result):
        assert result["SourceSystem"].iloc[0] == "Schoology"

    def it_should_map_id_to_SourceSystemIdentifier(result):
        assert result["SourceSystemIdentifier"].iloc[0] == "2942191527#2942251001#100032890"

    def it_should_map_uid_to_LMSUserSourceSystemIdentifier(result):
        assert result["LMSUserSourceSystemIdentifier"].iloc[0] == 100032890

    def it_should_map_created_to_SubmissionDateTime(result):
        assert result["SubmissionDateTime"].iloc[0] == "2020-11-04 11:29:44"
