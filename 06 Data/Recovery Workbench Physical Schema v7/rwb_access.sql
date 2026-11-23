-- SCB Collections and Recovery. Henka Group, 22 November 2026.
-- (C) Siam Commercial Bank and Henka Pte Ltd
-- Recovery Workbench physical schema, PostgreSQL. Service rwb-access (P4, Access and authority), wave 1. Version 7.
-- Change log: 7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.
-- Schema rwb_access; login rwb_access; REST base /api/recovery/access/v1; topic rwb.access.events.v1; queue rwb-access.
-- Source: 06 Data/Recovery Workbench Physical Schema v6.sql (read only). Table, index, comment and seed text is copied unchanged; only the schema and the foreign keys change.
-- Tables in this file: 5. Owned by this service in the Ownership Map v1: 5. Platform library objects created here as well: 4.
-- Owner for every object comes from Recovery Workbench Microservice Ownership Map v1 (D-RCV-60).
-- Cross-owner references: a foreign key whose two tables have different owners in the Ownership Map is cut to a plain uuid column; integrity is through the owner's API contract (see README.md).

CREATE SCHEMA IF NOT EXISTS rwb_access;
SET search_path TO rwb_access;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ---------------------------------------------------------------------------
-- Platform library objects (owner PLT in the Ownership Map; DP-09, RWB-PLT-TE006-CON).
-- Created in every service schema. No foreign key to a business table.
-- ---------------------------------------------------------------------------

-- Outbox event: An application event or outbound work request written in the same transaction as the change.
CREATE TABLE outbox_event (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type varchar(40) NOT NULL,
    schema_version integer NOT NULL,
    case_id uuid,  -- cross-service reference: rwb_case.recovery_case(id); integrity through the owner's contract
    case_seq bigint,
    idempotency_key varchar(120) NOT NULL,
    payload jsonb NOT NULL,
    actor_ref varchar(64),
    occurred_at timestamptz NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_outbox_event UNIQUE (case_seq, idempotency_key)
);

-- Outbox delivery: The delivery of one outbox event to one consumer, with its retries.
CREATE TABLE outbox_delivery (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id uuid NOT NULL,
    consumer varchar(60) NOT NULL,
    status varchar(12) NOT NULL DEFAULT 'PENDING',
    attempt_count integer NOT NULL DEFAULT 0,
    next_attempt_at timestamptz NOT NULL,
    last_error_code varchar(40),
    delivered_at timestamptz,
    task_id uuid,  -- cross-service reference: rwb_case.task(id); integrity through the owner's contract
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_outbox_delivery UNIQUE (event_id, consumer)
);

-- Processed event: An event or work key a consumer has already processed, so a repeat is ignored and counted.
CREATE TABLE processed_event (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    consumer varchar(60) NOT NULL,
    idempotency_key varchar(120) NOT NULL,
    event_id uuid,
    hit_count integer NOT NULL DEFAULT 1,
    last_seen_at timestamptz,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_processed_event UNIQUE (consumer, idempotency_key)
);

-- Idempotency key: The stored response of an API request sent with an Idempotency-Key header, kept 24 hours.
CREATE TABLE idempotency_key (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    idempotency_key uuid NOT NULL,
    endpoint varchar(100) NOT NULL,
    request_hash char(64) NOT NULL,
    response jsonb NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_idempotency_key UNIQUE (idempotency_key)
);

