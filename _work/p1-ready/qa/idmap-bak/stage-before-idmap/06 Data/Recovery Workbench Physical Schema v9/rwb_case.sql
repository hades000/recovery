-- SCB Collections and Recovery. Henka Group, 22 November 2026.
-- (C) Siam Commercial Bank and Henka Pte Ltd
-- Recovery Workbench physical schema, PostgreSQL. Service rwb-case (P3, Case and workflow), wave 1. Version 7.
-- Change log: 7, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.
-- Change log: 9, 27 November 2026, D-RCV-60 P1 developer readiness (RD-P1 register); targeted edits.
-- Schema rwb_case; login rwb_case; REST base /api/recovery/case/v1; topic rwb.case.events.v1; queue rwb-case.
-- Source: 06 Data/Recovery Workbench Physical Schema v6.sql (read only). Table, index, comment and seed text is copied unchanged; only the schema and the foreign keys change.
-- Tables in this file: 15. Owned by this service in the Ownership Map v1: 15. Platform library objects created here as well: 4.
-- Owner for every object comes from Recovery Workbench Microservice Ownership Map v1 (D-RCV-60).
-- Cross-owner references: a foreign key whose two tables have different owners in the Ownership Map is cut to a plain uuid column; integrity is through the owner's API contract (see README.md).

CREATE SCHEMA IF NOT EXISTS rwb_case;
SET search_path TO rwb_case;
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

-- Recovery case: One recovery case per customer per product, from 90 days past due to close.
CREATE TABLE recovery_case (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_no varchar(18) NOT NULL,
    product_group varchar(15) NOT NULL,
    primary_person_key varchar(255),
    status varchar(20) NOT NULL DEFAULT 'NEW',
    stage_code varchar(20),
    route_state varchar(60),
    route_code varchar(4),
    owner_user_id uuid,
    queue_id uuid,
    team_code varchar(20),
    region_code varchar(10),
    entry_date date NOT NULL,
    dpd_at_entry integer NOT NULL,
    exposure_band varchar(10),
    total_outstanding_at_entry numeric(18,2) NOT NULL,
    prescription_date date,
    stage_clock_start timestamptz,
    deviation_open boolean NOT NULL DEFAULT false,
    legal_hold boolean NOT NULL DEFAULT false,
    rule_version varchar(20),
    closed_date date,
    closure_reason varchar(20),
    plan_ref varchar(30),
    plan_status varchar(10),
    plan_status_as_of date,
    next_action_text varchar(1000),
    next_action_owner_role varchar(20),
    next_action_due_date date,
    next_action_rule_id varchar(20),
    next_action_waiting boolean NOT NULL DEFAULT false,
    last_allocation_date date,
    status_before_hold varchar(20),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_recovery_case UNIQUE (case_no)
);

