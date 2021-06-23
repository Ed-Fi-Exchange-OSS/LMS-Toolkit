CREATE TRIGGER [edfilms].[edfilms_Assignment_TR_UpdateChangeVersion] ON [edfilms].[Assignment] AFTER UPDATE AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [edfilms].[Assignment]
    SET ChangeVersion = (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM [edfilms].[Assignment] u
    WHERE EXISTS (SELECT 1 FROM inserted i WHERE i.id = u.id);
END	
GO

CREATE TRIGGER [edfilms].[edfilms_AssignmentSubmission_TR_UpdateChangeVersion] ON [edfilms].[AssignmentSubmission] AFTER UPDATE AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [edfilms].[AssignmentSubmission]
    SET ChangeVersion = (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM [edfilms].[AssignmentSubmission] u
    WHERE EXISTS (SELECT 1 FROM inserted i WHERE i.id = u.id);
END	
GO

