-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.AssignmentSubmission (
    AssignmentSubmissionIdentifier INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    AssignmentIdentifier INT NOT NULL,
    LMSUserIdentifier INT NOT NULL,
    SubmissionStatus NVARCHAR(255) NULL,
    SubmissionDateTime DATETIME2 NULL,
    EarnedPoints INT NULL,
    Grade NVARCHAR(20) NULL,
    SourceCreateDate DATETIME2 NULL,
    SourceLastModifiedDate DATETIME2 NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    DeletedAt DATETIME2(7) NULL,
    CONSTRAINT AssignmentSubmission_PK PRIMARY KEY CLUSTERED (
        AssignmentSubmissionIdentifier ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

ALTER TABLE lms.AssignmentSubmission ADD CONSTRAINT AssignmentSubmission_DF_CreateDate DEFAULT (getdate()) FOR CreateDate;
ALTER TABLE lms.AssignmentSubmission ADD CONSTRAINT AssignmentSubmission_DF_LastModifiedDate DEFAULT (getdate()) FOR LastModifiedDate;
ALTER TABLE lms.AssignmentSubmission ADD CONSTRAINT AssignmentSubmission_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

ALTER TABLE lms.AssignmentSubmission WITH CHECK ADD CONSTRAINT FK_AssignmentSubmission_Assignment FOREIGN KEY (AssignmentIdentifier)
REFERENCES lms.Assignment (AssignmentIdentifier)
ON DELETE CASCADE;
ALTER TABLE lms.AssignmentSubmission WITH CHECK ADD CONSTRAINT FK_AssignmentSubmission_User FOREIGN KEY (LMSUserIdentifier)
REFERENCES lms.LMSUser (LMSUserIdentifier)
ON DELETE CASCADE;


EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Submission for an assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the Assignment Submission.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'AssignmentSubmissionIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a user by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the assignment data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'SourceSystem';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'AssignmentIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'LMSUserIdentifier';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The status of the submission.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'SubmissionStatus';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date of the submission.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'SubmissionDateTime';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The grade if graded.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'Grade';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The earned points.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'EarnedPoints';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'SourceCreateDate';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'DeletedAt';

CREATE TABLE lms.stg_AssignmentSubmission (
    StagingId INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    AssignmentSourceSystemIdentifier NVARCHAR(255) NOT NULL,
    LMSUserSourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SubmissionStatus NVARCHAR(255) NULL,
    SubmissionDateTime DATETIME2 NULL,
    EarnedPoints INT NULL,
    Grade NVARCHAR(20) NULL,
    SourceCreateDate DATETIME2 NULL,
    SourceLastModifiedDate DATETIME2 NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    DeletedAt DATETIME2(7) NULL,
    CONSTRAINT stg_AssignmentSubmission_PK PRIMARY KEY CLUSTERED (
        StagingId ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

CREATE INDEX IX_stg_AssignmentSubmission_Natural_Key ON lms.stg_AssignmentSubmission (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
