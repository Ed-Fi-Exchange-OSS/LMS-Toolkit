-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE VIEW lmsx.missing_assignment_category_descriptors AS
    SELECT * FROM LMS.Assignment lmsAssignment
	WHERE NOT EXISTS(
			SELECT 1 FROM edfi.Descriptor assignmentCatDescriptor WHERE
				assignmentCatDescriptor.CodeValue = lmsAssignment.AssignmentCategory
				AND assignmentCatDescriptor.Namespace = 'uri://ed-fi.org/edfilms/AssignmentCategoryDescriptor/' + lmsAssignment.SourceSystem
		)
