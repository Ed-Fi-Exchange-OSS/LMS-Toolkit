-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.AssignmentSubmission (
    AssignmentSubmissionIdentifier INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    AssignmentIdentifier INT NOT NULL,
    LMSUserIdentifier INT NOT NULL,
    SubmissionStatus VARCHAR(255) NULL,
    SubmissionDateTime TIMESTAMP NULL,
    EarnedPoints INT NULL,
    Grade VARCHAR(20) NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL DEFAULT (now()),
    LastModifiedDate TIMESTAMP NOT NULL DEFAULT (now()),
    DeletedAt TIMESTAMP NULL,
    CONSTRAINT AssignmentSubmission_PK PRIMARY KEY (
        AssignmentSubmissionIdentifier
    )
);

ALTER TABLE lms.AssignmentSubmission ADD CONSTRAINT AssignmentSubmission_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

ALTER TABLE lms.AssignmentSubmission ADD CONSTRAINT FK_AssignmentSubmission_Assignment FOREIGN KEY (AssignmentIdentifier)
REFERENCES lms.Assignment (AssignmentIdentifier)
ON DELETE CASCADE;

ALTER TABLE lms.AssignmentSubmission ADD CONSTRAINT FK_AssignmentSubmission_User FOREIGN KEY (LMSUserIdentifier)
REFERENCES lms.LMSUser (LMSUserIdentifier)
ON DELETE CASCADE;


COMMENT ON TABLE lms.AssignmentSubmission IS 'Submission for an assignment.';
COMMENT ON COLUMN lms.AssignmentSubmission.AssignmentSubmissionIdentifier IS 'A unique numeric identifier assigned to the Assignment Submission.';
COMMENT ON COLUMN lms.AssignmentSubmission.SourceSystemIdentifier IS 'A unique number or alphanumeric code assigned to a user by the source system.';
COMMENT ON COLUMN lms.AssignmentSubmission.SourceSystem IS 'The system code or name providing the assignment data.';
COMMENT ON COLUMN lms.AssignmentSubmission.AssignmentIdentifier IS 'A unique numeric identifier assigned to the assignment.';
COMMENT ON COLUMN lms.AssignmentSubmission.LMSUserIdentifier IS 'A unique numeric identifier assigned to the user.';
COMMENT ON COLUMN lms.AssignmentSubmission.SubmissionStatus IS 'The status of the submission.';
COMMENT ON COLUMN lms.AssignmentSubmission.SubmissionDateTime IS 'The date of the submission.';
COMMENT ON COLUMN lms.AssignmentSubmission.Grade IS 'The grade if graded.';
COMMENT ON COLUMN lms.AssignmentSubmission.EarnedPoints IS 'The earned points.';
COMMENT ON COLUMN lms.AssignmentSubmission.SourceCreateDate IS 'The source system datetime the record was created.';
COMMENT ON COLUMN lms.AssignmentSubmission.SourceLastModifiedDate IS 'The source system datetime the record was last modified.';
COMMENT ON COLUMN lms.AssignmentSubmission.DeletedAt IS 'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''';

CREATE TABLE lms.stg_AssignmentSubmission (
    StagingId INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    AssignmentSourceSystemIdentifier VARCHAR(255) NOT NULL,
    LMSUserSourceSystemIdentifier VARCHAR(255) NOT NULL,
    SubmissionStatus VARCHAR(255) NULL,
    SubmissionDateTime TIMESTAMP NULL,
    EarnedPoints INT NULL,
    Grade VARCHAR(20) NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL,
    LastModifiedDate TIMESTAMP NOT NULL,
    CONSTRAINT stg_AssignmentSubmission_PK PRIMARY KEY (
        StagingId
    )
);

CREATE INDEX IX_stg_AssignmentSubmission_Natural_Key ON lms.stg_AssignmentSubmission (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
