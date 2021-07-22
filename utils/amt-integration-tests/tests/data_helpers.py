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

# If it was a production script we would probably want to add a WHERE clause for not inserting duplicated
# records, for testing purposes we can assume this table is not populated when running the script.
POPULATE_SESSION_GRADING_PERIOD_SQL = """
INSERT INTO edfi.SessionGradingPeriod
    (GradingPeriodDescriptorId, PeriodSequence, SchoolId, SchoolYear, SessionName)
SELECT
    gradingperiod.GradingPeriodDescriptorId,
    gradingperiod.PeriodSequence,
    gradingperiod.SchoolId,
    gradingperiod.SchoolYear,
    SessionName
FROM edfi.Session session
INNER JOIN edfi.GradingPeriod gradingperiod
    ON session.SchoolYear = gradingperiod.SchoolYear
    AND gradingperiod.SchoolId = session.SchoolId
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


def _get_lmsx_options(engine: engine.base.Engine) -> dict:
    return {"con": engine, "schema": SCHEMA_LMSX, **APPEND_OPTIONS}


def __get_descriptor_id(
    engine: engine.base.Engine, codevalue: str = None, namespace: str = None
) -> int:
    assert (
        codevalue is not None or namespace is not None
    ), "At least one of the parameters(codevalue or namespace) must not be none"

    descriptor_id = 0
    with engine.connect() as connection:
        sql = text(
            f"""
                SELECT TOP 1 DescriptorId FROM edfi.Descriptor
                WHERE
                {f"CodeValue = '{codevalue}'" if codevalue is not None else "" }
                {"and" if codevalue is not None and namespace is not None else ""}
                {f"namespace = '{namespace}'" if namespace is not None else "" }
            """
        )
        result = connection.execute(sql, engine)
        for row in result:
            descriptor_id = row["DescriptorId"]

    return descriptor_id


def _get_descriptor_id_by_codevalue_and_namespace(
    engine: engine.base.Engine, codevalue: str, namespace: str
) -> int:
    return __get_descriptor_id(engine, codevalue, namespace)


def _get_descriptor_id_by_codevalue(engine: engine.base.Engine, codevalue: str) -> int:
    return __get_descriptor_id(engine, codevalue)


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
    SCHOOL_ID = "SchoolId"

    if SCHOOL_ID not in already_loaded.keys():
        already_loaded[SCHOOL_ID] = []

    if id in already_loaded[SCHOOL_ID]:
        # This school has already been loaded, no more action required
        return

    ed_org = pd.DataFrame([{"EducationOrganizationId": id, "NameOfInstitution": id}])
    ed_org.to_sql("EducationOrganization", **_get_edfi_options(engine))

    school = pd.DataFrame([{SCHOOL_ID: id}])
    school.to_sql("School", **_get_edfi_options(engine))

    already_loaded[SCHOOL_ID].append(id)


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


def load_session(
    engine: engine.base.Engine, school_id: str, session_name: str, school_year: str
) -> None:
    SESSION = "Session"
    DESCRIPTOR_NAMESPACE = "uri://ed-fi.org/Term"

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
            "Namespace": DESCRIPTOR_NAMESPACE,
        }
    )

    term_descriptor_sql = _prepare_descriptor_sql(row, SCHEMA_EDFI, "TermDescriptor")

    with engine.connect() as connection:
        connection.execute(text(term_descriptor_sql))

    descriptor_id = _get_descriptor_id_by_codevalue_and_namespace(
        engine, term_code_value, DESCRIPTOR_NAMESPACE
    )

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
    GRADING_PERIOD_KEY = "Grading Period"
    GRADING_PERIOD_DESCRIPTOR_KEY = "Grading Period Descriptor"
    DESCRIPTOR_NAMESPACE = "uri://ed-fi.org/Descriptor"

    grading_periods_df = read_keyvalue_pairs_as_dataframe(grading_period_table)
    grading_period_descriptor = str(grading_periods_df["Descriptor"].iloc[0])

    # Add descriptor for grading period
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
            descriptor, SCHEMA_EDFI, "GradingPeriodDescriptor"
        )

        with engine.connect() as connection:
            connection.execute(text(descriptor_sql))

        already_loaded[GRADING_PERIOD_DESCRIPTOR_KEY].append(grading_period_descriptor)

    descriptor_id = _get_descriptor_id_by_codevalue_and_namespace(
        engine, grading_period_descriptor, DESCRIPTOR_NAMESPACE
    )

    # Now add the grading period
    if GRADING_PERIOD_KEY not in already_loaded.keys():
        already_loaded[GRADING_PERIOD_KEY] = []

    grading_period_value = (
        str(grading_periods_df["PeriodSequence"].iloc[0])
        + str(grading_periods_df["Descriptor"].iloc[0])
        + str(grading_periods_df["SchoolId"].iloc[0])
        + str(grading_periods_df["SchoolYear"].iloc[0])
    )

    if grading_period_value in already_loaded[GRADING_PERIOD_KEY]:
        return

    grading_periods_df.rename(
        columns={"Descriptor": "GradingPeriodDescriptorId"}, inplace=True
    )
    grading_periods_df["GradingPeriodDescriptorId"] = descriptor_id

    grading_periods_df.to_sql("GradingPeriod", **_get_edfi_options(engine))

    already_loaded[GRADING_PERIOD_KEY].append(grading_period_value)


def load_assignment(engine: engine.base.Engine, assignment_table: str) -> None:
    assignment_df = read_keyvalue_pairs_as_dataframe(assignment_table)
    assignment_identifier = assignment_df.iloc[0]["AssignmentIdentifier"]

    ASSIGNMENT_KEY = "Assignment"
    if ASSIGNMENT_KEY not in already_loaded.keys():
        already_loaded[ASSIGNMENT_KEY] = []

    if assignment_identifier in already_loaded[ASSIGNMENT_KEY]:
        return

    sourcesystem = str(assignment_df["SourceSystem"].iloc[0])
    assignmentCategory = str(assignment_df["AssignmentCategory"].iloc[0])

    sourcesystem_descriptor_id = _get_descriptor_id_by_codevalue(engine, sourcesystem)
    assignment_df.rename(
        columns={"SourceSystem": "LMSSourceSystemDescriptorId"}, inplace=True
    )
    assignment_df["LMSSourceSystemDescriptorId"] = sourcesystem_descriptor_id

    assignmentcategory_descriptor_id = _get_descriptor_id_by_codevalue(
        engine, assignmentCategory
    )
    assignment_df.rename(
        columns={"AssignmentCategory": "AssignmentCategoryDescriptorId"}, inplace=True
    )
    assignment_df["AssignmentCategoryDescriptorId"] = assignmentcategory_descriptor_id

    assignment_df.to_sql("Assignment", **_get_lmsx_options(engine))

    already_loaded[ASSIGNMENT_KEY].append(assignment_identifier)


def populate_session_grading_period(engine: engine.base.Engine):
    SESSION_GRADING_PERIOD_KEY = "session grading period"
    if SESSION_GRADING_PERIOD_KEY in already_loaded.keys():
        return

    with engine.connect() as connection:
        connection.execute(POPULATE_SESSION_GRADING_PERIOD_SQL)

    already_loaded[SESSION_GRADING_PERIOD_KEY] = "loaded"


def load_student(engine: engine.base.Engine, student_table: str) -> None:
    student_df = read_keyvalue_pairs_as_dataframe(student_table)
    unique_id = student_df.iloc[0]["StudentUniqueId"]

    STUDENT_KEY = "Student"
    if STUDENT_KEY not in already_loaded.keys():
        already_loaded[STUDENT_KEY] = []

    if unique_id in already_loaded[STUDENT_KEY]:
        return

    student_df.to_sql("Student", **_get_edfi_options(engine))

    already_loaded[STUDENT_KEY].append(unique_id)


def _get_student_usi(engine: engine.base.Engine, student_unique_id: str) -> str:
    student_df = pd.read_sql(
        "SELECT StudentUSI FROM edfi.Student WHERE StudentUniqueId = ?",
        engine,
        params=[student_unique_id],
    )
    return str(student_df.iloc[0]["StudentUSI"])


def load_student_association(
    engine: engine.base.Engine, student_unique_id: str, school_id: str
) -> None:

    student_usi = _get_student_usi(engine, student_unique_id)

    # Student enrollment requires a SexType descriptor - not nullable
    SEX_TYPE_DESCRIPTOR = "Not identified"
    SEX_TYPE_DESCRIPTOR_KEY = "Sex Type"
    DESCRIPTOR_NAMESPACE = "uri://ed-fi.org/SexType"

    if SEX_TYPE_DESCRIPTOR_KEY not in already_loaded.keys():
        already_loaded[SEX_TYPE_DESCRIPTOR_KEY] = []

    if SEX_TYPE_DESCRIPTOR not in already_loaded[SEX_TYPE_DESCRIPTOR_KEY]:
        descriptor = pd.Series(
            {
                "CodeValue": SEX_TYPE_DESCRIPTOR,
                "ShortDescription": SEX_TYPE_DESCRIPTOR,
                "Description": SEX_TYPE_DESCRIPTOR,
                "Namespace": DESCRIPTOR_NAMESPACE,
            }
        )
        descriptor_sql = _prepare_descriptor_sql(
            descriptor, SCHEMA_EDFI, "SexDescriptor"
        )

        with engine.connect() as connection:
            connection.execute(text(descriptor_sql))

        already_loaded[SEX_TYPE_DESCRIPTOR_KEY].append(SEX_TYPE_DESCRIPTOR)

    descriptor_id = _get_descriptor_id_by_codevalue_and_namespace(
        engine, SEX_TYPE_DESCRIPTOR, DESCRIPTOR_NAMESPACE
    )

    # Now we can enroll the student at the school
    ENROLL_KEY = "Enrollment"
    enroll_value = f"{school_id}{student_usi}"

    if ENROLL_KEY not in already_loaded.keys():
        already_loaded[ENROLL_KEY] = []

    if enroll_value in already_loaded[ENROLL_KEY]:
        return

    enroll_df = pd.DataFrame(
        [
            {
                "EducationOrganizationId": school_id,
                "StudentUSI": student_usi,
                "SexDescriptorId": descriptor_id,
            }
        ]
    )

    enroll_df.to_sql(
        "StudentEducationOrganizationAssociation", **_get_edfi_options(engine)
    )

    already_loaded[ENROLL_KEY].append(enroll_value)


def load_student_section_association(
    engine: engine.base.Engine, student_unique_id: str, section_identifier
) -> None:

    student_usi = _get_student_usi(engine, student_unique_id)

    SECTION_ENROLL_KEY = "Section enroll"
    section_enroll_value = f"{student_usi}{section_identifier}"

    if SECTION_ENROLL_KEY not in already_loaded.keys():
        already_loaded[SECTION_ENROLL_KEY] = []

    if section_enroll_value in already_loaded[SECTION_ENROLL_KEY]:
        return

    # need to requery for the full section natural key
    SQL = """
