-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

create or replace procedure lms.harmonize_lmsuser_canvas()
language SQL
as $$

    update
        lms.lmsuser
    set
        edfistudentid = edfistudent.id
    from
        lms.lmsuser u
    inner join
        edfi.student edfistudent
    on
        u.sisuseridentifier = edfistudent.studentuniqueid
    where
        lms.lmsuser.sourcesystemidentifier = u.sourcesystemidentifier
    and
        lms.lmsuser.sourcesystem = u.sourcesystem
    and
        u.sourcesystem = 'Canvas'
    and
        u.edfistudentid is null
	and
        u.deletedat is null;
$$;
