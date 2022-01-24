# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.


def truncate_stg_table(table: str) -> str:
    return f"TRUNCATE TABLE lms.stg_{table};"


def disable_staging_natural_key_index(table: str) -> str:
    return f"ALTER INDEX IX_stg_{table}_Natural_Key on lms.stg_{table} DISABLE;"


def enable_staging_natural_key_index(table: str) -> str:
    return f"ALTER INDEX IX_stg_{table}_Natural_Key on lms.stg_{table} REBUILD;"


def insert_new_records_to_production(table: str, column_string: str) -> str:
    return f"""
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
"""


def insert_new_records_to_production_for_user_relation(
    table: str, insert_columns: str, select_columns: str
) -> str:
    return f"""
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
"""


def insert_new_records_to_production_for_section_relation(
    table: str, insert_columns: str, select_columns: str
) -> str:
    return f"""
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
"""


def insert_new_records_to_production_for_section_and_user_relation(
    table: str, insert_columns: str, select_columns: str
) -> str:
    return f"""
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
"""


def insert_new_records_to_production_for_assignment_and_user_relation(
    table: str, insert_columns: str, select_columns: str
) -> str:
    return f"""
INSERT INTO
    lms.{table}
(
    AssignmentIdentifier,
    LMSUserIdentifier,{insert_columns}
)
SELECT
    Assignment.AssignmentIdentifier,
    LMSUser.LMSUserIdentifier,{select_columns}
FROM
    lms.stg_{table} as stg
INNER JOIN
    lms.Assignment
ON
    stg.AssignmentSourceSystemIdentifier = Assignment.SourceSystemIdentifier
AND
    stg.SourceSystem = Assignment.SourceSystem
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
"""


def insert_new_records_to_production_for_attendance_events(
    insert_columns: str, select_columns: str
) -> str:
    return f"""
INSERT INTO
    lms.LMSUserAttendanceEvent
(
    LMSSectionIdentifier,
    LMSUserIdentifier,
    LMSUserLMSSectionAssociationIdentifier,{insert_columns}
)
SELECT
    LMSSection.LMSSectionIdentifier,
    LMSUser.LMSUserIdentifier,
    LMSUserLMSSectionAssociation.LMSUserLMSSectionAssociationIdentifier,{select_columns}
FROM
    lms.stg_LMSUserAttendanceEvent as stg
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
INNER JOIN
    lms.LMSUserLMSSectionAssociation
ON
    LMSUser.LMSUserIdentifier = LMSUserLMSSectionAssociation.LMSUserIdentifier
AND
    LMSSection.LMSSectionIdentifier = LMSUserLMSSectionAssociation.LMSSectionIdentifier
WHERE NOT EXISTS (
  SELECT
    1
  FROM
    lms.LMSUserAttendanceEvent
  WHERE
    SourceSystemIdentifier = stg.SourceSystemIdentifier
  AND
    SourceSystem = stg.SourceSystem
)
"""


def copy_updates_to_production(table: str, update_columns: str) -> str:
    return f"""
UPDATE
    t
SET{update_columns}
FROM
    lms.{table} as t
INNER JOIN
    lms.stg_{table} as stg
ON
    t.SourceSystem = stg.SourceSystem
AND
    t.SourceSystemIdentifier = stg.SourceSystemIdentifier
AND
    t.LastModifiedDate <> stg.LastModifiedDate
"""


def soft_delete_from_production(table: str, source_system: str) -> str:
    return f"""
UPDATE
    t
SET
    t.DeletedAt = getdate()
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
"""


def soft_delete_from_production_for_section_relation(
    table: str, source_system: str
) -> str:
    return f"""
UPDATE
    t
SET
    t.DeletedAt = getdate()
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
"""


def soft_delete_from_production_for_assignment_relation(
    table: str, source_system: str
) -> str:
    return f"""
UPDATE
    t
SET
    t.DeletedAt = getdate()
FROM
    lms.{table} as t
WHERE
    t.AssignmentIdentifier IN (
        SELECT
            a.AssignmentIdentifier
        FROM
           lms.Assignment as a
        INNER JOIN
            lms.stg_{table} as stg
        ON
            stg.AssignmentSourceSystemIdentifier = a.SourceSystemIdentifier
        AND
            stg.SourceSystem = a.SourceSystem
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
"""


def insert_new_submission_types() -> str:
    return """
INSERT INTO lms.AssignmentSubmissionType (
    AssignmentIdentifier,
    SubmissionType
)
SELECT
    lms.Assignment.AssignmentIdentifier,
    lms.stg_AssignmentSubmissionType.SubmissionType
FROM
    lms.stg_AssignmentSubmissionType
    INNER JOIN
        lms.Assignment
    ON
        lms.stg_AssignmentSubmissionType.SourceSystem = lms.Assignment.SourceSystem
    AND
        lms.stg_AssignmentSubmissionType.SourceSystemIdentifier = lms.Assignment.SourceSystemIdentifier
WHERE
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.AssignmentSubmissionType
        WHERE
            AssignmentIdentifier = lms.Assignment.AssignmentIdentifier
        AND
            SubmissionType = lms.stg_AssignmentSubmissionType.SubmissionType
    )
"""


def soft_delete_removed_submission_types(source_system: str) -> str:
    return f"""
UPDATE
    AssignmentSubmissionType
SET
    DeletedAt = GETDATE()
FROM
    lms.AssignmentSubmissionType
INNER JOIN
    lms.Assignment
ON
    lms.AssignmentSubmissionType.AssignmentIdentifier = lms.Assignment.AssignmentIdentifier
WHERE
    SourceSystem = '{source_system}'
AND
    NOT EXISTS (
        SELECT
            1
        FROM
            lms.stg_AssignmentSubmissionType
        WHERE
            stg_AssignmentSubmissionType.SourceSystem = Assignment.SourceSystem
        AND
            stg_AssignmentSubmissionType.SourceSystemIdentifier = Assignment.SourceSystemIdentifier
        AND
            stg_AssignmentSubmissionType.SubmissionType = AssignmentSubmissionType.SubmissionType
    )
"""


def unsoft_delete_returned_submission_types(source_system: str) -> str:
    return f"""
UPDATE
    AssignmentSubmissionType
SET
    DeletedAt = NULL
FROM
    lms.AssignmentSubmissionType
INNER JOIN
    lms.Assignment
ON
    lms.AssignmentSubmissionType.AssignmentIdentifier = lms.Assignment.AssignmentIdentifier
WHERE
    SourceSystem = '{source_system}'
AND
    EXISTS (
        SELECT
            1
        FROM
            lms.stg_AssignmentSubmissionType
        WHERE
            lms.stg_AssignmentSubmissionType.SourceSystem = lms.Assignment.SourceSystem
        AND
            lms.stg_AssignmentSubmissionType.SourceSystemIdentifier = lms.Assignment.SourceSystemIdentifier
        AND
            lms.stg_AssignmentSubmissionType.SubmissionType = lms.AssignmentSubmissionType.SubmissionType
    )
"""


def get_processed_files(resource_name: str) -> str:
    return f"""
SELECT
    FullPath
FROM
    lms.ProcessedFiles
WHERE
    ResourceName = '{resource_name}'
"""


def add_processed_file(path: str, resource_name: str, rows: int) -> str:
    return f"""
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
"""
