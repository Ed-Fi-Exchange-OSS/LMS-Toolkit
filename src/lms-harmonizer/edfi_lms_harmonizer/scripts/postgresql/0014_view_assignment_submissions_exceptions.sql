-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

create view lmsx.assignment_submissions_exceptions as
    select * from lms.assignmentsubmission lmsassignmentsubmission
    where not exists(
            select 1 from lmsx.assignmentsubmission lmsxassignmentsubmission
                inner join lmsx.assignment lmsxassginment
					on lmsxassginment.assignmentidentifier = lmsxassignmentsubmission.assignmentidentifier
				inner join lms.assignment lmsassginment
					on lmsxassginment.assignmentidentifier = lmsassginment.sourcesystemidentifier
				inner join edfi.descriptor sourcesystemdescriptor
					on sourcesystemdescriptor.descriptorid = lmsxassginment.lmssourcesystemdescriptorid

            where lmsxassignmentsubmission.assignmentsubmissionidentifier = lmsassignmentsubmission.sourcesystemidentifier
				and sourcesystemdescriptor.codevalue = lmsassginment.sourcesystem
        )
        and lmsassignmentsubmission.deletedat is null;
