-- Story: RWB-E1-044
SET search_path TO x;
SET LOCAL search_path TO x;
SET SESSION search_path TO x;
SELECT set_config('search_path', 'x', false);
ALTER ROLE rwb_migrator SET search_path TO x;
ALTER DATABASE ace SET search_path TO x;
ALTER FUNCTION ${recoverySchema}.f1() SET search_path TO x;
RESET search_path;
