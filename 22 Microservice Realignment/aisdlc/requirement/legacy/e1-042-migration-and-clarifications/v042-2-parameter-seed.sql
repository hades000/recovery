-- Story: RWB-E1-042
-- Migration: parameter catalog seed (generated)
-- Schema: ${recoverySchema}
--
-- REVIEW COPY. D-RCV-28 requires one migration per story named
-- V<seq>__<story>_<name>.sql. Commit the consolidated
-- V0042__rwb_e1_042_parameter_catalog_and_seed.sql unless a migration-lint
-- exception is approved for the split. See section 2 of the clarification pack.
--
-- Generated from config/parameter-catalog.csv by tools/Generate-ParameterSeed.ps1.
-- Do not edit by hand: change the catalog CSV and regenerate this file.
--
-- Seed provenance. These rows are deployment defaults, not a maker-checker approval
-- by a person. The author is the system seed account (the nil UUID); approver_user_id
-- stays NULL and approved_at records the release date. The first human load through
-- POST /admin/reference-loads with table PARAMETER starts at version 2.
--
-- Seed set. This bootstrap file carries the rows RWB-E1-042 itself defines, the two
-- RWB-E1-002 parameters that precede it, the service-level status list RWB-E1-045
-- needs, and the five PRODUCT-scope catalog entries RWB-E1-045 defines. It is not a
-- claim to be the full Epic 1 catalog; that is config/parameter-catalog.csv and is
-- tracked as OI-E1-042-003. Product-scope rows carry no default by design: their
-- values are PRODUCT_PARAMETER rows, not parameter_value rows.

INSERT INTO ${recoverySchema}.parameter_catalog
    (param_key, kind, value_type, unit, min_value, max_value, default_value,
     scope, required, owner_role, environments, used_by, secret, description, created_by)
