# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest

from edfi_canvas_extractor.mapping.helpers import convert_to_standard_date_time_string


def describe_when_converting_datetime_to_standard_format() -> None:
    @pytest.mark.parametrize("input, expected", [
        ("2013-01-01T00:00:00-06:00", "2013-01-01 06:00:00"),
        ("2021-01-20T21:12:16Z", "2021-01-20 21:12:16"),
        ("I'm not a date", ""),
        ("", "")
    ])
    def it_converts_the_string(input: str, expected: str) -> None:
        df = pd.DataFrame([{"d": input}])

        convert_to_standard_date_time_string(df, "d")

        assert df["d"].iloc[0] == expected
