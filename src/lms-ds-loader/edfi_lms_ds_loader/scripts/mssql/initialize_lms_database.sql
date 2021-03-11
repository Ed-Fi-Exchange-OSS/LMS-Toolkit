-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'lms')
EXEC sys.sp_executesql N'CREATE SCHEMA lms';


CREATE TABLE lms.MigrationJournal (
    Script VARCHAR(250) NOT NULL,
    InstallDate DATETIME2 NOT NULL DEFAULT (getdate()),
    CONSTRAINT PK_MigrationJournal PRIMARY KEY CLUSTERED (Script)
) ON [PRIMARY];
