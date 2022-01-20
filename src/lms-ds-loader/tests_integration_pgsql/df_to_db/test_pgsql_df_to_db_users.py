# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from typing import Tuple, List
from pandas import DataFrame
from sqlalchemy.engine.base import Connection
from edfi_lms_ds_loader.sql_lms_operations import SqlLmsOperations
from edfi_lms_ds_loader.df_to_db import upload_users

USER_NAMES = ["Alice", "Bob", "Charlie"]
ORIGINAL_USER_ROLE = "5"
ORIGINAL_LAST_MODIFIED_DATE = "2021-01-11"
UPDATED_LAST_MODIFIED_DATE = "2022-01-11"


# User DataFrame factory for tests given list of names
def create_user_df(names: List[str]) -> DataFrame:
    repeat = len(names)

    return DataFrame(
        {
            "SourceSystemIdentifier": names,
            "Name": names,
            "EmailAddress": ["3"] * repeat,
            "SourceSystem": ["4"] * repeat,
            "UserRole": [ORIGINAL_USER_ROLE] * repeat,
            "LocalUserIdentifier": ["6"] * repeat,
            "SISUserIdentifier": ["7"] * repeat,
            "SourceCreateDate": ["2021-01-08"] * repeat,
            "SourceLastModifiedDate": ["2021-01-09"] * repeat,
            "CreateDate": ["2021-01-10"] * repeat,
            "LastModifiedDate": [ORIGINAL_LAST_MODIFIED_DATE] * repeat,
        }
    )


def describe_when_a_user_is_updated():
    UPDATED_USER_ROLE = "55"

    def it_should_have_the_update_in_production(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection]
    ):
        adapter, connection = test_pgsql_db

        def initial_upload():
            # act
            upload_users(adapter, create_user_df(USER_NAMES))

            # assert - staging table is correct
            stg_LMSUser = connection.execute(
                "SELECT Name, UserRole from lms.stg_LMSUser"
            ).fetchall()
            assert len(stg_LMSUser) == 3
            assert USER_NAMES == [x["Name"] for x in stg_LMSUser]

            # assert - user roles are correct in staging
            assert [ORIGINAL_USER_ROLE, ORIGINAL_USER_ROLE, ORIGINAL_USER_ROLE] == [
                x["UserRole"] for x in stg_LMSUser
            ]

            # assert - production table is correct
            LMSUser = connection.execute(
                "SELECT Name, UserRole from lms.LMSUser"
            ).fetchall()
            assert len(LMSUser) == 3
            assert USER_NAMES == [x["Name"] for x in LMSUser]

            # assert - user roles are correct in production
            assert [ORIGINAL_USER_ROLE, ORIGINAL_USER_ROLE, ORIGINAL_USER_ROLE] == [
                x["UserRole"] for x in LMSUser
            ]

        def update_bob_user_role():
            # arrange - update to Bob's user role
            updated_user_df = create_user_df(USER_NAMES)
            updated_user_df.at[1, "UserRole"] = UPDATED_USER_ROLE
            updated_user_df.at[1, "LastModifiedDate"] = UPDATED_LAST_MODIFIED_DATE

            # act
            upload_users(adapter, updated_user_df)

            # assert - staging table is loaded
            stg_LMSUser = connection.execute(
                "SELECT Name, UserRole from lms.stg_LMSUser"
            ).fetchall()
            assert len(stg_LMSUser) == 3
            assert USER_NAMES == [x["Name"] for x in stg_LMSUser]

            # assert - user roles are correct in staging
            assert [ORIGINAL_USER_ROLE, UPDATED_USER_ROLE, ORIGINAL_USER_ROLE] == [
                x["UserRole"] for x in stg_LMSUser
            ]

            # assert - production table is loaded
            LMSUser = connection.execute(
                "SELECT Name, UserRole from lms.LMSUser"
            ).fetchall()
            assert len(LMSUser) == 3
            assert USER_NAMES == [x["Name"] for x in LMSUser]

            # assert - user roles are correct in production
            assert [ORIGINAL_USER_ROLE, UPDATED_USER_ROLE, ORIGINAL_USER_ROLE] == [
                x["UserRole"] for x in LMSUser
            ]

        initial_upload()
        update_bob_user_role()


def describe_when_a_user_goes_missing_then_reappears():
    USER_NAMES_WITHOUT_BOB = ["Alice", "Charlie"]

    def it_should_soft_delete_then_restore(
        test_pgsql_db: Tuple[SqlLmsOperations, Connection]
    ):
        adapter, connection = test_pgsql_db

        def initial_upload():
            # act
            upload_users(adapter, create_user_df(USER_NAMES))

            # assert - staging table is correct
            stg_LMSUser = connection.execute(
                "SELECT Name from lms.stg_LMSUser"
            ).fetchall()
            assert len(stg_LMSUser) == 3
            assert USER_NAMES == [x["Name"] for x in stg_LMSUser]

            # assert - production table is correct
            LMSUser = connection.execute(
                "SELECT Name, DeletedAt from lms.LMSUser"
            ).fetchall()
            assert len(LMSUser) == 3
            assert USER_NAMES == [x["Name"] for x in LMSUser]
            assert [None, None, None] == [x["DeletedAt"] for x in LMSUser]

        def upload_with_bob_missing():
            # act
            upload_users(adapter, create_user_df(USER_NAMES_WITHOUT_BOB))

            # assert - staging table doesn't have Bob
            stg_LMSUser = connection.execute(
                "SELECT Name from lms.stg_LMSUser"
            ).fetchall()
            assert len(stg_LMSUser) == 2
            assert USER_NAMES_WITHOUT_BOB == [x["Name"] for x in stg_LMSUser]

            # assert - production table still has all three, with Bob soft deleted
            LMSUser = connection.execute(
                "SELECT Name, DeletedAt from lms.LMSUser"
            ).fetchall()
            assert len(LMSUser) == 3
            assert USER_NAMES == [x["Name"] for x in LMSUser]
            deleted_ats = [x["DeletedAt"] for x in LMSUser]
            assert deleted_ats[0] is None
            assert deleted_ats[1] is not None
            assert deleted_ats[2] is None

        def upload_with_bob_restored():
            # arrange - Bob restored
            updated_user_df = create_user_df(USER_NAMES)
            updated_user_df.at[1, "LastModifiedDate"] = UPDATED_LAST_MODIFIED_DATE

            # act
            upload_users(adapter, updated_user_df)

            # assert - staging table has Bob
            stg_LMSUser = connection.execute(
                "SELECT Name from lms.stg_LMSUser"
            ).fetchall()
            assert len(stg_LMSUser) == 3
            assert USER_NAMES == [x["Name"] for x in stg_LMSUser]

            # assert - production table still has all three, with Bob no longer soft deleted
            LMSUser = connection.execute(
                "SELECT Name, DeletedAt from lms.LMSUser"
            ).fetchall()
            assert len(LMSUser) == 3
            assert USER_NAMES == [x["Name"] for x in LMSUser]
            assert [None, None, None] == [x["DeletedAt"] for x in LMSUser]

        initial_upload()
        upload_with_bob_missing()
        upload_with_bob_restored()
