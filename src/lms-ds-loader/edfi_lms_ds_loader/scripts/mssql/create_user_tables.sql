-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.LMSUser (
    LMSUserIdentifier INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    UserRole NVARCHAR(60) NOT NULL,
    SISUserIdentifier NVARCHAR(255) NULL,
    LocalUserIdentifier NVARCHAR(255) NULL,
    [Name] NVARCHAR(255) NOT NULL,
    EmailAddress NVARCHAR(255) NOT NULL,
    SourceCreateDate DATETIME2(7) NULL,
    SourceLastModifiedDate DATETIME2(7) NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    DeletedAt DATETIME2(7) NULL,
    CONSTRAINT LMSUser_PK PRIMARY KEY CLUSTERED (
        LMSUserIdentifier ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

ALTER TABLE lms.LMSUser ADD CONSTRAINT LMSUser_DF_CreateDate DEFAULT (getdate()) FOR CreateDate;

ALTER TABLE lms.LMSUser ADD CONSTRAINT LMSUser_DF_LastModifiedDate DEFAULT (getdate()) FOR LastModifiedDate;

ALTER TABLE lms.LMSUser ADD CONSTRAINT UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);




CREATE TABLE lms.stg_LMSUser (
    StagingId INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    UserRole NVARCHAR(60) NOT NULL,
    SISUserIdentifier NVARCHAR(255) NULL,
    LocalUserIdentifier NVARCHAR(255) NULL,
    [Name] NVARCHAR(255) NOT NULL,
    EmailAddress NVARCHAR(255) NOT NULL,
    SourceCreateDate DATETIME2(7) NULL,
    SourceLastModifiedDate DATETIME2(7) NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    CONSTRAINT stg_LMSUser_PK PRIMARY KEY CLUSTERED (
        StagingId ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

CREATE INDEX IX_stg_LMSUser_Natural_Key ON lms.stg_LMSUser (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
