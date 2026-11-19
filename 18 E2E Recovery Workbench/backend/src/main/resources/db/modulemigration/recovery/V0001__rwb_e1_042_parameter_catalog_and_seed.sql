-- Story: RWB-E1-042
-- Parameter catalog and seed for RWB-E1-042 (spec SPEC-001, -002, -006); columns from Physical Schema v6
-- (lines 1386-1434); D-RCV-28. Forward only. The schema qualifier is the Flyway placeholder only.
--
-- Statement groups, in order: the two tables as Physical Schema v6 defines them; the three columns this
-- story adds; the guarded constraints; the indexes; the comments; the 19 catalog rows; the 40 approved
-- value rows; the self-check block.

-- 1. Tables, exactly as Physical Schema v6 lines 1386-1434 (type, width, nullability, default, order).
CREATE TABLE IF NOT EXISTS ${recoverySchema}.parameter_catalog (
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
    CONSTRAINT uk_parameter_catalog UNIQUE (param_key)
);

CREATE TABLE IF NOT EXISTS ${recoverySchema}.parameter_value (
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
    CONSTRAINT uk_parameter_value UNIQUE (param_key, environment, product_group, version_no)
);

-- 2. The three columns this story adds (SPEC-002).
ALTER TABLE ${recoverySchema}.parameter_value ADD COLUMN IF NOT EXISTS load_id uuid;
ALTER TABLE ${recoverySchema}.parameter_value ADD COLUMN IF NOT EXISTS content_hash char(64);
ALTER TABLE ${recoverySchema}.parameter_value ADD COLUMN IF NOT EXISTS rollback_reason varchar(400);

-- 3. Constraints, each guarded by name so the file applies on an empty schema and on a schema built
--    from Physical Schema v6 (SPEC-001).
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint
                   WHERE conname = 'ck_parameter_catalog_scope'
                     AND conrelid = '${recoverySchema}.parameter_catalog'::regclass) THEN
        ALTER TABLE ${recoverySchema}.parameter_catalog
            ADD CONSTRAINT ck_parameter_catalog_scope CHECK (scope IN ('GLOBAL', 'PRODUCT'));
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint
                   WHERE conname = 'ck_parameter_catalog_kind'
                     AND conrelid = '${recoverySchema}.parameter_catalog'::regclass) THEN
        ALTER TABLE ${recoverySchema}.parameter_catalog
            ADD CONSTRAINT ck_parameter_catalog_kind CHECK (kind IN ('BUSINESS', 'ENVIRONMENT'));
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint
                   WHERE conname = 'ck_parameter_catalog_value_type'
                     AND conrelid = '${recoverySchema}.parameter_catalog'::regclass) THEN
        ALTER TABLE ${recoverySchema}.parameter_catalog
            ADD CONSTRAINT ck_parameter_catalog_value_type CHECK (value_type IN ('STRING', 'INTEGER', 'DECIMAL',
                'BOOLEAN', 'DATE', 'TIME', 'DURATION', 'CODE', 'CODE_LIST', 'JSON'));
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint
                   WHERE conname = 'ck_parameter_catalog_environments'
                     AND conrelid = '${recoverySchema}.parameter_catalog'::regclass) THEN
        ALTER TABLE ${recoverySchema}.parameter_catalog
            ADD CONSTRAINT ck_parameter_catalog_environments CHECK (environments IS NULL OR environments = ''
                OR environments ~ '^(DEV|SIT|UAT|PROD)(,(DEV|SIT|UAT|PROD))*$');
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint
                   WHERE conname = 'ck_parameter_catalog_secret_default'
                     AND conrelid = '${recoverySchema}.parameter_catalog'::regclass) THEN
        ALTER TABLE ${recoverySchema}.parameter_catalog
            ADD CONSTRAINT ck_parameter_catalog_secret_default CHECK (NOT secret OR default_value IS NULL);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint
                   WHERE conname = 'ck_parameter_value_environment'
                     AND conrelid = '${recoverySchema}.parameter_value'::regclass) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT ck_parameter_value_environment CHECK (environment IN ('DEV', 'SIT', 'UAT', 'PROD'));
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint
                   WHERE conname = 'ck_parameter_value_status'
                     AND conrelid = '${recoverySchema}.parameter_value'::regclass) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT ck_parameter_value_status CHECK (status IN ('VALIDATED', 'APPROVED', 'IN_FORCE',
                'SUPERSEDED', 'ROLLED_BACK', 'REFUSED'));
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint
                   WHERE conname = 'ck_parameter_value_dates'
                     AND conrelid = '${recoverySchema}.parameter_value'::regclass) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT ck_parameter_value_dates CHECK (valid_to IS NULL OR valid_to >= valid_from);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint
                   WHERE conname = 'ck_parameter_value_version'
                     AND conrelid = '${recoverySchema}.parameter_value'::regclass) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT ck_parameter_value_version CHECK (version_no >= 1);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint
                   WHERE conname = 'ck_parameter_value_maker_checker'
                     AND conrelid = '${recoverySchema}.parameter_value'::regclass) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT ck_parameter_value_maker_checker CHECK (approver_user_id IS NULL
                OR approver_user_id <> author_user_id);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint
                   WHERE conname = 'ck_parameter_value_approved_at'
                     AND conrelid = '${recoverySchema}.parameter_value'::regclass) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT ck_parameter_value_approved_at CHECK (status NOT IN ('APPROVED', 'IN_FORCE')
                OR approved_at IS NOT NULL);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint
                   WHERE conname = 'ck_parameter_value_load_hash'
                     AND conrelid = '${recoverySchema}.parameter_value'::regclass) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT ck_parameter_value_load_hash CHECK ((load_id IS NULL) = (content_hash IS NULL)
                AND (content_hash IS NULL OR content_hash ~ '^[0-9a-f]{64}$'));
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint
                   WHERE conname = 'ck_parameter_value_rollback_reason'
                     AND conrelid = '${recoverySchema}.parameter_value'::regclass) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT ck_parameter_value_rollback_reason CHECK (status <> 'ROLLED_BACK'
                OR (rollback_reason IS NOT NULL AND length(btrim(rollback_reason)) > 0));
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint
                   WHERE conname = 'fk_parameter_value_catalog'
                     AND conrelid = '${recoverySchema}.parameter_value'::regclass) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT fk_parameter_value_catalog FOREIGN KEY (param_key)
                REFERENCES ${recoverySchema}.parameter_catalog (param_key);
    END IF;
