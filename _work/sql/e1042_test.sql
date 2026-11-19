-- Story: RWB-E1-042
-- Migration: parameter catalog, parameter value table and catalog seed
-- Schema: recovery
--
-- Consolidated per D-RCV-28: one migration file for RWB-E1-042. It contains the
-- DDL from V042_1__parameter_catalog.sql and the generated seed from
-- V042_2__parameter_seed.sql. The split files are review copies only; commit this
-- file unless a migration-lint exception is approved for the split.
--
-- Definition source: Recovery Workbench Physical Schema v4.sql, parameter_catalog and
-- parameter_value. Parameter keys are the business names; no key is a table name.
--
-- Baseline note. RWB-E1-001 V0001__rwb_e1_001_recovery_schema.sql is written from the
-- Physical Schema and already creates both tables. This file is therefore guarded: it
-- creates what is absent and then adds the E1-042 constraints, foreign key, uniqueness
-- rules and indexes only when they are absent. On a schema built without the baseline it
-- creates the complete E1-042 definition. The drift check remains the control that an
-- environment matches the migrations.
CREATE TABLE IF NOT EXISTS recovery.parameter_catalog (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    param_key varchar(100) NOT NULL,
    kind varchar(15) NOT NULL,
    value_type varchar(15) NOT NULL,
    unit varchar(20),
    min_value varchar(40),
    max_value varchar(40),
    default_value varchar(400),
    scope varchar(10) NOT NULL DEFAULT 'GLOBAL',
    required boolean NOT NULL DEFAULT false,
    owner_role varchar(20) NOT NULL,
    environments varchar(40),
    used_by varchar(400),
    secret boolean NOT NULL DEFAULT false,
    description varchar(400) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_parameter_catalog UNIQUE (param_key),
    CONSTRAINT ck_parameter_catalog_scope CHECK (scope IN ('GLOBAL', 'PRODUCT')),
    CONSTRAINT ck_parameter_catalog_kind CHECK (kind IN ('BUSINESS', 'ENVIRONMENT')),
    CONSTRAINT ck_parameter_catalog_value_type CHECK (
        value_type IN ('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'DATE', 'TIME',
                       'DURATION', 'CODE', 'CODE_LIST', 'JSON')
    ),
    CONSTRAINT ck_parameter_catalog_environments CHECK (
        environments IS NULL
        OR environments = ''
        OR environments ~ '^(DEV|SIT|UAT|PROD)(,(DEV|SIT|UAT|PROD))*$'
    ),
    CONSTRAINT ck_parameter_catalog_secret_default CHECK (
        NOT (secret AND default_value IS NOT NULL)
    )
);

CREATE TABLE IF NOT EXISTS recovery.parameter_value (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    param_key varchar(100) NOT NULL,
    environment varchar(4) NOT NULL,
    param_value varchar(400) NOT NULL,
    product_group varchar(15),
    version_no integer NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    status varchar(15) NOT NULL DEFAULT 'VALIDATED',
    author_user_id uuid NOT NULL,
    approver_user_id uuid,
    approved_at timestamptz,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_parameter_value UNIQUE (param_key, environment, product_group, version_no),
    CONSTRAINT ck_parameter_value_environment CHECK (environment IN ('DEV', 'SIT', 'UAT', 'PROD')),
    CONSTRAINT ck_parameter_value_status CHECK (
        status IN ('VALIDATED', 'APPROVED', 'IN_FORCE', 'SUPERSEDED', 'ROLLED_BACK', 'REFUSED')
    ),
    CONSTRAINT ck_parameter_value_dates CHECK (valid_to IS NULL OR valid_to >= valid_from),
    CONSTRAINT ck_parameter_value_version CHECK (version_no >= 1),
    CONSTRAINT ck_parameter_value_maker_checker CHECK (
        approver_user_id IS NULL OR approver_user_id <> author_user_id
    ),
    CONSTRAINT ck_parameter_value_approved_at CHECK (
        status NOT IN ('APPROVED', 'IN_FORCE') OR approved_at IS NOT NULL
    )
);

