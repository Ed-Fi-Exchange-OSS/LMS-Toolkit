-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.LMSSystemActivity (
    LMSSystemActivityIdentifier INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    LMSUserIdentifier INT NOT NULL,
    ActivityType VARCHAR(60) NOT NULL,
    ActivityDateTime TIMESTAMP NOT NULL,
    ActivityStatus VARCHAR(60) NOT NULL,
    ParentSourceSystemIdentifier VARCHAR(255) NULL,
    ActivityTimeInMinutes INT NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    DeletedAt TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL DEFAULT (now()),
    LastModifiedDate TIMESTAMP NOT NULL DEFAULT (now()),
    CONSTRAINT LMSSystemActivity_PK PRIMARY KEY (
        LMSSystemActivityIdentifier
    )
);

ALTER TABLE lms.LMSSystemActivity ADD CONSTRAINT LMSSystemActivity_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

ALTER TABLE lms.LMSSystemActivity ADD CONSTRAINT FK_LMSSystemActivity_LMSUser FOREIGN KEY (LMSUserIdentifier)
REFERENCES lms.LMSUser (LMSUserIdentifier)
ON DELETE CASCADE;

COMMENT ON TABLE lms.LMSSystemActivity IS 'A system activity performed by a user within the instructional system.';
COMMENT ON COLUMN lms.LMSSystemActivity.LMSSystemActivityIdentifier IS 'A unique numeric identifier assigned to the system activity.';
COMMENT ON COLUMN lms.LMSSystemActivity.SourceSystemIdentifier IS 'A unique number or alphanumeric code assigned to a system activity by the source system.';
COMMENT ON COLUMN lms.LMSSystemActivity.SourceSystem IS 'The system code or name providing the user data.';
COMMENT ON COLUMN lms.LMSSystemActivity.LMSUserIdentifier IS 'A unique numeric identifier assigned to the user.';
COMMENT ON COLUMN lms.LMSSystemActivity.ActivityType IS 'The type of activity. E.g., Discussion Post.';
COMMENT ON COLUMN lms.LMSSystemActivity.ActivityDateTime IS 'The date/time the activity occurred.';
COMMENT ON COLUMN lms.LMSSystemActivity.ActivityStatus IS 'The activity status.';
COMMENT ON COLUMN lms.LMSSystemActivity.ParentSourceSystemIdentifier IS 'The unique identifier assigned to the parent system activity.';
COMMENT ON COLUMN lms.LMSSystemActivity.ActivityTimeInMinutes IS 'The total activity time in minutes.';
COMMENT ON COLUMN lms.LMSSystemActivity.SourceCreateDate IS 'The source system datetime the record was created.';
COMMENT ON COLUMN lms.LMSSystemActivity.SourceLastModifiedDate IS 'The source system datetime the record was last modified.';
COMMENT ON COLUMN lms.LMSSystemActivity.DeletedAt IS 'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.';

CREATE TABLE lms.stg_LMSSystemActivity (
    StagingId INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    LMSUserSourceSystemIdentifier VARCHAR(255) NOT NULL,
    ActivityType VARCHAR(60) NOT NULL,
    ActivityDateTime TIMESTAMP NOT NULL,
    ActivityStatus VARCHAR(60) NOT NULL,
    ParentSourceSystemIdentifier VARCHAR(255) NULL,
    ActivityTimeInMinutes INT NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL,
    LastModifiedDate TIMESTAMP NOT NULL,
    CONSTRAINT stg_LMSSystemActivity_PK PRIMARY KEY (
        StagingId
    )
);

CREATE INDEX IX_stg_LMSSystemActivity_Natural_Key ON lms.stg_LMSSystemActivity (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
