-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

create view lmsx.exceptions_lmssection as
    select
        lmssectionidentifier,
        sourcesystemidentifier,
        sourcesystem,
        sissectionidentifier
    from
        lms.lmssection
    where
        edfisectionid is null
    and
        deletedat is null;
