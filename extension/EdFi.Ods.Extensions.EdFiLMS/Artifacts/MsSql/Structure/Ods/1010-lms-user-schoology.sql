-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE OR ALTER PROCEDURE lms.harmonize_lmsuser_schoology AS
BEGIN
    SET NOCOUNT ON;

    UPDATE
        lmsuser
    SET
        lmsuser.EdFiStudentId = edfistudent.Id
    FROM
        lms.LMSUser lmsuser
    INNER JOIN
        edfi.Student edfistudent
    ON
        lmsuser.SISUserIdentifier = edfistudent.StudentUniqueId
    WHERE
        lmsuser.SourceSystem = 'Schoology'
    AND
        lmsuser.EdFiStudentId is NULL
	AND
        lmsuser.DeletedAt IS NULL;
END;
