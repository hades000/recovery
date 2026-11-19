-- Story: RWB-E1-044
CREATE INDEX idx$on ON rwb_case.t1 (a);
CREATE TRIGGER trg$on AFTER INSERT ON rwb_case.t1 FOR EACH ROW EXECUTE FUNCTION f1();
CREATE POLICY p$on ON rwb_case.t1 USING (true);
