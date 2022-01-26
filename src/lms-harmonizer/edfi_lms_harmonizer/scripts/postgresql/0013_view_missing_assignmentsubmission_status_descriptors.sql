-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

create view lmsx.missing_assignment_submission_status_descriptors as
    select * from lms.assignmentsubmission lmsassignmentsubmission
    where not exists(
            select 1 from edfi.descriptor assignmentcatdescriptor where
                assignmentcatdescriptor.codevalue = lmsassignmentsubmission.submissionstatus
                and assignmentcatdescriptor.namespace = 'uri://ed-fi.org/edfilms/SubmissionStatusDescriptor/' || lmsassignmentsubmission.sourcesystem
        );
