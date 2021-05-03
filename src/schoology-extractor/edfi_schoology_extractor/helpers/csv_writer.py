# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import logging

logger = logging.getLogger(__name__)


def df_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """
    Exports a DataFrame to CSV

    Parameters
    ----------
    df : DataFrame
        The data that will be exported to csv.
    output_path : str
        The path and name where you want your csv to be generated.

    """

    df.to_csv(output_path, index=False)
    logger.info("The file has been generated => %s" % output_path)
