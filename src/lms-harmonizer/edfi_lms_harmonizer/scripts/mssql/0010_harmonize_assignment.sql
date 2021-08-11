-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE OR ALTER PROCEDURE [lms].[harmonize_assignment] @SourceSystem nvarchar(255), @Namespace nvarchar(255) AS
BEGIN
    SET NOCOUNT ON;

	-- Load temporary table
	SELECT
		lmsAssignment.SourceSystemIdentifier as AssignmentIdentifier,
		sourceSystemDescriptor.DescriptorId as LMSSourceSystemDescriptorId,
		lmsAssignment.Title,
		assignmentCatDescriptor.DescriptorId as AssignmentCategoryDescriptorId,
		lmsAssignment.AssignmentDescription,
		lmsAssignment.StartDateTime,
		lmsAssignment.EndDateTime,
		lmsAssignment.DueDateTime,
		lmsAssignment.MaxPoints,
		edfiSection.SectionIdentifier,
		edfiSection.LocalCourseCode,
		edfiSection.SessionName,
		edfiSection.SchoolYear,
		edfiSection.SchoolId,
		lmsAssignment.LastModifiedDate as ASSIGNMENT_LAST_MODIFIED_DATE,
		lmssection.DeletedAt as SECTION_DELETED,
		lmsAssignment.DeletedAt as ASSIGNMENT_DELETED
	INTO #ALL_ASSIGNMENTS
 	FROM lms.Assignment lmsAssignment
		INNER JOIN lms.LMSSection lmssection
			ON lmsAssignment.LMSSectionIdentifier = lmssection.LMSSectionIdentifier

		INNER JOIN edfi.Section edfiSection
			ON lmssection.EdFiSectionId = edfiSection.Id

		INNER JOIN edfi.Descriptor sourceSystemDescriptor
			ON sourceSystemDescriptor.CodeValue = lmsAssignment.SourceSystem

		INNER JOIN lmsx.LMSSourceSystemDescriptor
		    ON sourceSystemDescriptor.DescriptorId  = LMSSourceSystemDescriptor.LMSSourceSystemDescriptorId

		INNER JOIN edfi.Descriptor assignmentCatDescriptor
			ON assignmentCatDescriptor.CodeValue = lmsAssignment.AssignmentCategory
			AND assignmentCatDescriptor.Namespace = 'uri://ed-fi.org/edfilms/AssignmentCategoryDescriptor/' + @SourceSystem

		INNER JOIN lmsx.AssignmentCategoryDescriptor
			ON assignmentCatDescriptor.DescriptorId = AssignmentCategoryDescriptor.AssignmentCategoryDescriptorId

    WHERE lmsAssignment.SourceSystem = @SourceSystem

	INSERT INTO lmsx.[Assignment]
		([AssignmentIdentifier]
		,[LMSSourceSystemDescriptorId]
		,[Title]
		,[AssignmentCategoryDescriptorId]
		,[AssignmentDescription]
		,[StartDateTime]
		,[EndDateTime]
		,[DueDateTime]
		,[MaxPoints]
		,[SectionIdentifier]
		,[LocalCourseCode]
		,[SessionName]
		,[SchoolYear]
		,[SchoolId]
		,[Namespace])
	SELECT
		[AssignmentIdentifier]
		,[LMSSourceSystemDescriptorId]
		,[Title]
		,[AssignmentCategoryDescriptorId]
		,[AssignmentDescription]
		,[StartDateTime]
		,[EndDateTime]
		,[DueDateTime]
		,[MaxPoints]
		,[SectionIdentifier]
		,[LocalCourseCode]
		,[SessionName]
		,[SchoolYear]
		,[SchoolId]
		,@Namespace
	FROM
	#ALL_ASSIGNMENTS
	WHERE
		#ALL_ASSIGNMENTS.[AssignmentIdentifier] NOT IN (
            SELECT AssignmentIdentifier FROM lmsx.Assignment
        )
		AND
			[SECTION_DELETED] IS NULL
		AND
			[ASSIGNMENT_DELETED] IS NULL


	UPDATE LMSX.Assignment
	SET
		LMSX.Assignment.[Title] = #ALL_ASSIGNMENTS.Title,
		LMSX.Assignment.[AssignmentCategoryDescriptorId] = #ALL_ASSIGNMENTS.AssignmentCategoryDescriptorId,
		LMSX.Assignment.[AssignmentDescription] = #ALL_ASSIGNMENTS.AssignmentDescription,
		LMSX.Assignment.[StartDateTime] = #ALL_ASSIGNMENTS.StartDateTime,
		LMSX.Assignment.[EndDateTime] = #ALL_ASSIGNMENTS.EndDateTime,
		LMSX.Assignment.[DueDateTime] = #ALL_ASSIGNMENTS.DueDateTime,
		LMSX.Assignment.[MaxPoints] = #ALL_ASSIGNMENTS.MaxPoints,
		LMSX.Assignment.[LastModifiedDate] = GETDATE()
	FROM
		#ALL_ASSIGNMENTS
	WHERE
		LMSX.Assignment.AssignmentIdentifier = #ALL_ASSIGNMENTS.AssignmentIdentifier
		AND
			#ALL_ASSIGNMENTS.[ASSIGNMENT_LAST_MODIFIED_DATE] > LMSX.Assignment.LastModifiedDate


	DELETE FROM LMSX.AssignmentSubmission
		WHERE LMSX.AssignmentSubmission.AssignmentIdentifier IN (
            SELECT [AssignmentIdentifier] FROM #ALL_ASSIGNMENTS WHERE ASSIGNMENT_DELETED IS NOT NULL
        )


	DELETE FROM LMSX.Assignment
		WHERE LMSX.Assignment.AssignmentIdentifier IN (
            SELECT [AssignmentIdentifier] FROM #ALL_ASSIGNMENTS WHERE ASSIGNMENT_DELETED IS NOT NULL
        )

	DROP TABLE #ALL_ASSIGNMENTS

END;
