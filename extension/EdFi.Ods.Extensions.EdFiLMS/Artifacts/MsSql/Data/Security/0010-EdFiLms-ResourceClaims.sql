-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

DECLARE @applicationId INT

SELECT @applicationId = ApplicationId
FROM dbo.Applications
WHERE ApplicationName = 'Ed-Fi ODS API'

DECLARE @systemDescriptorsResourceClaimId INT
SELECT @systemDescriptorsResourceClaimId = ResourceClaimId
FROM dbo.ResourceClaims
WHERE ResourceName = 'systemDescriptors'

DECLARE @relationshipBasedDataResourceClaimId INT
SELECT @relationshipBasedDataResourceClaimId = ResourceClaimId
FROM dbo.ResourceClaims
WHERE ResourceName = 'relationshipBasedData'

MERGE dbo.ResourceClaims as t
USING (
	SELECT * FROM (VALUES
		 (
			'assignment',
			'assignment',
			'http://ed-fi.org/ods/identity/claims/edfilms/assignment',
			@relationshipBasedDataResourceClaimId,
			@applicationId
		),
		(
			'assignmentSubmission',
			'assignmentSubmission',
			'http://ed-fi.org/ods/identity/claims/edfilms/assignmentSubmission',
			@relationshipBasedDataResourceClaimId,
			@applicationId
		),
		(
			'assignmentCategoryDescriptor',
			'assignmentCategoryDescriptor',
			'http://ed-fi.org/ods/identity/claims/edfilms/assignmentCategoryDescriptor',
			@systemDescriptorsResourceClaimId,
			@ApplicationId
		),
		(
			'lMSSourceSystemDescriptor',
			'lMSSourceSystemDescriptor',
			'http://ed-fi.org/ods/identity/claims/edfilms/lMSSourceSystemDescriptor',
			@systemDescriptorsResourceClaimId,
			@ApplicationId
		),
		(
			'submissionStatusDescriptor',
			'submissionStatusDescriptor',
			'http://ed-fi.org/ods/identity/claims/edfilms/submissionStatusDescriptor',
			@systemDescriptorsResourceClaimId,
			@ApplicationId
		),
		(
			'submissionTypeDescriptor',
			'submissionTypeDescriptor',
			'http://ed-fi.org/ods/identity/claims/edfilms/submissionTypeDescriptor',
			@systemDescriptorsResourceClaimId,
			@ApplicationId
		)
	) as tbl(DisplayName, ResourceName, ClaimName, ParentResourceClaimId, Application_ApplicationId)
) as s
ON
	t.ResourceName = s.ResourceName
AND
	t.ClaimName = s.ClaimName
AND
	t.ParentResourceClaimId = s.ParentResourceClaimId
AND
	t.Application_ApplicationId = s.Application_ApplicationId
WHEN NOT MATCHED THEN
INSERT
	(DisplayName, ResourceName, ClaimName, ParentResourceClaimId, Application_ApplicationId)
VALUES
	(s.DisplayName, s.ResourceName, s.ClaimName, s.ParentResourceClaimId, s.Application_ApplicationId);
