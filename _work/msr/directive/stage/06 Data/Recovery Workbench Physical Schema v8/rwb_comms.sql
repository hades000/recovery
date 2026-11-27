-- SCB Collections and Recovery. Henka Group, 22 November 2026.
-- (C) Siam Commercial Bank and Henka Pte Ltd
-- Recovery Workbench physical schema, PostgreSQL. Service rwb-comms (P6, Communications), wave 1. Version 7.
-- Change log: 7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.
-- Schema rwb_comms; login rwb_comms; REST base /api/recovery/comms/v1; topic rwb.comms.events.v1; queue rwb-comms.
-- Source: 06 Data/Recovery Workbench Physical Schema v6.sql (read only). Table, index, comment and seed text is copied unchanged; only the schema and the foreign keys change.
-- Tables in this file: 3. Owned by this service in the Ownership Map v1: 3. Platform library objects created here as well: 4.
-- Owner for every object comes from Recovery Workbench Microservice Ownership Map v1 (D-RCV-60).
-- Cross-owner references: a foreign key whose two tables have different owners in the Ownership Map is cut to a plain uuid column; integrity is through the owner's API contract (see README.md).

CREATE SCHEMA IF NOT EXISTS rwb_comms;
SET search_path TO rwb_comms;
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

-- Notice: A demand, recall or statutory notice and its proof of delivery.
CREATE TABLE notice (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,  -- cross-service reference: rwb_case.recovery_case(id); integrity through the owner's contract
    document_id uuid,  -- cross-service reference: rwb_document.document(id); integrity through the owner's contract
    notice_type varchar(25) NOT NULL,
    sent_date date,
    barcode varchar(40),
    callback_date date,
    delivery_status varchar(15),
    sent_type varchar(10),
    person_key varchar(255),
    template_id uuid,
    hold_reason varchar(30),
    dispatch_file_id uuid,  -- cross-service reference: rwb_integration.outbound_item(id); integrity through the owner's contract
    dispatch_attempts integer NOT NULL DEFAULT 0,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Template: A letter or notice template.
CREATE TABLE template (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    template_code varchar(30) NOT NULL,
    template_version integer NOT NULL DEFAULT 1,
    language varchar(2) NOT NULL DEFAULT 'TH',
    product_group varchar(15),
    body_ref varchar(400) NOT NULL,
    approved_by_legal boolean NOT NULL DEFAULT false,
    approved_by uuid,
    approved_at timestamptz,
    valid_from date,
    channel varchar(15),
    notice_type varchar(25),
    signature_basis varchar(20),
    merge_codes jsonb,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_template UNIQUE (template_code, template_version)
);

-- Merge field: A merge code a template may use and the field that supplies its value, by catalog version.
CREATE TABLE merge_field (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    merge_code varchar(40) NOT NULL,
    source_entity varchar(60) NOT NULL,
    source_field varchar(60) NOT NULL,
    field_id varchar(16) NOT NULL,
    is_required boolean NOT NULL DEFAULT false,
    personal_data boolean NOT NULL DEFAULT false,
    catalog_version varchar(20) NOT NULL,
    valid_from date NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_merge_field UNIQUE (merge_code, catalog_version)
);

-- ---------------------------------------------------------------------------
-- Foreign keys kept inside this service (same owner).
-- ---------------------------------------------------------------------------

ALTER TABLE notice ADD CONSTRAINT fk_notice_template_id FOREIGN KEY (template_id) REFERENCES template (id) ON DELETE RESTRICT;
ALTER TABLE processed_event ADD CONSTRAINT fk_processed_event_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;
ALTER TABLE outbox_delivery ADD CONSTRAINT fk_outbox_delivery_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------

CREATE INDEX ix_notice_case_id ON notice (case_id);
CREATE INDEX ix_notice_document_id ON notice (document_id);
CREATE INDEX ix_notice_person_key ON notice (person_key);
CREATE INDEX ix_notice_template_id ON notice (template_id);
CREATE INDEX ix_notice_dispatch_file_id ON notice (dispatch_file_id);
CREATE INDEX ix_processed_event_event_id ON processed_event (event_id);
CREATE INDEX ix_outbox_event_case_id ON outbox_event (case_id);
CREATE INDEX ix_outbox_delivery_event_id ON outbox_delivery (event_id);
CREATE INDEX ix_outbox_delivery_task_id ON outbox_delivery (task_id);

-- ---------------------------------------------------------------------------
-- Data dictionary comments
-- ---------------------------------------------------------------------------

COMMENT ON TABLE merge_field IS 'A merge code a template may use and the field that supplies its value, by catalog version.';
COMMENT ON TABLE outbox_delivery IS 'The delivery of one outbox event to one consumer, with its retries.';
COMMENT ON TABLE outbox_event IS 'An application event or outbound work request written in the same transaction as the change.';
COMMENT ON TABLE idempotency_key IS 'The stored response of an API request sent with an Idempotency-Key header, kept 24 hours.';
COMMENT ON TABLE processed_event IS 'An event or work key a consumer has already processed, so a repeat is ignored and counted.';
COMMENT ON TABLE template IS 'A letter or notice template.';
COMMENT ON TABLE notice IS 'A demand, recall or statutory notice and its proof of delivery.';
COMMENT ON COLUMN notice.id IS 'Record identifier of the notice';
COMMENT ON COLUMN notice.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN notice.document_id IS 'The generated notice';
COMMENT ON COLUMN notice.notice_type IS 'Demand, recall, statutory sale notice, guarantor notice';
COMMENT ON COLUMN notice.sent_date IS 'Date sent';
COMMENT ON COLUMN notice.barcode IS 'Registered mail barcode';
COMMENT ON COLUMN notice.callback_date IS 'Date the proof of delivery came back';
COMMENT ON COLUMN notice.delivery_status IS 'Delivered, refused, undeliverable, pending';
COMMENT ON COLUMN notice.sent_type IS 'Before NPL or NPL';
COMMENT ON COLUMN notice.person_key IS 'Party the notice is addressed to';
COMMENT ON COLUMN notice.template_id IS 'Template version the notice was generated from';
COMMENT ON COLUMN notice.hold_reason IS 'Why the notice is held: missing merge field, TEMPLATE_WITHDRAWN, CONTACT_STOP_Xn, LEGAL_HOLD';
COMMENT ON COLUMN notice.dispatch_file_id IS 'WIN file the notice was last written to';
COMMENT ON COLUMN notice.dispatch_attempts IS 'Number of WIN files the notice has been sent in without acknowledgment';
COMMENT ON COLUMN template.id IS 'Record identifier of the template';
COMMENT ON COLUMN template.template_code IS 'Template code';
COMMENT ON COLUMN template.template_version IS 'Version; unique with template_code, since a template holds several versions';
COMMENT ON COLUMN template.language IS 'Thai or English';
COMMENT ON COLUMN template.product_group IS 'Product group it applies to';
COMMENT ON COLUMN template.body_ref IS 'Stored template body';
COMMENT ON COLUMN template.approved_by_legal IS 'True once Legal approves the wording';
COMMENT ON COLUMN template.approved_by IS 'Legal counsel who approved the version';
COMMENT ON COLUMN template.approved_at IS 'When the version was approved';
COMMENT ON COLUMN template.valid_from IS 'Date from which the approved version is current';
COMMENT ON COLUMN template.channel IS 'Channel the template is for: letter, SMS or LINE';
COMMENT ON COLUMN template.notice_type IS 'Notice type for a notice template; empty for other documents';
COMMENT ON COLUMN template.signature_basis IS 'How Legal allows the document to be signed';
COMMENT ON COLUMN template.merge_codes IS 'The merge codes the template body uses';
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
COMMENT ON COLUMN merge_field.id IS 'Record identifier of the merge field';
COMMENT ON COLUMN merge_field.merge_code IS 'Code written in the template body, for example CASE_NO';
COMMENT ON COLUMN merge_field.source_entity IS 'Entity that holds the value';
COMMENT ON COLUMN merge_field.source_field IS 'Field that holds the value';
COMMENT ON COLUMN merge_field.field_id IS 'BR Field ID of the source field in the data dictionary';
COMMENT ON COLUMN merge_field.is_required IS 'True when generation holds on an empty value';
COMMENT ON COLUMN merge_field.personal_data IS 'True when the value is personal data, detokenized only at generation';
COMMENT ON COLUMN merge_field.catalog_version IS 'Version of the catalog load';
COMMENT ON COLUMN merge_field.valid_from IS 'Date the catalog version comes into force';

-- ---------------------------------------------------------------------------
-- Cross-service references cut from this file (no database foreign key)
-- ---------------------------------------------------------------------------
-- notice.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- notice.document_id -> rwb_document.document.id (owner P5); the column stays uuid and integrity is through the owner's contract.
-- notice.dispatch_file_id -> rwb_integration.outbound_item.id (owner P2); the column stays uuid and integrity is through the owner's contract.
-- outbox_event.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- outbox_delivery.task_id -> rwb_case.task.id (owner P3); the column stays uuid and integrity is through the owner's contract.
