-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE SCHEMA IF NOT EXISTS lms;

CREATE TABLE IF NOT EXISTS lms.migrationjournal (
    script VARCHAR(250) NOT NULL,
    installdate TIMESTAMP NOT NULL DEFAULT (now()),
    CONSTRAINT pk_migrationjournal PRIMARY KEY (script)
);
