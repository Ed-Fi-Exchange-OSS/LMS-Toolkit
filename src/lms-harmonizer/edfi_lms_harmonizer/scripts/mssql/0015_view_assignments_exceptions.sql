-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE VIEW lmsx.assignments_exceptions AS
    SELECT * FROM LMS.Assignment lmsAssignment
	WHERE NOT EXISTS(
			SELECT 1 FROM lmsx.Assignment lmsxassignment
			where lmsxassignment.AssignmentIdentifier = lmsAssignment.SourceSystemIdentifier
		)
