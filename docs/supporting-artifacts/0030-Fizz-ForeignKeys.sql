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

ALTER TABLE [fizz].[AssignmentSubmission] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmission_LMSUser] FOREIGN KEY ([LMSUserIdentifier])
REFERENCES [fizz].[LMSUser] ([LMSUserIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmission_LMSUser]
ON [fizz].[AssignmentSubmission] ([LMSUserIdentifier] ASC)
GO

ALTER TABLE [fizz].[AssignmentSubmissionType] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmissionType_Assignment] FOREIGN KEY ([AssignmentIdentifier])
REFERENCES [fizz].[Assignment] ([AssignmentIdentifier])
ON DELETE CASCADE
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmissionType_Assignment]
ON [fizz].[AssignmentSubmissionType] ([AssignmentIdentifier] ASC)
GO

ALTER TABLE [fizz].[LMSGrade] WITH CHECK ADD CONSTRAINT [FK_LMSGrade_LMSUserLMSSectionAssociation] FOREIGN KEY ([LMSSectionIdentifier], [LMSUserIdentifier], [LMSUserLMSSectionAssociationIdentifier])
REFERENCES [fizz].[LMSUserLMSSectionAssociation] ([LMSSectionIdentifier], [LMSUserIdentifier], [LMSUserLMSSectionAssociationIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSGrade_LMSUserLMSSectionAssociation]
ON [fizz].[LMSGrade] ([LMSSectionIdentifier] ASC, [LMSUserIdentifier] ASC, [LMSUserLMSSectionAssociationIdentifier] ASC)
GO

ALTER TABLE [fizz].[LMSUserActivity] WITH CHECK ADD CONSTRAINT [FK_LMSUserActivity_Assignment] FOREIGN KEY ([AssignmentIdentifier])
REFERENCES [fizz].[Assignment] ([AssignmentIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSUserActivity_Assignment]
ON [fizz].[LMSUserActivity] ([AssignmentIdentifier] ASC)
GO

ALTER TABLE [fizz].[LMSUserActivity] WITH CHECK ADD CONSTRAINT [FK_LMSUserActivity_LMSSection] FOREIGN KEY ([LMSSectionIdentifier])
REFERENCES [fizz].[LMSSection] ([LMSSectionIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSUserActivity_LMSSection]
ON [fizz].[LMSUserActivity] ([LMSSectionIdentifier] ASC)
GO

ALTER TABLE [fizz].[LMSUserActivity] WITH CHECK ADD CONSTRAINT [FK_LMSUserActivity_LMSUser] FOREIGN KEY ([LMSUserIdentifier])
REFERENCES [fizz].[LMSUser] ([LMSUserIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSUserActivity_LMSUser]
ON [fizz].[LMSUserActivity] ([LMSUserIdentifier] ASC)
GO

ALTER TABLE [fizz].[LMSUserAttendanceEvent] WITH CHECK ADD CONSTRAINT [FK_LMSUserAttendanceEvent_LMSUser] FOREIGN KEY ([LMSUserIdentifier])
REFERENCES [fizz].[LMSUser] ([LMSUserIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSUserAttendanceEvent_LMSUser]
ON [fizz].[LMSUserAttendanceEvent] ([LMSUserIdentifier] ASC)
GO

ALTER TABLE [fizz].[LMSUserAttendanceEvent] WITH CHECK ADD CONSTRAINT [FK_LMSUserAttendanceEvent_LMSUserLMSSectionAssociation] FOREIGN KEY ([LMSSectionIdentifier], [LMSUserIdentifier], [LMSUserLMSSectionAssociationIdentifier])
REFERENCES [fizz].[LMSUserLMSSectionAssociation] ([LMSSectionIdentifier], [LMSUserIdentifier], [LMSUserLMSSectionAssociationIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSUserAttendanceEvent_LMSUserLMSSectionAssociation]
ON [fizz].[LMSUserAttendanceEvent] ([LMSSectionIdentifier] ASC, [LMSUserIdentifier] ASC, [LMSUserLMSSectionAssociationIdentifier] ASC)
GO

ALTER TABLE [fizz].[LMSUserLMSSectionAssociation] WITH CHECK ADD CONSTRAINT [FK_LMSUserLMSSectionAssociation_LMSSection] FOREIGN KEY ([LMSSectionIdentifier])
REFERENCES [fizz].[LMSSection] ([LMSSectionIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSUserLMSSectionAssociation_LMSSection]
ON [fizz].[LMSUserLMSSectionAssociation] ([LMSSectionIdentifier] ASC)
GO

ALTER TABLE [fizz].[LMSUserLMSSectionAssociation] WITH CHECK ADD CONSTRAINT [FK_LMSUserLMSSectionAssociation_LMSUser] FOREIGN KEY ([LMSUserIdentifier])
REFERENCES [fizz].[LMSUser] ([LMSUserIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSUserLMSSectionAssociation_LMSUser]
ON [fizz].[LMSUserLMSSectionAssociation] ([LMSUserIdentifier] ASC)
GO

