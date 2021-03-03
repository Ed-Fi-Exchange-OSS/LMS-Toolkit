-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.LMSUser (
    LMSUserIdentifier SERIAL,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    UserRole VARCHAR(60) NOT NULL,
    SISUserIdentifier VARCHAR(255) NULL,
    LocalUserIdentifier VARCHAR(255) NULL,
    Name VARCHAR(255) NOT NULL,
    EmailAddress VARCHAR(255) NOT NULL,
    SourceCreateDate TIMESTAMP(7) NULL,
    SourceLastModifiedDate TIMESTAMP(7) NULL,
    CreateDate TIMESTAMP NOT NULL DEFAULT (now()),
    LastModifiedDate TIMESTAMP NOT NULL DEFAULT (now()),
    DeletedAt TIMESTAMP NULL,
    CONSTRAINT LMSUser_PK PRIMARY KEY (
        LMSUserIdentifier
    )
) ;

ALTER TABLE lms.LMSUser ADD CONSTRAINT UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);




CREATE TABLE lms.stg_LMSUser (
    StagingId SERIAL,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    UserRole VARCHAR(60) NOT NULL,
    SISUserIdentifier VARCHAR(255) NULL,
    LocalUserIdentifier VARCHAR(255) NULL,
    Name VARCHAR(255) NOT NULL,
    EmailAddress VARCHAR(255) NOT NULL,
    SourceCreateDate TIMESTAMP(7) NULL,
    SourceLastModifiedDate TIMESTAMP(7) NULL,
    CreateDate TIMESTAMP NOT NULL,
    LastModifiedDate TIMESTAMP NOT NULL,
    CONSTRAINT stg_LMSUser_PK PRIMARY KEY (
        StagingId
    )
);

CREATE INDEX IX_stg_LMSUser_Natural_Key ON lms.stg_LMSUser (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
