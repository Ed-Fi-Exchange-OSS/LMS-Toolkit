# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

"""Grade Bands feature tests."""

from pytest_bdd import (
    given,
    parsers,
    scenario,
    then,
    when,
)
import pandas as pd
from sqlalchemy import engine


from .assertion_helpers import assert_dataframe_equals_table


@scenario('grade_bands_table.feature', 'Checking for the Table')
def test_checking_for_the_table():
    """Checking for the Table."""


@given("Analytics Middle Tier has been installed")
def given_AMT_is_installed(mssql_fixture: engine.base.Engine):
    # AMT installation is handled in the fixture setup
    pass


@when("I query the Grade Band Table", target_fixture="grade_band_df")
def query_the_grade_band_table(mssql_fixture: engine.base.Engine):
    return pd.read_sql("select * from analytics.engage_GradeBands order by LowerBound", mssql_fixture)


@then(parsers.parse("Grade Band has the following default records\n{records}"))
def grade_band_has_records(records: str, grade_band_df: pd.DataFrame):
    assert_dataframe_equals_table(records, grade_band_df)
