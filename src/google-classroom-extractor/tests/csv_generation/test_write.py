# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime
from typing import Dict, Tuple
from unittest.mock import call, patch
from pandas import DataFrame
from google_classroom_extractor.csv_generation.write import (
    write_multi_csv,
    write_multi_tuple_csv,
    write_csv
)


DF1_TO_WRITE: DataFrame = DataFrame(data={"dummy": ["1"]})
DF2_TO_WRITE: DataFrame = DataFrame(data={"dummy": ["1"]})
ID1_VALUE: str = "ID1_VALUE"
ID2_VALUE: str = "ID2_VALUE"
MULTI_CSV_TEMPLATE = "{id}"
MULTI_TUPLE_CSV_TEMPLATE = "{id1}{id2}"
OUTPUT_DATE: datetime = datetime.now()


def describe_when_calling_write_multi_csv_with_one_dataframe():
    @patch("google_classroom_extractor.csv_generation.write.write_csv")
    def it_should_call_write_csv_once_with_df1(mock_write_csv):
        # arrange
        dfs_to_write: Dict[str, DataFrame] = {
            ID1_VALUE: DF1_TO_WRITE,
        }

        # act
        write_multi_csv(dfs_to_write, OUTPUT_DATE, MULTI_CSV_TEMPLATE)

        # assert
        assert mock_write_csv.call_args_list == [
            call(DF1_TO_WRITE, OUTPUT_DATE, ID1_VALUE)
        ]


def describe_when_calling_write_multi_csv_with_two_dataframes():
    @patch("google_classroom_extractor.csv_generation.write.write_csv")
    def it_should_call_write_csv_once_with_df1(mock_write_csv):
        # arrange
        dfs_to_write: Dict[str, DataFrame] = {
            ID1_VALUE: DF1_TO_WRITE,
            ID2_VALUE: DF2_TO_WRITE,
        }

        # act
        write_multi_csv(dfs_to_write, OUTPUT_DATE, MULTI_CSV_TEMPLATE)

        # assert
        assert mock_write_csv.call_args_list == [
            call(DF1_TO_WRITE, OUTPUT_DATE, ID1_VALUE),
            call(DF2_TO_WRITE, OUTPUT_DATE, ID2_VALUE),
        ]


def describe_when_calling_write_multi_tuple_csv_with_one_dataframe():
    @patch("google_classroom_extractor.csv_generation.write.write_csv")
    def it_should_call_write_csv_once_with_df1(mock_write_csv):
        # arrange
        dfs_to_write: Dict[Tuple[str, str], DataFrame] = {
            (ID1_VALUE, ID2_VALUE): DF1_TO_WRITE,
        }

        # act
        write_multi_tuple_csv(dfs_to_write, OUTPUT_DATE, MULTI_TUPLE_CSV_TEMPLATE)

        # assert
        assert mock_write_csv.call_args_list == [
            call(DF1_TO_WRITE, OUTPUT_DATE, f"{ID1_VALUE}{ID2_VALUE}")
        ]


def describe_when_calling_write_multi_tuple_csv_with_two_dataframes():
    @patch("google_classroom_extractor.csv_generation.write.write_csv")
    def it_should_call_write_csv_once_with_df1(mock_write_csv):
        # arrange
        dfs_to_write: Dict[Tuple[str, str], DataFrame] = {
            (ID1_VALUE, ID2_VALUE): DF1_TO_WRITE,
            (ID2_VALUE, ID1_VALUE): DF2_TO_WRITE,
        }

        # act
        write_multi_tuple_csv(dfs_to_write, OUTPUT_DATE, MULTI_TUPLE_CSV_TEMPLATE)

        # assert
        assert mock_write_csv.call_args_list == [
            call(DF1_TO_WRITE, OUTPUT_DATE, f"{ID1_VALUE}{ID2_VALUE}"),
            call(DF2_TO_WRITE, OUTPUT_DATE, f"{ID2_VALUE}{ID1_VALUE}")
        ]


def describe_when_writing_csv_to_file():
    def it_should_handle_exceptions():
        df_to_write = DF1_TO_WRITE
        output_date = OUTPUT_DATE
        directory = "this:is:invalid:will:cause:exception"

        write_csv(df_to_write, output_date, directory)

        # if we make it this far without an exception, then the exception caused
        # by the bad directory must have been handled correctly.
