# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd

from edfi_canvas_extractor.mapping import constants


def convert_to_standard_date_time_string(df: pd.DataFrame, column: str) -> None:
    # Converting string to datetime, then formatting, back to string, and finally
    # replacing any errors (na) with empty string.

    df[column] = pd.to_datetime(
        df[column], infer_datetime_format=True, errors="coerce", utc=True
    ).dt.strftime(constants.DATE_FORMAT)

    df.loc[df[column].isna(), column] = ""
