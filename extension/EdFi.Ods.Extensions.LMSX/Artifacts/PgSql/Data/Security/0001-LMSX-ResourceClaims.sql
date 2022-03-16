-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

DO
$$DECLARE
    application_name varchar(200) := 'ed-fi ods api';
    application_id int;
    system_descriptors_resource_claim_id int;
    lms_metadata_resource_claim_id int;
    authorization_strategy_id int;
BEGIN

    SELECT
      applicationid INTO application_id
    FROM
      dbo.applications
    WHERE
      applicationname = 'Ed-Fi ODS API';

    SELECT
      resourceclaimid INTO system_descriptors_resource_claim_id
    FROM
      dbo.resourceclaims
    WHERE
      resourcename = 'systemDescriptors';

    -- Create parent resource claim for LMSX resources

    INSERT INTO
      dbo.resourceclaims (
        displayname,
        resourcename,
        claimname,
        parentresourceclaimid,
        application_applicationid
    )
    VALUES (
      'lmsMetadata',
      'lmsMetadata',
      'http://ed-fi.org/ods/identity/claims/domains/lmsMetadata',
      null,
      application_id
    );


    SELECT lastval() INTO lms_metadata_resource_claim_id;

     -- Create individual resource claims

    INSERT INTO dbo.resourceclaims (
        displayname,
        resourcename,
        claimname,
        parentresourceclaimid,
        application_applicationid
    )
    SELECT
        *
    FROM (SELECT * FROM (
        VALUES
            (
                'assignment',
                'assignment',
                'http://ed-fi.org/ods/identity/claims/lmsx/assignment',
                lms_metadata_resource_claim_id,
                application_id
            ),
            (
                'assignmentSubmission',
                'assignmentSubmission',
                'http://ed-fi.org/ods/identity/claims/lmsx/assignmentSubmission',
                lms_metadata_resource_claim_id,
                application_id
            ),
            (
                'assignmentCategoryDescriptor',
                'assignmentCategoryDescriptor',
                'http://ed-fi.org/ods/identity/claims/lmsx/assignmentCategoryDescriptor',
                system_descriptors_resource_claim_id,
                application_id
            ),
            (
                'lmsSourceSystemDescriptor',
                'lmsSourceSystemDescriptor',
                'http://ed-fi.org/ods/identity/claims/lmsx/lmsSourceSystemDescriptor',
                system_descriptors_resource_claim_id,
                application_id
            ),
            (
                'submissionStatusDescriptor',
                'submissionStatusDescriptor',
                'http://ed-fi.org/ods/identity/claims/lmsx/submissionStatusDescriptor',
                system_descriptors_resource_claim_id,
                application_id
            ),
            (
                'submissionTypeDescriptor',
                'submissionTypeDescriptor',
                'http://ed-fi.org/ods/identity/claims/lmsx/submissionTypeDescriptor',
                system_descriptors_resource_claim_id,
                application_id
            )
        ) as tbl(displayname, resourcename, claimname, parentresourceclaimid, application_applicationid)
    ) as s
    ON CONFLICT DO NOTHING;

    -- Set namespace-based authorization strategy for LMS resource claims

    SELECT
      authorizationstrategyid INTO authorization_strategy_id
    FROM
      dbo.authorizationstrategies
    WHERE
      authorizationstrategyname = 'NamespaceBased';

    INSERT INTO
      dbo.resourceclaimauthorizationmetadatas (
        action_actionid,
        authorizationstrategy_authorizationstrategyid,
        resourceclaim_resourceclaimid,
        validationrulesetname
      )
    SELECT
      actions.actionid,
      authorization_strategy_id,
      lms_metadata_resource_claim_id,
      null
    FROM
      dbo.actions
	  WHERE
      actionname in ('Create','Read','Update','Delete');

    -- Create LMS Vendor claim set

    INSERT INTO
      dbo.claimsets (
        claimsetname,
        application_applicationid
      )
    VALUES (
      'LMS Vendor',
      application_id
    );

    --Add resource claims to LMS Vendor and Ed-Fi Sandbox claim sets

    INSERT INTO
      dbo.claimsetresourceclaims (
        action_actionid,
        claimset_claimsetid,
        resourceclaim_resourceclaimid
      )
    SELECT
      a.actionid,
      c.claimsetid,
      lms_metadata_resource_claim_id
    FROM dbo.actions a
        ,dbo.claimsets c
    WHERE (
        c.claimsetname = 'LMS Vendor'
      OR
        c.claimsetname = 'Ed-Fi Sandbox'
    )
    ON CONFLICT DO NOTHING;

END$$
