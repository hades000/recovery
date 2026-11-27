-- SCB Collections and Recovery. Henka Group, 22 November 2026.
-- (C) Siam Commercial Bank and Henka Pte Ltd
-- Recovery Workbench physical schema, PostgreSQL. Service rwb-reporting (P9, Reporting), wave 1. Version 7.
-- Change log: 7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.
-- Change log: 9, 27 November 2026, D-RCV-60 P1 developer readiness (RD-P1 register); targeted edits.
-- Schema rwb_reporting; login rwb_reporting; REST base /api/recovery/reporting/v1; topic rwb.reporting.events.v1; queue rwb-reporting.
-- Source: 06 Data/Recovery Workbench Physical Schema v6.sql (read only). Table, index, comment and seed text is copied unchanged; only the schema and the foreign keys change.
-- Tables in this file: 3. Owned by this service in the Ownership Map v1: 3. Platform library objects created here as well: 4.
-- Owner for every object comes from Recovery Workbench Microservice Ownership Map v1 (D-RCV-60).
-- Cross-owner references: a foreign key whose two tables have different owners in the Ownership Map is cut to a plain uuid column; integrity is through the owner's API contract (see README.md).

CREATE SCHEMA IF NOT EXISTS rwb_reporting;
SET search_path TO rwb_reporting;
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

-- Measure definition: The agreed definition of a reported measure, by version.
CREATE TABLE measure_definition (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    measure_code varchar(40) NOT NULL,
    name varchar(120) NOT NULL,
    formula varchar(1000) NOT NULL,
    data_product varchar(25) NOT NULL,
    unit varchar(10) NOT NULL,
    definition_version varchar(20) NOT NULL,
    approved_by uuid,
    approved_at timestamptz,
    valid_from date NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_measure_definition UNIQUE (measure_code, definition_version)
);

-- Measure snapshot: The value of one measure for a business date, product and dimension value.
CREATE TABLE measure_snapshot (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    measure_code varchar(40) NOT NULL,
    definition_version varchar(20) NOT NULL,
    business_date date NOT NULL,
    product_group varchar(15),
    dimension_code varchar(20),
    dimension_value varchar(60),
    value numeric(18,4) NOT NULL,
    case_count integer,
    is_baseline boolean NOT NULL DEFAULT false,
    frozen boolean NOT NULL DEFAULT false,
    published_at timestamptz,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Measure publish: Whether the day's dashboard data set was published or held after reconciling to the case list.
CREATE TABLE measure_publish (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    business_date date NOT NULL,
    status varchar(10) NOT NULL,
    case_list_count integer NOT NULL,
    dashboard_count integer NOT NULL,
    held_reason varchar(200),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_measure_publish UNIQUE (business_date)
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

COMMENT ON TABLE measure_publish IS 'Whether the day''s dashboard data set was published or held after reconciling to the case list.';
COMMENT ON TABLE measure_snapshot IS 'The value of one measure for a business date, product and dimension value.';
COMMENT ON TABLE measure_definition IS 'The agreed definition of a reported measure, by version.';
COMMENT ON TABLE outbox_delivery IS 'The delivery of one outbox event to one consumer, with its retries.';
COMMENT ON TABLE outbox_event IS 'An application event or outbound work request written in the same transaction as the change.';
COMMENT ON TABLE idempotency_key IS 'The stored response of an API request sent with an Idempotency-Key header, kept 24 hours.';
COMMENT ON TABLE processed_event IS 'An event or work key a consumer has already processed, so a repeat is ignored and counted.';
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
COMMENT ON COLUMN measure_definition.id IS 'Record identifier of the measure definition';
COMMENT ON COLUMN measure_definition.measure_code IS 'Measure code';
COMMENT ON COLUMN measure_definition.name IS 'Measure name';
COMMENT ON COLUMN measure_definition.formula IS 'Formula in plain terms';
COMMENT ON COLUMN measure_definition.data_product IS 'Data product the measure reads';
COMMENT ON COLUMN measure_definition.unit IS 'Count, baht, days or percent';
COMMENT ON COLUMN measure_definition.definition_version IS 'Definition version, for example MD-2026.11';
COMMENT ON COLUMN measure_definition.approved_by IS 'Tribe lead who approved';
COMMENT ON COLUMN measure_definition.approved_at IS 'Approval time';
COMMENT ON COLUMN measure_definition.valid_from IS 'Date the definition comes into force';
COMMENT ON COLUMN measure_snapshot.id IS 'Record identifier of the measure snapshot';
COMMENT ON COLUMN measure_snapshot.measure_code IS 'Measure, from measure_definition';
COMMENT ON COLUMN measure_snapshot.definition_version IS 'Definition version used';
COMMENT ON COLUMN measure_snapshot.business_date IS 'Business date measured';
COMMENT ON COLUMN measure_snapshot.product_group IS 'Product group';
COMMENT ON COLUMN measure_snapshot.dimension_code IS 'Dimension: route, age band, queue, stage or agent';
COMMENT ON COLUMN measure_snapshot.dimension_value IS 'Value of the dimension';
COMMENT ON COLUMN measure_snapshot.value IS 'Measure value';
COMMENT ON COLUMN measure_snapshot.case_count IS 'Cases behind the value';
COMMENT ON COLUMN measure_snapshot.is_baseline IS 'True for a row of the baseline date';
COMMENT ON COLUMN measure_snapshot.frozen IS 'True when the row may not change';
COMMENT ON COLUMN measure_snapshot.published_at IS 'When published';
COMMENT ON COLUMN measure_publish.id IS 'Record identifier of the measure publish';
COMMENT ON COLUMN measure_publish.business_date IS 'Business date';
COMMENT ON COLUMN measure_publish.status IS 'Published or held';
COMMENT ON COLUMN measure_publish.case_list_count IS 'Open cases on the case list at the cut-off';
COMMENT ON COLUMN measure_publish.dashboard_count IS 'Open cases in the dashboard facts';
COMMENT ON COLUMN measure_publish.held_reason IS 'Why the publish is held';

-- ---------------------------------------------------------------------------
-- Cross-service references cut from this file (no database foreign key)
-- ---------------------------------------------------------------------------
-- outbox_event.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- outbox_delivery.task_id -> rwb_case.task.id (owner P3); the column stays uuid and integrity is through the owner's contract.

-- ---------------------------------------------------------------------------
-- Migration provenance columns (RD-P1-027; 27 November 2026). Added once per table by the owner's own Flyway step;
-- null for rows created live. LOV-MIGRATION-SOURCE values are Pending, owner data owner (GAP-3275).
-- ---------------------------------------------------------------------------
ALTER TABLE measure_snapshot ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN measure_snapshot.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN measure_snapshot.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
