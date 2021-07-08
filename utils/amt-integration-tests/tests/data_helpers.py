# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os

import pandas as pd
from sqlalchemy import engine

DESCRIPTOR_SQL = """
INSERT INTO edfi.Descriptor (CodeValue, ShortDescription, Description, Namespace)
VALUES ('<cv>', '<sd>', '<d>', '<n>');
INSERT INTO lmsx.<tbl> (<tbl>Id)
VALUES (@@identity);
"""

def _get_value(row: pd.Series, column: str) -> str:
    # Escape any apostrophes so that this is safe to run
    return row[column].replace("'", "''")


def _prepare_template(row: pd.Series, table: str) -> str:
    return (
        DESCRIPTOR_SQL.replace("<cv>", _get_value(row, "CodeValue"))
                      .replace("<sd>", _get_value(row, "ShortDescription"))
                      .replace("<d>", _get_value(row, "Description"))
                      .replace("<n>", _get_value(row, "Namespace"))
                      .replace("<tbl>", table)
    )


def _read_and_load_descriptors(engine: engine.base.Engine, descriptor_type: str) -> None:
    descriptor = f"{descriptor_type}Descriptor"

    file_path = os.path.join("..", "..", "extension", "Descriptors", f"{descriptor}.xml")
    df = pd.read_xml(file_path)

    with engine.connect() as connection:
        for _, row in df.iterrows():
            sql = _prepare_template(row, descriptor)
            connection.execute(sql)


def load_lms_descriptors(engine: engine.base.Engine) -> None:
    _read_and_load_descriptors(engine, "AssignmentCategory")
    _read_and_load_descriptors(engine, "LMSSourceSystem")
    _read_and_load_descriptors(engine, "SubmissionStatus")
    _read_and_load_descriptors(engine, "SubmissionType")
