BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'lmsx.Assignment') AND name = N'UX_Assignment_ChangeVersion')
    CREATE INDEX [UX_Assignment_ChangeVersion] ON [lmsx].[Assignment] ([ChangeVersion] ASC)
    GO
COMMIT

BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'lmsx.AssignmentSubmission') AND name = N'UX_AssignmentSubmission_ChangeVersion')
    CREATE INDEX [UX_AssignmentSubmission_ChangeVersion] ON [lmsx].[AssignmentSubmission] ([ChangeVersion] ASC)
    GO
COMMIT

