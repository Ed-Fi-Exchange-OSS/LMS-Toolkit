-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

create view lmsx.assignments_exceptions as
    select lmsassignment.* from lms.assignment lmsassignment
	where not exists(
			select 1 from lmsx.assignment lmsxassignment
			inner join edfi.descriptor on lmsxassignment.lmssourcesystemdescriptorid = descriptor.descriptorid
			where lmsxassignment.assignmentidentifier = lmsassignment.sourcesystemidentifier
			and descriptor.codevalue = lmsassignment.sourcesystem
		)
		and lmsassignment.deletedat is null;
