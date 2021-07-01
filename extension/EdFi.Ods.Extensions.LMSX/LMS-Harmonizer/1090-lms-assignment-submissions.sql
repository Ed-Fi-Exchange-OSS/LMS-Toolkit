-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE OR ALTER PROCEDURE [lms].[harmonize_assignment_submissions] AS
BEGIN
    SET NOCOUNT ON;
	select * from edfi.Descriptor edfides
	inner join lmsx.SubmissionStatusDescriptor lmsdes on edfides.DescriptorId = lmsdes.SubmissionStatusDescriptorId

	SELECT
		lmsSubmission.AssignmentSubmissionIdentifier, --[AssignmentSubmissionIdentifier],
		lmsUser.EdFiStudentId, --[StudentUSI],
		lmsxAssignment.AssignmentIdentifier, --[AssignmentIdentifier],
		lmsxAssignment.SchoolId, --[SchoolId],
		submissionStatusDescriptor.DescriptorId, --[SubmissionStatusDescriptorId],
		lmsSubmission.SubmissionDateTime, --[SubmissionDateTime],
		lmsSubmission.EarnedPoints, --[EarnedPoints],
		lmsSubmission.Grade, --[Grade],
		lmsSubmission.CreateDate,
		lmsSubmission.LastModifiedDate,
		lmsSubmission.DeletedAt
	INTO #ALL_SUBMISSIONS
	FROM LMS.AssignmentSubmission lmsSubmission
	INNER JOIN LMSX.Assignment lmsxAssignment
		ON lmsSubmission.AssignmentIdentifier = lmsxAssignment.AssignmentIdentifier
	INNER JOIN LMS.LMSUser lmsUser
		ON lmsUser.LMSUserIdentifier = lmsSubmission.LMSUserIdentifier
	INNER JOIN EDFI.Descriptor submissionStatusDescriptor
		ON submissionStatusDescriptor.CodeValue = lmsSubmission.SubmissionStatus

		INNER JOIN LMSX.SubmissionStatusDescriptor lmsxSubmissionStatus
			ON submissionStatusDescriptor.DescriptorId = lmsxSubmissionStatus.SubmissionStatusDescriptorId


	INSERT INTO LMSX.AssignmentSubmission(
		[AssignmentSubmissionIdentifier],
		[StudentUSI],
		[AssignmentIdentifier],
		[SchoolId],
		[SubmissionStatusDescriptorId],
		[SubmissionDateTime],
		[EarnedPoints],
		[Grade]
	)
	SELECT
		AssignmentSubmissionIdentifier, --[AssignmentSubmissionIdentifier],
		EdFiStudentId, --[StudentUSI],
		AssignmentIdentifier, --[AssignmentIdentifier],
		SchoolId, --[SchoolId],
		DescriptorId, --[SubmissionStatusDescriptorId],
		SubmissionDateTime, --[SubmissionDateTime],
		EarnedPoints, --[EarnedPoints],
		Grade,
		CreateDate,
		LastModifiedDate,
		DeletedAt
	FROM #ALL_SUBMISSIONS
	WHERE
		#ALL_SUBMISSIONS.AssignmentSubmissionIdentifier NOT IN
			(SELECT AssignmentSubmission.AssignmentSubmissionIdentifier FROM LMSX.AssignmentSubmission)
		AND #ALL_SUBMISSIONS.DeletedAt IS NULL

	DROP TABLE #ALL_SUBMISSIONS

END;
