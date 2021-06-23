CREATE FUNCTION tracked_deletes_edfilms.AssignmentCategoryDescriptor_TR_DelTrkg()
    RETURNS trigger AS
$BODY$
BEGIN
    INSERT INTO tracked_deletes_edfilms.AssignmentCategoryDescriptor(AssignmentCategoryDescriptorId, Id, ChangeVersion)
    SELECT OLD.AssignmentCategoryDescriptorId, Id, nextval('changes.ChangeVersionSequence')
    FROM edfi.Descriptor WHERE DescriptorId = OLD.AssignmentCategoryDescriptorId;
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER TrackDeletes AFTER DELETE ON edfilms.AssignmentCategoryDescriptor 
    FOR EACH ROW EXECUTE PROCEDURE tracked_deletes_edfilms.AssignmentCategoryDescriptor_TR_DelTrkg();

CREATE FUNCTION tracked_deletes_edfilms.AssignmentSubmission_TR_DelTrkg()
    RETURNS trigger AS
$BODY$
BEGIN
    INSERT INTO tracked_deletes_edfilms.AssignmentSubmission(AssignmentSubmissionIdentifier, Id, ChangeVersion)
    VALUES (OLD.AssignmentSubmissionIdentifier, OLD.Id, nextval('changes.ChangeVersionSequence'));
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER TrackDeletes AFTER DELETE ON edfilms.AssignmentSubmission 
    FOR EACH ROW EXECUTE PROCEDURE tracked_deletes_edfilms.AssignmentSubmission_TR_DelTrkg();

CREATE FUNCTION tracked_deletes_edfilms.Assignment_TR_DelTrkg()
    RETURNS trigger AS
$BODY$
BEGIN
    INSERT INTO tracked_deletes_edfilms.Assignment(AssignmentIdentifier, Id, ChangeVersion)
    VALUES (OLD.AssignmentIdentifier, OLD.Id, nextval('changes.ChangeVersionSequence'));
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER TrackDeletes AFTER DELETE ON edfilms.Assignment 
    FOR EACH ROW EXECUTE PROCEDURE tracked_deletes_edfilms.Assignment_TR_DelTrkg();

CREATE FUNCTION tracked_deletes_edfilms.LMSSourceSystemDescriptor_TR_DelTrkg()
    RETURNS trigger AS
$BODY$
BEGIN
    INSERT INTO tracked_deletes_edfilms.LMSSourceSystemDescriptor(LMSSourceSystemDescriptorId, Id, ChangeVersion)
    SELECT OLD.LMSSourceSystemDescriptorId, Id, nextval('changes.ChangeVersionSequence')
    FROM edfi.Descriptor WHERE DescriptorId = OLD.LMSSourceSystemDescriptorId;
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER TrackDeletes AFTER DELETE ON edfilms.LMSSourceSystemDescriptor 
    FOR EACH ROW EXECUTE PROCEDURE tracked_deletes_edfilms.LMSSourceSystemDescriptor_TR_DelTrkg();

CREATE FUNCTION tracked_deletes_edfilms.SubmissionStatusDescriptor_TR_DelTrkg()
    RETURNS trigger AS
$BODY$
BEGIN
    INSERT INTO tracked_deletes_edfilms.SubmissionStatusDescriptor(SubmissionStatusDescriptorId, Id, ChangeVersion)
    SELECT OLD.SubmissionStatusDescriptorId, Id, nextval('changes.ChangeVersionSequence')
    FROM edfi.Descriptor WHERE DescriptorId = OLD.SubmissionStatusDescriptorId;
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER TrackDeletes AFTER DELETE ON edfilms.SubmissionStatusDescriptor 
    FOR EACH ROW EXECUTE PROCEDURE tracked_deletes_edfilms.SubmissionStatusDescriptor_TR_DelTrkg();

CREATE FUNCTION tracked_deletes_edfilms.SubmissionTypeDescriptor_TR_DelTrkg()
    RETURNS trigger AS
$BODY$
BEGIN
    INSERT INTO tracked_deletes_edfilms.SubmissionTypeDescriptor(SubmissionTypeDescriptorId, Id, ChangeVersion)
    SELECT OLD.SubmissionTypeDescriptorId, Id, nextval('changes.ChangeVersionSequence')
    FROM edfi.Descriptor WHERE DescriptorId = OLD.SubmissionTypeDescriptorId;
    RETURN NULL;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER TrackDeletes AFTER DELETE ON edfilms.SubmissionTypeDescriptor 
    FOR EACH ROW EXECUTE PROCEDURE tracked_deletes_edfilms.SubmissionTypeDescriptor_TR_DelTrkg();

