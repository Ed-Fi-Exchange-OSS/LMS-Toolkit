-- Extended Properties [lmsx].[Assignment] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Course work assigned to students enrolled in a section.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique string assigned to the assignment, based on the source system of record.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'AssignmentIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Namespace for the Assignment.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'Namespace'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The system code or name providing the assignment data.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'LMSSourceSystemDescriptorId'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The assignment title or name.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'Title'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The category or type of assignment.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'AssignmentCategoryDescriptorId'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The assignment description.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'AssignmentDescription'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The start date and time for the assignment. Students will have access to the assignment after this date.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'StartDateTime'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The end date and time for the assignment. Students will no longer have access to the assignment after this date.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'EndDateTime'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time the assignment is due.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'DueDateTime'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The maximum number of points a student may receive for a submission of the assignment.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'MaxPoints'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The local identifier assigned to a section.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'SectionIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The local code assigned by the School that identifies the course offering provided for the instruction of students.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'LocalCourseCode'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The identifier for the calendar for the academic session (e.g., 2010/11, 2011 Summer).', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'SessionName'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The identifier for the school year.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'SchoolYear'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The identifier assigned to a school.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'Assignment', @level2type=N'COLUMN', @level2name=N'SchoolId'
GO

-- Extended Properties [lmsx].[AssignmentCategoryDescriptor] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The category or type of assignment.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentCategoryDescriptor'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique identifier used as Primary Key, not derived from business logic, when acting as Foreign Key, references the parent table.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentCategoryDescriptor', @level2type=N'COLUMN', @level2name=N'AssignmentCategoryDescriptorId'
GO

-- Extended Properties [lmsx].[AssignmentSubmission] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A user''s submission of course work for an assignment.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentSubmission'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique numeric identifier assigned to the submission.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'AssignmentSubmissionIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Namespace for the AssignmentSubmission.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'Namespace'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique alphanumeric code assigned to a student.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'StudentUSI'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique string assigned to the assignment, based on the source system of record.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'AssignmentIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The status of the submission in relation to the late acceptance policy.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'SubmissionStatusDescriptorId'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The date and time of the assignment submission.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'SubmissionDateTime'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The points earned for the submission.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'EarnedPoints'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The grade received for the submission.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentSubmission', @level2type=N'COLUMN', @level2name=N'Grade'
GO

-- Extended Properties [lmsx].[AssignmentSubmissionType] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The type(s) of submissions available for the assignment.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentSubmissionType'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique string assigned to the assignment, based on the source system of record.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentSubmissionType', @level2type=N'COLUMN', @level2name=N'AssignmentIdentifier'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'Namespace for the Assignment.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentSubmissionType', @level2type=N'COLUMN', @level2name=N'Namespace'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The type(s) of submissions available for the assignment.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'AssignmentSubmissionType', @level2type=N'COLUMN', @level2name=N'SubmissionTypeDescriptorId'
GO

-- Extended Properties [lmsx].[LMSSourceSystemDescriptor] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The Learning Management System (LMS) source system', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'LMSSourceSystemDescriptor'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique identifier used as Primary Key, not derived from business logic, when acting as Foreign Key, references the parent table.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'LMSSourceSystemDescriptor', @level2type=N'COLUMN', @level2name=N'LMSSourceSystemDescriptorId'
GO

-- Extended Properties [lmsx].[SubmissionStatusDescriptor] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The status of the submission in relation to the late acceptance policy.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'SubmissionStatusDescriptor'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique identifier used as Primary Key, not derived from business logic, when acting as Foreign Key, references the parent table.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'SubmissionStatusDescriptor', @level2type=N'COLUMN', @level2name=N'SubmissionStatusDescriptorId'
GO

-- Extended Properties [lmsx].[SubmissionTypeDescriptor] --
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'The type(s) of submissions available for the assignment.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'SubmissionTypeDescriptor'
GO
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'A unique identifier used as Primary Key, not derived from business logic, when acting as Foreign Key, references the parent table.', @level0type=N'SCHEMA', @level0name=N'lmsx', @level1type=N'TABLE', @level1name=N'SubmissionTypeDescriptor', @level2type=N'COLUMN', @level2name=N'SubmissionTypeDescriptorId'
GO