END $$;

-- 4. Indexes.
CREATE INDEX IF NOT EXISTS ix_parameter_value_in_force
    ON ${recoverySchema}.parameter_value (param_key, environment, valid_from) WHERE status = 'APPROVED';

CREATE INDEX IF NOT EXISTS ix_parameter_value_load
    ON ${recoverySchema}.parameter_value (load_id);

CREATE UNIQUE INDEX IF NOT EXISTS ux_parameter_value_version_all
    ON ${recoverySchema}.parameter_value (param_key, environment, COALESCE(product_group, '*'), version_no);

CREATE UNIQUE INDEX IF NOT EXISTS ux_parameter_value_approved_from
    ON ${recoverySchema}.parameter_value (param_key, environment, COALESCE(product_group, '*'), valid_from)
    WHERE status IN ('APPROVED', 'IN_FORCE');

-- 5. Comments.
COMMENT ON TABLE ${recoverySchema}.parameter_catalog IS
    'The definition of every parameter and environment setting, with its owner and default.';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.environments IS
    'Comma list of the environments the key must be set in: DEV, SIT, UAT, PROD.';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.used_by IS
    'The consumers of the key, separated by a semicolon.';
COMMENT ON TABLE ${recoverySchema}.parameter_value IS
    'An approved, dated value version of a parameter per environment and product group.';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.load_id IS
    'The reference load that wrote this row; NULL only for a seeded row.';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.content_hash IS
    'SHA-256 of the canonical load, lower-case hex; NULL exactly when load_id is NULL.';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.rollback_reason IS
    'Why an approved load was rolled back; required when status is ROLLED_BACK.';

-- 6. The 19 catalog rows of spec section 12.4 (ON CONFLICT keeps a re-run harmless).
INSERT INTO ${recoverySchema}.parameter_catalog (param_key, kind, value_type, unit, min_value, max_value,
    default_value, scope, required, owner_role, environments, used_by, secret, description,
    created_by, updated_by)
