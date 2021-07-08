# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os

import pandas as pd
from sqlalchemy import engine, text

DESCRIPTOR_SQL = """
INSERT INTO edfi.Descriptor (CodeValue, ShortDescription, Description, Namespace)
    VALUES ('<cv>', '<sd>', '<d>', '<n>');
DECLARE @id int = @@identity;
INSERT INTO <schema>.<tbl> (<tbl>Id) VALUES (@id);
"""

SCHEMA_LMSX = "lmsx"
SCHEMA_EDFI = "edfi"


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


def _read_and_load_descriptors(
    engine: engine.base.Engine, descriptor_type: str
) -> None:
    descriptor = f"{descriptor_type}Descriptor"

    file_path = os.path.join(
        "..", "..", "extension", "Descriptors", f"{descriptor}.xml"
    )
    df = pd.read_xml(file_path)

    with engine.connect() as connection:
        for _, row in df.iterrows():
            sql = _prepare_descriptor_sql(row, SCHEMA_LMSX, descriptor)
            connection.execute(text(sql))


def load_lms_descriptors(engine: engine.base.Engine) -> None:
    _read_and_load_descriptors(engine, "AssignmentCategory")
    _read_and_load_descriptors(engine, "LMSSourceSystem")
    _read_and_load_descriptors(engine, "SubmissionStatus")
    _read_and_load_descriptors(engine, "SubmissionType")


APPEND_OPTIONS = {"if_exists": "append", "index": False}


def load_school(engine: engine.base.Engine, id: str) -> None:
    ed_org = pd.DataFrame([{"EducationOrganizationId": id, "NameOfInstitution": id}])
    ed_org.to_sql("EducationOrganization", engine, schema="edfi", **APPEND_OPTIONS)

    school = pd.DataFrame([{"schoolid": id}])
    school.to_sql("School", engine, schema="edfi", **APPEND_OPTIONS)


def load_school_year(engine: engine.base.Engine, school_year: str) -> None:
    school_year_type = pd.DataFrame(
        [
            {
                "SchoolYear": school_year,
                "SchoolYearDescription": school_year,
                "CurrentSchoolYear": True,
            }
        ]
    )
    school_year_type = school_year_type.astype({"SchoolYear": int})
    school_year_type.to_sql("SchoolYearType", engine, schema="edfi", **APPEND_OPTIONS)


def load_session(
    engine: engine.base.Engine, school_id: str, session_name: str, school_year: str
) -> None:

    # We need to have a term descriptor before we can insert a school year
    term_code_value = f"TERM:{session_name}"
    row = pd.Series(
        {
            "CodeValue": term_code_value,
            "ShortDescription": session_name,
            "Description": session_name,
            "Namespace": "uri://ed-fi.org/Term",
        }
    )

    term_descriptor_sql = _prepare_descriptor_sql(row, SCHEMA_EDFI, "TermDescriptor")
    descriptor_id = 0

    with engine.connect() as connection:
        connection.execute(text(term_descriptor_sql))

        sql = text(
            f"SELECT DescriptorId FROM edfi.Descriptor WHERE CodeValue = '{term_code_value}'"
        )
        result = connection.execute(sql, engine)
        for row in result:
            descriptor_id = row["DescriptorId"]

    session = pd.DataFrame(
        [
            {
                "SchoolId": school_id,
                "SchoolYear": school_year,
                "SessionName": session_name,
                "BeginDate": "2021-01-01",
                "EndDate": "2021-08-03",
                "TermDescriptorId": descriptor_id,
                "TotalInstructionalDays": 1,
            }
        ]
    )

    session.to_sql("Session", engine, schema=SCHEMA_EDFI, **APPEND_OPTIONS)
