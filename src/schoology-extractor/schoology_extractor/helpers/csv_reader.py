# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from gzip import open as gz_open
from pandas import DataFrame, read_csv
import logging

logger = logging.getLogger(__name__)


def load_data_frame(file_path: str) -> DataFrame:
    logger.info("Reading file `%s`", file_path)

    if file_path.endswith(".csv.gz"):
        with gz_open(file_path) as file:
            return read_csv(file)
    elif file_path.endswith(".csv"):
        return read_csv(file_path)
    elif file_path.endswith(".gitkeep"):
        return DataFrame()

    raise RuntimeError(f"Unrecognizable file type: {file_path}")
