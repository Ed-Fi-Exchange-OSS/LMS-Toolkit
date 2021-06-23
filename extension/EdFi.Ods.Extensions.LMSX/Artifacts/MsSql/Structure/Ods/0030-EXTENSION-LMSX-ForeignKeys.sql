ALTER TABLE [edfilms].[Assignment] WITH CHECK ADD CONSTRAINT [FK_Assignment_AssignmentCategoryDescriptor] FOREIGN KEY ([AssignmentCategoryDescriptorId])
REFERENCES [edfilms].[AssignmentCategoryDescriptor] ([AssignmentCategoryDescriptorId])
GO

CREATE NONCLUSTERED INDEX [FK_Assignment_AssignmentCategoryDescriptor]
ON [edfilms].[Assignment] ([AssignmentCategoryDescriptorId] ASC)
GO

ALTER TABLE [edfilms].[Assignment] WITH CHECK ADD CONSTRAINT [FK_Assignment_LMSSourceSystemDescriptor] FOREIGN KEY ([LMSSourceSystemDescriptorId])
REFERENCES [edfilms].[LMSSourceSystemDescriptor] ([LMSSourceSystemDescriptorId])
GO

CREATE NONCLUSTERED INDEX [FK_Assignment_LMSSourceSystemDescriptor]
ON [edfilms].[Assignment] ([LMSSourceSystemDescriptorId] ASC)
GO

ALTER TABLE [edfilms].[Assignment] WITH CHECK ADD CONSTRAINT [FK_Assignment_Section] FOREIGN KEY ([LocalCourseCode], [SchoolId], [SchoolYear], [SectionIdentifier], [SessionName])
REFERENCES [edfi].[Section] ([LocalCourseCode], [SchoolId], [SchoolYear], [SectionIdentifier], [SessionName])
ON UPDATE CASCADE
GO

CREATE NONCLUSTERED INDEX [FK_Assignment_Section]
ON [edfilms].[Assignment] ([LocalCourseCode] ASC, [SchoolId] ASC, [SchoolYear] ASC, [SectionIdentifier] ASC, [SessionName] ASC)
GO

ALTER TABLE [edfilms].[AssignmentCategoryDescriptor] WITH CHECK ADD CONSTRAINT [FK_AssignmentCategoryDescriptor_Descriptor] FOREIGN KEY ([AssignmentCategoryDescriptorId])
REFERENCES [edfi].[Descriptor] ([DescriptorId])
ON DELETE CASCADE
GO

ALTER TABLE [edfilms].[AssignmentSubmission] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmission_Assignment] FOREIGN KEY ([AssignmentIdentifier])
REFERENCES [edfilms].[Assignment] ([AssignmentIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmission_Assignment]
ON [edfilms].[AssignmentSubmission] ([AssignmentIdentifier] ASC)
GO

ALTER TABLE [edfilms].[AssignmentSubmission] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmission_Student] FOREIGN KEY ([StudentUSI])
REFERENCES [edfi].[Student] ([StudentUSI])
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmission_Student]
ON [edfilms].[AssignmentSubmission] ([StudentUSI] ASC)
GO

ALTER TABLE [edfilms].[AssignmentSubmission] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmission_SubmissionStatusDescriptor] FOREIGN KEY ([SubmissionStatusDescriptorId])
REFERENCES [edfilms].[SubmissionStatusDescriptor] ([SubmissionStatusDescriptorId])
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmission_SubmissionStatusDescriptor]
ON [edfilms].[AssignmentSubmission] ([SubmissionStatusDescriptorId] ASC)
GO

ALTER TABLE [edfilms].[AssignmentSubmissionType] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmissionType_Assignment] FOREIGN KEY ([AssignmentIdentifier])
REFERENCES [edfilms].[Assignment] ([AssignmentIdentifier])
ON DELETE CASCADE
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmissionType_Assignment]
ON [edfilms].[AssignmentSubmissionType] ([AssignmentIdentifier] ASC)
GO

ALTER TABLE [edfilms].[AssignmentSubmissionType] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmissionType_SubmissionTypeDescriptor] FOREIGN KEY ([SubmissionTypeDescriptorId])
REFERENCES [edfilms].[SubmissionTypeDescriptor] ([SubmissionTypeDescriptorId])
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmissionType_SubmissionTypeDescriptor]
ON [edfilms].[AssignmentSubmissionType] ([SubmissionTypeDescriptorId] ASC)
GO

ALTER TABLE [edfilms].[LMSSourceSystemDescriptor] WITH CHECK ADD CONSTRAINT [FK_LMSSourceSystemDescriptor_Descriptor] FOREIGN KEY ([LMSSourceSystemDescriptorId])
REFERENCES [edfi].[Descriptor] ([DescriptorId])
ON DELETE CASCADE
GO

ALTER TABLE [edfilms].[SubmissionStatusDescriptor] WITH CHECK ADD CONSTRAINT [FK_SubmissionStatusDescriptor_Descriptor] FOREIGN KEY ([SubmissionStatusDescriptorId])
REFERENCES [edfi].[Descriptor] ([DescriptorId])
ON DELETE CASCADE
GO

ALTER TABLE [edfilms].[SubmissionTypeDescriptor] WITH CHECK ADD CONSTRAINT [FK_SubmissionTypeDescriptor_Descriptor] FOREIGN KEY ([SubmissionTypeDescriptorId])
REFERENCES [edfi].[Descriptor] ([DescriptorId])
ON DELETE CASCADE
GO

