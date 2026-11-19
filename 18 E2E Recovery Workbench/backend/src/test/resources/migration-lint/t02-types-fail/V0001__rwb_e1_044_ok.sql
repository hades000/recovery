-- Story: RWB-E1-044
SELECT x::public.t1;
SELECT CAST(x AS public.t1);
CREATE TABLE ${recoverySchema}.c1 (id public.t1);
