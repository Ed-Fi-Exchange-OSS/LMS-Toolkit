CREATE TRIGGER [edfilms].[edfilms_AssignmentCategoryDescriptor_TR_DeleteTracking] ON [edfilms].[AssignmentCategoryDescriptor] AFTER DELETE AS
BEGIN
    IF @@rowcount = 0 
        RETURN

    SET NOCOUNT ON

    INSERT INTO [tracked_deletes_edfilms].[AssignmentCategoryDescriptor](AssignmentCategoryDescriptorId, Id, ChangeVersion)
    SELECT  d.AssignmentCategoryDescriptorId, Id, (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM    deleted d
            INNER JOIN edfi.Descriptor b ON d.AssignmentCategoryDescriptorId = b.DescriptorId
END
GO

ALTER TABLE [edfilms].[AssignmentCategoryDescriptor] ENABLE TRIGGER [edfilms_AssignmentCategoryDescriptor_TR_DeleteTracking]
GO


CREATE TRIGGER [edfilms].[edfilms_AssignmentSubmission_TR_DeleteTracking] ON [edfilms].[AssignmentSubmission] AFTER DELETE AS
BEGIN
    IF @@rowcount = 0 
        RETURN

    SET NOCOUNT ON

    INSERT INTO [tracked_deletes_edfilms].[AssignmentSubmission](AssignmentSubmissionIdentifier, Id, ChangeVersion)
    SELECT  AssignmentSubmissionIdentifier, Id, (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM    deleted d
END
GO

ALTER TABLE [edfilms].[AssignmentSubmission] ENABLE TRIGGER [edfilms_AssignmentSubmission_TR_DeleteTracking]
GO


CREATE TRIGGER [edfilms].[edfilms_Assignment_TR_DeleteTracking] ON [edfilms].[Assignment] AFTER DELETE AS
BEGIN
    IF @@rowcount = 0 
        RETURN

    SET NOCOUNT ON

    INSERT INTO [tracked_deletes_edfilms].[Assignment](AssignmentIdentifier, Id, ChangeVersion)
    SELECT  AssignmentIdentifier, Id, (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM    deleted d
END
GO

ALTER TABLE [edfilms].[Assignment] ENABLE TRIGGER [edfilms_Assignment_TR_DeleteTracking]
GO


CREATE TRIGGER [edfilms].[edfilms_LMSSourceSystemDescriptor_TR_DeleteTracking] ON [edfilms].[LMSSourceSystemDescriptor] AFTER DELETE AS
BEGIN
    IF @@rowcount = 0 
        RETURN

    SET NOCOUNT ON

    INSERT INTO [tracked_deletes_edfilms].[LMSSourceSystemDescriptor](LMSSourceSystemDescriptorId, Id, ChangeVersion)
    SELECT  d.LMSSourceSystemDescriptorId, Id, (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM    deleted d
            INNER JOIN edfi.Descriptor b ON d.LMSSourceSystemDescriptorId = b.DescriptorId
END
GO

ALTER TABLE [edfilms].[LMSSourceSystemDescriptor] ENABLE TRIGGER [edfilms_LMSSourceSystemDescriptor_TR_DeleteTracking]
GO


CREATE TRIGGER [edfilms].[edfilms_SubmissionStatusDescriptor_TR_DeleteTracking] ON [edfilms].[SubmissionStatusDescriptor] AFTER DELETE AS
BEGIN
    IF @@rowcount = 0 
        RETURN

    SET NOCOUNT ON

    INSERT INTO [tracked_deletes_edfilms].[SubmissionStatusDescriptor](SubmissionStatusDescriptorId, Id, ChangeVersion)
    SELECT  d.SubmissionStatusDescriptorId, Id, (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM    deleted d
            INNER JOIN edfi.Descriptor b ON d.SubmissionStatusDescriptorId = b.DescriptorId
END
GO

ALTER TABLE [edfilms].[SubmissionStatusDescriptor] ENABLE TRIGGER [edfilms_SubmissionStatusDescriptor_TR_DeleteTracking]
GO


CREATE TRIGGER [edfilms].[edfilms_SubmissionTypeDescriptor_TR_DeleteTracking] ON [edfilms].[SubmissionTypeDescriptor] AFTER DELETE AS
BEGIN
    IF @@rowcount = 0 
        RETURN

    SET NOCOUNT ON

    INSERT INTO [tracked_deletes_edfilms].[SubmissionTypeDescriptor](SubmissionTypeDescriptorId, Id, ChangeVersion)
    SELECT  d.SubmissionTypeDescriptorId, Id, (NEXT VALUE FOR [changes].[ChangeVersionSequence])
    FROM    deleted d
            INNER JOIN edfi.Descriptor b ON d.SubmissionTypeDescriptorId = b.DescriptorId
END
GO

ALTER TABLE [edfilms].[SubmissionTypeDescriptor] ENABLE TRIGGER [edfilms_SubmissionTypeDescriptor_TR_DeleteTracking]
GO


