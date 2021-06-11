CREATE TRIGGER UpdateChangeVersion BEFORE UPDATE ON edfilms.Assignment
    FOR EACH ROW EXECUTE PROCEDURE changes.UpdateChangeVersion();

CREATE TRIGGER UpdateChangeVersion BEFORE UPDATE ON edfilms.AssignmentSubmission
    FOR EACH ROW EXECUTE PROCEDURE changes.UpdateChangeVersion();

