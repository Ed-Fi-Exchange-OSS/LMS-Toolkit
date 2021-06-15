
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
        LMSSection.SISSectionIdentifier = edfisection.id
    WHERE
        LMSSection.SourceSystem = 'Google Classroom'
    AND
        LMSSection.EdFiSectionId is NULL
	AND
        LMSSection.DeletedAt IS NULL;
END;

