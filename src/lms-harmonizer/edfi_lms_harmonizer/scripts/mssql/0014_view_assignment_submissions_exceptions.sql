-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE VIEW lmsx.assignment_submissions_exceptions AS
    SELECT * FROM LMS.AssignmentSubmission lmsAssignmentSubmission
    WHERE NOT EXISTS(
            SELECT 1 FROM lmsx.AssignmentSubmission lmsxassignmentsubmission
                where lmsxassignmentsubmission.AssignmentSubmissionIdentifier = lmsAssignmentSubmission.SourceSystemIdentifier
        )
