-- Story: RWB-E1-044
CREATE TABLE ${recoverySchema}.c1 (id rwb_case.t1);
CREATE TABLE IF NOT EXISTS ${recoverySchema}.c2 (
  id int,
  "Note" "rwb_case".ty1 NOT NULL
);
ALTER TABLE ${recoverySchema}.c1 ADD COLUMN note rwb_case.ty1;
ALTER TABLE ${recoverySchema}.c1 ADD COLUMN IF NOT EXISTS note2 rwb_case.ty1;
ALTER TABLE ${recoverySchema}.c1 ADD note3 rwb_case.ty1;
ALTER TABLE ${recoverySchema}.c1 ALTER COLUMN note TYPE rwb_case.ty2;
ALTER TABLE ${recoverySchema}.c1 ALTER COLUMN note SET DATA TYPE rwb_case.ty2;
