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
    StartDateTime TIMESTAMP(7) NULL,
    EndDateTime TIMESTAMP(7) NULL,
    DueDateTime TIMESTAMP(7) NULL,
    MaxPoints INT NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL DEFAULT now(),
    LastModifiedDate TIMESTAMP NOT NULL DEFAULT now(),
    DeletedAt TIMESTAMP(7) NULL,
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
    StartDateTime TIMESTAMP(7) NULL,
    EndDateTime TIMESTAMP(7) NULL,
    DueDateTime TIMESTAMP(7) NULL,
    MaxPoints INT NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL,
    LastModifiedDate TIMESTAMP NOT NULL,
    CONSTRAINT stg_Assignment_PK PRIMARY KEY (StagingId)
);

CREATE INDEX IX_stg_Assignment_Natural_Key ON lms.stg_Assignment (SourceSystemIdentifier, SourceSystem, LastModifiedDate);


-- Table lms.AssignmentSubmissionType --

CREATE TABLE lms.AssignmentSubmissionType (
    AssignmentIdentifier INT NOT NULL,
    SubmissionType VARCHAR(60) NOT NULL,
    CreateDate TIMESTAMP NOT NULL,
    DeletedAt TIMESTAMP(7) NULL,
    CONSTRAINT AssignmentSubmissionType_PK PRIMARY KEY (
        AssignmentIdentifier,
        SubmissionType
    )
);

ALTER TABLE lms.AssignmentSubmissionType ADD CONSTRAINT AssignmentSubmissionType_DF_CreateDate DEFAULT (getdate()) FOR CreateDate;


ALTER TABLE lms.AssignmentSubmissionType WITH CHECK ADD CONSTRAINT FK_AssignmentSubmissionType_Assignment FOREIGN KEY (AssignmentIdentifier)
REFERENCES lms.Assignment (AssignmentIdentifier)
ON DELETE CASCADE;

CREATE NONCLUSTERED INDEX FK_AssignmentSubmissionType_Assignment
ON lms.AssignmentSubmissionType (AssignmentIdentifier);


CREATE TABLE lms.stg_AssignmentSubmissionType (
    StagingId INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    SubmissionType VARCHAR(60) NOT NULL,
    CreateDate TIMESTAMP NOT NULL,
    CONSTRAINT stg_AssignmentSubmissionType_PK PRIMARY KEY (
        StagingId
    )
);

CREATE INDEX IX_stg_AssignmentSubmissionType_Natural_Key ON lms.stg_AssignmentSubmissionType (SourceSystemIdentifier, SourceSystem);
