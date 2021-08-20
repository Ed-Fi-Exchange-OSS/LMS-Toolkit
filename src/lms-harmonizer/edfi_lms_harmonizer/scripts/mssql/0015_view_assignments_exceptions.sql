-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE VIEW lmsx.assignments_exceptions AS
    SELECT lmsAssignment.* FROM LMS.Assignment lmsAssignment
	WHERE NOT EXISTS(
			SELECT 1 FROM lmsx.Assignment lmsxassignment
			INNER JOIN edfi.Descriptor on lmsxassignment.LMSSourceSystemDescriptorId = Descriptor.DescriptorId
			WHERE lmsxassignment.AssignmentIdentifier = lmsAssignment.SourceSystemIdentifier
			AND Descriptor.CodeValue = lmsAssignment.SourceSystem
		)
		AND lmsAssignment.DeletedAt IS NULL
