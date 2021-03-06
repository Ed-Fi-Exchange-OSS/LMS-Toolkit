-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'lms.Assignment') AND name = N'UX_Assignment_Id')
    CREATE UNIQUE NONCLUSTERED INDEX UX_Assignment_Id ON [lms].[Assignment]
    (Id) WITH (PAD_INDEX = ON, FILLFACTOR = 75, STATISTICS_NORECOMPUTE = OFF) ON [PRIMARY]
    GO
COMMIT

BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'lms.AssignmentSubmission') AND name = N'UX_AssignmentSubmission_Id')
    CREATE UNIQUE NONCLUSTERED INDEX UX_AssignmentSubmission_Id ON [lms].[AssignmentSubmission]
    (Id) WITH (PAD_INDEX = ON, FILLFACTOR = 75, STATISTICS_NORECOMPUTE = OFF) ON [PRIMARY]
    GO
COMMIT

BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'lms.LMSGrade') AND name = N'UX_LMSGrade_Id')
    CREATE UNIQUE NONCLUSTERED INDEX UX_LMSGrade_Id ON [lms].[LMSGrade]
    (Id) WITH (PAD_INDEX = ON, FILLFACTOR = 75, STATISTICS_NORECOMPUTE = OFF) ON [PRIMARY]
    GO
COMMIT

BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'lms.LMSSection') AND name = N'UX_LMSSection_Id')
    CREATE UNIQUE NONCLUSTERED INDEX UX_LMSSection_Id ON [lms].[LMSSection]
    (Id) WITH (PAD_INDEX = ON, FILLFACTOR = 75, STATISTICS_NORECOMPUTE = OFF) ON [PRIMARY]
    GO
COMMIT

BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'lms.LMSSectionActivity') AND name = N'UX_LMSSectionActivity_Id')
    CREATE UNIQUE NONCLUSTERED INDEX UX_LMSSectionActivity_Id ON [lms].[LMSSectionActivity]
    (Id) WITH (PAD_INDEX = ON, FILLFACTOR = 75, STATISTICS_NORECOMPUTE = OFF) ON [PRIMARY]
    GO
COMMIT

BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'lms.LMSSystemActivity') AND name = N'UX_LMSSystemActivity_Id')
    CREATE UNIQUE NONCLUSTERED INDEX UX_LMSSystemActivity_Id ON [lms].[LMSSystemActivity]
    (Id) WITH (PAD_INDEX = ON, FILLFACTOR = 75, STATISTICS_NORECOMPUTE = OFF) ON [PRIMARY]
    GO
COMMIT

BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'lms.LMSUser') AND name = N'UX_LMSUser_Id')
    CREATE UNIQUE NONCLUSTERED INDEX UX_LMSUser_Id ON [lms].[LMSUser]
    (Id) WITH (PAD_INDEX = ON, FILLFACTOR = 75, STATISTICS_NORECOMPUTE = OFF) ON [PRIMARY]
    GO
COMMIT

BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'lms.LMSUserAttendanceEvent') AND name = N'UX_LMSUserAttendanceEvent_Id')
    CREATE UNIQUE NONCLUSTERED INDEX UX_LMSUserAttendanceEvent_Id ON [lms].[LMSUserAttendanceEvent]
    (Id) WITH (PAD_INDEX = ON, FILLFACTOR = 75, STATISTICS_NORECOMPUTE = OFF) ON [PRIMARY]
    GO
COMMIT

BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'lms.LMSUserLMSSectionAssociation') AND name = N'UX_LMSUserLMSSectionAssociation_Id')
    CREATE UNIQUE NONCLUSTERED INDEX UX_LMSUserLMSSectionAssociation_Id ON [lms].[LMSUserLMSSectionAssociation]
    (Id) WITH (PAD_INDEX = ON, FILLFACTOR = 75, STATISTICS_NORECOMPUTE = OFF) ON [PRIMARY]
    GO
COMMIT

