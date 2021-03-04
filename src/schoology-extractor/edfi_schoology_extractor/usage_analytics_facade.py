# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
import os

import pandas as pd
import sqlalchemy

from .helpers import csv_reader
from .helpers import sync
from .mapping import usage_analytics as usageMap

logger = logging.getLogger(__name__)


def get_system_activities(
    usage_input_dir: str, db_engine: sqlalchemy.engine.base.Engine
) -> pd.DataFrame:
    """
    Processes the .csv or .gz files from the input directory.

    Parameters
    ----------
    usage_input_dir: str
        Directory where the System Activities reports are stored

    Returns
    -------
    pd.DataFrame
        Data reshaped into the Ed-Fi LMS Unified Data Model(UDM)
    """

    output = pd.DataFrame()
    logger.debug(
        f"Processing usage analytics files: loading files from {usage_input_dir}"
    )
    for file in os.scandir(usage_input_dir):
        # It is not expected to have anything different from .gz or .csv
        # in case there's something different, this method will throw an
        # exception

        mapped_row = pd.DataFrame()

        if not sync.usage_file_is_processed(file.name, db_engine):
            logger.info(f"Processing usage analytics file: {file.name}")
            row_data = csv_reader.load_data_frame(file.path)
            mapped_row = usageMap.map_to_udm(row_data)
            sync.insert_usage_file_name(file.name, db_engine)
        else:
            logger.debug(
                f"Ignoring usage analytics file because it has already been processed: {file.name}"
            )

        if not output.empty:
            output.append(mapped_row)
        else:
            output = mapped_row

    if output.empty:
        logger.info("No new usage analytics files were found")
        return output

    # If reports have overlapping dates then we'll have duplicates
    logger.debug(
        "Processing usage_analytics files: Removing duplicated system activities from DataFrame"
    )
    output.drop_duplicates(inplace=True)

    return output
