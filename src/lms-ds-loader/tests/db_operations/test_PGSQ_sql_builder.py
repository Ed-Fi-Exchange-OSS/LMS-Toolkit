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
    soft_delete_from_production_for_section_relation,
    get_processed_files,
    add_processed_file,
)


def describe_when_truncate_stg_table_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "a_table_for_testing"
        expected = f"TRUNCATE TABLE lms.stg_{table} RESTART IDENTITY;".strip()

        # Act
        sql = truncate_stg_table(table).strip()

        # Assert
        assert sql == expected


def describe_when_drop_staging_natural_key_index_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "a_table_for_testing"
        expected = (
            f"DROP INDEX IF EXISTS lms.ix_stg_{table.lower()}_natural_key;".strip()
        )

        # Act
        sql = drop_staging_natural_key_index(table).strip()

        # Assert
        assert sql == expected


def describe_when_recreate_staging_natural_key_index_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "a_table_for_testing"
        expected = f"CREATE INDEX ix_stg_{table}_natural_key ON lms.stg_{table} (SourceSystemIdentifier, SourceSystem, LastModifiedDate);"

        # Act
        sql = recreate_staging_natural_key_index(table)

        # Assert
        assert sql == expected


def describe_when_insert_new_records_to_production_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "a_table_for_testing"
        column_string = "columns"
        expected = f"""
INSERT INTO
    lms.{table}
({column_string}
)
SELECT{column_string}
FROM
    lms.stg_{table} as stg
WHERE
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.{table}
        WHERE
            SourceSystemIdentifier = stg.SourceSystemIdentifier
        AND
            SourceSystem = stg.SourceSystem
    )
""".strip()

        # Act
        sql = insert_new_records_to_production(table, column_string).strip()

        # Assert
        assert sql == expected


def describe_when_insert_new_records_to_production_for_user_relation_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "a_table_for_testing"
        insert_columns = "columns"
        select_columns = "columns2"
        expected = f"""
INSERT INTO
    lms.{table}
(
    LMSUserIdentifier,{insert_columns}
)
SELECT
    LMSUser.LMSUserIdentifier,{select_columns}
FROM
    lms.stg_{table} as stg
INNER JOIN
    lms.LMSUser
ON
    stg.LMSUserSourceSystemIdentifier = LMSUser.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSUser.SourceSystem
WHERE NOT EXISTS (
  SELECT
    1
  FROM
    lms.{table}
  WHERE
    SourceSystemIdentifier = stg.SourceSystemIdentifier
  AND
    SourceSystem = stg.SourceSystem
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
        table = "a_table_for_testing"
        insert_columns = "columns"
        select_columns = "columns2"
        expected = f"""
INSERT INTO
    lms.{table}
(
    LMSSectionIdentifier,{insert_columns}
)
SELECT
    LMSSection.LMSSectionIdentifier,{select_columns}
FROM
    lms.stg_{table} as stg
INNER JOIN
    lms.LMSSection
ON
    stg.LMSSectionSourceSystemIdentifier = LMSSection.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSSection.SourceSystem
