# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License,  Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime

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

    def it_should_have_correct_number_of_columns(result):
        assert result.shape[1] == 12

    def it_should_have_schoology_as_SourceSystem(result):
        assert result["SourceSystem"].iloc[0] == "Schoology"

    def it_should_map_id_to_SourceSystemIdentifier(result):
        assert result["SourceSystemIdentifier"].iloc[0] == "2942191527#2942251001#100032890"

    def it_should_map_uid_to_LMSUserSourceSystemIdentifier(result):
        assert result["LMSUserSourceSystemIdentifier"].iloc[0] == 100032890

    def it_should_map_created_to_SubmissionDateTime(result):
        # The Unix timestamp is converted based on timezone, so the answer below
        # depends on the test agent's time zone. Thus we can't hard-code a time.
        # This test is not as meaningful now that a conversion is being done in
        # both places - but at least the test is still validating that a date
        # _has been_ converted from the timestamp.
        expected = datetime.fromtimestamp(1604510984)
        actual = datetime.fromisoformat(result["SubmissionDateTime"].iloc[0])
        assert expected == actual

    def it_should_have_empty_SourceCreateDate(result):
        assert result["SourceCreateDate"].iloc[0] == ""

    def it_should_have_empty_SourceLastModifiedDate(result):
        assert result["SourceLastModifiedDate"].iloc[0] == ""
