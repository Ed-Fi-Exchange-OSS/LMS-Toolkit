# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from sqlalchemy.engine.base import Connection

from .helpers.sql_scripts import (
    CREATE_SCHEMA_EDFI,
    CREATE_SCHEMA_LMS,
    CREATE_SCHEMA_EDFILMS,
    CREATE_TABLE_LMS_USER,
    CREATE_TABLE_EDFI_STUDENT_ETC,
    CREATE_TABLE_EDFI_SECTION,
    CREATE_TABLE_LMS_SECTION,
)


def _create_schemas(connection: Connection):
    connection.execute(CREATE_SCHEMA_EDFI)
    connection.execute(CREATE_SCHEMA_LMS)
    connection.execute(CREATE_SCHEMA_EDFILMS)


def _create_user_tables(connection: Connection):
    # from edfi_lms_ds_loader's create_user_tables.sql and add_mapping_columns_for_edfi_student_and_section.sql
    connection.execute(CREATE_TABLE_LMS_USER)
    # from ODS/API 5.2's 0002-Tables.sql
    connection.execute(CREATE_TABLE_EDFI_STUDENT_ETC)


def _create_section_tables(connection: Connection):
    connection.execute(CREATE_TABLE_EDFI_SECTION)
    connection.execute(CREATE_TABLE_LMS_SECTION)


# This is a copy/paste shortcut to initialize the test database with the proper structure
def migrate_lms_user_and_edfi_student(connection: Connection):
    _create_schemas(connection)
    _create_user_tables(connection)
    _create_section_tables(connection)