-- ---------------------------------------------------------------------------
-- Add the E1-042 objects when the baseline created the tables without them.
-- Each object is added only when it is absent, so the file is safe on either
-- schema. The constraint names match the Physical Schema where one exists.
-- ---------------------------------------------------------------------------

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'uk_parameter_catalog'
          AND conrelid = to_regclass('recovery.parameter_catalog')
    ) THEN
        ALTER TABLE recovery.parameter_catalog
            ADD CONSTRAINT uk_parameter_catalog UNIQUE (param_key);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_catalog_scope'
          AND conrelid = to_regclass('recovery.parameter_catalog')
    ) THEN
        ALTER TABLE recovery.parameter_catalog
            ADD CONSTRAINT ck_parameter_catalog_scope
            CHECK (scope IN ('GLOBAL', 'PRODUCT'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_catalog_kind'
          AND conrelid = to_regclass('recovery.parameter_catalog')
    ) THEN
        ALTER TABLE recovery.parameter_catalog
            ADD CONSTRAINT ck_parameter_catalog_kind
            CHECK (kind IN ('BUSINESS', 'ENVIRONMENT'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_catalog_value_type'
          AND conrelid = to_regclass('recovery.parameter_catalog')
    ) THEN
        ALTER TABLE recovery.parameter_catalog
            ADD CONSTRAINT ck_parameter_catalog_value_type
            CHECK (value_type IN ('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'DATE', 'TIME',
                                  'DURATION', 'CODE', 'CODE_LIST', 'JSON'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_catalog_environments'
          AND conrelid = to_regclass('recovery.parameter_catalog')
    ) THEN
        ALTER TABLE recovery.parameter_catalog
            ADD CONSTRAINT ck_parameter_catalog_environments
            CHECK (
                environments IS NULL
                OR environments = ''
                OR environments ~ '^(DEV|SIT|UAT|PROD)(,(DEV|SIT|UAT|PROD))*$'
            );
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_catalog_secret_default'
          AND conrelid = to_regclass('recovery.parameter_catalog')
    ) THEN
        ALTER TABLE recovery.parameter_catalog
            ADD CONSTRAINT ck_parameter_catalog_secret_default
            CHECK (NOT (secret AND default_value IS NOT NULL));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'uk_parameter_value'
          AND conrelid = to_regclass('recovery.parameter_value')
    ) THEN
        ALTER TABLE recovery.parameter_value
            ADD CONSTRAINT uk_parameter_value
            UNIQUE (param_key, environment, product_group, version_no);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_value_environment'
          AND conrelid = to_regclass('recovery.parameter_value')
    ) THEN
        ALTER TABLE recovery.parameter_value
            ADD CONSTRAINT ck_parameter_value_environment
            CHECK (environment IN ('DEV', 'SIT', 'UAT', 'PROD'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_value_status'
          AND conrelid = to_regclass('recovery.parameter_value')
    ) THEN
        ALTER TABLE recovery.parameter_value
            ADD CONSTRAINT ck_parameter_value_status
            CHECK (status IN ('VALIDATED', 'APPROVED', 'IN_FORCE', 'SUPERSEDED', 'ROLLED_BACK', 'REFUSED'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_value_dates'
          AND conrelid = to_regclass('recovery.parameter_value')
    ) THEN
        ALTER TABLE recovery.parameter_value
            ADD CONSTRAINT ck_parameter_value_dates
            CHECK (valid_to IS NULL OR valid_to >= valid_from);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_value_version'
          AND conrelid = to_regclass('recovery.parameter_value')
    ) THEN
        ALTER TABLE recovery.parameter_value
            ADD CONSTRAINT ck_parameter_value_version
            CHECK (version_no >= 1);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_value_maker_checker'
          AND conrelid = to_regclass('recovery.parameter_value')
    ) THEN
        ALTER TABLE recovery.parameter_value
            ADD CONSTRAINT ck_parameter_value_maker_checker
            CHECK (approver_user_id IS NULL OR approver_user_id <> author_user_id);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_value_approved_at'
          AND conrelid = to_regclass('recovery.parameter_value')
    ) THEN
        ALTER TABLE recovery.parameter_value
            ADD CONSTRAINT ck_parameter_value_approved_at
            CHECK (status NOT IN ('APPROVED', 'IN_FORCE') OR approved_at IS NOT NULL);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_parameter_value_catalog'
          AND conrelid = to_regclass('recovery.parameter_value')
    ) THEN
        ALTER TABLE recovery.parameter_value
            ADD CONSTRAINT fk_parameter_value_catalog
            FOREIGN KEY (param_key)
            REFERENCES recovery.parameter_catalog (param_key);
    END IF;
END;
$$;

-- Lookup index required by the story: the approved value in force for a key and
-- environment on a business date.
CREATE INDEX IF NOT EXISTS ix_parameter_value_in_force
    ON recovery.parameter_value (param_key, environment, valid_from)
    WHERE status = 'APPROVED';

-- Product-scoped lookup. The story's service also accepts a product group; the index
-- keeps that read on one index without changing the story's required index.
CREATE INDEX IF NOT EXISTS ix_parameter_value_lookup
    ON recovery.parameter_value (param_key, environment, product_group, valid_from DESC)
    WHERE status IN ('APPROVED', 'IN_FORCE');

-- The Physical Schema unique key includes nullable product_group. PostgreSQL treats
-- NULLs as distinct, so the constraint alone does not stop two version 1 rows for the
-- same global key and environment. This expression index closes that hole. The sentinel
-- '*' is not a valid LOV-PRODUCT value.
CREATE UNIQUE INDEX IF NOT EXISTS ux_parameter_value_version_all
    ON recovery.parameter_value
       (param_key, environment, COALESCE(product_group, '*'), version_no);

