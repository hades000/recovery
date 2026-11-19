-- Story: RWB-E1-044
CREATE TABLE ${recoverySchema}.c1 (t_id bigint REFERENCES ${recoverySchema}.t1(id));
CREATE TABLE ${recoverySchema}.c2 (t_id bigint REFERENCES t2(id));
