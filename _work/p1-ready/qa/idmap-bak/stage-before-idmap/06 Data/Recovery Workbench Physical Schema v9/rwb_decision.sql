-- SCB Collections and Recovery. Henka Group, 22 November 2026.
-- (C) Siam Commercial Bank and Henka Pte Ltd
-- Recovery Workbench physical schema, PostgreSQL. Service rwb-decision (P7, Decision and rules), wave 1. Version 7.
-- Change log: 7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.
-- Change log: 9, 27 November 2026, D-RCV-60 P1 developer readiness (RD-P1 register); targeted edits.
-- Schema rwb_decision; login rwb_decision; REST base /api/recovery/decision/v1; topic rwb.decision.events.v1; queue rwb-decision.
-- Source: 06 Data/Recovery Workbench Physical Schema v6.sql (read only). Table, index, comment and seed text is copied unchanged; only the schema and the foreign keys change.
-- Tables in this file: 6. Owned by this service in the Ownership Map v1: 6. Platform library objects created here as well: 4.
-- Owner for every object comes from Recovery Workbench Microservice Ownership Map v1 (D-RCV-60).
-- Cross-owner references: a foreign key whose two tables have different owners in the Ownership Map is cut to a plain uuid column; integrity is through the owner's API contract (see README.md).

CREATE SCHEMA IF NOT EXISTS rwb_decision;
SET search_path TO rwb_decision;
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

-- Decision log entry: One record per decision. Append only and hash chained.
CREATE TABLE decision_log_entry (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid,  -- cross-service reference: rwb_case.recovery_case(id); integrity through the owner's contract
    decision_code varchar(8) NOT NULL,
    rule_id varchar(20),
    rule_version varchar(20),
    model_version varchar(40),
    agent_version varchar(40),
    inputs_ref varchar(400) NOT NULL,
    recommendation jsonb,
    approver_user_id uuid,
    approval_level varchar(4),
    final_call varchar(40) NOT NULL,
    override_reason varchar(1000),
    actions jsonb,
    outcome jsonb,
    decided_at timestamptz NOT NULL DEFAULT now(),
    prev_hash char(64) NOT NULL,
    entry_hash char(64) NOT NULL,
    chain_seq bigint NOT NULL,
    corrects_entry_id uuid,
    actor_user_id uuid,
    idempotency_key varchar(80),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_decision_log_entry UNIQUE (entry_hash, chain_seq, idempotency_key),
    CONSTRAINT uk_decision_log_entry_chain_seq UNIQUE (chain_seq),
    CONSTRAINT uk_decision_log_entry_idempotency_key UNIQUE (idempotency_key)
);

-- Rule package: One Drools decision-table package, with its owner and first-match policy.
CREATE TABLE rule_package (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    package_code varchar(30) NOT NULL,
    title varchar(200) NOT NULL,
    owner_role varchar(20) NOT NULL,
    hit_policy varchar(10) NOT NULL DEFAULT 'FIRST',
    CONSTRAINT uk_rule_package UNIQUE (package_code),
    CONSTRAINT ck_rule_package_hit_policy CHECK (hit_policy IN ('FIRST'))
);

-- Rule package version: One uploaded and approved version of a rule package, with its workbook, DRL and checksum.
CREATE TABLE rule_package_version (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    package_id uuid NOT NULL,
    version_label varchar(30) NOT NULL,
    status varchar(20) NOT NULL DEFAULT 'LOADED',
    source_blob_ref varchar(500) NOT NULL,
    drl_source text NOT NULL,
    checksum varchar(64) NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    author uuid NOT NULL,
    approver uuid,
    loaded_at timestamptz NOT NULL DEFAULT now(),
    approved_at timestamptz,
    test_result varchar(20),
    dry_run_counts jsonb,
    rollback_of uuid,
    change_checklist jsonb,
    CONSTRAINT uk_rule_package_version UNIQUE (package_id, version_label),
    CONSTRAINT ck_rule_package_version_status CHECK (status IN ('LOADED', 'APPROVED', 'IN_FORCE', 'SUPERSEDED', 'ROLLED_BACK', 'REFUSED'))
);

