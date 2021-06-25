-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE OR ALTER PROCEDURE lmsx.harmonize_assignment AS
BEGIN

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
		,[Id])
	SELECT
		lmsAssignment.AssignmentIdentifier,
		sourceSystemDescriptor.id, -- [SourceSystem]
		lmsAssignment.[Title],
		assignmentCategoryDescriptor.Id, -- [AssignmentCategory]
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
		lmsAssignment.SourceSystemIdentifier

	FROM lms.Assignment lmsAssignment
		INNER JOIN lms.LMSSection lmssection
			ON lmsAssignment.LMSSectionIdentifier = lmssection.LMSSectionIdentifier

		INNER JOIN edfi.Section edfiSection
			ON lmssection.EdFiSectionId = edfiSection.Id

		INNER JOIN edfi.Descriptor sourceSystemDescriptor
			ON sourceSystemDescriptor.ShortDescription = lmsAssignment.SourceSystem
			AND sourceSystemDescriptor.Id in (select * from lmsx.LMSSourceSystemDescriptor)

		INNER JOIN edfi.Descriptor assignmentCategoryDescriptor
			ON assignmentCategoryDescriptor.ShortDescription = lmsAssignment.AssignmentCategory
			AND assignmentCategoryDescriptor.id in (select * from lmsx.AssignmentCategoryDescriptor)

	WHERE
		LMSSection.DeletedAt IS NULL
		AND
		lmsAssignment.DeletedAt IS NULL

END;
