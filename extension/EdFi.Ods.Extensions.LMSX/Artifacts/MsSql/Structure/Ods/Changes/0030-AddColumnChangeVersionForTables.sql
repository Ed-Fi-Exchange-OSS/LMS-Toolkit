IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[lmsx].[Assignment]') AND name = 'ChangeVersion')
ALTER TABLE [lmsx].[Assignment] ADD [ChangeVersion] [BIGINT] DEFAULT (NEXT VALUE FOR [changes].[ChangeVersionSequence]) NOT NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[lmsx].[AssignmentSubmission]') AND name = 'ChangeVersion')
ALTER TABLE [lmsx].[AssignmentSubmission] ADD [ChangeVersion] [BIGINT] DEFAULT (NEXT VALUE FOR [changes].[ChangeVersionSequence]) NOT NULL;

