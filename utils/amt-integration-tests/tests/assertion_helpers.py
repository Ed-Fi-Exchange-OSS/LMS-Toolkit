# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


import pandas as pd


from .table_helpers import read_string_table_as_2d_list, read_string_table_as_dataframe


def assert_dataframe_equals_table(table: str, actual: pd.DataFrame) -> None:

    expected = read_string_table_as_dataframe(table)

    # Not concerned about data type for these tests, so just cast everything
    # to string to simplify the assertions
    actual = actual.astype("string")

    pd.testing.assert_frame_equal(expected, actual)


def assert_dataframe_has_columns(columns: str, actual: pd.DataFrame) -> None:

    _, data = read_string_table_as_2d_list(columns)

    e = sorted([d[0] for d in data])
    a = sorted(list(actual.columns))

    msg = f"Expected: {e}\nActual: {a}"

    assert e == a, msg
