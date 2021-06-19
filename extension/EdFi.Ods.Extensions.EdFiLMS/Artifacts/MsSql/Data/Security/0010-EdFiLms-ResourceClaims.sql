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
			'http://ed-fi.org/ods/identity/claims/ed-fi-lms/assignment',
			@relationshipBasedDataResourceClaimId,
			@applicationId
		),
		(
			'assignmentSubmission',
			'assignmentSubmission',
			'http://ed-fi.org/ods/identity/claims/ed-fi-lms/assignmentSubmission',
			@relationshipBasedDataResourceClaimId,
			@applicationId
		),
		(
			'assignmentCategoryDescriptor',
			'assignmentCategoryDescriptor',
			'http://ed-fi.org/ods/identity/claims/ed-fi-lms/assignmentCategoryDescriptor',
			@systemDescriptorsResourceClaimId,
			@ApplicationId
		),
		(
			'lMSSourceSystemDescriptor',
			'lMSSourceSystemDescriptor',
			'http://ed-fi.org/ods/identity/claims/ed-fi-lms/lMSSourceSystemDescriptor',
			@systemDescriptorsResourceClaimId,
			@ApplicationId
		),
		(
			'submissionStatusDescriptor',
			'submissionStatusDescriptor',
			'http://ed-fi.org/ods/identity/claims/ed-fi-lms/submissionStatusDescriptor',
			@systemDescriptorsResourceClaimId,
			@ApplicationId
		),
		(
			'submissionTypeDescriptor',
			'submissionTypeDescriptor',
			'http://ed-fi.org/ods/identity/claims/ed-fi-lms/submissionTypeDescriptor',
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


-- Provide the Sandbox claimset with full access to the new resources, if it exists
-- MERGE INTO dbo.ClaimSetResourceClaims as t
-- USING (
-- 	SELECT
-- 		a.ActionId,
-- 		c.ClaimSetId,
-- 		r.ResourceClaimId
-- 	FROM
-- 		dbo.Actions a
-- 	CROSS JOIN
-- 		dbo.ClaimSets c
-- 	CROSS JOIN
-- 		dbo.ResourceClaims r
-- 	WHERE
-- 		c.ClaimSetName = 'Ed-Fi Sandbox'
-- 	AND
-- 		r.ClaimName LIKE 'http://ed-fi.org/ods/identity/claims/ed-fi-lms%'
-- ) as s
-- ON
-- 	t.Action_ActionId = s.ActionId
-- AND
-- 	t.ClaimSet_ClaimSetId = s.ClaimSetId
-- AND
-- 	t.ResourceClaim_ResourceClaimId = s.ResourceClaimId
-- WHEN NOT MATCHED THEN
-- INSERT
-- 	(Action_ActionId, ClaimSet_ClaimSetId, ResourceClaim_ResourceClaimId)
-- VALUES
-- 	(ActionId, ClaimSetId, ResourceClaimId);


-- {
--   "message": "Access to the resource could not be authorized. Are you missing a claim? This resource can be authorized by the following
--   claims:\r\n    \r\nThe API client has been assigned the 'Ed-Fi Sandbox' claim set with the following resource claims:\r\n
--   http://ed-fi.org/ods/identity/claims/domains/edFiTypes\r\n    http://ed-fi.org/ods/identity/claims/domains/systemDescriptors\r\n
--   http://ed-fi.org/ods/identity/claims/domains/managedDescriptors\r\n    http://ed-fi.org/ods/identity/claims/domains/educationOrganizations\r\n
--    http://ed-fi.org/ods/identity/claims/domains/people\r\n    http://ed-fi.org/ods/identity/claims/domains/relationshipBasedData\r\n
--    http://ed-fi.org/ods/identity/claims/domains/assessmentMetadata\r\n    http://ed-fi.org/ods/identity/claims/domains/identity\r\n
--    http://ed-fi.org/ods/identity/claims/domains/educationStandards\r\n    http://ed-fi.org/ods/identity/claims/domains/primaryRelationships\r\n
--    http://ed-fi.org/ods/identity/claims/domains/surveyDomain\r\n    http://ed-fi.org/ods/identity/claims/communityProviderLicense\r\n
--    http://ed-fi.org/ods/identity/claims/educationContent\r\n    http://ed-fi.org/ods/identity/claims/ed-fi-lms/assignmentCategoryDescriptor\r\n
--    http://ed-fi.org/ods/identity/claims/ed-fi-lms/lMSSourceSystemDescriptor\r\n
--     http://ed-fi.org/ods/identity/claims/ed-fi-lms/submissionStatusDescriptor\r\n
--      http://ed-fi.org/ods/identity/claims/ed-fi-lms/submissionTypeDescriptor"
-- }