WHERE NOT EXISTS (
  SELECT
    1
  FROM
    lms.{table}
  WHERE
    SourceSystemIdentifier = stg.SourceSystemIdentifier
  AND
    SourceSystem = stg.SourceSystem
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
        table = "a_table_for_testing"
        insert_columns = "columns"
        select_columns = "columns2"
        expected = f"""
INSERT INTO
    lms.{table}
(
    LMSSectionIdentifier,
    LMSUserIdentifier,{insert_columns}
)
SELECT
    LMSSection.LMSSectionIdentifier,
    LMSUser.LMSUserIdentifier,{select_columns}
FROM
    lms.stg_{table} as stg
INNER JOIN
    lms.LMSSection
ON
    stg.LMSSectionSourceSystemIdentifier = LMSSection.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSSection.SourceSystem
INNER JOIN
    lms.LMSUser
ON
    stg.LMSUserSourceSystemIdentifier = LMSUser.SourceSystemIdentifier
AND
    stg.SourceSystem = LMSUser.SourceSystem
WHERE NOT EXISTS (
  SELECT
    1
  FROM
    lms.{table}
  WHERE
    SourceSystemIdentifier = stg.SourceSystemIdentifier
  AND
    SourceSystem = stg.SourceSystem
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
        table = "a_table_for_testing"
        update_columns = "columns"
        expected = f"""
UPDATE
    lms.{table}
SET{update_columns}
FROM
    lms.{table} t
INNER JOIN
    lms.stg_{table} as stg
ON
    t.SourceSystem = stg.SourceSystem
AND
    t.SourceSystemIdentifier = stg.SourceSystemIdentifier
AND
    t.LastModifiedDate <> stg.LastModifiedDate
WHERE
    t.SourceSystemIdentifier = lms.{table}.SourceSystemIdentifier
AND
    t.SourceSystem = lms.{table}.SourceSystem
""".strip()

        # Act
        sql = copy_updates_to_production(table, update_columns).strip()

        # Assert
        assert sql == expected


def describe_when_soft_delete_from_production_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "a_table_for_testing"
        source_system = "sourcesystem"
        expected = f"""
UPDATE
    lms.{table}
SET
    DeletedAt = Now()
FROM
    lms.{table} as t
WHERE
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.stg_{table} as stg
        WHERE
            t.SourceSystemIdentifier = stg.SourceSystemIdentifier
        AND
            t.SourceSystem = stg.SourceSystem
    )
AND
    t.DeletedAt IS NULL
AND
    t.SourceSystem = '{source_system}'
AND
    lms.{table}.SourceSystem = t.SourceSystem
AND
    lms.{table}.SourceSystemIdentifier= t.SourceSystemIdentifier
""".strip()

        # Act
        sql = soft_delete_from_production(table, source_system).strip()

        # Assert
        assert sql == expected


def describe_when_soft_delete_from_production_for_section_relation_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        table = "a_table_for_testing"
        source_system = "sourcesystem"
        expected = f"""
UPDATE
    t
SET
    t.DeletedAt = now()
FROM
    lms.{table} as t
WHERE
    t.LMSSectionIdentifier IN (
        SELECT
            s.LMSSectionIdentifier
        FROM
           lms.LMSSection as s
        INNER JOIN
            lms.stg_{table} as stg
        ON
            stg.LMSSectionSourceSystemIdentifier = s.SourceSystemIdentifier
        AND
            stg.SourceSystem = s.SourceSystem
    )
AND
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.stg_{table} as stg
        WHERE
            t.SourceSystemIdentifier = stg.SourceSystemIdentifier
        AND
            t.SourceSystem = stg.SourceSystem
    )
AND
    t.DeletedAt IS NULL
AND
    t.SourceSystem = '{source_system}'
""".strip()

        # Act
        sql = soft_delete_from_production_for_section_relation(
            table, source_system
        ).strip()

        # Assert
        assert sql == expected


def describe_when_get_processed_files_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        resource_name = "a_resource_name"
        expected = f"""
SELECT
    fullpath
FROM
    lms.ProcessedFiles
WHERE
    ResourceName = '{resource_name}'
""".strip()

        # Act
        sql = get_processed_files(resource_name).strip()

        # Assert
        assert sql == expected


def describe_when_add_processed_file_is_called():
    def it_should_return_the_expected_sql():
        # Arrange
        path = "the_path/"
        resource_name = "a_resource_name"
        rows = 23
        expected = f"""
INSERT INTO
    lms.ProcessedFiles
(
    FullPath,
    ResourceName,
    NumberOfRows
)
VALUES
(
    '{path}',
    '{resource_name}',
    {rows}
)
""".strip()

        # Act
        sql = add_processed_file(path, resource_name, rows).strip()

        # Assert
        assert sql == expected
