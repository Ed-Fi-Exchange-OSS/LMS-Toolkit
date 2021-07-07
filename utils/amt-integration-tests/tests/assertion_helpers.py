# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd


def _read_string_table_as_dataframe(table: str) -> pd.DataFrame:

    rows = table.strip().split("\n")
    column_names = [c.strip() for c in rows[0].split("|") if c != ""]

    c = [[v.strip() for v in r.split('|') if v != ""] for r in rows[1:]]

    return pd.DataFrame(c, columns=column_names, dtype="string")


def assert_dataframe_equals_table(table: str, actual: pd.DataFrame) -> None:

    expected = _read_string_table_as_dataframe(table)

    # Not concerned about data type for these tests, so just cast everything
    # to string to simplify the assertions
    actual = actual.astype("string")

    pd.testing.assert_frame_equal(expected, actual, check_dtype=False)
