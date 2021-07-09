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

-- Create parent resource claim for LMSX resources

INSERT INTO dbo.ResourceClaims
	(DisplayName, ResourceName, ClaimName, ParentResourceClaimId, Application_ApplicationId)
VALUES
	('lmsMetadata', 'lmsMetadata', 'http://ed-fi.org/ods/identity/claims/domains/lmsMetadata', NULL, @applicationId);

DECLARE @lmsMetadataResourceClaimId INT
SELECT @lmsMetadataResourceClaimId = ResourceClaimId
FROM dbo.ResourceClaims
WHERE ResourceName = 'lmsMetadata'


-- Create individual resource claims

MERGE dbo.ResourceClaims as t
USING (
	SELECT * FROM (VALUES
		 (
			'assignment',
			'assignment',
			'http://ed-fi.org/ods/identity/claims/lmsx/assignment',
			@lmsMetadataResourceClaimId,
			@applicationId
		),
		(
			'assignmentSubmission',
			'assignmentSubmission',
			'http://ed-fi.org/ods/identity/claims/lmsx/assignmentSubmission',
			@lmsMetadataResourceClaimId,
			@applicationId
		),
		(
			'assignmentCategoryDescriptor',
			'assignmentCategoryDescriptor',
			'http://ed-fi.org/ods/identity/claims/lmsx/assignmentCategoryDescriptor',
			@systemDescriptorsResourceClaimId,
			@ApplicationId
		),
		(
			'lmsSourceSystemDescriptor',
			'lmsSourceSystemDescriptor',
			'http://ed-fi.org/ods/identity/claims/lmsx/lmsSourceSystemDescriptor',
			@systemDescriptorsResourceClaimId,
			@ApplicationId
		),
		(
			'submissionStatusDescriptor',
			'submissionStatusDescriptor',
			'http://ed-fi.org/ods/identity/claims/lmsx/submissionStatusDescriptor',
			@systemDescriptorsResourceClaimId,
			@ApplicationId
		),
		(
			'submissionTypeDescriptor',
			'submissionTypeDescriptor',
			'http://ed-fi.org/ods/identity/claims/lmsx/submissionTypeDescriptor',
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


-- Set namespace-based authorization strategy for LMS resource claims

DECLARE @AuthorizationStrategyId INT
SELECT @AuthorizationStrategyId  = (SELECT AuthorizationStrategyId FROM [dbo].[AuthorizationStrategies] WHERE AuthorizationStrategyName = 'NamespaceBased');

INSERT INTO [dbo].[ResourceClaimAuthorizationMetadatas]
    ([Action_ActionId]
    ,[AuthorizationStrategy_AuthorizationStrategyId]
    ,[ResourceClaim_ResourceClaimId]
    ,[ValidationRuleSetName])
SELECT ac.ActionId, @AuthorizationStrategyId, ResourceClaimId, null
FROM [dbo].[ResourceClaims]
CROSS APPLY
    (SELECT ActionId
    FROM [dbo].[Actions]
    WHERE ActionName IN ('Create', 'Read', 'Update', 'Delete')) AS ac
WHERE ResourceName IN ('lmsMetadata');


-- Create LMS Vendor claim set

INSERT INTO dbo.ClaimSets
	(ClaimSetName, Application_ApplicationId)
VALUES
	('LMS Vendor', @applicationId);


--Add resource claims to LMS Vendor and Ed-Fi Sandbox claim sets

INSERT INTO [dbo].[ClaimSetResourceClaims]
SELECT [ActionId]
    ,[ClaimSetId]
    ,[ResourceClaimId]
    ,NULL
    ,NULL
FROM Actions a
    ,ClaimSets c
    ,ResourceClaims r
WHERE r.ResourceName IN ('lmsMetadata')
    AND (
        c.ClaimSetName = 'LMS Vendor'
        OR c.ClaimSetName = 'Ed-Fi Sandbox'
        )
    AND NOT EXISTS (
        SELECT 1
        FROM ClaimSetResourceClaims
        WHERE Action_ActionId = a.ActionId
            AND ClaimSet_ClaimSetId = c.ClaimSetId
            AND ResourceClaim_ResourceClaimId = r.ResourceClaimId
        )
