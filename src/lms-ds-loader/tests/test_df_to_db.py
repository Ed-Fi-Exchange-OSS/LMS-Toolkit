# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from typing import Tuple
from unittest.mock import Mock

import pandas as pd
import pytest

from edfi_lms_ds_loader.df_to_db import upload_file


GENERIC_TABLE = "c"
SOURCE_SYSTEM = "google"


def describe_given_a_dataframe() -> None:
    @pytest.fixture
    def when_uploading_it() -> Tuple[Mock, pd.DataFrame]:
        # Arrange
        adapter = Mock()

        df = pd.DataFrame([{"SourceSystem": SOURCE_SYSTEM}])

        # Act
        upload_file(adapter, df, GENERIC_TABLE)

        return adapter, df

    def it_disables_the_natural_key_index(when_uploading_it) -> None:
        adapter, _ = when_uploading_it
        adapter.disable_staging_natural_key_index.assert_called_with(GENERIC_TABLE)

    def it_truncates_the_staging_table(when_uploading_it) -> None:
        adapter, _ = when_uploading_it
        adapter.truncate_staging_table.assert_called_with(GENERIC_TABLE)

    def it_reenables_natural_key_index(when_uploading_it) -> None:
        adapter, _ = when_uploading_it
        adapter.enable_staging_natural_key_index.assert_called_with(GENERIC_TABLE)

    def it_inserts_into_staging_table(when_uploading_it) -> None:
        adapter, df = when_uploading_it
        adapter.insert_into_staging.assert_called_with(df, GENERIC_TABLE)

    def it_inserts_into_production_table(when_uploading_it) -> None:
        adapter, _ = when_uploading_it
        adapter.insert_new_records_to_production.assert_called_with(GENERIC_TABLE, ["SourceSystem"])

    def it_updates_production_table(when_uploading_it) -> None:
        adapter, _ = when_uploading_it
        adapter.copy_updates_to_production.assert_called_with(GENERIC_TABLE, ["SourceSystem"])

    def it_soft_deletes_from_production_table(when_uploading_it) -> None:
        adapter, _ = when_uploading_it
        adapter.soft_delete_from_production.assert_called_with(GENERIC_TABLE, SOURCE_SYSTEM)

