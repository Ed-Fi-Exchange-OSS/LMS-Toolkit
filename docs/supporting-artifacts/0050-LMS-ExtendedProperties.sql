-- SPDX-License-Identifier: Apache-2.0
-- Licensed to the Ed-Fi Alliance under one or more agreements.
-- The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
-- See the LICENSE and NOTICES files in the project root for more information.

-- Extended Properties [lms].[Assignment] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Course work assigned to students enrolled in a section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'AssignmentIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a user by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the assignment data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'SourceSystem'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'LMSSectionIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The assignment title or name.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'Title'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The category or type of assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'AssignmentCategory'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The assignment description.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'AssignmentDescription'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The start date and time for the assignment. Students will have access to the assignment after this date.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'StartDateTime'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The end date and time for the assignment. Students will no longer have access to the assignment after this date.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'EndDateTime'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time the assignment is due.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'DueDateTime'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The maximum number of points a student may receive for a submission of the assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'MaxPoints'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'SourceCreateDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'DeletedAt'
GO

-- Extended Properties [lms].[AssignmentSubmission] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A user''s submission of course work for an assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the submission.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'AssignmentSubmissionIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a submission by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the assignment submission data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'SourceSystem'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'LMSUserIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'AssignmentIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The status of the submission in relation to the late acceptance policy.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'Status'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time of the assignment submission.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'SubmissionDateTime'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The points earned for the submission.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'EarnedPoints'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The grade received for the submission.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'Grade'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'SourceCreateDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'DeletedAt'
GO

-- Extended Properties [lms].[AssignmentSubmissionType] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The type(s) of submissions available for the assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmissionType'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmissionType', @level2type=N'COLUMN', @level2name=N'AssignmentIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The type(s) of submissions available for the assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'AssignmentSubmissionType', @level2type=N'COLUMN', @level2name=N'SubmissionType'
GO

-- Extended Properties [lms].[LMSGrade] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A grade assigned to a user in a section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSGrade'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the grade.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSGrade', @level2type=N'COLUMN', @level2name=N'LMSGradeIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a user by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSGrade', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the grade data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSGrade', @level2type=N'COLUMN', @level2name=N'SourceSystem'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSGrade', @level2type=N'COLUMN', @level2name=N'LMSUserIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSGrade', @level2type=N'COLUMN', @level2name=N'LMSSectionIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user section association.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSGrade', @level2type=N'COLUMN', @level2name=N'LMSUserLMSSectionAssociationIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The user''s letter or numeric grade for the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSGrade', @level2type=N'COLUMN', @level2name=N'Grade'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The type of grade reported. E.g., Current, Final.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSGrade', @level2type=N'COLUMN', @level2name=N'GradeType'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSGrade', @level2type=N'COLUMN', @level2name=N'SourceCreateDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSGrade', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSGrade', @level2type=N'COLUMN', @level2name=N'DeletedAt'
GO

-- Extended Properties [lms].[LMSSection] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'An organized grouping of course content and users over a period of time for the purpose of providing instruction.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'LMSSectionIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a user by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the section data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'SourceSystem'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The section identifier defined in the Student Information System (SIS).', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'SISSectionIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The section title or name.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'Title'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The section description.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'SectionDescription'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The enrollment term for the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'Term'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The section status from the source system. E.g., Published, Completed.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'LMSSectionStatus'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'SourceCreateDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSection', @level2type=N'COLUMN', @level2name=N'DeletedAt'
GO

-- Extended Properties [lms].[LMSSectionActivity] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A section activity performed by a user within the instructional system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSectionActivity'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the section activity.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSectionActivity', @level2type=N'COLUMN', @level2name=N'LMSSectionActivityIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a section activity by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSectionActivity', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the user data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSectionActivity', @level2type=N'COLUMN', @level2name=N'SourceSystem'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSectionActivity', @level2type=N'COLUMN', @level2name=N'LMSUserIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSectionActivity', @level2type=N'COLUMN', @level2name=N'LMSSectionIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The type of activity. E.g., Discussion Post.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSectionActivity', @level2type=N'COLUMN', @level2name=N'ActivityType'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date/time the activity occurred.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSectionActivity', @level2type=N'COLUMN', @level2name=N'ActivityDateTime'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The activity status.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSectionActivity', @level2type=N'COLUMN', @level2name=N'ActivityStatus'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The unique identifier assigned to the parent section activity.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSectionActivity', @level2type=N'COLUMN', @level2name=N'ParentSourceSystemIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The total activity time in minutes.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSectionActivity', @level2type=N'COLUMN', @level2name=N'ActivityTimeInMinutes'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSectionActivity', @level2type=N'COLUMN', @level2name=N'SourceCreateDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSectionActivity', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSectionActivity', @level2type=N'COLUMN', @level2name=N'DeletedAt'
GO

-- Extended Properties [lms].[LMSSystemActivity] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'An activity performed by a user within the instructional system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the section activity.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'LMSSystemActivityIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a system activity by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the user data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'SourceSystem'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'LMSUserIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The type of activity. E.g., Account Access/Log In.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'ActivityType'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date/time the activity occurred.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'ActivityDateTime'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The activity status.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'ActivityStatus'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The unique identifier assigned to the parent system activity.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'ParentSourceSystemIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The total activity time in minutes.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'ActivityTimeInMinutes'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'SourceCreateDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSSystemActivity', @level2type=N'COLUMN', @level2name=N'DeletedAt'
GO

-- Extended Properties [lms].[LMSUser] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A person using the instructional system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'LMSUserIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a user by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the user data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'SourceSystem'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The role assigned to the user. E.g., Student, Teacher, Administrator.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'UserRole'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The user identifier defined in the Student Information System (SIS).', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'SISUserIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The user identifier assigned by a school or district.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'LocalUserIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The full name of the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'Name'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The primary e-mail address for the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'EmailAddress'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'SourceCreateDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUser', @level2type=N'COLUMN', @level2name=N'DeletedAt'
GO

-- Extended Properties [lms].[LMSUserAttendanceEvent] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Attendance statuses assigned to users for a specific date.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user attendance event.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'LMSUserAttendanceEventIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a user by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the user data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'SourceSystem'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'LMSUserIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'LMSSectionIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user section association.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'LMSUserLMSSectionAssociationIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date of the attendance event.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'EventDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A code describing the attendance event. E.g., In Attendance, Excused Absence, Unexcused Absence.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'AttendanceStatus'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'SourceCreateDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time at which a record was detected as no longer available from the source system, and thus should be treated as ''deleted''.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserAttendanceEvent', @level2type=N'COLUMN', @level2name=N'DeletedAt'
GO

-- Extended Properties [lms].[LMSUserLMSSectionAssociation] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The association of a user and section. For a student, this would be a section enrollment. For a teacher, this would be a section assignment.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the section.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'LMSSectionIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'LMSUserIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the user section association.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'LMSUserLMSSectionAssociationIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique number or alphanumeric code assigned to a user by the source system.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'SourceSystemIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the user data.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'SourceSystem'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The status of the user section association. E.g., Active, Inactive, Withdrawn.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'EnrollmentStatus'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was created.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'SourceCreateDate'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The source system datetime the record was last modified.', @level0type=N'SCHEMA', @level0name=N'lms', @level1type=N'TABLE', @level1name=N'LMSUserLMSSectionAssociation', @level2type=N'COLUMN', @level2name=N'SourceLastModifiedDate'
GO

