-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

CREATE OR ALTER PROCEDURE [lms].[harmonize_assignment_submissions] @SourceSystem nvarchar(255), @Namespace nvarchar(255) AS
BEGIN
    SET NOCOUNT ON;


	SELECT
		lmsSubmission.AssignmentSubmissionIdentifier,
		EDFISTUDENT.StudentUSI,
		lmsxAssignment.AssignmentIdentifier,
		submissionStatusDescriptor.DescriptorId,
		lmsSubmission.SubmissionDateTime,
		lmsSubmission.EarnedPoints,
		lmsSubmission.Grade,
		lmsSubmission.CreateDate,
		lmsSubmission.LastModifiedDate,
		lmsSubmission.DeletedAt
	INTO #ALL_SUBMISSIONS
	FROM
		lms.AssignmentSubmission as lmsSubmission
	INNER JOIN
		lms.Assignment as lmsAssignment
	ON
		lmsSubmission.AssignmentIdentifier = lmsAssignment.AssignmentIdentifier
	INNER JOIN
		lmsx.Assignment as lmsxAssignment
	ON
		lmsAssignment.SourceSystemIdentifier = lmsxAssignment.AssignmentIdentifier
	INNER JOIN LMS.LMSUser lmsUser
		ON lmsUser.LMSUserIdentifier = lmsSubmission.LMSUserIdentifier
	INNER JOIN EDFI.Descriptor submissionStatusDescriptor
		ON submissionStatusDescriptor.ShortDescription = lmsSubmission.SubmissionStatus
		AND submissionStatusDescriptor.Namespace = 'uri://ed-fi.org/edfilms/SubmissionStatusDescriptor/' + lmsSubmission.SourceSystem
    INNER JOIN LMSX.SubmissionStatusDescriptor lmsxSubmissionStatus
        ON submissionStatusDescriptor.DescriptorId = lmsxSubmissionStatus.SubmissionStatusDescriptorId
	INNER JOIN EDFI.Student EDFISTUDENT
		ON EDFISTUDENT.Id = lmsUser.EdFiStudentId
    WHERE lmsSubmission.SourceSystem = @SourceSystem

	-- Here we are building missing submissions when they are not present
	-- We do this to standardize what is shown in the visualizations

	INSERT INTO #ALL_SUBMISSIONS
	SELECT
		edfisectionassociation.SectionIdentifier
			+ '#' + lmsxassignment.AssignmentIdentifier
			+ '#' + lmsstudent.SourceSystemIdentifier
			as AssignmentSubmissionIdentifier,

		edfisectionassociation.StudentUSI,
		lmsxassignment.AssignmentIdentifier,
		submsisionstatusdescriptor.DescriptorId,
		NULL as SubmissionDateTime,
		NULL as EarnedPoints,
		NULL as Grade,
		GETDATE() as CreateDate,
		GETDATE() as LastModifiedDate,
		NULL AS DeletedAt

	FROM edfi.StudentSectionAssociation edfisectionassociation
	INNER JOIN lmsx.Assignment lmsxassignment
		ON edfisectionassociation.SectionIdentifier = lmsxassignment.SectionIdentifier
	INNER JOIN edfi.Student edfistudent
		ON edfistudent.StudentUSI = edfisectionassociation.StudentUSI
	INNER JOIN lms.LMSUser lmsstudent
		ON lmsstudent.EdFiStudentId = edfistudent.Id
	LEFT JOIN lmsx.AssignmentSubmission lmsxsubmission
		ON lmsxsubmission.AssignmentIdentifier = lmsxassignment.AssignmentIdentifier
			AND lmsxsubmission.StudentUSI = edfisectionassociation.StudentUSI
	INNER JOIN edfi.Descriptor sourcesystemdesc
		ON sourcesystemdesc.DescriptorId = lmsxassignment.LMSSourceSystemDescriptorId
	INNER JOIN edfi.Descriptor submsisionstatusdescriptor
		ON submsisionstatusdescriptor.Namespace = 'uri://ed-fi.org/edfilms/SubmissionStatusDescriptor/' + sourcesystemdesc.CodeValue
		AND submsisionstatusdescriptor.CodeValue in ('missing', 'MISSING')
	WHERE lmsxsubmission.StudentUSI IS NULL
	AND lmsxassignment.DueDateTime < GETDATE()

	INSERT INTO LMSX.AssignmentSubmission(
		[AssignmentSubmissionIdentifier],
		[StudentUSI],
		[AssignmentIdentifier],
		[Namespace],
		[SubmissionStatusDescriptorId],
		[SubmissionDateTime],
		[EarnedPoints],
		[Grade]
	)
	SELECT
		[AssignmentSubmissionIdentifier],
		[StudentUSI],
		[AssignmentIdentifier],
		@Namespace,
		[DescriptorId],
		[SubmissionDateTime],
		[EarnedPoints],
		[Grade]
	FROM #ALL_SUBMISSIONS
	WHERE
		#ALL_SUBMISSIONS.AssignmentSubmissionIdentifier NOT IN
			(SELECT DISTINCT AssignmentSubmission.AssignmentSubmissionIdentifier FROM LMSX.AssignmentSubmission)
		AND #ALL_SUBMISSIONS.StudentUSI NOT IN
            (SELECT DISTINCT StudentUSI FROM LMSX.AssignmentSubmission)
		AND #ALL_SUBMISSIONS.DeletedAt IS NULL


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

	DELETE FROM LMSX.AssignmentSubmission
	WHERE LMSX.AssignmentSubmission.AssignmentSubmissionIdentifier IN
		(SELECT LMSSUBMISSION.AssignmentSubmissionIdentifier FROM LMS.AssignmentSubmission LMSSUBMISSION WHERE LMSSUBMISSION.DeletedAt IS NOT NULL)

	DROP TABLE #ALL_SUBMISSIONS

END;