-- Rule: One versioned routing rule or sentry.
CREATE TABLE rule_row (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_id varchar(20) NOT NULL,
    rule_version varchar(20) NOT NULL,
    route_set varchar(15) NOT NULL,
    from_state varchar(60) NOT NULL,
    event_code varchar(60) NOT NULL,
    condition_expr varchar(1000),
    action_text varchar(1000) NOT NULL,
    to_state varchar(60) NOT NULL,
    owner_role varchar(20) NOT NULL,
    timer_spec varchar(60),
    valid_from date NOT NULL,
    valid_to date,
    approved_by uuid NOT NULL,
    test_case_id varchar(20) NOT NULL,
    rule_table varchar(15),
    row_order integer,
    target_queue_code varchar(30),
    package_version_id uuid,
    drools_rule_name varchar(60),
    outputs jsonb,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_rule_row UNIQUE (rule_id, rule_version)
);

-- Rule test case: A test case of the rule table test harness, with its expected and actual result.
CREATE TABLE rule_test_case (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    test_case_id varchar(20) NOT NULL,
    route_set varchar(15) NOT NULL,
    rule_version varchar(20) NOT NULL,
    rule_id varchar(20) NOT NULL,
    package_version_id uuid,
    from_state varchar(60) NOT NULL,
    event_code varchar(60) NOT NULL,
    facts jsonb NOT NULL,
    expected_to_state varchar(60) NOT NULL,
    expected_owner_role varchar(20),
    expected_timer_spec varchar(60),
    result varchar(10),
    result_detail varchar(1000),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_rule_test_case UNIQUE (test_case_id, rule_version)
);

