-- Story: RWB-E1-044
CREATE FUNCTION ${recoverySchema}.f() RETURNS int LANGUAGE sql AS $$
SELECT a.id FROM public.t1 a
$$;
