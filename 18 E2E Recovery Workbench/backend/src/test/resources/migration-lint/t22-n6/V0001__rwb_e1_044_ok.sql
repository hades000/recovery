-- Story: RWB-E1-044
CREATE FUNCTION ${recoverySchema}.f() RETURNS int LANGUAGE sql AS $$ SELECT 1 -- $$; CREATE TABLE public.x (id int);
