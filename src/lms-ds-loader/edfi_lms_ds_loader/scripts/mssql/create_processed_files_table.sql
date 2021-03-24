/*
 * SPDX-License-Identifier: Apache-2.0
 * Licensed to the Ed-Fi Alliance under one or more agreements.
 * The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
 * See the LICENSE and NOTICES files in the project root for more information.
 */

CREATE TABLE lms.ProcessedFiles (
    FullPath NVARCHAR(255) NOT NULL,
    ResourceName NVARCHAR(128) NOT NULL,
    NumberOfRows INT NOT NULL,
    UploadDateTime DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT ProcessedFiles_PK PRIMARY KEY CLUSTERED (
        FullPath
    ) ON [PRIMARY]
) ON [PRIMARY];

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The full path of the processed file.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'ProcessedFiles', @level2type=N'COLUMN', @level2name=N'FullPath';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The name of the resource.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'ProcessedFiles', @level2type=N'COLUMN', @level2name=N'ResourceName';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Number of rows for the file.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'ProcessedFiles', @level2type=N'COLUMN', @level2name=N'NumberOfRows';
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Datetime when the file was uploaded to the database.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'ProcessedFiles', @level2type=N'COLUMN', @level2name=N'UploadDateTime';