-- Delegation limit: An approval limit by decision, level, product and amount.
CREATE TABLE delegation_limit (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    decision_code varchar(8) NOT NULL,
    approval_level varchar(4) NOT NULL,
    product_group varchar(15) NOT NULL,
    principal_limit numeric(18,2),
    loss_pct_limit numeric(5,2),
    min_price_pct_fmv numeric(5,2),
    holder_user_id uuid,
    substitute_user_id uuid,
    valid_from date NOT NULL,
    valid_to date,
    limit_version varchar(20) NOT NULL,
    regulation_item varchar(10) NOT NULL,
    applies_when varchar(40),
    max_loss_amount numeric(18,2),
    max_delay_count integer,
    min_price_pct_principal numeric(5,2),
    min_received_pct numeric(5,2),
    max_term_years numeric(4,1),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Role: A Workbench role, held as data.
CREATE TABLE role (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    role_code varchar(20) NOT NULL,
    role_name varchar(80) NOT NULL,
    role_class varchar(15) NOT NULL,
    default_scope varchar(8) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_role UNIQUE (role_code)
);

-- Permission: What a role may do in one capability area.
CREATE TABLE permission (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id uuid NOT NULL,
    capability_area varchar(30) NOT NULL,
    letters varchar(5) NOT NULL DEFAULT '-',
    matrix_version varchar(20) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Masking rule: Which role sees which personal data field unmasked, by version.
CREATE TABLE masking_rule (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    role_code varchar(20) NOT NULL,
    field_id varchar(16) NOT NULL,
    unmasked boolean NOT NULL DEFAULT false,
    masking_version varchar(20) NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_masking_rule UNIQUE (role_code, field_id, masking_version)
);

-- Role conflict: A pair of roles one person may not hold together, by version.
CREATE TABLE role_conflict (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    role_code varchar(20) NOT NULL,
    conflicts_with varchar(30) NOT NULL,
    reason varchar(200) NOT NULL,
    conflict_version varchar(20) NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_role_conflict UNIQUE (role_code, conflicts_with, conflict_version)
);

-- ---------------------------------------------------------------------------
-- Foreign keys kept inside this service (same owner).
-- ---------------------------------------------------------------------------

ALTER TABLE permission ADD CONSTRAINT fk_permission_role_id FOREIGN KEY (role_id) REFERENCES role (id) ON DELETE RESTRICT;
ALTER TABLE processed_event ADD CONSTRAINT fk_processed_event_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;
ALTER TABLE outbox_delivery ADD CONSTRAINT fk_outbox_delivery_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------

CREATE INDEX ix_permission_role_id ON permission (role_id);
CREATE INDEX ix_processed_event_event_id ON processed_event (event_id);
CREATE INDEX ix_outbox_event_case_id ON outbox_event (case_id);
CREATE INDEX ix_outbox_delivery_event_id ON outbox_delivery (event_id);
CREATE INDEX ix_outbox_delivery_task_id ON outbox_delivery (task_id);

-- ---------------------------------------------------------------------------
-- Data dictionary comments
-- ---------------------------------------------------------------------------

COMMENT ON TABLE role_conflict IS 'A pair of roles one person may not hold together, by version.';
COMMENT ON TABLE masking_rule IS 'Which role sees which personal data field unmasked, by version.';
COMMENT ON TABLE outbox_delivery IS 'The delivery of one outbox event to one consumer, with its retries.';
COMMENT ON TABLE outbox_event IS 'An application event or outbound work request written in the same transaction as the change.';
COMMENT ON TABLE idempotency_key IS 'The stored response of an API request sent with an Idempotency-Key header, kept 24 hours.';
COMMENT ON TABLE processed_event IS 'An event or work key a consumer has already processed, so a repeat is ignored and counted.';
COMMENT ON TABLE permission IS 'What a role may do in one capability area.';
COMMENT ON TABLE role IS 'A Workbench role, held as data.';
COMMENT ON TABLE delegation_limit IS 'An approval limit by decision, level, product and amount.';
COMMENT ON COLUMN delegation_limit.id IS 'Record identifier of the delegation limit';
COMMENT ON COLUMN delegation_limit.decision_code IS 'Decision the limit applies to';
COMMENT ON COLUMN delegation_limit.approval_level IS 'Level 1 to 6 under Regulation กกค.540031';
COMMENT ON COLUMN delegation_limit.product_group IS 'Product group';
COMMENT ON COLUMN delegation_limit.principal_limit IS 'Principal limit, baht; empty means no limit';
COMMENT ON COLUMN delegation_limit.loss_pct_limit IS 'Loss limit as a percentage';
COMMENT ON COLUMN delegation_limit.min_price_pct_fmv IS 'Lowest sale price as a percentage of fair market value';
COMMENT ON COLUMN delegation_limit.holder_user_id IS 'Person holding the level';
COMMENT ON COLUMN delegation_limit.substitute_user_id IS 'Substitute when the holder is absent';
COMMENT ON COLUMN delegation_limit.valid_from IS 'Valid from';
COMMENT ON COLUMN delegation_limit.valid_to IS 'Valid to';
COMMENT ON COLUMN delegation_limit.limit_version IS 'Delegation version the row belongs to, for example DOA-2026.11';
COMMENT ON COLUMN delegation_limit.regulation_item IS 'Item of Regulation กกค.540031, for example 2.1.1; one decision code covers several items';
COMMENT ON COLUMN delegation_limit.applies_when IS 'Case condition that selects the row, WO_CRITERIA_MET or WO_CRITERIA_NOT_MET for item 2.1.10';
COMMENT ON COLUMN delegation_limit.max_loss_amount IS 'Maximum loss the level may approve, baht';
COMMENT ON COLUMN delegation_limit.max_delay_count IS 'Most delays of legal action, seizure or auction the level may approve on a case';
COMMENT ON COLUMN delegation_limit.min_price_pct_principal IS 'Lowest sale price as a percentage of principal outstanding';
COMMENT ON COLUMN delegation_limit.min_received_pct IS 'Lowest amount received against the total debt, percent';
COMMENT ON COLUMN delegation_limit.max_term_years IS 'Longest lease term the level may approve, years';
COMMENT ON COLUMN role.id IS 'Record identifier of the role';
COMMENT ON COLUMN role.role_code IS 'Role code, for example RW-CASEOWN';
COMMENT ON COLUMN role.role_name IS 'Role name';
COMMENT ON COLUMN role.role_class IS 'Bank user, partner user, non-human actor';
COMMENT ON COLUMN role.default_scope IS 'Own, team, region, all';
COMMENT ON COLUMN permission.id IS 'Record identifier of the permission';
COMMENT ON COLUMN permission.role_id IS 'The role this record belongs to';
COMMENT ON COLUMN permission.capability_area IS 'One of the 14 capability areas';
COMMENT ON COLUMN permission.letters IS 'C, R, U, D and A, or a dash for none';
COMMENT ON COLUMN permission.matrix_version IS 'Permission matrix version';
COMMENT ON COLUMN processed_event.id IS 'Record identifier of the processed event';
COMMENT ON COLUMN processed_event.consumer IS 'Consumer name';
COMMENT ON COLUMN processed_event.idempotency_key IS 'Event or work key';
COMMENT ON COLUMN processed_event.event_id IS 'Outbox event of the first delivery, where the key came from an event';
COMMENT ON COLUMN processed_event.hit_count IS 'Deliveries seen, 1 on first';
COMMENT ON COLUMN processed_event.last_seen_at IS 'When the last repeat arrived';
COMMENT ON COLUMN idempotency_key.id IS 'Record identifier of the idempotent request';
COMMENT ON COLUMN idempotency_key.idempotency_key IS 'Idempotency-Key header value';
COMMENT ON COLUMN idempotency_key.endpoint IS 'Method and path of the request';
COMMENT ON COLUMN idempotency_key.request_hash IS 'SHA-256 of the request body';
COMMENT ON COLUMN idempotency_key.response IS 'Stored response returned to a repeat';
COMMENT ON COLUMN outbox_event.id IS 'Record identifier of the outbox event';
COMMENT ON COLUMN outbox_event.event_type IS 'Event name from EV-01 to EV-28, or an outbound work request type such as WIN_DISPATCH';
COMMENT ON COLUMN outbox_event.schema_version IS 'Schema version of the payload; consumers accept the current and previous version';
COMMENT ON COLUMN outbox_event.case_id IS 'The case the event belongs to; empty for events with no case; unique with case_seq';
COMMENT ON COLUMN outbox_event.case_seq IS 'Order of the event among the events of its case';
COMMENT ON COLUMN outbox_event.idempotency_key IS 'Key passed to every consumer so a repeat is dropped; unique on its own';
COMMENT ON COLUMN outbox_event.payload IS 'References and codes only; no personal data';
COMMENT ON COLUMN outbox_event.actor_ref IS 'User ID or service identity that caused the event';
COMMENT ON COLUMN outbox_event.occurred_at IS 'When the change happened';
COMMENT ON COLUMN outbox_delivery.id IS 'Record identifier of the outbox delivery';
COMMENT ON COLUMN outbox_delivery.event_id IS 'The outbox event delivered';
COMMENT ON COLUMN outbox_delivery.consumer IS 'Consumer name from the consumer list; unique with event_id';
COMMENT ON COLUMN outbox_delivery.status IS 'Pending, retrying, delivered or exception';
COMMENT ON COLUMN outbox_delivery.attempt_count IS 'Delivery attempts made';
COMMENT ON COLUMN outbox_delivery.next_attempt_at IS 'When the next attempt is due';
COMMENT ON COLUMN outbox_delivery.last_error_code IS 'Code of the last failure returned by the consumer';
COMMENT ON COLUMN outbox_delivery.delivered_at IS 'When the consumer succeeded';
COMMENT ON COLUMN outbox_delivery.task_id IS 'The RESOLVE_OUTBOX_DELIVERY task raised when the delivery entered the exception queue';
COMMENT ON COLUMN masking_rule.id IS 'Record identifier of the masking rule';
COMMENT ON COLUMN masking_rule.role_code IS 'Role the rule applies to';
COMMENT ON COLUMN masking_rule.field_id IS 'BR Field ID of a personal data field (sys_fields.is_personal true)';
COMMENT ON COLUMN masking_rule.unmasked IS 'True when the role sees the field unmasked; no row means masked';
COMMENT ON COLUMN masking_rule.masking_version IS 'Version of the masking rules, for example MASK-2026.11';
COMMENT ON COLUMN masking_rule.valid_from IS 'Date the version comes into force';
COMMENT ON COLUMN masking_rule.valid_to IS 'Last date the version is in force';
COMMENT ON COLUMN role_conflict.id IS 'Record identifier of the role conflict';
COMMENT ON COLUMN role_conflict.role_code IS 'Role that may not be held with the other';
COMMENT ON COLUMN role_conflict.conflicts_with IS 'Role code, or ANY_BUSINESS_ROLE or ANY_OTHER_ROLE, per the Separation of duty sheet';
COMMENT ON COLUMN role_conflict.reason IS 'Why the pair is not allowed';
COMMENT ON COLUMN role_conflict.conflict_version IS 'Version of the conflict table, for example SOD-2026.11';
COMMENT ON COLUMN role_conflict.valid_from IS 'Date the version comes into force';
COMMENT ON COLUMN role_conflict.valid_to IS 'Last date the version is in force';

-- ---------------------------------------------------------------------------
-- Seed and dictionary rows
-- ---------------------------------------------------------------------------

-- Seed: roles
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-CASEOWN', 'Case owner', 'BANK_USER', 'OWN');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-TEAMMGR', 'Team manager', 'BANK_USER', 'TEAM');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-PHONECOL', 'Phone collector', 'BANK_USER', 'OWN');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-FIELDCOL', 'Field collector', 'BANK_USER', 'OWN');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-RESTRUCT', 'Restructuring officer (FCR)', 'BANK_USER', 'TEAM');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-SPECIAL', 'Hardship and vulnerability specialist', 'BANK_USER', 'TEAM');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-COMPLAIN', 'Complaint officer', 'BANK_USER', 'TEAM');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-FRAUD', 'Fraud investigator', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-LITOFF', 'Litigation officer', 'BANK_USER', 'TEAM');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-ENFORCE', 'Enforcement owner', 'BANK_USER', 'TEAM');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-LEGAL', 'Legal counsel', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-SALEOFF', 'Sale officer', 'BANK_USER', 'TEAM');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-NPAMGR', 'NPA and asset manager', 'BANK_USER', 'TEAM');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-DEBTSALE', 'Debt sale officer', 'BANK_USER', 'TEAM');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-WRITEOFF', 'Write-off team member', 'BANK_USER', 'TEAM');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-CREDITAD', 'Credit Administration officer', 'BANK_USER', 'TEAM');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-GUARANT', 'Guarantee officer', 'BANK_USER', 'TEAM');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-AGENCYMG', 'Partner and agency manager', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-CONDUCT', 'Conduct and QA officer', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-CAPACITY', 'Capacity and workforce planner', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-PRODHEAD', 'Product head (Mortgage, HP, SSME)', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-HEADLIT', 'Head of Litigation', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-HEADNPA', 'Head of NPA', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-HEADASL', 'Head of Asset Liquidity', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-CREDCOMM', 'Credit approval committee member', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-WOCOMM', 'Write-off committee member', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-RISK', 'Risk and model risk officer', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-COE', 'Center of excellence analyst', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-DATASTEW', 'Data steward and data product owner', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-FINANCE', 'Finance and CFO delegate', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-AUDIT', 'Internal audit', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-COMPLY', 'Compliance and PDPA officer', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-PLATADM', 'Platform administrator', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-REFADM', 'Reference data administrator', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-SECADM', 'Security administrator', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-BIANAL', 'Reporting and BI analyst', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('RW-TRIBE', 'Tribe lead and squad members', 'BANK_USER', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('PT-AGENCY', 'Collection agency (OA) user', 'PARTNER_USER', 'OWN');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('PT-LAWFIRM', 'Law firm user', 'PARTNER_USER', 'OWN');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('PT-VALUER', 'Valuer', 'PARTNER_USER', 'OWN');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('PT-AUCTION', 'Auction vendor', 'PARTNER_USER', 'OWN');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('PT-BUYER', 'Debt buyer and AMC', 'PARTNER_USER', 'OWN');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('PT-RAMC', 'RAMC user', 'PARTNER_USER', 'OWN');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('PT-LED', 'Legal Execution Department and court officer', 'PARTNER_USER', 'OWN');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('CU-BORROW', 'Customer (borrower)', 'CUSTOMER_PARTY', 'OWN');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('CU-GUARANT', 'Guarantor and co-borrower', 'CUSTOMER_PARTY', 'OWN');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('CU-HEIR', 'Heir and estate representative', 'CUSTOMER_PARTY', 'OWN');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('CU-BIDDER', 'Retail asset bidder', 'CUSTOMER_PARTY', 'OWN');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('SY-CASEWF', 'Case workflow module', 'NON_HUMAN_ACTOR', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('SY-RULES', 'Rules component', 'NON_HUMAN_ACTOR', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('SY-DATALOAD', 'Data load from COLLINS', 'NON_HUMAN_ACTOR', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('SY-OCR', 'OCR and extraction pipeline', 'NON_HUMAN_ACTOR', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('SY-DECLOG', 'Decision log writer', 'NON_HUMAN_ACTOR', 'ALL');
INSERT INTO role (role_code, role_name, role_class, default_scope) VALUES ('SY-AGENT', 'Agent platform', 'NON_HUMAN_ACTOR', 'ALL');
-- Seed: the permission matrix, version 1
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'CRU', '1' FROM role WHERE role_code = 'RW-CASEOWN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-CASEOWN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'CRU', '1' FROM role WHERE role_code = 'RW-CASEOWN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-CASEOWN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-CASEOWN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'RW-CASEOWN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-CASEOWN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-CASEOWN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-CASEOWN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'R', '1' FROM role WHERE role_code = 'RW-CASEOWN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-CASEOWN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-TEAMMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'CRUA', '1' FROM role WHERE role_code = 'RW-TEAMMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'R', '1' FROM role WHERE role_code = 'RW-TEAMMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-TEAMMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-TEAMMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-TEAMMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-TEAMMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-TEAMMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-TEAMMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'R', '1' FROM role WHERE role_code = 'RW-TEAMMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-TEAMMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-PHONECOL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-PHONECOL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-PHONECOL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-PHONECOL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-PHONECOL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-FIELDCOL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-FIELDCOL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-FIELDCOL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CR', '1' FROM role WHERE role_code = 'RW-FIELDCOL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-FIELDCOL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'RU', '1' FROM role WHERE role_code = 'RW-RESTRUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-RESTRUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'CRUA', '1' FROM role WHERE role_code = 'RW-RESTRUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'RW-RESTRUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-RESTRUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-RESTRUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-RESTRUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-RESTRUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'RU', '1' FROM role WHERE role_code = 'RW-SPECIAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-SPECIAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'CRU', '1' FROM role WHERE role_code = 'RW-SPECIAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'RW-SPECIAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-SPECIAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-SPECIAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-SPECIAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-SPECIAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'RU', '1' FROM role WHERE role_code = 'RW-COMPLAIN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-COMPLAIN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'R', '1' FROM role WHERE role_code = 'RW-COMPLAIN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-COMPLAIN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-COMPLAIN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'RW-COMPLAIN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-COMPLAIN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-COMPLAIN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-COMPLAIN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-COMPLAIN';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'RU', '1' FROM role WHERE role_code = 'RW-FRAUD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-FRAUD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'R', '1' FROM role WHERE role_code = 'RW-FRAUD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-FRAUD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'R', '1' FROM role WHERE role_code = 'RW-FRAUD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'RW-FRAUD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-FRAUD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-FRAUD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-FRAUD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-FRAUD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'RU', '1' FROM role WHERE role_code = 'RW-LITOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-LITOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'R', '1' FROM role WHERE role_code = 'RW-LITOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'CRUA', '1' FROM role WHERE role_code = 'RW-LITOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-LITOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'RW-LITOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-LITOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-LITOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-LITOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'CRU', '1' FROM role WHERE role_code = 'RW-LITOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-LITOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'RU', '1' FROM role WHERE role_code = 'RW-ENFORCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-ENFORCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'CRU', '1' FROM role WHERE role_code = 'RW-ENFORCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'CRU', '1' FROM role WHERE role_code = 'RW-ENFORCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'RW-ENFORCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-ENFORCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-ENFORCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-ENFORCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'CRU', '1' FROM role WHERE role_code = 'RW-ENFORCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-ENFORCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-LEGAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'R', '1' FROM role WHERE role_code = 'RW-LEGAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'RA', '1' FROM role WHERE role_code = 'RW-LEGAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-LEGAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRUA', '1' FROM role WHERE role_code = 'RW-LEGAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-LEGAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'RU', '1' FROM role WHERE role_code = 'RW-LEGAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-LEGAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'R', '1' FROM role WHERE role_code = 'RW-LEGAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-LEGAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'RU', '1' FROM role WHERE role_code = 'RW-SALEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-SALEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-SALEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'CRUA', '1' FROM role WHERE role_code = 'RW-SALEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'RW-SALEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'RW-SALEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-SALEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-SALEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-SALEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'CRU', '1' FROM role WHERE role_code = 'RW-SALEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-SALEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-NPAMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-NPAMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'CRU', '1' FROM role WHERE role_code = 'RW-NPAMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'RW-NPAMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'RW-NPAMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-NPAMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-NPAMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-NPAMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'CRU', '1' FROM role WHERE role_code = 'RW-NPAMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-NPAMGR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'RU', '1' FROM role WHERE role_code = 'RW-DEBTSALE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-DEBTSALE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-DEBTSALE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-DEBTSALE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'CRUA', '1' FROM role WHERE role_code = 'RW-DEBTSALE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'R', '1' FROM role WHERE role_code = 'RW-DEBTSALE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'RW-DEBTSALE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-DEBTSALE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-DEBTSALE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-DEBTSALE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'CRU', '1' FROM role WHERE role_code = 'RW-DEBTSALE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-DEBTSALE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-WRITEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-WRITEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-WRITEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'RW-WRITEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'CRU', '1' FROM role WHERE role_code = 'RW-WRITEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'RW-WRITEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-WRITEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-WRITEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-WRITEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-WRITEOFF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-CREDITAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-CREDITAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-CREDITAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'RW-CREDITAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'CRUA', '1' FROM role WHERE role_code = 'RW-CREDITAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'RW-CREDITAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-CREDITAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-CREDITAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-CREDITAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-CREDITAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'RU', '1' FROM role WHERE role_code = 'RW-GUARANT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-GUARANT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'CRU', '1' FROM role WHERE role_code = 'RW-GUARANT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-GUARANT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'RW-GUARANT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-GUARANT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-GUARANT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-GUARANT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'CRU', '1' FROM role WHERE role_code = 'RW-GUARANT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-GUARANT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-AGENCYMG';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-AGENCYMG';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-AGENCYMG';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-AGENCYMG';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'RW-AGENCYMG';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-AGENCYMG';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-AGENCYMG';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'RU', '1' FROM role WHERE role_code = 'RW-AGENCYMG';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-AGENCYMG';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'CRUDA', '1' FROM role WHERE role_code = 'RW-AGENCYMG';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-AGENCYMG';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-CONDUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-CONDUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'R', '1' FROM role WHERE role_code = 'RW-CONDUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-CONDUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-CONDUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'RW-CONDUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'R', '1' FROM role WHERE role_code = 'RW-CONDUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-CONDUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-CONDUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-CONDUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-CONDUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'R', '1' FROM role WHERE role_code = 'RW-CONDUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-CONDUCT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-CAPACITY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'RU', '1' FROM role WHERE role_code = 'RW-CAPACITY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-CAPACITY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-CAPACITY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'R', '1' FROM role WHERE role_code = 'RW-CAPACITY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-CAPACITY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-PRODHEAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-PRODHEAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'RA', '1' FROM role WHERE role_code = 'RW-PRODHEAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'RA', '1' FROM role WHERE role_code = 'RW-PRODHEAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'RA', '1' FROM role WHERE role_code = 'RW-PRODHEAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'RA', '1' FROM role WHERE role_code = 'RW-PRODHEAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'RA', '1' FROM role WHERE role_code = 'RW-PRODHEAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-PRODHEAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-PRODHEAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-PRODHEAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-PRODHEAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'R', '1' FROM role WHERE role_code = 'RW-PRODHEAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-PRODHEAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-HEADLIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-HEADLIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'RA', '1' FROM role WHERE role_code = 'RW-HEADLIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-HEADLIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-HEADLIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-HEADLIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-HEADLIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-HEADLIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'RA', '1' FROM role WHERE role_code = 'RW-HEADLIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-HEADLIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-HEADNPA';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-HEADNPA';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'RA', '1' FROM role WHERE role_code = 'RW-HEADNPA';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'RW-HEADNPA';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-HEADNPA';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-HEADNPA';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-HEADNPA';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-HEADNPA';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'RA', '1' FROM role WHERE role_code = 'RW-HEADNPA';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-HEADNPA';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-HEADASL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-HEADASL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'RA', '1' FROM role WHERE role_code = 'RW-HEADASL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'RA', '1' FROM role WHERE role_code = 'RW-HEADASL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-HEADASL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-HEADASL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-HEADASL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-HEADASL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'RA', '1' FROM role WHERE role_code = 'RW-HEADASL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-HEADASL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-CREDCOMM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'RA', '1' FROM role WHERE role_code = 'RW-CREDCOMM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-CREDCOMM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-CREDCOMM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-CREDCOMM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-CREDCOMM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-CREDCOMM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-WOCOMM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'RA', '1' FROM role WHERE role_code = 'RW-WOCOMM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-WOCOMM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-WOCOMM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-WOCOMM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-WOCOMM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-WOCOMM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-RISK';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-RISK';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'R', '1' FROM role WHERE role_code = 'RW-RISK';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-RISK';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-RISK';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'RW-RISK';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'R', '1' FROM role WHERE role_code = 'RW-RISK';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-RISK';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'RA', '1' FROM role WHERE role_code = 'RW-RISK';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-RISK';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-RISK';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'R', '1' FROM role WHERE role_code = 'RW-RISK';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-RISK';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-COE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-COE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'R', '1' FROM role WHERE role_code = 'RW-COE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-COE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-COE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'RW-COE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'R', '1' FROM role WHERE role_code = 'RW-COE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-COE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'CRUD', '1' FROM role WHERE role_code = 'RW-COE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'CRUD', '1' FROM role WHERE role_code = 'RW-COE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-COE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'R', '1' FROM role WHERE role_code = 'RW-COE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-COE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PLATFORM_ADMINISTRATION', 'R', '1' FROM role WHERE role_code = 'RW-COE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-DATASTEW';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-DATASTEW';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-DATASTEW';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'RU', '1' FROM role WHERE role_code = 'RW-DATASTEW';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-DATASTEW';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'CRU', '1' FROM role WHERE role_code = 'RW-DATASTEW';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PLATFORM_ADMINISTRATION', 'R', '1' FROM role WHERE role_code = 'RW-DATASTEW';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-FINANCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-FINANCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'RW-FINANCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'RA', '1' FROM role WHERE role_code = 'RW-FINANCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-FINANCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-FINANCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-FINANCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-FINANCE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-AUDIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-AUDIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'R', '1' FROM role WHERE role_code = 'RW-AUDIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-AUDIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-AUDIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'RW-AUDIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'R', '1' FROM role WHERE role_code = 'RW-AUDIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-AUDIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-AUDIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-AUDIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-AUDIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'R', '1' FROM role WHERE role_code = 'RW-AUDIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-AUDIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PLATFORM_ADMINISTRATION', 'R', '1' FROM role WHERE role_code = 'RW-AUDIT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-COMPLY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-COMPLY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'RU', '1' FROM role WHERE role_code = 'RW-COMPLY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-COMPLY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'RU', '1' FROM role WHERE role_code = 'RW-COMPLY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-COMPLY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'R', '1' FROM role WHERE role_code = 'RW-COMPLY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-COMPLY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PLATFORM_ADMINISTRATION', 'R', '1' FROM role WHERE role_code = 'RW-COMPLY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-PLATADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-PLATADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-PLATADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-PLATADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-PLATADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-PLATADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'R', '1' FROM role WHERE role_code = 'RW-PLATADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-PLATADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PLATFORM_ADMINISTRATION', 'CRUD', '1' FROM role WHERE role_code = 'RW-PLATADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-REFADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'CRUD', '1' FROM role WHERE role_code = 'RW-REFADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-REFADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-REFADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-SECADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-SECADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-SECADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-SECADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PLATFORM_ADMINISTRATION', 'CRUDA', '1' FROM role WHERE role_code = 'RW-SECADM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-BIANAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-BIANAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'R', '1' FROM role WHERE role_code = 'RW-BIANAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-BIANAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-BIANAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'RW-BIANAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'R', '1' FROM role WHERE role_code = 'RW-BIANAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-BIANAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-BIANAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-BIANAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'R', '1' FROM role WHERE role_code = 'RW-BIANAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'CRUD', '1' FROM role WHERE role_code = 'RW-BIANAL';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'RW-TRIBE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'RW-TRIBE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'R', '1' FROM role WHERE role_code = 'RW-TRIBE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'RW-TRIBE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'RW-TRIBE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'RW-TRIBE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'R', '1' FROM role WHERE role_code = 'RW-TRIBE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'RW-TRIBE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'RW-TRIBE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'RW-TRIBE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'R', '1' FROM role WHERE role_code = 'RW-TRIBE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'R', '1' FROM role WHERE role_code = 'RW-TRIBE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REPORTING', 'R', '1' FROM role WHERE role_code = 'RW-TRIBE';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'PT-AGENCY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CR', '1' FROM role WHERE role_code = 'PT-AGENCY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'RU', '1' FROM role WHERE role_code = 'PT-AGENCY';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'PT-LAWFIRM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'RU', '1' FROM role WHERE role_code = 'PT-LAWFIRM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'PT-LAWFIRM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'RU', '1' FROM role WHERE role_code = 'PT-LAWFIRM';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'PT-VALUER';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CR', '1' FROM role WHERE role_code = 'PT-VALUER';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'RU', '1' FROM role WHERE role_code = 'PT-VALUER';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'RU', '1' FROM role WHERE role_code = 'PT-AUCTION';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CR', '1' FROM role WHERE role_code = 'PT-AUCTION';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'RU', '1' FROM role WHERE role_code = 'PT-AUCTION';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'RU', '1' FROM role WHERE role_code = 'PT-BUYER';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'PT-BUYER';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'RU', '1' FROM role WHERE role_code = 'PT-BUYER';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'RU', '1' FROM role WHERE role_code = 'PT-RAMC';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'PT-RAMC';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'PT-RAMC';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'PARTNER_PORTAL', 'RU', '1' FROM role WHERE role_code = 'PT-RAMC';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'CRU', '1' FROM role WHERE role_code = 'SY-CASEWF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'CRU', '1' FROM role WHERE role_code = 'SY-CASEWF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'R', '1' FROM role WHERE role_code = 'SY-CASEWF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'SY-CASEWF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'SY-CASEWF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'SY-CASEWF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'R', '1' FROM role WHERE role_code = 'SY-CASEWF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'SY-CASEWF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'SY-CASEWF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'SY-CASEWF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'C', '1' FROM role WHERE role_code = 'SY-CASEWF';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'SY-RULES';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'SY-RULES';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'R', '1' FROM role WHERE role_code = 'SY-RULES';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'SY-RULES';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'SY-RULES';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'SY-RULES';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'R', '1' FROM role WHERE role_code = 'SY-RULES';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'SY-RULES';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'SY-RULES';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'SY-RULES';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'C', '1' FROM role WHERE role_code = 'SY-RULES';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'CU', '1' FROM role WHERE role_code = 'SY-DATALOAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'U', '1' FROM role WHERE role_code = 'SY-DATALOAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'CU', '1' FROM role WHERE role_code = 'SY-DATALOAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'U', '1' FROM role WHERE role_code = 'SY-DATALOAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'SY-DATALOAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'C', '1' FROM role WHERE role_code = 'SY-DATALOAD';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'SY-OCR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'CRU', '1' FROM role WHERE role_code = 'SY-OCR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'SY-OCR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'C', '1' FROM role WHERE role_code = 'SY-OCR';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'C', '1' FROM role WHERE role_code = 'SY-DECLOG';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'CASE_RECORD', 'R', '1' FROM role WHERE role_code = 'SY-AGENT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'QUEUE_AND_ALLOCATION', 'R', '1' FROM role WHERE role_code = 'SY-AGENT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'TREATMENT_AND_OFFER', 'R', '1' FROM role WHERE role_code = 'SY-AGENT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'LITIGATION', 'R', '1' FROM role WHERE role_code = 'SY-AGENT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'ASSET_AND_DISPOSAL', 'R', '1' FROM role WHERE role_code = 'SY-AGENT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DEBT_SALE', 'R', '1' FROM role WHERE role_code = 'SY-AGENT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'WRITE-OFF_AND_POSTING', 'R', '1' FROM role WHERE role_code = 'SY-AGENT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DOCUMENTS', 'R', '1' FROM role WHERE role_code = 'SY-AGENT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'RULES_AND_PARAMETERS', 'R', '1' FROM role WHERE role_code = 'SY-AGENT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'REFERENCE_DATA', 'R', '1' FROM role WHERE role_code = 'SY-AGENT';
INSERT INTO permission (role_id, capability_area, letters, matrix_version) SELECT id, 'DECISION_LOG', 'C', '1' FROM role WHERE role_code = 'SY-AGENT';

-- ---------------------------------------------------------------------------
-- Cross-service references cut from this file (no database foreign key)
-- ---------------------------------------------------------------------------
-- outbox_event.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- outbox_delivery.task_id -> rwb_case.task.id (owner P3); the column stays uuid and integrity is through the owner's contract.
