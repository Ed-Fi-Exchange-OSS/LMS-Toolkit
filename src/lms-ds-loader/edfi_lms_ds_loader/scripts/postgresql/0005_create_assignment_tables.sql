-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.



CREATE TABLE lms.Assignment (
    AssignmentIdentifier INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    LMSSectionIdentifier INT NOT NULL,
    Title VARCHAR(255) NOT NULL,
    AssignmentCategory VARCHAR(60) NOT NULL,
    AssignmentDescription VARCHAR(1024) NULL,
    StartDateTime TIMESTAMP NULL,
    EndDateTime TIMESTAMP NULL,
    DueDateTime TIMESTAMP NULL,
    MaxPoints INT NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL DEFAULT now(),
    LastModifiedDate TIMESTAMP NOT NULL DEFAULT now(),
    DeletedAt TIMESTAMP NULL,
    CONSTRAINT Assignment_PK PRIMARY KEY (
        AssignmentIdentifier
    )
);

ALTER TABLE lms.Assignment ADD CONSTRAINT Assignment_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

ALTER TABLE lms.Assignment ADD CONSTRAINT FK_Assignment_LMSSection FOREIGN KEY (LMSSectionIdentifier)
REFERENCES lms.LMSSection (LMSSectionIdentifier)
ON DELETE CASCADE;


CREATE TABLE lms.stg_Assignment (
    StagingId INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    LMSSectionSourceSystemIdentifier VARCHAR(255) NOT NULL,
    Title VARCHAR(255) NOT NULL,
    AssignmentCategory VARCHAR(60) NOT NULL,
    AssignmentDescription VARCHAR(1024) NULL,
    StartDateTime TIMESTAMP NULL,
    EndDateTime TIMESTAMP NULL,
    DueDateTime TIMESTAMP NULL,
    MaxPoints INT NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL DEFAULT (now()),
    LastModifiedDate TIMESTAMP NOT NULL DEFAULT (now()),
    CONSTRAINT stg_Assignment_PK PRIMARY KEY (StagingId)
);

CREATE INDEX IX_stg_Assignment_Natural_Key ON lms.stg_Assignment (SourceSystemIdentifier, SourceSystem, LastModifiedDate);

COMMENT ON TABLE lms.Assignment IS 'Course work assigned to students enrolled in a section.';
COMMENT ON COLUMN lms.Assignment.AssignmentIdentifier IS 'A unique numeric identifier assigned to the assignment.';
COMMENT ON COLUMN lms.Assignment.SourceSystemIdentifier IS 'A unique number or alphanumeric code assigned to a user by the source system.';
COMMENT ON COLUMN lms.Assignment.SourceSystem IS 'The system code or name providing the assignment data.';
COMMENT ON COLUMN lms.Assignment.LMSSectionIdentifier IS 'A unique numeric identifier assigned to the section.';
COMMENT ON COLUMN lms.Assignment.Title IS 'The assignment title or name.';
COMMENT ON COLUMN lms.Assignment.AssignmentCategory IS 'The category or type of assignment.';
COMMENT ON COLUMN lms.Assignment.AssignmentDescription IS 'The assignment description.';
COMMENT ON COLUMN lms.Assignment.StartDateTime IS 'The start date and time for the assignment. Students will have access to the assignment after this date.';
COMMENT ON COLUMN lms.Assignment.EndDateTime IS 'The end date and time for the assignment. Students will no longer have access to the assignment after this date.';
COMMENT ON COLUMN lms.Assignment.DueDateTime IS 'The date and time the assignment is due.';
COMMENT ON COLUMN lms.Assignment.MaxPoints IS 'The maximum number of points a student may receive for a submission of the assignment.';
COMMENT ON COLUMN lms.Assignment.SourceCreateDate IS 'The source system datetime the record was created.';
COMMENT ON COLUMN lms.Assignment.SourceLastModifiedDate IS 'The source system datetime the record was last modified.';
COMMENT ON COLUMN lms.Assignment.DeletedAt IS 'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''';


-- Table lms.AssignmentSubmissionType --

CREATE TABLE lms.AssignmentSubmissionType (
    AssignmentIdentifier INT NOT NULL,
    SubmissionType VARCHAR(60) NOT NULL,
    CreateDate TIMESTAMP NOT NULL DEFAULT (now()),
    DeletedAt TIMESTAMP NULL,
    CONSTRAINT AssignmentSubmissionType_PK PRIMARY KEY (
        AssignmentIdentifier,
        SubmissionType
    )
);

ALTER TABLE lms.AssignmentSubmissionType ADD CONSTRAINT FK_AssignmentSubmissionType_Assignment FOREIGN KEY (AssignmentIdentifier)
REFERENCES lms.Assignment (AssignmentIdentifier)
ON DELETE CASCADE;

CREATE INDEX FK_AssignmentSubmissionType_Assignment
ON lms.AssignmentSubmissionType (AssignmentIdentifier);

COMMENT ON TABLE lms.AssignmentSubmissionType IS 'The type(s) of submissions available for the assignment.';
COMMENT ON COLUMN lms.AssignmentSubmissionType.AssignmentIdentifier IS 'A unique numeric identifier assigned to the assignment.';
COMMENT ON COLUMN lms.AssignmentSubmissionType.SubmissionType IS 'The type(s) of submissions available for the assignment.';


CREATE TABLE lms.stg_AssignmentSubmissionType (
    StagingId INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    SubmissionType VARCHAR(60) NOT NULL,
    CreateDate TIMESTAMP NOT NULL DEFAULT (now()),
    CONSTRAINT stg_AssignmentSubmissionType_PK PRIMARY KEY (
        StagingId
    )
);

CREATE INDEX IX_stg_AssignmentSubmissionType_Natural_Key ON lms.stg_AssignmentSubmissionType (SourceSystemIdentifier, SourceSystem);
