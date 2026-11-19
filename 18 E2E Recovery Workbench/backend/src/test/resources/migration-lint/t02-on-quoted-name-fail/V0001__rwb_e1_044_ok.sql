-- Story: RWB-E1-044
CREATE TRIGGER "audit on insert" AFTER INSERT ON rwb_case.t1 FOR EACH ROW EXECUTE FUNCTION f1();
CREATE INDEX "on" ON rwb_case.t2 (a);
