-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.LMSUserAttendanceEvent (
    LMSUserAttendanceEventIdentifier INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    LMSUserIdentifier INT NOT NULL,
    LMSSectionIdentifier INT NULL,
    LMSUserLMSSectionAssociationIdentifier INT NULL,
    EventDate DATE NOT NULL,
    AttendanceStatus VARCHAR(60) NOT NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    DeletedAt TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL DEFAULT (now()),
    LastModifiedDate TIMESTAMP NOT NULL DEFAULT (now()),
    CONSTRAINT LMSUserAttendanceEvent_PK PRIMARY KEY (
        LMSUserAttendanceEventIdentifier
    )
);

ALTER TABLE lms.LMSUserAttendanceEvent ADD CONSTRAINT LMSUserAttendanceEvent_UK_SourceSystem UNIQUE (SourceSystemIdentifier, SourceSystem);

ALTER TABLE lms.LMSUserAttendanceEvent ADD CONSTRAINT FK_LMSUserAttendanceEvent_LMSUser FOREIGN KEY (LMSUserIdentifier)
REFERENCES lms.LMSUser (LMSUserIdentifier);

CREATE INDEX FK_LMSUserAttendanceEvent_LMSUser
ON lms.LMSUserAttendanceEvent (LMSUserIdentifier ASC);

ALTER TABLE lms.LMSUserAttendanceEvent ADD CONSTRAINT FK_LMSUserAttendanceEvent_LMSUserLMSSectionAssociation
FOREIGN KEY (LMSUserLMSSectionAssociationIdentifier)
REFERENCES lms.LMSUserLMSSectionAssociation (LMSUserLMSSectionAssociationIdentifier);

CREATE INDEX FK_LMSUserAttendanceEvent_LMSUserLMSSectionAssociation
ON lms.LMSUserAttendanceEvent (LMSSectionIdentifier ASC, LMSUserIdentifier ASC, LMSUserLMSSectionAssociationIdentifier ASC);


COMMENT ON TABLE lms.LMSUserAttendanceEvent IS 'Attendance statuses assigned to users for a specific date.';
COMMENT ON COLUMN lms.LMSUserAttendanceEvent.LMSUserAttendanceEventIdentifier IS 'A unique numeric identifier assigned to the user attendance event.';
COMMENT ON COLUMN lms.LMSUserAttendanceEvent.SourceSystemIdentifier IS 'A unique number or alphanumeric code assigned to a user by the source system.';
COMMENT ON COLUMN lms.LMSUserAttendanceEvent.SourceSystem IS 'The system code or name providing the user data.';
COMMENT ON COLUMN lms.LMSUserAttendanceEvent.LMSUserIdentifier IS 'A unique numeric identifier assigned to the user.';
COMMENT ON COLUMN lms.LMSUserAttendanceEvent.LMSSectionIdentifier IS 'A unique numeric identifier assigned to the section.';
COMMENT ON COLUMN lms.LMSUserAttendanceEvent.LMSUserLMSSectionAssociationIdentifier IS 'A unique numeric identifier assigned to the user section association.';
COMMENT ON COLUMN lms.LMSUserAttendanceEvent.EventDate IS 'The date of the attendance event.';
COMMENT ON COLUMN lms.LMSUserAttendanceEvent.AttendanceStatus IS 'A code describing the attendance event. E.g., In Attendance, Excused Absence, Unexcused Absence.';
COMMENT ON COLUMN lms.LMSUserAttendanceEvent.SourceCreateDate IS 'The source system datetime the record was created.';
COMMENT ON COLUMN lms.LMSUserAttendanceEvent.SourceLastModifiedDate IS 'The source system datetime the record was last modified.';
COMMENT ON COLUMN lms.LMSUserAttendanceEvent.DeletedAt IS 'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.';


CREATE TABLE lms.stg_LMSUserAttendanceEvent (
    StagingId INT GENERATED ALWAYS AS IDENTITY,
    SourceSystemIdentifier VARCHAR(255) NOT NULL,
    SourceSystem VARCHAR(255) NOT NULL,
    LMSUserSourceSystemIdentifier VARCHAR(255) NOT NULL,
    LMSSectionSourceSystemIdentifier VARCHAR(255) NULL,
    EventDate DATE NOT NULL,
    AttendanceStatus VARCHAR(60) NOT NULL,
    SourceCreateDate TIMESTAMP NULL,
    SourceLastModifiedDate TIMESTAMP NULL,
    CreateDate TIMESTAMP NOT NULL,
    LastModifiedDate TIMESTAMP NOT NULL,
    CONSTRAINT stg_LMSUserAttendanceEvent_PK PRIMARY KEY (
        StagingId
    )
);

CREATE INDEX IX_stg_LMSUserAttendanceEvent_Natural_Key ON lms.stg_LMSUserAttendanceEvent (SourceSystemIdentifier, SourceSystem, LastModifiedDate);
