ALTER TABLE [lmsx].[Assignment] WITH CHECK ADD CONSTRAINT [FK_Assignment_AssignmentCategoryDescriptor] FOREIGN KEY ([AssignmentCategoryDescriptorId])
REFERENCES [lmsx].[AssignmentCategoryDescriptor] ([AssignmentCategoryDescriptorId])
GO

CREATE NONCLUSTERED INDEX [FK_Assignment_AssignmentCategoryDescriptor]
ON [lmsx].[Assignment] ([AssignmentCategoryDescriptorId] ASC)
GO

ALTER TABLE [lmsx].[Assignment] WITH CHECK ADD CONSTRAINT [FK_Assignment_LMSSourceSystemDescriptor] FOREIGN KEY ([LMSSourceSystemDescriptorId])
REFERENCES [lmsx].[LMSSourceSystemDescriptor] ([LMSSourceSystemDescriptorId])
GO

CREATE NONCLUSTERED INDEX [FK_Assignment_LMSSourceSystemDescriptor]
ON [lmsx].[Assignment] ([LMSSourceSystemDescriptorId] ASC)
GO

ALTER TABLE [lmsx].[Assignment] WITH CHECK ADD CONSTRAINT [FK_Assignment_School] FOREIGN KEY ([SchoolId])
REFERENCES [edfi].[School] ([SchoolId])
GO

CREATE NONCLUSTERED INDEX [FK_Assignment_School]
ON [lmsx].[Assignment] ([SchoolId] ASC)
GO

ALTER TABLE [lmsx].[Assignment] WITH CHECK ADD CONSTRAINT [FK_Assignment_Section] FOREIGN KEY ([LocalCourseCode], [SchoolId], [SchoolYear], [SectionIdentifier], [SessionName])
REFERENCES [edfi].[Section] ([LocalCourseCode], [SchoolId], [SchoolYear], [SectionIdentifier], [SessionName])
ON UPDATE CASCADE
GO

CREATE NONCLUSTERED INDEX [FK_Assignment_Section]
ON [lmsx].[Assignment] ([LocalCourseCode] ASC, [SchoolId] ASC, [SchoolYear] ASC, [SectionIdentifier] ASC, [SessionName] ASC)
GO

ALTER TABLE [lmsx].[AssignmentCategoryDescriptor] WITH CHECK ADD CONSTRAINT [FK_AssignmentCategoryDescriptor_Descriptor] FOREIGN KEY ([AssignmentCategoryDescriptorId])
REFERENCES [edfi].[Descriptor] ([DescriptorId])
ON DELETE CASCADE
GO

ALTER TABLE [lmsx].[AssignmentSubmission] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmission_Assignment] FOREIGN KEY ([AssignmentIdentifier], [SchoolId])
REFERENCES [lmsx].[Assignment] ([AssignmentIdentifier], [SchoolId])
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmission_Assignment]
ON [lmsx].[AssignmentSubmission] ([AssignmentIdentifier] ASC, [SchoolId] ASC)
GO

ALTER TABLE [lmsx].[AssignmentSubmission] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmission_Student] FOREIGN KEY ([StudentUSI])
REFERENCES [edfi].[Student] ([StudentUSI])
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmission_Student]
ON [lmsx].[AssignmentSubmission] ([StudentUSI] ASC)
GO

ALTER TABLE [lmsx].[AssignmentSubmission] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmission_SubmissionStatusDescriptor] FOREIGN KEY ([SubmissionStatusDescriptorId])
REFERENCES [lmsx].[SubmissionStatusDescriptor] ([SubmissionStatusDescriptorId])
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmission_SubmissionStatusDescriptor]
ON [lmsx].[AssignmentSubmission] ([SubmissionStatusDescriptorId] ASC)
GO

ALTER TABLE [lmsx].[AssignmentSubmissionType] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmissionType_Assignment] FOREIGN KEY ([AssignmentIdentifier], [SchoolId])
REFERENCES [lmsx].[Assignment] ([AssignmentIdentifier], [SchoolId])
ON DELETE CASCADE
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmissionType_Assignment]
ON [lmsx].[AssignmentSubmissionType] ([AssignmentIdentifier] ASC, [SchoolId] ASC)
GO

ALTER TABLE [lmsx].[AssignmentSubmissionType] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmissionType_SubmissionTypeDescriptor] FOREIGN KEY ([SubmissionTypeDescriptorId])
REFERENCES [lmsx].[SubmissionTypeDescriptor] ([SubmissionTypeDescriptorId])
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmissionType_SubmissionTypeDescriptor]
ON [lmsx].[AssignmentSubmissionType] ([SubmissionTypeDescriptorId] ASC)
GO

ALTER TABLE [lmsx].[LMSSourceSystemDescriptor] WITH CHECK ADD CONSTRAINT [FK_LMSSourceSystemDescriptor_Descriptor] FOREIGN KEY ([LMSSourceSystemDescriptorId])
REFERENCES [edfi].[Descriptor] ([DescriptorId])
ON DELETE CASCADE
GO

ALTER TABLE [lmsx].[SubmissionStatusDescriptor] WITH CHECK ADD CONSTRAINT [FK_SubmissionStatusDescriptor_Descriptor] FOREIGN KEY ([SubmissionStatusDescriptorId])
REFERENCES [edfi].[Descriptor] ([DescriptorId])
ON DELETE CASCADE
GO

ALTER TABLE [lmsx].[SubmissionTypeDescriptor] WITH CHECK ADD CONSTRAINT [FK_SubmissionTypeDescriptor_Descriptor] FOREIGN KEY ([SubmissionTypeDescriptorId])
REFERENCES [edfi].[Descriptor] ([DescriptorId])
ON DELETE CASCADE
GO

