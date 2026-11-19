-- Story: RWB-E1-044
CREATE TABLE ${recoverySchema}.c1 (
  id int PRIMARY KEY,
  amount numeric(18, 2) NOT NULL DEFAULT 0,
  kind ${recoverySchema}.kind_type,
  created_at pg_catalog.timestamptz,
  parent_id int REFERENCES ${recoverySchema}.c0 (id),
  CONSTRAINT c1_amount_ck CHECK (amount >= 0),
  UNIQUE (id, kind)
);
ALTER TABLE ${recoverySchema}.c1 ADD COLUMN note ${recoverySchema}.note_type;
ALTER TABLE ${recoverySchema}.c1 ADD CONSTRAINT c1_note_ck CHECK (note IS NOT NULL);
ALTER TABLE ${recoverySchema}.c1 ALTER COLUMN note TYPE text;
SELECT count(DISTINCT c.id) FROM ${recoverySchema}.c1 c;
