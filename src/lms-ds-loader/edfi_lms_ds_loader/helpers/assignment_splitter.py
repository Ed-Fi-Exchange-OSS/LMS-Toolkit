# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import re
from typing import List, Tuple

import pandas as pd


def _splitter(text: str) -> List[str]:
    if len(text) == 0:
        return []

    if "'" not in text:
        return [text]

    # This regex looks for things like "a" and "b" in `['a', 'b']`.
    return re.findall("'([^']+)'", text)


def split(assignments_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:

    if assignments_df.empty:
        return (pd.DataFrame(), pd.DataFrame())

    SUB_TYPE = "SubmissionType"

    # These are columns that need to be in the final output, in addition to
    # SubmissionType. Note that "LastModifiedDate" does not make sense in this
    # case - if the source is modified then that value will become a "soft
    # deleted" row instead of being marked as modified.
    SOURCE_COLS = ["SourceSystem", "SourceSystemIdentifier", "CreateDate"]

    # Create a new DataFrame that will hold the Submission Type collection for
    # an Assignment.
    submission_type_df = assignments_df[[SUB_TYPE]].copy()

    # Remove Submission Type from the original DataFrame.
    assignments_df_2 = assignments_df.drop(SUB_TYPE, axis=1)

    # If an assignment has no SubmissionType then the resulting record will have
    # NA as a value. We don't care about those.
    submission_type_df.dropna(inplace=True)

    # No point in further processing if there are no rows.
    if submission_type_df.empty:
        return (assignments_df_2, submission_type_df)

    # Split the "SubmissionType" column, generating a variable number of new
    # columns - based on the number of items in the row that has the most items
    # in it.
    submission_type_df = submission_type_df.apply(
        lambda s: pd.Series(_splitter(s[0])), axis=1
    )

    # Because the operation above preserves the index from the original
    # DataFrame, we can merge the extra source columns from the original
    # DataFrame into the new one.
    submission_type_df[SOURCE_COLS] = assignments_df_2[SOURCE_COLS]

    # We have a variable number of new columns. Create a list containing just
    # the new columns.
    value_vars = list(set(submission_type_df.columns) - set(SOURCE_COLS))

    # The `melt` function takes the `value_var` columns and moves them to rows,
    # with each over the `value_var` column values being loaded into a single
    # new column labeled by `value_name`.
    submission_type_df = submission_type_df.melt(
        id_vars=SOURCE_COLS, value_vars=value_vars, value_name=SUB_TYPE
    )

    # The `melt` function also included the original column name for each
    # `value_var` in a new column called `variable`. Throw this one away.
    submission_type_df.drop(["variable"], inplace=True, axis=1)

    # Let's say that we had data like this in the original DataFrame:
    """
    SourceSystem, SourceSystemIdentifier, ..., SubmissionType,CreateDate,LastModifiedDate
    Canvas, 103, ..., "['online_text_entry', 'online_upload'],2021-03-11,2021-03-12"
    Canvas, 104, ..., "['online_upload'],2021-03-11,2021-03-12"
    """
    # Then the output right now is a DataFrame like this:
    """
    Canvas | 103 | online_text_entry | 2021-03-11
    Canvas | 103 | online_upload     | 2021-03-11
    Canvas | 104 | online_upload     | 2021-03-11
    Canvas | 104 | NA                | 2021-03-11
    """
    # Note the return of "NA". We need to remove these again.
    submission_type_df.dropna(inplace=True)

    return (assignments_df_2, submission_type_df)
