-- Story: RWB-E1-044
CREATE FUNCTION ${recoverySchema}.h() RETURNS int LANGUAGE sql AS $$
-- reads the source
SELECT a.id FROM public.t1 a
$$;