-- Case account: Links each loan account to the case it is recovered under.
CREATE TABLE case_account (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    account_key varchar(255),
    is_primary boolean NOT NULL DEFAULT false,
    linked_from date NOT NULL,
    linked_to date,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Case party: The role each party plays on a case.
CREATE TABLE case_party (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    person_key varchar(255),
    party_role varchar(20) NOT NULL,
    role_from date NOT NULL,
    role_to date,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Queue: A queue of work belonging to one team and one role.
CREATE TABLE queue (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    queue_code varchar(30) NOT NULL,
    queue_name varchar(100) NOT NULL,
    team_code varchar(20) NOT NULL,
    role_code varchar(20) NOT NULL,
    assignment_method varchar(20) NOT NULL DEFAULT 'ROUND_ROBIN',
    capacity_cap integer,
    overflow_queue_id uuid,
    rr_cursor_user_id uuid,
    table_version integer,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_queue UNIQUE (queue_code)
);

-- Assignment: Who holds a case or a task and from when.
CREATE TABLE assignment (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    task_id uuid,
    assignee_user_id uuid NOT NULL,
    assigned_at timestamptz NOT NULL DEFAULT now(),
    ended_at timestamptz,
    reason varchar(20) NOT NULL,
    rule_id varchar(20),
    queue_id uuid,
    transfer_reason_code varchar(20),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Task: A unit of work on a case: a CMMN human, customer, partner or decision task.
CREATE TABLE task (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    task_code varchar(60) NOT NULL,
    element_type varchar(20) NOT NULL,
    discretion varchar(15) NOT NULL,
    status varchar(15) NOT NULL DEFAULT 'OPEN',
    owner_role varchar(20),
    due_at timestamptz,
    completed_at timestamptz,
    outcome_code varchar(40),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Timer: A running clock on a case: a service level, a legal period or an offer validity.
CREATE TABLE timer (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    task_id uuid,
    timer_type varchar(20) NOT NULL,
    started_at timestamptz NOT NULL,
    expires_at timestamptz NOT NULL,
    warn_at timestamptz,
    paused boolean NOT NULL DEFAULT false,
    status varchar(15) NOT NULL DEFAULT 'RUNNING',
    escalation_level integer NOT NULL DEFAULT 0,
    warned_at timestamptz,
    treatment_id uuid,  -- cross-service reference: rwb_treatment.treatment(id); integrity through the owner's contract
    escalated_to_role varchar(20),
    escalated_at timestamptz,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- List value: A value in a list of values.
CREATE TABLE lov_value (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    lov_code varchar(30) NOT NULL,
    value_code varchar(30) NOT NULL,
    label_en varchar(120) NOT NULL,
    label_th varchar(120),
    sort_order integer NOT NULL DEFAULT 0,
    valid_from date NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_lov_value UNIQUE (lov_code, value_code)
);

-- Case entry exclusion: An account at 90 days past due that an exclusion rule kept out of recovery on a business date.
CREATE TABLE case_entry_exclusion (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_key varchar(255),
    business_date date NOT NULL,
    reason_code varchar(20) NOT NULL,
    rule_id varchar(20) NOT NULL,
    rule_version varchar(20) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_case_entry_exclusion UNIQUE (business_date, account_key)
);

-- Queue member: A person who works a queue, with personal capacity and skills, by version.
CREATE TABLE queue_member (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    queue_id uuid NOT NULL,
    user_id uuid NOT NULL,
    capacity integer,
    skill_codes varchar(200),
    table_version integer NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Queue measure: One snapshot of a queue's counts, ageing and breaches, published when it reconciles to the case list.
CREATE TABLE queue_measure (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    queue_id uuid NOT NULL,
    as_of timestamptz NOT NULL,
    depth integer NOT NULL,
    unassigned integer NOT NULL,
    avg_age_days numeric(7,2),
    max_age_days integer,
    owner_min integer,
    owner_max integer,
    breached integer NOT NULL,
    status varchar(15) NOT NULL DEFAULT 'TAKEN',
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_queue_measure UNIQUE (as_of)
);

-- Parameter catalog: The definition of every parameter and environment setting, with its owner and default.
CREATE TABLE parameter_catalog (
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

-- Parameter value: An approved, dated value version of a parameter per environment and product group.
CREATE TABLE parameter_value (
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

-- Reference version: One version of a reference or rule table, with its author, approver, checks and change checklist.
CREATE TABLE reference_version (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    table_code varchar(30) NOT NULL,
    version_no integer NOT NULL,
    version_label varchar(20),
    valid_from date NOT NULL,
    valid_to date,
    status varchar(15) NOT NULL DEFAULT 'VALIDATED',
    author_user_id uuid NOT NULL,
    approver_user_id uuid,
    approved_at timestamptz,
    row_count integer NOT NULL,
    content_hash char(64) NOT NULL,
    load_id uuid NOT NULL,
    dry_run_counts jsonb,
    rollback_reason varchar(400),
    change_request_ref varchar(30),
    impact_summary varchar(1000),
    test_result varchar(10),
    rollback_plan varchar(1000),
    verified_by uuid,
    verified_at timestamptz,
    verify_note varchar(1000),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_reference_version UNIQUE (table_code, version_no)
);

-- Reference row: One row of a reference table version held as data.
CREATE TABLE reference_row (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    version_id uuid NOT NULL,
    row_key varchar(200) NOT NULL,
    row_data jsonb NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_reference_row UNIQUE (row_key)
);

-- ---------------------------------------------------------------------------
-- Foreign keys kept inside this service (same owner).
-- ---------------------------------------------------------------------------

ALTER TABLE recovery_case ADD CONSTRAINT fk_recovery_case_queue_id FOREIGN KEY (queue_id) REFERENCES queue (id) ON DELETE RESTRICT;
ALTER TABLE case_account ADD CONSTRAINT fk_case_account_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE case_party ADD CONSTRAINT fk_case_party_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE queue ADD CONSTRAINT fk_queue_overflow_queue_id FOREIGN KEY (overflow_queue_id) REFERENCES queue (id) ON DELETE RESTRICT;
ALTER TABLE assignment ADD CONSTRAINT fk_assignment_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE assignment ADD CONSTRAINT fk_assignment_task_id FOREIGN KEY (task_id) REFERENCES task (id) ON DELETE RESTRICT;
ALTER TABLE assignment ADD CONSTRAINT fk_assignment_queue_id FOREIGN KEY (queue_id) REFERENCES queue (id) ON DELETE RESTRICT;
ALTER TABLE task ADD CONSTRAINT fk_task_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE timer ADD CONSTRAINT fk_timer_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE timer ADD CONSTRAINT fk_timer_task_id FOREIGN KEY (task_id) REFERENCES task (id) ON DELETE RESTRICT;
ALTER TABLE processed_event ADD CONSTRAINT fk_processed_event_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;
ALTER TABLE outbox_delivery ADD CONSTRAINT fk_outbox_delivery_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;
ALTER TABLE queue_member ADD CONSTRAINT fk_queue_member_queue_id FOREIGN KEY (queue_id) REFERENCES queue (id) ON DELETE RESTRICT;
ALTER TABLE queue_measure ADD CONSTRAINT fk_queue_measure_queue_id FOREIGN KEY (queue_id) REFERENCES queue (id) ON DELETE RESTRICT;
ALTER TABLE reference_row ADD CONSTRAINT fk_reference_row_version_id FOREIGN KEY (version_id) REFERENCES reference_version (id) ON DELETE RESTRICT;

-- ---------------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------------

-- Indexes on references and on the columns queues, timers and the decision log are read by
CREATE INDEX ix_recovery_case_primary_person_key ON recovery_case (primary_person_key);
CREATE INDEX ix_recovery_case_queue_id ON recovery_case (queue_id);
CREATE INDEX ix_case_account_case_id ON case_account (case_id);
CREATE INDEX ix_case_account_account_key ON case_account (account_key);
CREATE INDEX ix_case_party_case_id ON case_party (case_id);
CREATE INDEX ix_case_party_person_key ON case_party (person_key);
CREATE INDEX ix_queue_overflow_queue_id ON queue (overflow_queue_id);
CREATE INDEX ix_assignment_case_id ON assignment (case_id);
CREATE INDEX ix_assignment_task_id ON assignment (task_id);
CREATE INDEX ix_assignment_queue_id ON assignment (queue_id);
CREATE INDEX ix_task_case_id ON task (case_id);
CREATE INDEX ix_timer_case_id ON timer (case_id);
CREATE INDEX ix_timer_task_id ON timer (task_id);
CREATE INDEX ix_timer_treatment_id ON timer (treatment_id);
CREATE INDEX ix_processed_event_event_id ON processed_event (event_id);
CREATE INDEX ix_outbox_event_case_id ON outbox_event (case_id);
CREATE INDEX ix_outbox_delivery_event_id ON outbox_delivery (event_id);
CREATE INDEX ix_outbox_delivery_task_id ON outbox_delivery (task_id);
CREATE INDEX ix_case_entry_exclusion_account_key ON case_entry_exclusion (account_key);
CREATE INDEX ix_queue_member_queue_id ON queue_member (queue_id);
CREATE INDEX ix_queue_measure_queue_id ON queue_measure (queue_id);
CREATE INDEX ix_reference_row_version_id ON reference_row (version_id);
CREATE INDEX ix_case_status_queue ON recovery_case (status, queue_id);
CREATE INDEX ix_case_owner_status ON recovery_case (owner_user_id, status);
CREATE INDEX ix_case_prescription ON recovery_case (prescription_date) WHERE closed_date IS NULL;
CREATE INDEX ix_timer_due ON timer (expires_at) WHERE status = 'RUNNING';
CREATE INDEX ix_task_open ON task (case_id, status) WHERE status IN ('OPEN','IN_PROGRESS');

-- ---------------------------------------------------------------------------
-- Data dictionary comments
-- ---------------------------------------------------------------------------

COMMENT ON TABLE reference_row IS 'One row of a reference table version held as data.';
COMMENT ON TABLE reference_version IS 'One version of a reference or rule table, with its author, approver, checks and change checklist.';
COMMENT ON TABLE parameter_value IS 'An approved, dated value version of a parameter per environment and product group.';
COMMENT ON TABLE parameter_catalog IS 'The definition of every parameter and environment setting, with its owner and default.';
COMMENT ON TABLE queue_measure IS 'One snapshot of a queue''s counts, ageing and breaches, published when it reconciles to the case list.';
COMMENT ON TABLE queue_member IS 'A person who works a queue, with personal capacity and skills, by version.';
COMMENT ON TABLE case_entry_exclusion IS 'An account at 90 days past due that an exclusion rule kept out of recovery on a business date.';
COMMENT ON TABLE outbox_delivery IS 'The delivery of one outbox event to one consumer, with its retries.';
COMMENT ON TABLE outbox_event IS 'An application event or outbound work request written in the same transaction as the change.';
COMMENT ON TABLE idempotency_key IS 'The stored response of an API request sent with an Idempotency-Key header, kept 24 hours.';
COMMENT ON TABLE processed_event IS 'An event or work key a consumer has already processed, so a repeat is ignored and counted.';
COMMENT ON TABLE lov_value IS 'A value in a list of values.';
COMMENT ON TABLE timer IS 'A running clock on a case: a service level, a legal period or an offer validity.';
COMMENT ON TABLE task IS 'A unit of work on a case: a CMMN human, customer, partner or decision task.';
COMMENT ON TABLE assignment IS 'Who holds a case or a task and from when.';
COMMENT ON TABLE queue IS 'A queue of work belonging to one team and one role.';
COMMENT ON TABLE case_party IS 'The role each party plays on a case.';
COMMENT ON TABLE case_account IS 'Links each loan account to the case it is recovered under.';
COMMENT ON TABLE recovery_case IS 'One recovery case per customer per product, from 90 days past due to close.';
COMMENT ON COLUMN recovery_case.id IS 'Record identifier of the case';
COMMENT ON COLUMN recovery_case.case_no IS 'Case number RW-YYYY-NNNNNN, issued at creation and never reused';
COMMENT ON COLUMN recovery_case.product_group IS 'Mortgage, hire purchase, SSME or unsecured';
COMMENT ON COLUMN recovery_case.primary_person_key IS 'The borrower the case is opened for';
COMMENT ON COLUMN recovery_case.status IS 'Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed';
COMMENT ON COLUMN recovery_case.stage_code IS 'The stage the case is on';
COMMENT ON COLUMN recovery_case.route_state IS 'The routing state from the rule set, for example FIRM_INSTRUCTED';
COMMENT ON COLUMN recovery_case.route_code IS 'The approved route R1 to R8';
COMMENT ON COLUMN recovery_case.owner_user_id IS 'The case owner';
COMMENT ON COLUMN recovery_case.queue_id IS 'The queue the case is in';
COMMENT ON COLUMN recovery_case.team_code IS 'The owning team, used by scope rules';
COMMENT ON COLUMN recovery_case.region_code IS 'The owning region, used by scope rules';
COMMENT ON COLUMN recovery_case.entry_date IS 'The date the case entered recovery';
COMMENT ON COLUMN recovery_case.dpd_at_entry IS 'Days past due on the entry date';
COMMENT ON COLUMN recovery_case.exposure_band IS 'Exposure band set from the outstanding balance at entry';
COMMENT ON COLUMN recovery_case.total_outstanding_at_entry IS 'Total outstanding across linked accounts at entry, in baht';
COMMENT ON COLUMN recovery_case.prescription_date IS 'The earliest date a legal claim on the case expires';
COMMENT ON COLUMN recovery_case.stage_clock_start IS 'When the current state started, for the service level';
COMMENT ON COLUMN recovery_case.deviation_open IS 'True while any deviation X1 to X7 is open';
COMMENT ON COLUMN recovery_case.legal_hold IS 'True while a legal hold stops normal routing';
COMMENT ON COLUMN recovery_case.rule_version IS 'The rule version the current state was entered under';
COMMENT ON COLUMN recovery_case.closed_date IS 'The date the case closed';
COMMENT ON COLUMN recovery_case.closure_reason IS 'Cured, settled, realized, sold, written off, insurance settled, merged, canceled';
COMMENT ON COLUMN recovery_case.plan_ref IS 'Reference of the ACE restructure plan on the case';
COMMENT ON COLUMN recovery_case.plan_status IS 'ACE plan status: created, approved, booked or broken';
COMMENT ON COLUMN recovery_case.plan_status_as_of IS 'Date of the plan status in ACE';
COMMENT ON COLUMN recovery_case.next_action_text IS 'The next action, copied from action_text of the rule that moved the case';
COMMENT ON COLUMN recovery_case.next_action_owner_role IS 'Owner role of the next action, from owner_role of the rule';
COMMENT ON COLUMN recovery_case.next_action_due_date IS 'Due date from the rule''s timer_spec or the service levels and timers table';
COMMENT ON COLUMN recovery_case.next_action_rule_id IS 'Rule ID that set the next action';
COMMENT ON COLUMN recovery_case.next_action_waiting IS 'True when the next action waits on a customer, party or partner';
COMMENT ON COLUMN recovery_case.last_allocation_date IS 'Business date of the last allocation run that decided the case';
COMMENT ON COLUMN recovery_case.status_before_hold IS 'The case status when a legal hold was placed, restored when it is lifted';
COMMENT ON COLUMN case_account.id IS 'Record identifier of the case account link';
COMMENT ON COLUMN case_account.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN case_account.account_key IS 'The loan_account this record belongs to';
COMMENT ON COLUMN case_account.is_primary IS 'True for the account the case was opened on';
COMMENT ON COLUMN case_account.linked_from IS 'Date the account joined the case';
COMMENT ON COLUMN case_account.linked_to IS 'Date the account left the case';
COMMENT ON COLUMN case_party.id IS 'Record identifier of the case party link';
COMMENT ON COLUMN case_party.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN case_party.person_key IS 'The party this record belongs to';
COMMENT ON COLUMN case_party.party_role IS 'Borrower, co-borrower, guarantor, authorized signatory, heir';
COMMENT ON COLUMN case_party.role_from IS 'Date the role starts';
COMMENT ON COLUMN case_party.role_to IS 'Date the role ends';
COMMENT ON COLUMN queue.id IS 'Record identifier of the queue';
COMMENT ON COLUMN queue.queue_code IS 'Queue code';
COMMENT ON COLUMN queue.queue_name IS 'Queue name';
COMMENT ON COLUMN queue.team_code IS 'Team the queue belongs to';
COMMENT ON COLUMN queue.role_code IS 'Role that works the queue';
COMMENT ON COLUMN queue.assignment_method IS 'Round robin, lowest load, named owner, skill';
COMMENT ON COLUMN queue.capacity_cap IS 'Most open cases one person may hold in the queue';
COMMENT ON COLUMN queue.overflow_queue_id IS 'Queue that receives overflow';
COMMENT ON COLUMN queue.rr_cursor_user_id IS 'The member last given a case by round robin in the queue';
COMMENT ON COLUMN queue.table_version IS 'The QUEUE reference version applied to the row';
COMMENT ON COLUMN assignment.id IS 'Record identifier of the assignment';
COMMENT ON COLUMN assignment.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN assignment.task_id IS 'The task this record belongs to';
COMMENT ON COLUMN assignment.assignee_user_id IS 'The person or service identity assigned';
COMMENT ON COLUMN assignment.assigned_at IS 'When assigned';
COMMENT ON COLUMN assignment.ended_at IS 'When the assignment ended';
COMMENT ON COLUMN assignment.reason IS 'Allocation, transfer, rebalance, manual, escalation';
COMMENT ON COLUMN assignment.rule_id IS 'The rule that made the assignment';
COMMENT ON COLUMN assignment.queue_id IS 'The queue the assignment placed the case in';
COMMENT ON COLUMN assignment.transfer_reason_code IS 'Coded reason for a manual transfer or move';
COMMENT ON COLUMN task.id IS 'Record identifier of the task';
COMMENT ON COLUMN task.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN task.task_code IS 'The task in the case model, for example VERIFY_PACK';
COMMENT ON COLUMN task.element_type IS 'Human, customer, partner or decision task, milestone, event listener';
COMMENT ON COLUMN task.discretion IS 'Automatic, discretionary, required';
COMMENT ON COLUMN task.status IS 'Open, in progress, done, canceled';
COMMENT ON COLUMN task.owner_role IS 'Role that owns the task';
COMMENT ON COLUMN task.due_at IS 'When the task is due';
COMMENT ON COLUMN task.completed_at IS 'When it completed';
COMMENT ON COLUMN task.outcome_code IS 'The event the task produced';
COMMENT ON COLUMN timer.id IS 'Record identifier of the timer';
COMMENT ON COLUMN timer.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN timer.task_id IS 'The task this record belongs to';
COMMENT ON COLUMN timer.timer_type IS 'Service level, notice period, cure period, prescription, hearing deadline, offer validity, holding age, claim deadline';
COMMENT ON COLUMN timer.started_at IS 'When it started';
COMMENT ON COLUMN timer.expires_at IS 'When it expires';
COMMENT ON COLUMN timer.warn_at IS 'When the warning is raised';
COMMENT ON COLUMN timer.paused IS 'True while paused by a deviation. A prescription timer never pauses';
COMMENT ON COLUMN timer.status IS 'Running, paused, expired, stopped';
COMMENT ON COLUMN timer.escalation_level IS 'How many times it has escalated';
COMMENT ON COLUMN timer.warned_at IS 'When the warning was sent, so it is sent once';
COMMENT ON COLUMN timer.treatment_id IS 'The treatment a plan timer belongs to';
COMMENT ON COLUMN timer.escalated_to_role IS 'Role the breach was last escalated to';
COMMENT ON COLUMN timer.escalated_at IS 'When the timer last escalated';
COMMENT ON COLUMN lov_value.id IS 'Record identifier of the list value';
COMMENT ON COLUMN lov_value.lov_code IS 'List code, for example LOV-ROUTE';
COMMENT ON COLUMN lov_value.value_code IS 'Value code';
COMMENT ON COLUMN lov_value.label_en IS 'English label';
COMMENT ON COLUMN lov_value.label_th IS 'Thai label';
COMMENT ON COLUMN lov_value.sort_order IS 'Display order';
COMMENT ON COLUMN lov_value.valid_from IS 'Valid from';
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
COMMENT ON COLUMN case_entry_exclusion.id IS 'Record identifier of the case entry exclusion';
COMMENT ON COLUMN case_entry_exclusion.account_key IS 'The account excluded; unique with business_date';
COMMENT ON COLUMN case_entry_exclusion.business_date IS 'Business date of the exclusion';
COMMENT ON COLUMN case_entry_exclusion.reason_code IS 'Deceased, fraud, bankruptcy, active plan or open dispute';
COMMENT ON COLUMN case_entry_exclusion.rule_id IS 'Exclusion rule that blocked the entry';
COMMENT ON COLUMN case_entry_exclusion.rule_version IS 'Version of that rule';
COMMENT ON COLUMN queue_member.id IS 'Record identifier of the queue member';
COMMENT ON COLUMN queue_member.queue_id IS 'The queue';
COMMENT ON COLUMN queue_member.user_id IS 'The person';
COMMENT ON COLUMN queue_member.capacity IS 'Most open cases the person may hold in the queue';
COMMENT ON COLUMN queue_member.skill_codes IS 'Skills of the person, comma separated';
COMMENT ON COLUMN queue_member.table_version IS 'QUEUE_MEMBER reference version the row belongs to';
COMMENT ON COLUMN queue_member.valid_from IS 'Date the row comes into force';
COMMENT ON COLUMN queue_member.valid_to IS 'Last date the row is in force';
COMMENT ON COLUMN queue_measure.id IS 'Record identifier of the queue measure';
COMMENT ON COLUMN queue_measure.queue_id IS 'The queue measured; unique with as_of';
COMMENT ON COLUMN queue_measure.as_of IS 'When the snapshot was taken';
COMMENT ON COLUMN queue_measure.depth IS 'Open cases in the queue';
COMMENT ON COLUMN queue_measure.unassigned IS 'Open cases with no owner';
COMMENT ON COLUMN queue_measure.avg_age_days IS 'Average age of the open cases, days';
COMMENT ON COLUMN queue_measure.max_age_days IS 'Age of the oldest open case, days';
COMMENT ON COLUMN queue_measure.owner_min IS 'Fewest open cases held by one owner';
COMMENT ON COLUMN queue_measure.owner_max IS 'Most open cases held by one owner';
COMMENT ON COLUMN queue_measure.breached IS 'Open cases past their service level';
COMMENT ON COLUMN queue_measure.status IS 'Taken, published or held';
COMMENT ON COLUMN parameter_catalog.id IS 'Record identifier of the parameter definition';
COMMENT ON COLUMN parameter_catalog.param_key IS 'Parameter key, for example case.entry.dpd';
COMMENT ON COLUMN parameter_catalog.kind IS 'Kind of parameter, for example ENVIRONMENT for an environment setting';
COMMENT ON COLUMN parameter_catalog.value_type IS 'Type of the value';
COMMENT ON COLUMN parameter_catalog.unit IS 'Unit, for example CALENDAR_DAYS, WORKING_DAYS, BAHT, PERCENT, COUNT, CODE_LIST';
COMMENT ON COLUMN parameter_catalog.min_value IS 'Lowest allowed value';
COMMENT ON COLUMN parameter_catalog.max_value IS 'Highest allowed value';
COMMENT ON COLUMN parameter_catalog.default_value IS 'Default value';
COMMENT ON COLUMN parameter_catalog.scope IS 'Product, when the parameter is keyed by product group, or global';
COMMENT ON COLUMN parameter_catalog.required IS 'True when every product in force must have a row';
COMMENT ON COLUMN parameter_catalog.owner_role IS 'Role that owns the parameter';
COMMENT ON COLUMN parameter_catalog.environments IS 'Environments the parameter is set in';
COMMENT ON COLUMN parameter_catalog.used_by IS 'Modules and stories that read the parameter';
COMMENT ON COLUMN parameter_catalog.secret IS 'True for a secret; its value is never returned';
COMMENT ON COLUMN parameter_catalog.description IS 'What the parameter controls';
COMMENT ON COLUMN parameter_value.id IS 'Record identifier of the parameter value';
COMMENT ON COLUMN parameter_value.param_key IS 'Parameter, from parameter_catalog';
COMMENT ON COLUMN parameter_value.environment IS 'DEV, SIT, UAT or PROD';
COMMENT ON COLUMN parameter_value.param_value IS 'Value as text';
COMMENT ON COLUMN parameter_value.product_group IS 'Product group for a product-scoped parameter';
COMMENT ON COLUMN parameter_value.version_no IS 'Version number';
COMMENT ON COLUMN parameter_value.valid_from IS 'Date the value comes into force';
COMMENT ON COLUMN parameter_value.valid_to IS 'Last date the value is in force';
COMMENT ON COLUMN parameter_value.status IS 'Validated, approved, in force, superseded, rolled back or refused';
COMMENT ON COLUMN parameter_value.author_user_id IS 'Who loaded the value';
COMMENT ON COLUMN parameter_value.approver_user_id IS 'Who approved the value; never the author';
COMMENT ON COLUMN parameter_value.approved_at IS 'When the value was approved';
COMMENT ON COLUMN reference_version.id IS 'Record identifier of the reference version';
COMMENT ON COLUMN reference_version.table_code IS 'The reference or rule table the version belongs to, for example EXPOSURE_BAND or ALLOCATION';
COMMENT ON COLUMN reference_version.version_no IS 'Version number, one above the previous version of the table';
COMMENT ON COLUMN reference_version.version_label IS 'Version label the rows carry, for example DOCTYPE-2026.11';
COMMENT ON COLUMN reference_version.valid_from IS 'Date the version comes into force';
COMMENT ON COLUMN reference_version.valid_to IS 'Last date the version is in force; set when the next version is approved';
COMMENT ON COLUMN reference_version.status IS 'Validated, approved, in force, superseded, rolled back or refused';
COMMENT ON COLUMN reference_version.author_user_id IS 'Who loaded the version';
COMMENT ON COLUMN reference_version.approver_user_id IS 'Who approved the version; never the author';
COMMENT ON COLUMN reference_version.approved_at IS 'When the version was approved';
COMMENT ON COLUMN reference_version.row_count IS 'Rows in the version';
COMMENT ON COLUMN reference_version.content_hash IS 'SHA-256 of the rows sorted by key; used for idempotency';
COMMENT ON COLUMN reference_version.load_id IS 'Identifier of the reference load request that created the version';
COMMENT ON COLUMN reference_version.dry_run_counts IS 'Counts of live cases each changed rule row would move, from the dry run';
COMMENT ON COLUMN reference_version.rollback_reason IS 'Reason given for a rollback';
COMMENT ON COLUMN reference_version.change_request_ref IS 'Reference of the change request in the bank''s request tool';
COMMENT ON COLUMN reference_version.impact_summary IS 'What the change affects, for example the open cases it touches';
COMMENT ON COLUMN reference_version.test_result IS 'Passed or failed, from the load checks or the rule table test harness';
COMMENT ON COLUMN reference_version.rollback_plan IS 'How to return to the previous version';
COMMENT ON COLUMN reference_version.verified_by IS 'Who verified the change after it took effect';
COMMENT ON COLUMN reference_version.verified_at IS 'When the change was verified';
COMMENT ON COLUMN reference_version.verify_note IS 'What was checked';
COMMENT ON COLUMN reference_row.id IS 'Record identifier of the reference row';
COMMENT ON COLUMN reference_row.version_id IS 'The reference version the row belongs to; unique with row_key';
COMMENT ON COLUMN reference_row.row_key IS 'Key of the row inside its table';
COMMENT ON COLUMN reference_row.row_data IS 'Column values of the row';

-- ---------------------------------------------------------------------------
-- Seed and dictionary rows
-- ---------------------------------------------------------------------------

-- Seed: closed lists of values. Thai labels are added when approved (DL10)
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT', 'MORTGAGE', 'Mortgage', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT', 'HIRE_PURCHASE', 'Hire purchase', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT', 'SSME', 'SSME', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT', 'UNSECURED', 'Unsecured', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'NEW', 'New', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'ASSIGNED', 'Assigned', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'IN_PROGRESS', 'In progress', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'WAITING_CUSTOMER', 'Waiting customer', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'WAITING_PARTNER', 'Waiting partner', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'WAITING_APPROVAL', 'Waiting approval', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'ON_HOLD', 'On hold', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CASE-STATUS', 'CLOSED', 'Closed', 8, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-STAGE', 'RESTRUCTURE', 'Restructure', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-STAGE', 'SETTLEMENT', 'Settlement', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-STAGE', 'DEED_IN_LIEU', 'Deed in lieu', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-STAGE', 'GUARANTEE_CLAIM', 'Guarantee claim', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-STAGE', 'LITIGATION', 'Litigation', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-STAGE', 'ASSET_DISPOSAL', 'Asset disposal', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-STAGE', 'DEBT_SALE', 'Debt sale', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-STAGE', 'WRITE_OFF', 'Write-off', 8, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-STAGE', 'DEVIATIONS', 'Deviations', 9, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE', 'R1', 'Restructure', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE', 'R2', 'Settlement', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE', 'R3', 'Deed in lieu', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE', 'R4', 'Guarantee claim', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE', 'R5', 'Litigation', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE', 'R6', 'Asset disposal', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE', 'R7', 'Debt sale', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE', 'R8', 'Write-off', 8, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLOSURE', 'CURED', 'Cured', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLOSURE', 'SETTLED', 'Settled', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLOSURE', 'REALIZED', 'Realized', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLOSURE', 'SOLD', 'Sold', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLOSURE', 'WRITTEN_OFF', 'Written off', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLOSURE', 'INSURANCE_SETTLED', 'Insurance settled', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLOSURE', 'MERGED', 'Merged', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLOSURE', 'CANCELED', 'Canceled', 8, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTY-ROLE', 'BORROWER', 'Borrower', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTY-ROLE', 'CO_BORROWER', 'Co-borrower', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTY-ROLE', 'GUARANTOR', 'Guarantor', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTY-ROLE', 'AUTHORIZED_SIGNATORY', 'Authorized signatory', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTY-ROLE', 'HEIR', 'Heir', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DEVIATION', 'X1', 'Dispute or complaint', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DEVIATION', 'X2', 'Vulnerable customer or hardship', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DEVIATION', 'X3', 'Deceased customer', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DEVIATION', 'X4', 'Fraud', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DEVIATION', 'X5', 'Bankruptcy or external seizure', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DEVIATION', 'X6', 'Lost contact', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DEVIATION', 'X7', 'Collateral event', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DEV-OUTCOME', 'RETURNED', 'Returned', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DEV-OUTCOME', 'RE_ROUTED', 'Re-routed', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DEV-OUTCOME', 'CASE_ENDED', 'Case ended', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RAISED-BY', 'SCREENING_AGENT', 'Screening agent', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RAISED-BY', 'RULE', 'Rule', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RAISED-BY', 'OFFICER', 'Officer', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RAISED-BY', 'CUSTOMER_CONTACT', 'Customer contact', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSIGN', 'ROUND_ROBIN', 'Round robin', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSIGN', 'LOWEST_LOAD', 'Lowest load', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSIGN', 'NAMED_OWNER', 'Named owner', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSIGN', 'SKILL', 'Skill', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSIGN-REASON', 'ALLOCATION', 'Allocation', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSIGN-REASON', 'TRANSFER', 'Transfer', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSIGN-REASON', 'REBALANCE', 'Rebalance', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSIGN-REASON', 'MANUAL', 'Manual', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSIGN-REASON', 'ESCALATION', 'Escalation', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ELEMENT', 'HUMAN_TASK', 'Human task', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ELEMENT', 'CUSTOMER_TASK', 'Customer task', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ELEMENT', 'PARTNER_TASK', 'Partner task', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ELEMENT', 'DECISION_TASK', 'Decision task', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ELEMENT', 'STAGE_ENTRY', 'Stage entry', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ELEMENT', 'MILESTONE', 'Milestone', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ELEMENT', 'EVENT_LISTENER', 'Event listener', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DISCRETION', 'AUTOMATIC', 'Automatic', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DISCRETION', 'DISCRETIONARY', 'Discretionary', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DISCRETION', 'REQUIRED', 'Required', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TASK-STATUS', 'OPEN', 'Open', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TASK-STATUS', 'IN_PROGRESS', 'In progress', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TASK-STATUS', 'DONE', 'Done', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TASK-STATUS', 'CANCELED', 'Canceled', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TIMER', 'SERVICE_LEVEL', 'Service level', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TIMER', 'NOTICE_PERIOD', 'Notice period', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TIMER', 'CURE_PERIOD', 'Cure period', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TIMER', 'PRESCRIPTION', 'Prescription', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TIMER', 'HEARING_DEADLINE', 'Hearing deadline', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TIMER', 'OFFER_VALIDITY', 'Offer validity', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TIMER', 'HOLDING_AGE', 'Holding age', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TIMER', 'CLAIM_DEADLINE', 'Claim deadline', 8, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TIMER', 'INSTALLMENT_DUE', 'Installment due', 9, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TIMER-STATUS', 'RUNNING', 'Running', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TIMER-STATUS', 'PAUSED', 'Paused', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TIMER-STATUS', 'EXPIRED', 'Expired', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TIMER-STATUS', 'STOPPED', 'Stopped', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTY-TYPE', 'INDIVIDUAL', 'Individual', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTY-TYPE', 'JURISTIC_PERSON', 'Juristic person', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ID-TYPE', 'THAI_NATIONAL_ID', 'Thai national ID', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ID-TYPE', 'PASSPORT', 'Passport', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ID-TYPE', 'COMPANY_REGISTRATION', 'Company registration', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SEGMENT', 'RETAIL', 'Retail', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SEGMENT', 'SSME', 'SSME', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SEGMENT', 'CORPORATE', 'Corporate', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CHANNEL', 'MOBILE', 'Mobile', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CHANNEL', 'HOME_PHONE', 'Home phone', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CHANNEL', 'WORK_PHONE', 'Work phone', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CHANNEL', 'LINE', 'LINE', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CHANNEL', 'EMAIL', 'Email', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CHANNEL', 'POSTAL_ADDRESS', 'Postal address', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CHANNEL', 'CALL', 'Call', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CHANNEL', 'VISIT', 'Visit', 8, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CHANNEL', 'SMS', 'SMS', 9, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CHANNEL', 'LETTER', 'Letter', 10, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CHANNEL', 'PORTAL', 'Portal', 11, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CHANNEL', 'BRANCH', 'Branch', 12, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONTACT-SRC', 'BANK_RECORD', 'Bank record', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONTACT-SRC', 'FIELD_VISIT', 'Field visit', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONTACT-SRC', 'AGENCY', 'Agency', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONTACT-SRC', 'BUREAU_TRACE', 'Bureau trace', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONTACT-SRC', 'CUSTOMER', 'Customer', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONSENT', 'GIVEN', 'Given', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONSENT', 'WITHDRAWN', 'Withdrawn', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONSENT', 'UNKNOWN', 'Unknown', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-COLL-TYPE', 'LAND', 'Land', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-COLL-TYPE', 'HOUSE', 'House', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-COLL-TYPE', 'CONDOMINIUM', 'Condominium', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-COLL-TYPE', 'VEHICLE', 'Vehicle', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-COLL-TYPE', 'DEPOSIT', 'Deposit', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-COLL-TYPE', 'OTHER', 'Other', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OCCUPANCY', 'OWNER', 'Owner', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OCCUPANCY', 'TENANT', 'Tenant', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OCCUPANCY', 'VACANT', 'Vacant', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OCCUPANCY', 'UNKNOWN', 'Unknown', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ENCUMBRANCE', 'CLEAR', 'Clear', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ENCUMBRANCE', 'OTHER_CREDITOR', 'Other creditor', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ENCUMBRANCE', 'SEIZED', 'Seized', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ENCUMBRANCE', 'UNDER_DISPUTE', 'Under dispute', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPRAISAL', 'MARKET', 'Market', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPRAISAL', 'OFFICIAL', 'Official', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPRAISAL', 'FORCED_SALE', 'Forced sale', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPRAISAL', 'DESKTOP', 'Desktop', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPRAISAL', 'AGENT_ESTIMATE', 'Agent estimate', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSET-TYPE', 'DETACHED_HOUSE', 'Detached house', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSET-TYPE', 'TOWNHOUSE', 'Townhouse', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSET-TYPE', 'CONDOMINIUM', 'Condominium', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSET-TYPE', 'LAND', 'Land', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSET-TYPE', 'COMMERCIAL_BUILDING', 'Commercial building', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ASSET-TYPE', 'VEHICLE', 'Vehicle', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRANSFER-IN', 'AUCTION_PURCHASE', 'Auction purchase', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRANSFER-IN', 'DEED_IN_LIEU', 'Deed in lieu', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRANSFER-IN', 'REPOSSESSION', 'Repossession', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-HOLDING', 'HELD', 'Held', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-HOLDING', 'LISTED', 'Listed', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-HOLDING', 'UNDER_OFFER', 'Under offer', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-HOLDING', 'SOLD', 'Sold', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-HOLDING', 'TRANSFERRED', 'Transferred', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-HOLDING', 'RENTED', 'Rented', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TREATMENT', 'RESTRUCTURE', 'Restructure', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TREATMENT', 'SETTLEMENT', 'Settlement', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TREATMENT', 'DEED_IN_LIEU', 'Deed in lieu', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TREATMENT', 'BUY_BACK', 'Buy-back', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TREATMENT', 'GUARANTEE_CLAIM', 'Guarantee claim', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TREATMENT', 'REPOSSESSION', 'Repossession', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TREATMENT', 'AUCTION', 'Auction', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TREATMENT', 'DEBT_SALE', 'Debt sale', 8, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TREATMENT', 'WRITE_OFF', 'Write-off', 9, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TREATMENT', 'RAMC_TRANSFER', 'RAMC transfer', 10, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TREATMENT', 'RENTAL', 'Rental', 11, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PROPOSER', 'AGENT', 'Agent', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PROPOSER', 'RULE', 'Rule', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PROPOSER', 'PERSON', 'Person', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPROVAL-LEVEL', 'L1', 'Board of Directors', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPROVAL-LEVEL', 'L2', 'Executive Committee', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPROVAL-LEVEL', 'L3', 'Problem Asset Resolution Committee or Management Committee', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPROVAL-LEVEL', 'L4', 'Head of Recovery, function level, or Problem Asset Resolution Committee', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPROVAL-LEVEL', 'L5', 'Recovery executive, division level', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPROVAL-LEVEL', 'L6', 'Recovery executive, department level', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRT-OUTCOME', 'KEPT', 'Kept', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRT-OUTCOME', 'BROKEN', 'Broken', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRT-OUTCOME', 'COMPLETED', 'Completed', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRT-OUTCOME', 'CANCELED', 'Canceled', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRT-OUTCOME', 'DECLINED', 'Declined', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLAIM-TYPE', 'TCG', 'TCG', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLAIM-TYPE', 'CREDIT_LIFE_INSURANCE', 'Credit life insurance', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLAIM-TYPE', 'MORTGAGE_INSURANCE', 'Mortgage insurance', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLAIM-TYPE', 'COLLATERAL_INSURANCE', 'Collateral insurance', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLAIM-STATUS', 'PREPARING', 'Preparing', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLAIM-STATUS', 'FILED', 'Filed', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLAIM-STATUS', 'DEFECT', 'Defect', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLAIM-STATUS', 'PAID', 'Paid', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CLAIM-STATUS', 'REJECTED', 'Rejected', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEGAL-TYPE', 'NOTICE', 'Notice', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEGAL-TYPE', 'CIVIL_CASE', 'Civil case', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEGAL-TYPE', 'APPEAL', 'Appeal', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEGAL-TYPE', 'ENFORCEMENT', 'Enforcement', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEGAL-TYPE', 'BANKRUPTCY_PETITION', 'Bankruptcy petition', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEGAL-TYPE', 'LED_AUCTION', 'LED auction', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEGAL-STATUS', 'OPEN', 'Open', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEGAL-STATUS', 'FILED', 'Filed', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEGAL-STATUS', 'JUDGMENT', 'Judgment', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEGAL-STATUS', 'ENFORCING', 'Enforcing', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEGAL-STATUS', 'CLOSED', 'Closed', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEGAL-STATUS', 'WITHDRAWN', 'Withdrawn', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-NOTICE', 'DEMAND', 'Demand', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-NOTICE', 'RECALL', 'Recall', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-NOTICE', 'STATUTORY_SALE_NOTICE', 'Statutory sale notice', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-NOTICE', 'GUARANTOR_NOTICE', 'Guarantor notice', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DELIVERY', 'DELIVERED', 'Delivered', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DELIVERY', 'REFUSED', 'Refused', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DELIVERY', 'UNDELIVERABLE', 'Undeliverable', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DELIVERY', 'PENDING', 'Pending', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SENT-TYPE', 'BEFORE_NPL', 'Before NPL', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SENT-TYPE', 'NPL', 'NPL', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-HEARING', 'FIRST_HEARING', 'First hearing', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-HEARING', 'WITNESS', 'Witness', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-HEARING', 'JUDGMENT_READING', 'Judgment reading', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-HEARING', 'MEDIATION', 'Mediation', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-HEARING-OUTCOME', 'HELD', 'Held', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-HEARING-OUTCOME', 'ADJOURNED', 'Adjourned', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-HEARING-OUTCOME', 'SETTLED', 'Settled', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-HEARING-OUTCOME', 'JUDGMENT', 'Judgment', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTNER-TYPE', 'AGENCY', 'Agency', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTNER-TYPE', 'LAW_FIRM', 'Law firm', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTNER-TYPE', 'VALUER', 'Valuer', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTNER-TYPE', 'AUCTION_VENDOR', 'Auction vendor', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTNER-TYPE', 'BROKER', 'Broker', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTNER-TYPE', 'DEBT_BUYER', 'Debt buyer', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTNER-TYPE', 'AMC', 'AMC', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARTNER-TYPE', 'RAMC', 'RAMC', 8, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PANEL', 'ACTIVE', 'Active', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PANEL', 'ON_NOTICE', 'On notice', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PANEL', 'SUSPENDED', 'Suspended', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PANEL', 'EXITED', 'Exited', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INSTRUCTION', 'COLLECT', 'Collect', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INSTRUCTION', 'FILE_SUIT', 'File suit', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INSTRUCTION', 'ENFORCE', 'Enforce', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INSTRUCTION', 'APPRAISE', 'Appraise', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INSTRUCTION', 'REPOSSESS', 'Repossess', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INSTRUCTION', 'LIST', 'List', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INSTRUCTION', 'SELL', 'Sell', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INSTR-STATUS', 'SENT', 'Sent', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INSTR-STATUS', 'ACCEPTED', 'Accepted', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INSTR-STATUS', 'DECLINED', 'Declined', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INSTR-STATUS', 'IN_PROGRESS', 'In progress', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INSTR-STATUS', 'DONE', 'Done', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INSTR-STATUS', 'RECALLED', 'Recalled', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SALE-CHANNEL', 'DUTCH_AUCTION', 'Dutch auction', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SALE-CHANNEL', 'BROKER', 'Broker', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SALE-CHANNEL', 'DIRECT', 'Direct', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SALE-CHANNEL', 'LED_AUCTION', 'LED auction', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SALE-CHANNEL', 'RAMC', 'RAMC', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LISTING', 'DRAFT', 'Draft', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LISTING', 'LIVE', 'Live', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LISTING', 'UNDER_OFFER', 'Under offer', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LISTING', 'SOLD', 'Sold', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LISTING', 'WITHDRAWN', 'Withdrawn', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-BUYER-CLASS', 'AMC', 'AMC', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-BUYER-CLASS', 'NON_AMC', 'Non-AMC', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LOT-STATUS', 'BUILDING', 'Building', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LOT-STATUS', 'OFFERED', 'Offered', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LOT-STATUS', 'AWARDED', 'Awarded', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LOT-STATUS', 'TRANSFERRED', 'Transferred', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LOT-STATUS', 'CLOSED', 'Closed', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PUTBACK', 'NONE', 'None', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PUTBACK', 'CLAIMED', 'Claimed', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PUTBACK', 'ACCEPTED', 'Accepted', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PUTBACK', 'REJECTED', 'Rejected', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DIRECTION', 'INBOUND', 'Inbound', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DIRECTION', 'OUTBOUND', 'Outbound', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONTACT-RESULT', 'RIGHT_PARTY', 'Right party', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONTACT-RESULT', 'THIRD_PARTY', 'Third party', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONTACT-RESULT', 'NO_ANSWER', 'No answer', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONTACT-RESULT', 'WRONG_NUMBER', 'Wrong number', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONTACT-RESULT', 'REFUSED', 'Refused', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONDUCT', 'PASSED', 'Passed', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONDUCT', 'BLOCKED', 'Blocked', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONDUCT', 'NOT_APPLICABLE', 'Not applicable', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SOURCE', 'EFS', 'EFS', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SOURCE', 'WORKBENCH', 'Workbench', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DOC-SOURCE', 'SCAN', 'Scan', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DOC-SOURCE', 'UPLOAD', 'Upload', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DOC-SOURCE', 'GENERATED', 'Generated', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DOC-SOURCE', 'PARTNER', 'Partner', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DOC-SOURCE', 'EMAIL', 'Email', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REVIEW', 'NOT_NEEDED', 'Not needed', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REVIEW', 'PENDING', 'Pending', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REVIEW', 'CONFIRMED', 'Confirmed', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REVIEW', 'CORRECTED', 'Corrected', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CUSTODY', 'VAULT', 'Vault', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CUSTODY', 'BRANCH', 'Branch', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CUSTODY', 'POST', 'Post', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CUSTODY', 'LAWYER', 'Lawyer', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CUSTODY', 'COURT', 'Court', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CUSTODY', 'LAND_OFFICE', 'Land office', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PROCEEDS-SRC', 'CUSTOMER', 'Customer', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PROCEEDS-SRC', 'LED', 'LED', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PROCEEDS-SRC', 'AUCTION', 'Auction', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PROCEEDS-SRC', 'BUYER', 'Buyer', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PROCEEDS-SRC', 'AGENCY', 'Agency', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PROCEEDS-SRC', 'INSURER', 'Insurer', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PROCEEDS-SRC', 'GUARANTOR', 'Guarantor', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MATCH', 'INSTALLMENT', 'Installment', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MATCH', 'SETTLEMENT', 'Settlement', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MATCH', 'FEE', 'Fee', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MATCH', 'SALE_PROCEEDS', 'Sale proceeds', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MATCH', 'UNMATCHED', 'Unmatched', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE-SET', 'RESTRUCTURE', 'Restructure', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE-SET', 'SETTLEMENT', 'Settlement', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE-SET', 'DEED_IN_LIEU', 'Deed in lieu', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE-SET', 'GUARANTEE_CLAIM', 'Guarantee claim', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE-SET', 'LITIGATION', 'Litigation', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE-SET', 'ASSET_DISPOSAL', 'Asset disposal', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE-SET', 'DEBT_SALE', 'Debt sale', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE-SET', 'WRITE_OFF', 'Write-off', 8, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE-SET', 'DEVIATIONS', 'Deviations', 9, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROUTE-SET', 'UNIVERSAL_RULES', 'Universal rules', 10, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROLE-CLASS', 'BANK_USER', 'Bank user', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROLE-CLASS', 'PARTNER_USER', 'Partner user', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ROLE-CLASS', 'NON_HUMAN_ACTOR', 'Non-human actor', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SCOPE', 'OWN', 'Own', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SCOPE', 'TEAM', 'Team', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SCOPE', 'REGION', 'Region', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SCOPE', 'ALL', 'All', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPABILITY', 'CASE_RECORD', 'Case record', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPABILITY', 'QUEUE_AND_ALLOCATION', 'Queue and allocation', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPABILITY', 'TREATMENT_AND_OFFER', 'Treatment and offer', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPABILITY', 'LITIGATION', 'Litigation', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPABILITY', 'ASSET_AND_DISPOSAL', 'Asset and disposal', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPABILITY', 'DEBT_SALE', 'Debt sale', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPABILITY', 'WRITE_OFF_AND_POSTING', 'Write-off and posting', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPABILITY', 'DOCUMENTS', 'Documents', 8, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPABILITY', 'RULES_AND_PARAMETERS', 'Rules and parameters', 9, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPABILITY', 'REFERENCE_DATA', 'Reference data', 10, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPABILITY', 'DECISION_LOG', 'Decision log', 11, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPABILITY', 'PARTNER_PORTAL', 'Partner portal', 12, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPABILITY', 'REPORTING', 'Reporting', 13, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPABILITY', 'PLATFORM_ADMINISTRATION', 'Platform administration', 14, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LANG', 'TH', 'TH', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LANG', 'EN', 'EN', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DATA-PRODUCT', 'DP01', 'Account and arrears', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DATA-PRODUCT', 'DP02', 'Customer and party', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DATA-PRODUCT', 'DP03', 'Case and ownership', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DATA-PRODUCT', 'DP04', 'Treatment and offers', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DATA-PRODUCT', 'DP05', 'Contact and promises', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DATA-PRODUCT', 'DP06', 'Collateral and assets', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DATA-PRODUCT', 'DP07', 'Legal events and cases', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DATA-PRODUCT', 'DP08', 'Partner performance', 8, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DATA-PRODUCT', 'DP09', 'Debt sale', 9, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DATA-PRODUCT', 'DP10', 'Documents and extracted fields', 10, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DATA-PRODUCT', 'DP11', 'Scores and route economics', 11, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DATA-PRODUCT', 'DP12', 'Decision log', 12, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DATA-PRODUCT', 'DP13', 'Money and closure', 13, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DATA-PRODUCT', 'DP14', 'Reference data', 14, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REFRESH', 'DAILY', 'Daily', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REFRESH', 'WEEKLY', 'Weekly', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REFRESH', 'MONTHLY', 'Monthly', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REFRESH', 'ON_CHANGE', 'On change', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-FRESHNESS', 'LOADED', 'Loaded', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-FRESHNESS', 'STALE', 'Stale', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONTRACT-STATUS', 'DRAFT', 'Draft', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONTRACT-STATUS', 'PUBLISHED', 'Published', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONTRACT-STATUS', 'SUPERSEDED', 'Superseded', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LOAD-STATUS', 'RUNNING', 'Running', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LOAD-STATUS', 'COMPLETED', 'Completed', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LOAD-STATUS', 'REFUSED', 'Refused', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LOAD-STATUS', 'LATE', 'Late', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LOAD-STATUS', 'FAILED', 'Failed', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LOAD-STATUS', 'SUPERSEDED', 'Superseded', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DQ-STATUS', 'OPEN', 'Open', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DQ-STATUS', 'CLEARED', 'Cleared', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DQ-RULE-TYPE', 'NOT_NULL', 'Not null', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DQ-RULE-TYPE', 'UNIQUE_ACROSS', 'Unique across', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DQ-RULE-TYPE', 'RANGE', 'Range', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DQ-RULE-TYPE', 'SUM_EQUALS', 'Sum equals', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DQ-RULE-TYPE', 'EXISTS_LINK', 'Exists link', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DQ-RULE-TYPE', 'MAX_AGE_DAYS', 'Max age days', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-DQ-RULE-TYPE', 'FIELD_BEFORE', 'Field before', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRACKER-LOCATION', 'EXCEL', 'Excel', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRACKER-LOCATION', 'SHAREPOINT', 'SharePoint', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRACKER-LOCATION', 'LOCAL_FILE', 'Local file', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRACKER-LOCATION', 'NONE', 'None', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-UPDATE-CYCLE', 'DAILY', 'Daily', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-UPDATE-CYCLE', 'WEEKLY', 'Weekly', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-UPDATE-CYCLE', 'MONTHLY', 'Monthly', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-UPDATE-CYCLE', 'AD_HOC', 'Ad hoc', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRACKER-DECISION', 'LOAD', 'Load', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRACKER-DECISION', 'RETIRE', 'Retire', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRACKER-DECISION', 'KEEP', 'Keep', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRACKER-STATUS', 'LISTED', 'Listed', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRACKER-STATUS', 'LOADED', 'Loaded', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRACKER-STATUS', 'SIGNED_OFF', 'Signed off', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRACKER-STATUS', 'RETIRED', 'Retired', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRACKER-STATUS', 'KEPT', 'Kept', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PUBLISH-STATUS', 'PENDING', 'Pending', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PUBLISH-STATUS', 'HELD', 'Held', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PUBLISH-STATUS', 'RELEASED', 'Released', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REC-RESULT', 'PASS', 'Pass', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REC-RESULT', 'BREAK', 'Break', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RETENTION-END', 'ARCHIVE', 'Archive', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RETENTION-END', 'REVIEW', 'Review', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRANSPORT', 'SFTP', 'SFTP', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRANSPORT', 'COLLINS', 'COLLINS', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTERFACE-RUN', 'RECEIVED', 'Received', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTERFACE-RUN', 'LOADED', 'Loaded', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTERFACE-RUN', 'REFUSED', 'Refused', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTERFACE-RUN', 'MISSING', 'Missing', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTERFACE-RUN', 'DUPLICATE', 'Duplicate', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTERFACE-RUN', 'FAILED', 'Failed', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OUTBOUND-STATUS', 'PENDING', 'Pending', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OUTBOUND-STATUS', 'SENT', 'Sent', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OUTBOUND-STATUS', 'RETRY', 'Retry', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OUTBOUND-STATUS', 'EXCEPTION', 'Exception', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OUTBOUND-STATUS', 'ACKNOWLEDGED', 'Acknowledged', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OUTBOX-DELIVERY', 'PENDING', 'Pending', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OUTBOX-DELIVERY', 'RETRYING', 'Retrying', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OUTBOX-DELIVERY', 'DELIVERED', 'Delivered', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OUTBOX-DELIVERY', 'EXCEPTION', 'Exception', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ENVIRONMENT', 'DEV', 'DEV', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ENVIRONMENT', 'SIT', 'SIT', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ENVIRONMENT', 'UAT', 'UAT', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ENVIRONMENT', 'PROD', 'PROD', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT-STATUS', 'ACTIVE', 'Active', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT-STATUS', 'DELINQUENT', 'Delinquent', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT-STATUS', 'CLOSED', 'Closed', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PRODUCT-STATUS', 'WRITTEN_OFF', 'Written off', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EXCLUSION-REASON', 'DECEASED', 'Deceased', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EXCLUSION-REASON', 'FRAUD', 'Fraud', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EXCLUSION-REASON', 'BANKRUPTCY', 'Bankruptcy', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EXCLUSION-REASON', 'ACTIVE_PLAN', 'Active plan', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EXCLUSION-REASON', 'OPEN_DISPUTE', 'Open dispute', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SNAPSHOT-STATUS', 'TAKEN', 'Taken', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SNAPSHOT-STATUS', 'PUBLISHED', 'Published', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SNAPSHOT-STATUS', 'HELD', 'Held', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARAM-SCOPE', 'PRODUCT', 'Product', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PARAM-SCOPE', 'GLOBAL', 'Global', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-VERSION-STATUS', 'VALIDATED', 'Validated', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-VERSION-STATUS', 'APPROVED', 'Approved', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-VERSION-STATUS', 'IN_FORCE', 'In force', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-VERSION-STATUS', 'SUPERSEDED', 'Superseded', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-VERSION-STATUS', 'ROLLED_BACK', 'Rolled back', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-VERSION-STATUS', 'REFUSED', 'Refused', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TEST-RESULT', 'PASSED', 'Passed', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TEST-RESULT', 'FAILED', 'Failed', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'PRODUCT', 'Product', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'REGION', 'Region', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'EXPOSURE_BAND', 'Exposure band', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'ROLE', 'Role', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'TEAM', 'Team', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'QUEUE', 'Queue', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'QUEUE_MEMBER', 'Queue member', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'SERVICE_LEVEL', 'Service level', 8, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'DOCUMENT_TYPE', 'Document type', 9, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'DOCUMENT_CHECKLIST', 'Document checklist', 10, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'RETENTION_CLASS', 'Retention class', 11, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'TEMPLATE', 'Template', 12, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'DELEGATION_LIMIT', 'Delegation limit', 13, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'PERMISSION', 'Permission', 14, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'MASKING_RULE', 'Masking rule', 15, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'PARTNER_USER', 'Partner user', 16, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'LEGAL_PERIOD', 'Legal period', 17, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'HOLIDAY', 'Holiday', 18, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'PRODUCT_PARAMETER', 'Product parameter', 19, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'PARAMETER', 'Parameter', 20, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'ENTRY', 'Entry', 21, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'EXCLUSION', 'Exclusion', 22, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'ALLOCATION', 'Allocation', 23, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'ASSIGNMENT', 'Assignment', 24, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-REF-TABLE', 'TRANSFER', 'Transfer', 25, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RULE-TABLE', 'ENTRY', 'Entry', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RULE-TABLE', 'EXCLUSION', 'Exclusion', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RULE-TABLE', 'ALLOCATION', 'Allocation', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RULE-TABLE', 'ASSIGNMENT', 'Assignment', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RULE-TABLE', 'TRANSFER', 'Transfer', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRANSFER-REASON', 'R01', 'Capacity', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRANSFER-REASON', 'R02', 'Customer deceased', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRANSFER-REASON', 'R03', 'Skill', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRANSFER-REASON', 'R04', 'Owner absent', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRANSFER-REASON', 'R05', 'Legal referral', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRANSFER-REASON', 'R06', 'Wrong queue', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PLAN-STATUS', 'CREATED', 'Created', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PLAN-STATUS', 'APPROVED', 'Approved', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PLAN-STATUS', 'BOOKED', 'Booked', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-PLAN-STATUS', 'BROKEN', 'Broken', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEDGER-EVENT', 'CONTACT', 'Contact', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEDGER-EVENT', 'LETTER', 'Letter', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEDGER-EVENT', 'PROMISE', 'Promise', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEDGER-EVENT', 'PAYMENT', 'Payment', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEDGER-EVENT', 'HANDOVER', 'Handover', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEDGER-EVENT', 'CASE_CREATED', 'Case created', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEDGER-EVENT', 'CASE_ALLOCATED', 'Case allocated', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEDGER-EVENT', 'CASE_TRANSFERRED', 'Case transferred', 8, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEDGER-EVENT', 'CASE_ESCALATED', 'Case escalated', 9, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEDGER-EVENT', 'DOCUMENT_ATTACHED', 'Document attached', 10, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEDGER-EVENT', 'DECISION_TAKEN', 'Decision taken', 11, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEDGER-EVENT', 'CORRECTION', 'Correction', 12, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEDGER-EVENT', 'PARTNER_RESULT', 'Partner result', 13, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-LEDGER-EVENT', 'OFFER', 'Offer', 14, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ACTOR-TYPE', 'USER', 'User', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ACTOR-TYPE', 'SERVICE', 'Service', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-ACTOR-TYPE', 'PARTNER', 'Partner', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SEND-STATUS', 'SENT', 'Sent', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SEND-STATUS', 'DELIVERED', 'Delivered', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SEND-STATUS', 'READ', 'Read', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SEND-STATUS', 'FAILED', 'Failed', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPTURE-KIND', 'PHOTO', 'Photo', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPTURE-KIND', 'BILL', 'Bill', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CAPTURE-KIND', 'CHECKLIST', 'Checklist', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SCAN-RESULT', 'CLEAN', 'Clean', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SCAN-RESULT', 'INFECTED', 'Infected', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OCR-STATUS', 'PENDING', 'Pending', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OCR-STATUS', 'DONE', 'Done', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OCR-STATUS', 'RESCAN', 'Rescan', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-OCR-STATUS', 'FAILED', 'Failed', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTAKE-MATCH', 'PENDING', 'Pending', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTAKE-MATCH', 'MATCHED', 'Matched', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTAKE-MATCH', 'NO_MATCH', 'No match', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTAKE-MATCH', 'MULTIPLE', 'Multiple', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTAKE-MATCH', 'CONFLICT', 'Conflict', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTAKE-MATCH', 'CASE_CLOSED', 'Case closed', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTAKE-MATCH', 'NO_TYPE', 'No type', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EXTRACT-STATUS', 'PENDING', 'Pending', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EXTRACT-STATUS', 'DONE', 'Done', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EXTRACT-STATUS', 'FAILED', 'Failed', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTAKE-REVIEW', 'RESCAN', 'Rescan', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTAKE-REVIEW', 'UNREADABLE_FILE', 'Unreadable file', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTAKE-REVIEW', 'LOW_CONFIDENCE', 'Low confidence', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTAKE-REVIEW', 'MODEL_UNAVAILABLE', 'Model unavailable', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTAKE-REVIEW', 'UNKNOWN_TYPE', 'Unknown type', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTAKE-OUTCOME', 'ATTACHED', 'Attached', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-INTAKE-OUTCOME', 'DISCARDED', 'Discarded', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RETENTION-ACTION', 'ARCHIVED', 'Archived', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RETENTION-ACTION', 'LISTED', 'Listed', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RETENTION-ACTION', 'HELD', 'Held', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-RETENTION-ACTION', 'EXCEPTION', 'Exception', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SIGN-METHOD', 'E_SIGNATURE', 'E-signature', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SIGN-METHOD', 'BRANCH', 'Branch', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SIGN-METHOD', 'PAPER', 'Paper', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SIGN-STATUS', 'QUEUED', 'Queued', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SIGN-STATUS', 'SENT', 'Sent', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SIGN-STATUS', 'SIGNED', 'Signed', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SIGN-STATUS', 'DECLINED', 'Declined', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SIGN-STATUS', 'EXPIRED', 'Expired', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SIGNATURE-BASIS', 'E_SIGNATURE_ALLOWED', 'E-signature allowed', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SIGNATURE-BASIS', 'WET_INK_REQUIRED', 'Wet ink required', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRT-SIGNATURE', 'PENDING', 'Pending', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRT-SIGNATURE', 'SIGNED', 'Signed', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-TRT-SIGNATURE', 'NOT_SIGNED', 'Not signed', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CREDIT-RESULT', 'APPROVED', 'Approved', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CREDIT-RESULT', 'REFUSED', 'Refused', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPROVAL-STATUS', 'WAITING', 'Waiting', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPROVAL-STATUS', 'HELD_NO_LIMIT', 'Held, no limit', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPROVAL-STATUS', 'APPROVED', 'Approved', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPROVAL-STATUS', 'REFUSED', 'Refused', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-APPROVAL-STATUS', 'RETURNED', 'Returned', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MATCH-TYPE', 'EXACT', 'Exact', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MATCH-TYPE', 'WINDOW', 'Window', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MATCH-TYPE', 'PARTIAL', 'Partial', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MEASURE-UNIT', 'COUNT', 'Count', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MEASURE-UNIT', 'THB', 'Baht', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MEASURE-UNIT', 'DAYS', 'Days', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MEASURE-UNIT', 'PERCENT', 'Percent', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MEASURE-DIM', 'ROUTE', 'Route', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MEASURE-DIM', 'AGE_BAND', 'Age band', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MEASURE-DIM', 'QUEUE', 'Queue', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MEASURE-DIM', 'STAGE', 'Stage', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MEASURE-DIM', 'AGENT', 'Agent', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MEASURE-PUBLISH', 'PUBLISHED', 'Published', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-MEASURE-PUBLISH', 'HELD', 'Held', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AGENT', 'INTAKE', 'Intake', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AGENT', 'SCREENING', 'Screening', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AGENT', 'LEGAL_DOC', 'Legal doc', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AGENT', 'EXTRACT', 'Extract', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AGENT', 'TDR_OFFER', 'Tdr offer', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AUTONOMY', 'OFF', 'Off', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AUTONOMY', 'SHADOW', 'Shadow', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AUTONOMY', 'L1', 'L1', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONFIG-STATUS', 'LOADED', 'Loaded', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONFIG-STATUS', 'APPROVED', 'Approved', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-CONFIG-STATUS', 'RETIRED', 'Retired', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AGENT-RUN', 'ANSWERED', 'Answered', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AGENT-RUN', 'TIMED_OUT', 'Timed out', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AGENT-RUN', 'GUARDRAIL_FAILED', 'Guardrail failed', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AGENT-RUN', 'BELOW_FLOOR', 'Below floor', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AGENT-RUN', 'TOOL_UNAVAILABLE', 'Tool unavailable', 5, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AGENT-RUN', 'MODEL_ERROR', 'Model error', 6, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AGENT-RUN', 'DISABLED', 'Disabled', 7, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SUBJECT-TYPE', 'CASE', 'Case', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SUBJECT-TYPE', 'DOCUMENT', 'Document', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-SUBJECT-TYPE', 'LEGAL_ACTION', 'Legal action', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EVAL-STATUS', 'RUNNING', 'Running', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EVAL-STATUS', 'DONE', 'Done', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EVAL-STATUS', 'FAILED', 'Failed', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EXTRACT-APPROACH', 'AGENT', 'Agent', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EXTRACT-APPROACH', 'OCR_TEMPLATE', 'OCR template', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EXTRACT-APPROACH', 'MODEL', 'Model', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-EXTRACT-APPROACH', 'OCR_AND_MODEL', 'OCR and model', 4, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-FEEDBACK', 'ACCEPTED', 'Accepted', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-FEEDBACK', 'CORRECTED', 'Corrected', 2, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-FEEDBACK', 'REJECTED', 'Rejected', 3, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AGENT-ALERT', 'COST_CAP', 'Cost cap', 1, DATE '2026-11-30');
INSERT INTO lov_value (lov_code, value_code, label_en, sort_order, valid_from) VALUES ('LOV-AGENT-ALERT', 'DRIFT', 'Drift', 2, DATE '2026-11-30');

-- ---------------------------------------------------------------------------
-- Cross-service references cut from this file (no database foreign key)
-- ---------------------------------------------------------------------------
-- timer.treatment_id -> rwb_treatment.treatment.id (owner S2); the column stays uuid and integrity is through the owner's contract.
-- outbox_event.case_id -> rwb_case.recovery_case.id (owner P3); the column stays uuid and integrity is through the owner's contract.
-- outbox_delivery.task_id -> rwb_case.task.id (owner P3); the column stays uuid and integrity is through the owner's contract.

-- ---------------------------------------------------------------------------
-- Migration provenance columns (RD-P1-027; 27 November 2026). Added once per table by the owner's own Flyway step;
-- null for rows created live. LOV-MIGRATION-SOURCE values are Pending, owner data owner (GAP-3275).
-- ---------------------------------------------------------------------------
ALTER TABLE recovery_case ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN recovery_case.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN recovery_case.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE case_account ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN case_account.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN case_account.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE case_party ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN case_party.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN case_party.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE assignment ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN assignment.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN assignment.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE task ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN task.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN task.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE timer ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN timer.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN timer.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE queue ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN queue.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN queue.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE lov_value ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN lov_value.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN lov_value.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE reference_version ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN reference_version.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN reference_version.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE reference_row ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN reference_row.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN reference_row.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE parameter_catalog ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN parameter_catalog.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN parameter_catalog.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
ALTER TABLE parameter_value ADD COLUMN migration_source varchar(20), ADD COLUMN migrated_at timestamptz;
COMMENT ON COLUMN parameter_value.migration_source IS 'Legacy source of a migrated row (LOV-MIGRATION-SOURCE); null for live rows. Internal, not personal';
COMMENT ON COLUMN parameter_value.migrated_at IS 'UTC instant the owner load wrote the migrated row; null for live rows. Internal, not personal';
