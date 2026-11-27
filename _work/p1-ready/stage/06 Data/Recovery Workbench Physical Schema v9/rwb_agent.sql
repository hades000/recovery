-- SCB Collections and Recovery. Henka Group, 22 November 2026.
-- (C) Siam Commercial Bank and Henka Pte Ltd
-- Recovery Workbench physical schema, PostgreSQL. Service rwb-agent (P10, Agent), wave 1. Version 7.
-- Change log: 7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.
-- Schema rwb_agent; login rwb_agent; REST base /api/recovery/agent/v1; topic rwb.agent.events.v1; queue rwb-agent.
-- Source: 06 Data/Recovery Workbench Physical Schema v6.sql (read only). Table, index, comment and seed text is copied unchanged; only the schema and the foreign keys change.
-- Tables in this file: 8. Owned by this service in the Ownership Map v1: 8. Platform library objects created here as well: 4.
-- Owner for every object comes from Recovery Workbench Microservice Ownership Map v1 (D-RCV-60).
-- Cross-owner references: a foreign key whose two tables have different owners in the Ownership Map is cut to a plain uuid column; integrity is through the owner's API contract (see README.md).

CREATE SCHEMA IF NOT EXISTS rwb_agent;
SET search_path TO rwb_agent;
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

-- Agent policy: A version of an agent's policy: model, tools, autonomy, limits and fallback.
CREATE TABLE agent_policy (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_code varchar(30) NOT NULL,
    policy_version varchar(20) NOT NULL,
    model_code varchar(40) NOT NULL,
    model_version varchar(40) NOT NULL,
    output_schema_ref varchar(400) NOT NULL,
    allowed_tools jsonb,
    autonomy_mode varchar(10) NOT NULL DEFAULT 'OFF',
    segment_product_group varchar(15),
    segment_region_code varchar(10),
    confidence_floor numeric(5,4) NOT NULL,
    timeout_seconds integer NOT NULL,
    daily_cost_cap_thb numeric(12,2) NOT NULL,
    price_per_1k_tokens_thb numeric(10,4) NOT NULL,
    alert_role varchar(20) NOT NULL,
    review_date date,
    evaluation_run_id uuid,
    promotion_conditions jsonb,
    watch_measures jsonb,
    fallback_rule varchar(20),
    status varchar(12) NOT NULL DEFAULT 'LOADED',
    valid_from date NOT NULL,
    valid_to date,
    loaded_by uuid NOT NULL,
    approved_by uuid,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_agent_policy UNIQUE (agent_code, policy_version)
);

-- Agent prompt: A version of an agent's prompt text.
CREATE TABLE agent_prompt (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_code varchar(30) NOT NULL,
    prompt_version varchar(20) NOT NULL,
    body_text text NOT NULL,
    body_hash char(64) NOT NULL,
    status varchar(12) NOT NULL DEFAULT 'LOADED',
    valid_from date NOT NULL,
    valid_to date,
    loaded_by uuid NOT NULL,
    approved_by uuid,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_agent_prompt UNIQUE (agent_code, prompt_version)
);

-- Agent run: One call of an agent or model, with its versions, checks, answer, cost and fallback.
CREATE TABLE agent_run (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_code varchar(30) NOT NULL,
    agent_version varchar(40) NOT NULL,
    prompt_version varchar(20),
    model_version varchar(40) NOT NULL,
    case_id uuid,  -- cross-service reference: rwb_case.recovery_case(id); integrity through the owner's contract
    subject_id uuid,
    autonomy_mode varchar(10) NOT NULL,
    trigger_event varchar(30) NOT NULL,
    idempotency_key varchar(120) NOT NULL,
    status varchar(20) NOT NULL,
    fallback boolean NOT NULL DEFAULT false,
    guardrail_result jsonb,
    output jsonb,
    confidence numeric(5,4),
    latency_ms integer,
    tokens_in integer,
    tokens_out integer,
    cost_thb numeric(12,4),
    data_as_of date,
    run_at timestamptz NOT NULL,
    evaluation_run_id uuid,
    decision_log_id uuid,  -- cross-service reference: rwb_decision.decision_log_entry(id); integrity through the owner's contract
    segment_product_group varchar(15),
    segment_region_code varchar(10),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_agent_run UNIQUE (idempotency_key)
);

