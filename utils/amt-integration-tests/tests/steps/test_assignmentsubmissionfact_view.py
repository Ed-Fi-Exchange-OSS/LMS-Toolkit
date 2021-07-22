# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

"""AssignmentSubmissionDim view feature tests"""

from pytest_bdd import (
    given,
    parsers,
    scenario,
    then,
    when,
)
import pandas as pd
from sqlalchemy import engine

from ..assertion_helpers import (
    assert_dataframe_has_one_row_matching,
    assert_dataframe_has_columns,
)
from ..data_helpers import (
    load_assignment,
    load_assignment_submission,
    load_grading_period,
    load_school,
    load_school_year,
    load_session,
    load_section,
    load_student_section_association,
    load_student,
    load_student_association,
    populate_session_grading_period,
)


@scenario("../features/assignmentsubmissionfact_view.feature", "Ensure the view exists")
def test_assignment_dim_view_exists() -> None:
    pass


@scenario(
    "../features/assignmentsubmissionfact_view.feature",
    "On Time Happy Path (Canvas - on-time)",
)
def test_ontime_canvas() -> None:
    pass


@scenario(
    "../features/assignmentsubmissionfact_view.feature",
    "On Time Happy Path (Canvas - graded)",
)
def test_ontime_graded() -> None:
    pass


@scenario(
    "../features/assignmentsubmissionfact_view.feature", "Late Happy Path (Canvas)"
)
def test_late_canvas() -> None:
    pass


@scenario(
    "../features/assignmentsubmissionfact_view.feature",
    "Missing or Past Due Happy Path (Canvas)",
)
def test_pastdue_canvas() -> None:
    pass


@scenario(
    "../features/assignmentsubmissionfact_view.feature",
    "On Time Happy Path (Schoology)",
)
def test_ontime_schoology() -> None:
    pass


@scenario(
    "../features/assignmentsubmissionfact_view.feature", "Late Happy Path (Schoology)"
)
def test_late_schoology() -> None:
    pass


@scenario(
    "../features/assignmentsubmissionfact_view.feature",
    "Do not report on Schoology drafts",
)
def test_draft_schoology() -> None:
    pass


@scenario(
    "../features/assignmentsubmissionfact_view.feature", "On Time Happy Path (Google)"
)
def test_ontime_google() -> None:
    pass


@scenario(
    "../features/assignmentsubmissionfact_view.feature",
    "On Time Happy Path (Google - Returned)",
)
def test_returned_google() -> None:
    pass


@scenario(
    "../features/assignmentsubmissionfact_view.feature", "Late Happy Path (Google)"
)
def test_late_google() -> None:
    pass


@scenario(
    "../features/assignmentsubmissionfact_view.feature",
    "Missing or Past Due Happy Path (Google)",
)
def test_pastdue_google() -> None:
    pass


@scenario(
    "../features/assignmentsubmissionfact_view.feature",
    "Do not report on Google New submissions",
)
def test_new_google() -> None:
    pass


@scenario(
    "../features/assignmentsubmissionfact_view.feature",
    "Do not report on Google Created submissions",
)
def test_created_google() -> None:
    pass


@scenario(
    "../features/assignmentsubmissionfact_view.feature",
    "Do not report on Google Reclaimed submissions",
)
def test_reclaimed_google() -> None:
    pass


@given("Analytics Middle Tier has been installed")
def given_AMT_is_installed(mssql_fixture: engine.base.Engine):
    # AMT installation is handled in the fixture setup
    pass


@given(parsers.parse("there is a school with id {school_id}"))
def given_there_is_a_school(mssql_fixture: engine.base.Engine, school_id: str) -> None:
    load_school(mssql_fixture, school_id)


@given(parsers.parse("the school year is {school_year}"))
def given_school_year(mssql_fixture: engine.base.Engine, school_year: str) -> None:
    load_school_year(mssql_fixture, school_year)


@given(
    parsers.parse(
        'school {school_id} has a session called "{session_name}" in year {school_year}'
    )
)
def given_session(
    mssql_fixture: engine.base.Engine,
    school_id: str,
    session_name: str,
    school_year: str,
) -> None:
    load_session(mssql_fixture, school_id, session_name, school_year)


@given(parsers.parse("there is a section\n{section_table}"))
def given_section(mssql_fixture: engine.base.Engine, section_table: str) -> None:
    load_section(mssql_fixture, section_table)


@given(parsers.parse("there is a grading period\n{grading_period_table}"))
def given_grading_period(
    mssql_fixture: engine.base.Engine, grading_period_table: str
) -> None:
    load_grading_period(mssql_fixture, grading_period_table)


@given("edfi.SessionGradingPeriod table is populated")
def given_session_grading_period_is_populated(
    mssql_fixture: engine.base.Engine,
) -> None:
    populate_session_grading_period(mssql_fixture)


@given(parsers.parse("there is a student\n{student_table}"))
def given_there_is_a_student(
    mssql_fixture: engine.base.Engine, student_table: str
) -> None:
    load_student(mssql_fixture, student_table)


@given(parsers.parse('student "{student_id}" is enrolled at school {school_id}'))
def given_student_enrolled(
    mssql_fixture: engine.base.Engine, student_id: str, school_id: str
) -> None:
    load_student_association(mssql_fixture, student_id, school_id)


@given(parsers.parse("there is one Assignment\n{assignment_table}"))
def given_assignment(mssql_fixture: engine.base.Engine, assignment_table: str) -> None:
    load_assignment(mssql_fixture, assignment_table)


@given(
    parsers.parse(
        'student "{student_unique_id}" is enrolled in section "{section_identifier}"'
    )
)
def given_student_section_enrollment(
    mssql_fixture: engine.base.Engine, student_unique_id: str, section_identifier: str
) -> None:
    load_student_section_association(
        mssql_fixture, student_unique_id, section_identifier
    )


@given(
    parsers.parse(
        'student "{student_unique_id}" has a submission for assignment "{assignment_identifier}"\n{submission_table}'
    )
)
def given_assignment_submission(
    mssql_fixture: engine.base.Engine,
    student_unique_id: str,
    assignment_identifier: str,
    submission_table: str,
) -> None:
    load_assignment_submission(
        mssql_fixture, student_unique_id, assignment_identifier, submission_table
    )


@when(
    parsers.parse('I query for assignment submission "{submission_identifier}"'),
    target_fixture="assignment_df",
)
def when_query_for_assignment(
    mssql_fixture: engine.base.Engine, submission_identifier: str
) -> pd.DataFrame:

    SELECT_FROM_ASSIGNMENT = "SELECT * FROM analytics.engage_AssignmentSubmissionFact WHERE AssignmentSubmissionKey = ?"
    return pd.read_sql(
        SELECT_FROM_ASSIGNMENT, mssql_fixture, params=[submission_identifier]
    )


@then(parsers.parse("it has these columns:\n{table}"))
def it_has_columns(table: str, assignment_df: pd.DataFrame) -> None:
    assert_dataframe_has_columns(table, assignment_df)


@then(parsers.parse("there should be {expected} submission records"))
def then_zero_records(assignment_df, expected) -> None:
    assert assignment_df.shape[0] == int(expected)


@then(parsers.parse("the submission record should have these values:\n{table}"))
def it_has_values(table: str, assignment_df: pd.DataFrame) -> None:
    assert_dataframe_has_one_row_matching(table, assignment_df)
