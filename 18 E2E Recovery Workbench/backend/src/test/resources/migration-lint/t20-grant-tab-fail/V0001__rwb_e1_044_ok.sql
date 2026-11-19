-- Story: RWB-E1-044
DO $$
BEGIN
GRANT	SELECT ON ${recoverySchema}.q TO rwb_migrator;
REVOKE	ALL ON ${recoverySchema}.q FROM rwb_migrator;
END
$$;
CREATE FUNCTION ${recoverySchema}.f() RETURNS void LANGUAGE plpgsql AS $body$
BEGIN
	GRANT	SELECT ON ${recoverySchema}.q TO rwb_migrator;
	REVOKE	ALL ON ${recoverySchema}.q FROM rwb_migrator;
END
$body$;
