-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.LMSSystemActivity (
    LMSSystemActivityIdentifier INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    LMSUserIdentifier INT NOT NULL,
    ActivityType NVARCHAR(60) NOT NULL,
    ActivityDateTime DATETIME2(7) NOT NULL,
    ActivityStatus NVARCHAR(60) NOT NULL,
    ParentSourceSystemIdentifier NVARCHAR(255) NULL,
    ActivityTimeInMinutes INT NULL,
    SourceCreateDate DATETIME2(7) NULL,
    SourceLastModifiedDate DATETIME2(7) NULL,
    DeletedAt DATETIME2(7) NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    CONSTRAINT LMSSystemActivity_PK PRIMARY KEY CLUSTERED (
        LMSSystemActivityIdentifier ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

ALTER TABLE lms.LMSSystemActivity ADD CONSTRAINT LMSSystemActivity_DF_CreateDate DEFAULT (getdate()) FOR CreateDate;
ALTER TABLE lms.LMSSystemActivity ADD CONSTRAINT LMSSystemActivity_DF_LastModifiedDate DEFAULT (getdate()) FOR LastModifiedDate;
ALTER TABLE lms.LMSSystemActivity ADD CONSTRAINT LMSSystemActivity_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

ALTER TABLE lms.LMSSystemActivity WITH CHECK ADD CONSTRAINT FK_LMSSystemActivity_LMSUser FOREIGN KEY (LMSUserIdentifier)
REFERENCES lms.LMSUser (LMSUserIdentifier)
ON DELETE CASCADE;

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A system activity performed by a user within the instructional system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the system activity.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'LMSSystemActivityIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a system activity by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the user data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'SourceSystem';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'LMSUserIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The type of activity. E.g., Discussion Post.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'ActivityType';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date/time the activity occurred.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'ActivityDateTime';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The activity status.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'ActivityStatus';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The unique identifier assigned to the parent system activity.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'ParentSourceSystemIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The total activity time in minutes.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'ActivityTimeInMinutes';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'SourceCreateDate';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'DeletedAt';

CREATE TABLE lms.stg_LMSSystemActivity (
    StagingId INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    LMSUserSourceSystemIdentifier NVARCHAR(255) NOT NULL,
    ActivityType NVARCHAR(60) NOT NULL,
    ActivityDateTime DATETIME2(7) NOT NULL,
    ActivityStatus NVARCHAR(60) NOT NULL,
    ParentSourceSystemIdentifier NVARCHAR(255) NULL,
    ActivityTimeInMinutes INT NULL,
    SourceCreateDate DATETIME2(7) NULL,
    SourceLastModifiedDate DATETIME2(7) NULL,
    DeletedAt DATETIME2(7) NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    CONSTRAINT stg_LMSSystemActivity_PK PRIMARY KEY CLUSTERED (
        StagingId ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

CREATE INDEX IX_stg_LMSSystemActivity_Natural_Key ON lms.stg_LMSSystemActivity (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
