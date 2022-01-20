# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from sqlalchemy.engine.base import Connection
from edfi_lms_ds_loader.sql_lms_operations import SqlLmsOperations
from edfi_lms_ds_loader.helpers.argparser import MainArguments
from tests_integration_pgsql.conftest import Settings


def main_arguments(adapter: SqlLmsOperations, csv_path: str) -> MainArguments:
    args = MainArguments(
        csv_path,
        "postgresql",
        "INFO",
        Settings.host,
        Settings.db,
        Settings.port,
        False,
        False,
    )
    args.build_pgsql_adapter(Settings.user, Settings.password)

    # monkey patch the test adapter
    args.get_db_operations_adapter = lambda: adapter  # type: ignore
    return args


def reset_identity_sequence_number(
    connection: Connection, table: str, column: str
) -> None:
    sql = f"""
select setval(pg_get_serial_sequence('{table}', '{column}'),
               (select max({column}) from {table})
        );
"""
    connection.execute(sql)


def insert_user(
    connection: Connection, ss_identifier: str, source_system: str, identifier: int
):
    # insert a required user with LMSUserIdentifier = 1
    connection.execute(
        f"""
    INSERT INTO lms.LMSUser
           (LMSUserIdentifier
           ,SourceSystemIdentifier
           ,SourceSystem
           ,UserRole
           ,SISUserIdentifier
           ,LocalUserIdentifier
           ,Name
           ,EmailAddress
           ,SourceCreateDate
           ,SourceLastModifiedDate
           ,CreateDate
           ,LastModifiedDate
           ,DeletedAt)
     VALUES
           ({identifier}
           ,'{ss_identifier}'
           ,'{source_system}'
           ,'student'
           ,'{ss_identifier}'
           ,'{ss_identifier}'
           ,'{ss_identifier}'
           ,'{ss_identifier}'
           ,NULL
           ,NULL
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,NULL
           )
"""
    )
    reset_identity_sequence_number(connection, "lms.LMSUser", "LMSUserIdentifier")


def insert_section(
    connection: Connection, ss_identifier: str, source_system: str, identifier: int
):
    connection.execute(
        f"""
    INSERT INTO lms.LMSSection
           (LMSSectionIdentifier
           ,SourceSystemIdentifier
           ,SourceSystem
           ,SISSectionIdentifier
           ,Title
           ,SectionDescription
           ,Term
           ,LMSSectionStatus
           ,SourceCreateDate
           ,SourceLastModifiedDate
           ,CreateDate
           ,LastModifiedDate
           ,DeletedAt)
     VALUES
           ({identifier}
           ,'{ss_identifier}'
           ,'{source_system}'
           ,'{ss_identifier}'
           ,'{ss_identifier}'
           ,'{ss_identifier}'
           ,'{ss_identifier}'
           ,'Archived'
           ,NULL
           ,NULL
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,NULL
           )
"""
    )
    reset_identity_sequence_number(connection, "lms.LMSSection", "LMSSectionIdentifier")


def insert_assignment(
    connection: Connection,
    ss_identifier: str,
    source_system: str,
    identifier: int,
    section_identifier: int,
):
    connection.execute(
        f"""
    INSERT INTO lms.Assignment
           (AssignmentIdentifier
           ,SourceSystemIdentifier
           ,SourceSystem
           ,LMSSectionIdentifier
           ,Title
           ,AssignmentCategory
           ,AssignmentDescription
           ,StartDateTime
           ,EndDateTime
           ,DueDateTime
           ,MaxPoints
           ,SourceCreateDate
           ,SourceLastModifiedDate
           ,CreateDate
           ,LastModifiedDate
           ,DeletedAt)
     VALUES
           ({identifier}
           ,'{ss_identifier}'
           ,'{source_system}'
           ,'{section_identifier}
           ,'{ss_identifier}'
           ,'online_upload'
           ,'{ss_identifier}'
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,100
           ,NULL
           ,NULL
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,NULL
           )
"""
    )
    reset_identity_sequence_number(connection, "lms.Assignment", "AssignmentIdentifier")


def insert_user_section_association(
    connection: Connection,
    ss_identifier: str,
    source_system: str,
    identifier: int,
    user_identifier: int,
    section_identifier: int,
):
    connection.execute(
        f"""
    INSERT INTO lms.LMSUserLMSSectionAssociation
           (LMSUserLMSSectionAssociationIdentifier
           ,LMSSectionIdentifier
           ,LMSUserIdentifier
           ,SourceSystemIdentifier
           ,SourceSystem
           ,EnrollmentStatus
           ,SourceCreateDate
           ,SourceLastModifiedDate
           ,CreateDate
           ,LastModifiedDate
           ,DeletedAt)
     VALUES
           ({identifier}
           ,'{section_identifier}
           ,'{user_identifier}
           ,'{ss_identifier}'
           ,'{source_system}'
           ,'Active'
           ,NULL
           ,NULL
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,NULL
           )
"""
    )
    reset_identity_sequence_number(
        connection,
        "lms.LMSUserLMSSectionAssociation",
        "LMSUserLMSSectionAssociationIdentifier",
    )
