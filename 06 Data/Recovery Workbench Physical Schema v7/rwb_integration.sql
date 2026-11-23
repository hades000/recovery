-- SCB Collections and Recovery. Henka Group, 22 November 2026.
-- (C) Siam Commercial Bank and Henka Pte Ltd
-- Recovery Workbench physical schema, PostgreSQL. Service rwb-integration (P2, Integration), wave 1. Version 7.
-- Change log: 7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.
-- Schema rwb_integration; login rwb_integration; REST base /api/recovery/integration/v1; topic rwb.integration.events.v1; queue rwb-integration.
-- Source: 06 Data/Recovery Workbench Physical Schema v6.sql (read only). Table, index, comment and seed text is copied unchanged; only the schema and the foreign keys change.
-- Tables in this file: 5. Owned by this service in the Ownership Map v1: 3. Platform library objects created here as well: 4.
-- Owner for every object comes from Recovery Workbench Microservice Ownership Map v1 (D-RCV-60).
-- Cross-owner references: a foreign key whose two tables have different owners in the Ownership Map is cut to a plain uuid column; integrity is through the owner's API contract (see README.md).

CREATE SCHEMA IF NOT EXISTS rwb_integration;
SET search_path TO rwb_integration;
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

-- Interface config: The settings of one file interface, by version.
CREATE TABLE interface_config (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    interface_id varchar(10) NOT NULL,
    direction varchar(8) NOT NULL,
    transport varchar(10) NOT NULL,
    inbound_path varchar(200),
    file_pattern varchar(120),
    data_product varchar(25),
    max_attempts integer NOT NULL,
    retry_intervals_min varchar(60),
    owner_role varchar(20) NOT NULL,
    alert_role varchar(20),
    valid_from date NOT NULL,
    valid_to date,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_interface_config UNIQUE (interface_id, valid_from)
);

-- Outbound item: One outbound file waiting to be sent, sent or in the exception queue.
CREATE TABLE outbound_item (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    interface_id varchar(10) NOT NULL,
    idempotency_key varchar(120) NOT NULL,
    payload_ref varchar(400) NOT NULL,
    case_ids jsonb,
    attempt_count integer NOT NULL DEFAULT 0,
    next_attempt_at timestamptz,
    status varchar(12) NOT NULL DEFAULT 'PENDING',
    last_error varchar(400),
    owner_role varchar(20) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_outbound_item UNIQUE (idempotency_key)
);

-- Feature flag: A feature flag with its value per environment, owner and removal date.
CREATE TABLE feature_flag (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    flag_key varchar(80) NOT NULL,
    description varchar(400) NOT NULL,
    owner_user_id uuid NOT NULL,
    owner_team varchar(60),
    default_on boolean NOT NULL DEFAULT false,
    dev_on boolean NOT NULL DEFAULT false,
    sit_on boolean NOT NULL DEFAULT false,
    uat_on boolean NOT NULL DEFAULT false,
    prod_on boolean NOT NULL DEFAULT false,
    removal_date date NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_feature_flag UNIQUE (flag_key)
);

-- Hosting note: feature_flag and feature_flag_change are platform library objects owned by PLT in the Ownership Map.
-- They are emitted once, in rwb_integration, because rwb-integration serves the feature-flag admin API
-- (Ownership Map ruling ASM-0039; GAP-0109, ASM-0180).

