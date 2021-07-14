-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE OR ALTER PROCEDURE lms.harmonize_lmssection_canvas AS
BEGIN
    SET NOCOUNT ON;

    UPDATE
        LMSSection
    SET
        LMSSection.EdFiSectionId = edfisection.Id
    FROM
        lms.LMSSection LMSSection
    INNER JOIN
        edfi.Section edfisection
    ON
        LMSSection.SISSectionIdentifier = edfisection.SectionIdentifier
    WHERE
        LMSSection.SourceSystem = 'Canvas'
    AND
        LMSSection.EdFiSectionId is NULL
	AND
        LMSSection.DeletedAt IS NULL;
END;

