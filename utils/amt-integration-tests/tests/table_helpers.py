# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Dict, List, Tuple

import pandas as pd


def read_string_table_as_2d_list(table: str) -> Tuple[List[str], List[List[str]]]:
    rows = table.strip().split("\n")
    column_names = [c.strip() for c in rows[0].split("|") if c != ""]
    data = [[v.strip() for v in r.split('|') if v != ""] for r in rows[1:]]

    return column_names, data


def read_string_table_as_dataframe(table: str) -> pd.DataFrame:

    column_names, data = read_string_table_as_2d_list(table)

    return pd.DataFrame(data, columns=column_names, dtype="string")


def read_keyvalue_pairs_as_dict(kv_pairs: str) -> Dict[str, str]:
    _, data = read_string_table_as_2d_list(kv_pairs)

    kv_d: Dict[str, str] = {}

    for kv in data:
        kv_d[kv[0]] = kv[1]

    return kv_d
