CREATE FUNCTION tracked_deletes_lmsx.AssignmentCategoryDescriptor_TR_DelTrkg()
    RETURNS trigger AS
$BODY$
BEGIN
    INSERT INTO tracked_deletes_lmsx.AssignmentCategoryDescriptor(AssignmentCategoryDescriptorId, Id, ChangeVersion)
    SELECT OLD.AssignmentCategoryDescriptorId, Id, nextval('changes.ChangeVersionSequence')
    FROM edfi.Descriptor WHERE DescriptorId = OLD.AssignmentCategoryDescriptorId;
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER TrackDeletes AFTER DELETE ON lmsx.AssignmentCategoryDescriptor 
    FOR EACH ROW EXECUTE PROCEDURE tracked_deletes_lmsx.AssignmentCategoryDescriptor_TR_DelTrkg();

CREATE FUNCTION tracked_deletes_lmsx.AssignmentSubmission_TR_DelTrkg()
    RETURNS trigger AS
$BODY$
BEGIN
    INSERT INTO tracked_deletes_lmsx.AssignmentSubmission(AssignmentSubmissionIdentifier, Namespace, StudentUSI, Id, ChangeVersion)
    VALUES (OLD.AssignmentSubmissionIdentifier, OLD.Namespace, OLD.StudentUSI, OLD.Id, nextval('changes.ChangeVersionSequence'));
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER TrackDeletes AFTER DELETE ON lmsx.AssignmentSubmission 
    FOR EACH ROW EXECUTE PROCEDURE tracked_deletes_lmsx.AssignmentSubmission_TR_DelTrkg();

CREATE FUNCTION tracked_deletes_lmsx.Assignment_TR_DelTrkg()
    RETURNS trigger AS
$BODY$
BEGIN
    INSERT INTO tracked_deletes_lmsx.Assignment(AssignmentIdentifier, Namespace, Id, ChangeVersion)
    VALUES (OLD.AssignmentIdentifier, OLD.Namespace, OLD.Id, nextval('changes.ChangeVersionSequence'));
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER TrackDeletes AFTER DELETE ON lmsx.Assignment 
    FOR EACH ROW EXECUTE PROCEDURE tracked_deletes_lmsx.Assignment_TR_DelTrkg();

CREATE FUNCTION tracked_deletes_lmsx.LMSSourceSystemDescriptor_TR_DelTrkg()
    RETURNS trigger AS
$BODY$
BEGIN
    INSERT INTO tracked_deletes_lmsx.LMSSourceSystemDescriptor(LMSSourceSystemDescriptorId, Id, ChangeVersion)
    SELECT OLD.LMSSourceSystemDescriptorId, Id, nextval('changes.ChangeVersionSequence')
    FROM edfi.Descriptor WHERE DescriptorId = OLD.LMSSourceSystemDescriptorId;
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER TrackDeletes AFTER DELETE ON lmsx.LMSSourceSystemDescriptor 
    FOR EACH ROW EXECUTE PROCEDURE tracked_deletes_lmsx.LMSSourceSystemDescriptor_TR_DelTrkg();

CREATE FUNCTION tracked_deletes_lmsx.SubmissionStatusDescriptor_TR_DelTrkg()
    RETURNS trigger AS
$BODY$
BEGIN
    INSERT INTO tracked_deletes_lmsx.SubmissionStatusDescriptor(SubmissionStatusDescriptorId, Id, ChangeVersion)
    SELECT OLD.SubmissionStatusDescriptorId, Id, nextval('changes.ChangeVersionSequence')
    FROM edfi.Descriptor WHERE DescriptorId = OLD.SubmissionStatusDescriptorId;
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER TrackDeletes AFTER DELETE ON lmsx.SubmissionStatusDescriptor 
    FOR EACH ROW EXECUTE PROCEDURE tracked_deletes_lmsx.SubmissionStatusDescriptor_TR_DelTrkg();

CREATE FUNCTION tracked_deletes_lmsx.SubmissionTypeDescriptor_TR_DelTrkg()
    RETURNS trigger AS
$BODY$
BEGIN
    INSERT INTO tracked_deletes_lmsx.SubmissionTypeDescriptor(SubmissionTypeDescriptorId, Id, ChangeVersion)
    SELECT OLD.SubmissionTypeDescriptorId, Id, nextval('changes.ChangeVersionSequence')
    FROM edfi.Descriptor WHERE DescriptorId = OLD.SubmissionTypeDescriptorId;
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER TrackDeletes AFTER DELETE ON lmsx.SubmissionTypeDescriptor 
    FOR EACH ROW EXECUTE PROCEDURE tracked_deletes_lmsx.SubmissionTypeDescriptor_TR_DelTrkg();

