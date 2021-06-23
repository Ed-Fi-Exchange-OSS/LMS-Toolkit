CREATE TRIGGER UpdateChangeVersion BEFORE UPDATE ON lmsx.Assignment
    FOR EACH ROW EXECUTE PROCEDURE changes.UpdateChangeVersion();

CREATE TRIGGER UpdateChangeVersion BEFORE UPDATE ON lmsx.AssignmentSubmission
    FOR EACH ROW EXECUTE PROCEDURE changes.UpdateChangeVersion();

