-- SCB Collections and Recovery. Henka Group, 22 November 2026.
-- (C) Siam Commercial Bank and Henka Pte Ltd
-- Recovery Workbench physical schema, PostgreSQL. Service rwb-document (P5, Document), wave 1. Version 7.
-- Change log: 7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.
-- Change log: 9, 27 November 2026, D-RCV-60 P1 developer readiness (RD-P1 register); targeted edits.
-- Schema rwb_document; login rwb_document; REST base /api/recovery/document/v1; topic rwb.document.events.v1; queue rwb-document.
-- Source: 06 Data/Recovery Workbench Physical Schema v6.sql (read only). Table, index, comment and seed text is copied unchanged; only the schema and the foreign keys change.
-- Tables in this file: 12. Owned by this service in the Ownership Map v1: 12. Platform library objects created here as well: 4.
-- Owner for every object comes from Recovery Workbench Microservice Ownership Map v1 (D-RCV-60).
-- Cross-owner references: a foreign key whose two tables have different owners in the Ownership Map is cut to a plain uuid column; integrity is through the owner's API contract (see README.md).

CREATE SCHEMA IF NOT EXISTS rwb_document;
SET search_path TO rwb_document;
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

-- Document: A document held against a case.
CREATE TABLE document (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,  -- cross-service reference: rwb_case.recovery_case(id); integrity through the owner's contract
    person_key varchar(255),
    document_type varchar(30) NOT NULL,
    source varchar(12) NOT NULL,
    storage_ref varchar(400) NOT NULL,
    classification_confidence numeric(5,4),
    review_status varchar(12) NOT NULL DEFAULT 'NOT_NEEDED',
    retention_class varchar(10) NOT NULL,
    write_once boolean NOT NULL DEFAULT false,
    doc_version integer NOT NULL DEFAULT 1,
    previous_version_id uuid,
    content_sha256 char(64) NOT NULL,
    captured_at timestamptz,
    capture_latitude numeric(9,6),
    capture_longitude numeric(9,6),
    client_file_id varchar(64),
    capture_kind varchar(12),
    template_id uuid,  -- cross-service reference: rwb_comms.template(id); integrity through the owner's contract
    treatment_id uuid,  -- cross-service reference: rwb_treatment.treatment(id); integrity through the owner's contract
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Document field: A field read from a document.
CREATE TABLE document_field (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id uuid NOT NULL,
    field_name varchar(60) NOT NULL,
    field_value varchar(1000),
    confidence numeric(5,4),
    confirmed_by uuid,
    extracted_value varchar(1000),
    extractor_version varchar(40),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Document custody: Each movement of an original document.
CREATE TABLE document_custody (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id uuid NOT NULL,
    moved_at timestamptz NOT NULL,
    from_location varchar(20) NOT NULL,
    to_location varchar(20) NOT NULL,
    held_by varchar(120) NOT NULL,
    due_back date,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Retention rule: How long rows of a table or a retention class are kept and what happens at the end, by version.
CREATE TABLE retention_rule (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    product_code varchar(25) NOT NULL,
    table_name varchar(60) NOT NULL,
    record_class varchar(20) NOT NULL,
    retention_months integer NOT NULL,
    age_basis_field varchar(60) NOT NULL,
    end_action varchar(12) NOT NULL DEFAULT 'ARCHIVE',
    rule_version varchar(20) NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    approved_by uuid,
    reference_version_id uuid,  -- cross-service reference: rwb_case.reference_version(id); integrity through the owner's contract
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_retention_rule UNIQUE (table_name, record_class, rule_version)
);

-- Document type: A document type, the fields extracted from it and its Legal and NPA sign-off, by version.
CREATE TABLE document_type (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    doc_type_code varchar(30) NOT NULL,
    label_en varchar(120) NOT NULL,
    label_th varchar(120),
    write_once boolean NOT NULL DEFAULT false,
    retention_class varchar(10) NOT NULL,
    field_definitions jsonb NOT NULL,
    legal_signoff_by uuid,
    legal_signoff_date date,
    npa_signoff_by uuid,
    npa_signoff_date date,
    table_version varchar(20) NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    reference_version_id uuid,  -- cross-service reference: rwb_case.reference_version(id); integrity through the owner's contract
    classify_threshold numeric(4,3),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_document_type UNIQUE (doc_type_code, table_version)
);

-- Document checklist item: A document type required or expected for a case stage and route, by checklist version.
CREATE TABLE document_checklist_item (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    stage_code varchar(20) NOT NULL,
    route_code varchar(4),
    document_type varchar(30) NOT NULL,
    required boolean NOT NULL DEFAULT false,
    sort_order integer NOT NULL DEFAULT 0,
    table_version varchar(20) NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    reference_version_id uuid,  -- cross-service reference: rwb_case.reference_version(id); integrity through the owner's contract
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_document_checklist_item UNIQUE (stage_code, route_code, document_type, table_version)
);

-- Case document check: The latest document completeness check of a case against its checklist.
CREATE TABLE case_document_check (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,  -- cross-service reference: rwb_case.recovery_case(id); integrity through the owner's contract
    checklist_version varchar(20),
    required_count integer NOT NULL DEFAULT 0,
    present_count integer NOT NULL DEFAULT 0,
    missing_types jsonb,
    complete boolean,
    checked_at timestamptz NOT NULL,
    last_event_id uuid,  -- cross-service reference: platform-library.outbox_event(id); integrity through the owner's contract
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Document hub parameter: A document hub parameter value, by version.
CREATE TABLE document_hub_parameter (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    param_code varchar(40) NOT NULL,
    param_value varchar(200) NOT NULL,
    unit varchar(20),
    table_version varchar(20) NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    reference_version_id uuid,  -- cross-service reference: rwb_case.reference_version(id); integrity through the owner's contract
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_document_hub_parameter UNIQUE (param_code, table_version)
);

-- Document intake: A file received by the document hub, from scan to OCR, classification, extraction, matching and review.
CREATE TABLE document_intake (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source varchar(12) NOT NULL,
    source_ref varchar(400) NOT NULL,
    channel_code varchar(40),
    file_name varchar(255),
    file_size bigint,
    captured_at timestamptz,
    sender_address varchar(320),
    partner_id uuid,  -- cross-service reference: rwb_partner.partner(id); integrity through the owner's contract
    run_id uuid,
    received_at timestamptz NOT NULL,
    file_sha256 char(64) NOT NULL,
    intake_ref varchar(400) NOT NULL,
    scan_result varchar(10),
    scanned_at timestamptz,
    case_id uuid,  -- cross-service reference: rwb_case.recovery_case(id); integrity through the owner's contract
    document_id uuid,
    ocr_ref varchar(400),
    ocr_status varchar(12) NOT NULL DEFAULT 'PENDING',
    ocr_attempts integer NOT NULL DEFAULT 0,
    page_count integer,
    rescan_pages varchar(200),
    ocr_quality numeric(5,4),
    languages varchar(20),
    ocr_engine_version varchar(40),
    predicted_type varchar(30),
    classification_confidence numeric(5,4),
    type_candidates jsonb,
    classifier_version varchar(40),
    classify_fallback boolean NOT NULL DEFAULT false,
    match_status varchar(12) NOT NULL DEFAULT 'PENDING',
    candidate_case_ids jsonb,
    extracted_fields jsonb,
    extract_status varchar(12),
    extract_attempts integer NOT NULL DEFAULT 0,
    review_reason varchar(20),
    review_outcome varchar(12),
    resolved_by uuid,
    resolved_at timestamptz,
    discard_reason varchar(400),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Document text: The OCR text of one page of an intake item.
CREATE TABLE document_text (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    intake_id uuid NOT NULL,
    document_id uuid,
    page_no integer NOT NULL,
    text_content text NOT NULL,
    quality numeric(5,4),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_document_text UNIQUE (page_no)
);

-- Retention action: What the monthly retention job did with one document.
CREATE TABLE retention_action (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id uuid NOT NULL,
    run_month char(7) NOT NULL,
    action varchar(12) NOT NULL,
    decision_log_id uuid,  -- cross-service reference: rwb_decision.decision_log_entry(id); integrity through the owner's contract
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_retention_action UNIQUE (run_month)
);

-- Signature request: A request for a party to sign a generated document, and its result.
CREATE TABLE signature_request (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,  -- cross-service reference: rwb_case.recovery_case(id); integrity through the owner's contract
    treatment_id uuid,  -- cross-service reference: rwb_treatment.treatment(id); integrity through the owner's contract
    document_id uuid NOT NULL,
    person_key varchar(255),
    method varchar(15) NOT NULL,
    status varchar(15) NOT NULL DEFAULT 'QUEUED',
    sent_at timestamptz,
    signed_at timestamptz,
    signed_document_id uuid,
    expires_at timestamptz,
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

ALTER TABLE document ADD CONSTRAINT fk_document_previous_version_id FOREIGN KEY (previous_version_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE document_field ADD CONSTRAINT fk_document_field_document_id FOREIGN KEY (document_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE document_custody ADD CONSTRAINT fk_document_custody_document_id FOREIGN KEY (document_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE processed_event ADD CONSTRAINT fk_processed_event_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;
ALTER TABLE outbox_delivery ADD CONSTRAINT fk_outbox_delivery_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;
ALTER TABLE document_intake ADD CONSTRAINT fk_document_intake_document_id FOREIGN KEY (document_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE document_text ADD CONSTRAINT fk_document_text_intake_id FOREIGN KEY (intake_id) REFERENCES document_intake (id) ON DELETE RESTRICT;
ALTER TABLE document_text ADD CONSTRAINT fk_document_text_document_id FOREIGN KEY (document_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE retention_action ADD CONSTRAINT fk_retention_action_document_id FOREIGN KEY (document_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE signature_request ADD CONSTRAINT fk_signature_request_document_id FOREIGN KEY (document_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE signature_request ADD CONSTRAINT fk_signature_request_signed_document_id FOREIGN KEY (signed_document_id) REFERENCES document (id) ON DELETE RESTRICT;

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------

CREATE INDEX ix_document_case_id ON document (case_id);
CREATE INDEX ix_document_person_key ON document (person_key);
CREATE INDEX ix_document_previous_version_id ON document (previous_version_id);
CREATE INDEX ix_document_template_id ON document (template_id);
CREATE INDEX ix_document_treatment_id ON document (treatment_id);
CREATE INDEX ix_document_field_document_id ON document_field (document_id);
CREATE INDEX ix_document_custody_document_id ON document_custody (document_id);
CREATE INDEX ix_retention_rule_reference_version_id ON retention_rule (reference_version_id);
CREATE INDEX ix_processed_event_event_id ON processed_event (event_id);
CREATE INDEX ix_outbox_event_case_id ON outbox_event (case_id);
CREATE INDEX ix_outbox_delivery_event_id ON outbox_delivery (event_id);
CREATE INDEX ix_outbox_delivery_task_id ON outbox_delivery (task_id);
CREATE INDEX ix_document_type_reference_version_id ON document_type (reference_version_id);
CREATE INDEX ix_document_checklist_item_reference_version_id ON document_checklist_item (reference_version_id);
CREATE INDEX ix_case_document_check_case_id ON case_document_check (case_id);
CREATE INDEX ix_case_document_check_last_event_id ON case_document_check (last_event_id);
CREATE INDEX ix_document_hub_parameter_reference_version_id ON document_hub_parameter (reference_version_id);
CREATE INDEX ix_document_intake_partner_id ON document_intake (partner_id);
CREATE INDEX ix_document_intake_run_id ON document_intake (run_id);
CREATE INDEX ix_document_intake_case_id ON document_intake (case_id);
CREATE INDEX ix_document_intake_document_id ON document_intake (document_id);
CREATE INDEX ix_document_text_intake_id ON document_text (intake_id);
CREATE INDEX ix_document_text_document_id ON document_text (document_id);
CREATE INDEX ix_retention_action_document_id ON retention_action (document_id);
CREATE INDEX ix_retention_action_decision_log_id ON retention_action (decision_log_id);
CREATE INDEX ix_signature_request_case_id ON signature_request (case_id);
CREATE INDEX ix_signature_request_treatment_id ON signature_request (treatment_id);
CREATE INDEX ix_signature_request_document_id ON signature_request (document_id);
CREATE INDEX ix_signature_request_person_key ON signature_request (person_key);
CREATE INDEX ix_signature_request_signed_document_id ON signature_request (signed_document_id);

-- ---------------------------------------------------------------------------
-- Data dictionary comments
-- ---------------------------------------------------------------------------

COMMENT ON TABLE signature_request IS 'A request for a party to sign a generated document, and its result.';
COMMENT ON TABLE retention_action IS 'What the monthly retention job did with one document.';
COMMENT ON TABLE document_text IS 'The OCR text of one page of an intake item.';
COMMENT ON TABLE document_intake IS 'A file received by the document hub, from scan to OCR, classification, extraction, matching and review.';
COMMENT ON TABLE document_hub_parameter IS 'A document hub parameter value, by version.';
COMMENT ON TABLE case_document_check IS 'The latest document completeness check of a case against its checklist.';
COMMENT ON TABLE document_checklist_item IS 'A document type required or expected for a case stage and route, by checklist version.';
COMMENT ON TABLE document_type IS 'A document type, the fields extracted from it and its Legal and NPA sign-off, by version.';
COMMENT ON TABLE outbox_delivery IS 'The delivery of one outbox event to one consumer, with its retries.';
COMMENT ON TABLE outbox_event IS 'An application event or outbound work request written in the same transaction as the change.';
COMMENT ON TABLE idempotency_key IS 'The stored response of an API request sent with an Idempotency-Key header, kept 24 hours.';
COMMENT ON TABLE processed_event IS 'An event or work key a consumer has already processed, so a repeat is ignored and counted.';
COMMENT ON TABLE retention_rule IS 'How long rows of a table or a retention class are kept and what happens at the end, by version.';
COMMENT ON TABLE document_custody IS 'Each movement of an original document.';
COMMENT ON TABLE document_field IS 'A field read from a document.';
COMMENT ON TABLE document IS 'A document held against a case.';
COMMENT ON COLUMN document.id IS 'Record identifier of the document';
COMMENT ON COLUMN document.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN document.person_key IS 'The party this record belongs to';
COMMENT ON COLUMN document.document_type IS 'Type from the document checklist';
COMMENT ON COLUMN document.source IS 'Scan, upload, generated, partner, email';
COMMENT ON COLUMN document.storage_ref IS 'Reference to the stored file';
COMMENT ON COLUMN document.classification_confidence IS 'OCR classification confidence';
COMMENT ON COLUMN document.review_status IS 'Not needed, pending, confirmed, corrected';
COMMENT ON COLUMN document.retention_class IS 'Retention class';
COMMENT ON COLUMN document.write_once IS 'True for legal documents held write-once';
COMMENT ON COLUMN document.doc_version IS 'Document version';
COMMENT ON COLUMN document.previous_version_id IS 'The document row this version supersedes; empty for version 1';
COMMENT ON COLUMN document.content_sha256 IS 'SHA-256 of the stored file, for the duplicate check and the integrity check';
COMMENT ON COLUMN document.captured_at IS 'Device time when the field app captured the file';
COMMENT ON COLUMN document.capture_latitude IS 'GPS latitude at capture';
COMMENT ON COLUMN document.capture_longitude IS 'GPS longitude at capture';
COMMENT ON COLUMN document.client_file_id IS 'Field app file ID, unique per case, for repeat syncs';
COMMENT ON COLUMN document.capture_kind IS 'Photo, bill or checklist';
COMMENT ON COLUMN document.template_id IS 'Template version a generated document was made from';
COMMENT ON COLUMN document.treatment_id IS 'Treatment a generated document belongs to';
COMMENT ON COLUMN document_field.id IS 'Record identifier of the document field';
COMMENT ON COLUMN document_field.document_id IS 'The document this record belongs to';
COMMENT ON COLUMN document_field.field_name IS 'Field name from the document type';
COMMENT ON COLUMN document_field.field_value IS 'Value read, masked where personal';
COMMENT ON COLUMN document_field.confidence IS 'Extraction confidence';
COMMENT ON COLUMN document_field.confirmed_by IS 'Who confirmed a low confidence value';
COMMENT ON COLUMN document_field.extracted_value IS 'The value as first read by the extractor, kept when a person corrects field_value; masked by role';
COMMENT ON COLUMN document_field.extractor_version IS 'Extraction approach and model version that produced the value';
COMMENT ON COLUMN document_custody.id IS 'Record identifier of the custody movement';
COMMENT ON COLUMN document_custody.document_id IS 'The document this record belongs to';
COMMENT ON COLUMN document_custody.moved_at IS 'When it moved';
COMMENT ON COLUMN document_custody.from_location IS 'Vault, branch, post, lawyer, court, land office';
COMMENT ON COLUMN document_custody.to_location IS 'Where it went';
COMMENT ON COLUMN document_custody.held_by IS 'Person or firm holding it';
COMMENT ON COLUMN document_custody.due_back IS 'When it is due back';
COMMENT ON COLUMN retention_rule.id IS 'Record identifier of the retention rule';
COMMENT ON COLUMN retention_rule.product_code IS 'Data product the rule applies to';
COMMENT ON COLUMN retention_rule.table_name IS 'Table the rule applies to, from sys_objects; never decision_log_entry';
COMMENT ON COLUMN retention_rule.record_class IS 'Retention class from LOV-RETENTION, or LAKE_COPY for the decision log lake copy';
COMMENT ON COLUMN retention_rule.retention_months IS 'Retention period in months, 1 to 600';
COMMENT ON COLUMN retention_rule.age_basis_field IS 'Field the age is measured from, for example interaction.occurred_at';
COMMENT ON COLUMN retention_rule.end_action IS 'Archive or review at the end of the period';
COMMENT ON COLUMN retention_rule.rule_version IS 'Version, for example RET-2026.11';
COMMENT ON COLUMN retention_rule.valid_from IS 'Date the version comes into force';
COMMENT ON COLUMN retention_rule.valid_to IS 'Last date the version is in force';
COMMENT ON COLUMN retention_rule.approved_by IS 'Who approved the version';
COMMENT ON COLUMN retention_rule.reference_version_id IS 'Reference version that brought the row';
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
COMMENT ON COLUMN document_type.id IS 'Record identifier of the document type';
COMMENT ON COLUMN document_type.doc_type_code IS 'Document type code, the value set of LOV-DOC-TYPE';
COMMENT ON COLUMN document_type.label_en IS 'English label';
COMMENT ON COLUMN document_type.label_th IS 'Thai label';
COMMENT ON COLUMN document_type.write_once IS 'True for a legal type held in the write-once container';
COMMENT ON COLUMN document_type.retention_class IS 'Retention class of the type';
COMMENT ON COLUMN document_type.field_definitions IS 'Fields extracted from the type: name, label, data type, personal flag, required flag, extraction method (TEMPLATE or MODEL), review only flag and optional pattern';
COMMENT ON COLUMN document_type.legal_signoff_by IS 'Legal counsel user who signed the type and its fields';
COMMENT ON COLUMN document_type.legal_signoff_date IS 'Date of the Legal sign-off';
COMMENT ON COLUMN document_type.npa_signoff_by IS 'Head of NPA user who signed the type and its fields';
COMMENT ON COLUMN document_type.npa_signoff_date IS 'Date of the NPA sign-off';
COMMENT ON COLUMN document_type.table_version IS 'Version of the type table, for example DOCTYPE-2026.11';
COMMENT ON COLUMN document_type.valid_from IS 'Date the version comes into force';
COMMENT ON COLUMN document_type.valid_to IS 'Last date the version is in force';
COMMENT ON COLUMN document_type.reference_version_id IS 'Reference version that brought the row';
COMMENT ON COLUMN document_type.classify_threshold IS 'Confidence below which a document of this type goes to the review queue';
COMMENT ON COLUMN document_checklist_item.id IS 'Record identifier of the checklist item';
COMMENT ON COLUMN document_checklist_item.stage_code IS 'Case stage the row applies to';
COMMENT ON COLUMN document_checklist_item.route_code IS 'Route the row applies to; empty for every route';
COMMENT ON COLUMN document_checklist_item.document_type IS 'Document type';
COMMENT ON COLUMN document_checklist_item.required IS 'True when the type is required for the stage and route';
COMMENT ON COLUMN document_checklist_item.sort_order IS 'Order of the item on the checklist';
COMMENT ON COLUMN document_checklist_item.table_version IS 'Version of the checklist, for example CHK-2026.11';
COMMENT ON COLUMN document_checklist_item.valid_from IS 'Date the version comes into force';
COMMENT ON COLUMN document_checklist_item.valid_to IS 'Last date the version is in force';
COMMENT ON COLUMN document_checklist_item.reference_version_id IS 'Reference version that brought the row';
COMMENT ON COLUMN case_document_check.id IS 'Record identifier of the completeness check';
COMMENT ON COLUMN case_document_check.case_id IS 'Case checked; one row per case; unique';
COMMENT ON COLUMN case_document_check.checklist_version IS 'Checklist version used';
COMMENT ON COLUMN case_document_check.required_count IS 'Number of required types';
COMMENT ON COLUMN case_document_check.present_count IS 'Number of required types present';
COMMENT ON COLUMN case_document_check.missing_types IS 'Required types not present';
COMMENT ON COLUMN case_document_check.complete IS 'True when every required type is present; empty when the stage has no checklist';
COMMENT ON COLUMN case_document_check.checked_at IS 'When the check last ran';
COMMENT ON COLUMN case_document_check.last_event_id IS 'Event that triggered the last check, for repeat detection';
COMMENT ON COLUMN document_hub_parameter.id IS 'Record identifier of the document hub parameter';
COMMENT ON COLUMN document_hub_parameter.param_code IS 'Parameter code, for example INTAKE_MAX_FILE_MB, OCR_MIN_QUALITY, CLASSIFY_THRESHOLD, CASE_NO_PATTERN, SEARCH_MAX_RESULTS';
COMMENT ON COLUMN document_hub_parameter.param_value IS 'Parameter value as text, typed by the reader';
COMMENT ON COLUMN document_hub_parameter.unit IS 'Unit of the value, for example MB, seconds, ratio';
COMMENT ON COLUMN document_hub_parameter.table_version IS 'Version of the parameter load';
COMMENT ON COLUMN document_hub_parameter.valid_from IS 'Date the value comes into force';
COMMENT ON COLUMN document_hub_parameter.valid_to IS 'Last date the value is in force';
COMMENT ON COLUMN document_hub_parameter.reference_version_id IS 'Reference version that brought the row';
COMMENT ON COLUMN document_intake.id IS 'Record identifier of the intake item';
COMMENT ON COLUMN document_intake.source IS 'Source of the file';
COMMENT ON COLUMN document_intake.source_ref IS 'Path, partner reference or email message ID at the channel';
COMMENT ON COLUMN document_intake.channel_code IS 'Branch code, MAILROOM, partner code or mailbox code';
COMMENT ON COLUMN document_intake.file_name IS 'File name as received; personal where it names a customer';
COMMENT ON COLUMN document_intake.file_size IS 'File size in bytes';
COMMENT ON COLUMN document_intake.captured_at IS 'Scan time recorded by the scanner, for scanner files';
COMMENT ON COLUMN document_intake.sender_address IS 'Sender email address for mailbox items; masked by role';
COMMENT ON COLUMN document_intake.partner_id IS 'Partner that sent the file by SFTP';
COMMENT ON COLUMN document_intake.run_id IS 'JOB-12 run that took the item in';
COMMENT ON COLUMN document_intake.received_at IS 'When the Workbench received the file';
COMMENT ON COLUMN document_intake.file_sha256 IS 'SHA-256 of the file';
COMMENT ON COLUMN document_intake.intake_ref IS 'Received file in the intake container';
COMMENT ON COLUMN document_intake.scan_result IS 'Malware scan result: clean or infected; empty until scanned';
COMMENT ON COLUMN document_intake.scanned_at IS 'When the malware scan ran';
COMMENT ON COLUMN document_intake.case_id IS 'Case the item belongs to once known';
COMMENT ON COLUMN document_intake.document_id IS 'Document created from the item, or the uploaded document';
COMMENT ON COLUMN document_intake.ocr_ref IS 'OCR JSON output (text and layout) in the standard container';
COMMENT ON COLUMN document_intake.ocr_status IS 'Pending, done, rescan or failed';
COMMENT ON COLUMN document_intake.ocr_attempts IS 'Number of OCR calls made for the item';
COMMENT ON COLUMN document_intake.page_count IS 'Number of pages read';
COMMENT ON COLUMN document_intake.rescan_pages IS 'Page numbers below the OCR quality threshold';
COMMENT ON COLUMN document_intake.ocr_quality IS 'Lowest page quality of the item';
COMMENT ON COLUMN document_intake.languages IS 'Languages found, for example th,en';
COMMENT ON COLUMN document_intake.ocr_engine_version IS 'Version of the OCR service that read the item';
COMMENT ON COLUMN document_intake.predicted_type IS 'Type with the highest classification score';
COMMENT ON COLUMN document_intake.classification_confidence IS 'Score of the predicted type';
COMMENT ON COLUMN document_intake.type_candidates IS 'Top two types with their scores';
COMMENT ON COLUMN document_intake.classifier_version IS 'Model version that classified the item';
COMMENT ON COLUMN document_intake.classify_fallback IS 'True when the classifier did not answer and the item went to a person';
COMMENT ON COLUMN document_intake.match_status IS 'Pending, matched, no match, multiple, conflict, case closed or no type';
COMMENT ON COLUMN document_intake.candidate_case_ids IS 'Cases found for the item when more than one or none can be chosen by rule';
COMMENT ON COLUMN document_intake.extracted_fields IS 'Fields read before the item is attached: field name, value, extracted value, confidence, state, extractor version, personal flag';
COMMENT ON COLUMN document_intake.extract_status IS 'Pending, done or failed';
COMMENT ON COLUMN document_intake.extract_attempts IS 'Number of extraction attempts';
COMMENT ON COLUMN document_intake.review_reason IS 'Why the item needs a person: rescan, unreadable file, low confidence, model unavailable, unknown type';
COMMENT ON COLUMN document_intake.review_outcome IS 'Attached or discarded once a person resolves the review item';
COMMENT ON COLUMN document_intake.resolved_by IS 'Who resolved the review item';
COMMENT ON COLUMN document_intake.resolved_at IS 'When the review item was resolved';
COMMENT ON COLUMN document_intake.discard_reason IS 'Reason given when a review item is discarded';
COMMENT ON COLUMN document_text.id IS 'Record identifier of the page text';
COMMENT ON COLUMN document_text.intake_id IS 'Intake item the page belongs to; unique with page_no';
COMMENT ON COLUMN document_text.document_id IS 'Document the page belongs to once attached';
COMMENT ON COLUMN document_text.page_no IS 'Page number';
COMMENT ON COLUMN document_text.text_content IS 'OCR text of the page; masked by role on read';
COMMENT ON COLUMN document_text.quality IS 'Mean word confidence of the page';
COMMENT ON COLUMN retention_action.id IS 'Record identifier of the retention action';
COMMENT ON COLUMN retention_action.document_id IS 'Document acted on; unique with run_month';
COMMENT ON COLUMN retention_action.run_month IS 'Month of the JOB-17 run, YYYY-MM';
COMMENT ON COLUMN retention_action.action IS 'Archived, listed, held or exception';
COMMENT ON COLUMN retention_action.decision_log_id IS 'DOCRET decision log entry for an archive';
COMMENT ON COLUMN signature_request.id IS 'Record identifier of the signature request';
COMMENT ON COLUMN signature_request.case_id IS 'Case';
COMMENT ON COLUMN signature_request.treatment_id IS 'Treatment the agreement belongs to';
COMMENT ON COLUMN signature_request.document_id IS 'Generated document sent for signature';
COMMENT ON COLUMN signature_request.person_key IS 'Signing party';
COMMENT ON COLUMN signature_request.method IS 'E-signature, branch or paper';
COMMENT ON COLUMN signature_request.status IS 'Queued, sent, signed, declined or expired';
COMMENT ON COLUMN signature_request.sent_at IS 'When the request was sent';
COMMENT ON COLUMN signature_request.signed_at IS 'When the party signed';
COMMENT ON COLUMN signature_request.signed_document_id IS 'Signed copy or branch scan';
COMMENT ON COLUMN signature_request.expires_at IS 'End of the offer validity';

-- ---------------------------------------------------------------------------
-- Cross-service references cut from this file (no database foreign key)
-- ---------------------------------------------------------------------------
-- document.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- document.template_id -> rwb_comms.template.id (owner P6); the column stays uuid and integrity is through the owner's contract.
-- document.treatment_id -> rwb_treatment.treatment.id (owner S2); the column stays uuid and integrity is through the owner's contract.
-- retention_rule.reference_version_id -> rwb_case.reference_version.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- outbox_event.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- outbox_delivery.task_id -> rwb_case.task.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- document_type.reference_version_id -> rwb_case.reference_version.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- document_checklist_item.reference_version_id -> rwb_case.reference_version.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- case_document_check.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- case_document_check.last_event_id -> platform-library.outbox_event.id (owner PLT); the column stays uuid and integrity is through the owner's contract.
-- document_hub_parameter.reference_version_id -> rwb_case.reference_version.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- document_intake.partner_id -> rwb_partner.partner.id (owner S9); the column stays uuid and integrity is through the owner's contract.
-- document_intake.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- retention_action.decision_log_id -> rwb_decision.decision_log_entry.id (owner P7); the column stays uuid and integrity is through the owner's contract.
-- signature_request.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- signature_request.treatment_id -> rwb_treatment.treatment.id (owner S2); the column stays uuid and integrity is through the owner's contract.

-- ---------------------------------------------------------------------------
-- Migration provenance columns (RD-P1-027; 27 November 2026). Added once per table by the owner's own Flyway step;
-- null for rows created live. LOV-MIGRATION-SOURCE values are Pending, owner data owner (GAP-3275).
-- ---------------------------------------------------------------------------
ALTER TABLE document ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN document.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN document.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE document_field ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN document_field.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN document_field.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE document_custody ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN document_custody.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN document_custody.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE document_type ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN document_type.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN document_type.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE retention_rule ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN retention_rule.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN retention_rule.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
