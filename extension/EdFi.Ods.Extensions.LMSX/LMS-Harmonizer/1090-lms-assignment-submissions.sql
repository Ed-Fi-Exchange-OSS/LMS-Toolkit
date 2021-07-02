-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE OR ALTER PROCEDURE [lms].[harmonize_assignment_submissions] AS
BEGIN
    SET NOCOUNT ON;

	-- Load temporal table
	SELECT
		lmsSubmission.AssignmentSubmissionIdentifier,
		lmsUser.EdFiStudentId,
		lmsxAssignment.AssignmentIdentifier,
		lmsxAssignment.SchoolId,
		submissionStatusDescriptor.DescriptorId,
		lmsSubmission.SubmissionDateTime,
		lmsSubmission.EarnedPoints,
		lmsSubmission.Grade,
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

	-- Insert new records
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
		AssignmentSubmissionIdentifier,
		EdFiStudentId,
		AssignmentIdentifier,
		SchoolId,
		DescriptorId,
		SubmissionDateTime,
		EarnedPoints,
		Grade,
		CreateDate,
		LastModifiedDate,
		DeletedAt
	FROM #ALL_SUBMISSIONS
	WHERE
		#ALL_SUBMISSIONS.AssignmentSubmissionIdentifier NOT IN
			(SELECT AssignmentSubmission.AssignmentSubmissionIdentifier FROM LMSX.AssignmentSubmission)
		AND #ALL_SUBMISSIONS.DeletedAt IS NULL


	-- Update existing records
	UPDATE LMSX.AssignmentSubmission SET
		LMSX.AssignmentSubmission.SubmissionStatusDescriptorId = #ALL_SUBMISSIONS.DescriptorId,
		LMSX.AssignmentSubmission.SubmissionDateTime = #ALL_SUBMISSIONS.SubmissionDateTime,
		LMSX.AssignmentSubmission.EarnedPoints = #ALL_SUBMISSIONS.EarnedPoints,
		LMSX.AssignmentSubmission.Grade = #ALL_SUBMISSIONS.Grade,
		LMSX.AssignmentSubmission.LastModifiedDate = GETDATE()
	FROM #ALL_SUBMISSIONS
	WHERE #ALL_SUBMISSIONS.AssignmentSubmissionIdentifier = LMSX.AssignmentSubmission.AssignmentSubmissionIdentifier
	AND #ALL_SUBMISSIONS.LastModifiedDate > LMSX.AssignmentSubmission.LastModifiedDate
	AND #ALL_SUBMISSIONS.DeletedAt IS NULL


	-- delete records if needed
	DELETE FROM LMSX.AssignmentSubmission
	WHERE LMSX.AssignmentSubmission.AssignmentSubmissionIdentifier IN
		(SELECT LMSSUBMISSION.AssignmentSubmissionIdentifier FROM LMS.AssignmentSubmission LMSSUBMISSION WHERE LMSSUBMISSION.DeletedAt IS NOT NULL)


	DROP TABLE #ALL_SUBMISSIONS


END;
