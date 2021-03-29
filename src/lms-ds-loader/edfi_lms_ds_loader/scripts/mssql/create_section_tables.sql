-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.LMSSection (
    LMSSectionIdentifier INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    SISSectionIdentifier NVARCHAR(255) NULL,
    Title NVARCHAR(255) NOT NULL,
    SectionDescription NVARCHAR(1024) NULL,
    Term NVARCHAR(60) NULL,
    LMSSectionStatus NVARCHAR(60) NULL,
    SourceCreateDate DATETIME2(7) NULL,
    SourceLastModifiedDate DATETIME2(7) NULL,
    Discriminator NVARCHAR(128) NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    DeletedAt DATETIME2(7) NULL,
    CONSTRAINT LMSSection_PK PRIMARY KEY CLUSTERED (
        LMSSectionIdentifier ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

ALTER TABLE lms.LMSSection ADD CONSTRAINT LMSSection_DF_CreateDate DEFAULT (getdate()) FOR CreateDate;
ALTER TABLE lms.LMSSection ADD CONSTRAINT LMSSection_DF_LastModifiedDate DEFAULT (getdate()) FOR LastModifiedDate;
ALTER TABLE lms.LMSSection ADD CONSTRAINT LMSSection_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'An organized grouping of course content and users over a period of time for the purpose of providing instruction.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'LMSSectionIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a user by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the section data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'SourceSystem';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The section identifier defined in the Student Information System (SIS).', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'SISSectionIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The section title or name.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'Title';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The section description.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'SectionDescription';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The enrollment term for the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'Term';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The section status from the source system. E.g., Published, Completed.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'LMSSectionStatus';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'SourceCreateDate';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'DeletedAt';

CREATE TABLE lms.stg_LMSSection (
    StagingId INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    SISSectionIdentifier NVARCHAR(255) NULL,
    Title NVARCHAR(255) NOT NULL,
    SectionDescription NVARCHAR(1024) NULL,
    Term NVARCHAR(60) NULL,
    LMSSectionStatus NVARCHAR(60) NULL,
    SourceCreateDate DATETIME2(7) NULL,
    SourceLastModifiedDate DATETIME2(7) NULL,
    Discriminator NVARCHAR(128) NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    CONSTRAINT stg_LMSSection_PK PRIMARY KEY CLUSTERED (
        StagingId ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

CREATE INDEX IX_stg_LMSSection_Natural_Key ON lms.stg_LMSSection (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
