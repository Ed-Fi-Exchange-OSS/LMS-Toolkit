-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE VIEW lmsx.assignment_submissions_exceptions AS
    SELECT * FROM LMS.AssignmentSubmission lmsAssignmentSubmission
    WHERE NOT EXISTS(
            SELECT 1 FROM lmsx.AssignmentSubmission lmsxassignmentsubmission
                INNER JOIN lmsx.Assignment lmsxassginment
					ON lmsxassginment.AssignmentIdentifier = lmsxassignmentsubmission.AssignmentIdentifier
				INNER JOIN lms.Assignment lmsassginment
					ON lmsxassginment.AssignmentIdentifier = lmsassginment.SourceSystemIdentifier
				INNER JOIN edfi.Descriptor sourcesystemdescriptor
					ON sourcesystemdescriptor.DescriptorId = lmsxassginment.LMSSourceSystemDescriptorId

            WHERE lmsxassignmentsubmission.AssignmentSubmissionIdentifier = lmsAssignmentSubmission.SourceSystemIdentifier
				AND sourcesystemdescriptor.CodeValue = lmsassginment.SourceSystem
        )
        AND lmsAssignmentSubmission.DeletedAt IS NULL