SELECT LocalCourseCode, SchoolId, SchoolYear, SectionIdentifier, SessionName
FROM edfi.Section
WHERE SectionIdentifier = ?
"""

    section_df = pd.read_sql(SQL, engine, params=[section_identifier])

    section_association = section_df[
        [
            "LocalCourseCode",
            "SchoolId",
            "SchoolYear",
            "SectionIdentifier",
            "SessionName",
        ]
    ].copy()
    section_association["StudentUsi"] = student_usi
    section_association["BeginDate"] = "2021-07-20"

    section_association.to_sql("StudentSectionAssociation", **_get_edfi_options(engine))

    already_loaded[SECTION_ENROLL_KEY] = section_enroll_value


def load_assignment_submission(
    engine: engine.base.Engine,
    student_unique_id: str,
    assignment_identifier: str,
    submission_table: str,
) -> None:
    submission_df = read_keyvalue_pairs_as_dataframe(submission_table)
    identifier = submission_df.iloc[0]["AssignmentSubmissionIdentifier"]

    SUBMISSION_KEY = "Submission"
    if SUBMISSION_KEY not in already_loaded.keys():
        already_loaded[SUBMISSION_KEY] = []

    if identifier in already_loaded[SUBMISSION_KEY]:
        return

    submission_df["StudentUSI"] = _get_student_usi(engine, student_unique_id)
    submission_df["AssignmentIdentifier"] = assignment_identifier

    # Look up the status descriptor
    sql = """
SELECT
    sdesc.DescriptorId
FROM
    edfi.Descriptor sdesc
CROSS JOIN
    lmsx.Assignment
INNER JOIN
    edfi.Descriptor
ON
    Assignment.LMSSourceSystemDescriptorId = Descriptor.DescriptorId
AND
    Assignment.AssignmentIdentifier = ?
AND
    sdesc.Namespace = 'uri://ed-fi.org/edfilms/SubmissionStatusDescriptor/' + Descriptor.CodeValue
WHERE
    sdesc.CodeValue = ?
"""
    code_value = str(submission_df.iloc[0]["SubmissionStatus"])
    status_descriptor = pd.read_sql(
        sql, engine, params=[assignment_identifier, code_value]
    ).iloc[0]["DescriptorId"]
    submission_df["SubmissionStatusDescriptorId"] = status_descriptor
    submission_df.drop(columns=["SubmissionStatus"], inplace=True)

    submission_df.to_sql("AssignmentSubmission", **_get_lmsx_options(engine))

    already_loaded[SUBMISSION_KEY].append(identifier)
