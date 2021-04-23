# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Tuple, List
from pandas import DataFrame
from sqlalchemy.engine.base import Connection
from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations
from edfi_lms_ds_loader.df_to_db import upload_users


def create_user_df(names: List[str]) -> DataFrame:
    repeat = len(names)

    return DataFrame(
        {
            "SourceSystemIdentifier": names,
            "Name": names,
            "EmailAddress": ["3"] * repeat,
            "SourceSystem": ["4"] * repeat,
            "UserRole": ["5"] * repeat,
            "LocalUserIdentifier": ["6"] * repeat,
            "SISUserIdentifier": ["7"] * repeat,
            "SourceCreateDate": ["2021-01-08"] * repeat,
            "SourceLastModifiedDate": ["2021-01-09"] * repeat,
            "CreateDate": ["2021-01-10"] * repeat,
            "LastModifiedDate": ["2021-01-11"] * repeat,
        }
    )


# A test in three parts - initial three users, then one user missing, then three users restored
def describe_when_a_user_goes_missing_then_reappears():
    initial_pull_names = ["Alice", "Bob", "Charlie"]
    bob_missing_from_names = ["Alice", "Charlie"]

    def it_should_soft_delete_then_restore(test_db: Tuple[MssqlLmsOperations, Connection]):
        # arrange
        adapter, connection = test_db

        # act - initial pull
        upload_users(adapter, create_user_df(initial_pull_names))

        # assert - staging table is correct
        stg_LMSUser = connection.execute("SELECT Name from lms.stg_LMSUser").fetchall()
        assert len(stg_LMSUser) == 3
        assert initial_pull_names == [x["Name"] for x in stg_LMSUser]

        # assert - production table is correct
        LMSUser = connection.execute("SELECT Name, DeletedAt from lms.LMSUser").fetchall()
        assert len(LMSUser) == 3
        assert initial_pull_names == [x["Name"] for x in LMSUser]
        assert [None, None, None] == [x["DeletedAt"] for x in LMSUser]

        # act - pull with Bob missing
        upload_users(adapter, create_user_df(bob_missing_from_names))

        # assert - staging table doesn't have Bob
        stg_LMSUser = connection.execute("SELECT Name from lms.stg_LMSUser").fetchall()
        assert len(stg_LMSUser) == 2
        assert bob_missing_from_names == [x["Name"] for x in stg_LMSUser]

        # assert - production table still has all three, with Bob soft deleted
        LMSUser = connection.execute("SELECT Name, DeletedAt from lms.LMSUser").fetchall()
        assert len(LMSUser) == 3
        assert initial_pull_names == [x["Name"] for x in LMSUser]
        deleted_ats = [x["DeletedAt"] for x in LMSUser]
        assert deleted_ats[0] is None
        assert deleted_ats[1] is not None
        assert deleted_ats[2] is None

        # act - pull with Bob restored
        upload_users(adapter, create_user_df(initial_pull_names))

        # assert - staging table has Bob
        stg_LMSUser = connection.execute("SELECT Name from lms.stg_LMSUser").fetchall()
        assert len(stg_LMSUser) == 3
        assert initial_pull_names == [x["Name"] for x in stg_LMSUser]

        # assert - production table still has all three, with Bob no longer soft deleted
        LMSUser = connection.execute("SELECT Name, DeletedAt from lms.LMSUser").fetchall()
        assert len(LMSUser) == 3
        assert initial_pull_names == [x["Name"] for x in LMSUser]
        assert [None, None, None] == [x["DeletedAt"] for x in LMSUser]
