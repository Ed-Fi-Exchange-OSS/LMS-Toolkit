-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.LMSSection (
    LMSSectionIdentifier INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    SISSectionIdentifier VARCHAR(255) NULL,
    Title VARCHAR(255) NOT NULL,
    SectionDescription VARCHAR(1024) NULL,
    Term VARCHAR(60) NULL,
    LMSSectionStatus VARCHAR(60) NULL,
    EdFiSectionId UUID NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL DEFAULT now(),
    LastModifiedDate TIMESTAMP NOT NULL DEFAULT now(),
    DeletedAt TIMESTAMP NULL,
    CONSTRAINT LMSSection_PK PRIMARY KEY (
        LMSSectionIdentifier
    )
);

ALTER TABLE lms.LMSSection ADD CONSTRAINT LMSSection_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

CREATE INDEX IX_LMSSection_EdfiSectionId
    ON lms.LMSSection (EdFiSectionId)
    WHERE DeletedAt is NOT NULL;

COMMENT ON TABLE lms.LMSSection IS 'An organized grouping of course content and users over a period of time for the purpose of providing instruction.';
COMMENT ON COLUMN lms.LMSSection.LMSSectionIdentifier IS 'A unique numeric identifier assigned to the section.';
COMMENT ON COLUMN lms.LMSSection.SourceSystemIdentifier IS 'A unique number or alphanumeric code assigned to a user by the source system.';
COMMENT ON COLUMN lms.LMSSection.SourceSystem IS 'The system code or name providing the section data.';
COMMENT ON COLUMN lms.LMSSection.SISSectionIdentifier IS 'The section identifier defined in the Student Information System (SIS).';
COMMENT ON COLUMN lms.LMSSection.Title IS 'The section title or name.';
COMMENT ON COLUMN lms.LMSSection.SectionDescription IS 'The section description.';
COMMENT ON COLUMN lms.LMSSection.Term IS 'The enrollment term for the section.';
COMMENT ON COLUMN lms.LMSSection.LMSSectionStatus IS 'The section status from the source system. E.g., Published, Completed.';
COMMENT ON COLUMN lms.LMSSection.SourceCreateDate IS 'The source system datetime the record was created.';
COMMENT ON COLUMN lms.LMSSection.SourceLastModifiedDate IS 'The source system datetime the record was last modified.';
COMMENT ON COLUMN lms.LMSSection.DeletedAt IS 'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''';
COMMENT ON COLUMN lms.LMSSection.EdFiSectionId IS 'A mapping from this LMSSection to an EdFi Section Id, which uniquely identifies an EdFi Section';

CREATE TABLE lms.stg_LMSSection (
    StagingId INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    SISSectionIdentifier VARCHAR(255) NULL,
    Title VARCHAR(255) NOT NULL,
    SectionDescription VARCHAR(1024) NULL,
    Term VARCHAR(60) NULL,
    LMSSectionStatus VARCHAR(60) NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL,
    LastModifiedDate TIMESTAMP NOT NULL,
    CONSTRAINT stg_LMSSection_PK PRIMARY KEY (
        StagingId
    )
);

CREATE INDEX IX_stg_LMSSection_Natural_Key ON lms.stg_LMSSection (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
