# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from sqlalchemy.engine.base import Connection
from edfi_lms_ds_loader.mssql_lms_operations import MssqlLmsOperations
from edfi_lms_ds_loader.helpers.argparser import MainArguments


def main_arguments(adapter: MssqlLmsOperations, csv_path: str) -> MainArguments:
    args = MainArguments(csv_path=csv_path, engine="mssql", log_level="INFO")
    args.set_connection_string_using_integrated_security(
        "localhost", 1433, "test_integration_lms_toolkit"
    )
    # monkey patch the test adapter
    args.get_db_operations_adapter = lambda: adapter  # type: ignore
    return args


def insert_user(
    connection: Connection, ss_identifier: str, source_system: str, identifier: int
):
    # insert a required user with LMSUserIdentifier = 1
    connection.execute("SET IDENTITY_INSERT lms.LMSUser ON")
    connection.execute(
        f"""
    INSERT INTO [lms].[LMSUser]
           ([LMSUserIdentifier]
           ,[SourceSystemIdentifier]
           ,[SourceSystem]
           ,[UserRole]
           ,[SISUserIdentifier]
           ,[LocalUserIdentifier]
           ,[Name]
           ,[EmailAddress]
           ,[SourceCreateDate]
           ,[SourceLastModifiedDate]
           ,[CreateDate]
           ,[LastModifiedDate]
           ,[DeletedAt])
     VALUES
           ({identifier}
           ,N'{ss_identifier}'
           ,N'{source_system}'
           ,N'student'
           ,N'{ss_identifier}'
           ,N'{ss_identifier}'
           ,N'{ss_identifier}'
           ,N'{ss_identifier}'
           ,NULL
           ,NULL
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,NULL
           )
"""
    )
    connection.execute("SET IDENTITY_INSERT lms.LMSUser OFF")


def insert_section(
    connection: Connection, ss_identifier: str, source_system: str, identifier: int
):
    connection.execute("SET IDENTITY_INSERT lms.LMSSection ON")
    connection.execute(
        f"""
    INSERT INTO [lms].[LMSSection]
           ([LMSSectionIdentifier]
           ,[SourceSystemIdentifier]
           ,[SourceSystem]
           ,[SISSectionIdentifier]
           ,[Title]
           ,[SectionDescription]
           ,[Term]
           ,[LMSSectionStatus]
           ,[SourceCreateDate]
           ,[SourceLastModifiedDate]
           ,[CreateDate]
           ,[LastModifiedDate]
           ,[DeletedAt])
     VALUES
           ({identifier}
           ,N'{ss_identifier}'
           ,N'{source_system}'
           ,N'{ss_identifier}'
           ,N'{ss_identifier}'
           ,N'{ss_identifier}'
           ,N'{ss_identifier}'
           ,N'Archived'
           ,NULL
           ,NULL
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,NULL
           )
"""
    )
    connection.execute("SET IDENTITY_INSERT lms.LMSSection OFF")


def insert_assignment(
    connection: Connection,
    ss_identifier: str,
    source_system: str,
    identifier: int,
    section_identifier: int,
):
    connection.execute("SET IDENTITY_INSERT lms.Assignment ON")
    connection.execute(
        f"""
    INSERT INTO [lms].[Assignment]
           ([AssignmentIdentifier]
           ,[SourceSystemIdentifier]
           ,[SourceSystem]
           ,[LMSSectionIdentifier]
           ,[Title]
           ,[AssignmentCategory]
           ,[AssignmentDescription]
           ,[StartDateTime]
           ,[EndDateTime]
           ,[DueDateTime]
           ,[MaxPoints]
           ,[SourceCreateDate]
           ,[SourceLastModifiedDate]
           ,[CreateDate]
           ,[LastModifiedDate]
           ,[DeletedAt])
     VALUES
           ({identifier}
           ,N'{ss_identifier}'
           ,N'{source_system}'
           ,{section_identifier}
           ,N'{ss_identifier}'
           ,N'online_upload'
           ,N'{ss_identifier}'
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,100
           ,NULL
           ,NULL
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,NULL
           )
"""
    )
    connection.execute("SET IDENTITY_INSERT lms.Assignment OFF")


def insert_user_section_association(
    connection: Connection,
    ss_identifier: str,
    source_system: str,
    identifier: int,
    user_identifier: int,
    section_identifier: int,
):
    connection.execute("SET IDENTITY_INSERT lms.LMSUserLMSSectionAssociation ON")
    connection.execute(
        f"""
    INSERT INTO [lms].[LMSUserLMSSectionAssociation]
           ([LMSUserLMSSectionAssociationIdentifier]
           ,[LMSSectionIdentifier]
           ,[LMSUserIdentifier]
           ,[SourceSystemIdentifier]
           ,[SourceSystem]
           ,[EnrollmentStatus]
           ,[SourceCreateDate]
           ,[SourceLastModifiedDate]
           ,[CreateDate]
           ,[LastModifiedDate]
           ,[DeletedAt])
     VALUES
           ({identifier}
           ,{section_identifier}
           ,{user_identifier}
           ,N'{ss_identifier}'
           ,N'{source_system}'
           ,N'Active'
           ,NULL
           ,NULL
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,CAST(N'2021-01-01 00:00:00' AS DateTime)
           ,NULL
           )
"""
    )
    connection.execute("SET IDENTITY_INSERT lms.LMSUserLMSSectionAssociation OFF")
