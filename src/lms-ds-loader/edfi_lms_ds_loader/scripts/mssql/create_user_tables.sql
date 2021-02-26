-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE [lms].[LMSUser] (
    [LMSUserIdentifier] [INT] IDENTITY,
    [SourceSystemIdentifier] [NVARCHAR](255) NOT NULL,
    [SourceSystem] [NVARCHAR](255) NOT NULL,
    [UserRole] [NVARCHAR](60) NOT NULL,
    [SISUserIdentifier] [NVARCHAR](255) NULL,
    [LocalUserIdentifier] [NVARCHAR](255) NULL,
    [Name] [NVARCHAR](255) NOT NULL,
    [EmailAddress] [NVARCHAR](255) NOT NULL,
    [SourceCreateDate] [DATETIME2](7) NULL,
    [SourceLastModifiedDate] [DATETIME2](7) NULL,
    [Discriminator] [NVARCHAR](128) NULL,
    [CreateDate] [DATETIME2] NOT NULL,
    [LastModifiedDate] [DATETIME2] NOT NULL,
    [Id] [UNIQUEIDENTIFIER] NOT NULL,
    CONSTRAINT [LMSUser_PK] PRIMARY KEY CLUSTERED (
        [LMSUserIdentifier] ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [lms].[LMSUser] ADD CONSTRAINT [LMSUser_DF_CreateDate] DEFAULT (getdate()) FOR [CreateDate]
GO
ALTER TABLE [lms].[LMSUser] ADD CONSTRAINT [LMSUser_DF_Id] DEFAULT (newid()) FOR [Id]
GO
ALTER TABLE [lms].[LMSUser] ADD CONSTRAINT [LMSUser_DF_LastModifiedDate] DEFAULT (getdate()) FOR [LastModifiedDate]
GO