-- Agent sample: One labeled subject in a versioned evaluation sample.
CREATE TABLE agent_sample (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_code varchar(30) NOT NULL,
    sample_code varchar(30) NOT NULL,
    sample_version integer NOT NULL,
    subject_type varchar(15) NOT NULL,
    subject_id uuid NOT NULL,
    label_key varchar(60) NOT NULL,
    expected_value varchar(1000),
    labeled_by uuid NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_agent_sample UNIQUE (sample_code, sample_version, label_key)
);

-- Agent evaluation run: One evaluation of an agent version against a sample.
CREATE TABLE agent_evaluation_run (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_code varchar(30) NOT NULL,
    sample_code varchar(30) NOT NULL,
    sample_version integer NOT NULL,
    policy_version varchar(20),
    prompt_version varchar(20),
    model_version varchar(40),
    status varchar(12) NOT NULL DEFAULT 'RUNNING',
    started_at timestamptz NOT NULL,
    finished_at timestamptz,
    requested_by uuid NOT NULL,
    total_cost_thb numeric(12,4),
    p95_latency_ms integer,
    failure_counts jsonb,
    proposal jsonb,
    review_count integer,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Agent evaluation: The score of one approach on one label key in an evaluation run.
CREATE TABLE agent_evaluation (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_run_id uuid NOT NULL,
    approach varchar(20) NOT NULL,
    label_key varchar(60) NOT NULL,
    sample_size integer NOT NULL,
    true_positive integer,
    false_positive integer,
    false_negative integer,
    agreement_rate numeric(5,4),
    precision_value numeric(5,4),
    recall_value numeric(5,4),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Agent feedback: A person's verdict on an agent answer.
CREATE TABLE agent_feedback (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_run_id uuid NOT NULL,
    item_key varchar(20) NOT NULL,
    verdict varchar(10) NOT NULL,
    reason varchar(1000),
    decision_log_id uuid,  -- cross-service reference: rwb_decision.decision_log_entry(id); integrity through the owner's contract
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Agent alert: A cost cap or drift alert raised for an agent.
CREATE TABLE agent_alert (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_code varchar(30) NOT NULL,
    alert_type varchar(12) NOT NULL,
    segment varchar(30) NOT NULL,
    business_date date NOT NULL,
    measured_value numeric(14,4) NOT NULL,
    threshold_value numeric(14,4) NOT NULL,
    sent_to_role varchar(20) NOT NULL,
    sent_at timestamptz,
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
ALTER TABLE agent_policy ADD CONSTRAINT fk_agent_policy_evaluation_run_id FOREIGN KEY (evaluation_run_id) REFERENCES agent_evaluation_run (id) ON DELETE RESTRICT;
ALTER TABLE agent_run ADD CONSTRAINT fk_agent_run_evaluation_run_id FOREIGN KEY (evaluation_run_id) REFERENCES agent_evaluation_run (id) ON DELETE RESTRICT;
ALTER TABLE agent_evaluation ADD CONSTRAINT fk_agent_evaluation_evaluation_run_id FOREIGN KEY (evaluation_run_id) REFERENCES agent_evaluation_run (id) ON DELETE RESTRICT;
ALTER TABLE agent_feedback ADD CONSTRAINT fk_agent_feedback_agent_run_id FOREIGN KEY (agent_run_id) REFERENCES agent_run (id) ON DELETE RESTRICT;

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------

CREATE INDEX ix_processed_event_event_id ON processed_event (event_id);
CREATE INDEX ix_outbox_event_case_id ON outbox_event (case_id);
CREATE INDEX ix_outbox_delivery_event_id ON outbox_delivery (event_id);
CREATE INDEX ix_outbox_delivery_task_id ON outbox_delivery (task_id);
CREATE INDEX ix_agent_policy_evaluation_run_id ON agent_policy (evaluation_run_id);
CREATE INDEX ix_agent_run_case_id ON agent_run (case_id);
CREATE INDEX ix_agent_run_evaluation_run_id ON agent_run (evaluation_run_id);
CREATE INDEX ix_agent_run_decision_log_id ON agent_run (decision_log_id);
CREATE INDEX ix_agent_evaluation_evaluation_run_id ON agent_evaluation (evaluation_run_id);
CREATE INDEX ix_agent_feedback_agent_run_id ON agent_feedback (agent_run_id);
CREATE INDEX ix_agent_feedback_decision_log_id ON agent_feedback (decision_log_id);

-- ---------------------------------------------------------------------------
-- Data dictionary comments
-- ---------------------------------------------------------------------------

COMMENT ON TABLE agent_alert IS 'A cost cap or drift alert raised for an agent.';
COMMENT ON TABLE agent_feedback IS 'A person''s verdict on an agent answer.';
COMMENT ON TABLE agent_evaluation IS 'The score of one approach on one label key in an evaluation run.';
COMMENT ON TABLE agent_evaluation_run IS 'One evaluation of an agent version against a sample.';
COMMENT ON TABLE agent_sample IS 'One labeled subject in a versioned evaluation sample.';
COMMENT ON TABLE agent_run IS 'One call of an agent or model, with its versions, checks, answer, cost and fallback.';
COMMENT ON TABLE agent_prompt IS 'A version of an agent''s prompt text.';
COMMENT ON TABLE agent_policy IS 'A version of an agent''s policy: model, tools, autonomy, limits and fallback.';
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
COMMENT ON COLUMN agent_policy.id IS 'Record identifier of the agent policy version';
COMMENT ON COLUMN agent_policy.agent_code IS 'Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER';
COMMENT ON COLUMN agent_policy.policy_version IS 'Policy version, for example P1';
COMMENT ON COLUMN agent_policy.model_code IS 'Model deployment the agent calls through the gateway';
COMMENT ON COLUMN agent_policy.model_version IS 'Model version the policy uses';
COMMENT ON COLUMN agent_policy.output_schema_ref IS 'Reference to the JSON Schema the answer must meet';
COMMENT ON COLUMN agent_policy.allowed_tools IS 'Tools the agent may call through the tool gateway';
COMMENT ON COLUMN agent_policy.autonomy_mode IS 'Off, shadow or L1';
COMMENT ON COLUMN agent_policy.segment_product_group IS 'Product group the mode applies to; empty for all';
COMMENT ON COLUMN agent_policy.segment_region_code IS 'Region the mode applies to; empty for all';
COMMENT ON COLUMN agent_policy.confidence_floor IS 'Answers below this confidence fall back or are marked for review';
COMMENT ON COLUMN agent_policy.timeout_seconds IS 'Seconds the gateway waits before the rule result is used';
COMMENT ON COLUMN agent_policy.daily_cost_cap_thb IS 'Daily model cost limit per agent, baht';
COMMENT ON COLUMN agent_policy.price_per_1k_tokens_thb IS 'Model price per 1,000 tokens, baht';
COMMENT ON COLUMN agent_policy.alert_role IS 'Role that receives cost and drift alerts';
COMMENT ON COLUMN agent_policy.review_date IS 'Date the version is reviewed again, for a parked or shadow agent';
COMMENT ON COLUMN agent_policy.evaluation_run_id IS 'Evaluation run an autonomy step is based on';
COMMENT ON COLUMN agent_policy.promotion_conditions IS 'Conditions the evaluation must meet for the stated mode';
COMMENT ON COLUMN agent_policy.watch_measures IS 'Measures and limits to watch after the step, including drift points and minimum feedback';
COMMENT ON COLUMN agent_policy.fallback_rule IS 'Rule applied when the agent does not answer, for example R-UNI-32';
COMMENT ON COLUMN agent_policy.status IS 'Loaded, approved or retired';
COMMENT ON COLUMN agent_policy.valid_from IS 'Date the version takes effect';
COMMENT ON COLUMN agent_policy.valid_to IS 'Last date the version is in force';
COMMENT ON COLUMN agent_policy.loaded_by IS 'Who loaded the version';
COMMENT ON COLUMN agent_policy.approved_by IS 'Who approved the version';
COMMENT ON COLUMN agent_prompt.id IS 'Record identifier of the agent prompt version';
COMMENT ON COLUMN agent_prompt.agent_code IS 'Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER';
COMMENT ON COLUMN agent_prompt.prompt_version IS 'Prompt version, for example PR1';
COMMENT ON COLUMN agent_prompt.body_text IS 'Prompt text with placeholders; no personal data';
COMMENT ON COLUMN agent_prompt.body_hash IS 'SHA-256 of the prompt text';
COMMENT ON COLUMN agent_prompt.status IS 'Loaded, approved or retired';
COMMENT ON COLUMN agent_prompt.valid_from IS 'Date the version takes effect';
COMMENT ON COLUMN agent_prompt.valid_to IS 'Last date the version is in force';
COMMENT ON COLUMN agent_prompt.loaded_by IS 'Who loaded the version';
COMMENT ON COLUMN agent_prompt.approved_by IS 'Who approved the version';
COMMENT ON COLUMN agent_run.id IS 'Record identifier of the agent run';
COMMENT ON COLUMN agent_run.agent_code IS 'Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER';
COMMENT ON COLUMN agent_run.agent_version IS 'Agent, policy and prompt version as <agent>@<policy>/<prompt>';
COMMENT ON COLUMN agent_run.prompt_version IS 'Prompt version used';
COMMENT ON COLUMN agent_run.model_version IS 'Model version used';
COMMENT ON COLUMN agent_run.case_id IS 'The case the run is for';
COMMENT ON COLUMN agent_run.subject_id IS 'Document, legal action or treatment the run is about, where not the case';
COMMENT ON COLUMN agent_run.autonomy_mode IS 'Mode the run used: shadow or L1';
COMMENT ON COLUMN agent_run.trigger_event IS 'CaseCreated, DocumentStored, STEP or EVALUATION';
COMMENT ON COLUMN agent_run.idempotency_key IS 'Unique key of the run request';
COMMENT ON COLUMN agent_run.status IS 'Answered, timed out, guardrail failed, below floor, tool unavailable, model error or disabled';
COMMENT ON COLUMN agent_run.fallback IS 'True when the rule result was used instead of the answer';
COMMENT ON COLUMN agent_run.guardrail_result IS 'Failed check codes and details';
COMMENT ON COLUMN agent_run.output IS 'Checked answer, masked; never returned for shadow runs';
COMMENT ON COLUMN agent_run.confidence IS 'Confidence of the answer';
COMMENT ON COLUMN agent_run.latency_ms IS 'Time from call to answer or timeout, milliseconds';
COMMENT ON COLUMN agent_run.tokens_in IS 'Input tokens returned by the endpoint';
COMMENT ON COLUMN agent_run.tokens_out IS 'Output tokens returned by the endpoint';
COMMENT ON COLUMN agent_run.cost_thb IS 'Cost of the run, baht';
COMMENT ON COLUMN agent_run.data_as_of IS 'Oldest business date of the inputs used';
COMMENT ON COLUMN agent_run.run_at IS 'When the run started';
COMMENT ON COLUMN agent_run.evaluation_run_id IS 'Evaluation run the run belongs to, if any';
COMMENT ON COLUMN agent_run.decision_log_id IS 'Decision log entry written for the step that used the run';
COMMENT ON COLUMN agent_run.segment_product_group IS 'Product group of the case at run time';
COMMENT ON COLUMN agent_run.segment_region_code IS 'Region of the case at run time';
COMMENT ON COLUMN agent_sample.id IS 'Record identifier of the sample row';
COMMENT ON COLUMN agent_sample.agent_code IS 'Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER';
COMMENT ON COLUMN agent_sample.sample_code IS 'Sample code, for example INTAKE-S1';
COMMENT ON COLUMN agent_sample.sample_version IS 'Version of the sample';
COMMENT ON COLUMN agent_sample.subject_type IS 'Case, document or legal action';
COMMENT ON COLUMN agent_sample.subject_id IS 'The case, document or legal action labeled';
COMMENT ON COLUMN agent_sample.label_key IS 'Gap type, deviation code, field name or checklist item';
COMMENT ON COLUMN agent_sample.expected_value IS 'Labeled value; SHA-256 hash for personal values';
COMMENT ON COLUMN agent_sample.labeled_by IS 'Who labeled the row';
COMMENT ON COLUMN agent_evaluation_run.id IS 'Record identifier of the evaluation run';
COMMENT ON COLUMN agent_evaluation_run.agent_code IS 'Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER';
COMMENT ON COLUMN agent_evaluation_run.sample_code IS 'Sample used';
COMMENT ON COLUMN agent_evaluation_run.sample_version IS 'Sample version used';
COMMENT ON COLUMN agent_evaluation_run.policy_version IS 'Policy version evaluated';
COMMENT ON COLUMN agent_evaluation_run.prompt_version IS 'Prompt version evaluated';
COMMENT ON COLUMN agent_evaluation_run.model_version IS 'Model version evaluated';
COMMENT ON COLUMN agent_evaluation_run.status IS 'Running, done or failed';
COMMENT ON COLUMN agent_evaluation_run.started_at IS 'When the run started';
COMMENT ON COLUMN agent_evaluation_run.finished_at IS 'When the run ended';
COMMENT ON COLUMN agent_evaluation_run.requested_by IS 'Who started the run';
COMMENT ON COLUMN agent_evaluation_run.total_cost_thb IS 'Cost of all runs in the evaluation, baht';
COMMENT ON COLUMN agent_evaluation_run.p95_latency_ms IS '95th percentile latency, milliseconds';
COMMENT ON COLUMN agent_evaluation_run.failure_counts IS 'Count of runs by failure status and check code';
COMMENT ON COLUMN agent_evaluation_run.proposal IS 'Proposed approach and confidence threshold per document type';
COMMENT ON COLUMN agent_evaluation_run.review_count IS 'Proposals below the confidence floor, scored separately';
COMMENT ON COLUMN agent_evaluation.id IS 'Record identifier of the evaluation score';
COMMENT ON COLUMN agent_evaluation.evaluation_run_id IS 'Evaluation run the score belongs to';
COMMENT ON COLUMN agent_evaluation.approach IS 'Agent, OCR template, model, or OCR and model';
COMMENT ON COLUMN agent_evaluation.label_key IS 'Gap type, code, field or item scored';
COMMENT ON COLUMN agent_evaluation.sample_size IS 'Labeled subjects scored';
COMMENT ON COLUMN agent_evaluation.true_positive IS 'True positives';
COMMENT ON COLUMN agent_evaluation.false_positive IS 'False positives';
COMMENT ON COLUMN agent_evaluation.false_negative IS 'False negatives';
COMMENT ON COLUMN agent_evaluation.agreement_rate IS 'Share of subjects where the answer equals the label';
COMMENT ON COLUMN agent_evaluation.precision_value IS 'TP / (TP + FP)';
COMMENT ON COLUMN agent_evaluation.recall_value IS 'TP / (TP + FN)';
COMMENT ON COLUMN agent_feedback.id IS 'Record identifier of the feedback';
COMMENT ON COLUMN agent_feedback.agent_run_id IS 'Agent run the feedback is on';
COMMENT ON COLUMN agent_feedback.item_key IS 'SUMMARY for the intake summary, or the deviation code';
COMMENT ON COLUMN agent_feedback.verdict IS 'Accepted, corrected or rejected';
COMMENT ON COLUMN agent_feedback.reason IS 'Reason for a correction or a rejection';
COMMENT ON COLUMN agent_feedback.decision_log_id IS 'Decision log entry written for the feedback';
COMMENT ON COLUMN agent_alert.id IS 'Record identifier of the alert';
COMMENT ON COLUMN agent_alert.agent_code IS 'Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER';
COMMENT ON COLUMN agent_alert.alert_type IS 'Cost cap or drift';
COMMENT ON COLUMN agent_alert.segment IS 'Product group and region, or ALL';
COMMENT ON COLUMN agent_alert.business_date IS 'Business date measured';
COMMENT ON COLUMN agent_alert.measured_value IS 'Cost in baht or acceptance rate measured';
COMMENT ON COLUMN agent_alert.threshold_value IS 'Limit the value was compared with';
COMMENT ON COLUMN agent_alert.sent_to_role IS 'Role notified';
COMMENT ON COLUMN agent_alert.sent_at IS 'When the notification was sent; empty until sent';

-- ---------------------------------------------------------------------------
-- Cross-service references cut from this file (no database foreign key)
-- ---------------------------------------------------------------------------
-- outbox_event.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- outbox_delivery.task_id -> rwb_case.task.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- agent_run.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- agent_run.decision_log_id -> rwb_decision.decision_log_entry.id (owner P7); the column stays uuid and integrity is through the owner's contract.
-- agent_feedback.decision_log_id -> rwb_decision.decision_log_entry.id (owner P7); the column stays uuid and integrity is through the owner's contract.
