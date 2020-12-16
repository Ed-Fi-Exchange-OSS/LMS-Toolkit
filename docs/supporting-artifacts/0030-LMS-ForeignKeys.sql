ALTER TABLE [lms].[Assignment] WITH CHECK ADD CONSTRAINT [FK_Assignment_LMSSection] FOREIGN KEY ([LMSSectionIdentifier])
REFERENCES [lms].[LMSSection] ([LMSSectionIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_Assignment_LMSSection]
ON [lms].[Assignment] ([LMSSectionIdentifier] ASC)
GO

ALTER TABLE [lms].[AssignmentSubmission] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmission_Assignment] FOREIGN KEY ([AssignmentIdentifier])
REFERENCES [lms].[Assignment] ([AssignmentIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmission_Assignment]
ON [lms].[AssignmentSubmission] ([AssignmentIdentifier] ASC)
GO

ALTER TABLE [lms].[AssignmentSubmission] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmission_LMSUser] FOREIGN KEY ([LMSUserIdentifier])
REFERENCES [lms].[LMSUser] ([LMSUserIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmission_LMSUser]
ON [lms].[AssignmentSubmission] ([LMSUserIdentifier] ASC)
GO

ALTER TABLE [lms].[AssignmentSubmissionType] WITH CHECK ADD CONSTRAINT [FK_AssignmentSubmissionType_Assignment] FOREIGN KEY ([AssignmentIdentifier])
REFERENCES [lms].[Assignment] ([AssignmentIdentifier])
ON DELETE CASCADE
GO

CREATE NONCLUSTERED INDEX [FK_AssignmentSubmissionType_Assignment]
ON [lms].[AssignmentSubmissionType] ([AssignmentIdentifier] ASC)
GO

ALTER TABLE [lms].[LMSGrade] WITH CHECK ADD CONSTRAINT [FK_LMSGrade_LMSUserLMSSectionAssociation] FOREIGN KEY ([LMSSectionIdentifier], [LMSUserIdentifier], [LMSUserLMSSectionAssociationIdentifier])
REFERENCES [lms].[LMSUserLMSSectionAssociation] ([LMSSectionIdentifier], [LMSUserIdentifier], [LMSUserLMSSectionAssociationIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSGrade_LMSUserLMSSectionAssociation]
ON [lms].[LMSGrade] ([LMSSectionIdentifier] ASC, [LMSUserIdentifier] ASC, [LMSUserLMSSectionAssociationIdentifier] ASC)
GO

ALTER TABLE [lms].[LMSSectionActivity] WITH CHECK ADD CONSTRAINT [FK_LMSSectionActivity_LMSSection] FOREIGN KEY ([LMSSectionIdentifier])
REFERENCES [lms].[LMSSection] ([LMSSectionIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSSectionActivity_LMSSection]
ON [lms].[LMSSectionActivity] ([LMSSectionIdentifier] ASC)
GO

ALTER TABLE [lms].[LMSSectionActivity] WITH CHECK ADD CONSTRAINT [FK_LMSSectionActivity_LMSUser] FOREIGN KEY ([LMSUserIdentifier])
REFERENCES [lms].[LMSUser] ([LMSUserIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSSectionActivity_LMSUser]
ON [lms].[LMSSectionActivity] ([LMSUserIdentifier] ASC)
GO

ALTER TABLE [lms].[LMSSystemActivity] WITH CHECK ADD CONSTRAINT [FK_LMSSystemActivity_LMSUser] FOREIGN KEY ([LMSUserIdentifier])
REFERENCES [lms].[LMSUser] ([LMSUserIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSSystemActivity_LMSUser]
ON [lms].[LMSSystemActivity] ([LMSUserIdentifier] ASC)
GO

ALTER TABLE [lms].[LMSUserAttendanceEvent] WITH CHECK ADD CONSTRAINT [FK_LMSUserAttendanceEvent_LMSUser] FOREIGN KEY ([LMSUserIdentifier])
REFERENCES [lms].[LMSUser] ([LMSUserIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSUserAttendanceEvent_LMSUser]
ON [lms].[LMSUserAttendanceEvent] ([LMSUserIdentifier] ASC)
GO

ALTER TABLE [lms].[LMSUserAttendanceEvent] WITH CHECK ADD CONSTRAINT [FK_LMSUserAttendanceEvent_LMSUserLMSSectionAssociation] FOREIGN KEY ([LMSSectionIdentifier], [LMSUserIdentifier], [LMSUserLMSSectionAssociationIdentifier])
REFERENCES [lms].[LMSUserLMSSectionAssociation] ([LMSSectionIdentifier], [LMSUserIdentifier], [LMSUserLMSSectionAssociationIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSUserAttendanceEvent_LMSUserLMSSectionAssociation]
ON [lms].[LMSUserAttendanceEvent] ([LMSSectionIdentifier] ASC, [LMSUserIdentifier] ASC, [LMSUserLMSSectionAssociationIdentifier] ASC)
GO

ALTER TABLE [lms].[LMSUserLMSSectionAssociation] WITH CHECK ADD CONSTRAINT [FK_LMSUserLMSSectionAssociation_LMSSection] FOREIGN KEY ([LMSSectionIdentifier])
REFERENCES [lms].[LMSSection] ([LMSSectionIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSUserLMSSectionAssociation_LMSSection]
ON [lms].[LMSUserLMSSectionAssociation] ([LMSSectionIdentifier] ASC)
GO

ALTER TABLE [lms].[LMSUserLMSSectionAssociation] WITH CHECK ADD CONSTRAINT [FK_LMSUserLMSSectionAssociation_LMSUser] FOREIGN KEY ([LMSUserIdentifier])
REFERENCES [lms].[LMSUser] ([LMSUserIdentifier])
GO

CREATE NONCLUSTERED INDEX [FK_LMSUserLMSSectionAssociation_LMSUser]
ON [lms].[LMSUserLMSSectionAssociation] ([LMSUserIdentifier] ASC)
GO

