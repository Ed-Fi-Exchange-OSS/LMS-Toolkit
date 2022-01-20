-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.LMSUser (
    LMSUserIdentifier INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    UserRole VARCHAR(60) NOT NULL,
    SISUserIdentifier VARCHAR(255) NULL,
    LocalUserIdentifier VARCHAR(255) NULL,
    Name VARCHAR(255) NOT NULL,
    EmailAddress VARCHAR(255) NOT NULL,
    EdFiStudentId UUID NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL DEFAULT (now()),
    LastModifiedDate TIMESTAMP NOT NULL DEFAULT (now()),
    DeletedAt TIMESTAMP NULL,
    CONSTRAINT LMSUser_PK PRIMARY KEY (
        LMSUserIdentifier
    )
) ;

ALTER TABLE lms.LMSUser ADD CONSTRAINT UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

CREATE INDEX IX_LMSUser_EdfiStudentId
    ON lms.LMSUser (EdFiStudentId)
    WHERE DeletedAt is NOT NULL;

COMMENT ON TABLE lms.LMSUser IS 'A person using the instructional system.';
COMMENT ON COLUMN lms.LMSUser.LMSUserIdentifier IS 'A unique numeric identifier assigned to the user.';
COMMENT ON COLUMN lms.LMSUser.SourceSystemIdentifier IS 'A unique number or alphanumeric code assigned to a user by the source system.';
COMMENT ON COLUMN lms.LMSUser.SourceSystem IS 'The system code or name providing the user data.';
COMMENT ON COLUMN lms.LMSUser.UserRole IS 'The role assigned to the user. E.g., Student, Teacher, Administrator.';
COMMENT ON COLUMN lms.LMSUser.SISUserIdentifier IS 'The user identifier defined in the Student Information System (SIS).';
COMMENT ON COLUMN lms.LMSUser.LocalUserIdentifier IS 'The user identifier assigned by a school or district.';
COMMENT ON COLUMN lms.LMSUser.Name IS 'The full name of the user.';
COMMENT ON COLUMN lms.LMSUser.EmailAddress IS 'The primary e-mail address for the user.';
COMMENT ON COLUMN lms.LMSUser.SourceCreateDate IS 'The source system datetime the record was created.';
COMMENT ON COLUMN lms.LMSUser.SourceLastModifiedDate IS 'The source system datetime the record was last modified.';
COMMENT ON COLUMN lms.LMSUser.DeletedAt IS 'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''';
COMMENT ON COLUMN lms.LMSUser.EdFiStudentId IS 'A mapping from this LMSUser to an EdFi Student Id, which uniquely identifies an EdFi Student';


CREATE TABLE lms.stg_LMSUser (
    StagingId INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    UserRole VARCHAR(60) NOT NULL,
    SISUserIdentifier VARCHAR(255) NULL,
    LocalUserIdentifier VARCHAR(255) NULL,
    Name VARCHAR(255) NOT NULL,
    EmailAddress VARCHAR(255) NOT NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL,
    LastModifiedDate TIMESTAMP NOT NULL,
    EdFiStudentId UUID null,
    CONSTRAINT stg_LMSUser_PK PRIMARY KEY (
        StagingId
    )
);

CREATE INDEX ix_stg_lmsuser_natural_key ON lms.stg_LMSUser (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
