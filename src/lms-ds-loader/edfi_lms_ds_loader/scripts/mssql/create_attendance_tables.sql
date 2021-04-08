-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.LMSUserAttendanceEvent (
    LMSUserAttendanceEventIdentifier INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    LMSUserIdentifier INT NOT NULL,
    LMSSectionIdentifier INT NULL,
    LMSUserLMSSectionAssociationIdentifier INT NULL,
    EventDate DATE NOT NULL,
    AttendanceStatus NVARCHAR(60) NOT NULL,
    SourceCreateDate DATETIME2(7) NULL,
    SourceLastModifiedDate DATETIME2(7) NULL,
    DeletedAt DATETIME2(7) NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    CONSTRAINT LMSUserAttendanceEvent_PK PRIMARY KEY CLUSTERED (
        LMSUserAttendanceEventIdentifier ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

ALTER TABLE lms.LMSUserAttendanceEvent ADD CONSTRAINT LMSUserAttendanceEvent_DF_CreateDate DEFAULT (getdate()) FOR CreateDate
ALTER TABLE lms.LMSUserAttendanceEvent ADD CONSTRAINT LMSUserAttendanceEvent_DF_LastModifiedDate DEFAULT (getdate()) FOR LastModifiedDate
ALTER TABLE lms.LMSUserAttendanceEvent ADD CONSTRAINT LMSUserAttendanceEvent_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

ALTER TABLE [lms].[LMSUserAttendanceEvent] WITH CHECK ADD CONSTRAINT [FK_LMSUserAttendanceEvent_LMSUser] FOREIGN KEY ([LMSUserIdentifier])
REFERENCES [lms].[LMSUser] ([LMSUserIdentifier])

CREATE NONCLUSTERED INDEX [FK_LMSUserAttendanceEvent_LMSUser]
ON [lms].[LMSUserAttendanceEvent] ([LMSUserIdentifier] ASC)

ALTER TABLE lms.LMSUserAttendanceEvent WITH CHECK ADD CONSTRAINT FK_LMSUserAttendanceEvent_LMSUserLMSSectionAssociation
FOREIGN KEY (LMSUserLMSSectionAssociationIdentifier)
REFERENCES lms.LMSUserLMSSectionAssociation (LMSUserLMSSectionAssociationIdentifier)

CREATE NONCLUSTERED INDEX [FK_LMSUserAttendanceEvent_LMSUserLMSSectionAssociation]
ON [lms].[LMSUserAttendanceEvent] ([LMSSectionIdentifier] ASC, [LMSUserIdentifier] ASC, [LMSUserLMSSectionAssociationIdentifier] ASC)


EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Attendance statuses assigned to users for a specific date.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user attendance event.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'LMSUserAttendanceEventIdentifier'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a user by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the user data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'SourceSystem'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'LMSUserIdentifier'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'LMSSectionIdentifier'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user section association.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'LMSUserLMSSectionAssociationIdentifier'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date of the attendance event.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'EventDate'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A code describing the attendance event. E.g., In Attendance, Excused Absence, Unexcused Absence.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'AttendanceStatus'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'SourceCreateDate'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate'
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'DeletedAt'


CREATE TABLE lms.stg_LMSUserAttendanceEvent (
    StagingId INT NOT NULL IDENTITY,
    SourceSystemIdentifier NVARCHAR(255) NOT NULL,
    SourceSystem NVARCHAR(255) NOT NULL,
    LMSUserSourceSystemIdentifier NVARCHAR(255) NOT NULL,
    LMSSectionSourceSystemIdentifier NVARCHAR(255) NULL,
    EventDate DATE NOT NULL,
    AttendanceStatus NVARCHAR(60) NOT NULL,
    SourceCreateDate DATETIME2(7) NULL,
    SourceLastModifiedDate DATETIME2(7) NULL,
    CreateDate DATETIME2 NOT NULL,
    LastModifiedDate DATETIME2 NOT NULL,
    CONSTRAINT stg_LMSUserAttendanceEvent_PK PRIMARY KEY CLUSTERED (
        StagingId ASC
    ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

CREATE INDEX IX_stg_LMSUserAttendanceEvent_Natural_Key ON lms.stg_LMSUserAttendanceEvent (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
