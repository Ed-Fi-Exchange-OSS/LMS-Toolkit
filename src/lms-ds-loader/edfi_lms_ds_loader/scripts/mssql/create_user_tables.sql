-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.LMSUser (
    LMSUserIdentifier INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    UserRole NVARCHAR(60) NOT NULL,
    SISUserIdentifier NVARCHAR(255) NULL,
    LocalUserIdentifier NVARCHAR(255) NULL,
    [Name] NVARCHAR(255) NOT NULL,
    EmailAddress NVARCHAR(255) NOT NULL,
    SourceCreateDate DATETIME2(7) NULL,
    SourceLastModifiedDate DATETIME2(7) NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    DeletedAt DATETIME2(7) NULL,
    CONSTRAINT LMSUser_PK PRIMARY KEY CLUSTERED (
        LMSUserIdentifier ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

ALTER TABLE lms.LMSUser ADD CONSTRAINT LMSUser_DF_CreateDate DEFAULT (getdate()) FOR CreateDate;

ALTER TABLE lms.LMSUser ADD CONSTRAINT LMSUser_DF_LastModifiedDate DEFAULT (getdate()) FOR LastModifiedDate;

ALTER TABLE lms.LMSUser ADD CONSTRAINT UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);




CREATE TABLE lms.stg_LMSUser (
    StagingId INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    UserRole NVARCHAR(60) NOT NULL,
    SISUserIdentifier NVARCHAR(255) NULL,
    LocalUserIdentifier NVARCHAR(255) NULL,
    [Name] NVARCHAR(255) NOT NULL,
    EmailAddress NVARCHAR(255) NOT NULL,
    SourceCreateDate DATETIME2(7) NULL,
    SourceLastModifiedDate DATETIME2(7) NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    CONSTRAINT stg_LMSUser_PK PRIMARY KEY CLUSTERED (
        StagingId ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

CREATE INDEX IX_stg_LMSUser_Natural_Key ON lms.stg_LMSUser (SourceSystemIdentifier, SourceSystem, LastModifiedDate);

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A person using the instructional system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'LMSUserIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a user by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the user data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'SourceSystem';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The role assigned to the user. E.g., Student, Teacher, Administrator.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'UserRole';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The user identifier defined in the Student Information System (SIS).', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'SISUserIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The user identifier assigned by a school or district.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'LocalUserIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The full name of the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'Name';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The primary e-mail address for the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'EmailAddress';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'SourceCreateDate';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'DeletedAt';