-- Feature flag change: One change of a feature flag value in one environment.
CREATE TABLE feature_flag_change (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    flag_key varchar(80) NOT NULL,
    environment varchar(4) NOT NULL,
    old_value boolean NOT NULL,
    new_value boolean NOT NULL,
    reason varchar(400) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Job catalog: A scheduled job with its owner, run book and expected duration.
CREATE TABLE job_catalog (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id varchar(6) NOT NULL,
    job_name varchar(80) NOT NULL,
    owner_role varchar(20) NOT NULL,
    schedule_text varchar(120) NOT NULL,
    runbook_path varchar(200),
    expected_minutes integer,
    alert_after_minutes integer,
    first_release varchar(3),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_job_catalog UNIQUE (job_id)
);

-- ---------------------------------------------------------------------------
-- Foreign keys kept inside this service (same owner).
-- ---------------------------------------------------------------------------

ALTER TABLE processed_event ADD CONSTRAINT fk_processed_event_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;
ALTER TABLE outbox_delivery ADD CONSTRAINT fk_outbox_delivery_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------

CREATE INDEX ix_processed_event_event_id ON processed_event (event_id);
CREATE INDEX ix_outbox_event_case_id ON outbox_event (case_id);
CREATE INDEX ix_outbox_delivery_event_id ON outbox_delivery (event_id);
CREATE INDEX ix_outbox_delivery_task_id ON outbox_delivery (task_id);

-- ---------------------------------------------------------------------------
-- Data dictionary comments
-- ---------------------------------------------------------------------------

COMMENT ON TABLE job_catalog IS 'A scheduled job with its owner, run book and expected duration.';
COMMENT ON TABLE feature_flag_change IS 'One change of a feature flag value in one environment.';
COMMENT ON TABLE feature_flag IS 'A feature flag with its value per environment, owner and removal date.';
COMMENT ON TABLE outbox_delivery IS 'The delivery of one outbox event to one consumer, with its retries.';
COMMENT ON TABLE outbox_event IS 'An application event or outbound work request written in the same transaction as the change.';
COMMENT ON TABLE idempotency_key IS 'The stored response of an API request sent with an Idempotency-Key header, kept 24 hours.';
COMMENT ON TABLE processed_event IS 'An event or work key a consumer has already processed, so a repeat is ignored and counted.';
COMMENT ON TABLE outbound_item IS 'One outbound file waiting to be sent, sent or in the exception queue.';
COMMENT ON TABLE interface_config IS 'The settings of one file interface, by version.';
COMMENT ON COLUMN interface_config.id IS 'Record identifier of the interface setting';
COMMENT ON COLUMN interface_config.interface_id IS 'Interface ID, for example INT-10';
COMMENT ON COLUMN interface_config.direction IS 'Inbound or outbound';
COMMENT ON COLUMN interface_config.transport IS 'SFTP or COLLINS';
COMMENT ON COLUMN interface_config.inbound_path IS 'Inbound or outbound folder';
COMMENT ON COLUMN interface_config.file_pattern IS 'File name pattern with the business date';
COMMENT ON COLUMN interface_config.data_product IS 'Data product the file feeds, for example DP06';
COMMENT ON COLUMN interface_config.max_attempts IS 'Most send attempts before the exception queue';
COMMENT ON COLUMN interface_config.retry_intervals_min IS 'Minutes between attempts, comma separated, for example 5,15,45';
COMMENT ON COLUMN interface_config.owner_role IS 'Role that receives the exception task';
COMMENT ON COLUMN interface_config.alert_role IS 'Role alerted on a refused or missing file';
COMMENT ON COLUMN interface_config.valid_from IS 'Date the version comes into force';
COMMENT ON COLUMN interface_config.valid_to IS 'Last date the version is in force';
COMMENT ON COLUMN outbound_item.id IS 'Record identifier of the outbound item';
COMMENT ON COLUMN outbound_item.interface_id IS 'Interface ID';
COMMENT ON COLUMN outbound_item.idempotency_key IS 'Unique key of the outbound work';
COMMENT ON COLUMN outbound_item.payload_ref IS 'Stored file to send';
COMMENT ON COLUMN outbound_item.case_ids IS 'Cases whose step waits on the file';
COMMENT ON COLUMN outbound_item.attempt_count IS 'Attempts made';
COMMENT ON COLUMN outbound_item.next_attempt_at IS 'When the next attempt is due';
COMMENT ON COLUMN outbound_item.status IS 'Pending, sent, retry, exception or acknowledged';
COMMENT ON COLUMN outbound_item.last_error IS 'Last transfer error, no personal data';
COMMENT ON COLUMN outbound_item.owner_role IS 'Role that owns the exception task';
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
COMMENT ON COLUMN feature_flag.id IS 'Record identifier of the feature flag';
COMMENT ON COLUMN feature_flag.flag_key IS 'Flag key rwb.<module>.<short-name>';
COMMENT ON COLUMN feature_flag.description IS 'What the flag switches';
COMMENT ON COLUMN feature_flag.owner_user_id IS 'Owner of the flag';
COMMENT ON COLUMN feature_flag.owner_team IS 'Owning squad';
COMMENT ON COLUMN feature_flag.default_on IS 'Default value';
COMMENT ON COLUMN feature_flag.dev_on IS 'Value in DEV';
COMMENT ON COLUMN feature_flag.sit_on IS 'Value in SIT';
COMMENT ON COLUMN feature_flag.uat_on IS 'Value in UAT';
COMMENT ON COLUMN feature_flag.prod_on IS 'Value in PROD';
COMMENT ON COLUMN feature_flag.removal_date IS 'Date by which the flag and its old path are removed';
COMMENT ON COLUMN feature_flag_change.id IS 'Record identifier of the feature flag change';
COMMENT ON COLUMN feature_flag_change.flag_key IS 'Flag changed';
COMMENT ON COLUMN feature_flag_change.environment IS 'DEV, SIT, UAT or PROD';
COMMENT ON COLUMN feature_flag_change.old_value IS 'Value before';
COMMENT ON COLUMN feature_flag_change.new_value IS 'Value after';
COMMENT ON COLUMN feature_flag_change.reason IS 'Reason for the change';
COMMENT ON COLUMN job_catalog.id IS 'Record identifier of the job';
COMMENT ON COLUMN job_catalog.job_id IS 'Job ID JOB-nn';
COMMENT ON COLUMN job_catalog.job_name IS 'Job name from the batch schedule';
COMMENT ON COLUMN job_catalog.owner_role IS 'Role that owns failures';
COMMENT ON COLUMN job_catalog.schedule_text IS 'Schedule as in the batch schedule';
COMMENT ON COLUMN job_catalog.runbook_path IS 'Path of the run book in the repository';
COMMENT ON COLUMN job_catalog.expected_minutes IS 'Expected duration in minutes';
COMMENT ON COLUMN job_catalog.alert_after_minutes IS 'Duration after which the owner is alerted';
COMMENT ON COLUMN job_catalog.first_release IS 'Epic of first release, for example E1';

-- ---------------------------------------------------------------------------
-- Cross-service references cut from this file (no database foreign key)
-- ---------------------------------------------------------------------------
-- outbox_event.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- outbox_delivery.task_id -> rwb_case.task.id (owner P3); the column stays uuid and integrity is through the owner's contract.
