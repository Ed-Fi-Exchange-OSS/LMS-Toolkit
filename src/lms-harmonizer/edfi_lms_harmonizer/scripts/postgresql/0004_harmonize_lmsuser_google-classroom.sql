-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

create or replace procedure lms.harmonize_lmsuser_google_classroom()
language SQL
as $$

    update
        lms.lmsuser
    set
        edfistudentid = s.id
    from
        edfi.student s

    inner join
        edfi.studenteducationorganizationassociationelectronicmail sem
    on
        s.studentusi = sem.studentusi

    inner join
        lms.lmsuser u
    on
        sem.electronicmailaddress = u.emailaddress

    where
        lms.lmsuser.sourcesystemidentifier = u.sourcesystemidentifier
    and
        lms.lmsuser.sourcesystem = u.sourcesystem
    and
        u.sourcesystem = 'Google'
    and
        u.edfistudentid is null
	and
        u.deletedat is null;
$$;
