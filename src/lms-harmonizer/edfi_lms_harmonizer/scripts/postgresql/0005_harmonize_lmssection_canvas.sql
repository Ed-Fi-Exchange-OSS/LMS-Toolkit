-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

create or replace procedure lms.harmonize_lmssection_canvas()
language SQL
as $$

    update
        lms.lmssection
    set
        edfisectionid = edfisection.id
    from
        lms.lmssection s
    inner join
        edfi.section edfisection
    on
        s.sissectionidentifier = edfisection.sectionidentifier
    where
        lms.lmssection.sourcesystemidentifier = s.sourcesystemidentifier
    and
        lms.lmssection.sourcesystem = s.sourcesystem
    and
        s.sourcesystem = 'Canvas'
    and
        s.edfisectionid is null
	and
        s.deletedat is null;
$$;
