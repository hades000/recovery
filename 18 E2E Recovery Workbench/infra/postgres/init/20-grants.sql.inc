-- Local only. Run by 10-load-ace-database.sh, not by the Postgres entrypoint (hence .sql.inc).
-- Applies the ADR-010 read boundary in the catalog, so a direct read of a public table by the
-- recovery service fails at the database and not only in code review.

-- The recovery schema and its tables belong to the migration account.
ALTER SCHEMA recovery OWNER TO rwb_migrator;
GRANT USAGE, CREATE ON SCHEMA recovery TO ace_view_owner;   -- CREATE is needed to own the views

-- ace_view_owner reads ACE. rwb_migrator holds USAGE on public and a membership of
-- ace_view_owner WITH INHERIT FALSE, SET TRUE (D-RUN-14): it has no table privilege of its own,
-- but it can SET ROLE ace_view_owner and then SELECT every ACE public table. The RWB-E1-069 view
-- migrations need that to create the views as their owner. Any migration script can therefore read
-- ACE data; this is a known risk, recorded under OPEN-051 (REVIEW-001 M10).
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO ace_view_owner;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ace_view_owner;

-- D-RUN-14: the two rights the recovery migration account needs for the ACE views, and no other.
GRANT USAGE ON SCHEMA public TO rwb_migrator;
GRANT ace_view_owner TO rwb_migrator WITH INHERIT FALSE, SET TRUE;

DO $$
DECLARE
  r record;
BEGIN
  -- Tables, sequences and non-ACE views: rwb_migrator
  FOR r IN SELECT c.relname, c.relkind FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
           WHERE n.nspname = 'recovery' AND c.relkind IN ('r', 'p', 'v')
             AND NOT (c.relkind = 'v' AND c.relname LIKE 'v\_ace\_%') LOOP
    EXECUTE format('ALTER TABLE recovery.%I OWNER TO rwb_migrator', r.relname);
  END LOOP;

  -- Functions: rwb_migrator, executable by the view owner and the service
  FOR r IN SELECT p.oid::regprocedure AS sig FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace
           WHERE n.nspname = 'recovery' LOOP
    EXECUTE format('ALTER FUNCTION %s OWNER TO rwb_migrator', r.sig);
  END LOOP;

  -- v_ace_* views: ace_view_owner, SELECT only for recovery_svc
  FOR r IN SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
           WHERE n.nspname = 'recovery' AND c.relkind = 'v' AND c.relname LIKE 'v\_ace\_%' LOOP
    EXECUTE format('ALTER VIEW recovery.%I OWNER TO ace_view_owner', r.relname);
    EXECUTE format('REVOKE ALL ON recovery.%I FROM recovery_svc', r.relname);
    EXECUTE format('GRANT SELECT ON recovery.%I TO recovery_svc', r.relname);
  END LOOP;
END $$;

GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA recovery TO ace_view_owner, recovery_svc;

-- recovery_svc: DML on Workbench tables (not on the ACE views)
GRANT USAGE ON SCHEMA recovery TO recovery_svc;
DO $$
DECLARE
  r record;
BEGIN
  FOR r IN SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
           WHERE n.nspname = 'recovery' AND c.relkind IN ('r', 'p') LOOP
    EXECUTE format('GRANT SELECT, INSERT, UPDATE, DELETE ON recovery.%I TO recovery_svc', r.relname);
  END LOOP;
END $$;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA recovery TO recovery_svc;

-- Objects Flyway creates later get the same grants.
ALTER DEFAULT PRIVILEGES FOR ROLE rwb_migrator IN SCHEMA recovery
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO recovery_svc;
ALTER DEFAULT PRIVILEGES FOR ROLE rwb_migrator IN SCHEMA recovery
  GRANT USAGE, SELECT ON SEQUENCES TO recovery_svc;
ALTER DEFAULT PRIVILEGES FOR ROLE rwb_migrator IN SCHEMA recovery
  GRANT EXECUTE ON FUNCTIONS TO recovery_svc, ace_view_owner;
