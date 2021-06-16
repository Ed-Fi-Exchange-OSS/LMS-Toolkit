# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

CREATE_SCHEMA_EDFI = """
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'edfi')
EXEC sys.sp_executesql N'CREATE SCHEMA edfi';
        """

CREATE_SCHEMA_LMS = """
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'lms')
EXEC sys.sp_executesql N'CREATE SCHEMA lms';
        """

CREATE_TABLE_LMS_USER = """
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

CREATE_TABLE_EDFI_STUDENT_ETC = """
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


CREATE_TABLE_LMS_SECTION = """
CREATE TABLE lms.LMSSection (
    LMSSectionIdentifier INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    SISSectionIdentifier NVARCHAR(255) NULL,
    Title NVARCHAR(255) NOT NULL,
    SectionDescription NVARCHAR(1024) NULL,
    Term NVARCHAR(60) NULL,
    LMSSectionStatus NVARCHAR(60) NULL,
    SourceCreateDate DATETIME2(7) NULL,
    SourceLastModifiedDate DATETIME2(7) NULL,
    EdFiSectionId UNIQUEIDENTIFIER NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    DeletedAt DATETIME2(7) NULL,
    CONSTRAINT LMSSection_PK PRIMARY KEY CLUSTERED (
        LMSSectionIdentifier ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY];

ALTER TABLE lms.LMSSection ADD CONSTRAINT LMSSection_DF_CreateDate DEFAULT (getdate()) FOR CreateDate;
ALTER TABLE lms.LMSSection ADD CONSTRAINT LMSSection_DF_LastModifiedDate DEFAULT (getdate()) FOR LastModifiedDate;
ALTER TABLE lms.LMSSection ADD CONSTRAINT LMSSection_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);
"""


CREATE_TABLE_EDFI_SECTION = """
CREATE TABLE [edfi].[Section](
    [LocalCourseCode] [nvarchar](60) NOT NULL,
    [SchoolId] [int] NOT NULL,
    [SchoolYear] [smallint] NOT NULL,
    [SectionIdentifier] [nvarchar](255) NOT NULL,
    [SessionName] [nvarchar](60) NOT NULL,
    [SequenceOfCourse] [int] NULL,
    [EducationalEnvironmentDescriptorId] [int] NULL,
    [MediumOfInstructionDescriptorId] [int] NULL,
    [PopulationServedDescriptorId] [int] NULL,
    [AvailableCredits] [decimal](9, 3) NULL,
    [AvailableCreditTypeDescriptorId] [int] NULL,
    [AvailableCreditConversion] [decimal](9, 2) NULL,
    [InstructionLanguageDescriptorId] [int] NULL,
    [LocationSchoolId] [int] NULL,
    [LocationClassroomIdentificationCode] [nvarchar](60) NULL,
    [OfficialAttendancePeriod] [bit] NULL,
    [SectionName] [nvarchar](100) NULL,
    [Discriminator] [nvarchar](128) NULL,
    [CreateDate] [DATETIME2](7) NOT NULL,
    [LastModifiedDate] [DATETIME2](7) NOT NULL,
    [Id] [uniqueidentifier] NOT NULL,
    [ChangeVersion] [bigint] NOT NULL,
 CONSTRAINT [Section_PK] PRIMARY KEY CLUSTERED
(
    [LocalCourseCode] ASC,
    [SchoolId] ASC,
    [SchoolYear] ASC,
    [SectionIdentifier] ASC,
    [SessionName] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY];
ALTER TABLE [edfi].[Section] ADD  CONSTRAINT [Section_DF_CreateDate]  DEFAULT (getdate()) FOR [CreateDate];
ALTER TABLE [edfi].[Section] ADD  CONSTRAINT [Section_DF_LastModifiedDate]  DEFAULT (getdate()) FOR [LastModifiedDate];
ALTER TABLE [edfi].[Section] ADD  CONSTRAINT [Section_DF_Id]  DEFAULT (newid()) FOR [Id];
"""
