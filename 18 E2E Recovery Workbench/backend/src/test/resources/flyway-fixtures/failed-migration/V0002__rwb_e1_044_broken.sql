-- Story: RWB-E1-044
CREATE TABLE ${recoverySchema}.broken_a (id bigint);
CREATE TABLE ${recoverySchema}.broken_b (id bigint) REFERENCES ${recoverySchema}.missing_table(id);