VALUES
    ('case.entry.dpd',
     'BUSINESS', 'INTEGER', 'CALENDAR_DAYS', '1', '365', '90',
     'GLOBAL', true, 'RW-COE', 'DEV,SIT,UAT,PROD',
     'recovery.casewf.casecreation', false,
     'Days past due at which an account enters recovery (DL16).',
     '00000000-0000-0000-0000-000000000000'::uuid),
    ('refdata.cache.ttl-seconds',
     'ENVIRONMENT', 'INTEGER', 'SECONDS', NULL, NULL, '300',
     'GLOBAL', true, 'RW-PLATADM', 'DEV,SIT,UAT,PROD',
     'recovery.casewf.refdata', false,
     'Time to live of the reference data row cache, in seconds (DL11).',
     '00000000-0000-0000-0000-000000000000'::uuid),
    ('config.cache.ttl-seconds',
     'ENVIRONMENT', 'INTEGER', 'SECONDS', NULL, NULL, '60',
     'GLOBAL', false, 'RW-PLATADM', 'DEV,SIT,UAT,PROD',
     'recovery.casewf.config', false,
     'Time to live of the configuration service cache, in seconds (DL11, assumed).',
     '00000000-0000-0000-0000-000000000000'::uuid),
    ('caselist.export.maxrows',
     'BUSINESS', 'INTEGER', 'COUNT', NULL, NULL, '10000',
     'GLOBAL', false, 'RW-COE', 'DEV,SIT,UAT,PROD',
     'recovery.casewf.caselist', false,
     'Maximum rows returned by the case list export (DL11, assumed).',
     '00000000-0000-0000-0000-000000000000'::uuid),
    ('ace.db.password',
     'ENVIRONMENT', 'STRING', NULL, NULL, NULL, NULL,
     'GLOBAL', false, 'RW-PLATADM', 'DEV,SIT,UAT,PROD',
     'ACE common module', true,
     'ACE database password; the value is held only in the ACE secret store (DL26).',
     '00000000-0000-0000-0000-000000000000'::uuid),
    ('recon.caselist.tolerance.pct',
     'BUSINESS', 'DECIMAL', 'PERCENT', NULL, NULL, '0.00',
     'GLOBAL', false, 'RW-COE', 'DEV,SIT,UAT,PROD',
     'recovery.dataengine.caselist', false,
     'Tolerance for the case-list count reconciliation REC-01 (DL25, assumed).',
     '00000000-0000-0000-0000-000000000000'::uuid),
    ('caselist.allocation.wait.until',
     'BUSINESS', 'TIME', 'TIME_OF_DAY', NULL, NULL, '07:15',
     'GLOBAL', false, 'RW-COE', 'DEV,SIT,UAT,PROD',
     'recovery.casewf.caselist', false,
     'Time by which allocation must be complete before the case list is built.',
     '00000000-0000-0000-0000-000000000000'::uuid),
    ('servicelevel.required-statuses',
     'BUSINESS', 'CODE_LIST', NULL, NULL, NULL, 'NEW,ASSIGNED,IN_PROGRESS,WAITING_CUSTOMER,WAITING_PARTNER,WAITING_APPROVAL',
     'GLOBAL', true, 'RW-COE', 'DEV,SIT,UAT,PROD',
     'recovery.casewf.refdata.product', false,
     'Case statuses for which every product in force must have a SERVICE_LEVEL row (DL22, assumed).',
     '00000000-0000-0000-0000-000000000000'::uuid),
    ('ENTRY_DPD',
     'BUSINESS', 'INTEGER', 'DAYS', NULL, NULL, NULL,
     'PRODUCT', true, 'RW-PRODHEAD', 'DEV,SIT,UAT,PROD',
     'recovery.casewf.casecreation, recovery.casewf.allocation', false,
     'Per-product entry threshold, in days past due; the values are PRODUCT_PARAMETER rows (RWB-E1-045).',
     '00000000-0000-0000-0000-000000000000'::uuid),
    ('EXCLUSION_LIST',
     'BUSINESS', 'CODE_LIST', NULL, NULL, NULL, NULL,
     'PRODUCT', true, 'RW-PRODHEAD', 'DEV,SIT,UAT,PROD',
     'recovery.casewf.casecreation, recovery.casewf.allocation', false,
     'Per-product exclusion list code; the values are PRODUCT_PARAMETER rows (RWB-E1-045).',
     '00000000-0000-0000-0000-000000000000'::uuid),
    ('NOTICE_PERIOD_DAYS',
     'BUSINESS', 'INTEGER', 'DAYS', '1', '365', NULL,
     'PRODUCT', true, 'RW-PRODHEAD', 'DEV,SIT,UAT,PROD',
     'recovery.casewf.timers', false,
     'Per-product notice period in days; the values are PRODUCT_PARAMETER rows (RWB-E1-045).',
     '00000000-0000-0000-0000-000000000000'::uuid),
    ('CURE_PERIOD_DAYS',
     'BUSINESS', 'INTEGER', 'DAYS', NULL, NULL, NULL,
     'PRODUCT', true, 'RW-PRODHEAD', 'DEV,SIT,UAT,PROD',
     'recovery.casewf.timers', false,
     'Per-product cure period in days; the values are PRODUCT_PARAMETER rows (RWB-E1-045).',
     '00000000-0000-0000-0000-000000000000'::uuid),
    ('EXPOSURE_BAND_SET',
     'BUSINESS', 'CODE_LIST', NULL, NULL, NULL, NULL,
     'PRODUCT', true, 'RW-PRODHEAD', 'DEV,SIT,UAT,PROD',
     'recovery.casewf.allocation', false,
     'Per-product exposure band set code; the values are PRODUCT_PARAMETER rows (RWB-E1-045).',
     '00000000-0000-0000-0000-000000000000'::uuid)
ON CONFLICT (param_key) DO NOTHING;

-- Default values, one row per environment the catalog line lists. A repeated run
-- inserts nothing: the NOT EXISTS test treats the NULL product_group as one value.
INSERT INTO ${recoverySchema}.parameter_value
    (param_key, environment, param_value, product_group, version_no, valid_from, valid_to,
     status, author_user_id, approver_user_id, approved_at, created_by)
SELECT
    v.param_key,
    v.environment,
    v.param_value,
    NULL,
    1,
    DATE '2026-11-30',
    NULL,
    'APPROVED',
    '00000000-0000-0000-0000-000000000000'::uuid,
    NULL,
    TIMESTAMPTZ '2026-11-30 00:00:00+07',
    '00000000-0000-0000-0000-000000000000'::uuid
