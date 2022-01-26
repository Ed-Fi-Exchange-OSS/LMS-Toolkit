-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

create schema if not exists lms;

create table if not exists lms.migrationjournal_harmonizer (
    script varchar(250) not null,
    installdate timestamp not null default (now()),
    constraint pk_migrationjournal_harmonizer primary key (script)
);
