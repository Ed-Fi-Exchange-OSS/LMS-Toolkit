ALTER TABLE [fizz].[Assignment] WITH CHECK ADD CONSTRAINT [FK_Assignment_LMSSection] FOREIGN KEY ([LMSSectionIdentifier])
REFERENCES [fizz].[LMSSection] ([LMSSectionIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_Assignment_LMSSection]
ON [fizz].[Assignment] ([LMSSectionIdentifier] ASC)
GO

ALTER TABLE [fizz].[AssignmentSubmission] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmission_Assignment] FOREIGN KEY ([AssignmentIdentifier])
REFERENCES [fizz].[Assignment] ([AssignmentIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmission_Assignment]
ON [fizz].[AssignmentSubmission] ([AssignmentIdentifier] ASC)
GO

ALTER TABLE [fizz].[AssignmentSubmission] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmission_User] FOREIGN KEY ([UserIdentifier])
REFERENCES [fizz].[User] ([UserIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmission_User]
ON [fizz].[AssignmentSubmission] ([UserIdentifier] ASC)
GO

ALTER TABLE [fizz].[AssignmentSubmissionType] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmissionType_Assignment] FOREIGN KEY ([AssignmentIdentifier])
REFERENCES [fizz].[Assignment] ([AssignmentIdentifier])
ON DELETE CASCADE
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmissionType_Assignment]
ON [fizz].[AssignmentSubmissionType] ([AssignmentIdentifier] ASC)
GO

ALTER TABLE [fizz].[LMSGrade] WITH CHECK ADD CONSTRAINT [FK_LMSGrade_UserLMSSectionAssociation] FOREIGN KEY ([LMSSectionIdentifier], [UserIdentifier], [UserLMSSectionAssociationIdentifier])
REFERENCES [fizz].[UserLMSSectionAssociation] ([LMSSectionIdentifier], [UserIdentifier], [UserLMSSectionAssociationIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSGrade_UserLMSSectionAssociation]
ON [fizz].[LMSGrade] ([LMSSectionIdentifier] ASC, [UserIdentifier] ASC, [UserLMSSectionAssociationIdentifier] ASC)
GO

ALTER TABLE [fizz].[UserAttendanceEvent] WITH CHECK ADD CONSTRAINT [FK_UserAttendanceEvent_User] FOREIGN KEY ([UserIdentifier])
REFERENCES [fizz].[User] ([UserIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_UserAttendanceEvent_User]
ON [fizz].[UserAttendanceEvent] ([UserIdentifier] ASC)
GO

ALTER TABLE [fizz].[UserAttendanceEvent] WITH CHECK ADD CONSTRAINT [FK_UserAttendanceEvent_UserLMSSectionAssociation] FOREIGN KEY ([LMSSectionIdentifier], [UserIdentifier], [UserLMSSectionAssociationIdentifier])
REFERENCES [fizz].[UserLMSSectionAssociation] ([LMSSectionIdentifier], [UserIdentifier], [UserLMSSectionAssociationIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_UserAttendanceEvent_UserLMSSectionAssociation]
ON [fizz].[UserAttendanceEvent] ([LMSSectionIdentifier] ASC, [UserIdentifier] ASC, [UserLMSSectionAssociationIdentifier] ASC)
GO

ALTER TABLE [fizz].[UserLMSActivity] WITH CHECK ADD CONSTRAINT [FK_UserLMSActivity_Assignment] FOREIGN KEY ([AssignmentIdentifier])
REFERENCES [fizz].[Assignment] ([AssignmentIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_UserLMSActivity_Assignment]
ON [fizz].[UserLMSActivity] ([AssignmentIdentifier] ASC)
GO

ALTER TABLE [fizz].[UserLMSActivity] WITH CHECK ADD CONSTRAINT [FK_UserLMSActivity_LMSSection] FOREIGN KEY ([LMSSectionIdentifier])
REFERENCES [fizz].[LMSSection] ([LMSSectionIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_UserLMSActivity_LMSSection]
ON [fizz].[UserLMSActivity] ([LMSSectionIdentifier] ASC)
GO

ALTER TABLE [fizz].[UserLMSActivity] WITH CHECK ADD CONSTRAINT [FK_UserLMSActivity_User] FOREIGN KEY ([UserIdentifier])
REFERENCES [fizz].[User] ([UserIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_UserLMSActivity_User]
ON [fizz].[UserLMSActivity] ([UserIdentifier] ASC)
GO

ALTER TABLE [fizz].[UserLMSSectionAssociation] WITH CHECK ADD CONSTRAINT [FK_UserLMSSectionAssociation_LMSSection] FOREIGN KEY ([LMSSectionIdentifier])
REFERENCES [fizz].[LMSSection] ([LMSSectionIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_UserLMSSectionAssociation_LMSSection]
ON [fizz].[UserLMSSectionAssociation] ([LMSSectionIdentifier] ASC)
GO

ALTER TABLE [fizz].[UserLMSSectionAssociation] WITH CHECK ADD CONSTRAINT [FK_UserLMSSectionAssociation_User] FOREIGN KEY ([UserIdentifier])
REFERENCES [fizz].[User] ([UserIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_UserLMSSectionAssociation_User]
ON [fizz].[UserLMSSectionAssociation] ([UserIdentifier] ASC)
GO