FROM (VALUES
    ('case.entry.dpd', 'DEV', '90'),
    ('case.entry.dpd', 'SIT', '90'),
    ('case.entry.dpd', 'UAT', '90'),
    ('case.entry.dpd', 'PROD', '90'),
    ('refdata.cache.ttl-seconds', 'DEV', '300'),
    ('refdata.cache.ttl-seconds', 'SIT', '300'),
    ('refdata.cache.ttl-seconds', 'UAT', '300'),
    ('refdata.cache.ttl-seconds', 'PROD', '300'),
    ('config.cache.ttl-seconds', 'DEV', '60'),
    ('config.cache.ttl-seconds', 'SIT', '60'),
    ('config.cache.ttl-seconds', 'UAT', '60'),
    ('config.cache.ttl-seconds', 'PROD', '60'),
    ('caselist.export.maxrows', 'DEV', '10000'),
    ('caselist.export.maxrows', 'SIT', '10000'),
    ('caselist.export.maxrows', 'UAT', '10000'),
    ('caselist.export.maxrows', 'PROD', '10000'),
    ('recon.caselist.tolerance.pct', 'DEV', '0.00'),
    ('recon.caselist.tolerance.pct', 'SIT', '0.00'),
    ('recon.caselist.tolerance.pct', 'UAT', '0.00'),
    ('recon.caselist.tolerance.pct', 'PROD', '0.00'),
    ('caselist.allocation.wait.until', 'DEV', '07:15'),
    ('caselist.allocation.wait.until', 'SIT', '07:15'),
    ('caselist.allocation.wait.until', 'UAT', '07:15'),
    ('caselist.allocation.wait.until', 'PROD', '07:15'),
    ('servicelevel.required-statuses', 'DEV', 'NEW,ASSIGNED,IN_PROGRESS,WAITING_CUSTOMER,WAITING_PARTNER,WAITING_APPROVAL'),
    ('servicelevel.required-statuses', 'SIT', 'NEW,ASSIGNED,IN_PROGRESS,WAITING_CUSTOMER,WAITING_PARTNER,WAITING_APPROVAL'),
    ('servicelevel.required-statuses', 'UAT', 'NEW,ASSIGNED,IN_PROGRESS,WAITING_CUSTOMER,WAITING_PARTNER,WAITING_APPROVAL'),
    ('servicelevel.required-statuses', 'PROD', 'NEW,ASSIGNED,IN_PROGRESS,WAITING_CUSTOMER,WAITING_PARTNER,WAITING_APPROVAL')
) AS v (param_key, environment, param_value)
WHERE NOT EXISTS (
    SELECT 1
    FROM ${recoverySchema}.parameter_value pv
    WHERE pv.param_key = v.param_key
      AND pv.environment = v.environment
      AND pv.product_group IS NULL
);

-- Deployment guard. Every required GLOBAL parameter that is not a secret must have
-- an approved value for every environment it lists. This is not a substitute for
-- ParameterStartupCheck: it catches a missing seed row before the service starts.
DO $$
DECLARE
    missing text;
BEGIN
    SELECT string_agg(c.param_key || ':' || e.environment, ', ' ORDER BY c.param_key, e.environment)
    INTO missing
    FROM ${recoverySchema}.parameter_catalog c
    CROSS JOIN LATERAL unnest(string_to_array(c.environments, ',')) AS e(environment)
    WHERE c.required
      AND c.scope = 'GLOBAL'
      AND NOT c.secret
      AND c.environments IS NOT NULL
      AND c.environments <> ''
      AND NOT EXISTS (
          SELECT 1
          FROM ${recoverySchema}.parameter_value pv
          WHERE pv.param_key = c.param_key
            AND pv.environment = e.environment
            AND pv.product_group IS NULL
            AND pv.status = 'APPROVED'
      );
    IF missing IS NOT NULL THEN
        RAISE EXCEPTION 'RWB-E1-042 seed incomplete: required parameter has no approved value for %', missing;
    END IF;
END;
$$;