VALUES
    ('case.entry.dpd', 'BUSINESS', 'INTEGER', 'CALENDAR_DAYS', '1', '365', '90', 'GLOBAL', true, 'RW-COE',
        'DEV,SIT,UAT,PROD', 'recovery.casewf.casecreation', false,
        'Days past due at which an account enters recovery (DL16).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('refdata.cache.ttl-seconds', 'ENVIRONMENT', 'INTEGER', 'SECONDS', NULL, NULL, '300', 'GLOBAL', true,
        'RW-PLATADM', 'DEV,SIT,UAT,PROD', 'recovery.casewf.refdata', false,
        'Time to live of the reference data row cache, in seconds (DL11).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('config.cache.ttl-seconds', 'ENVIRONMENT', 'INTEGER', 'SECONDS', NULL, NULL, '60', 'GLOBAL', false,
        'RW-PLATADM', 'DEV,SIT,UAT,PROD', 'recovery.casewf.config', false,
        'Time to live of the configuration service cache, in seconds (DL11, assumed).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('caselist.export.maxrows', 'BUSINESS', 'INTEGER', 'COUNT', NULL, NULL, '10000', 'GLOBAL', false, 'RW-COE',
        'DEV,SIT,UAT,PROD', 'recovery.casewf.caselist', false,
        'Maximum rows returned by the case list export (DL11, assumed).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('ace.db.password', 'ENVIRONMENT', 'STRING', NULL, NULL, NULL, NULL, 'GLOBAL', false, 'RW-PLATADM',
        'DEV,SIT,UAT,PROD', 'ACE common module', true,
        'ACE database password; the value is held only in the ACE secret store (DL26).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('recon.caselist.tolerance.pct', 'BUSINESS', 'DECIMAL', 'PERCENT', NULL, NULL, '0.00', 'GLOBAL', false,
        'RW-COE', 'DEV,SIT,UAT,PROD', 'recovery.dataengine.caselist', false,
        'Tolerance for the case-list count reconciliation REC-01 (DL25, assumed).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('caselist.allocation.wait.until', 'BUSINESS', 'TIME', 'TIME_OF_DAY', NULL, NULL, '07:15', 'GLOBAL', false,
        'RW-COE', 'DEV,SIT,UAT,PROD', 'recovery.casewf.caselist', false,
        'Time by which allocation must be complete before the case list is built.',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('servicelevel.required-statuses', 'BUSINESS', 'CODE_LIST', NULL, NULL, NULL,
        'NEW,ASSIGNED,IN_PROGRESS,WAITING_CUSTOMER,WAITING_PARTNER,WAITING_APPROVAL', 'GLOBAL', true, 'RW-COE',
        'DEV,SIT,UAT,PROD', 'recovery.casewf.refdata.product', false,
        'Case statuses for which every product in force must have a SERVICE_LEVEL row (DL22, assumed).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('ENTRY_DPD', 'BUSINESS', 'INTEGER', 'DAYS', NULL, NULL, NULL, 'PRODUCT', true, 'RW-PRODHEAD',
        'DEV,SIT,UAT,PROD', 'recovery.casewf.casecreation; recovery.casewf.allocation', false,
        'Per-product entry threshold, in days past due; the values are PRODUCT_PARAMETER rows (RWB-E1-045).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('EXCLUSION_LIST', 'BUSINESS', 'CODE_LIST', NULL, NULL, NULL, NULL, 'PRODUCT', true, 'RW-PRODHEAD',
        'DEV,SIT,UAT,PROD', 'recovery.casewf.casecreation; recovery.casewf.allocation', false,
        'Per-product exclusion list code; the values are PRODUCT_PARAMETER rows (RWB-E1-045).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('NOTICE_PERIOD_DAYS', 'BUSINESS', 'INTEGER', 'DAYS', '1', '365', NULL, 'PRODUCT', true, 'RW-PRODHEAD',
        'DEV,SIT,UAT,PROD', 'recovery.casewf.timers', false,
        'Per-product notice period in days; the values are PRODUCT_PARAMETER rows (RWB-E1-045).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('CURE_PERIOD_DAYS', 'BUSINESS', 'INTEGER', 'DAYS', NULL, NULL, NULL, 'PRODUCT', true, 'RW-PRODHEAD',
        'DEV,SIT,UAT,PROD', 'recovery.casewf.timers', false,
        'Per-product cure period in days; the values are PRODUCT_PARAMETER rows (RWB-E1-045).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('EXPOSURE_BAND_SET', 'BUSINESS', 'CODE_LIST', NULL, NULL, NULL, NULL, 'PRODUCT', true, 'RW-PRODHEAD',
        'DEV,SIT,UAT,PROD', 'recovery.casewf.allocation', false,
        'Per-product exposure band set code; the values are PRODUCT_PARAMETER rows (RWB-E1-045).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('temporal.target', 'ENVIRONMENT', 'STRING', NULL, NULL, NULL, NULL, 'GLOBAL', true, 'RW-PLATADM',
        'DEV,SIT,UAT,PROD', 'recovery.casewf.workflow (RWB-E1-070, RWB-E1-071)', false,
        'Temporal server endpoint the recovery workflow workers connect to.',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('temporal.namespace', 'ENVIRONMENT', 'STRING', NULL, NULL, NULL, 'rwb-recovery', 'GLOBAL', false,
        'RW-PLATADM', 'DEV,SIT,UAT,PROD', 'recovery.casewf.workflow (RWB-E1-070, RWB-E1-071)', false,
        'Temporal namespace the recovery workflows run in (default rwb-recovery).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('temporal.taskqueue.platform', 'ENVIRONMENT', 'STRING', NULL, NULL, NULL, 'rwb-platform', 'GLOBAL', false,
        'RW-PLATADM', 'DEV,SIT,UAT,PROD', 'recovery.casewf.workflow (RWB-E1-070, RWB-E1-071)', false,
        'Temporal task queue the platform workers poll (default rwb-platform).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('temporal.retention.days', 'ENVIRONMENT', 'INTEGER', 'DAYS', NULL, NULL, '30', 'GLOBAL', false,
        'RW-PLATADM', 'DEV,SIT,UAT,PROD',
        'recovery.casewf.workflow (RWB-E1-070, RWB-E1-071); RWB-E2-039', false,
        'Days a closed Temporal workflow history is retained (default 30).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('drools.kiebase.cache.max', 'ENVIRONMENT', 'INTEGER', 'COUNT', NULL, NULL, '20', 'GLOBAL', false,
        'RW-PLATADM', 'DEV,SIT,UAT,PROD', 'recovery.casewf.rules (RWB-E1-072)', false,
        'Maximum number of Drools KIE bases held in the rules cache (default 20).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042'),
    ('rules.testcases.min', 'BUSINESS', 'INTEGER', 'COUNT', NULL, NULL, '50', 'GLOBAL', false, 'RW-COE',
        'DEV,SIT,UAT,PROD', 'RWB-E1-073', false,
        'Minimum number of decision-table test cases a rule package must ship (default 50).',
        '00000000-0000-0000-0000-0000000e1042', '00000000-0000-0000-0000-0000000e1042')
ON CONFLICT (param_key) DO NOTHING;

-- 7. The 40 approved value rows: one per GLOBAL, non-secret, TABLE-sourced key with a default, per listed
--    environment (SPEC-006). A re-run inserts nothing.
INSERT INTO ${recoverySchema}.parameter_value (param_key, environment, param_value, product_group, version_no,
    valid_from, status, author_user_id, approver_user_id, approved_at, created_by)
SELECT v.param_key, e.environment, v.param_value, NULL, 1, DATE '2026-11-02', 'APPROVED',
       '00000000-0000-0000-0000-0000000e1042', NULL, now(), '00000000-0000-0000-0000-0000000e1042'
FROM (VALUES
    ('case.entry.dpd', '90'),
    ('refdata.cache.ttl-seconds', '300'),
    ('config.cache.ttl-seconds', '60'),
    ('caselist.export.maxrows', '10000'),
    ('recon.caselist.tolerance.pct', '0.00'),
    ('caselist.allocation.wait.until', '07:15'),
    ('servicelevel.required-statuses',
        'NEW,ASSIGNED,IN_PROGRESS,WAITING_CUSTOMER,WAITING_PARTNER,WAITING_APPROVAL'),
    ('temporal.taskqueue.platform', 'rwb-platform'),
    ('temporal.retention.days', '30'),
    ('rules.testcases.min', '50')
) AS v(param_key, param_value)
CROSS JOIN (VALUES ('DEV'), ('SIT'), ('UAT'), ('PROD')) AS e(environment)
WHERE NOT EXISTS (
    SELECT 1 FROM ${recoverySchema}.parameter_value p
    WHERE p.param_key = v.param_key
      AND p.environment = e.environment
      AND p.product_group IS NULL
);

-- 8. Self-check: every required GLOBAL non-secret row with a default has an approved value for each
--    environment it lists. Rows without a default are exempt (for example temporal.target, an ENV key).
DO $$
DECLARE
    missing integer;
BEGIN
    SELECT count(*) INTO missing
    FROM ${recoverySchema}.parameter_catalog c
    WHERE c.required
      AND c.scope = 'GLOBAL'
      AND NOT c.secret
      AND c.default_value IS NOT NULL
      AND c.environments IS NOT NULL
      AND EXISTS (
          SELECT 1 FROM unnest(string_to_array(c.environments, ',')) AS e(name)
          WHERE NOT EXISTS (
              SELECT 1 FROM ${recoverySchema}.parameter_value v
              WHERE v.param_key = c.param_key
                AND v.environment = e.name
                AND v.status = 'APPROVED'
          )
      );
    IF missing > 0 THEN
        RAISE EXCEPTION 'RWB-E1-042 seed self-check failed: % required parameters have no approved value', missing;
    END IF;
END $$;
