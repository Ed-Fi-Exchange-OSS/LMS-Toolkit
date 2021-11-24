-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

ALTER TABLE lms.LMSSection ADD EdFiSectionId UNIQUEIDENTIFIER NULL;

ALTER TABLE lms.LMSUser ADD EdFiStudentId UNIQUEIDENTIFIER NULL;

CREATE NONCLUSTERED INDEX IX_LMSSection_EdfiSectionId
    ON lms.LMSSection (EdFiSectionId)
    WHERE DeletedAt is NOT NULL;

CREATE NONCLUSTERED INDEX IX_LMSUser_EdfiStudentId
    ON lms.LMSUser (EdFiStudentId)
    WHERE DeletedAt is NOT NULL;

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A mapping from this LMSSection to an EdFi Section Id, which uniquely identifies an EdFi Section', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'EdFiSectionId';

EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A mapping from this LMSUser to an EdFi Student Id, which uniquely identifies an EdFi Student', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'EdFiStudentId';
