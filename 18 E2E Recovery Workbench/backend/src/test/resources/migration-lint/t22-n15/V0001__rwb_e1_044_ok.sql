-- Story: RWB-E1-044
INSERT INTO ${recoverySchema}.t1 (v) VALUES ('--'); CREATE TABLE ${recoverySchema}.c (t_id int REFERENCES public.t1(id));
