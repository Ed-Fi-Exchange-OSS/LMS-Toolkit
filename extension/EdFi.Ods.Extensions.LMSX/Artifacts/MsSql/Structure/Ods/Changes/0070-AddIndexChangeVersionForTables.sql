BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'edfilms.Assignment') AND name = N'UX_Assignment_ChangeVersion')
    CREATE INDEX [UX_Assignment_ChangeVersion] ON [edfilms].[Assignment] ([ChangeVersion] ASC)
    GO
COMMIT

BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'edfilms.AssignmentSubmission') AND name = N'UX_AssignmentSubmission_ChangeVersion')
    CREATE INDEX [UX_AssignmentSubmission_ChangeVersion] ON [edfilms].[AssignmentSubmission] ([ChangeVersion] ASC)
    GO
COMMIT

