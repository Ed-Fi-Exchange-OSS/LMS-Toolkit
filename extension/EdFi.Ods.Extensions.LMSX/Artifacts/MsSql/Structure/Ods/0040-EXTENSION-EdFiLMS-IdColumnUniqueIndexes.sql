BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'edfilms.Assignment') AND name = N'UX_Assignment_Id')
    CREATE UNIQUE NONCLUSTERED INDEX UX_Assignment_Id ON [edfilms].[Assignment]
    (Id) WITH (PAD_INDEX = ON, FILLFACTOR = 75, STATISTICS_NORECOMPUTE = OFF) ON [PRIMARY]
    GO
COMMIT

BEGIN TRANSACTION
    IF NOT EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'edfilms.AssignmentSubmission') AND name = N'UX_AssignmentSubmission_Id')
    CREATE UNIQUE NONCLUSTERED INDEX UX_AssignmentSubmission_Id ON [edfilms].[AssignmentSubmission]
    (Id) WITH (PAD_INDEX = ON, FILLFACTOR = 75, STATISTICS_NORECOMPUTE = OFF) ON [PRIMARY]
    GO
COMMIT

