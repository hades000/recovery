-- Story: RWB-E1-044
CREATE TABLE ${recoverySchema}.c1 (t_id bigint REFERENCES public.account(id));
