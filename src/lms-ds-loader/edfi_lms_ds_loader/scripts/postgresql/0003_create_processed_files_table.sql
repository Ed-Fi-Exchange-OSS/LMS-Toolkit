-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE TABLE lms.ProcessedFiles (
    FullPath VARCHAR(255) NOT NULL,
    ResourceName VARCHAR(128) NOT NULL,
    NumberOfRows INT NOT NULL,
    UploadDateTime TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT ProcessedFiles_PK PRIMARY KEY (
        FullPath
    )
);

COMMENT ON COLUMN lms.ProcessedFiles.FullPath IS 'The full path of the processed file.';
COMMENT ON COLUMN lms.ProcessedFiles.ResourceName IS 'The name of the resource.';
COMMENT ON COLUMN lms.ProcessedFiles.NumberOfRows IS 'Number of rows for the file.';
COMMENT ON COLUMN lms.ProcessedFiles.UploadDateTime IS 'Datetime when the file was uploaded to the database.';
