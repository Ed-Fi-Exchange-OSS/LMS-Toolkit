# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from edfi_lms_ds_loader.db_operations.PGSQL_sql_builder import (
    drop_staging_natural_key_index,
    truncate_stg_table,
    recreate_staging_natural_key_index,
    insert_new_records_to_production,
    insert_new_records_to_production_for_user_relation,
    insert_new_records_to_production_for_section_relation,
    insert_new_records_to_production_for_section_and_user_relation,
    copy_updates_to_production,
    soft_delete_from_production,
    get_processed_files,
    add_processed_file,
)


def describe_when_truncate_stg_table_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "A_TABLE_FOR_TESTING"
        expected = (
            "truncate table lms.stg_a_table_for_testing restart identity;".strip()
        )

        # Act
        sql = truncate_stg_table(table).strip()

        # Assert
        assert sql == expected


def describe_when_drop_staging_natural_key_index_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "A_TABLE_FOR_TESTING"
        expected = (
            "drop index if exists lms.ix_stg_a_table_for_testing_natural_key;".strip()
        )

        # Act
        sql = drop_staging_natural_key_index(table).strip()

        # Assert
        assert sql == expected


def describe_when_recreate_staging_natural_key_index_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "A_TABLE_FOR_TESTING"
        expected = "create index ix_stg_a_table_for_testing_natural_key on lms.stg_a_table_for_testing (sourcesystemidentifier, sourcesystem, lastmodifieddate);"

        # Act
        sql = recreate_staging_natural_key_index(table)

        # Assert
        assert sql == expected


def describe_when_insert_new_records_to_production_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "A_TABLE_FOR_TESTING"
        column_string = "COLUMNS"
        expected = """
insert into
    lms.a_table_for_testing
(columns
)
select columns
from
    lms.stg_a_table_for_testing as stg
where
    not exists (
        select
            1
        from
            lms.a_table_for_testing
        where
            sourcesystemidentifier = stg.sourcesystemidentifier
        and
            sourcesystem = stg.sourcesystem
    )
""".strip()

        # Act
        sql = insert_new_records_to_production(table, column_string).strip()

        # Assert
        assert sql == expected


def describe_when_insert_new_records_to_production_for_user_relation_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "A_TABLE_FOR_TESTING"
        insert_columns = "insert_columns"
        select_columns = "select_columns"
        expected = """
insert into
    lms.a_table_for_testing
(
    lmsuseridentifier,insert_columns
)
select
    lmsuser.lmsuseridentifier,select_columns
from
    lms.stg_a_table_for_testing as stg
inner join
    lms.lmsuser
on
    stg.lmsusersourcesystemidentifier = lmsuser.sourcesystemidentifier
and
    stg.sourcesystem = lmsuser.sourcesystem
where not exists (
  select
    1
  from
    lms.a_table_for_testing
  where
    sourcesystemidentifier = stg.sourcesystemidentifier
  and
    sourcesystem = stg.sourcesystem
)
""".strip()

        # Act
        sql = insert_new_records_to_production_for_user_relation(
            table, insert_columns, select_columns
        ).strip()

        # Assert
        assert sql == expected


def describe_when_insert_new_records_to_production_for_section_relation_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "A_TABLE_FOR_TESTING"
        insert_columns = "insert_columns"
        select_columns = "select_columns"
        expected = """
insert into
    lms.a_table_for_testing
(
    lmssectionidentifier,insert_columns
)
select
    lmssection.lmssectionidentifier,select_columns
from
    lms.stg_a_table_for_testing as stg
inner join
    lms.lmssection
on
    stg.lmssectionsourcesystemidentifier = lmssection.sourcesystemidentifier
and
    stg.sourcesystem = lmssection.sourcesystem
where not exists (
  select
    1
  from
    lms.a_table_for_testing
  where
    sourcesystemidentifier = stg.sourcesystemidentifier
  and
    sourcesystem = stg.sourcesystem
)
""".strip()

        # Act
        sql = insert_new_records_to_production_for_section_relation(
            table, insert_columns, select_columns
        ).strip()

        # Assert
        assert sql == expected


