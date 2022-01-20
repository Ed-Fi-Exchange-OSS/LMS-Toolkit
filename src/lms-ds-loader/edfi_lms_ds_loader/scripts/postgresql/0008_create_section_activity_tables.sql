-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.LMSSectionActivity (
    LMSSectionActivityIdentifier INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    LMSUserIdentifier INT NOT NULL,
    LMSSectionIdentifier INT NOT NULL,
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
    CONSTRAINT LMSSectionActivity_PK PRIMARY KEY (
        LMSSectionActivityIdentifier
    )
);

ALTER TABLE lms.LMSSectionActivity ADD CONSTRAINT LMSSectionActivity_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

ALTER TABLE lms.LMSSectionActivity ADD CONSTRAINT FK_LMSSectionActivity_LMSSection FOREIGN KEY (LMSSectionIdentifier)
REFERENCES lms.LMSSection (LMSSectionIdentifier)
ON DELETE CASCADE;

ALTER TABLE lms.LMSSectionActivity ADD CONSTRAINT FK_LMSSectionActivity_LMSUser FOREIGN KEY (LMSUserIdentifier)
REFERENCES lms.LMSUser (LMSUserIdentifier)
ON DELETE CASCADE;

COMMENT ON TABLE lms.LMSSectionActivity IS 'A section activity performed by a user within the instructional system.';
COMMENT ON COLUMN lms.LMSSectionActivity.LMSSectionActivityIdentifier IS 'A unique numeric identifier assigned to the section activity.';
COMMENT ON COLUMN lms.LMSSectionActivity.SourceSystemIdentifier IS 'A unique number or alphanumeric code assigned to a section activity by the source system.';
COMMENT ON COLUMN lms.LMSSectionActivity.SourceSystem IS 'The system code or name providing the user data.';
COMMENT ON COLUMN lms.LMSSectionActivity.LMSUserIdentifier IS 'A unique numeric identifier assigned to the user.';
COMMENT ON COLUMN lms.LMSSectionActivity.LMSSectionIdentifier IS 'A unique numeric identifier assigned to the section.';
COMMENT ON COLUMN lms.LMSSectionActivity.ActivityType IS 'The type of activity. E.g., Discussion Post.';
COMMENT ON COLUMN lms.LMSSectionActivity.ActivityDateTime IS 'The date/time the activity occurred.';
COMMENT ON COLUMN lms.LMSSectionActivity.ActivityStatus IS 'The activity status.';
COMMENT ON COLUMN lms.LMSSectionActivity.ParentSourceSystemIdentifier IS 'The unique identifier assigned to the parent section activity.';
COMMENT ON COLUMN lms.LMSSectionActivity.ActivityTimeInMinutes IS 'The total activity time in minutes.';
COMMENT ON COLUMN lms.LMSSectionActivity.SourceCreateDate IS 'The source system datetime the record was created.';
COMMENT ON COLUMN lms.LMSSectionActivity.SourceLastModifiedDate IS 'The source system datetime the record was last modified.';
COMMENT ON COLUMN lms.LMSSectionActivity.DeletedAt IS 'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''';

CREATE TABLE lms.stg_LMSSectionActivity (
    StagingId INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    LMSUserSourceSystemIdentifier VARCHAR(255) NOT NULL,
    LMSSectionSourceSystemIdentifier VARCHAR(255) NOT NULL,
    ActivityType VARCHAR(60) NOT NULL,
    ActivityDateTime TIMESTAMP NOT NULL,
    ActivityStatus VARCHAR(60) NOT NULL,
    ParentSourceSystemIdentifier VARCHAR(255) NULL,
    ActivityTimeInMinutes INT NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL,
    LastModifiedDate TIMESTAMP NOT NULL,
    CONSTRAINT stg_LMSSectionActivity_PK PRIMARY KEY (
        StagingId
    )
);

CREATE INDEX IX_stg_LMSSectionActivity_Natural_Key ON lms.stg_LMSSectionActivity (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