-- One approved value per key, environment, product group and valid-from date. This is
-- the database guard behind the load rule that a second approved version cannot share a
-- valid-from date; the service returns MSG-P3-027 before the insert.
CREATE UNIQUE INDEX IF NOT EXISTS ux_parameter_value_approved_from
    ON recovery.parameter_value
       (param_key, environment, COALESCE(product_group, '*'), valid_from)
    WHERE status IN ('APPROVED', 'IN_FORCE');

COMMENT ON TABLE recovery.parameter_catalog
    IS 'The definition of every parameter and environment setting, with its owner and default.';
COMMENT ON COLUMN recovery.parameter_catalog.id
    IS 'Record identifier of the parameter definition';
COMMENT ON COLUMN recovery.parameter_catalog.param_key
    IS 'Parameter key, for example case.entry.dpd';
COMMENT ON COLUMN recovery.parameter_catalog.kind
    IS 'Kind of parameter, for example ENVIRONMENT for an environment setting';
COMMENT ON COLUMN recovery.parameter_catalog.value_type
    IS 'Type of the value: STRING, INTEGER, DECIMAL, BOOLEAN, DATE, TIME, DURATION, CODE, CODE_LIST or JSON';
COMMENT ON COLUMN recovery.parameter_catalog.unit
    IS 'Unit, for example CALENDAR_DAYS, WORKING_DAYS, BAHT, PERCENT, COUNT, CODE_LIST';
COMMENT ON COLUMN recovery.parameter_catalog.min_value
    IS 'Lowest allowed value';
COMMENT ON COLUMN recovery.parameter_catalog.max_value
    IS 'Highest allowed value';
COMMENT ON COLUMN recovery.parameter_catalog.default_value
    IS 'Default value; never set for a secret';
COMMENT ON COLUMN recovery.parameter_catalog.scope
    IS 'Product, when the parameter is keyed by product group, or global';
COMMENT ON COLUMN recovery.parameter_catalog.required
    IS 'True when every product in force must have a row';
COMMENT ON COLUMN recovery.parameter_catalog.owner_role
    IS 'Role that owns the parameter';
COMMENT ON COLUMN recovery.parameter_catalog.environments
    IS 'Environments the parameter is set in, as a comma-separated list of DEV, SIT, UAT, PROD';
COMMENT ON COLUMN recovery.parameter_catalog.used_by
    IS 'Modules and stories that read the parameter';
COMMENT ON COLUMN recovery.parameter_catalog.secret
    IS 'True for a secret; its value is never returned';
COMMENT ON COLUMN recovery.parameter_catalog.description
    IS 'What the parameter controls';

COMMENT ON TABLE recovery.parameter_value
    IS 'An approved, dated value version of a parameter per environment and product group.';
COMMENT ON COLUMN recovery.parameter_value.id
    IS 'Record identifier of the parameter value';
COMMENT ON COLUMN recovery.parameter_value.param_key
    IS 'Parameter, from parameter_catalog';
COMMENT ON COLUMN recovery.parameter_value.environment
    IS 'DEV, SIT, UAT or PROD';
COMMENT ON COLUMN recovery.parameter_value.param_value
    IS 'Value as text';
COMMENT ON COLUMN recovery.parameter_value.product_group
    IS 'Product group for a product-scoped parameter; null for a global parameter';
COMMENT ON COLUMN recovery.parameter_value.version_no
    IS 'Version number, starting at 1';
COMMENT ON COLUMN recovery.parameter_value.valid_from
    IS 'Date the value comes into force';
COMMENT ON COLUMN recovery.parameter_value.valid_to
    IS 'Last date the value is in force';
COMMENT ON COLUMN recovery.parameter_value.status
    IS 'Validated, approved, in force, superseded, rolled back or refused';
COMMENT ON COLUMN recovery.parameter_value.author_user_id
    IS 'Who loaded the value';
COMMENT ON COLUMN recovery.parameter_value.approver_user_id
    IS 'Who approved the value; never the author';
COMMENT ON COLUMN recovery.parameter_value.approved_at
    IS 'When the value was approved';

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

INSERT INTO recovery.parameter_catalog
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
INSERT INTO recovery.parameter_value
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
    FROM recovery.parameter_value pv
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
    FROM recovery.parameter_catalog c
    CROSS JOIN LATERAL unnest(string_to_array(c.environments, ',')) AS e(environment)
    WHERE c.required
      AND c.scope = 'GLOBAL'
      AND NOT c.secret
      AND c.environments IS NOT NULL
      AND c.environments <> ''
      AND NOT EXISTS (
          SELECT 1
          FROM recovery.parameter_value pv
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
