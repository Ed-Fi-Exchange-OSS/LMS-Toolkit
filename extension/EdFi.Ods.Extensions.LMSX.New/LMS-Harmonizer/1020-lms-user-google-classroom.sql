-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE OR ALTER PROCEDURE lms.harmonize_lmsuser_google_classroom AS
BEGIN
    SET NOCOUNT ON;

-- Update based on any EdFi Student Electronic Mail matching with a LMS SISUserIdentifier
    UPDATE
        lms.LMSUser
    SET
        EdFiStudentId = selectemails.Id
    FROM
        (
            SELECT
                emails.ElectronicMailAddress, s.Id
            FROM
                edfi.Student s
            OUTER APPLY (
                SELECT
                    ElectronicMailAddress
                FROM
                    edfi.StudentEducationOrganizationAssociationElectronicMail sem
                WHERE
                    s.StudentUsi = sem.StudentUsi
            ) AS emails
        ) AS selectemails
    WHERE
        EmailAddress = selectemails.ElectronicMailAddress
    AND
        EdFiStudentId is NULL
	AND
        DeletedAt IS NULL;

END;
