# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from gzip import open as gz_open
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def load_data_frame(file_path: str) -> pd.DataFrame:
    logger.info("Reading file `%s`", file_path)

    if file_path.endswith("csv.gz"):
        with gz_open(file_path) as file:
            return pd.read_csv(file)  # type:ignore
    elif file_path.endswith(".csv"):
        return pd.read_csv(file)  # type:ignore
    elif file_path.endswith(".gitkeep"):
        return pd.DataFrame()  # type:ignore

    raise RuntimeError(f"Unrecognizable file type: {file_path}")
