# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import os

import pandas as pd
from sqlalchemy import engine, text

from .table_helpers import read_keyvalue_pairs_as_dataframe


DESCRIPTOR_SQL = """
INSERT INTO edfi.Descriptor (CodeValue, ShortDescription, Description, Namespace)
    VALUES ('<cv>', '<sd>', '<d>', '<n>');
DECLARE @id int = @@identity;
INSERT INTO <schema>.<tbl> (<tbl>Id) VALUES (@id);
"""

SCHEMA_LMSX = "lmsx"
SCHEMA_EDFI = "edfi"
APPEND_OPTIONS = {"if_exists": "append", "index": False}

# This static variable helps us keep track of what has already been uploaded so
# that we can avoid re-uploading, and thus encountering a duplicate key error.
already_loaded = {}


def _get_value(row: pd.Series, column: str) -> str:
    # Escape any apostrophes so that this is safe to run
    return row[column].replace("'", "''")


def _get_edfi_options(engine: engine.base.Engine) -> dict:
    return {"con": engine, "schema": SCHEMA_EDFI, **APPEND_OPTIONS}


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
    df = pd.read_xml(file_path)  # type: ignore

    with engine.connect() as connection:
        for _, row in df.iterrows():
            sql = _prepare_descriptor_sql(row, SCHEMA_LMSX, descriptor)
            connection.execute(text(sql))


def load_lms_descriptors(engine: engine.base.Engine) -> None:
    _read_and_load_descriptors(engine, "AssignmentCategory")
    _read_and_load_descriptors(engine, "LMSSourceSystem")
    _read_and_load_descriptors(engine, "SubmissionStatus")
    _read_and_load_descriptors(engine, "SubmissionType")


def load_school(engine: engine.base.Engine, id: str) -> None:
    SCHOOLID = "SchoolId"

    if SCHOOLID not in already_loaded.keys():
        already_loaded[SCHOOLID] = []

    if id in already_loaded[SCHOOLID]:
        # This school has already been loaded, no more action required
        return

    ed_org = pd.DataFrame([{"EducationOrganizationId": id, "NameOfInstitution": id}])
    ed_org.to_sql("EducationOrganization", **_get_edfi_options(engine))

    school = pd.DataFrame([{SCHOOLID: id}])
    school.to_sql("School", **_get_edfi_options(engine))

    already_loaded[SCHOOLID].append(id)


def load_school_year(engine: engine.base.Engine, school_year: str) -> None:
    SCHOOLYEAR = "SchoolYear"

    if SCHOOLYEAR not in already_loaded.keys():
        already_loaded[SCHOOLYEAR] = []

    if school_year in already_loaded[SCHOOLYEAR]:
        # This school has already been loaded, no more action required
        return

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
    school_year_type.to_sql("SchoolYearType", **_get_edfi_options(engine))

    already_loaded[SCHOOLYEAR].append(school_year)


counter = {"here": 0}


def load_session(
    engine: engine.base.Engine, school_id: str, session_name: str, school_year: str
) -> None:
    SESSION = "Session"

    if SESSION not in already_loaded.keys():
        already_loaded[SESSION] = []

    if session_name in already_loaded[SESSION]:
        # This school has already been loaded, no more action required
        return

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

    session.to_sql("Session", **_get_edfi_options(engine))

    already_loaded[SESSION].append(session_name)


def load_section(engine: engine.base.Engine, section_table: str) -> None:
    section_df = read_keyvalue_pairs_as_dataframe(section_table)

    SECTION = "Section"
    section_identifier = section_df["SectionIdentifier"].iloc[0]

    if SECTION not in already_loaded.keys():
        already_loaded[SECTION] = []

    if section_identifier in already_loaded[SECTION]:
        # This school has already been loaded, no more action required
        return

    # Before we can have a section, we must have a Course and then a Course
    # Offering.
    course_df = section_df[["LocalCourseCode", "SchoolId"]].copy()
    course_df.rename(
        columns={
            "LocalCourseCode": "CourseCode",
            "SchoolId": "EducationOrganizationId",
        },
        inplace=True,
    )

    course_df["CourseTitle"] = course_df["CourseCode"]
    course_df["NumberOfParts"] = 1
    course_df.to_sql("Course", **_get_edfi_options(engine))

    offering_df = section_df[
        ["LocalCourseCode", "SchoolId", "SchoolYear", "SessionName"]
    ].copy()
    offering_df["CourseCode"] = offering_df["LocalCourseCode"]
    offering_df["EducationOrganizationId"] = offering_df["SchoolId"]
    offering_df.to_sql("CourseOffering", **_get_edfi_options(engine))

    section_df.to_sql("Section", **_get_edfi_options(engine))

    already_loaded[SECTION].append(section_identifier)


def load_grading_period(engine: engine.base.Engine, grading_period_table: str) -> None:
    GRADING_PERIOD_DESCRIPTOR_KEY = "Grading Period Descriptor"
    GRADING_PERIOD_KEY = "Grading Period"
    grading_periods_df = read_keyvalue_pairs_as_dataframe(grading_period_table)
    grading_period_descriptor = grading_periods_df["Descriptor"].iloc[0]
    descriptor_id = 0

    if GRADING_PERIOD_DESCRIPTOR_KEY not in already_loaded.keys():
        already_loaded[GRADING_PERIOD_DESCRIPTOR_KEY] = []

    if grading_period_descriptor not in already_loaded[GRADING_PERIOD_DESCRIPTOR_KEY]:
        descriptor = pd.Series(
            {
                "CodeValue": grading_period_descriptor,
                "ShortDescription": grading_period_descriptor,
                "Description": grading_period_descriptor,
                "Namespace": "uri://ed-fi.org/Descriptor",
            }
        )
        descriptor_sql = _prepare_descriptor_sql(
            descriptor, SCHEMA_EDFI, "TermDescriptor"
        )

        with engine.connect() as connection:
            connection.execute(text(descriptor_sql))

        already_loaded[GRADING_PERIOD_DESCRIPTOR_KEY].append(grading_period_descriptor)

    with engine.connect() as connection:
        sql = text(
            f"SELECT DescriptorId FROM edfi.Descriptor WHERE CodeValue = '{grading_period_descriptor}'"
        )
        result = connection.execute(sql, engine)
        for row in result:
            descriptor_id = row["DescriptorId"]

        sql = text(
            f"""SELECT GradingPeriodDescriptorId FROM edfi.GradingPeriodDescriptor
            WHERE GradingPeriodDescriptorId = {descriptor_id}"""
        )

        result = connection.execute(sql, engine)
        grading_period_descriptor_id = 0
        for row in result:
            grading_period_descriptor_id = row["GradingPeriodDescriptorId"]

        if grading_period_descriptor_id == 0:
            connection.execute(
                f"""
            INSERT INTO edfi.[GradingPeriodDescriptor]([GradingPeriodDescriptorId])
            VALUES ({descriptor_id})
            """
            )

    if GRADING_PERIOD_KEY not in already_loaded.keys():
        already_loaded[GRADING_PERIOD_KEY] = []

        grading_periods_df.rename(columns={"Descriptor": "GradingPeriodDescriptorId"}, inplace=True)
        grading_periods_df["GradingPeriodDescriptorId"] = descriptor_id

        grading_periods_df.to_sql("GradingPeriod", **_get_edfi_options(engine))
