-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE VIEW lmsx.missing_assignment_submission_status_descriptors AS
    SELECT * FROM LMS.AssignmentSubmission lmsAssignmentSubmission
    WHERE NOT EXISTS(
            SELECT 1 FROM edfi.Descriptor assignmentCatDescriptor WHERE
                assignmentCatDescriptor.CodeValue = lmsAssignmentSubmission.SubmissionStatus
                AND assignmentCatDescriptor.Namespace = 'uri://ed-fi.org/edfilms/SubmissionStatusDescriptor/' + lmsAssignmentSubmission.SourceSystem
        )
