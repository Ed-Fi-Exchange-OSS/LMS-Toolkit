CREATE TRIGGER [lmsx].[lmsx_Assignment_TR_UpdateChangeVersion] ON [lmsx].[Assignment] AFTER UPDATE AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [lmsx].[Assignment]
    SET ChangeVersion = (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM [lmsx].[Assignment] u
    WHERE EXISTS (SELECT 1 FROM inserted i WHERE i.id = u.id);
END	
GO

CREATE TRIGGER [lmsx].[lmsx_AssignmentSubmission_TR_UpdateChangeVersion] ON [lmsx].[AssignmentSubmission] AFTER UPDATE AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [lmsx].[AssignmentSubmission]
    SET ChangeVersion = (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM [lmsx].[AssignmentSubmission] u
    WHERE EXISTS (SELECT 1 FROM inserted i WHERE i.id = u.id);
END	
GO

