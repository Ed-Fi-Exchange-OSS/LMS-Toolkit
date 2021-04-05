-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.Assignment (
    AssignmentIdentifier INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    LMSSectionIdentifier INT NOT NULL,
    Title NVARCHAR(255) NOT NULL,
    AssignmentCategory NVARCHAR(60) NOT NULL,
    AssignmentDescription NVARCHAR(1024) NULL,
    StartDateTime DATETIME2(7) NULL,
    EndDateTime DATETIME2(7) NULL,
    DueDateTime DATETIME2(7) NULL,
    MaxPoints INT NULL,
    SourceCreateDate DATETIME2 NULL,
    SourceLastModifiedDate DATETIME2 NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    DeletedAt DATETIME2(7) NULL,
    CONSTRAINT Assignment_PK PRIMARY KEY CLUSTERED (
        AssignmentIdentifier ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

ALTER TABLE lms.Assignment ADD CONSTRAINT Assignment_DF_CreateDate DEFAULT (getdate()) FOR CreateDate;
ALTER TABLE lms.Assignment ADD CONSTRAINT Assignment_DF_LastModifiedDate DEFAULT (getdate()) FOR LastModifiedDate;
ALTER TABLE lms.Assignment ADD CONSTRAINT Assignment_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

ALTER TABLE lms.Assignment WITH CHECK ADD CONSTRAINT FK_Assignment_LMSSection FOREIGN KEY (LMSSectionIdentifier)
REFERENCES lms.LMSSection (LMSSectionIdentifier)
ON DELETE CASCADE;


EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Course work assigned to students enrolled in a section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'AssignmentIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a user by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the assignment data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'SourceSystem';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'LMSSectionIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The assignment title or name.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'Title';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The category or type of assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'AssignmentCategory';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The assignment description.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'AssignmentDescription';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The start date and time for the assignment. Students will have access to the assignment after this date.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'StartDateTime';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The end date and time for the assignment. Students will no longer have access to the assignment after this date.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'EndDateTime';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time the assignment is due.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'DueDateTime';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The maximum number of points a student may receive for a submission of the assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'MaxPoints';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'SourceCreateDate';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'DeletedAt';

CREATE TABLE lms.stg_Assignment (
    StagingId INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    LMSSectionSourceSystemIdentifier NVARCHAR(255) NOT NULL,
    Title NVARCHAR(255) NOT NULL,
    AssignmentCategory NVARCHAR(60) NOT NULL,
    AssignmentDescription NVARCHAR(1024) NULL,
    StartDateTime DATETIME2(7) NULL,
    EndDateTime DATETIME2(7) NULL,
    DueDateTime DATETIME2(7) NULL,
    MaxPoints INT NULL,
    SourceCreateDate DATETIME2 NULL,
    SourceLastModifiedDate DATETIME2 NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    CONSTRAINT stg_Assignment_PK PRIMARY KEY CLUSTERED (
        StagingId ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

CREATE INDEX IX_stg_Assignment_Natural_Key ON lms.stg_Assignment (SourceSystemIdentifier, SourceSystem, LastModifiedDate);


-- Table lms.AssignmentSubmissionType --

CREATE TABLE lms.AssignmentSubmissionType (
    AssignmentIdentifier INT NOT NULL,
    SubmissionType NVARCHAR(60) NOT NULL,
    CreateDate DATETIME2 NOT NULL,
    DeletedAt DATETIME2(7) NULL,
    CONSTRAINT AssignmentSubmissionType_PK PRIMARY KEY CLUSTERED (
        AssignmentIdentifier ASC,
        SubmissionType ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

ALTER TABLE lms.AssignmentSubmissionType ADD CONSTRAINT AssignmentSubmissionType_DF_CreateDate DEFAULT (getdate()) FOR CreateDate;


ALTER TABLE lms.AssignmentSubmissionType WITH CHECK ADD CONSTRAINT FK_AssignmentSubmissionType_Assignment FOREIGN KEY (AssignmentIdentifier)
REFERENCES lms.Assignment (AssignmentIdentifier)
ON DELETE CASCADE;

CREATE NONCLUSTERED INDEX FK_AssignmentSubmissionType_Assignment
ON lms.AssignmentSubmissionType (AssignmentIdentifier ASC);

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The type(s) of submissions available for the assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmissionType';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmissionType', @level2type=N'COLUMN', @level2name=N'AssignmentIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The type(s) of submissions available for the assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmissionType', @level2type=N'COLUMN', @level2name=N'SubmissionType';


CREATE TABLE lms.stg_AssignmentSubmissionType (
    StagingId INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    SubmissionType NVARCHAR(60) NOT NULL,
    CreateDate DATETIME2 NOT NULL,
    CONSTRAINT stg_AssignmentSubmissionType_PK PRIMARY KEY CLUSTERED (
        StagingId ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

CREATE INDEX IX_stg_AssignmentSubmissionType_Natural_Key ON lms.stg_AssignmentSubmissionType (SourceSystemIdentifier, SourceSystem);
