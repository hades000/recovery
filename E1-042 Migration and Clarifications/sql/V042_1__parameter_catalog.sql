-- Story: RWB-E1-042
-- Migration: parameter catalog and parameter value tables
-- Schema: ${recoverySchema}
--
-- REVIEW COPY. The requested names V042_1__parameter_catalog.sql and
-- V042_2__parameter_seed.sql do not satisfy D-RCV-28, which requires one migration per
-- story named V<seq>__<story>_<name>.sql. Commit the consolidated
-- V0042__rwb_e1_042_parameter_catalog_and_seed.sql unless a migration-lint exception is
-- approved for the split. See section 2 of the clarification pack.
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
          AND conrelid = to_regclass('${recoverySchema}.parameter_catalog')
    ) THEN
        ALTER TABLE ${recoverySchema}.parameter_catalog
            ADD CONSTRAINT uk_parameter_catalog UNIQUE (param_key);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_catalog_scope'
          AND conrelid = to_regclass('${recoverySchema}.parameter_catalog')
    ) THEN
        ALTER TABLE ${recoverySchema}.parameter_catalog
            ADD CONSTRAINT ck_parameter_catalog_scope
            CHECK (scope IN ('GLOBAL', 'PRODUCT'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_catalog_kind'
          AND conrelid = to_regclass('${recoverySchema}.parameter_catalog')
    ) THEN
        ALTER TABLE ${recoverySchema}.parameter_catalog
            ADD CONSTRAINT ck_parameter_catalog_kind
            CHECK (kind IN ('BUSINESS', 'ENVIRONMENT'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_catalog_value_type'
          AND conrelid = to_regclass('${recoverySchema}.parameter_catalog')
    ) THEN
        ALTER TABLE ${recoverySchema}.parameter_catalog
            ADD CONSTRAINT ck_parameter_catalog_value_type
            CHECK (value_type IN ('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'DATE', 'TIME',
                                  'DURATION', 'CODE', 'CODE_LIST', 'JSON'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_catalog_environments'
          AND conrelid = to_regclass('${recoverySchema}.parameter_catalog')
    ) THEN
        ALTER TABLE ${recoverySchema}.parameter_catalog
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
          AND conrelid = to_regclass('${recoverySchema}.parameter_catalog')
    ) THEN
        ALTER TABLE ${recoverySchema}.parameter_catalog
            ADD CONSTRAINT ck_parameter_catalog_secret_default
            CHECK (NOT (secret AND default_value IS NOT NULL));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'uk_parameter_value'
          AND conrelid = to_regclass('${recoverySchema}.parameter_value')
    ) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT uk_parameter_value
            UNIQUE (param_key, environment, product_group, version_no);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_value_environment'
          AND conrelid = to_regclass('${recoverySchema}.parameter_value')
    ) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT ck_parameter_value_environment
            CHECK (environment IN ('DEV', 'SIT', 'UAT', 'PROD'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_value_status'
          AND conrelid = to_regclass('${recoverySchema}.parameter_value')
    ) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT ck_parameter_value_status
            CHECK (status IN ('VALIDATED', 'APPROVED', 'IN_FORCE', 'SUPERSEDED', 'ROLLED_BACK', 'REFUSED'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_value_dates'
          AND conrelid = to_regclass('${recoverySchema}.parameter_value')
    ) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT ck_parameter_value_dates
            CHECK (valid_to IS NULL OR valid_to >= valid_from);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_value_version'
          AND conrelid = to_regclass('${recoverySchema}.parameter_value')
    ) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT ck_parameter_value_version
            CHECK (version_no >= 1);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_value_maker_checker'
          AND conrelid = to_regclass('${recoverySchema}.parameter_value')
    ) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT ck_parameter_value_maker_checker
            CHECK (approver_user_id IS NULL OR approver_user_id <> author_user_id);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_parameter_value_approved_at'
          AND conrelid = to_regclass('${recoverySchema}.parameter_value')
    ) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT ck_parameter_value_approved_at
            CHECK (status NOT IN ('APPROVED', 'IN_FORCE') OR approved_at IS NOT NULL);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_parameter_value_catalog'
          AND conrelid = to_regclass('${recoverySchema}.parameter_value')
    ) THEN
        ALTER TABLE ${recoverySchema}.parameter_value
            ADD CONSTRAINT fk_parameter_value_catalog
            FOREIGN KEY (param_key)
            REFERENCES ${recoverySchema}.parameter_catalog (param_key);
    END IF;
