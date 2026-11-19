-- Story: RWB-E1-044
CREATE FUNCTION ${recoverySchema}.g() RETURNS int LANGUAGE sql AS $fn$ SELECT 1 /* $fn$;
CREATE TABLE public.x (id int);
-- */
