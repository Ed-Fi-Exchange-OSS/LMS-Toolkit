# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import List
from canvasapi.canvas import Canvas
from pandas import DataFrame
from canvas_extractor.api.resource_sync import (
    add_hash_and_json_to,
    add_sourceid_to,
)

MOCK_CANVAS_BASE_URL = "https://example.com"
MOCK_CANVAS_ACCESS_TOKEN = "1234567890"


def prep_expected_sync_df(df: DataFrame, identity_columns: List[str]) -> DataFrame:
    result_df: DataFrame = add_hash_and_json_to(df)
    add_sourceid_to(result_df, identity_columns)
    result_df = result_df[["Json", "Hash", "SourceId"]]
    result_df.set_index("SourceId", inplace=True)
    return result_df


def prep_from_sync_db_df(df: DataFrame, identity_columns: List[str]) -> DataFrame:
    result_df: DataFrame = df[["Json", "Hash", "SourceId"]]
    result_df.set_index("SourceId", inplace=True)
    return result_df


def setup_fake_canvas_object() -> Canvas:
    return Canvas(MOCK_CANVAS_BASE_URL, MOCK_CANVAS_ACCESS_TOKEN)
