-- SCB Collections and Recovery. Henka Group, 22 November 2026.
-- (C) Siam Commercial Bank and Henka Pte Ltd
-- Recovery Workbench physical schema, PostgreSQL. Service rwb-deviation (S8, Deviation), wave 2. Version 7.
-- Change log: 7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.
-- Change log: 9, 27 November 2026, D-RCV-60 P1 developer readiness (RD-P1 register); targeted edits.
-- Schema rwb_deviation; login rwb_deviation; REST base /api/recovery/deviation/v1; topic rwb.deviation.events.v1; queue rwb-deviation.
-- Source: 06 Data/Recovery Workbench Physical Schema v6.sql (read only). Table, index, comment and seed text is copied unchanged; only the schema and the foreign keys change.
-- Tables in this file: 1. Owned by this service in the Ownership Map v1: 1. Platform library objects created here as well: 4.
-- Owner for every object comes from Recovery Workbench Microservice Ownership Map v1 (D-RCV-60).
-- Cross-owner references: a foreign key whose two tables have different owners in the Ownership Map is cut to a plain uuid column; integrity is through the owner's API contract (see README.md).

CREATE SCHEMA IF NOT EXISTS rwb_deviation;
SET search_path TO rwb_deviation;
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

-- Deviation: A deviation X1 to X7 raised on a case.
CREATE TABLE deviation (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,  -- cross-service reference: rwb_case.recovery_case(id); integrity through the owner's contract
    deviation_code varchar(3) NOT NULL,
    raised_at timestamptz NOT NULL,
    raised_by varchar(20) NOT NULL,
    paused_state varchar(60) NOT NULL,
    handler_user_id uuid,
    contact_stop boolean NOT NULL DEFAULT false,
    cleared_at timestamptz,
    outcome varchar(20),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- ---------------------------------------------------------------------------
-- Foreign keys kept inside this service (same owner).
-- ---------------------------------------------------------------------------

ALTER TABLE processed_event ADD CONSTRAINT fk_processed_event_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;
ALTER TABLE outbox_delivery ADD CONSTRAINT fk_outbox_delivery_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------

CREATE INDEX ix_deviation_case_id ON deviation (case_id);
CREATE INDEX ix_processed_event_event_id ON processed_event (event_id);
CREATE INDEX ix_outbox_event_case_id ON outbox_event (case_id);
CREATE INDEX ix_outbox_delivery_event_id ON outbox_delivery (event_id);
CREATE INDEX ix_outbox_delivery_task_id ON outbox_delivery (task_id);

-- ---------------------------------------------------------------------------
-- Data dictionary comments
-- ---------------------------------------------------------------------------

COMMENT ON TABLE outbox_delivery IS 'The delivery of one outbox event to one consumer, with its retries.';
COMMENT ON TABLE outbox_event IS 'An application event or outbound work request written in the same transaction as the change.';
COMMENT ON TABLE idempotency_key IS 'The stored response of an API request sent with an Idempotency-Key header, kept 24 hours.';
COMMENT ON TABLE processed_event IS 'An event or work key a consumer has already processed, so a repeat is ignored and counted.';
COMMENT ON TABLE deviation IS 'A deviation X1 to X7 raised on a case.';
COMMENT ON COLUMN deviation.id IS 'Record identifier of the deviation';
COMMENT ON COLUMN deviation.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN deviation.deviation_code IS 'X1 to X7';
COMMENT ON COLUMN deviation.raised_at IS 'When it was raised';
COMMENT ON COLUMN deviation.raised_by IS 'Screening agent, rule, officer, customer contact';
COMMENT ON COLUMN deviation.paused_state IS 'The routing state the case was in when paused';
COMMENT ON COLUMN deviation.handler_user_id IS 'The named handler';
COMMENT ON COLUMN deviation.contact_stop IS 'True when customer contact is stopped';
COMMENT ON COLUMN deviation.cleared_at IS 'When it cleared';
COMMENT ON COLUMN deviation.outcome IS 'Returned, re-routed, case ended';
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

-- ---------------------------------------------------------------------------
-- Cross-service references cut from this file (no database foreign key)
-- ---------------------------------------------------------------------------
-- deviation.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- outbox_event.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- outbox_delivery.task_id -> rwb_case.task.id (owner P3); the column stays uuid and integrity is through the owner's contract.

-- ---------------------------------------------------------------------------
-- Migration provenance columns (RD-P1-027; 27 November 2026). Added once per table by the owner's own Flyway step;
-- null for rows created live. LOV-MIGRATION-SOURCE values are Pending, owner data owner (GAP-3275).
-- ---------------------------------------------------------------------------
ALTER TABLE deviation ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN deviation.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN deviation.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
