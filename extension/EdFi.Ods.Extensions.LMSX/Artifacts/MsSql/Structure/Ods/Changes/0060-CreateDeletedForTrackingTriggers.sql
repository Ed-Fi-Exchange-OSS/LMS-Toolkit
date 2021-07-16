CREATE TRIGGER [lmsx].[lmsx_AssignmentCategoryDescriptor_TR_DeleteTracking] ON [lmsx].[AssignmentCategoryDescriptor] AFTER DELETE AS
BEGIN
    IF @@rowcount = 0 
        RETURN

    SET NOCOUNT ON

    INSERT INTO [tracked_deletes_lmsx].[AssignmentCategoryDescriptor](AssignmentCategoryDescriptorId, Id, ChangeVersion)
    SELECT  d.AssignmentCategoryDescriptorId, Id, (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM    deleted d
            INNER JOIN edfi.Descriptor b ON d.AssignmentCategoryDescriptorId = b.DescriptorId
END
GO

ALTER TABLE [lmsx].[AssignmentCategoryDescriptor] ENABLE TRIGGER [lmsx_AssignmentCategoryDescriptor_TR_DeleteTracking]
GO


CREATE TRIGGER [lmsx].[lmsx_AssignmentSubmission_TR_DeleteTracking] ON [lmsx].[AssignmentSubmission] AFTER DELETE AS
BEGIN
    IF @@rowcount = 0 
        RETURN

    SET NOCOUNT ON

    INSERT INTO [tracked_deletes_lmsx].[AssignmentSubmission](AssignmentSubmissionIdentifier, Namespace, StudentUSI, Id, ChangeVersion)
    SELECT  AssignmentSubmissionIdentifier, Namespace, StudentUSI, Id, (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM    deleted d
END
GO

ALTER TABLE [lmsx].[AssignmentSubmission] ENABLE TRIGGER [lmsx_AssignmentSubmission_TR_DeleteTracking]
GO


CREATE TRIGGER [lmsx].[lmsx_Assignment_TR_DeleteTracking] ON [lmsx].[Assignment] AFTER DELETE AS
BEGIN
    IF @@rowcount = 0 
        RETURN

    SET NOCOUNT ON

    INSERT INTO [tracked_deletes_lmsx].[Assignment](AssignmentIdentifier, Namespace, Id, ChangeVersion)
    SELECT  AssignmentIdentifier, Namespace, Id, (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM    deleted d
END
GO

ALTER TABLE [lmsx].[Assignment] ENABLE TRIGGER [lmsx_Assignment_TR_DeleteTracking]
GO


CREATE TRIGGER [lmsx].[lmsx_LMSSourceSystemDescriptor_TR_DeleteTracking] ON [lmsx].[LMSSourceSystemDescriptor] AFTER DELETE AS
BEGIN
    IF @@rowcount = 0 
        RETURN

    SET NOCOUNT ON

    INSERT INTO [tracked_deletes_lmsx].[LMSSourceSystemDescriptor](LMSSourceSystemDescriptorId, Id, ChangeVersion)
    SELECT  d.LMSSourceSystemDescriptorId, Id, (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM    deleted d
            INNER JOIN edfi.Descriptor b ON d.LMSSourceSystemDescriptorId = b.DescriptorId
END
GO

ALTER TABLE [lmsx].[LMSSourceSystemDescriptor] ENABLE TRIGGER [lmsx_LMSSourceSystemDescriptor_TR_DeleteTracking]
GO


CREATE TRIGGER [lmsx].[lmsx_SubmissionStatusDescriptor_TR_DeleteTracking] ON [lmsx].[SubmissionStatusDescriptor] AFTER DELETE AS
BEGIN
    IF @@rowcount = 0 
        RETURN

    SET NOCOUNT ON

    INSERT INTO [tracked_deletes_lmsx].[SubmissionStatusDescriptor](SubmissionStatusDescriptorId, Id, ChangeVersion)
    SELECT  d.SubmissionStatusDescriptorId, Id, (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM    deleted d
            INNER JOIN edfi.Descriptor b ON d.SubmissionStatusDescriptorId = b.DescriptorId
END
GO

ALTER TABLE [lmsx].[SubmissionStatusDescriptor] ENABLE TRIGGER [lmsx_SubmissionStatusDescriptor_TR_DeleteTracking]
GO


CREATE TRIGGER [lmsx].[lmsx_SubmissionTypeDescriptor_TR_DeleteTracking] ON [lmsx].[SubmissionTypeDescriptor] AFTER DELETE AS
BEGIN
    IF @@rowcount = 0 
        RETURN

    SET NOCOUNT ON

    INSERT INTO [tracked_deletes_lmsx].[SubmissionTypeDescriptor](SubmissionTypeDescriptorId, Id, ChangeVersion)
    SELECT  d.SubmissionTypeDescriptorId, Id, (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM    deleted d
            INNER JOIN edfi.Descriptor b ON d.SubmissionTypeDescriptorId = b.DescriptorId
END
GO

ALTER TABLE [lmsx].[SubmissionTypeDescriptor] ENABLE TRIGGER [lmsx_SubmissionTypeDescriptor_TR_DeleteTracking]
GO


