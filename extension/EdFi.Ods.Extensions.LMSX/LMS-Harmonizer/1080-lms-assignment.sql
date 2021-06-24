-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE OR ALTER PROCEDURE lms.harmonize_assignment AS
BEGIN

	INSERT INTO [edfilms].[Assignment]
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
		,[CreateDate]
		,[LastModifiedDate]
		,[Id])
	SELECT
		lmsAssignment.AssignmentIdentifier,
		-- lmsAssignment.[LMSSourceSystemDescriptorId], -- [SourceSystem]
		lmsAssignment.[Title],
		-- [AssignmentCategoryDescriptorId], -- [AssignmentCategory]
		lmsAssignment.[AssignmentDescription],
		lmsAssignment.[StartDateTime],
		lmsAssignment.[EndDateTime],
		lmsAssignment.[DueDateTime],
		lmsAssignment.[MaxPoints],
		lmssection.EdFiSectionId,
		edfiSection.LocalCourseCode,
		edfiSection.[SessionName],
		edfiSection.[SchoolYear],
		edfiSection.[SchoolId],
		lmsAssignment.[CreateDate],
		lmsAssignment.[LastModifiedDate],
		lmsAssignment.SourceSystemIdentifier

	FROM lms.Assignment lmsAssignment
		INNER JOIN lms.LMSSection lmssection
			ON lmsAssignment.LMSSectionIdentifier = lmssection.LMSSectionIdentifier
		INNER JOIN edfi.Section edfiSection
			ON lmssection.EdFiSectionId = edfiSection.Id
		INNER JOIN edfi.Descriptor sourceSystemDescriptor
			ON sourceSystemDescriptor.Id
	WHERE
		LMSSection.DeletedAt IS NULL
		AND
		lmsAssignment.DeletedAt IS NULL;

END;
