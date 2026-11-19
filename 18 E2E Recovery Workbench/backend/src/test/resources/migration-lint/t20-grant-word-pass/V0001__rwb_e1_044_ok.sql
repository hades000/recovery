-- Story: RWB-E1-044
CREATE TABLE ${recoverySchema}.q (
  id int,
  granted_at timestamptz,
  revoked_by text,
  grantee text
);
