# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from sqlalchemy.engine.base import Connection
from edfi_lms_ds_loader.sql_lms_operations import SqlLmsOperations
from edfi_lms_ds_loader.helpers.argparser import MainArguments
from tests_integration_pgsql.conftest import ConnectionSettings


def main_arguments(
    operations_adapter: SqlLmsOperations, csv_path: str, settings: ConnectionSettings
) -> MainArguments:
    args = MainArguments(
        csv_path,
        "postgresql",
        "INFO",
        settings.host,
        settings.db,
        settings.port,
        False,
        False,
    )
    args.db_adapter = operations_adapter.db_adapter

    # monkey patch the test adapter
    args.get_db_operations_adapter = lambda: operations_adapter  # type: ignore
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
    insert into lms.lmsuser
           (lmsuseridentifier
           ,sourcesystemidentifier
           ,sourcesystem
           ,userrole
           ,sisuseridentifier
           ,localuseridentifier
           ,name
           ,emailaddress
           ,sourcecreatedate
           ,sourcelastmodifieddate
           ,createdate
           ,lastmodifieddate
           ,deletedat)
        overriding system value
     values
           ({identifier}
           ,'{ss_identifier}'
           ,'{source_system}'
           ,'student'
           ,'{ss_identifier}'
           ,'{ss_identifier}'
           ,'{ss_identifier}'
           ,'{ss_identifier}'
           ,null
           ,null
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,null
           )
"""
    )
    reset_identity_sequence_number(connection, "lms.lmsuser", "lmsuseridentifier")


def insert_section(
    connection: Connection, ss_identifier: str, source_system: str, identifier: int
):
    connection.execute(
        f"""
    insert into lms.lmssection
           (lmssectionidentifier
           ,sourcesystemidentifier
           ,sourcesystem
           ,sissectionidentifier
           ,title
           ,sectiondescription
           ,term
           ,lmssectionstatus
           ,sourcecreatedate
           ,sourcelastmodifieddate
           ,createdate
           ,lastmodifieddate
           ,deletedat)
        overriding system value
     values
           ({identifier}
           ,'{ss_identifier}'
           ,'{source_system}'
           ,'{ss_identifier}'
           ,'{ss_identifier}'
           ,'{ss_identifier}'
           ,'{ss_identifier}'
           ,'Archived'
           ,null
           ,null
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,null
           )
"""
    )
    reset_identity_sequence_number(connection, "lms.lmssection", "lmssectionidentifier")


def insert_assignment(
    connection: Connection,
    ss_identifier: str,
    source_system: str,
    identifier: int,
    section_identifier: int,
):
    connection.execute(
        f"""
    insert into lms.assignment
           (assignmentidentifier
           ,sourcesystemidentifier
           ,sourcesystem
           ,lmssectionidentifier
           ,title
           ,assignmentcategory
           ,assignmentdescription
           ,startdatetime
           ,enddatetime
           ,duedatetime
           ,maxpoints
           ,sourcecreatedate
           ,sourcelastmodifieddate
           ,createdate
           ,lastmodifieddate
           ,deletedat)
        overriding system value
     values
           ({identifier}
           ,'{ss_identifier}'
           ,'{source_system}'
           ,'{section_identifier}'
           ,'{ss_identifier}'
           ,'online_upload'
           ,'{ss_identifier}'
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,100
           ,null
           ,null
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,null
           )
"""
    )
    reset_identity_sequence_number(connection, "lms.assignment", "assignmentidentifier")


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
    insert into lms.lmsuserlmssectionassociation
           (lmsuserlmssectionassociationidentifier
           ,lmssectionidentifier
           ,lmsuseridentifier
           ,sourcesystemidentifier
           ,sourcesystem
           ,enrollmentstatus
           ,sourcecreatedate
           ,sourcelastmodifieddate
           ,createdate
           ,lastmodifieddate
           ,deletedat)
        overriding system value
     values
           ({identifier}
           ,'{section_identifier}'
           ,'{user_identifier}'
           ,'{ss_identifier}'
           ,'{source_system}'
           ,'active'
           ,null
           ,null
           ,'2021-01-01 00:00:00'
           ,'2021-01-01 00:00:00'
           ,null
           )
"""
    )
    reset_identity_sequence_number(
        connection,
        "lms.lmsuserlmssectionassociation",
        "lmsuserlmssectionassociationidentifier",
    )
