# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


import re

import pandas as pd

from .table_helpers import read_keyvalue_pairs_as_dict, read_string_table_as_2d_list, read_string_table_as_dataframe


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


# Note that this gathers multiple tests results before the assert occurs,
# so that we can compare all expected columns at the same time
# without one failure causing the rest of the tests to be skipped.
def assert_dataframe_has_one_row_matching(table: str, actual: pd.DataFrame) -> None:
    assert actual.shape[0] > 0, "Unable to analyze because there are no rows"

    row = read_keyvalue_pairs_as_dict(table)

    errors = []
    for column, value in row.items():
        test = str(actual[column].iloc[0])

        if value.startswith("r"):
            # This is assumes a format of r"expression" thus leading to
            # re.compile("expression").
            r = re.compile(value[2:-1])
            if not r.match(test):
                errors.append(f"{column}: expected `{value}`, actual `{test}`")
        else:
            if test != value:
                errors.append(f"{column}: expected `{value}`, actual `{test}`")

    assert len(errors) == 0, "\n".join(errors)
