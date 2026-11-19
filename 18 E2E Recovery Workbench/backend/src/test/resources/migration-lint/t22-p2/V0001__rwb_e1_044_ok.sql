-- Story: RWB-E1-044
CREATE FUNCTION ${recoverySchema}.f() RETURNS text LANGUAGE sql AS $$ SELECT 'public.x' $$;
