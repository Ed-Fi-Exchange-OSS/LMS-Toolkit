# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pytest
import pandas as pd

from data_extractor.lib.export_data import tocsv

class TestExportData():
    class Test_when_tocsv_method_is_called():
        def test_given_no_data_parameter_then_throw_assert_exception(self):
            with pytest.raises(AssertionError):
                tocsv(None, '')

        def test_given_no_output_parameter_then_throw_assert_exception(self):
            with pytest.raises(AssertionError):
                tocsv([], None)

        def test_then_call_DataFrame_method(self, mocker):

            # Arrange
            DataFrame_mock = mocker.patch.object(pd, "DataFrame")

            # Act
            tocsv([], '')

            # Assert
            DataFrame_mock.assert_called_once()

        def test_then_call_DataFrame_method(self, mocker):

            # Arrange
            df_mock = mocker.Mock()
            DataFrame_mock = mocker.MagicMock(return_value = df_mock)
            mocker.patch.object(pd, "DataFrame", new = DataFrame_mock)

            # Act
            tocsv([], '')

            # Assert
            df_mock.to_csv.assert_called_once()



