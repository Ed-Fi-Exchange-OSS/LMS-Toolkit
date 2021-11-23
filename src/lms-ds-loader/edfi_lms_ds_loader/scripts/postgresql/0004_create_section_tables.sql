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
    SourceCreateDate TIMESTAMP(7) NULL,
    SourceLastModifiedDate TIMESTAMP(7) NULL,
    CreateDate TIMESTAMP NOT NULL DEFAULT now(),
    LastModifiedDate TIMESTAMP NOT NULL DEFAULT now(),
    DeletedAt TIMESTAMP(7) NULL,
    CONSTRAINT LMSSection_PK PRIMARY KEY (
        LMSSectionIdentifier
    )
);

ALTER TABLE lms.LMSSection ADD CONSTRAINT LMSSection_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

CREATE TABLE lms.stg_LMSSection (
    StagingId INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    SISSectionIdentifier VARCHAR(255) NULL,
    Title VARCHAR(255) NOT NULL,
    SectionDescription VARCHAR(1024) NULL,
    Term VARCHAR(60) NULL,
    LMSSectionStatus VARCHAR(60) NULL,
    SourceCreateDate TIMESTAMP(7) NULL,
    SourceLastModifiedDate TIMESTAMP(7) NULL,
    CreateDate TIMESTAMP NOT NULL,
    LastModifiedDate TIMESTAMP NOT NULL,
    CONSTRAINT stg_LMSSection_PK PRIMARY KEY (
        StagingId
    )
);

CREATE INDEX IX_stg_LMSSection_Natural_Key ON lms.stg_LMSSection (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