END;
$$;

-- Lookup index required by the story: the approved value in force for a key and
-- environment on a business date.
CREATE INDEX IF NOT EXISTS ix_parameter_value_in_force
    ON ${recoverySchema}.parameter_value (param_key, environment, valid_from)
    WHERE status = 'APPROVED';

-- Product-scoped lookup. The story's service also accepts a product group; the index
-- keeps that read on one index without changing the story's required index.
CREATE INDEX IF NOT EXISTS ix_parameter_value_lookup
    ON ${recoverySchema}.parameter_value (param_key, environment, product_group, valid_from DESC)
    WHERE status IN ('APPROVED', 'IN_FORCE');

-- The Physical Schema unique key includes nullable product_group. PostgreSQL treats
-- NULLs as distinct, so the constraint alone does not stop two version 1 rows for the
-- same global key and environment. This expression index closes that hole. The sentinel
-- '*' is not a valid LOV-PRODUCT value.
CREATE UNIQUE INDEX IF NOT EXISTS ux_parameter_value_version_all
    ON ${recoverySchema}.parameter_value
       (param_key, environment, COALESCE(product_group, '*'), version_no);

-- One approved value per key, environment, product group and valid-from date. This is
-- the database guard behind the load rule that a second approved version cannot share a
-- valid-from date; the service returns MSG-P3-027 before the insert.
CREATE UNIQUE INDEX IF NOT EXISTS ux_parameter_value_approved_from
    ON ${recoverySchema}.parameter_value
       (param_key, environment, COALESCE(product_group, '*'), valid_from)
    WHERE status IN ('APPROVED', 'IN_FORCE');

COMMENT ON TABLE ${recoverySchema}.parameter_catalog
    IS 'The definition of every parameter and environment setting, with its owner and default.';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.id
    IS 'Record identifier of the parameter definition';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.param_key
    IS 'Parameter key, for example case.entry.dpd';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.kind
    IS 'Kind of parameter, for example ENVIRONMENT for an environment setting';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.value_type
    IS 'Type of the value: STRING, INTEGER, DECIMAL, BOOLEAN, DATE, TIME, DURATION, CODE, CODE_LIST or JSON';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.unit
    IS 'Unit, for example CALENDAR_DAYS, WORKING_DAYS, BAHT, PERCENT, COUNT, CODE_LIST';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.min_value
    IS 'Lowest allowed value';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.max_value
    IS 'Highest allowed value';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.default_value
    IS 'Default value; never set for a secret';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.scope
    IS 'Product, when the parameter is keyed by product group, or global';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.required
    IS 'True when every product in force must have a row';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.owner_role
    IS 'Role that owns the parameter';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.environments
    IS 'Environments the parameter is set in, as a comma-separated list of DEV, SIT, UAT, PROD';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.used_by
    IS 'Modules and stories that read the parameter';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.secret
    IS 'True for a secret; its value is never returned';
COMMENT ON COLUMN ${recoverySchema}.parameter_catalog.description
    IS 'What the parameter controls';

COMMENT ON TABLE ${recoverySchema}.parameter_value
    IS 'An approved, dated value version of a parameter per environment and product group.';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.id
    IS 'Record identifier of the parameter value';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.param_key
    IS 'Parameter, from parameter_catalog';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.environment
    IS 'DEV, SIT, UAT or PROD';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.param_value
    IS 'Value as text';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.product_group
    IS 'Product group for a product-scoped parameter; null for a global parameter';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.version_no
    IS 'Version number, starting at 1';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.valid_from
    IS 'Date the value comes into force';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.valid_to
    IS 'Last date the value is in force';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.status
    IS 'Validated, approved, in force, superseded, rolled back or refused';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.author_user_id
    IS 'Who loaded the value';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.approver_user_id
    IS 'Who approved the value; never the author';
COMMENT ON COLUMN ${recoverySchema}.parameter_value.approved_at
    IS 'When the value was approved';