-- Approval: An item waiting for approval, routed to the level the delegation of authority requires.
CREATE TABLE approval (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,  -- cross-service reference: rwb_case.recovery_case(id); integrity through the owner's contract
    decision_code varchar(8) NOT NULL,
    regulation_item varchar(10),
    capability_area varchar(30) NOT NULL,
    route_role_code varchar(20),
    approval_level varchar(4),
    delegation_limit_id uuid,  -- cross-service reference: rwb_access.delegation_limit(id); integrity through the owner's contract
    limit_version varchar(20),
    product_group varchar(15) NOT NULL,
    amount numeric(18,2),
    terms jsonb,
    prepared_by uuid NOT NULL,
    assigned_user_id uuid,
    status varchar(20) NOT NULL DEFAULT 'WAITING',
    due_at timestamptz,
    escalation_level integer NOT NULL DEFAULT 0,
    source_type varchar(20) NOT NULL,
    source_ref varchar(60) NOT NULL,
    rule_id varchar(20),
    rule_version varchar(20),
    decision_log_id uuid,
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

ALTER TABLE decision_log_entry ADD CONSTRAINT fk_decision_log_entry_corrects_entry_id FOREIGN KEY (corrects_entry_id) REFERENCES decision_log_entry (id) ON DELETE RESTRICT;
ALTER TABLE processed_event ADD CONSTRAINT fk_processed_event_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;
ALTER TABLE outbox_delivery ADD CONSTRAINT fk_outbox_delivery_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;
ALTER TABLE approval ADD CONSTRAINT fk_approval_decision_log_id FOREIGN KEY (decision_log_id) REFERENCES decision_log_entry (id) ON DELETE RESTRICT;
ALTER TABLE rule_package_version ADD CONSTRAINT fk_rule_package_version_package_id FOREIGN KEY (package_id) REFERENCES rule_package (id) ON DELETE RESTRICT;
ALTER TABLE rule_package_version ADD CONSTRAINT fk_rule_package_version_rollback_of FOREIGN KEY (rollback_of) REFERENCES rule_package_version (id) ON DELETE RESTRICT;
ALTER TABLE rule_row ADD CONSTRAINT fk_rule_row_package_version_id FOREIGN KEY (package_version_id) REFERENCES rule_package_version (id) ON DELETE RESTRICT;
ALTER TABLE rule_test_case ADD CONSTRAINT fk_rule_test_case_package_version_id FOREIGN KEY (package_version_id) REFERENCES rule_package_version (id) ON DELETE RESTRICT;

-- ---------------------------------------------------------------------------
-- Append-only guard (trigger) from the source
-- ---------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION refuse_change() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION '% is append only: % refused', TG_TABLE_NAME, TG_OP;
END;
$$;

CREATE TRIGGER tr_declog_append_only BEFORE UPDATE OR DELETE ON decision_log_entry FOR EACH ROW EXECUTE FUNCTION refuse_change();

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------

CREATE INDEX ix_decision_log_entry_case_id ON decision_log_entry (case_id);
CREATE INDEX ix_decision_log_entry_corrects_entry_id ON decision_log_entry (corrects_entry_id);
CREATE INDEX ix_processed_event_event_id ON processed_event (event_id);
CREATE INDEX ix_outbox_event_case_id ON outbox_event (case_id);
CREATE INDEX ix_outbox_delivery_event_id ON outbox_delivery (event_id);
CREATE INDEX ix_outbox_delivery_task_id ON outbox_delivery (task_id);
CREATE INDEX ix_approval_case_id ON approval (case_id);
CREATE INDEX ix_approval_delegation_limit_id ON approval (delegation_limit_id);
CREATE INDEX ix_approval_decision_log_id ON approval (decision_log_id);
CREATE INDEX ix_declog_case_time ON decision_log_entry (case_id, decided_at);
CREATE INDEX ix_rule_lookup ON rule_row (route_set, from_state, event_code) WHERE is_active;
CREATE INDEX ix_rule_package_version_lookup ON rule_package_version (package_id, status, valid_from);
CREATE INDEX ix_rule_row_package_version_id ON rule_row (package_version_id);
CREATE INDEX ix_rule_test_case_package_version_id ON rule_test_case (package_version_id);

-- ---------------------------------------------------------------------------
-- Data dictionary comments
-- ---------------------------------------------------------------------------

COMMENT ON TABLE rule_package_version IS 'One uploaded and approved version of a rule package, with its workbook, DRL and checksum.';
COMMENT ON TABLE rule_package IS 'One Drools decision-table package, with its owner and first-match policy.';
COMMENT ON TABLE approval IS 'An item waiting for approval, routed to the level the delegation of authority requires.';
COMMENT ON TABLE rule_test_case IS 'A test case of the rule table test harness, with its expected and actual result.';
COMMENT ON TABLE outbox_delivery IS 'The delivery of one outbox event to one consumer, with its retries.';
COMMENT ON TABLE outbox_event IS 'An application event or outbound work request written in the same transaction as the change.';
COMMENT ON TABLE idempotency_key IS 'The stored response of an API request sent with an Idempotency-Key header, kept 24 hours.';
COMMENT ON TABLE processed_event IS 'An event or work key a consumer has already processed, so a repeat is ignored and counted.';
COMMENT ON TABLE rule_row IS 'One versioned routing rule or sentry.';
COMMENT ON TABLE decision_log_entry IS 'One record per decision. Append only and hash chained.';
COMMENT ON COLUMN decision_log_entry.id IS 'Record identifier of the decision log entry';
COMMENT ON COLUMN decision_log_entry.case_id IS 'The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case';
COMMENT ON COLUMN decision_log_entry.decision_code IS 'D5.1 to D9.3, X1 to X7, or an access event';
COMMENT ON COLUMN decision_log_entry.rule_id IS 'Rule that fired';
COMMENT ON COLUMN decision_log_entry.rule_version IS 'Rule version';
COMMENT ON COLUMN decision_log_entry.model_version IS 'Model version used';
COMMENT ON COLUMN decision_log_entry.agent_version IS 'Agent and prompt version used';
COMMENT ON COLUMN decision_log_entry.inputs_ref IS 'Reference to the inputs snapshot, with the freshness of each input';
COMMENT ON COLUMN decision_log_entry.recommendation IS 'Option, reasons, confidence and alternatives';
COMMENT ON COLUMN decision_log_entry.approver_user_id IS 'Who approved';
COMMENT ON COLUMN decision_log_entry.approval_level IS 'Approval level applied';
COMMENT ON COLUMN decision_log_entry.final_call IS 'The option decided';
COMMENT ON COLUMN decision_log_entry.override_reason IS 'Reason when the person did not follow the recommendation';
COMMENT ON COLUMN decision_log_entry.actions IS 'Target system, result and timestamps of each action';
COMMENT ON COLUMN decision_log_entry.outcome IS 'Cash, cure, loss and time, written when known';
COMMENT ON COLUMN decision_log_entry.decided_at IS 'When decided';
COMMENT ON COLUMN decision_log_entry.prev_hash IS 'Hash of the previous entry';
COMMENT ON COLUMN decision_log_entry.entry_hash IS 'Hash of this entry';
COMMENT ON COLUMN decision_log_entry.chain_seq IS 'Position of the entry in the hash chain; prev_hash is the entry_hash of chain_seq minus 1; unique on its own';
COMMENT ON COLUMN decision_log_entry.corrects_entry_id IS 'The entry this entry corrects';
COMMENT ON COLUMN decision_log_entry.actor_user_id IS 'The person or service identity whose action, preparation or access the entry records';
COMMENT ON COLUMN decision_log_entry.idempotency_key IS 'Event ID of the calling module; a repeat returns the first entry; unique on its own';
COMMENT ON COLUMN rule_package.id IS 'DF-REF-274. Record identifier of the rule package';
COMMENT ON COLUMN rule_package.package_code IS 'DF-REF-275. Package code: ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER, RESTRUCTURE, PAYMENT_MATCH or BOOKING_MATCH';
COMMENT ON COLUMN rule_package.title IS 'DF-REF-276. Package title shown to the rule author';
COMMENT ON COLUMN rule_package.owner_role IS 'DF-REF-277. Role that owns the package, RW-COE';
COMMENT ON COLUMN rule_package.hit_policy IS 'DF-REF-278. Hit policy, FIRST: exactly one row decides';
COMMENT ON COLUMN rule_package_version.id IS 'DF-REF-279. Record identifier of the rule package version';
COMMENT ON COLUMN rule_package_version.package_id IS 'DF-REF-280. The rule_package this version belongs to';
COMMENT ON COLUMN rule_package_version.version_label IS 'DF-REF-281. Version label, for example ALLOC-2026.12';
COMMENT ON COLUMN rule_package_version.status IS 'DF-REF-282. LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK or REFUSED';
COMMENT ON COLUMN rule_package_version.source_blob_ref IS 'DF-REF-283. Blob path of the uploaded XLS workbook';
COMMENT ON COLUMN rule_package_version.drl_source IS 'DF-REF-284. DRL generated from the workbook, compiled to a KieBase';
COMMENT ON COLUMN rule_package_version.checksum IS 'DF-REF-285. SHA-256 of the workbook and the generated DRL';
COMMENT ON COLUMN rule_package_version.valid_from IS 'DF-REF-286. Date the version comes into force';
COMMENT ON COLUMN rule_package_version.valid_to IS 'DF-REF-287. Last date the version is in force';
COMMENT ON COLUMN rule_package_version.author IS 'DF-REF-288. Who loaded the version; never the approver';
COMMENT ON COLUMN rule_package_version.approver IS 'DF-REF-289. RW-RISK approver of the version';
COMMENT ON COLUMN rule_package_version.loaded_at IS 'DF-REF-290. When the version was loaded';
COMMENT ON COLUMN rule_package_version.approved_at IS 'DF-REF-291. When the version was approved';
COMMENT ON COLUMN rule_package_version.test_result IS 'DF-REF-292. PASSED or FAILED from the scenario and dry run checks';
COMMENT ON COLUMN rule_package_version.dry_run_counts IS 'DF-REF-293. Counts of open cases each changed row would move, from the dry run';
COMMENT ON COLUMN rule_package_version.rollback_of IS 'DF-REF-294. The version this one rolls back to';
COMMENT ON COLUMN rule_package_version.change_checklist IS 'DF-REF-295. Request, impact, test result, approver, load, verify and rollback plan';
COMMENT ON COLUMN rule_row.id IS 'Record identifier of the rule row';
COMMENT ON COLUMN rule_row.rule_id IS 'Rule ID, for example R-LIT-12';
COMMENT ON COLUMN rule_row.rule_version IS 'Version';
COMMENT ON COLUMN rule_row.route_set IS 'Route set';
COMMENT ON COLUMN rule_row.from_state IS 'From state';
COMMENT ON COLUMN rule_row.event_code IS 'Event';
COMMENT ON COLUMN rule_row.condition_expr IS 'Condition';
COMMENT ON COLUMN rule_row.action_text IS 'Action';
COMMENT ON COLUMN rule_row.to_state IS 'To state';
COMMENT ON COLUMN rule_row.owner_role IS 'Owner of the next state';
COMMENT ON COLUMN rule_row.timer_spec IS 'Timer';
COMMENT ON COLUMN rule_row.valid_from IS 'Valid from';
COMMENT ON COLUMN rule_row.valid_to IS 'Valid to';
COMMENT ON COLUMN rule_row.approved_by IS 'Who approved the version';
COMMENT ON COLUMN rule_row.test_case_id IS 'Test case that proves the rule';
COMMENT ON COLUMN rule_row.rule_table IS 'The Epic 1 rule table a row belongs to';
COMMENT ON COLUMN rule_row.row_order IS 'Order in which rows of one rule table are evaluated; first match wins';
COMMENT ON COLUMN rule_row.target_queue_code IS 'The queue an allocation or transfer row places the case in';
COMMENT ON COLUMN rule_row.package_version_id IS 'DF-REF-296. The rule_package_version the row was parsed from';
COMMENT ON COLUMN rule_row.drools_rule_name IS 'DF-REF-297. Rule name in the DRL, the rule ID, for example ALLOC-031';
COMMENT ON COLUMN rule_row.outputs IS 'DF-REF-298. Output columns of the decision-table row as JSON';
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
COMMENT ON COLUMN rule_test_case.id IS 'Record identifier of the rule test case';
COMMENT ON COLUMN rule_test_case.test_case_id IS 'The test case named by rule_row.test_case_id';
COMMENT ON COLUMN rule_test_case.route_set IS 'Route set';
COMMENT ON COLUMN rule_test_case.rule_version IS 'Rule version tested';
COMMENT ON COLUMN rule_test_case.rule_id IS 'Rule the test expects to hit';
COMMENT ON COLUMN rule_test_case.package_version_id IS 'DF-REF-299. The rule_package_version the test case runs against';
COMMENT ON COLUMN rule_test_case.from_state IS 'Input state';
COMMENT ON COLUMN rule_test_case.event_code IS 'Input event';
COMMENT ON COLUMN rule_test_case.facts IS 'Synthetic case file facts the condition reads';
COMMENT ON COLUMN rule_test_case.expected_to_state IS 'Expected to state';
COMMENT ON COLUMN rule_test_case.expected_owner_role IS 'Expected owner role';
COMMENT ON COLUMN rule_test_case.expected_timer_spec IS 'Expected timer';
COMMENT ON COLUMN rule_test_case.result IS 'Passed or failed';
COMMENT ON COLUMN rule_test_case.result_detail IS 'Expected against actual, and the rows that hit';
COMMENT ON COLUMN approval.id IS 'Record identifier of the approval';
COMMENT ON COLUMN approval.case_id IS 'The case';
COMMENT ON COLUMN approval.decision_code IS 'Decision to approve';
COMMENT ON COLUMN approval.regulation_item IS 'Delegation item, for example 2.1.1';
COMMENT ON COLUMN approval.capability_area IS 'Area whose A letter the approver needs';
COMMENT ON COLUMN approval.route_role_code IS 'Role for a decision with no amount limit, for example RW-LITOFF';
COMMENT ON COLUMN approval.approval_level IS 'Required level L1 to L6';
COMMENT ON COLUMN approval.delegation_limit_id IS 'Delegation row that covers the item';
COMMENT ON COLUMN approval.limit_version IS 'Delegation version the item routed under';
COMMENT ON COLUMN approval.product_group IS 'Product group';
COMMENT ON COLUMN approval.amount IS 'Principal used for the limit, baht';
COMMENT ON COLUMN approval.terms IS 'Proposed and changed terms';
COMMENT ON COLUMN approval.prepared_by IS 'Person or service identity that prepared the item';
COMMENT ON COLUMN approval.assigned_user_id IS 'Holder the item is assigned to; empty for a role route';
COMMENT ON COLUMN approval.status IS 'Waiting, held with no limit, approved, refused or returned';
COMMENT ON COLUMN approval.due_at IS 'When the service level ends';
COMMENT ON COLUMN approval.escalation_level IS 'Times escalated';
COMMENT ON COLUMN approval.source_type IS 'What asked for approval, for example NOTICE or TREATMENT';
COMMENT ON COLUMN approval.source_ref IS 'ID of the source record, for example the notice ID';
COMMENT ON COLUMN approval.rule_id IS 'Rule that asked for approval';
COMMENT ON COLUMN approval.rule_version IS 'Version of that rule';
COMMENT ON COLUMN approval.decision_log_id IS 'Decision log entry of the outcome';

-- ---------------------------------------------------------------------------
-- Seed and dictionary rows
-- ---------------------------------------------------------------------------

-- Seed: rule packages (D-RCV-36, ADR-012)
INSERT INTO rule_package (package_code, title, owner_role, hit_policy) VALUES ('ENTRY', 'Entry rules', 'RW-COE', 'FIRST');
INSERT INTO rule_package (package_code, title, owner_role, hit_policy) VALUES ('EXCLUSION', 'Exclusion rules', 'RW-COE', 'FIRST');
INSERT INTO rule_package (package_code, title, owner_role, hit_policy) VALUES ('ALLOCATION', 'Allocation rules', 'RW-COE', 'FIRST');
INSERT INTO rule_package (package_code, title, owner_role, hit_policy) VALUES ('ASSIGNMENT', 'Assignment rules', 'RW-COE', 'FIRST');
INSERT INTO rule_package (package_code, title, owner_role, hit_policy) VALUES ('TRANSFER', 'Transfer rules', 'RW-COE', 'FIRST');
INSERT INTO rule_package (package_code, title, owner_role, hit_policy) VALUES ('RESTRUCTURE', 'Restructure rules', 'RW-COE', 'FIRST');
INSERT INTO rule_package (package_code, title, owner_role, hit_policy) VALUES ('PAYMENT_MATCH', 'Payment match rules', 'RW-COE', 'FIRST');
INSERT INTO rule_package (package_code, title, owner_role, hit_policy) VALUES ('BOOKING_MATCH', 'Booking match rules', 'RW-COE', 'FIRST');

-- ---------------------------------------------------------------------------
-- Cross-service references cut from this file (no database foreign key)
-- ---------------------------------------------------------------------------
-- decision_log_entry.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- outbox_event.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- outbox_delivery.task_id -> rwb_case.task.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- approval.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- approval.delegation_limit_id -> rwb_access.delegation_limit.id (owner P4); the column stays uuid and integrity is through the owner's contract.

-- ---------------------------------------------------------------------------
-- Migration provenance columns (RD-P1-027; 27 November 2026). Added once per table by the owner's own Flyway step;
-- null for rows created live. LOV-MIGRATION-SOURCE values are Pending, owner data owner (GAP-3275).
-- ---------------------------------------------------------------------------
ALTER TABLE decision_log_entry ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN decision_log_entry.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN decision_log_entry.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE approval ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN approval.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN approval.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE rule_package ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN rule_package.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN rule_package.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE rule_package_version ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN rule_package_version.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN rule_package_version.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE rule_row ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN rule_row.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN rule_row.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE rule_test_case ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN rule_test_case.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN rule_test_case.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
