# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
import os

import pandas as pd
from edfi_sql_adapter import sql_adapter

DESCRIPTOR_SQL = """
SELECT FROM edfi.Descriptor TOP 1 'exists'
    WHERE  CodeValue='<cv>', ShortDescription='<sd>', Description='<d>', Namespace='<n>');
"""


def _get_value(row: pd.Series, column: str) -> str:
    # Escape any apostrophes so that this is safe to run
    return row[column].replace("'", "''")


def _prepare_descriptor_sql(row: pd.Series, schema: str, table: str) -> str:
    return (
        DESCRIPTOR_SQL.replace("<cv>", _get_value(row, "CodeValue"))
        .replace("<sd>", _get_value(row, "ShortDescription"))
        .replace("<d>", _get_value(row, "Description"))
        .replace("<n>", _get_value(row, "Namespace"))
        .replace("<tbl>", table)
        .replace("<schema>", schema)
    )


def _get_descriptors_df(descriptor_name: str) -> pd.DataFrame:
    file_path = os.path.join(
        "..", "..", "extension", "Descriptors", f"{descriptor_name}.xml"
    )
    return pd.read_xml(file_path)  # type: ignore


def _read_and_validate_descriptor(
    engine: sql_adapter, descriptor_type: str, missing_descriptors: list[str]
) -> None:
    descriptor = f"{descriptor_type}Descriptor"
    df = _get_descriptors_df(descriptor)

    for _, row in df.iterrows():
        print(row)


def validate_lms_descriptors(adapter: sql_adapter) -> list[str]:
    missing_descriptors = list[str]()
    _read_and_validate_descriptor(adapter, "AssignmentCategory", missing_descriptors)
    _read_and_validate_descriptor(adapter, "LMSSourceSystem", missing_descriptors)
    _read_and_validate_descriptor(adapter, "SubmissionStatus", missing_descriptors)
    _read_and_validate_descriptor(adapter, "SubmissionType", missing_descriptors)

    return missing_descriptors
