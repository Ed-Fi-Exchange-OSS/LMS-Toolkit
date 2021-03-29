-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.LMSUserLMSSectionAssociation (
    LMSSectionIdentifier INT NOT NULL,
    LMSUserIdentifier INT NOT NULL,
    LMSUserLMSSectionAssociationIdentifier INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    EnrollmentStatus NVARCHAR(60) NOT NULL,
    StartDate DATETIME2(7) NULL,
    EndDate DATETIME2(7) NULL,
    SourceCreateDate DATETIME2(7) NULL,
    SourceLastModifiedDate DATETIME2(7) NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    DeletedAt DATETIME2(7) NULL,
    CONSTRAINT LMSUserLMSSectionAssociation_PK PRIMARY KEY CLUSTERED (
        LMSUserLMSSectionAssociationIdentifier ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

ALTER TABLE lms.LMSUserLMSSectionAssociation ADD CONSTRAINT LMSUserLMSSectionAssociation_DF_CreateDate DEFAULT (getdate()) FOR CreateDate;
ALTER TABLE lms.LMSUserLMSSectionAssociation ADD CONSTRAINT LMSUserLMSSectionAssociation_DF_LastModifiedDate DEFAULT (getdate()) FOR LastModifiedDate;
ALTER TABLE lms.LMSUserLMSSectionAssociation ADD CONSTRAINT LMSUserLMSSectionAssociation_DF_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

ALTER TABLE lms.LMSUserLMSSectionAssociation WITH CHECK ADD CONSTRAINT FK_LMSUserLMSSectionAssociation_LMSSection FOREIGN KEY (LMSSectionIdentifier)
REFERENCES lms.LMSSection (LMSSectionIdentifier)
ON DELETE CASCADE;
ALTER TABLE lms.LMSUserLMSSectionAssociation WITH CHECK ADD CONSTRAINT FK_LMSUserLMSSectionAssociation_LMSUser FOREIGN KEY (LMSUserIdentifier)
REFERENCES lms.LMSUser (LMSUserIdentifier)
ON DELETE CASCADE;

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The association of a user and section. For a student, this would be a section enrollment. For a teacher, this would be a section assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'LMSSectionIdentifier'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'LMSUserIdentifier'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user section association.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'LMSUserLMSSectionAssociationIdentifier'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a user by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the user data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'SourceSystem'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The status of the user section association. E.g., Active, Inactive, Withdrawn.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'EnrollmentStatus'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Month, day, and year of the user''s entry or assignment to the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'StartDate'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Month, day, and year of the user''s withdrawal or exit from the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'EndDate'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'SourceCreateDate'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'DeletedAt';

CREATE TABLE lms.stg_LMSUserLMSSectionAssociation (
    StagingId INT NOT NULL IDENTITY,
    LMSSectionSourceSystemIdentifier NVARCHAR(255) NOT NULL,
    LMSUserSourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    EnrollmentStatus NVARCHAR(60) NOT NULL,
    StartDate DATETIME2(7) NULL,
    EndDate DATETIME2(7) NULL,
    SourceCreateDate DATETIME2(7) NULL,
    SourceLastModifiedDate DATETIME2(7) NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    CONSTRAINT stg_LMSUserLMSSectionAssociation_PK PRIMARY KEY CLUSTERED (
        StagingId ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

CREATE INDEX IX_stg_LMSUserLMSSectionAssociation_Natural_Key ON lms.stg_LMSUserLMSSectionAssociation (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
