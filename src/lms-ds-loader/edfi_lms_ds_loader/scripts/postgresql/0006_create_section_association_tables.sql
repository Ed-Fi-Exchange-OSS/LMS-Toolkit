-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.LMSUserLMSSectionAssociation (
    LMSUserLMSSectionAssociationIdentifier INT GENERATED ALWAYS AS IDENTITY,
    LMSSectionIdentifier INT NOT NULL,
    LMSUserIdentifier INT NOT NULL,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    EnrollmentStatus VARCHAR(60) NOT NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL DEFAULT (now()),
    LastModifiedDate TIMESTAMP NOT NULL DEFAULT (now()),
    DeletedAt TIMESTAMP NULL,
    CONSTRAINT LMSUserLMSSectionAssociation_PK PRIMARY KEY (
        LMSUserLMSSectionAssociationIdentifier
    )
);

ALTER TABLE lms.LMSUserLMSSectionAssociation ADD CONSTRAINT LMSUserLMSSectionAssociation_DF_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

ALTER TABLE lms.LMSUserLMSSectionAssociation ADD CONSTRAINT FK_LMSUserLMSSectionAssociation_LMSSection FOREIGN KEY (LMSSectionIdentifier)
REFERENCES lms.LMSSection (LMSSectionIdentifier)
ON DELETE CASCADE;
ALTER TABLE lms.LMSUserLMSSectionAssociation ADD CONSTRAINT FK_LMSUserLMSSectionAssociation_LMSUser FOREIGN KEY (LMSUserIdentifier)
REFERENCES lms.LMSUser (LMSUserIdentifier)
ON DELETE CASCADE;

COMMENT ON TABLE lms.LmsUserLMSSectionAssociation IS 'The association of a user and section. For a student, this would be a section enrollment. For a teacher, this would be a section assignment.';
COMMENT ON COLUMN lms.LMSUserLMSSectionAssociation.LMSSectionIdentifier IS 'A unique numeric identifier assigned to the section.';
COMMENT ON COLUMN lms.LMSUserLMSSectionAssociation.LMSUserIdentifier IS 'A unique numeric identifier assigned to the user.';
COMMENT ON COLUMN lms.LMSUserLMSSectionAssociation.LMSUserLMSSectionAssociationIdentifier IS 'A unique numeric identifier assigned to the user section association.';
COMMENT ON COLUMN lms.LMSUserLMSSectionAssociation.SourceSystemIdentifier IS 'A unique number or alphanumeric code assigned to a user by the source system.';
COMMENT ON COLUMN lms.LMSUserLMSSectionAssociation.SourceSystem IS 'The system code or name providing the user data.';
COMMENT ON COLUMN lms.LMSUserLMSSectionAssociation.EnrollmentStatus IS 'The status of the user section association. E.g., Active, Inactive, Withdrawn.';
COMMENT ON COLUMN lms.LMSUserLMSSectionAssociation.SourceCreateDate IS 'The source system datetime the record was created.';
COMMENT ON COLUMN lms.LMSUserLMSSectionAssociation.SourceLastModifiedDate IS 'The source system datetime the record was last modified.';
COMMENT ON COLUMN lms.LMSUserLMSSectionAssociation.DeletedAt IS 'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''';

CREATE TABLE lms.stg_LMSUserLMSSectionAssociation (
    StagingId INT GENERATED ALWAYS AS IDENTITY,
    LMSSectionSourceSystemIdentifier VARCHAR(255) NOT NULL,
    LMSUserSourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    EnrollmentStatus VARCHAR(60) NOT NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL,
    LastModifiedDate TIMESTAMP NOT NULL,
    CONSTRAINT stg_LMSUserLMSSectionAssociation_PK PRIMARY KEY (
        StagingId
    )
);

CREATE INDEX IX_stg_LMSUserLMSSectionAssociation_Natural_Key ON lms.stg_LMSUserLMSSectionAssociation (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
