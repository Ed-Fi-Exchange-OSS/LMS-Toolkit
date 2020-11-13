# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging

import pandas as pd

from .mapping import usage_analytics as usageMap


def get_system_activities(usage_df: pd.DataFrame) -> pd.DataFrame:

    # TODO: instead of accepting the usage data frame as an argument, accept the
    # input file directory as an argument. Get all file names from the input
    # directory. For each file, look in SQLite to see if the file has been
    # processed (this will necessitate creating a new table, of course). Then
    # for each file, use the csv_reader class to read in a DataFrame. If
    # there are multiple files then combine them into the same DataFrame.
    # Psuedocode below might be improved with some logging. Logging here
    # is probably better than logging inside the csv_reader or usageMap.
    #
    # def get_system_activities(input_directory) -> pd.DataFrame.
    #   output = pd.DataFrame()
    #   for file in os.scandir({only .csv or .csv.gz files}):
    #       raw_data = csv_reader.load_data_frame(file)
    #       mapped_data = usageMap.map_to_udm(raw_data)
    #       output.append(mapped_data)
    #
    #   # If reports have overlapping dates then we'll have duplicates
    #   output.drop_duplicates(inplace=True)
    #
    #   return output

    return usageMap.map_to_udm(usage_df)
