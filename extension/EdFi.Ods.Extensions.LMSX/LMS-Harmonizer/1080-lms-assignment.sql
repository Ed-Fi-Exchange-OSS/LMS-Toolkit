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
		,[SchoolId])
	SELECT
		lmsAssignment.AssignmentIdentifier,
		sourceSystemDescriptor.DescriptorId,
		lmsAssignment.[Title],
		assignmentCatDescriptor.DescriptorId,
		lmsAssignment.[AssignmentDescription],
		lmsAssignment.[StartDateTime],
		lmsAssignment.[EndDateTime],
		lmsAssignment.[DueDateTime],
		lmsAssignment.[MaxPoints],
		edfiSection.SectionIdentifier,
		edfiSection.LocalCourseCode,
		edfiSection.[SessionName],
		edfiSection.[SchoolYear],
		edfiSection.[SchoolId]

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

		INNER JOIN lmsx.AssignmentCategoryDescriptor
			ON assignmentCatDescriptor.DescriptorId = AssignmentCategoryDescriptor.AssignmentCategoryDescriptorId

	WHERE
		LMSSection.DeletedAt IS NULL
		AND
		lmsAssignment.DeletedAt IS NULL
		AND
		lmsAssignment.SourceSystemIdentifier not in (select AssignmentIdentifier from lmsx.Assignment)

END;
