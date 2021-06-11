# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.
from sqlalchemy.engine.base import Connection

# This is a copy/paste shortcut to initialize the test database with the proper structure


def migrate_lms_user_and_edfi_student(connection: Connection):
    connection.execute(
        """
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'edfi')
EXEC sys.sp_executesql N'CREATE SCHEMA edfi';
        """
    )

    connection.execute(
        """
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'lms')
EXEC sys.sp_executesql N'CREATE SCHEMA lms';
        """
    )

    # from edfi_lms_ds_loader's create_user_tables.sql and add_mapping_columns_for_edfi_student_and_section.sql
    connection.execute(
        """
IF OBJECT_ID(N'lms.LMSUser', N'U') IS NULL
BEGIN

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

ALTER TABLE lms.LMSUser ADD EdFiStudentId UNIQUEIDENTIFIER NULL;

CREATE NONCLUSTERED INDEX IX_LMSUser_EdfiStudentId
    ON lms.LMSUser (EdFiStudentId)
    WHERE DeletedAt is NOT NULL;

END;
        """
    )

    # from ODS/API 5.2's 0002-Tables.sql
    connection.execute(
        """
IF OBJECT_ID(N'edfi.Student', N'U') IS NULL
BEGIN

CREATE TABLE [edfi].[Student] (
    [StudentUSI] [INT] IDENTITY(1,1) NOT NULL,
    [PersonalTitlePrefix] [NVARCHAR](30) NULL,
    [FirstName] [NVARCHAR](75) NOT NULL,
    [MiddleName] [NVARCHAR](75) NULL,
    [LastSurname] [NVARCHAR](75) NOT NULL,
    [GenerationCodeSuffix] [NVARCHAR](10) NULL,
    [MaidenName] [NVARCHAR](75) NULL,
    [BirthDate] [DATE] NOT NULL,
    [BirthCity] [NVARCHAR](30) NULL,
    [BirthStateAbbreviationDescriptorId] [INT] NULL,
    [BirthInternationalProvince] [NVARCHAR](150) NULL,
    [BirthCountryDescriptorId] [INT] NULL,
    [DateEnteredUS] [DATE] NULL,
    [MultipleBirthStatus] [BIT] NULL,
    [BirthSexDescriptorId] [INT] NULL,
    [CitizenshipStatusDescriptorId] [INT] NULL,
    [PersonId] [NVARCHAR](32) NULL,
    [SourceSystemDescriptorId] [INT] NULL,
    [StudentUniqueId] [NVARCHAR](32) NOT NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [Student_PK] PRIMARY KEY CLUSTERED (
        [StudentUSI] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];
END;

IF OBJECT_ID(N'edfi.StudentEducationOrganizationAssociation', N'U') IS NULL
BEGIN
CREATE TABLE [edfi].[StudentEducationOrganizationAssociation] (
    [EducationOrganizationId] [INT] NOT NULL,
    [StudentUSI] [INT] NOT NULL,
    [SexDescriptorId] [INT] NOT NULL,
    [ProfileThumbnail] [NVARCHAR](255) NULL,
    [HispanicLatinoEthnicity] [BIT] NULL,
    [OldEthnicityDescriptorId] [INT] NULL,
    [LimitedEnglishProficiencyDescriptorId] [INT] NULL,
    [LoginId] [NVARCHAR](60) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [StudentEducationOrganizationAssociation_PK] PRIMARY KEY CLUSTERED (
        [EducationOrganizationId] ASC,
        [StudentUSI] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];
END;

IF OBJECT_ID(N'edfi.StudentEducationOrganizationAssociationElectronicMail', N'U') IS NULL
BEGIN
CREATE TABLE [edfi].[StudentEducationOrganizationAssociationElectronicMail] (
    [EducationOrganizationId] [INT] NOT NULL,
    [ElectronicMailAddress] [NVARCHAR](128) NOT NULL,
    [ElectronicMailTypeDescriptorId] [INT] NOT NULL,
    [StudentUSI] [INT] NOT NULL,
    [PrimaryEmailAddressIndicator] [BIT] NULL,
    [DoNotPublishIndicator] [BIT] NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    CONSTRAINT [StudentEducationOrganizationAssociationElectronicMail_PK] PRIMARY KEY CLUSTERED (
        [EducationOrganizationId] ASC,
        [ElectronicMailAddress] ASC,
        [ElectronicMailTypeDescriptorId] ASC,
        [StudentUSI] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];
END;

IF OBJECT_ID(N'edfi.StudentEducationOrganizationAssociationStudentIdentificationCode', N'U') IS NULL
BEGIN
CREATE TABLE [edfi].[StudentEducationOrganizationAssociationStudentIdentificationCode] (
    [AssigningOrganizationIdentificationCode] [NVARCHAR](60) NOT NULL,
    [EducationOrganizationId] [INT] NOT NULL,
    [StudentIdentificationSystemDescriptorId] [INT] NOT NULL,
    [StudentUSI] [INT] NOT NULL,
    [IdentificationCode] [NVARCHAR](60) NOT NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    CONSTRAINT [StudentEducationOrganizationAssociationStudentIdentificationCode_PK] PRIMARY KEY CLUSTERED (
        [AssigningOrganizationIdentificationCode] ASC,
        [EducationOrganizationId] ASC,
        [StudentIdentificationSystemDescriptorId] ASC,
        [StudentUSI] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];
END;
        """
    )
