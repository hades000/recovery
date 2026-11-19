-- Story: RWB-E1-044
CREATE FUNCTION ${recoverySchema}.f(p text) RETURNS boolean LANGUAGE sql AS $$ SELECT p ~ '^\d{8}$' $$;
