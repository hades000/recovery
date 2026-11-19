-- Story: RWB-E1-044
GRANT SELECT ON ${recoverySchema}.q TO rwb_migrator;
REVOKE ALL ON ${recoverySchema}.q FROM rwb_migrator;
SELECT 1; GRANT SELECT ON ${recoverySchema}.q TO rwb_migrator;
