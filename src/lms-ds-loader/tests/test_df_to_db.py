# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from unittest.mock import Mock

import pandas as pd

from edfi_lms_ds_loader.df_to_db import upload_file


def describe_when_uploading_a_dataframe():
    def it_orchestrates_calls_through_the_db_adapter():

        # Arrange
        adapter = Mock()
        TABLE = "c"
        SOURCE_SYSTEM = "google"

        df = pd.DataFrame([{"SourceSystem": SOURCE_SYSTEM}])

        # Act
        upload_file(adapter, df, TABLE)

        # Assert
        adapter.disable_staging_natural_key_index.assert_called_with(TABLE)
        adapter.truncate_staging_table.assert_called_with(TABLE)
        adapter.enable_staging_natural_key_index.assert_called_with(TABLE)
        adapter.insert_into_staging.assert_called_with(df, TABLE)
        adapter.insert_new_records_to_production.assert_called_with(TABLE, ["SourceSystem"])
        adapter.copy_updates_to_production.assert_called_with(TABLE, ["SourceSystem"])
        adapter.soft_delete_from_production.assert_called_with(TABLE, SOURCE_SYSTEM)