def describe_when_insert_new_records_to_production_for_section_and_user_relation_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "A_TABLE_FOR_TESTING"
        insert_columns = "insert_columns"
        select_columns = "select_columns"
        expected = """
insert into
    lms.a_table_for_testing
(
    lmssectionidentifier,
    lmsuseridentifier,insert_columns
)
select
    lmssection.lmssectionidentifier,
    lmsuser.lmsuseridentifier,select_columns
from
    lms.stg_a_table_for_testing as stg
inner join
    lms.lmssection
on
    stg.lmssectionsourcesystemidentifier = lmssection.sourcesystemidentifier
and
    stg.sourcesystem = lmssection.sourcesystem
inner join
    lms.lmsuser
on
    stg.lmsusersourcesystemidentifier = lmsuser.sourcesystemidentifier
and
    stg.sourcesystem = lmsuser.sourcesystem
where not exists (
  select
    1
  from
    lms.a_table_for_testing
  where
    sourcesystemidentifier = stg.sourcesystemidentifier
  and
    sourcesystem = stg.sourcesystem
)
""".strip()

        # Act
        sql = insert_new_records_to_production_for_section_and_user_relation(
            table, insert_columns, select_columns
        ).strip()

        # Assert
        assert sql == expected


def describe_when_copy_updates_to_production_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "A_TABLE_FOR_TESTING"
        update_columns = "update_columns"
        expected = """
update
    lms.a_table_for_testing
set update_columns
from
    lms.a_table_for_testing t
inner join
    lms.stg_a_table_for_testing as stg
on
    t.sourcesystem = stg.sourcesystem
and
    t.sourcesystemidentifier = stg.sourcesystemidentifier
and
    t.lastmodifieddate <> stg.lastmodifieddate
where
    t.sourcesystemidentifier = lms.a_table_for_testing.sourcesystemidentifier
and
    t.sourcesystem = lms.a_table_for_testing.sourcesystem
""".strip()

        # Act
        sql = copy_updates_to_production(table, update_columns).strip()

        # Assert
        assert sql == expected


def describe_when_soft_delete_from_production_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "A_TABLE_FOR_TESTING"
        source_system = "sourcESystem"
        expected = """
update
    lms.a_table_for_testing
set
    deletedat = now()
from
    lms.a_table_for_testing as t
where
    not exists (
        select
            1
        from
            lms.stg_a_table_for_testing as stg
        where
            t.sourcesystemidentifier = stg.sourcesystemidentifier
        and
            t.sourcesystem = stg.sourcesystem
    )
and
    t.deletedat is null
and
    t.sourcesystem = 'sourcESystem'
and
    lms.a_table_for_testing.sourcesystem = t.sourcesystem
and
    lms.a_table_for_testing.sourcesystemidentifier = t.sourcesystemidentifier
""".strip()

        # Act
        sql = soft_delete_from_production(table, source_system).strip()

        # Assert
        assert sql == expected


def describe_when_get_processed_files_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        resource_name = "a_Resource_Name"
        expected = """
select
    fullpath
from
    lms.processedfiles
where
    resourcename = 'a_Resource_Name'
""".strip()

        # Act
        sql = get_processed_files(resource_name).strip()

        # Assert
        assert sql == expected


def describe_when_add_processed_file_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        path = "the_Path/"
        resource_name = "a_Resource_Name"
        rows = 23
        expected = """
insert into
    lms.processedfiles
(
    fullpath,
    resourcename,
    numberofrows
)
values
(
    'the_Path/',
    'a_Resource_Name',
    23
)
""".strip()

        # Act
        sql = add_processed_file(path, resource_name, rows).strip()

        # Assert
        assert sql == expected
