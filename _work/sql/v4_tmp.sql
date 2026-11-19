-- Recovery Workbench physical schema, PostgreSQL
-- SCB Collections and Recovery. Henka Group, 28 October 2026. Version 1.
-- (C) Siam Commercial Bank and Henka Pte Ltd
-- 108 tables in the recovery module of the ACE database, the metadata registry of bank TSD section T3, and seed reference data.

CREATE SCHEMA IF NOT EXISTS recovery;
SET search_path TO recovery;
CREATE EXTENSION IF NOT EXISTS pgcrypto;


-- Recovery case: One recovery case per customer per product, from 90 days past due to close.
CREATE TABLE recovery_case (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_no varchar(18) NOT NULL,
    product_group varchar(15) NOT NULL,
    primary_customer_id uuid NOT NULL,
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
    account_id uuid NOT NULL,
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
    party_id uuid NOT NULL,
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

-- Deviation: A deviation X1 to X7 raised on a case.
CREATE TABLE deviation (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
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
    treatment_id uuid,
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

-- Party: A person or company with a role on one or more cases.
CREATE TABLE party (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    cif_no varchar(20) NOT NULL,
    party_type varchar(15) NOT NULL,
    first_name varchar(100) NOT NULL,
    last_name varchar(100),
    id_type varchar(20) NOT NULL,
    id_no_token varchar(64) NOT NULL,
    date_of_birth date,
    segment varchar(20),
    vulnerable_flag boolean NOT NULL DEFAULT false,
    deceased_flag boolean NOT NULL DEFAULT false,
    bankruptcy_flag boolean NOT NULL DEFAULT false,
    fraud_flag boolean NOT NULL DEFAULT false,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_party UNIQUE (cif_no)
);

-- Contact point: A way to reach a party, with its consent and whether it works.
CREATE TABLE contact_point (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    party_id uuid NOT NULL,
    channel varchar(15) NOT NULL,
    value_token varchar(256) NOT NULL,
    source varchar(15) NOT NULL,
    consent_status varchar(12) NOT NULL DEFAULT 'UNKNOWN',
    verified_at timestamptz,
    failed_count integer NOT NULL DEFAULT 0,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Loan account: A loan account in the core bank.
CREATE TABLE loan_account (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_no varchar(20) NOT NULL,
    contract_no varchar(20),
    product_code varchar(10) NOT NULL,
    product_category_efs varchar(60),
    business_unit varchar(10),
    contract_date date,
    interest_rate numeric(7,4),
    principal_outstanding numeric(18,2) NOT NULL DEFAULT 0,
    interest_outstanding numeric(18,2) NOT NULL DEFAULT 0,
    fees_outstanding numeric(18,2) NOT NULL DEFAULT 0,
    total_balance numeric(18,2) NOT NULL DEFAULT 0,
    accounting_balance numeric(18,2),
    days_past_due integer NOT NULL DEFAULT 0,
    bucket varchar(10),
    classification varchar(10),
    last_payment_date date,
    next_installment_date date,
    tdr_flag boolean NOT NULL DEFAULT false,
    last_tdr_date date,
    data_as_of date NOT NULL,
    dispute_open boolean NOT NULL DEFAULT false,
    settlement_booked_date date,
    settlement_booked_amount numeric(18,2),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_loan_account UNIQUE (account_no)
);

-- Account payment: A payment posted to a loan account.
CREATE TABLE account_payment (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id uuid NOT NULL,
    payment_code varchar(20) NOT NULL,
    payment_date date NOT NULL,
    payment_amount numeric(18,2) NOT NULL,
    payment_channel varchar(15),
    data_as_of date NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_account_payment UNIQUE (payment_code)
);

-- Collateral: Property or vehicle securing one or more accounts.
CREATE TABLE collateral (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    collateral_no varchar(20) NOT NULL,
    collateral_type varchar(15) NOT NULL,
    title_doc_no varchar(40),
    plot_no varchar(20),
    area_text varchar(20),
    province varchar(40),
    district varchar(60),
    subdistrict varchar(60),
    occupancy varchar(15),
    encumbrance_status varchar(15),
    insured_value numeric(18,2),
    insurance_expiry date,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_collateral UNIQUE (collateral_no)
);

-- Account collateral: Which collateral secures which account.
CREATE TABLE account_collateral (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id uuid NOT NULL,
    collateral_id uuid NOT NULL,
    lien_rank integer,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Valuation: An appraisal of collateral or an asset.
CREATE TABLE valuation (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    collateral_id uuid,
    asset_id uuid,
    appraisal_no varchar(20) NOT NULL,
    appraisal_type varchar(15) NOT NULL,
    appraised_value numeric(18,2) NOT NULL,
    forced_sale_value numeric(18,2),
    appraisal_date date NOT NULL,
    valuer_partner_id uuid,
    accepted boolean NOT NULL DEFAULT false,
    stale_flag boolean NOT NULL DEFAULT false,
    age_days integer,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_valuation UNIQUE (appraisal_no)
);

-- Asset: An asset the bank holds after repossession, deed in lieu or auction purchase.
CREATE TABLE asset (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid,
    collateral_id uuid,
    asset_ref varchar(20) NOT NULL,
    asset_code varchar(20),
    asset_type varchar(20) NOT NULL,
    transfer_in_type varchar(20) NOT NULL,
    from_segment varchar(20),
    transfer_in_date date NOT NULL,
    book_value numeric(18,2) NOT NULL,
    auction_purchase_price numeric(18,2),
    repossessed_date date,
    stock_date date,
    holding_status varchar(15) NOT NULL DEFAULT 'HELD',
    holding_cost_to_date numeric(18,2),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_asset UNIQUE (asset_ref)
);

-- Treatment: A resolution put to the customer or carried out on the case, with its terms and outcome.
CREATE TABLE treatment (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    decision_log_id uuid,
    treatment_type varchar(20) NOT NULL,
    proposed_by varchar(10) NOT NULL,
    proposed_at timestamptz NOT NULL,
    offer_amount numeric(18,2),
    haircut_amount numeric(18,2),
    installments integer,
    valid_until date,
    approval_level varchar(4),
    booked_at timestamptz,
    outcome varchar(12),
    outcome_at timestamptz,
    nleads_ref varchar(30),
    credit_result varchar(10),
    credit_result_reason varchar(1000),
    credit_result_at timestamptz,
    interest_rate numeric(7,4),
    booking_difference jsonb,
    first_due_date date,
    signature_status varchar(12),
    installment_amount numeric(18,2),
    installments_paid integer NOT NULL DEFAULT 0,
    installment_shortfall numeric(18,2),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Guarantee claim: A claim against a Thai Credit Guarantee Corporation guarantee or an insurer.
CREATE TABLE guarantee_claim (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    claim_type varchar(25) NOT NULL,
    claim_deadline date NOT NULL,
    claimed_amount numeric(18,2) NOT NULL,
    filed_at date,
    paid_amount numeric(18,2),
    status varchar(12) NOT NULL DEFAULT 'PREPARING',
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Legal action: A notice, lawsuit, appeal, enforcement or bankruptcy action on a case.
CREATE TABLE legal_action (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    law_firm_id uuid,
    action_type varchar(20) NOT NULL,
    lawsuit_no varchar(30),
    black_case_no varchar(30),
    red_case_no varchar(30),
    court_name varchar(120),
    claim_amount numeric(18,2),
    filed_date date,
    judgment_date date,
    judgment_amount numeric(18,2),
    lit_status varchar(200),
    status varchar(15) NOT NULL DEFAULT 'OPEN',
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Notice: A demand, recall or statutory notice and its proof of delivery.
CREATE TABLE notice (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    document_id uuid,
    notice_type varchar(25) NOT NULL,
    sent_date date,
    barcode varchar(40),
    callback_date date,
    delivery_status varchar(15),
    sent_type varchar(10),
    party_id uuid,
    template_id uuid,
    hold_reason varchar(30),
    dispatch_file_id uuid,
    dispatch_attempts integer NOT NULL DEFAULT 0,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Hearing: A court hearing on a legal action.
CREATE TABLE hearing (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    legal_action_id uuid NOT NULL,
    hearing_date timestamptz NOT NULL,
    hearing_type varchar(20),
    outcome varchar(20),
    next_date timestamptz,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Partner: An outside firm the bank places work with.
CREATE TABLE partner (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_code varchar(20) NOT NULL,
    partner_name varchar(160) NOT NULL,
    partner_type varchar(15) NOT NULL,
    panel_status varchar(12) NOT NULL DEFAULT 'ACTIVE',
    contract_end date,
    score numeric(5,2),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_partner UNIQUE (partner_code)
);

-- Partner instruction: Work placed with a partner on a case.
CREATE TABLE partner_instruction (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    partner_id uuid NOT NULL,
    instruction_type varchar(20) NOT NULL,
    instructed_at timestamptz NOT NULL,
    due_at timestamptz,
    status varchar(12) NOT NULL DEFAULT 'SENT',
    result_code varchar(40),
    fee_amount numeric(18,2),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Listing: An asset offered for sale, with its prices and rounds.
CREATE TABLE listing (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id uuid NOT NULL,
    sale_channel varchar(15) NOT NULL,
    start_price numeric(18,2) NOT NULL,
    floor_price numeric(18,2) NOT NULL,
    round_no integer NOT NULL DEFAULT 1,
    listed_at timestamptz,
    status varchar(12) NOT NULL DEFAULT 'DRAFT',
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Asset sale: The sale of an asset.
CREATE TABLE asset_sale (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    asset_id uuid NOT NULL,
    listing_id uuid,
    contract_date date NOT NULL,
    sale_date date NOT NULL,
    sale_price numeric(18,2) NOT NULL,
    transfer_fee numeric(18,2),
    specific_business_tax numeric(18,2),
    corporate_income_tax numeric(18,2),
    gain_loss numeric(18,2),
    incentive_amount numeric(18,2),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Debt sale lot: A lot of accounts offered to debt buyers.
CREATE TABLE debt_sale_lot (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    lot_no varchar(15) NOT NULL,
    cut_off_date date NOT NULL,
    segment varchar(20) NOT NULL,
    reserve_price numeric(18,2),
    buyer_partner_id uuid,
    buyer_class varchar(10),
    signing_date date,
    approval_authority varchar(60),
    payment_terms varchar(400),
    status varchar(12) NOT NULL DEFAULT 'BUILDING',
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_debt_sale_lot UNIQUE (lot_no)
);

-- Debt sale account: An account in a debt sale lot.
CREATE TABLE debt_sale_account (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    lot_id uuid NOT NULL,
    account_id uuid NOT NULL,
    borrower_code varchar(20),
    outstanding numeric(18,2) NOT NULL,
    selling_price numeric(18,2),
    put_back_status varchar(12),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Interaction: One entry in the interaction ledger: a contact, letter, promise, payment or hand-over.
CREATE TABLE interaction (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    party_id uuid,
    occurred_at timestamptz NOT NULL,
    channel varchar(15),
    direction varchar(8),
    action_code varchar(10),
    contact_result varchar(20),
    promise_amount numeric(18,2),
    promise_date date,
    summary varchar(2000),
    conduct_check varchar(15),
    source_system varchar(10) NOT NULL DEFAULT 'WORKBENCH',
    event_code varchar(40),
    actor_type varchar(10),
    actor_ref varchar(64),
    source_ref varchar(60),
    idempotency_key varchar(120),
    case_seq bigint,
    decision_log_id uuid,
    corrects_entry_id uuid,
    contact_point_id uuid,
    from_holder_ref varchar(60),
    to_holder_ref varchar(60),
    treatment_id uuid,
    proceeds_id uuid,
    retention_class varchar(10),
    delivery_status varchar(15),
    external_ref varchar(60),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_interaction UNIQUE (idempotency_key)
);

-- Document: A document held against a case.
CREATE TABLE document (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    party_id uuid,
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
    template_id uuid,
    treatment_id uuid,
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

-- Decision log entry: One record per decision. Append only and hash chained.
CREATE TABLE decision_log_entry (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid,
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

-- Score: A score or estimate COLLINS returns for an account or case.
CREATE TABLE score (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id uuid,
    case_id uuid,
    model_code varchar(30) NOT NULL,
    model_version varchar(20) NOT NULL,
    score_value numeric(12,4),
    estimate_value numeric(18,2),
    route_code varchar(4),
    scored_at date NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Proceeds: Money received on a case and what it was matched to.
CREATE TABLE proceeds (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    treatment_id uuid,
    account_payment_id uuid,
    source varchar(12) NOT NULL,
    amount numeric(18,2) NOT NULL,
    received_date date NOT NULL,
    matched_to varchar(15) NOT NULL DEFAULT 'UNMATCHED',
    posting_ref varchar(40),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Write-off: A write-off of the balance on a case.
CREATE TABLE write_off (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    decision_log_id uuid,
    amount numeric(18,2) NOT NULL,
    tax_criteria_met boolean NOT NULL DEFAULT false,
    committee_date date,
    posted_date date,
    responsibility_center varchar(10),
    cost_center varchar(10),
    gl_product varchar(10),
    recovered_after numeric(18,2) NOT NULL DEFAULT 0,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
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
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_rule_row UNIQUE (rule_id, rule_version)
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

-- Role: A Workbench role, held as data.
CREATE TABLE role (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    role_code varchar(20) NOT NULL,
    role_name varchar(80) NOT NULL,
    role_class varchar(15) NOT NULL,
    default_scope varchar(8) NOT NULL,
    entra_group varchar(120),
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

-- Data product: One of the 14 data products, with its single system of record, owner and refresh cycle.
CREATE TABLE data_product (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    product_code varchar(25) NOT NULL,
    product_name varchar(80) NOT NULL,
    definition varchar(400) NOT NULL,
    system_of_record varchar(120) NOT NULL,
    owner_role varchar(20) NOT NULL,
    owner_user_id uuid,
    refresh_cycle varchar(10) NOT NULL,
    expected_by varchar(20),
    valid_from date NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_data_product UNIQUE (product_code)
);

-- Data product access: Which role may read which data product, by version.
CREATE TABLE data_product_access (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    product_code varchar(25) NOT NULL,
    role_code varchar(20) NOT NULL,
    can_read boolean NOT NULL DEFAULT false,
    access_version varchar(20) NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_data_product_access UNIQUE (product_code, role_code, access_version)
);

-- Data product load: The freshness stamp of a data product for one business date.
CREATE TABLE data_product_load (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    product_code varchar(25) NOT NULL,
    source_system varchar(40) NOT NULL,
    business_date date NOT NULL,
    source_extracted_at timestamptz NOT NULL,
    loaded_at timestamptz NOT NULL,
    status varchar(10) NOT NULL DEFAULT 'LOADED',
    stale_flagged_at timestamptz,
    duplicate_count integer NOT NULL DEFAULT 0,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_data_product_load UNIQUE (product_code, business_date)
);

-- Data contract: A versioned data contract with one source system, confirmed by its system owner.
CREATE TABLE data_contract (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_code varchar(20) NOT NULL,
    source_system varchar(80) NOT NULL,
    interface_id varchar(40) NOT NULL,
    contract_version integer NOT NULL,
    status varchar(10) NOT NULL DEFAULT 'DRAFT',
    confirmed_by_role varchar(80),
    confirmed_on date,
    confirmation_document_ref varchar(400),
    published_at timestamptz,
    published_by uuid,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_data_contract UNIQUE (contract_code, contract_version)
);

-- Sys objects: The metadata registry of entities: one row per object in the data dictionary.
CREATE TABLE sys_objects (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    object_name varchar(60) NOT NULL,
    business_name varchar(120) NOT NULL,
    subject_area varchar(10) NOT NULL,
    data_product varchar(10) NOT NULL,
    system_of_record varchar(120) NOT NULL,
    description varchar(400) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_sys_objects UNIQUE (object_name)
);

-- Sys fields: The metadata registry of fields: the data dictionary held as data.
CREATE TABLE sys_fields (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    field_id varchar(16) NOT NULL,
    object_name varchar(60) NOT NULL,
    field_name varchar(60) NOT NULL,
    data_type varchar(12) NOT NULL,
    physical_type varchar(30) NOT NULL,
    is_mandatory boolean NOT NULL,
    lov_code varchar(30),
    references_object varchar(60),
    source_system varchar(80) NOT NULL,
    source_field varchar(80),
    is_personal boolean NOT NULL DEFAULT false,
    description varchar(400) NOT NULL,
    owner_role varchar(20),
    refresh_cycle varchar(30),
    late_behavior varchar(200),
    interface_id varchar(10),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_sys_fields UNIQUE (field_id)
);

-- Sys field version: Each version of a field definition, kept when the definition changes.
CREATE TABLE sys_field_version (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    field_id varchar(16) NOT NULL,
    field_version integer NOT NULL,
    definition jsonb NOT NULL,
    change_reason varchar(400) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_sys_field_version UNIQUE (field_id, field_version)
);

-- Load run: One run of a data load or job step, with its checks and row counts.
CREATE TABLE load_run (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    interface_id varchar(10),
    job_code varchar(6),
    product_code varchar(25),
    business_date date NOT NULL,
    status varchar(12) NOT NULL DEFAULT 'RUNNING',
    started_at timestamptz NOT NULL,
    ended_at timestamptz,
    rows_read integer,
    rows_loaded integer,
    rows_held integer,
    rows_rejected integer,
    failed_check varchar(8),
    check_results jsonb,
    mapping_version varchar(20),
    interface_run_id uuid,
    tracker_id uuid,
    loaded_by uuid,
    source_file_name varchar(200),
    source_file_hash char(64),
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Dq exception: A record a load check or data quality rule held, until it passes again.
CREATE TABLE dq_exception (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    load_run_id uuid NOT NULL,
    product_code varchar(25) NOT NULL,
    check_code varchar(8) NOT NULL,
    record_key varchar(60) NOT NULL,
    reason_code varchar(8) NOT NULL,
    detail varchar(400),
    raised_on date NOT NULL,
    status varchar(10) NOT NULL DEFAULT 'OPEN',
    rule_version varchar(20),
    cleared_on date,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Dq rule: A versioned data quality row rule run on a P1 table.
CREATE TABLE dq_rule (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_code varchar(8) NOT NULL,
    rule_version varchar(20) NOT NULL,
    rule_name varchar(120) NOT NULL,
    product_code varchar(25) NOT NULL,
    target_entity varchar(60) NOT NULL,
    rule_type varchar(15) NOT NULL,
    rule_params jsonb NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    approved_by uuid NOT NULL,
    test_case_id varchar(20) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_dq_rule UNIQUE (rule_code, rule_version)
);

-- Source field map: How a source field maps to a Workbench field, by interface and mapping version.
CREATE TABLE source_field_map (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    interface_id varchar(10) NOT NULL,
    mapping_version varchar(20) NOT NULL,
    source_field varchar(80) NOT NULL,
    target_entity varchar(60) NOT NULL,
    target_field varchar(60) NOT NULL,
    transformation varchar(200) NOT NULL,
    approved_by uuid,
    approved_on date,
    approval_ref varchar(200),
    valid_from date NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_source_field_map UNIQUE (interface_id, mapping_version, source_field)
);

-- Source code map: How a source code maps to a Workbench list value, by interface and map version.
CREATE TABLE source_code_map (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    interface_id varchar(10) NOT NULL,
    lov_code varchar(30) NOT NULL,
    source_code varchar(30) NOT NULL,
    value_code varchar(30) NOT NULL,
    map_version varchar(20) NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_source_code_map UNIQUE (interface_id, lov_code, source_code, map_version)
);

-- Tracker inventory: A team's Excel or SharePoint tracker, its decision and its load, sign-off and retirement.
CREATE TABLE tracker_inventory (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tracker_code varchar(20) NOT NULL,
    inventory_version varchar(20) NOT NULL,
    team_code varchar(20) NOT NULL,
    tracker_name varchar(120) NOT NULL,
    location_type varchar(12) NOT NULL,
    location_ref varchar(400),
    owner_user_id uuid,
    field_list jsonb NOT NULL,
    update_cycle varchar(10),
    target_product varchar(25),
    decision varchar(8),
    decision_reason varchar(400),
    status varchar(12) NOT NULL DEFAULT 'LISTED',
    valid_from date NOT NULL,
    file_rows integer,
    loaded_rows integer,
    rejected_rows integer,
    last_load_run_id uuid,
    signed_off_by uuid,
    signed_off_at timestamptz,
    source_file_ref varchar(400),
    archive_ref varchar(400),
    retired_at timestamptz,
    retire_confirmed_by uuid,
    unfed_fields jsonb,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_tracker_inventory UNIQUE (tracker_code, inventory_version)
);

-- Tracker row: One row loaded from a tracker file, with its non-personal fields.
CREATE TABLE tracker_row (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tracker_id uuid NOT NULL,
    load_run_id uuid NOT NULL,
    row_no integer NOT NULL,
    account_no varchar(20),
    target_product varchar(25) NOT NULL,
    source_file_name varchar(200) NOT NULL,
    field_values jsonb,
    loaded_on date NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Case list row: One row of the daily case list per case account and business date, published to Power BI.
CREATE TABLE case_list_row (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    business_date date NOT NULL,
    case_id uuid NOT NULL,
    case_no varchar(18) NOT NULL,
    account_id uuid NOT NULL,
    account_no varchar(20) NOT NULL,
    product_group varchar(15) NOT NULL,
    stage_code varchar(20),
    status varchar(20) NOT NULL,
    owner_user_id uuid,
    queue_code varchar(30),
    team_code varchar(20),
    route_code varchar(4),
    total_balance numeric(18,2) NOT NULL DEFAULT 0,
    days_past_due integer NOT NULL DEFAULT 0,
    refreshed_at timestamptz NOT NULL,
    last_contact_at timestamptz,
    last_action_code varchar(10),
    publish_status varchar(10) NOT NULL DEFAULT 'PENDING',
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_case_list_row UNIQUE (business_date)
);

-- Collections history: An EFS contact or promise on an account, loaded from the COLLINS daily batch.
CREATE TABLE collections_history (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_no varchar(20) NOT NULL,
    efs_record_key varchar(40) NOT NULL,
    contact_at timestamptz NOT NULL,
    action_code varchar(10) NOT NULL,
    action_contact_status varchar(20),
    contact_result varchar(20),
    promise_amount numeric(18,2),
    promise_date date,
    business_date date NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_collections_history UNIQUE (efs_record_key)
);

-- Reconciliation result: The daily reconciliation of the case list to ALS by product group.
CREATE TABLE reconciliation_result (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    rec_code varchar(6) NOT NULL,
    business_date date NOT NULL,
    product_group varchar(15) NOT NULL,
    source_count integer NOT NULL,
    workbench_count integer NOT NULL,
    source_amount numeric(18,2),
    workbench_amount numeric(18,2),
    variance_count integer NOT NULL,
    variance_pct numeric(9,4) NOT NULL,
    tolerance_pct numeric(9,4) NOT NULL,
    result varchar(8) NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_reconciliation_result UNIQUE (rec_code, business_date, product_group)
);

-- Lake copy watermark: How far a copy to the data lake has reached, for example the decision log copy.
CREATE TABLE lake_copy_watermark (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    copy_name varchar(40) NOT NULL,
    last_entry_hash char(64),
    last_decided_at timestamptz,
    rows_copied_total bigint NOT NULL DEFAULT '0',
    business_date date,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_lake_copy_watermark UNIQUE (copy_name)
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
    reference_version_id uuid,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_retention_rule UNIQUE (table_name, record_class, rule_version)
);

-- Dp treatment: The copy of each treatment for a business date in the DP04 data product.
CREATE TABLE dp_treatment (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    treatment_id uuid NOT NULL,
    case_id uuid NOT NULL,
    decision_log_id uuid,
    treatment_type varchar(20) NOT NULL,
    proposed_by varchar(10) NOT NULL,
    proposed_at timestamptz NOT NULL,
    offer_amount numeric(18,2),
    haircut_amount numeric(18,2),
    installments integer,
    valid_until date,
    approval_level varchar(4),
    booked_at timestamptz,
    outcome varchar(12),
    outcome_at timestamptz,
    business_date date NOT NULL,
    contract_no varchar(20),
    contract_date date,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_dp_treatment UNIQUE (business_date)
);

-- Dp guarantee claim: The copy of each guarantee claim for a business date in the DP04 data product.
CREATE TABLE dp_guarantee_claim (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    guarantee_claim_id uuid NOT NULL,
    case_id uuid NOT NULL,
    claim_type varchar(25) NOT NULL,
    claim_deadline date NOT NULL,
    claimed_amount numeric(18,2) NOT NULL,
    filed_at date,
    paid_amount numeric(18,2),
    status varchar(12) NOT NULL,
    business_date date NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_dp_guarantee_claim UNIQUE (business_date)
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

-- Interface run: One inbound file received by the adapter and the result of its file checks.
CREATE TABLE interface_run (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    interface_id varchar(10) NOT NULL,
    file_name varchar(200) NOT NULL,
    file_hash char(64) NOT NULL,
    business_date date NOT NULL,
    record_count integer,
    control_total numeric(18,2),
    status varchar(12) NOT NULL DEFAULT 'RECEIVED',
    failed_check varchar(40),
    checks jsonb,
    started_at timestamptz NOT NULL,
    ended_at timestamptz,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_interface_run UNIQUE (interface_id, file_hash, business_date)
);

-- Interface signoff: The data steward's sign-off that an interface no longer needs manual handling.
CREATE TABLE interface_signoff (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    interface_id varchar(10) NOT NULL,
    from_date date NOT NULL,
    to_date date NOT NULL,
    clean_days integer NOT NULL,
    signed_by uuid NOT NULL,
    signed_at timestamptz NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_interface_signoff UNIQUE (interface_id)
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

-- Outbox event: An application event or outbound work request written in the same transaction as the change.
CREATE TABLE outbox_event (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type varchar(40) NOT NULL,
    schema_version integer NOT NULL,
    case_id uuid,
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
    task_id uuid,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_outbox_delivery UNIQUE (event_id, consumer)
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

-- Party product: Another product the party holds at the bank, from the customer profile.
CREATE TABLE party_product (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    party_id uuid NOT NULL,
    product_type varchar(20) NOT NULL,
    account_no varchar(20) NOT NULL,
    product_status varchar(15) NOT NULL,
    data_as_of date NOT NULL,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid
);

-- Efs ledger outcome: Which EFS action codes enter the interaction ledger and on which channel.
CREATE TABLE efs_ledger_outcome (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    action_code varchar(10) NOT NULL,
    channel varchar(15) NOT NULL DEFAULT 'CALL',
    in_ledger boolean NOT NULL DEFAULT true,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_efs_ledger_outcome UNIQUE (action_code)
);

-- Case entry exclusion: An account at 90 days past due that an exclusion rule kept out of recovery on a business date.
CREATE TABLE case_entry_exclusion (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id uuid NOT NULL,
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
    CONSTRAINT uk_case_entry_exclusion UNIQUE (business_date)
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

-- Rule test case: A test case of the rule table test harness, with its expected and actual result.
CREATE TABLE rule_test_case (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    test_case_id varchar(20) NOT NULL,
    route_set varchar(15) NOT NULL,
    rule_version varchar(20) NOT NULL,
    rule_id varchar(20) NOT NULL,
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

-- Partner user: A partner user's identity bound to one partner firm and one partner role.
CREATE TABLE partner_user (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    identity_ref varchar(64) NOT NULL,
    partner_id uuid NOT NULL,
    role_code varchar(20) NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_partner_user UNIQUE (identity_ref)
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
    reference_version_id uuid,
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
    reference_version_id uuid,
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
    case_id uuid NOT NULL,
    checklist_version varchar(20),
    required_count integer NOT NULL DEFAULT 0,
    present_count integer NOT NULL DEFAULT 0,
    missing_types jsonb,
    complete boolean,
    checked_at timestamptz NOT NULL,
    last_event_id uuid,
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
    reference_version_id uuid,
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
    partner_id uuid,
    run_id uuid,
    received_at timestamptz NOT NULL,
    file_sha256 char(64) NOT NULL,
    intake_ref varchar(400) NOT NULL,
    scan_result varchar(10),
    scanned_at timestamptz,
    case_id uuid,
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
    decision_log_id uuid,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_retention_action UNIQUE (run_month)
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

-- Signature request: A request for a party to sign a generated document, and its result.
CREATE TABLE signature_request (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    treatment_id uuid,
    document_id uuid NOT NULL,
    party_id uuid NOT NULL,
    method varchar(15) NOT NULL,
    status varchar(15) NOT NULL DEFAULT 'QUEUED',
    external_ref varchar(60),
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

-- Approval: An item waiting for approval, routed to the level the delegation of authority requires.
CREATE TABLE approval (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id uuid NOT NULL,
    decision_code varchar(8) NOT NULL,
    regulation_item varchar(10),
    capability_area varchar(30) NOT NULL,
    route_role_code varchar(20),
    approval_level varchar(4),
    delegation_limit_id uuid,
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

-- Payment match rule: A rule for matching a payment to a plan installment, by version.
CREATE TABLE payment_match_rule (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_code varchar(20) NOT NULL,
    rule_version varchar(20) NOT NULL,
    match_type varchar(15) NOT NULL,
    amount_tolerance_pct numeric(5,2) NOT NULL DEFAULT 0,
    window_days_before integer NOT NULL DEFAULT 0,
    window_days_after integer NOT NULL DEFAULT 0,
    grace_days integer NOT NULL DEFAULT 0,
    partial_floor_pct numeric(5,2),
    priority integer NOT NULL,
    valid_from date NOT NULL,
    valid_to date,
    approved_by uuid,
    is_active boolean NOT NULL DEFAULT true,
    state varchar(40),
    version integer NOT NULL DEFAULT 1,
    created_at timestamptz NOT NULL DEFAULT now(),
    created_by uuid,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by uuid,
    CONSTRAINT uk_payment_match_rule UNIQUE (rule_code, rule_version)
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
    case_id uuid,
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
    decision_log_id uuid,
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
    decision_log_id uuid,
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

-- References between tables

-- v_data_dictionary: the data dictionary as one row per field, joining the metadata tables to
-- the data product catalog so a developer can ask where a field comes from and who owns it.
CREATE VIEW v_data_dictionary AS
SELECT o.object_name      AS entity,
       f.field_name       AS field,
       f.field_id,
       f.data_type,
       f.physical_type,
       f.is_mandatory,
       f.lov_code,
       f.references_object,
       f.source_system,
       f.source_field,
       f.is_personal,
       o.data_product,
       p.refresh_cycle,
       f.owner_role,
       p.owner_user_id,
       f.late_behavior,
       f.interface_id,
       f.description
FROM sys_fields f
JOIN sys_objects o ON o.object_name = f.object_name
LEFT JOIN data_product p ON p.product_code = o.data_product AND p.is_active
WHERE f.is_active AND o.is_active;

COMMENT ON VIEW v_data_dictionary IS 'The data dictionary as one row per field, with its data product, refresh cycle and owner.';

ALTER TABLE recovery_case ADD CONSTRAINT fk_recovery_case_primary_customer_id FOREIGN KEY (primary_customer_id) REFERENCES party (id) ON DELETE RESTRICT;
ALTER TABLE recovery_case ADD CONSTRAINT fk_recovery_case_queue_id FOREIGN KEY (queue_id) REFERENCES queue (id) ON DELETE RESTRICT;
ALTER TABLE case_account ADD CONSTRAINT fk_case_account_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE case_account ADD CONSTRAINT fk_case_account_account_id FOREIGN KEY (account_id) REFERENCES loan_account (id) ON DELETE RESTRICT;
ALTER TABLE case_party ADD CONSTRAINT fk_case_party_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE case_party ADD CONSTRAINT fk_case_party_party_id FOREIGN KEY (party_id) REFERENCES party (id) ON DELETE RESTRICT;
ALTER TABLE deviation ADD CONSTRAINT fk_deviation_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE queue ADD CONSTRAINT fk_queue_overflow_queue_id FOREIGN KEY (overflow_queue_id) REFERENCES queue (id) ON DELETE RESTRICT;
ALTER TABLE assignment ADD CONSTRAINT fk_assignment_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE assignment ADD CONSTRAINT fk_assignment_task_id FOREIGN KEY (task_id) REFERENCES task (id) ON DELETE RESTRICT;
ALTER TABLE assignment ADD CONSTRAINT fk_assignment_queue_id FOREIGN KEY (queue_id) REFERENCES queue (id) ON DELETE RESTRICT;
ALTER TABLE task ADD CONSTRAINT fk_task_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE timer ADD CONSTRAINT fk_timer_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE timer ADD CONSTRAINT fk_timer_task_id FOREIGN KEY (task_id) REFERENCES task (id) ON DELETE RESTRICT;
ALTER TABLE timer ADD CONSTRAINT fk_timer_treatment_id FOREIGN KEY (treatment_id) REFERENCES treatment (id) ON DELETE RESTRICT;
ALTER TABLE contact_point ADD CONSTRAINT fk_contact_point_party_id FOREIGN KEY (party_id) REFERENCES party (id) ON DELETE RESTRICT;
ALTER TABLE account_payment ADD CONSTRAINT fk_account_payment_account_id FOREIGN KEY (account_id) REFERENCES loan_account (id) ON DELETE RESTRICT;
ALTER TABLE account_collateral ADD CONSTRAINT fk_account_collateral_account_id FOREIGN KEY (account_id) REFERENCES loan_account (id) ON DELETE RESTRICT;
ALTER TABLE account_collateral ADD CONSTRAINT fk_account_collateral_collateral_id FOREIGN KEY (collateral_id) REFERENCES collateral (id) ON DELETE RESTRICT;
ALTER TABLE valuation ADD CONSTRAINT fk_valuation_collateral_id FOREIGN KEY (collateral_id) REFERENCES collateral (id) ON DELETE RESTRICT;
ALTER TABLE valuation ADD CONSTRAINT fk_valuation_asset_id FOREIGN KEY (asset_id) REFERENCES asset (id) ON DELETE RESTRICT;
ALTER TABLE valuation ADD CONSTRAINT fk_valuation_valuer_partner_id FOREIGN KEY (valuer_partner_id) REFERENCES partner (id) ON DELETE RESTRICT;
ALTER TABLE asset ADD CONSTRAINT fk_asset_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE asset ADD CONSTRAINT fk_asset_collateral_id FOREIGN KEY (collateral_id) REFERENCES collateral (id) ON DELETE RESTRICT;
ALTER TABLE treatment ADD CONSTRAINT fk_treatment_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE treatment ADD CONSTRAINT fk_treatment_decision_log_id FOREIGN KEY (decision_log_id) REFERENCES decision_log_entry (id) ON DELETE RESTRICT;
ALTER TABLE guarantee_claim ADD CONSTRAINT fk_guarantee_claim_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE legal_action ADD CONSTRAINT fk_legal_action_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE legal_action ADD CONSTRAINT fk_legal_action_law_firm_id FOREIGN KEY (law_firm_id) REFERENCES partner (id) ON DELETE RESTRICT;
ALTER TABLE notice ADD CONSTRAINT fk_notice_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE notice ADD CONSTRAINT fk_notice_document_id FOREIGN KEY (document_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE notice ADD CONSTRAINT fk_notice_party_id FOREIGN KEY (party_id) REFERENCES party (id) ON DELETE RESTRICT;
ALTER TABLE notice ADD CONSTRAINT fk_notice_template_id FOREIGN KEY (template_id) REFERENCES template (id) ON DELETE RESTRICT;
ALTER TABLE notice ADD CONSTRAINT fk_notice_dispatch_file_id FOREIGN KEY (dispatch_file_id) REFERENCES outbound_item (id) ON DELETE RESTRICT;
ALTER TABLE hearing ADD CONSTRAINT fk_hearing_legal_action_id FOREIGN KEY (legal_action_id) REFERENCES legal_action (id) ON DELETE RESTRICT;
ALTER TABLE partner_instruction ADD CONSTRAINT fk_partner_instruction_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE partner_instruction ADD CONSTRAINT fk_partner_instruction_partner_id FOREIGN KEY (partner_id) REFERENCES partner (id) ON DELETE RESTRICT;
ALTER TABLE listing ADD CONSTRAINT fk_listing_asset_id FOREIGN KEY (asset_id) REFERENCES asset (id) ON DELETE RESTRICT;
ALTER TABLE asset_sale ADD CONSTRAINT fk_asset_sale_asset_id FOREIGN KEY (asset_id) REFERENCES asset (id) ON DELETE RESTRICT;
ALTER TABLE asset_sale ADD CONSTRAINT fk_asset_sale_listing_id FOREIGN KEY (listing_id) REFERENCES listing (id) ON DELETE RESTRICT;
ALTER TABLE debt_sale_lot ADD CONSTRAINT fk_debt_sale_lot_buyer_partner_id FOREIGN KEY (buyer_partner_id) REFERENCES partner (id) ON DELETE RESTRICT;
ALTER TABLE debt_sale_account ADD CONSTRAINT fk_debt_sale_account_lot_id FOREIGN KEY (lot_id) REFERENCES debt_sale_lot (id) ON DELETE RESTRICT;
ALTER TABLE debt_sale_account ADD CONSTRAINT fk_debt_sale_account_account_id FOREIGN KEY (account_id) REFERENCES loan_account (id) ON DELETE RESTRICT;
ALTER TABLE interaction ADD CONSTRAINT fk_interaction_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE interaction ADD CONSTRAINT fk_interaction_party_id FOREIGN KEY (party_id) REFERENCES party (id) ON DELETE RESTRICT;
ALTER TABLE interaction ADD CONSTRAINT fk_interaction_decision_log_id FOREIGN KEY (decision_log_id) REFERENCES decision_log_entry (id) ON DELETE RESTRICT;
ALTER TABLE interaction ADD CONSTRAINT fk_interaction_corrects_entry_id FOREIGN KEY (corrects_entry_id) REFERENCES interaction (id) ON DELETE RESTRICT;
ALTER TABLE interaction ADD CONSTRAINT fk_interaction_contact_point_id FOREIGN KEY (contact_point_id) REFERENCES contact_point (id) ON DELETE RESTRICT;
ALTER TABLE interaction ADD CONSTRAINT fk_interaction_treatment_id FOREIGN KEY (treatment_id) REFERENCES treatment (id) ON DELETE RESTRICT;
ALTER TABLE interaction ADD CONSTRAINT fk_interaction_proceeds_id FOREIGN KEY (proceeds_id) REFERENCES proceeds (id) ON DELETE RESTRICT;
ALTER TABLE document ADD CONSTRAINT fk_document_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE document ADD CONSTRAINT fk_document_party_id FOREIGN KEY (party_id) REFERENCES party (id) ON DELETE RESTRICT;
ALTER TABLE document ADD CONSTRAINT fk_document_previous_version_id FOREIGN KEY (previous_version_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE document ADD CONSTRAINT fk_document_template_id FOREIGN KEY (template_id) REFERENCES template (id) ON DELETE RESTRICT;
ALTER TABLE document ADD CONSTRAINT fk_document_treatment_id FOREIGN KEY (treatment_id) REFERENCES treatment (id) ON DELETE RESTRICT;
ALTER TABLE document_field ADD CONSTRAINT fk_document_field_document_id FOREIGN KEY (document_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE document_custody ADD CONSTRAINT fk_document_custody_document_id FOREIGN KEY (document_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE decision_log_entry ADD CONSTRAINT fk_decision_log_entry_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE decision_log_entry ADD CONSTRAINT fk_decision_log_entry_corrects_entry_id FOREIGN KEY (corrects_entry_id) REFERENCES decision_log_entry (id) ON DELETE RESTRICT;
ALTER TABLE score ADD CONSTRAINT fk_score_account_id FOREIGN KEY (account_id) REFERENCES loan_account (id) ON DELETE RESTRICT;
ALTER TABLE score ADD CONSTRAINT fk_score_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE proceeds ADD CONSTRAINT fk_proceeds_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE proceeds ADD CONSTRAINT fk_proceeds_treatment_id FOREIGN KEY (treatment_id) REFERENCES treatment (id) ON DELETE RESTRICT;
ALTER TABLE proceeds ADD CONSTRAINT fk_proceeds_account_payment_id FOREIGN KEY (account_payment_id) REFERENCES account_payment (id) ON DELETE RESTRICT;
ALTER TABLE write_off ADD CONSTRAINT fk_write_off_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE write_off ADD CONSTRAINT fk_write_off_decision_log_id FOREIGN KEY (decision_log_id) REFERENCES decision_log_entry (id) ON DELETE RESTRICT;
ALTER TABLE permission ADD CONSTRAINT fk_permission_role_id FOREIGN KEY (role_id) REFERENCES role (id) ON DELETE RESTRICT;
ALTER TABLE load_run ADD CONSTRAINT fk_load_run_interface_run_id FOREIGN KEY (interface_run_id) REFERENCES interface_run (id) ON DELETE RESTRICT;
ALTER TABLE load_run ADD CONSTRAINT fk_load_run_tracker_id FOREIGN KEY (tracker_id) REFERENCES tracker_inventory (id) ON DELETE RESTRICT;
ALTER TABLE dq_exception ADD CONSTRAINT fk_dq_exception_load_run_id FOREIGN KEY (load_run_id) REFERENCES load_run (id) ON DELETE RESTRICT;
ALTER TABLE tracker_inventory ADD CONSTRAINT fk_tracker_inventory_last_load_run_id FOREIGN KEY (last_load_run_id) REFERENCES load_run (id) ON DELETE RESTRICT;
ALTER TABLE tracker_row ADD CONSTRAINT fk_tracker_row_tracker_id FOREIGN KEY (tracker_id) REFERENCES tracker_inventory (id) ON DELETE RESTRICT;
ALTER TABLE tracker_row ADD CONSTRAINT fk_tracker_row_load_run_id FOREIGN KEY (load_run_id) REFERENCES load_run (id) ON DELETE RESTRICT;
ALTER TABLE case_list_row ADD CONSTRAINT fk_case_list_row_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE case_list_row ADD CONSTRAINT fk_case_list_row_account_id FOREIGN KEY (account_id) REFERENCES loan_account (id) ON DELETE RESTRICT;
ALTER TABLE retention_rule ADD CONSTRAINT fk_retention_rule_reference_version_id FOREIGN KEY (reference_version_id) REFERENCES reference_version (id) ON DELETE RESTRICT;
ALTER TABLE dp_treatment ADD CONSTRAINT fk_dp_treatment_treatment_id FOREIGN KEY (treatment_id) REFERENCES treatment (id) ON DELETE RESTRICT;
ALTER TABLE dp_treatment ADD CONSTRAINT fk_dp_treatment_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE dp_treatment ADD CONSTRAINT fk_dp_treatment_decision_log_id FOREIGN KEY (decision_log_id) REFERENCES decision_log_entry (id) ON DELETE RESTRICT;
ALTER TABLE dp_guarantee_claim ADD CONSTRAINT fk_dp_guarantee_claim_guarantee_claim_id FOREIGN KEY (guarantee_claim_id) REFERENCES guarantee_claim (id) ON DELETE RESTRICT;
ALTER TABLE dp_guarantee_claim ADD CONSTRAINT fk_dp_guarantee_claim_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE processed_event ADD CONSTRAINT fk_processed_event_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;
ALTER TABLE outbox_event ADD CONSTRAINT fk_outbox_event_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE sys_fields ADD CONSTRAINT fk_sys_fields_object_name FOREIGN KEY (object_name) REFERENCES sys_objects (object_name) ON DELETE RESTRICT;
ALTER TABLE sys_objects ADD CONSTRAINT fk_sys_objects_data_product FOREIGN KEY (data_product) REFERENCES data_product (product_code) ON DELETE RESTRICT;
ALTER TABLE outbox_delivery ADD CONSTRAINT fk_outbox_delivery_event_id FOREIGN KEY (event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;
ALTER TABLE outbox_delivery ADD CONSTRAINT fk_outbox_delivery_task_id FOREIGN KEY (task_id) REFERENCES task (id) ON DELETE RESTRICT;
ALTER TABLE party_product ADD CONSTRAINT fk_party_product_party_id FOREIGN KEY (party_id) REFERENCES party (id) ON DELETE RESTRICT;
ALTER TABLE case_entry_exclusion ADD CONSTRAINT fk_case_entry_exclusion_account_id FOREIGN KEY (account_id) REFERENCES loan_account (id) ON DELETE RESTRICT;
ALTER TABLE queue_member ADD CONSTRAINT fk_queue_member_queue_id FOREIGN KEY (queue_id) REFERENCES queue (id) ON DELETE RESTRICT;
ALTER TABLE queue_measure ADD CONSTRAINT fk_queue_measure_queue_id FOREIGN KEY (queue_id) REFERENCES queue (id) ON DELETE RESTRICT;
ALTER TABLE reference_row ADD CONSTRAINT fk_reference_row_version_id FOREIGN KEY (version_id) REFERENCES reference_version (id) ON DELETE RESTRICT;
ALTER TABLE partner_user ADD CONSTRAINT fk_partner_user_partner_id FOREIGN KEY (partner_id) REFERENCES partner (id) ON DELETE RESTRICT;
ALTER TABLE document_type ADD CONSTRAINT fk_document_type_reference_version_id FOREIGN KEY (reference_version_id) REFERENCES reference_version (id) ON DELETE RESTRICT;
ALTER TABLE document_checklist_item ADD CONSTRAINT fk_document_checklist_item_reference_version_id FOREIGN KEY (reference_version_id) REFERENCES reference_version (id) ON DELETE RESTRICT;
ALTER TABLE case_document_check ADD CONSTRAINT fk_case_document_check_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE case_document_check ADD CONSTRAINT fk_case_document_check_last_event_id FOREIGN KEY (last_event_id) REFERENCES outbox_event (id) ON DELETE RESTRICT;
ALTER TABLE document_hub_parameter ADD CONSTRAINT fk_document_hub_parameter_reference_version_id FOREIGN KEY (reference_version_id) REFERENCES reference_version (id) ON DELETE RESTRICT;
ALTER TABLE document_intake ADD CONSTRAINT fk_document_intake_partner_id FOREIGN KEY (partner_id) REFERENCES partner (id) ON DELETE RESTRICT;
ALTER TABLE document_intake ADD CONSTRAINT fk_document_intake_run_id FOREIGN KEY (run_id) REFERENCES load_run (id) ON DELETE RESTRICT;
ALTER TABLE document_intake ADD CONSTRAINT fk_document_intake_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE document_intake ADD CONSTRAINT fk_document_intake_document_id FOREIGN KEY (document_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE document_text ADD CONSTRAINT fk_document_text_intake_id FOREIGN KEY (intake_id) REFERENCES document_intake (id) ON DELETE RESTRICT;
ALTER TABLE document_text ADD CONSTRAINT fk_document_text_document_id FOREIGN KEY (document_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE retention_action ADD CONSTRAINT fk_retention_action_document_id FOREIGN KEY (document_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE retention_action ADD CONSTRAINT fk_retention_action_decision_log_id FOREIGN KEY (decision_log_id) REFERENCES decision_log_entry (id) ON DELETE RESTRICT;
ALTER TABLE signature_request ADD CONSTRAINT fk_signature_request_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE signature_request ADD CONSTRAINT fk_signature_request_treatment_id FOREIGN KEY (treatment_id) REFERENCES treatment (id) ON DELETE RESTRICT;
ALTER TABLE signature_request ADD CONSTRAINT fk_signature_request_document_id FOREIGN KEY (document_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE signature_request ADD CONSTRAINT fk_signature_request_party_id FOREIGN KEY (party_id) REFERENCES party (id) ON DELETE RESTRICT;
ALTER TABLE signature_request ADD CONSTRAINT fk_signature_request_signed_document_id FOREIGN KEY (signed_document_id) REFERENCES document (id) ON DELETE RESTRICT;
ALTER TABLE approval ADD CONSTRAINT fk_approval_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE approval ADD CONSTRAINT fk_approval_delegation_limit_id FOREIGN KEY (delegation_limit_id) REFERENCES delegation_limit (id) ON DELETE RESTRICT;
ALTER TABLE approval ADD CONSTRAINT fk_approval_decision_log_id FOREIGN KEY (decision_log_id) REFERENCES decision_log_entry (id) ON DELETE RESTRICT;
ALTER TABLE agent_policy ADD CONSTRAINT fk_agent_policy_evaluation_run_id FOREIGN KEY (evaluation_run_id) REFERENCES agent_evaluation_run (id) ON DELETE RESTRICT;
ALTER TABLE agent_run ADD CONSTRAINT fk_agent_run_case_id FOREIGN KEY (case_id) REFERENCES recovery_case (id) ON DELETE RESTRICT;
ALTER TABLE agent_run ADD CONSTRAINT fk_agent_run_evaluation_run_id FOREIGN KEY (evaluation_run_id) REFERENCES agent_evaluation_run (id) ON DELETE RESTRICT;
ALTER TABLE agent_run ADD CONSTRAINT fk_agent_run_decision_log_id FOREIGN KEY (decision_log_id) REFERENCES decision_log_entry (id) ON DELETE RESTRICT;
ALTER TABLE agent_evaluation ADD CONSTRAINT fk_agent_evaluation_evaluation_run_id FOREIGN KEY (evaluation_run_id) REFERENCES agent_evaluation_run (id) ON DELETE RESTRICT;
ALTER TABLE agent_feedback ADD CONSTRAINT fk_agent_feedback_agent_run_id FOREIGN KEY (agent_run_id) REFERENCES agent_run (id) ON DELETE RESTRICT;
ALTER TABLE agent_feedback ADD CONSTRAINT fk_agent_feedback_decision_log_id FOREIGN KEY (decision_log_id) REFERENCES decision_log_entry (id) ON DELETE RESTRICT;

-- Indexes on references and on the columns queues, timers and the decision log are read by
CREATE INDEX ix_recovery_case_primary_customer_id ON recovery_case (primary_customer_id);
CREATE INDEX ix_recovery_case_queue_id ON recovery_case (queue_id);
CREATE INDEX ix_case_account_case_id ON case_account (case_id);
CREATE INDEX ix_case_account_account_id ON case_account (account_id);
CREATE INDEX ix_case_party_case_id ON case_party (case_id);
CREATE INDEX ix_case_party_party_id ON case_party (party_id);
CREATE INDEX ix_deviation_case_id ON deviation (case_id);
CREATE INDEX ix_queue_overflow_queue_id ON queue (overflow_queue_id);
CREATE INDEX ix_assignment_case_id ON assignment (case_id);
CREATE INDEX ix_assignment_task_id ON assignment (task_id);
CREATE INDEX ix_assignment_queue_id ON assignment (queue_id);
CREATE INDEX ix_task_case_id ON task (case_id);
CREATE INDEX ix_timer_case_id ON timer (case_id);
CREATE INDEX ix_timer_task_id ON timer (task_id);
CREATE INDEX ix_timer_treatment_id ON timer (treatment_id);
CREATE INDEX ix_contact_point_party_id ON contact_point (party_id);
CREATE INDEX ix_account_payment_account_id ON account_payment (account_id);
CREATE INDEX ix_account_collateral_account_id ON account_collateral (account_id);
CREATE INDEX ix_account_collateral_collateral_id ON account_collateral (collateral_id);
CREATE INDEX ix_valuation_collateral_id ON valuation (collateral_id);
CREATE INDEX ix_valuation_asset_id ON valuation (asset_id);
CREATE INDEX ix_valuation_valuer_partner_id ON valuation (valuer_partner_id);
CREATE INDEX ix_asset_case_id ON asset (case_id);
CREATE INDEX ix_asset_collateral_id ON asset (collateral_id);
CREATE INDEX ix_treatment_case_id ON treatment (case_id);
CREATE INDEX ix_treatment_decision_log_id ON treatment (decision_log_id);
CREATE INDEX ix_guarantee_claim_case_id ON guarantee_claim (case_id);
CREATE INDEX ix_legal_action_case_id ON legal_action (case_id);
CREATE INDEX ix_legal_action_law_firm_id ON legal_action (law_firm_id);
CREATE INDEX ix_notice_case_id ON notice (case_id);
CREATE INDEX ix_notice_document_id ON notice (document_id);
CREATE INDEX ix_notice_party_id ON notice (party_id);
CREATE INDEX ix_notice_template_id ON notice (template_id);
CREATE INDEX ix_notice_dispatch_file_id ON notice (dispatch_file_id);
CREATE INDEX ix_hearing_legal_action_id ON hearing (legal_action_id);
CREATE INDEX ix_partner_instruction_case_id ON partner_instruction (case_id);
CREATE INDEX ix_partner_instruction_partner_id ON partner_instruction (partner_id);
CREATE INDEX ix_listing_asset_id ON listing (asset_id);
CREATE INDEX ix_asset_sale_asset_id ON asset_sale (asset_id);
CREATE INDEX ix_asset_sale_listing_id ON asset_sale (listing_id);
CREATE INDEX ix_debt_sale_lot_buyer_partner_id ON debt_sale_lot (buyer_partner_id);
CREATE INDEX ix_debt_sale_account_lot_id ON debt_sale_account (lot_id);
CREATE INDEX ix_debt_sale_account_account_id ON debt_sale_account (account_id);
CREATE INDEX ix_interaction_case_id ON interaction (case_id);
CREATE INDEX ix_interaction_party_id ON interaction (party_id);
CREATE INDEX ix_interaction_decision_log_id ON interaction (decision_log_id);
CREATE INDEX ix_interaction_corrects_entry_id ON interaction (corrects_entry_id);
CREATE INDEX ix_interaction_contact_point_id ON interaction (contact_point_id);
CREATE INDEX ix_interaction_treatment_id ON interaction (treatment_id);
CREATE INDEX ix_interaction_proceeds_id ON interaction (proceeds_id);
CREATE INDEX ix_document_case_id ON document (case_id);
CREATE INDEX ix_document_party_id ON document (party_id);
CREATE INDEX ix_document_previous_version_id ON document (previous_version_id);
CREATE INDEX ix_document_template_id ON document (template_id);
CREATE INDEX ix_document_treatment_id ON document (treatment_id);
CREATE INDEX ix_document_field_document_id ON document_field (document_id);
CREATE INDEX ix_document_custody_document_id ON document_custody (document_id);
CREATE INDEX ix_decision_log_entry_case_id ON decision_log_entry (case_id);
CREATE INDEX ix_decision_log_entry_corrects_entry_id ON decision_log_entry (corrects_entry_id);
CREATE INDEX ix_score_account_id ON score (account_id);
CREATE INDEX ix_score_case_id ON score (case_id);
CREATE INDEX ix_proceeds_case_id ON proceeds (case_id);
CREATE INDEX ix_proceeds_treatment_id ON proceeds (treatment_id);
CREATE INDEX ix_proceeds_account_payment_id ON proceeds (account_payment_id);
CREATE INDEX ix_write_off_case_id ON write_off (case_id);
CREATE INDEX ix_write_off_decision_log_id ON write_off (decision_log_id);
CREATE INDEX ix_permission_role_id ON permission (role_id);
CREATE INDEX ix_load_run_interface_run_id ON load_run (interface_run_id);
CREATE INDEX ix_load_run_tracker_id ON load_run (tracker_id);
CREATE INDEX ix_dq_exception_load_run_id ON dq_exception (load_run_id);
CREATE INDEX ix_tracker_inventory_last_load_run_id ON tracker_inventory (last_load_run_id);
CREATE INDEX ix_tracker_row_tracker_id ON tracker_row (tracker_id);
CREATE INDEX ix_tracker_row_load_run_id ON tracker_row (load_run_id);
CREATE INDEX ix_case_list_row_case_id ON case_list_row (case_id);
CREATE INDEX ix_case_list_row_account_id ON case_list_row (account_id);
CREATE INDEX ix_retention_rule_reference_version_id ON retention_rule (reference_version_id);
CREATE INDEX ix_dp_treatment_treatment_id ON dp_treatment (treatment_id);
CREATE INDEX ix_dp_treatment_case_id ON dp_treatment (case_id);
CREATE INDEX ix_dp_treatment_decision_log_id ON dp_treatment (decision_log_id);
CREATE INDEX ix_dp_guarantee_claim_guarantee_claim_id ON dp_guarantee_claim (guarantee_claim_id);
CREATE INDEX ix_dp_guarantee_claim_case_id ON dp_guarantee_claim (case_id);
CREATE INDEX ix_processed_event_event_id ON processed_event (event_id);
CREATE INDEX ix_outbox_event_case_id ON outbox_event (case_id);
CREATE INDEX ix_outbox_delivery_event_id ON outbox_delivery (event_id);
CREATE INDEX ix_outbox_delivery_task_id ON outbox_delivery (task_id);
CREATE INDEX ix_party_product_party_id ON party_product (party_id);
CREATE INDEX ix_case_entry_exclusion_account_id ON case_entry_exclusion (account_id);
CREATE INDEX ix_queue_member_queue_id ON queue_member (queue_id);
CREATE INDEX ix_queue_measure_queue_id ON queue_measure (queue_id);
CREATE INDEX ix_reference_row_version_id ON reference_row (version_id);
CREATE INDEX ix_partner_user_partner_id ON partner_user (partner_id);
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
CREATE INDEX ix_signature_request_party_id ON signature_request (party_id);
CREATE INDEX ix_signature_request_signed_document_id ON signature_request (signed_document_id);
CREATE INDEX ix_approval_case_id ON approval (case_id);
CREATE INDEX ix_approval_delegation_limit_id ON approval (delegation_limit_id);
CREATE INDEX ix_approval_decision_log_id ON approval (decision_log_id);
CREATE INDEX ix_agent_policy_evaluation_run_id ON agent_policy (evaluation_run_id);
CREATE INDEX ix_agent_run_case_id ON agent_run (case_id);
CREATE INDEX ix_agent_run_evaluation_run_id ON agent_run (evaluation_run_id);
CREATE INDEX ix_agent_run_decision_log_id ON agent_run (decision_log_id);
CREATE INDEX ix_agent_evaluation_evaluation_run_id ON agent_evaluation (evaluation_run_id);
CREATE INDEX ix_agent_feedback_agent_run_id ON agent_feedback (agent_run_id);
CREATE INDEX ix_agent_feedback_decision_log_id ON agent_feedback (decision_log_id);
CREATE INDEX ix_case_status_queue ON recovery_case (status, queue_id);
CREATE INDEX ix_case_owner_status ON recovery_case (owner_user_id, status);
CREATE INDEX ix_case_prescription ON recovery_case (prescription_date) WHERE closed_date IS NULL;
CREATE INDEX ix_timer_due ON timer (expires_at) WHERE status = 'RUNNING';
CREATE INDEX ix_task_open ON task (case_id, status) WHERE status IN ('OPEN','IN_PROGRESS');
CREATE INDEX ix_declog_case_time ON decision_log_entry (case_id, decided_at);
CREATE INDEX ix_interaction_case_time ON interaction (case_id, occurred_at);
CREATE INDEX ix_account_dpd ON loan_account (days_past_due);
CREATE INDEX ix_rule_lookup ON rule_row (route_set, from_state, event_code) WHERE is_active;

-- The decision log and the interaction ledger are append only
CREATE OR REPLACE FUNCTION refuse_change() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION '% is append only: % refused', TG_TABLE_NAME, TG_OP;
END;
$$;
CREATE TRIGGER tr_declog_append_only BEFORE UPDATE OR DELETE ON decision_log_entry FOR EACH ROW EXECUTE FUNCTION refuse_change();
CREATE TRIGGER tr_interaction_append_only BEFORE UPDATE OR DELETE ON interaction FOR EACH ROW EXECUTE FUNCTION refuse_change();

-- Descriptions
COMMENT ON TABLE agent_alert IS 'A cost cap or drift alert raised for an agent.';
COMMENT ON TABLE agent_feedback IS 'A person''s verdict on an agent answer.';
COMMENT ON TABLE agent_evaluation IS 'The score of one approach on one label key in an evaluation run.';
COMMENT ON TABLE agent_evaluation_run IS 'One evaluation of an agent version against a sample.';
COMMENT ON TABLE agent_sample IS 'One labeled subject in a versioned evaluation sample.';
COMMENT ON TABLE agent_run IS 'One call of an agent or model, with its versions, checks, answer, cost and fallback.';
COMMENT ON TABLE agent_prompt IS 'A version of an agent''s prompt text.';
COMMENT ON TABLE agent_policy IS 'A version of an agent''s policy: model, tools, autonomy, limits and fallback.';
COMMENT ON TABLE measure_publish IS 'Whether the day''s dashboard data set was published or held after reconciling to the case list.';
COMMENT ON TABLE measure_snapshot IS 'The value of one measure for a business date, product and dimension value.';
COMMENT ON TABLE measure_definition IS 'The agreed definition of a reported measure, by version.';
COMMENT ON TABLE payment_match_rule IS 'A rule for matching a payment to a plan installment, by version.';
COMMENT ON TABLE approval IS 'An item waiting for approval, routed to the level the delegation of authority requires.';
COMMENT ON TABLE signature_request IS 'A request for a party to sign a generated document, and its result.';
COMMENT ON TABLE merge_field IS 'A merge code a template may use and the field that supplies its value, by catalog version.';
COMMENT ON TABLE retention_action IS 'What the monthly retention job did with one document.';
COMMENT ON TABLE document_text IS 'The OCR text of one page of an intake item.';
COMMENT ON TABLE document_intake IS 'A file received by the document hub, from scan to OCR, classification, extraction, matching and review.';
COMMENT ON TABLE document_hub_parameter IS 'A document hub parameter value, by version.';
COMMENT ON TABLE case_document_check IS 'The latest document completeness check of a case against its checklist.';
COMMENT ON TABLE document_checklist_item IS 'A document type required or expected for a case stage and route, by checklist version.';
COMMENT ON TABLE document_type IS 'A document type, the fields extracted from it and its Legal and NPA sign-off, by version.';
COMMENT ON TABLE partner_user IS 'A partner user''s identity bound to one partner firm and one partner role.';
COMMENT ON TABLE role_conflict IS 'A pair of roles one person may not hold together, by version.';
COMMENT ON TABLE masking_rule IS 'Which role sees which personal data field unmasked, by version.';
COMMENT ON TABLE rule_test_case IS 'A test case of the rule table test harness, with its expected and actual result.';
COMMENT ON TABLE reference_row IS 'One row of a reference table version held as data.';
COMMENT ON TABLE reference_version IS 'One version of a reference or rule table, with its author, approver, checks and change checklist.';
COMMENT ON TABLE parameter_value IS 'An approved, dated value version of a parameter per environment and product group.';
COMMENT ON TABLE parameter_catalog IS 'The definition of every parameter and environment setting, with its owner and default.';
COMMENT ON TABLE queue_measure IS 'One snapshot of a queue''s counts, ageing and breaches, published when it reconciles to the case list.';
COMMENT ON TABLE queue_member IS 'A person who works a queue, with personal capacity and skills, by version.';
COMMENT ON TABLE case_entry_exclusion IS 'An account at 90 days past due that an exclusion rule kept out of recovery on a business date.';
COMMENT ON TABLE efs_ledger_outcome IS 'Which EFS action codes enter the interaction ledger and on which channel.';
COMMENT ON TABLE party_product IS 'Another product the party holds at the bank, from the customer profile.';
COMMENT ON TABLE job_catalog IS 'A scheduled job with its owner, run book and expected duration.';
COMMENT ON TABLE feature_flag_change IS 'One change of a feature flag value in one environment.';
COMMENT ON TABLE feature_flag IS 'A feature flag with its value per environment, owner and removal date.';
COMMENT ON TABLE outbox_delivery IS 'The delivery of one outbox event to one consumer, with its retries.';
COMMENT ON TABLE outbox_event IS 'An application event or outbound work request written in the same transaction as the change.';
COMMENT ON TABLE idempotency_key IS 'The stored response of an API request sent with an Idempotency-Key header, kept 24 hours.';
COMMENT ON TABLE processed_event IS 'An event or work key a consumer has already processed, so a repeat is ignored and counted.';
COMMENT ON TABLE outbound_item IS 'One outbound file waiting to be sent, sent or in the exception queue.';
COMMENT ON TABLE interface_signoff IS 'The data steward''s sign-off that an interface no longer needs manual handling.';
COMMENT ON TABLE interface_run IS 'One inbound file received by the adapter and the result of its file checks.';
COMMENT ON TABLE interface_config IS 'The settings of one file interface, by version.';
COMMENT ON TABLE dp_guarantee_claim IS 'The copy of each guarantee claim for a business date in the DP04 data product.';
COMMENT ON TABLE dp_treatment IS 'The copy of each treatment for a business date in the DP04 data product.';
COMMENT ON TABLE retention_rule IS 'How long rows of a table or a retention class are kept and what happens at the end, by version.';
COMMENT ON TABLE lake_copy_watermark IS 'How far a copy to the data lake has reached, for example the decision log copy.';
COMMENT ON TABLE reconciliation_result IS 'The daily reconciliation of the case list to ALS by product group.';
COMMENT ON TABLE collections_history IS 'An EFS contact or promise on an account, loaded from the COLLINS daily batch.';
COMMENT ON TABLE case_list_row IS 'One row of the daily case list per case account and business date, published to Power BI.';
COMMENT ON TABLE tracker_row IS 'One row loaded from a tracker file, with its non-personal fields.';
COMMENT ON TABLE tracker_inventory IS 'A team''s Excel or SharePoint tracker, its decision and its load, sign-off and retirement.';
COMMENT ON TABLE source_code_map IS 'How a source code maps to a Workbench list value, by interface and map version.';
COMMENT ON TABLE source_field_map IS 'How a source field maps to a Workbench field, by interface and mapping version.';
COMMENT ON TABLE dq_rule IS 'A versioned data quality row rule run on a P1 table.';
COMMENT ON TABLE dq_exception IS 'A record a load check or data quality rule held, until it passes again.';
COMMENT ON TABLE load_run IS 'One run of a data load or job step, with its checks and row counts.';
COMMENT ON TABLE sys_field_version IS 'Each version of a field definition, kept when the definition changes.';
COMMENT ON TABLE sys_fields IS 'The metadata registry of fields: the data dictionary held as data.';
COMMENT ON TABLE sys_objects IS 'The metadata registry of entities: one row per object in the data dictionary.';
COMMENT ON TABLE data_contract IS 'A versioned data contract with one source system, confirmed by its system owner.';
COMMENT ON TABLE data_product_load IS 'The freshness stamp of a data product for one business date.';
COMMENT ON TABLE data_product_access IS 'Which role may read which data product, by version.';
COMMENT ON TABLE data_product IS 'One of the 14 data products, with its single system of record, owner and refresh cycle.';
COMMENT ON TABLE template IS 'A letter or notice template.';
COMMENT ON TABLE permission IS 'What a role may do in one capability area.';
COMMENT ON TABLE role IS 'A Workbench role, held as data.';
COMMENT ON TABLE lov_value IS 'A value in a list of values.';
COMMENT ON TABLE delegation_limit IS 'An approval limit by decision, level, product and amount.';
COMMENT ON TABLE rule_row IS 'One versioned routing rule or sentry.';
COMMENT ON TABLE write_off IS 'A write-off of the balance on a case.';
COMMENT ON TABLE proceeds IS 'Money received on a case and what it was matched to.';
COMMENT ON TABLE score IS 'A score or estimate COLLINS returns for an account or case.';
COMMENT ON TABLE decision_log_entry IS 'One record per decision. Append only and hash chained.';
COMMENT ON TABLE document_custody IS 'Each movement of an original document.';
COMMENT ON TABLE document_field IS 'A field read from a document.';
COMMENT ON TABLE document IS 'A document held against a case.';
COMMENT ON TABLE interaction IS 'One entry in the interaction ledger: a contact, letter, promise, payment or hand-over.';
COMMENT ON TABLE debt_sale_account IS 'An account in a debt sale lot.';
COMMENT ON TABLE debt_sale_lot IS 'A lot of accounts offered to debt buyers.';
COMMENT ON TABLE asset_sale IS 'The sale of an asset.';
COMMENT ON TABLE listing IS 'An asset offered for sale, with its prices and rounds.';
COMMENT ON TABLE partner_instruction IS 'Work placed with a partner on a case.';
COMMENT ON TABLE partner IS 'An outside firm the bank places work with.';
COMMENT ON TABLE hearing IS 'A court hearing on a legal action.';
COMMENT ON TABLE notice IS 'A demand, recall or statutory notice and its proof of delivery.';
COMMENT ON TABLE legal_action IS 'A notice, lawsuit, appeal, enforcement or bankruptcy action on a case.';
COMMENT ON TABLE guarantee_claim IS 'A claim against a Thai Credit Guarantee Corporation guarantee or an insurer.';
COMMENT ON TABLE treatment IS 'A resolution put to the customer or carried out on the case, with its terms and outcome.';
COMMENT ON TABLE asset IS 'An asset the bank holds after repossession, deed in lieu or auction purchase.';
COMMENT ON TABLE valuation IS 'An appraisal of collateral or an asset.';
COMMENT ON TABLE account_collateral IS 'Which collateral secures which account.';
COMMENT ON TABLE collateral IS 'Property or vehicle securing one or more accounts.';
COMMENT ON TABLE account_payment IS 'A payment posted to a loan account.';
COMMENT ON TABLE loan_account IS 'A loan account in the core bank.';
COMMENT ON TABLE contact_point IS 'A way to reach a party, with its consent and whether it works.';
COMMENT ON TABLE party IS 'A person or company with a role on one or more cases.';
COMMENT ON TABLE timer IS 'A running clock on a case: a service level, a legal period or an offer validity.';
COMMENT ON TABLE task IS 'A unit of work on a case: a CMMN human, customer, partner or decision task.';
COMMENT ON TABLE assignment IS 'Who holds a case or a task and from when.';
COMMENT ON TABLE queue IS 'A queue of work belonging to one team and one role.';
COMMENT ON TABLE deviation IS 'A deviation X1 to X7 raised on a case.';
COMMENT ON TABLE case_party IS 'The role each party plays on a case.';
COMMENT ON TABLE case_account IS 'Links each loan account to the case it is recovered under.';
COMMENT ON TABLE recovery_case IS 'One recovery case per customer per product, from 90 days past due to close.';
COMMENT ON COLUMN recovery_case.id IS 'Record identifier of the case';
COMMENT ON COLUMN recovery_case.case_no IS 'Case number RW-YYYY-NNNNNN, issued at creation and never reused';
COMMENT ON COLUMN recovery_case.product_group IS 'Mortgage, hire purchase, SSME or unsecured';
COMMENT ON COLUMN recovery_case.primary_customer_id IS 'The borrower the case is opened for';
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
COMMENT ON COLUMN case_account.account_id IS 'The loan_account this record belongs to';
COMMENT ON COLUMN case_account.is_primary IS 'True for the account the case was opened on';
COMMENT ON COLUMN case_account.linked_from IS 'Date the account joined the case';
COMMENT ON COLUMN case_account.linked_to IS 'Date the account left the case';
COMMENT ON COLUMN case_party.id IS 'Record identifier of the case party link';
COMMENT ON COLUMN case_party.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN case_party.party_id IS 'The party this record belongs to';
COMMENT ON COLUMN case_party.party_role IS 'Borrower, co-borrower, guarantor, authorized signatory, heir';
COMMENT ON COLUMN case_party.role_from IS 'Date the role starts';
COMMENT ON COLUMN case_party.role_to IS 'Date the role ends';
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
COMMENT ON COLUMN party.id IS 'Record identifier of the party';
COMMENT ON COLUMN party.cif_no IS 'Customer number in the bank';
COMMENT ON COLUMN party.party_type IS 'Individual or juristic person';
COMMENT ON COLUMN party.first_name IS 'First name or company name';
COMMENT ON COLUMN party.last_name IS 'Last name';
COMMENT ON COLUMN party.id_type IS 'Thai national ID, passport, company registration';
COMMENT ON COLUMN party.id_no_token IS 'Tokenized identity number. The clear value is never stored in the Workbench';
COMMENT ON COLUMN party.date_of_birth IS 'Date of birth';
COMMENT ON COLUMN party.segment IS 'Retail, SSME, corporate';
COMMENT ON COLUMN party.vulnerable_flag IS 'Vulnerable customer or hardship confirmed';
COMMENT ON COLUMN party.deceased_flag IS 'Death confirmed';
COMMENT ON COLUMN party.bankruptcy_flag IS 'Bankruptcy or receivership confirmed';
COMMENT ON COLUMN party.fraud_flag IS 'True while fraud is confirmed or under investigation for the party';
COMMENT ON COLUMN contact_point.id IS 'Record identifier of the contact point';
COMMENT ON COLUMN contact_point.party_id IS 'The party this record belongs to';
COMMENT ON COLUMN contact_point.channel IS 'Mobile, home phone, work phone, LINE, email, postal address';
COMMENT ON COLUMN contact_point.value_token IS 'The number, handle or address, stored masked';
COMMENT ON COLUMN contact_point.source IS 'Bank record, field visit, agency, bureau trace, customer';
COMMENT ON COLUMN contact_point.consent_status IS 'Given, withdrawn, unknown';
COMMENT ON COLUMN contact_point.verified_at IS 'When it last reached the right party';
COMMENT ON COLUMN contact_point.failed_count IS 'Failed attempts since last success';
COMMENT ON COLUMN loan_account.id IS 'Record identifier of the account';
COMMENT ON COLUMN loan_account.account_no IS 'Account number';
COMMENT ON COLUMN loan_account.contract_no IS 'Contract number';
COMMENT ON COLUMN loan_account.product_code IS 'Core bank product code';
COMMENT ON COLUMN loan_account.product_category_efs IS 'Product category in EFS';
COMMENT ON COLUMN loan_account.business_unit IS 'Owning business unit';
COMMENT ON COLUMN loan_account.contract_date IS 'Contract date';
COMMENT ON COLUMN loan_account.interest_rate IS 'Contract interest rate, percent';
COMMENT ON COLUMN loan_account.principal_outstanding IS 'Principal outstanding, baht';
COMMENT ON COLUMN loan_account.interest_outstanding IS 'Accrued interest outstanding, baht';
COMMENT ON COLUMN loan_account.fees_outstanding IS 'Fees outstanding, baht';
COMMENT ON COLUMN loan_account.total_balance IS 'Total balance, baht';
COMMENT ON COLUMN loan_account.accounting_balance IS 'Accounting balance, baht';
COMMENT ON COLUMN loan_account.days_past_due IS 'Days past due';
COMMENT ON COLUMN loan_account.bucket IS 'Arrears bucket, for example 91-120, 180+';
COMMENT ON COLUMN loan_account.classification IS 'Loan classification and stage';
COMMENT ON COLUMN loan_account.last_payment_date IS 'Date of the last payment';
COMMENT ON COLUMN loan_account.next_installment_date IS 'Next installment date';
COMMENT ON COLUMN loan_account.tdr_flag IS 'True when the account is under a restructure';
COMMENT ON COLUMN loan_account.last_tdr_date IS 'Date of the last restructure';
COMMENT ON COLUMN loan_account.data_as_of IS 'The business date of the load';
COMMENT ON COLUMN loan_account.dispute_open IS 'True while the customer disputes the balance or the security on the account';
COMMENT ON COLUMN loan_account.settlement_booked_date IS 'Date a settlement was booked in ALS; source field to confirm with the system owner';
COMMENT ON COLUMN loan_account.settlement_booked_amount IS 'Settlement amount booked in ALS, baht; source field to confirm with the system owner';
COMMENT ON COLUMN account_payment.id IS 'Record identifier of the account payment';
COMMENT ON COLUMN account_payment.account_id IS 'The loan_account this record belongs to';
COMMENT ON COLUMN account_payment.payment_code IS 'Payment reference';
COMMENT ON COLUMN account_payment.payment_date IS 'Value date';
COMMENT ON COLUMN account_payment.payment_amount IS 'Amount, baht';
COMMENT ON COLUMN account_payment.payment_channel IS 'Channel the payment came through';
COMMENT ON COLUMN account_payment.data_as_of IS 'The business date of the load';
COMMENT ON COLUMN collateral.id IS 'Record identifier of the collateral';
COMMENT ON COLUMN collateral.collateral_no IS 'Collateral number';
COMMENT ON COLUMN collateral.collateral_type IS 'Land, house, condominium, vehicle, deposit, other';
COMMENT ON COLUMN collateral.title_doc_no IS 'Title deed or registration number';
COMMENT ON COLUMN collateral.plot_no IS 'Plot number';
COMMENT ON COLUMN collateral.area_text IS 'Land area in rai-ngan-wa';
COMMENT ON COLUMN collateral.province IS 'Province';
COMMENT ON COLUMN collateral.district IS 'District';
COMMENT ON COLUMN collateral.subdistrict IS 'Subdistrict';
COMMENT ON COLUMN collateral.occupancy IS 'Occupied by owner, tenant, vacant, unknown';
COMMENT ON COLUMN collateral.encumbrance_status IS 'Clear, other creditor, seized, under dispute';
COMMENT ON COLUMN collateral.insured_value IS 'Insured value, baht';
COMMENT ON COLUMN collateral.insurance_expiry IS 'Insurance expiry date';
COMMENT ON COLUMN account_collateral.id IS 'Record identifier of the account collateral link';
COMMENT ON COLUMN account_collateral.account_id IS 'The loan_account this record belongs to';
COMMENT ON COLUMN account_collateral.collateral_id IS 'The collateral this record belongs to';
COMMENT ON COLUMN account_collateral.lien_rank IS 'Rank of the bank''s lien';
COMMENT ON COLUMN valuation.id IS 'Record identifier of the valuation';
COMMENT ON COLUMN valuation.collateral_id IS 'The collateral this record belongs to';
COMMENT ON COLUMN valuation.asset_id IS 'The asset this record belongs to';
COMMENT ON COLUMN valuation.appraisal_no IS 'Appraisal number';
COMMENT ON COLUMN valuation.appraisal_type IS 'Market, official, forced sale, desktop, agent estimate';
COMMENT ON COLUMN valuation.appraised_value IS 'Appraised value, baht';
COMMENT ON COLUMN valuation.forced_sale_value IS 'Forced sale value, baht';
COMMENT ON COLUMN valuation.appraisal_date IS 'Appraisal date';
COMMENT ON COLUMN valuation.valuer_partner_id IS 'The valuer';
COMMENT ON COLUMN valuation.accepted IS 'True once accepted for the route decision';
COMMENT ON COLUMN valuation.stale_flag IS 'True when the appraisal is older than appraisal.max.age at the load business date';
COMMENT ON COLUMN valuation.age_days IS 'Age of the appraisal in days at the load business date';
COMMENT ON COLUMN asset.id IS 'Record identifier of the asset';
COMMENT ON COLUMN asset.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN asset.collateral_id IS 'The collateral this record belongs to';
COMMENT ON COLUMN asset.asset_ref IS 'Asset reference';
COMMENT ON COLUMN asset.asset_code IS 'Asset code';
COMMENT ON COLUMN asset.asset_type IS 'Detached house, townhouse, condominium, land, vehicle';
COMMENT ON COLUMN asset.transfer_in_type IS 'Auction purchase, deed in lieu, repossession';
COMMENT ON COLUMN asset.from_segment IS 'Segment the asset came from';
COMMENT ON COLUMN asset.transfer_in_date IS 'Date ownership passed to the bank';
COMMENT ON COLUMN asset.book_value IS 'Book value, baht';
COMMENT ON COLUMN asset.auction_purchase_price IS 'Price paid at auction, baht';
COMMENT ON COLUMN asset.repossessed_date IS 'Date the vehicle was repossessed';
COMMENT ON COLUMN asset.stock_date IS 'Date the vehicle entered stock';
COMMENT ON COLUMN asset.holding_status IS 'Held, listed, under offer, sold, transferred, rented';
COMMENT ON COLUMN asset.holding_cost_to_date IS 'Holding cost to date, baht';
COMMENT ON COLUMN treatment.id IS 'Record identifier of the treatment';
COMMENT ON COLUMN treatment.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN treatment.decision_log_id IS 'The decision that approved it';
COMMENT ON COLUMN treatment.treatment_type IS 'Restructure, settlement, deed in lieu, buy-back, guarantee claim, repossession, auction, debt sale, write-off, RAMC transfer, rental';
COMMENT ON COLUMN treatment.proposed_by IS 'Agent, rule, person';
COMMENT ON COLUMN treatment.proposed_at IS 'When proposed';
COMMENT ON COLUMN treatment.offer_amount IS 'Amount offered or agreed, baht';
COMMENT ON COLUMN treatment.haircut_amount IS 'Amount forgiven, baht';
COMMENT ON COLUMN treatment.installments IS 'Number of installments in a plan';
COMMENT ON COLUMN treatment.valid_until IS 'Offer validity';
COMMENT ON COLUMN treatment.approval_level IS 'Approval level that approved it';
COMMENT ON COLUMN treatment.booked_at IS 'When booked in the core';
COMMENT ON COLUMN treatment.outcome IS 'Kept, broken, completed, canceled, declined';
COMMENT ON COLUMN treatment.outcome_at IS 'When the outcome was recorded';
COMMENT ON COLUMN treatment.nleads_ref IS 'NLEADS reference of the credit approval';
COMMENT ON COLUMN treatment.credit_result IS 'Approved or refused, from NLEADS';
COMMENT ON COLUMN treatment.credit_result_reason IS 'Reason given by NLEADS; required when refused';
COMMENT ON COLUMN treatment.credit_result_at IS 'When the result was given in NLEADS';
COMMENT ON COLUMN treatment.interest_rate IS 'Approved interest rate of the plan, percent';
COMMENT ON COLUMN treatment.booking_difference IS 'Each term that differs between approval and booking: term, approved, booked, business date';
COMMENT ON COLUMN treatment.first_due_date IS 'Date the first installment is due';
COMMENT ON COLUMN treatment.signature_status IS 'Pending, signed or not signed, read by the routing rules';
COMMENT ON COLUMN treatment.installment_amount IS 'Amount due per plan installment, baht';
COMMENT ON COLUMN treatment.installments_paid IS 'Installments matched so far';
COMMENT ON COLUMN treatment.installment_shortfall IS 'Shortfall left on the plan by a partial payment, baht';
COMMENT ON COLUMN guarantee_claim.id IS 'Record identifier of the guarantee claim';
COMMENT ON COLUMN guarantee_claim.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN guarantee_claim.claim_type IS 'TCG, credit life insurance, mortgage insurance, collateral insurance';
COMMENT ON COLUMN guarantee_claim.claim_deadline IS 'Last date the claim can be filed';
COMMENT ON COLUMN guarantee_claim.claimed_amount IS 'Amount claimed, baht';
COMMENT ON COLUMN guarantee_claim.filed_at IS 'Date filed';
COMMENT ON COLUMN guarantee_claim.paid_amount IS 'Amount paid, baht';
COMMENT ON COLUMN guarantee_claim.status IS 'Preparing, filed, defect, paid, rejected';
COMMENT ON COLUMN legal_action.id IS 'Record identifier of the legal action';
COMMENT ON COLUMN legal_action.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN legal_action.law_firm_id IS 'The law firm instructed';
COMMENT ON COLUMN legal_action.action_type IS 'Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction';
COMMENT ON COLUMN legal_action.lawsuit_no IS 'Lawsuit reference in LIT';
COMMENT ON COLUMN legal_action.black_case_no IS 'Court black case number';
COMMENT ON COLUMN legal_action.red_case_no IS 'Court red case number after judgment';
COMMENT ON COLUMN legal_action.court_name IS 'Court';
COMMENT ON COLUMN legal_action.claim_amount IS 'Amount sued for, baht';
COMMENT ON COLUMN legal_action.filed_date IS 'Date filed';
COMMENT ON COLUMN legal_action.judgment_date IS 'Date of judgment';
COMMENT ON COLUMN legal_action.judgment_amount IS 'Amount awarded, baht';
COMMENT ON COLUMN legal_action.lit_status IS 'Latest status text in LIT';
COMMENT ON COLUMN legal_action.status IS 'Open, filed, judgment, enforcing, closed, withdrawn';
COMMENT ON COLUMN notice.id IS 'Record identifier of the notice';
COMMENT ON COLUMN notice.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN notice.document_id IS 'The generated notice';
COMMENT ON COLUMN notice.notice_type IS 'Demand, recall, statutory sale notice, guarantor notice';
COMMENT ON COLUMN notice.sent_date IS 'Date sent';
COMMENT ON COLUMN notice.barcode IS 'Registered mail barcode';
COMMENT ON COLUMN notice.callback_date IS 'Date the proof of delivery came back';
COMMENT ON COLUMN notice.delivery_status IS 'Delivered, refused, undeliverable, pending';
COMMENT ON COLUMN notice.sent_type IS 'Before NPL or NPL';
COMMENT ON COLUMN notice.party_id IS 'Party the notice is addressed to';
COMMENT ON COLUMN notice.template_id IS 'Template version the notice was generated from';
COMMENT ON COLUMN notice.hold_reason IS 'Why the notice is held: missing merge field, TEMPLATE_WITHDRAWN, CONTACT_STOP_Xn, LEGAL_HOLD';
COMMENT ON COLUMN notice.dispatch_file_id IS 'WIN file the notice was last written to';
COMMENT ON COLUMN notice.dispatch_attempts IS 'Number of WIN files the notice has been sent in without acknowledgment';
COMMENT ON COLUMN hearing.id IS 'Record identifier of the hearing';
COMMENT ON COLUMN hearing.legal_action_id IS 'The legal_action this record belongs to';
COMMENT ON COLUMN hearing.hearing_date IS 'Hearing date';
COMMENT ON COLUMN hearing.hearing_type IS 'First hearing, witness, judgment reading, mediation';
COMMENT ON COLUMN hearing.outcome IS 'Held, adjourned, settled, judgment';
COMMENT ON COLUMN hearing.next_date IS 'Next date set';
COMMENT ON COLUMN partner.id IS 'Record identifier of the partner';
COMMENT ON COLUMN partner.partner_code IS 'Partner code';
COMMENT ON COLUMN partner.partner_name IS 'Registered name';
COMMENT ON COLUMN partner.partner_type IS 'Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC';
COMMENT ON COLUMN partner.panel_status IS 'Active, on notice, suspended, exited';
COMMENT ON COLUMN partner.contract_end IS 'Contract end date';
COMMENT ON COLUMN partner.score IS 'Latest scorecard result';
COMMENT ON COLUMN partner_instruction.id IS 'Record identifier of the partner instruction';
COMMENT ON COLUMN partner_instruction.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN partner_instruction.partner_id IS 'The partner this record belongs to';
COMMENT ON COLUMN partner_instruction.instruction_type IS 'Collect, file suit, enforce, appraise, repossess, list, sell';
COMMENT ON COLUMN partner_instruction.instructed_at IS 'When instructed';
COMMENT ON COLUMN partner_instruction.due_at IS 'When the result is due';
COMMENT ON COLUMN partner_instruction.status IS 'Sent, accepted, declined, in progress, done, recalled';
COMMENT ON COLUMN partner_instruction.result_code IS 'Result reported by the partner';
COMMENT ON COLUMN partner_instruction.fee_amount IS 'Fee payable, baht';
COMMENT ON COLUMN listing.id IS 'Record identifier of the listing';
COMMENT ON COLUMN listing.asset_id IS 'The asset this record belongs to';
COMMENT ON COLUMN listing.sale_channel IS 'Dutch auction, broker, direct, LED auction, RAMC';
COMMENT ON COLUMN listing.start_price IS 'Start price, baht';
COMMENT ON COLUMN listing.floor_price IS 'Floor price approved, baht';
COMMENT ON COLUMN listing.round_no IS 'Current price round';
COMMENT ON COLUMN listing.listed_at IS 'When listed';
COMMENT ON COLUMN listing.status IS 'Draft, live, under offer, sold, withdrawn';
COMMENT ON COLUMN asset_sale.id IS 'Record identifier of the asset sale';
COMMENT ON COLUMN asset_sale.asset_id IS 'The asset this record belongs to';
COMMENT ON COLUMN asset_sale.listing_id IS 'The listing this record belongs to';
COMMENT ON COLUMN asset_sale.contract_date IS 'Sale contract date';
COMMENT ON COLUMN asset_sale.sale_date IS 'Sale date';
COMMENT ON COLUMN asset_sale.sale_price IS 'Sale price, baht';
COMMENT ON COLUMN asset_sale.transfer_fee IS 'Transfer fee, baht';
COMMENT ON COLUMN asset_sale.specific_business_tax IS 'Specific business tax, baht';
COMMENT ON COLUMN asset_sale.corporate_income_tax IS 'Corporate income tax, baht';
COMMENT ON COLUMN asset_sale.gain_loss IS 'Sale price less book value and costs';
COMMENT ON COLUMN asset_sale.incentive_amount IS 'Incentive paid on the sale, baht';
COMMENT ON COLUMN debt_sale_lot.id IS 'Record identifier of the debt sale lot';
COMMENT ON COLUMN debt_sale_lot.lot_no IS 'Lot number, for example 1/2024';
COMMENT ON COLUMN debt_sale_lot.cut_off_date IS 'Balance cut-off date';
COMMENT ON COLUMN debt_sale_lot.segment IS 'Segment of the lot';
COMMENT ON COLUMN debt_sale_lot.reserve_price IS 'Reserve price, baht';
COMMENT ON COLUMN debt_sale_lot.buyer_partner_id IS 'Winning buyer';
COMMENT ON COLUMN debt_sale_lot.buyer_class IS 'AMC or non-AMC';
COMMENT ON COLUMN debt_sale_lot.signing_date IS 'Date the sale was signed';
COMMENT ON COLUMN debt_sale_lot.approval_authority IS 'Authority that approved the sale';
COMMENT ON COLUMN debt_sale_lot.payment_terms IS 'Deposit and payment terms';
COMMENT ON COLUMN debt_sale_lot.status IS 'Building, offered, awarded, transferred, closed';
COMMENT ON COLUMN debt_sale_account.id IS 'Record identifier of the debt sale account';
COMMENT ON COLUMN debt_sale_account.lot_id IS 'The debt_sale_lot this record belongs to';
COMMENT ON COLUMN debt_sale_account.account_id IS 'The loan_account this record belongs to';
COMMENT ON COLUMN debt_sale_account.borrower_code IS 'Borrower code';
COMMENT ON COLUMN debt_sale_account.outstanding IS 'Outstanding at cut-off, baht';
COMMENT ON COLUMN debt_sale_account.selling_price IS 'Price allocated to the account, baht';
COMMENT ON COLUMN debt_sale_account.put_back_status IS 'None, claimed, accepted, rejected';
COMMENT ON COLUMN interaction.id IS 'Record identifier of the interaction';
COMMENT ON COLUMN interaction.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN interaction.party_id IS 'The party this record belongs to';
COMMENT ON COLUMN interaction.occurred_at IS 'When it happened';
COMMENT ON COLUMN interaction.channel IS 'Call, visit, SMS, LINE, email, letter, portal, branch; empty for Workbench events such as CASE_CREATED';
COMMENT ON COLUMN interaction.direction IS 'Inbound or outbound; empty for Workbench events such as CASE_CREATED';
COMMENT ON COLUMN interaction.action_code IS 'Action code';
COMMENT ON COLUMN interaction.contact_result IS 'Right party, third party, no answer, wrong number';
COMMENT ON COLUMN interaction.promise_amount IS 'Amount promised, baht';
COMMENT ON COLUMN interaction.promise_date IS 'Date promised';
COMMENT ON COLUMN interaction.summary IS 'Summary of what was said';
COMMENT ON COLUMN interaction.conduct_check IS 'Passed, blocked, not applicable';
COMMENT ON COLUMN interaction.source_system IS 'EFS for collections history, or the Workbench';
COMMENT ON COLUMN interaction.event_code IS 'Ledger event';
COMMENT ON COLUMN interaction.actor_type IS 'User, service or partner';
COMMENT ON COLUMN interaction.actor_ref IS 'User ID or service identity code that acted';
COMMENT ON COLUMN interaction.source_ref IS 'Producing module and event, or the interface, for example EV-02 CaseAllocated or INT-07';
COMMENT ON COLUMN interaction.idempotency_key IS 'Unique key of the event or request; repeats are rejected; unique on its own';
COMMENT ON COLUMN interaction.case_seq IS 'Gap-free sequence of the entry within its case; unique with case_id';
COMMENT ON COLUMN interaction.decision_log_id IS 'Decision log entry the entry records, for DECISION_TAKEN';
COMMENT ON COLUMN interaction.corrects_entry_id IS 'Entry this entry corrects';
COMMENT ON COLUMN interaction.contact_point_id IS 'The contact point reached; the number or address stays masked in contact_point';
COMMENT ON COLUMN interaction.from_holder_ref IS 'Who held the case before a hand-over: USER:<user id> or PARTNER:<partner code>';
COMMENT ON COLUMN interaction.to_holder_ref IS 'Who holds the case after a hand-over: USER:<user id> or PARTNER:<partner code>';
COMMENT ON COLUMN interaction.treatment_id IS 'The treatment offered, for an OFFER entry';
COMMENT ON COLUMN interaction.proceeds_id IS 'The proceeds matched, for a PAYMENT entry';
COMMENT ON COLUMN interaction.retention_class IS 'Retention class of the entry, set by entry type';
COMMENT ON COLUMN interaction.delivery_status IS 'Delivery state of an outbound SMS, LINE message or letter';
COMMENT ON COLUMN interaction.external_ref IS 'Reference returned by NSS, LINE OA or WIN';
COMMENT ON COLUMN document.id IS 'Record identifier of the document';
COMMENT ON COLUMN document.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN document.party_id IS 'The party this record belongs to';
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
COMMENT ON COLUMN score.id IS 'Record identifier of the score';
COMMENT ON COLUMN score.account_id IS 'The loan_account this record belongs to';
COMMENT ON COLUMN score.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN score.model_code IS 'Model, for example CRR_RET_380 asset pricing';
COMMENT ON COLUMN score.model_version IS 'Model version';
COMMENT ON COLUMN score.score_value IS 'Score';
COMMENT ON COLUMN score.estimate_value IS 'Estimated amount, baht, for example return by route or sale price';
COMMENT ON COLUMN score.route_code IS 'Route the estimate is for';
COMMENT ON COLUMN score.scored_at IS 'Score date';
COMMENT ON COLUMN proceeds.id IS 'Record identifier of the proceeds';
COMMENT ON COLUMN proceeds.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN proceeds.treatment_id IS 'The treatment this record belongs to';
COMMENT ON COLUMN proceeds.account_payment_id IS 'The account_payment this record belongs to';
COMMENT ON COLUMN proceeds.source IS 'Customer, LED, auction, buyer, agency, insurer, guarantor';
COMMENT ON COLUMN proceeds.amount IS 'Amount, baht';
COMMENT ON COLUMN proceeds.received_date IS 'Date received';
COMMENT ON COLUMN proceeds.matched_to IS 'Installment, settlement, fee, sale proceeds, unmatched';
COMMENT ON COLUMN proceeds.posting_ref IS 'Posting reference in the core or GL';
COMMENT ON COLUMN write_off.id IS 'Record identifier of the write-off';
COMMENT ON COLUMN write_off.case_id IS 'The recovery_case this record belongs to';
COMMENT ON COLUMN write_off.decision_log_id IS 'The decision_log_entry this record belongs to';
COMMENT ON COLUMN write_off.amount IS 'Amount written off, baht';
COMMENT ON COLUMN write_off.tax_criteria_met IS 'True when the tax criteria are met';
COMMENT ON COLUMN write_off.committee_date IS 'Committee approval date';
COMMENT ON COLUMN write_off.posted_date IS 'Posting date';
COMMENT ON COLUMN write_off.responsibility_center IS 'Responsibility center';
COMMENT ON COLUMN write_off.cost_center IS 'Operating cost center';
COMMENT ON COLUMN write_off.gl_product IS 'GL product code';
COMMENT ON COLUMN write_off.recovered_after IS 'Recovered after charge-off to date, baht';
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
COMMENT ON COLUMN lov_value.id IS 'Record identifier of the list value';
COMMENT ON COLUMN lov_value.lov_code IS 'List code, for example LOV-ROUTE';
COMMENT ON COLUMN lov_value.value_code IS 'Value code';
COMMENT ON COLUMN lov_value.label_en IS 'English label';
COMMENT ON COLUMN lov_value.label_th IS 'Thai label';
COMMENT ON COLUMN lov_value.sort_order IS 'Display order';
COMMENT ON COLUMN lov_value.valid_from IS 'Valid from';
COMMENT ON COLUMN role.id IS 'Record identifier of the role';
COMMENT ON COLUMN role.role_code IS 'Role code, for example RW-CASEOWN';
COMMENT ON COLUMN role.role_name IS 'Role name';
COMMENT ON COLUMN role.role_class IS 'Bank user, partner user, non-human actor';
COMMENT ON COLUMN role.default_scope IS 'Own, team, region, all';
COMMENT ON COLUMN role.entra_group IS 'Entra ID group mapped to the role';
COMMENT ON COLUMN permission.id IS 'Record identifier of the permission';
COMMENT ON COLUMN permission.role_id IS 'The role this record belongs to';
COMMENT ON COLUMN permission.capability_area IS 'One of the 14 capability areas';
COMMENT ON COLUMN permission.letters IS 'C, R, U, D and A, or a dash for none';
COMMENT ON COLUMN permission.matrix_version IS 'Permission matrix version';
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
COMMENT ON COLUMN data_product.id IS 'Record identifier of the data product';
COMMENT ON COLUMN data_product.product_code IS 'Data product code DP01 to DP14';
COMMENT ON COLUMN data_product.product_name IS 'Data product name, for example Account and arrears';
COMMENT ON COLUMN data_product.definition IS 'Definition of the product';
COMMENT ON COLUMN data_product.system_of_record IS 'The one system of record for the product';
COMMENT ON COLUMN data_product.owner_role IS 'Role of the owner, normally RW-DATASTEW';
COMMENT ON COLUMN data_product.owner_user_id IS 'The named owner of the product; required by the catalog load, empty in the seed';
COMMENT ON COLUMN data_product.refresh_cycle IS 'Daily, weekly, monthly or on change';
COMMENT ON COLUMN data_product.expected_by IS 'Time the load is expected by, for example 08:00 or MON 08:00';
COMMENT ON COLUMN data_product.valid_from IS 'Date the catalog version comes into force';
COMMENT ON COLUMN data_product_access.id IS 'Record identifier of the data product access row';
COMMENT ON COLUMN data_product_access.product_code IS 'Data product the row grants';
COMMENT ON COLUMN data_product_access.role_code IS 'Role the row applies to';
COMMENT ON COLUMN data_product_access.can_read IS 'True when the role may read the product';
COMMENT ON COLUMN data_product_access.access_version IS 'Version of the access table, for example DPA-2026.11';
COMMENT ON COLUMN data_product_access.valid_from IS 'Date the row comes into force';
COMMENT ON COLUMN data_product_access.valid_to IS 'Date the row ends';
COMMENT ON COLUMN data_product_load.id IS 'Record identifier of the freshness stamp';
COMMENT ON COLUMN data_product_load.product_code IS 'Data product loaded';
COMMENT ON COLUMN data_product_load.source_system IS 'Source system of the load';
COMMENT ON COLUMN data_product_load.business_date IS 'Business date of the load';
COMMENT ON COLUMN data_product_load.source_extracted_at IS 'When the source extract was taken, from the COLLINS control record or the file';
COMMENT ON COLUMN data_product_load.loaded_at IS 'When the load committed in the Workbench';
COMMENT ON COLUMN data_product_load.status IS 'Loaded or stale';
COMMENT ON COLUMN data_product_load.stale_flagged_at IS 'When the product was flagged stale';
COMMENT ON COLUMN data_product_load.duplicate_count IS 'Repeat stamps ignored for the same product and business date';
COMMENT ON COLUMN data_contract.id IS 'Record identifier of the data contract';
COMMENT ON COLUMN data_contract.contract_code IS 'Contract code per source system, for example DC-ALS';
COMMENT ON COLUMN data_contract.source_system IS 'Source system';
COMMENT ON COLUMN data_contract.interface_id IS 'Interfaces covered, for example INT-01, INT-02';
COMMENT ON COLUMN data_contract.contract_version IS 'Contract version';
COMMENT ON COLUMN data_contract.status IS 'Draft, published or superseded';
COMMENT ON COLUMN data_contract.confirmed_by_role IS 'Role of the system owner who confirmed, for example ALS system owner';
COMMENT ON COLUMN data_contract.confirmed_on IS 'Date of the confirmation';
COMMENT ON COLUMN data_contract.confirmation_document_ref IS 'Stored confirmation from the system owner';
COMMENT ON COLUMN data_contract.published_at IS 'When the contract was published';
COMMENT ON COLUMN data_contract.published_by IS 'Who published the contract';
COMMENT ON COLUMN sys_objects.id IS 'Record identifier of the registered object';
COMMENT ON COLUMN sys_objects.object_name IS 'Table name';
COMMENT ON COLUMN sys_objects.business_name IS 'Business name of the object';
COMMENT ON COLUMN sys_objects.subject_area IS 'Subject area code';
COMMENT ON COLUMN sys_objects.data_product IS 'Data product the object belongs to, DP01 to DP14 or None';
COMMENT ON COLUMN sys_objects.system_of_record IS 'System of record of the object';
COMMENT ON COLUMN sys_objects.description IS 'What the object holds';
COMMENT ON COLUMN sys_fields.id IS 'Record identifier of the registered field';
COMMENT ON COLUMN sys_fields.field_id IS 'BR Field ID, for example DF-CAS-001';
COMMENT ON COLUMN sys_fields.object_name IS 'Table the field belongs to, from sys_objects';
COMMENT ON COLUMN sys_fields.field_name IS 'Column name; unique with object_name';
COMMENT ON COLUMN sys_fields.data_type IS 'TSD data type: TEXT, NUMBER, DATE, BOOLEAN, LOV, USER_REF, CROSS_REF, FORMULA or ATTACHMENT';
COMMENT ON COLUMN sys_fields.physical_type IS 'PostgreSQL type';
COMMENT ON COLUMN sys_fields.is_mandatory IS 'True when the field is required';
COMMENT ON COLUMN sys_fields.lov_code IS 'List of values the field takes its values from';
COMMENT ON COLUMN sys_fields.references_object IS 'Table a cross-reference field points to';
COMMENT ON COLUMN sys_fields.source_system IS 'Source system of the value';
COMMENT ON COLUMN sys_fields.source_field IS 'Field name in the source system';
COMMENT ON COLUMN sys_fields.is_personal IS 'True for personal data under PDPA';
COMMENT ON COLUMN sys_fields.description IS 'Meaning of the field';
COMMENT ON COLUMN sys_fields.owner_role IS 'Owner of the field definition';
COMMENT ON COLUMN sys_fields.refresh_cycle IS 'Refresh frequency, for example Daily, end of day';
COMMENT ON COLUMN sys_fields.late_behavior IS 'What the Workbench does when the value is missing or late';
COMMENT ON COLUMN sys_fields.interface_id IS 'Interface that carries the field, INT-01 to INT-34; empty for Workbench fields';
COMMENT ON COLUMN sys_field_version.id IS 'Record identifier of the field version';
COMMENT ON COLUMN sys_field_version.field_id IS 'Field the version belongs to, from sys_fields';
COMMENT ON COLUMN sys_field_version.field_version IS 'Version number';
COMMENT ON COLUMN sys_field_version.definition IS 'The full field definition at this version';
COMMENT ON COLUMN sys_field_version.change_reason IS 'Reason for the change';
COMMENT ON COLUMN load_run.id IS 'Record identifier of the load or job run';
COMMENT ON COLUMN load_run.interface_id IS 'Interface loaded, for example INT-01; TRACKER for tracker loads; empty for job steps';
COMMENT ON COLUMN load_run.job_code IS 'Job the run belongs to, for example JOB-01';
COMMENT ON COLUMN load_run.product_code IS 'Data product loaded or built';
COMMENT ON COLUMN load_run.business_date IS 'Business date of the load';
COMMENT ON COLUMN load_run.status IS 'Running, completed, refused, late, failed or superseded';
COMMENT ON COLUMN load_run.started_at IS 'When the run started';
COMMENT ON COLUMN load_run.ended_at IS 'When the run ended';
COMMENT ON COLUMN load_run.rows_read IS 'Records read from the source';
COMMENT ON COLUMN load_run.rows_loaded IS 'Records written';
COMMENT ON COLUMN load_run.rows_held IS 'Records held in the exception list';
COMMENT ON COLUMN load_run.rows_rejected IS 'Rows rejected';
COMMENT ON COLUMN load_run.failed_check IS 'Check that refused the load, for example DQ-003';
COMMENT ON COLUMN load_run.check_results IS 'Result per check code, plus the sample and other counts';
COMMENT ON COLUMN load_run.mapping_version IS 'Source field mapping version used';
COMMENT ON COLUMN load_run.interface_run_id IS 'The P2 interface run the file load belongs to';
COMMENT ON COLUMN load_run.tracker_id IS 'Tracker of a tracker load';
COMMENT ON COLUMN load_run.loaded_by IS 'User who uploaded the file';
COMMENT ON COLUMN load_run.source_file_name IS 'Name of the loaded file';
COMMENT ON COLUMN load_run.source_file_hash IS 'SHA-256 of the loaded file';
COMMENT ON COLUMN dq_exception.id IS 'Record identifier of the data quality exception';
COMMENT ON COLUMN dq_exception.load_run_id IS 'The load run that raised it';
COMMENT ON COLUMN dq_exception.product_code IS 'Data product of the record';
COMMENT ON COLUMN dq_exception.check_code IS 'Load check (DQ-nnn), row rule (DQnn), reconciliation (REC-nn) or tracker check (TRK-nn)';
COMMENT ON COLUMN dq_exception.record_key IS 'Business key of the failing record, for example the account number; never personal data';
COMMENT ON COLUMN dq_exception.reason_code IS 'Reason code shown to the data product owner';
COMMENT ON COLUMN dq_exception.detail IS 'Short reason without personal data';
COMMENT ON COLUMN dq_exception.raised_on IS 'Business date raised';
COMMENT ON COLUMN dq_exception.status IS 'Open or cleared';
COMMENT ON COLUMN dq_exception.rule_version IS 'Rule version that raised the exception';
COMMENT ON COLUMN dq_exception.cleared_on IS 'Date the record passed again';
COMMENT ON COLUMN dq_rule.id IS 'Record identifier of the data quality rule';
COMMENT ON COLUMN dq_rule.rule_code IS 'Rule code, for example DQ02';
COMMENT ON COLUMN dq_rule.rule_version IS 'Rule version';
COMMENT ON COLUMN dq_rule.rule_name IS 'Rule name';
COMMENT ON COLUMN dq_rule.product_code IS 'Data product the rule runs for';
COMMENT ON COLUMN dq_rule.target_entity IS 'P1 table the rule checks';
COMMENT ON COLUMN dq_rule.rule_type IS 'Not null, unique across, range, sum equals, exists link, maximum age in days, field before';
COMMENT ON COLUMN dq_rule.rule_params IS 'Fields and values for the rule type';
COMMENT ON COLUMN dq_rule.valid_from IS 'Date the version comes into force';
COMMENT ON COLUMN dq_rule.valid_to IS 'Last date the version is in force';
COMMENT ON COLUMN dq_rule.approved_by IS 'Who approved the version';
COMMENT ON COLUMN dq_rule.test_case_id IS 'Test case that proves the rule';
COMMENT ON COLUMN source_field_map.id IS 'Record identifier of the source field mapping';
COMMENT ON COLUMN source_field_map.interface_id IS 'Interface the mapping is for';
COMMENT ON COLUMN source_field_map.mapping_version IS 'Mapping version';
COMMENT ON COLUMN source_field_map.source_field IS 'Field name in the source';
COMMENT ON COLUMN source_field_map.target_entity IS 'Workbench entity';
COMMENT ON COLUMN source_field_map.target_field IS 'Workbench field';
COMMENT ON COLUMN source_field_map.transformation IS 'Transformation type and parameters: COPY_TRIM, SUM, TO_DATE_BE, TO_NUMERIC_2, BOOLEAN_YN, CODE_MAP, BUSINESS_DATE';
COMMENT ON COLUMN source_field_map.approved_by IS 'Who approved the mapping version';
COMMENT ON COLUMN source_field_map.approved_on IS 'Approval date';
COMMENT ON COLUMN source_field_map.approval_ref IS 'Reference of the system owner''s sign-off on the mapping version';
COMMENT ON COLUMN source_field_map.valid_from IS 'Date the version comes into force';
COMMENT ON COLUMN source_code_map.id IS 'Record identifier of the source code mapping';
COMMENT ON COLUMN source_code_map.interface_id IS 'Interface the code map is for';
COMMENT ON COLUMN source_code_map.lov_code IS 'Target list of values';
COMMENT ON COLUMN source_code_map.source_code IS 'Code in the source';
COMMENT ON COLUMN source_code_map.value_code IS 'Workbench list value';
COMMENT ON COLUMN source_code_map.map_version IS 'Code map version';
COMMENT ON COLUMN source_code_map.valid_from IS 'Date the version comes into force';
COMMENT ON COLUMN source_code_map.valid_to IS 'Last date the version is in force';
COMMENT ON COLUMN tracker_inventory.id IS 'Record identifier of the tracker';
COMMENT ON COLUMN tracker_inventory.tracker_code IS 'Tracker code';
COMMENT ON COLUMN tracker_inventory.inventory_version IS 'Inventory version';
COMMENT ON COLUMN tracker_inventory.team_code IS 'Owning team';
COMMENT ON COLUMN tracker_inventory.tracker_name IS 'Tracker name';
COMMENT ON COLUMN tracker_inventory.location_type IS 'Excel, SharePoint, local file or none';
COMMENT ON COLUMN tracker_inventory.location_ref IS 'Where the tracker is kept';
COMMENT ON COLUMN tracker_inventory.owner_user_id IS 'Tracker owner';
COMMENT ON COLUMN tracker_inventory.field_list IS 'Field names with the personal data tag and the optional mapped-to field';
COMMENT ON COLUMN tracker_inventory.update_cycle IS 'Daily, weekly, monthly or ad hoc';
COMMENT ON COLUMN tracker_inventory.target_product IS 'Target data product for a LOAD decision';
COMMENT ON COLUMN tracker_inventory.decision IS 'Load, retire or keep';
COMMENT ON COLUMN tracker_inventory.decision_reason IS 'Reason for the decision';
COMMENT ON COLUMN tracker_inventory.status IS 'Listed, loaded, signed off, retired or kept';
COMMENT ON COLUMN tracker_inventory.valid_from IS 'Date the inventory version comes into force';
COMMENT ON COLUMN tracker_inventory.file_rows IS 'Rows in the loaded file';
COMMENT ON COLUMN tracker_inventory.loaded_rows IS 'Rows loaded';
COMMENT ON COLUMN tracker_inventory.rejected_rows IS 'Rows rejected';
COMMENT ON COLUMN tracker_inventory.last_load_run_id IS 'Latest load run of the tracker';
COMMENT ON COLUMN tracker_inventory.signed_off_by IS 'Team manager who signed off the load';
COMMENT ON COLUMN tracker_inventory.signed_off_at IS 'Sign-off time';
COMMENT ON COLUMN tracker_inventory.source_file_ref IS 'Stored tracker file in the write-once store';
COMMENT ON COLUMN tracker_inventory.archive_ref IS 'Read-only archive location of the retired tracker';
COMMENT ON COLUMN tracker_inventory.retired_at IS 'Retirement time';
COMMENT ON COLUMN tracker_inventory.retire_confirmed_by IS 'Team manager who confirmed the retirement';
COMMENT ON COLUMN tracker_inventory.unfed_fields IS 'Non-personal tracker fields no data product field carries';
COMMENT ON COLUMN tracker_row.id IS 'Record identifier of the tracker row';
COMMENT ON COLUMN tracker_row.tracker_id IS 'Tracker the row came from';
COMMENT ON COLUMN tracker_row.load_run_id IS 'Load run that loaded the row';
COMMENT ON COLUMN tracker_row.row_no IS 'Row number in the file';
COMMENT ON COLUMN tracker_row.account_no IS 'Account number';
COMMENT ON COLUMN tracker_row.target_product IS 'Target data product';
COMMENT ON COLUMN tracker_row.source_file_name IS 'Source file name';
COMMENT ON COLUMN tracker_row.field_values IS 'Non-personal tracker fields of the row';
COMMENT ON COLUMN tracker_row.loaded_on IS 'Load date';
COMMENT ON COLUMN case_list_row.id IS 'Record identifier of the case list row';
COMMENT ON COLUMN case_list_row.business_date IS 'Business date of the list';
COMMENT ON COLUMN case_list_row.case_id IS 'Case';
COMMENT ON COLUMN case_list_row.case_no IS 'Case number';
COMMENT ON COLUMN case_list_row.account_id IS 'Loan account; unique with business_date';
COMMENT ON COLUMN case_list_row.account_no IS 'Account number';
COMMENT ON COLUMN case_list_row.product_group IS 'Product group';
COMMENT ON COLUMN case_list_row.stage_code IS 'Stage';
COMMENT ON COLUMN case_list_row.status IS 'Case status';
COMMENT ON COLUMN case_list_row.owner_user_id IS 'Case owner';
COMMENT ON COLUMN case_list_row.queue_code IS 'Queue code';
COMMENT ON COLUMN case_list_row.team_code IS 'Team';
COMMENT ON COLUMN case_list_row.route_code IS 'Route';
COMMENT ON COLUMN case_list_row.total_balance IS 'Total balance, baht';
COMMENT ON COLUMN case_list_row.days_past_due IS 'Days past due';
COMMENT ON COLUMN case_list_row.refreshed_at IS 'When the row was built';
COMMENT ON COLUMN case_list_row.last_contact_at IS 'Latest EFS contact across the case''s accounts';
COMMENT ON COLUMN case_list_row.last_action_code IS 'Action code of the latest contact';
COMMENT ON COLUMN case_list_row.publish_status IS 'Pending, held or released for the date''s extract';
COMMENT ON COLUMN collections_history.id IS 'Record identifier of the collections history record';
COMMENT ON COLUMN collections_history.account_no IS 'Account number';
COMMENT ON COLUMN collections_history.efs_record_key IS 'EFS record key';
COMMENT ON COLUMN collections_history.contact_at IS 'Contact date and time';
COMMENT ON COLUMN collections_history.action_code IS 'EFS action code';
COMMENT ON COLUMN collections_history.action_contact_status IS 'EFS action contact status';
COMMENT ON COLUMN collections_history.contact_result IS 'Call result';
COMMENT ON COLUMN collections_history.promise_amount IS 'Amount promised, baht';
COMMENT ON COLUMN collections_history.promise_date IS 'Date promised';
COMMENT ON COLUMN collections_history.business_date IS 'Business date of the load';
COMMENT ON COLUMN reconciliation_result.id IS 'Record identifier of the reconciliation result';
COMMENT ON COLUMN reconciliation_result.rec_code IS 'Reconciliation, REC-01 or REC-02';
COMMENT ON COLUMN reconciliation_result.business_date IS 'Business date';
COMMENT ON COLUMN reconciliation_result.product_group IS 'Product group';
COMMENT ON COLUMN reconciliation_result.source_count IS 'ALS count';
COMMENT ON COLUMN reconciliation_result.workbench_count IS 'Case list count';
COMMENT ON COLUMN reconciliation_result.source_amount IS 'ALS balance sum, baht';
COMMENT ON COLUMN reconciliation_result.workbench_amount IS 'Case list balance sum, baht';
COMMENT ON COLUMN reconciliation_result.variance_count IS 'Count difference';
COMMENT ON COLUMN reconciliation_result.variance_pct IS 'Variance, percent';
COMMENT ON COLUMN reconciliation_result.tolerance_pct IS 'Tolerance used, percent';
COMMENT ON COLUMN reconciliation_result.result IS 'Pass or break';
COMMENT ON COLUMN lake_copy_watermark.id IS 'Record identifier of the lake copy watermark';
COMMENT ON COLUMN lake_copy_watermark.copy_name IS 'Name of the copy; DECISION_LOG for the decision log lake copy';
COMMENT ON COLUMN lake_copy_watermark.last_entry_hash IS 'Entry hash of the last decision log entry copied and matched';
COMMENT ON COLUMN lake_copy_watermark.last_decided_at IS 'decided_at of the last entry copied';
COMMENT ON COLUMN lake_copy_watermark.rows_copied_total IS 'Cumulative count of entries in the lake copy';
COMMENT ON COLUMN lake_copy_watermark.business_date IS 'Business date of the last complete partition';
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
COMMENT ON COLUMN dp_treatment.id IS 'Record identifier of the treatment copy';
COMMENT ON COLUMN dp_treatment.treatment_id IS 'The treatment copied; unique with business_date';
COMMENT ON COLUMN dp_treatment.case_id IS 'The case of the treatment';
COMMENT ON COLUMN dp_treatment.decision_log_id IS 'The decision that approved the treatment';
COMMENT ON COLUMN dp_treatment.treatment_type IS 'Treatment type';
COMMENT ON COLUMN dp_treatment.proposed_by IS 'Agent, rule or person';
COMMENT ON COLUMN dp_treatment.proposed_at IS 'When proposed';
COMMENT ON COLUMN dp_treatment.offer_amount IS 'Amount offered or agreed, baht';
COMMENT ON COLUMN dp_treatment.haircut_amount IS 'Amount forgiven, baht';
COMMENT ON COLUMN dp_treatment.installments IS 'Number of installments in a plan';
COMMENT ON COLUMN dp_treatment.valid_until IS 'Offer validity';
COMMENT ON COLUMN dp_treatment.approval_level IS 'Approval level that approved it';
COMMENT ON COLUMN dp_treatment.booked_at IS 'When booked in the core';
COMMENT ON COLUMN dp_treatment.outcome IS 'Kept, broken, completed, canceled or declined';
COMMENT ON COLUMN dp_treatment.outcome_at IS 'When the outcome was recorded';
COMMENT ON COLUMN dp_treatment.business_date IS 'Business date of the build';
COMMENT ON COLUMN dp_treatment.contract_no IS 'Contract number of the case''s primary account';
COMMENT ON COLUMN dp_treatment.contract_date IS 'Contract date of the case''s primary account';
COMMENT ON COLUMN dp_guarantee_claim.id IS 'Record identifier of the guarantee claim copy';
COMMENT ON COLUMN dp_guarantee_claim.guarantee_claim_id IS 'The guarantee claim copied; unique with business_date';
COMMENT ON COLUMN dp_guarantee_claim.case_id IS 'The case of the claim';
COMMENT ON COLUMN dp_guarantee_claim.claim_type IS 'TCG, credit life insurance, mortgage insurance or collateral insurance';
COMMENT ON COLUMN dp_guarantee_claim.claim_deadline IS 'Last date the claim can be filed';
COMMENT ON COLUMN dp_guarantee_claim.claimed_amount IS 'Amount claimed, baht';
COMMENT ON COLUMN dp_guarantee_claim.filed_at IS 'Date filed';
COMMENT ON COLUMN dp_guarantee_claim.paid_amount IS 'Amount paid, baht';
COMMENT ON COLUMN dp_guarantee_claim.status IS 'Preparing, filed, defect, paid or rejected';
COMMENT ON COLUMN dp_guarantee_claim.business_date IS 'Business date of the build';
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
COMMENT ON COLUMN interface_run.id IS 'Record identifier of the interface run';
COMMENT ON COLUMN interface_run.interface_id IS 'Interface ID';
COMMENT ON COLUMN interface_run.file_name IS 'File name';
COMMENT ON COLUMN interface_run.file_hash IS 'SHA-256 of the file';
COMMENT ON COLUMN interface_run.business_date IS 'Business date of the file';
COMMENT ON COLUMN interface_run.record_count IS 'Records read';
COMMENT ON COLUMN interface_run.control_total IS 'Control total from the trailer';
COMMENT ON COLUMN interface_run.status IS 'Received, loaded, refused, missing, duplicate or failed';
COMMENT ON COLUMN interface_run.failed_check IS 'Load check ID and name that refused the file';
COMMENT ON COLUMN interface_run.checks IS 'Result of each check and the run summary counts';
COMMENT ON COLUMN interface_run.started_at IS 'Run start';
COMMENT ON COLUMN interface_run.ended_at IS 'Run end';
COMMENT ON COLUMN interface_signoff.id IS 'Record identifier of the interface sign-off';
COMMENT ON COLUMN interface_signoff.interface_id IS 'Interface whose manual handling is retired';
COMMENT ON COLUMN interface_signoff.from_date IS 'First clean day counted';
COMMENT ON COLUMN interface_signoff.to_date IS 'Last clean day counted';
COMMENT ON COLUMN interface_signoff.clean_days IS 'Clean days in a row at sign-off';
COMMENT ON COLUMN interface_signoff.signed_by IS 'Data steward who signed off';
COMMENT ON COLUMN interface_signoff.signed_at IS 'When signed off';
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
COMMENT ON COLUMN party_product.id IS 'Record identifier of the party product';
COMMENT ON COLUMN party_product.party_id IS 'The party that holds the product';
COMMENT ON COLUMN party_product.product_type IS 'Product type from the customer profile';
COMMENT ON COLUMN party_product.account_no IS 'Account number of the product, masked by role';
COMMENT ON COLUMN party_product.product_status IS 'Active, delinquent, closed or written off';
COMMENT ON COLUMN party_product.data_as_of IS 'Business date of the customer profile load';
COMMENT ON COLUMN efs_ledger_outcome.id IS 'Record identifier of the EFS ledger outcome row';
COMMENT ON COLUMN efs_ledger_outcome.action_code IS 'EFS action code named for the ledger';
COMMENT ON COLUMN efs_ledger_outcome.channel IS 'Ledger channel for the action code';
COMMENT ON COLUMN efs_ledger_outcome.in_ledger IS 'True when rows with this action code enter the ledger';
COMMENT ON COLUMN case_entry_exclusion.id IS 'Record identifier of the case entry exclusion';
COMMENT ON COLUMN case_entry_exclusion.account_id IS 'The account excluded; unique with business_date';
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
COMMENT ON COLUMN rule_test_case.id IS 'Record identifier of the rule test case';
COMMENT ON COLUMN rule_test_case.test_case_id IS 'The test case named by rule_row.test_case_id';
COMMENT ON COLUMN rule_test_case.route_set IS 'Route set';
COMMENT ON COLUMN rule_test_case.rule_version IS 'Rule version tested';
COMMENT ON COLUMN rule_test_case.rule_id IS 'Rule the test expects to hit';
COMMENT ON COLUMN rule_test_case.from_state IS 'Input state';
COMMENT ON COLUMN rule_test_case.event_code IS 'Input event';
COMMENT ON COLUMN rule_test_case.facts IS 'Synthetic case file facts the condition reads';
COMMENT ON COLUMN rule_test_case.expected_to_state IS 'Expected to state';
COMMENT ON COLUMN rule_test_case.expected_owner_role IS 'Expected owner role';
COMMENT ON COLUMN rule_test_case.expected_timer_spec IS 'Expected timer';
COMMENT ON COLUMN rule_test_case.result IS 'Passed or failed';
COMMENT ON COLUMN rule_test_case.result_detail IS 'Expected against actual, and the rows that hit';
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
COMMENT ON COLUMN partner_user.id IS 'Record identifier of the partner user';
COMMENT ON COLUMN partner_user.identity_ref IS 'Partner identity directory ID';
COMMENT ON COLUMN partner_user.partner_id IS 'The firm the partner user works for';
COMMENT ON COLUMN partner_user.role_code IS 'The one partner role held, for example PT-LAWFIRM';
COMMENT ON COLUMN partner_user.valid_from IS 'Date the binding starts';
COMMENT ON COLUMN partner_user.valid_to IS 'Date the binding ends; no later than the firm''s contract end';
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
COMMENT ON COLUMN merge_field.id IS 'Record identifier of the merge field';
COMMENT ON COLUMN merge_field.merge_code IS 'Code written in the template body, for example CASE_NO';
COMMENT ON COLUMN merge_field.source_entity IS 'Entity that holds the value';
COMMENT ON COLUMN merge_field.source_field IS 'Field that holds the value';
COMMENT ON COLUMN merge_field.field_id IS 'BR Field ID of the source field in the data dictionary';
COMMENT ON COLUMN merge_field.is_required IS 'True when generation holds on an empty value';
COMMENT ON COLUMN merge_field.personal_data IS 'True when the value is personal data, detokenized only at generation';
COMMENT ON COLUMN merge_field.catalog_version IS 'Version of the catalog load';
COMMENT ON COLUMN merge_field.valid_from IS 'Date the catalog version comes into force';
COMMENT ON COLUMN signature_request.id IS 'Record identifier of the signature request';
COMMENT ON COLUMN signature_request.case_id IS 'Case';
COMMENT ON COLUMN signature_request.treatment_id IS 'Treatment the agreement belongs to';
COMMENT ON COLUMN signature_request.document_id IS 'Generated document sent for signature';
COMMENT ON COLUMN signature_request.party_id IS 'Signing party';
COMMENT ON COLUMN signature_request.method IS 'E-signature, branch or paper';
COMMENT ON COLUMN signature_request.status IS 'Queued, sent, signed, declined or expired';
COMMENT ON COLUMN signature_request.external_ref IS 'EasyApp reference';
COMMENT ON COLUMN signature_request.sent_at IS 'When the request was sent';
COMMENT ON COLUMN signature_request.signed_at IS 'When the party signed';
COMMENT ON COLUMN signature_request.signed_document_id IS 'Signed copy or branch scan';
COMMENT ON COLUMN signature_request.expires_at IS 'End of the offer validity';
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
COMMENT ON COLUMN payment_match_rule.id IS 'Record identifier of the payment match rule';
COMMENT ON COLUMN payment_match_rule.rule_code IS 'Row code, for example EXACT';
COMMENT ON COLUMN payment_match_rule.rule_version IS 'Parameter version, for example PM-2026.12';
COMMENT ON COLUMN payment_match_rule.match_type IS 'Exact, window or partial';
COMMENT ON COLUMN payment_match_rule.amount_tolerance_pct IS 'Allowed difference from the installment, 0 to 100 percent';
COMMENT ON COLUMN payment_match_rule.window_days_before IS 'Days before the due date a payment may arrive';
COMMENT ON COLUMN payment_match_rule.window_days_after IS 'Days after the due date a payment may arrive';
COMMENT ON COLUMN payment_match_rule.grace_days IS 'Days after the due date before PaymentMissed is raised';
COMMENT ON COLUMN payment_match_rule.partial_floor_pct IS 'Lowest share of the installment matched as partial, percent';
COMMENT ON COLUMN payment_match_rule.priority IS 'Order in which rows are tried';
COMMENT ON COLUMN payment_match_rule.valid_from IS 'Date the version comes into force';
COMMENT ON COLUMN payment_match_rule.valid_to IS 'Last date the version is in force';
COMMENT ON COLUMN payment_match_rule.approved_by IS 'Credit Administration approver';
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

-- Seed: the metadata registry
-- Probe: the 14 data_product rows that Physical Schema v5 must seed before sys_objects.
INSERT INTO data_product (product_code, product_name, definition, system_of_record, owner_role, refresh_cycle, expected_by, valid_from) VALUES
('DP01','Account and arrears','Loan accounts with balances, interest, fees, days past due, bucket, classification, restructure flag and payments','ACE (ingested from ALS via COLLINS)','RW-DATASTEW','DAILY','08:00','2026-11-30'),
('DP02','Customer and party','Customers, guarantors, co-borrowers and heirs, tokenized identifiers, contact points, consent and flags for vulnerability, death and bankruptcy','ACE (ingested from SCBPDM and the core bank)','RW-DATASTEW','DAILY','08:00','2026-11-30'),
('DP03','Case and ownership','The case, its accounts and parties, status, stage, route, owner, queue, tasks, timers and deviations','Recovery Workbench','RW-DATASTEW','On change','ON_CHANGE','2026-11-30'),
('DP04','Treatment and offers','Restructures, settlements, deeds in lieu, buy-backs and guarantee claims, with terms, approval level and outcome','Recovery Workbench; restructure plans in ACE','RW-DATASTEW','On change','ON_CHANGE','2026-11-30'),
('DP05','Contact and promises','Every contact, letter, promise and hand-over on the case, in order, including the collections history from EFS','ACE (ingested from EFS) and the Workbench','RW-DATASTEW','DAILY','08:00','2026-11-30'),
('DP06','Collateral and assets','Collateral, appraisals, assets held after repossession or transfer, listings and sale results','ACE (ingested from CCMS, SVAF, AMIS and RPS)','RW-DATASTEW','WEEKLY','MON 08:00','2026-11-30'),
('DP07','Legal events and cases','Notices and proof of delivery, lawsuits, court case numbers, hearings, judgments and enforcement','ACE (ingested from LIT and WIN); the Workbench for instructions','RW-DATASTEW','DAILY','08:00','2026-11-30'),
('DP08','Partner performance','Partners on the panel, work placed with each, results, fees and scorecards','Recovery Workbench','RW-DATASTEW','On change','ON_CHANGE','2026-11-30'),
('DP09','Debt sale','Debt sale lots, the accounts in each lot, buyers, prices, approval and put-backs','Recovery Workbench','RW-DATASTEW','On change','ON_CHANGE','2026-11-30'),
('DP10','Documents and extracted fields','Documents against the case, the fields read from them, retention class and custody of originals','Recovery Workbench document hub','RW-DATASTEW','On change','ON_CHANGE','2026-11-30'),
('DP11','Scores and route economics','Risk scores, expected return by route, estimated sale price and sale success rate, restructure scheme suggestions','ACE (ingested from COLLINS)','RW-DATASTEW','DAILY','08:00','2026-11-30'),
('DP12','Decision log','One entry per decision with the rule, model and agent versions, inputs, recommendation, approval, actions and outcome','Recovery Workbench','RW-DATASTEW','On change','ON_CHANGE','2026-11-30'),
('DP13','Money and closure','Payments and proceeds matched to the case, write-off postings and recovery after charge-off','ACE (ingested from ALS and GL)','RW-DATASTEW','DAILY','08:00','2026-11-30'),
('DP14','Reference data','Rules, approval limits, lists of values, roles, permissions and letter templates, each versioned','Recovery Workbench','RW-DATASTEW','BY_LOAD','BY_LOAD','2026-11-30');


INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('recovery_case', 'Recovery case', 'CAS', 'DP03', 'Workbench', 'One recovery case per customer per product, from 90 days past due to close.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('case_account', 'Case account', 'CAS', 'DP03', 'Workbench', 'Links each loan account to the case it is recovered under.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('case_party', 'Case party', 'CAS', 'DP03', 'Workbench', 'The role each party plays on a case.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('deviation', 'Deviation', 'CAS', 'DP03', 'Workbench', 'A deviation X1 to X7 raised on a case.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('queue', 'Queue', 'WRK', 'DP03', 'Workbench', 'A queue of work belonging to one team and one role.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('assignment', 'Assignment', 'WRK', 'DP03', 'Workbench', 'Who holds a case or a task and from when.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('task', 'Task', 'WRK', 'DP03', 'Workbench', 'A unit of work on a case: a CMMN human, customer, partner or decision task.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('timer', 'Timer', 'WRK', 'DP03', 'Workbench', 'A running clock on a case: a service level, a legal period or an offer validity.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('party', 'Party', 'PTY', 'DP02', 'SCBPDM via COLLINS', 'A person or company with a role on one or more cases.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('contact_point', 'Contact point', 'PTY', 'DP02', 'Workbench', 'A way to reach a party, with its consent and whether it works.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('loan_account', 'Loan account', 'ACC', 'DP01', 'Core bank (ALS) via COLLINS', 'A loan account in the core bank.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('account_payment', 'Account payment', 'ACC', 'DP01', 'Core bank (ALS) via COLLINS', 'A payment posted to a loan account.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('collateral', 'Collateral', 'COL', 'DP06', 'CCMS', 'Property or vehicle securing one or more accounts.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('account_collateral', 'Account collateral', 'COL', 'DP06', 'Workbench', 'Which collateral secures which account.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('valuation', 'Valuation', 'COL', 'DP06', 'SVAF', 'An appraisal of collateral or an asset.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('asset', 'Asset', 'COL', 'DP06', 'AMIS for property; RPS for vehicles', 'An asset the bank holds after repossession, deed in lieu or auction purchase.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('treatment', 'Treatment', 'TRT', 'DP04', 'Workbench', 'A resolution put to the customer or carried out on the case, with its terms and outcome.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('guarantee_claim', 'Guarantee claim', 'TRT', 'DP04', 'Workbench', 'A claim against a Thai Credit Guarantee Corporation guarantee or an insurer.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('legal_action', 'Legal action', 'LEG', 'DP07', 'LIT for court records; Workbench for instructions', 'A notice, lawsuit, appeal, enforcement or bankruptcy action on a case.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('notice', 'Notice', 'LEG', 'DP07', 'Workbench; WIN for dispatch', 'A demand, recall or statutory notice and its proof of delivery.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('hearing', 'Hearing', 'LEG', 'DP07', 'LIT', 'A court hearing on a legal action.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('partner', 'Partner', 'PRT', 'DP08', 'Workbench', 'An outside firm the bank places work with.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('partner_instruction', 'Partner instruction', 'PRT', 'DP08', 'Workbench', 'Work placed with a partner on a case.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('listing', 'Listing', 'SAL', 'DP06', 'Workbench', 'An asset offered for sale, with its prices and rounds.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('asset_sale', 'Asset sale', 'SAL', 'DP06', 'AMIS', 'The sale of an asset.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('debt_sale_lot', 'Debt sale lot', 'SAL', 'DP09', 'Workbench', 'A lot of accounts offered to debt buyers.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('debt_sale_account', 'Debt sale account', 'SAL', 'DP09', 'Workbench', 'An account in a debt sale lot.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('interaction', 'Interaction', 'INT', 'DP05', 'Workbench', 'One entry in the interaction ledger: a contact, letter, promise, payment or hand-over.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('document', 'Document', 'DOC', 'DP10', 'Workbench document hub', 'A document held against a case.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('document_field', 'Document field', 'DOC', 'DP10', 'Workbench document hub', 'A field read from a document.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('document_custody', 'Document custody', 'DOC', 'DP10', 'Workbench', 'Each movement of an original document.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('decision_log_entry', 'Decision log entry', 'DEC', 'DP12', 'Workbench', 'One record per decision. Append only and hash chained.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('score', 'Score', 'DEC', 'DP11', 'COLLINS', 'A score or estimate COLLINS returns for an account or case.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('proceeds', 'Proceeds', 'FIN', 'DP13', 'Workbench', 'Money received on a case and what it was matched to.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('write_off', 'Write-off', 'FIN', 'DP13', 'GL for posting; Workbench for the decision', 'A write-off of the balance on a case.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('rule_row', 'Rule', 'REF', 'DP14', 'Workbench', 'One versioned routing rule or sentry.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('delegation_limit', 'Delegation limit', 'REF', 'DP14', 'Workbench', 'An approval limit by decision, level, product and amount.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('lov_value', 'List value', 'REF', 'DP14', 'Workbench', 'A value in a list of values.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('role', 'Role', 'REF', 'DP14', 'Workbench', 'A Workbench role, held as data.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('permission', 'Permission', 'REF', 'DP14', 'Workbench', 'What a role may do in one capability area.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('template', 'Template', 'REF', 'DP14', 'Workbench', 'A letter or notice template.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('data_product', 'Data product', 'REF', 'DP14', 'Workbench', 'One of the 14 data products, with its single system of record, owner and refresh cycle.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('data_product_access', 'Data product access', 'REF', 'DP14', 'Workbench', 'Which role may read which data product, by version.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('data_product_load', 'Data product load', 'OPS', 'OPS', 'Workbench', 'The freshness stamp of a data product for one business date.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('data_contract', 'Data contract', 'OPS', 'OPS', 'Workbench', 'A versioned data contract with one source system, confirmed by its system owner.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('sys_objects', 'Sys objects', 'REF', 'DP14', 'Workbench', 'The metadata registry of entities: one row per object in the data dictionary.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('sys_fields', 'Sys fields', 'REF', 'DP14', 'Workbench', 'The metadata registry of fields: the data dictionary held as data.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('sys_field_version', 'Sys field version', 'REF', 'DP14', 'Workbench', 'Each version of a field definition, kept when the definition changes.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('load_run', 'Load run', 'OPS', 'OPS', 'Workbench', 'One run of a data load or job step, with its checks and row counts.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('dq_exception', 'Dq exception', 'OPS', 'OPS', 'Workbench', 'A record a load check or data quality rule held, until it passes again.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('dq_rule', 'Dq rule', 'OPS', 'OPS', 'Workbench', 'A versioned data quality row rule run on a P1 table.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('source_field_map', 'Source field map', 'OPS', 'OPS', 'Workbench', 'How a source field maps to a Workbench field, by interface and mapping version.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('source_code_map', 'Source code map', 'OPS', 'OPS', 'Workbench', 'How a source code maps to a Workbench list value, by interface and map version.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('tracker_inventory', 'Tracker inventory', 'OPS', 'OPS', 'Workbench', 'A team''s Excel or SharePoint tracker, its decision and its load, sign-off and retirement.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('tracker_row', 'Tracker row', 'OPS', 'OPS', 'Workbench', 'One row loaded from a tracker file, with its non-personal fields.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('case_list_row', 'Case list row', 'RPT', 'DP03', 'Workbench', 'One row of the daily case list per case account and business date, published to Power BI.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('collections_history', 'Collections history', 'INT', 'DP05', 'Workbench', 'An EFS contact or promise on an account, loaded from the COLLINS daily batch.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('reconciliation_result', 'Reconciliation result', 'OPS', 'OPS', 'Workbench', 'The daily reconciliation of the case list to ALS by product group.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('lake_copy_watermark', 'Lake copy watermark', 'OPS', 'OPS', 'Workbench', 'How far a copy to the data lake has reached, for example the decision log copy.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('retention_rule', 'Retention rule', 'REF', 'DP14', 'Workbench', 'How long rows of a table or a retention class are kept and what happens at the end, by version.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('dp_treatment', 'Dp treatment', 'TRT', 'DP04', 'Workbench', 'The copy of each treatment for a business date in the DP04 data product.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('dp_guarantee_claim', 'Dp guarantee claim', 'TRT', 'DP04', 'Workbench', 'The copy of each guarantee claim for a business date in the DP04 data product.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('interface_config', 'Interface config', 'OPS', 'OPS', 'Workbench', 'The settings of one file interface, by version.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('interface_run', 'Interface run', 'OPS', 'OPS', 'Workbench', 'One inbound file received by the adapter and the result of its file checks.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('interface_signoff', 'Interface signoff', 'OPS', 'OPS', 'Workbench', 'The data steward''s sign-off that an interface no longer needs manual handling.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('outbound_item', 'Outbound item', 'OPS', 'OPS', 'Workbench', 'One outbound file waiting to be sent, sent or in the exception queue.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('processed_event', 'Processed event', 'OPS', 'OPS', 'Workbench', 'An event or work key a consumer has already processed, so a repeat is ignored and counted.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('idempotency_key', 'Idempotency key', 'OPS', 'OPS', 'Workbench', 'The stored response of an API request sent with an Idempotency-Key header, kept 24 hours.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('outbox_event', 'Outbox event', 'OPS', 'OPS', 'Workbench', 'An application event or outbound work request written in the same transaction as the change.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('outbox_delivery', 'Outbox delivery', 'OPS', 'OPS', 'Workbench', 'The delivery of one outbox event to one consumer, with its retries.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('feature_flag', 'Feature flag', 'OPS', 'OPS', 'Workbench', 'A feature flag with its value per environment, owner and removal date.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('feature_flag_change', 'Feature flag change', 'OPS', 'OPS', 'Workbench', 'One change of a feature flag value in one environment.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('job_catalog', 'Job catalog', 'OPS', 'OPS', 'Workbench', 'A scheduled job with its owner, run book and expected duration.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('party_product', 'Party product', 'PTY', 'DP02', 'Workbench', 'Another product the party holds at the bank, from the customer profile.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('efs_ledger_outcome', 'Efs ledger outcome', 'REF', 'DP14', 'Workbench', 'Which EFS action codes enter the interaction ledger and on which channel.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('case_entry_exclusion', 'Case entry exclusion', 'CAS', 'DP03', 'Workbench', 'An account at 90 days past due that an exclusion rule kept out of recovery on a business date.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('queue_member', 'Queue member', 'WRK', 'DP03', 'Workbench', 'A person who works a queue, with personal capacity and skills, by version.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('queue_measure', 'Queue measure', 'RPT', 'DP03', 'Workbench', 'One snapshot of a queue''s counts, ageing and breaches, published when it reconciles to the case list.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('parameter_catalog', 'Parameter catalog', 'REF', 'DP14', 'Workbench', 'The definition of every parameter and environment setting, with its owner and default.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('parameter_value', 'Parameter value', 'REF', 'DP14', 'Workbench', 'An approved, dated value version of a parameter per environment and product group.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('reference_version', 'Reference version', 'REF', 'DP14', 'Workbench', 'One version of a reference or rule table, with its author, approver, checks and change checklist.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('reference_row', 'Reference row', 'REF', 'DP14', 'Workbench', 'One row of a reference table version held as data.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('rule_test_case', 'Rule test case', 'REF', 'DP14', 'Workbench', 'A test case of the rule table test harness, with its expected and actual result.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('masking_rule', 'Masking rule', 'REF', 'DP14', 'Workbench', 'Which role sees which personal data field unmasked, by version.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('role_conflict', 'Role conflict', 'REF', 'DP14', 'Workbench', 'A pair of roles one person may not hold together, by version.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('partner_user', 'Partner user', 'REF', 'DP14', 'Workbench', 'A partner user''s identity bound to one partner firm and one partner role.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('document_type', 'Document type', 'REF', 'DP14', 'Workbench', 'A document type, the fields extracted from it and its Legal and NPA sign-off, by version.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('document_checklist_item', 'Document checklist item', 'REF', 'DP14', 'Workbench', 'A document type required or expected for a case stage and route, by checklist version.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('case_document_check', 'Case document check', 'DOC', 'DP10', 'Workbench', 'The latest document completeness check of a case against its checklist.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('document_hub_parameter', 'Document hub parameter', 'REF', 'DP14', 'Workbench', 'A document hub parameter value, by version.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('document_intake', 'Document intake', 'DOC', 'DP10', 'Workbench', 'A file received by the document hub, from scan to OCR, classification, extraction, matching and review.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('document_text', 'Document text', 'DOC', 'DP10', 'Workbench', 'The OCR text of one page of an intake item.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('retention_action', 'Retention action', 'DOC', 'DP10', 'Workbench', 'What the monthly retention job did with one document.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('merge_field', 'Merge field', 'REF', 'DP14', 'Workbench', 'A merge code a template may use and the field that supplies its value, by catalog version.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('signature_request', 'Signature request', 'DOC', 'DP10', 'Workbench', 'A request for a party to sign a generated document, and its result.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('approval', 'Approval', 'DEC', 'DP12', 'Workbench', 'An item waiting for approval, routed to the level the delegation of authority requires.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('payment_match_rule', 'Payment match rule', 'REF', 'DP14', 'Workbench', 'A rule for matching a payment to a plan installment, by version.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('measure_definition', 'Measure definition', 'RPT', 'RPT', 'Workbench', 'The agreed definition of a reported measure, by version.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('measure_snapshot', 'Measure snapshot', 'RPT', 'RPT', 'Workbench', 'The value of one measure for a business date, product and dimension value.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('measure_publish', 'Measure publish', 'RPT', 'RPT', 'Workbench', 'Whether the day''s dashboard data set was published or held after reconciling to the case list.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('agent_policy', 'Agent policy', 'AGT', 'AGT', 'Workbench', 'A version of an agent''s policy: model, tools, autonomy, limits and fallback.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('agent_prompt', 'Agent prompt', 'AGT', 'AGT', 'Workbench', 'A version of an agent''s prompt text.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('agent_run', 'Agent run', 'AGT', 'AGT', 'Workbench', 'One call of an agent or model, with its versions, checks, answer, cost and fallback.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('agent_sample', 'Agent sample', 'AGT', 'AGT', 'Workbench', 'One labeled subject in a versioned evaluation sample.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('agent_evaluation_run', 'Agent evaluation run', 'AGT', 'AGT', 'Workbench', 'One evaluation of an agent version against a sample.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('agent_evaluation', 'Agent evaluation', 'AGT', 'AGT', 'Workbench', 'The score of one approach on one label key in an evaluation run.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('agent_feedback', 'Agent feedback', 'AGT', 'AGT', 'Workbench', 'A person''s verdict on an agent answer.');
INSERT INTO sys_objects (object_name, business_name, subject_area, data_product, system_of_record, description) VALUES ('agent_alert', 'Agent alert', 'AGT', 'AGT', 'Workbench', 'A cost cap or drift alert raised for an agent.');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-001', 'recovery_case', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the case');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-002', 'recovery_case', 'case_no', 'TEXT', 'varchar(18)', true, NULL, NULL, 'Workbench', NULL, false, 'Case number RW-YYYY-NNNNNN, issued at creation and never reused');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-003', 'recovery_case', 'product_group', 'LOV', 'varchar(15)', true, 'LOV-PRODUCT', NULL, 'Core bank (ALS) via COLLINS', 'Product_Category_Host', false, 'Mortgage, hire purchase, SSME or unsecured');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-004', 'recovery_case', 'primary_customer_id', 'CROSS_REF', 'uuid', true, NULL, 'party', 'Workbench', NULL, false, 'The borrower the case is opened for');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-005', 'recovery_case', 'status', 'LOV', 'varchar(20)', true, 'LOV-CASE-STATUS', NULL, 'Workbench', NULL, false, 'Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-006', 'recovery_case', 'stage_code', 'LOV', 'varchar(20)', false, 'LOV-STAGE', NULL, 'Workbench', NULL, false, 'The stage the case is on');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-007', 'recovery_case', 'route_state', 'TEXT', 'varchar(60)', false, NULL, NULL, 'Workbench', NULL, false, 'The routing state from the rule set, for example FIRM_INSTRUCTED');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-008', 'recovery_case', 'route_code', 'LOV', 'varchar(4)', false, 'LOV-ROUTE', NULL, 'Workbench', NULL, false, 'The approved route R1 to R8');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-009', 'recovery_case', 'owner_user_id', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'The case owner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-010', 'recovery_case', 'queue_id', 'CROSS_REF', 'uuid', false, NULL, 'queue', 'Workbench', NULL, false, 'The queue the case is in');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-011', 'recovery_case', 'team_code', 'LOV', 'varchar(20)', false, 'LOV-TEAM', NULL, 'Workbench', NULL, false, 'The owning team, used by scope rules');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-012', 'recovery_case', 'region_code', 'LOV', 'varchar(10)', false, 'LOV-REGION', NULL, 'Workbench', NULL, false, 'The owning region, used by scope rules');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-013', 'recovery_case', 'entry_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'The date the case entered recovery');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-014', 'recovery_case', 'dpd_at_entry', 'NUMBER', 'integer', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'DELAY_DAYS', false, 'Days past due on the entry date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-015', 'recovery_case', 'exposure_band', 'LOV', 'varchar(10)', false, 'LOV-EXPOSURE', NULL, 'Workbench', NULL, false, 'Exposure band set from the outstanding balance at entry');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-016', 'recovery_case', 'total_outstanding_at_entry', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'TOTAL_BALANCE', false, 'Total outstanding across linked accounts at entry, in baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-017', 'recovery_case', 'prescription_date', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'The earliest date a legal claim on the case expires');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-018', 'recovery_case', 'stage_clock_start', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the current state started, for the service level');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-019', 'recovery_case', 'deviation_open', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True while any deviation X1 to X7 is open');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-020', 'recovery_case', 'legal_hold', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True while a legal hold stops normal routing');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-021', 'recovery_case', 'rule_version', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'The rule version the current state was entered under');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-022', 'recovery_case', 'closed_date', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'The date the case closed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-023', 'recovery_case', 'closure_reason', 'LOV', 'varchar(20)', false, 'LOV-CLOSURE', NULL, 'Workbench', NULL, false, 'Cured, settled, realized, sold, written off, insurance settled, merged, canceled');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-046', 'recovery_case', 'plan_ref', 'TEXT', 'varchar(30)', false, NULL, NULL, 'ACE', NULL, false, 'Reference of the ACE restructure plan on the case');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-047', 'recovery_case', 'plan_status', 'LOV', 'varchar(10)', false, 'LOV-PLAN-STATUS', NULL, 'ACE', NULL, false, 'ACE plan status: created, approved, booked or broken');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-048', 'recovery_case', 'plan_status_as_of', 'DATE', 'date', false, NULL, NULL, 'ACE', NULL, false, 'Date of the plan status in ACE');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-049', 'recovery_case', 'next_action_text', 'TEXT', 'varchar(1000)', false, NULL, NULL, 'Workbench', NULL, false, 'The next action, copied from action_text of the rule that moved the case');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-050', 'recovery_case', 'next_action_owner_role', 'LOV', 'varchar(20)', false, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Owner role of the next action, from owner_role of the rule');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-051', 'recovery_case', 'next_action_due_date', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Due date from the rule''s timer_spec or the service levels and timers table');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-052', 'recovery_case', 'next_action_rule_id', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Rule ID that set the next action');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-053', 'recovery_case', 'next_action_waiting', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when the next action waits on a customer, party or partner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-054', 'recovery_case', 'last_allocation_date', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Business date of the last allocation run that decided the case');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-055', 'recovery_case', 'status_before_hold', 'LOV', 'varchar(20)', false, 'LOV-CASE-STATUS', NULL, 'Workbench', NULL, false, 'The case status when a legal hold was placed, restored when it is lifted');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-024', 'case_account', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the case account link');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-025', 'case_account', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-026', 'case_account', 'account_id', 'CROSS_REF', 'uuid', true, NULL, 'loan_account', 'Workbench', NULL, false, 'The loan_account this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-027', 'case_account', 'is_primary', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True for the account the case was opened on');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-028', 'case_account', 'linked_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the account joined the case');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-029', 'case_account', 'linked_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Date the account left the case');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-030', 'case_party', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the case party link');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-031', 'case_party', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-032', 'case_party', 'party_id', 'CROSS_REF', 'uuid', true, NULL, 'party', 'Workbench', NULL, false, 'The party this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-033', 'case_party', 'party_role', 'LOV', 'varchar(20)', true, 'LOV-PARTY-ROLE', NULL, 'Workbench', NULL, false, 'Borrower, co-borrower, guarantor, authorized signatory, heir');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-034', 'case_party', 'role_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the role starts');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-035', 'case_party', 'role_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Date the role ends');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-036', 'deviation', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the deviation');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-037', 'deviation', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-038', 'deviation', 'deviation_code', 'LOV', 'varchar(3)', true, 'LOV-DEVIATION', NULL, 'Workbench', NULL, false, 'X1 to X7');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-039', 'deviation', 'raised_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When it was raised');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-040', 'deviation', 'raised_by', 'LOV', 'varchar(20)', true, 'LOV-RAISED-BY', NULL, 'Workbench', NULL, false, 'Screening agent, rule, officer, customer contact');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-041', 'deviation', 'paused_state', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'The routing state the case was in when paused');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-042', 'deviation', 'handler_user_id', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'The named handler');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-043', 'deviation', 'contact_stop', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when customer contact is stopped');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-044', 'deviation', 'cleared_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When it cleared');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-045', 'deviation', 'outcome', 'LOV', 'varchar(20)', false, 'LOV-DEV-OUTCOME', NULL, 'Workbench', NULL, false, 'Returned, re-routed, case ended');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-001', 'queue', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the queue');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-002', 'queue', 'queue_code', 'TEXT', 'varchar(30)', true, NULL, NULL, 'Workbench', NULL, false, 'Queue code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-003', 'queue', 'queue_name', 'TEXT', 'varchar(100)', true, NULL, NULL, 'Workbench', NULL, false, 'Queue name');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-004', 'queue', 'team_code', 'LOV', 'varchar(20)', true, 'LOV-TEAM', NULL, 'Workbench', NULL, false, 'Team the queue belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-005', 'queue', 'role_code', 'LOV', 'varchar(20)', true, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role that works the queue');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-006', 'queue', 'assignment_method', 'LOV', 'varchar(20)', true, 'LOV-ASSIGN', NULL, 'Workbench', NULL, false, 'Round robin, lowest load, named owner, skill');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-007', 'queue', 'capacity_cap', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Most open cases one person may hold in the queue');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-008', 'queue', 'overflow_queue_id', 'CROSS_REF', 'uuid', false, NULL, 'queue', 'Workbench', NULL, false, 'Queue that receives overflow');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-037', 'queue', 'rr_cursor_user_id', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'The member last given a case by round robin in the queue');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-038', 'queue', 'table_version', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'The QUEUE reference version applied to the row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-009', 'assignment', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the assignment');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-010', 'assignment', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-011', 'assignment', 'task_id', 'CROSS_REF', 'uuid', false, NULL, 'task', 'Workbench', NULL, false, 'The task this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-012', 'assignment', 'assignee_user_id', 'USER_REF', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'The person or service identity assigned');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-013', 'assignment', 'assigned_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When assigned');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-014', 'assignment', 'ended_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the assignment ended');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-015', 'assignment', 'reason', 'LOV', 'varchar(20)', true, 'LOV-ASSIGN-REASON', NULL, 'Workbench', NULL, false, 'Allocation, transfer, rebalance, manual, escalation');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-016', 'assignment', 'rule_id', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'The rule that made the assignment');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-039', 'assignment', 'queue_id', 'CROSS_REF', 'uuid', false, NULL, 'queue', 'Workbench', NULL, false, 'The queue the assignment placed the case in');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-040', 'assignment', 'transfer_reason_code', 'LOV', 'varchar(20)', false, 'LOV-TRANSFER-REASON', NULL, 'Workbench', NULL, false, 'Coded reason for a manual transfer or move');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-017', 'task', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the task');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-018', 'task', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-019', 'task', 'task_code', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'The task in the case model, for example VERIFY_PACK');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-020', 'task', 'element_type', 'LOV', 'varchar(20)', true, 'LOV-ELEMENT', NULL, 'Workbench', NULL, false, 'Human, customer, partner or decision task, milestone, event listener');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-021', 'task', 'discretion', 'LOV', 'varchar(15)', true, 'LOV-DISCRETION', NULL, 'Workbench', NULL, false, 'Automatic, discretionary, required');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-022', 'task', 'status', 'LOV', 'varchar(15)', true, 'LOV-TASK-STATUS', NULL, 'Workbench', NULL, false, 'Open, in progress, done, canceled');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-023', 'task', 'owner_role', 'LOV', 'varchar(20)', false, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role that owns the task');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-024', 'task', 'due_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the task is due');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-025', 'task', 'completed_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When it completed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-026', 'task', 'outcome_code', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Workbench', NULL, false, 'The event the task produced');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-027', 'timer', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the timer');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-028', 'timer', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-029', 'timer', 'task_id', 'CROSS_REF', 'uuid', false, NULL, 'task', 'Workbench', NULL, false, 'The task this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-030', 'timer', 'timer_type', 'LOV', 'varchar(20)', true, 'LOV-TIMER', NULL, 'Workbench', NULL, false, 'Service level, notice period, cure period, prescription, hearing deadline, offer validity, holding age, claim deadline');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-031', 'timer', 'started_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When it started');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-032', 'timer', 'expires_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When it expires');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-033', 'timer', 'warn_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the warning is raised');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-034', 'timer', 'paused', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True while paused by a deviation. A prescription timer never pauses');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-035', 'timer', 'status', 'LOV', 'varchar(15)', true, 'LOV-TIMER-STATUS', NULL, 'Workbench', NULL, false, 'Running, paused, expired, stopped');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-036', 'timer', 'escalation_level', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'How many times it has escalated');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-041', 'timer', 'warned_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the warning was sent, so it is sent once');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-042', 'timer', 'treatment_id', 'CROSS_REF', 'uuid', false, NULL, 'treatment', 'Workbench', NULL, false, 'The treatment a plan timer belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-043', 'timer', 'escalated_to_role', 'LOV', 'varchar(20)', false, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role the breach was last escalated to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-044', 'timer', 'escalated_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the timer last escalated');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-001', 'party', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the party');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-002', 'party', 'cif_no', 'TEXT', 'varchar(20)', true, NULL, NULL, 'SCBPDM via COLLINS', 'CIF', true, 'Customer number in the bank');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-003', 'party', 'party_type', 'LOV', 'varchar(15)', true, 'LOV-PARTY-TYPE', NULL, 'SCBPDM via COLLINS', NULL, false, 'Individual or juristic person');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-004', 'party', 'first_name', 'TEXT', 'varchar(100)', true, NULL, NULL, 'SCBPDM via COLLINS', NULL, true, 'First name or company name');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-005', 'party', 'last_name', 'TEXT', 'varchar(100)', false, NULL, NULL, 'SCBPDM via COLLINS', NULL, true, 'Last name');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-006', 'party', 'id_type', 'LOV', 'varchar(20)', true, 'LOV-ID-TYPE', NULL, 'SCBPDM via COLLINS', NULL, false, 'Thai national ID, passport, company registration');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-007', 'party', 'id_no_token', 'TEXT', 'varchar(64)', true, NULL, NULL, 'SCBPDM via COLLINS', NULL, true, 'Tokenized identity number. The clear value is never stored in the Workbench');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-008', 'party', 'date_of_birth', 'DATE', 'date', false, NULL, NULL, 'SCBPDM via COLLINS', NULL, true, 'Date of birth');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-009', 'party', 'segment', 'LOV', 'varchar(20)', false, 'LOV-SEGMENT', NULL, 'SCBPDM via COLLINS', 'Segment', false, 'Retail, SSME, corporate');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-010', 'party', 'vulnerable_flag', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, true, 'Vulnerable customer or hardship confirmed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-011', 'party', 'deceased_flag', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, true, 'Death confirmed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-012', 'party', 'bankruptcy_flag', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, true, 'Bankruptcy or receivership confirmed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-021', 'party', 'fraud_flag', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Aric via COLLINS', NULL, true, 'True while fraud is confirmed or under investigation for the party');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-013', 'contact_point', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the contact point');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-014', 'contact_point', 'party_id', 'CROSS_REF', 'uuid', true, NULL, 'party', 'Workbench', NULL, false, 'The party this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-015', 'contact_point', 'channel', 'LOV', 'varchar(15)', true, 'LOV-CHANNEL', NULL, 'Workbench', NULL, false, 'Mobile, home phone, work phone, LINE, email, postal address');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-016', 'contact_point', 'value_token', 'TEXT', 'varchar(256)', true, NULL, NULL, 'SCBPDM via COLLINS', NULL, true, 'The number, handle or address, stored masked');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-017', 'contact_point', 'source', 'LOV', 'varchar(15)', true, 'LOV-CONTACT-SRC', NULL, 'Workbench', NULL, false, 'Bank record, field visit, agency, bureau trace, customer');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-018', 'contact_point', 'consent_status', 'LOV', 'varchar(12)', true, 'LOV-CONSENT', NULL, 'Workbench', NULL, false, 'Given, withdrawn, unknown');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-019', 'contact_point', 'verified_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When it last reached the right party');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-020', 'contact_point', 'failed_count', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Failed attempts since last success');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-001', 'loan_account', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the account');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-002', 'loan_account', 'account_no', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'ACCOUNT_KEY / iacct / AccNo', false, 'Account number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-003', 'loan_account', 'contract_no', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Core bank (ALS) via COLLINS', 'ContractNo', false, 'Contract number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-004', 'loan_account', 'product_code', 'LOV', 'varchar(10)', true, 'LOV-PRODUCT-CODE', NULL, 'Core bank (ALS) via COLLINS', 'acct_prd_cd', false, 'Core bank product code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-005', 'loan_account', 'product_category_efs', 'TEXT', 'varchar(60)', false, NULL, NULL, 'EFS via COLLINS', 'Product_Category_EFS', false, 'Product category in EFS');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-006', 'loan_account', 'business_unit', 'LOV', 'varchar(10)', false, 'LOV-BU', NULL, 'Core bank (ALS) via COLLINS', 'BU', false, 'Owning business unit');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-007', 'loan_account', 'contract_date', 'DATE', 'date', false, NULL, NULL, 'Core bank (ALS) via COLLINS', 'CONTRACT_DATE', false, 'Contract date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-008', 'loan_account', 'interest_rate', 'NUMBER', 'numeric(7,4)', false, NULL, NULL, 'Core bank (ALS) via COLLINS', 'INTEREST_RATE', false, 'Contract interest rate, percent');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-009', 'loan_account', 'principal_outstanding', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'Principal', false, 'Principal outstanding, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-010', 'loan_account', 'interest_outstanding', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'AINT1 + AINT2', false, 'Accrued interest outstanding, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-011', 'loan_account', 'fees_outstanding', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'AFEE', false, 'Fees outstanding, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-012', 'loan_account', 'total_balance', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'TOTAL_BALANCE', false, 'Total balance, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-013', 'loan_account', 'accounting_balance', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Core bank (ALS) via COLLINS', 'ACCOUNTING_BALANCE', false, 'Accounting balance, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-014', 'loan_account', 'days_past_due', 'NUMBER', 'integer', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'DELAY_DAYS', false, 'Days past due');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-015', 'loan_account', 'bucket', 'LOV', 'varchar(10)', false, 'LOV-BUCKET', NULL, 'Core bank (ALS) via COLLINS', 'Bucket', false, 'Arrears bucket, for example 91-120, 180+');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-016', 'loan_account', 'classification', 'LOV', 'varchar(10)', false, 'LOV-CLASS', NULL, 'Core bank (ALS) via COLLINS', NULL, false, 'Loan classification and stage');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-017', 'loan_account', 'last_payment_date', 'DATE', 'date', false, NULL, NULL, 'Core bank (ALS) via COLLINS', 'LAST_PAYMENT_DATE', false, 'Date of the last payment');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-018', 'loan_account', 'next_installment_date', 'DATE', 'date', false, NULL, NULL, 'Core bank (ALS) via COLLINS', 'NEXT_INSTALLMENT_DATE', false, 'Next installment date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-019', 'loan_account', 'tdr_flag', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'TDR list', false, 'True when the account is under a restructure');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-020', 'loan_account', 'last_tdr_date', 'DATE', 'date', false, NULL, NULL, 'Core bank (ALS) via COLLINS', 'Last_TDR_Date', false, 'Date of the last restructure');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-021', 'loan_account', 'data_as_of', 'DATE', 'date', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'ms_data_dt', false, 'The business date of the load');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-029', 'loan_account', 'dispute_open', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True while the customer disputes the balance or the security on the account');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-030', 'loan_account', 'settlement_booked_date', 'DATE', 'date', false, NULL, NULL, 'Core bank (ALS) via COLLINS', NULL, false, 'Date a settlement was booked in ALS; source field to confirm with the system owner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-031', 'loan_account', 'settlement_booked_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Core bank (ALS) via COLLINS', NULL, false, 'Settlement amount booked in ALS, baht; source field to confirm with the system owner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-022', 'account_payment', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the account payment');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-023', 'account_payment', 'account_id', 'CROSS_REF', 'uuid', true, NULL, 'loan_account', 'Workbench', NULL, false, 'The loan_account this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-024', 'account_payment', 'payment_code', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'Payment_Code', false, 'Payment reference');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-025', 'account_payment', 'payment_date', 'DATE', 'date', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'Payment_Date', false, 'Value date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-026', 'account_payment', 'payment_amount', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'Payment_Amount', false, 'Amount, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-027', 'account_payment', 'payment_channel', 'LOV', 'varchar(15)', false, 'LOV-PAY-CHANNEL', NULL, 'Core bank (ALS) via COLLINS', NULL, false, 'Channel the payment came through');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-ACC-028', 'account_payment', 'data_as_of', 'DATE', 'date', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'ms_data_dt', false, 'The business date of the load');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-001', 'collateral', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the collateral');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-002', 'collateral', 'collateral_no', 'TEXT', 'varchar(20)', true, NULL, NULL, 'CCMS', NULL, false, 'Collateral number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-003', 'collateral', 'collateral_type', 'LOV', 'varchar(15)', true, 'LOV-COLL-TYPE', NULL, 'CCMS', NULL, false, 'Land, house, condominium, vehicle, deposit, other');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-004', 'collateral', 'title_doc_no', 'TEXT', 'varchar(40)', false, NULL, NULL, 'CCMS', 'Title Deed / Ownership Doc', false, 'Title deed or registration number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-005', 'collateral', 'plot_no', 'TEXT', 'varchar(20)', false, NULL, NULL, 'CCMS', 'Plot No.', false, 'Plot number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-006', 'collateral', 'area_text', 'TEXT', 'varchar(20)', false, NULL, NULL, 'CCMS', 'Area', false, 'Land area in rai-ngan-wa');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-007', 'collateral', 'province', 'LOV', 'varchar(40)', false, 'LOV-PROVINCE', NULL, 'CCMS', 'Province', false, 'Province');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-008', 'collateral', 'district', 'TEXT', 'varchar(60)', false, NULL, NULL, 'CCMS', 'District', false, 'District');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-009', 'collateral', 'subdistrict', 'TEXT', 'varchar(60)', false, NULL, NULL, 'CCMS', 'Subdistrict', false, 'Subdistrict');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-010', 'collateral', 'occupancy', 'LOV', 'varchar(15)', false, 'LOV-OCCUPANCY', NULL, 'Workbench', NULL, false, 'Occupied by owner, tenant, vacant, unknown');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-011', 'collateral', 'encumbrance_status', 'LOV', 'varchar(15)', false, 'LOV-ENCUMBRANCE', NULL, 'Workbench', NULL, false, 'Clear, other creditor, seized, under dispute');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-012', 'collateral', 'insured_value', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'CCMS', 'Insvalue', false, 'Insured value, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-013', 'collateral', 'insurance_expiry', 'DATE', 'date', false, NULL, NULL, 'CCMS', NULL, false, 'Insurance expiry date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-014', 'account_collateral', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the account collateral link');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-015', 'account_collateral', 'account_id', 'CROSS_REF', 'uuid', true, NULL, 'loan_account', 'Workbench', NULL, false, 'The loan_account this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-016', 'account_collateral', 'collateral_id', 'CROSS_REF', 'uuid', true, NULL, 'collateral', 'Workbench', NULL, false, 'The collateral this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-017', 'account_collateral', 'lien_rank', 'NUMBER', 'integer', false, NULL, NULL, 'CCMS', NULL, false, 'Rank of the bank''s lien');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-018', 'valuation', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the valuation');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-019', 'valuation', 'collateral_id', 'CROSS_REF', 'uuid', false, NULL, 'collateral', 'Workbench', NULL, false, 'The collateral this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-020', 'valuation', 'asset_id', 'CROSS_REF', 'uuid', false, NULL, 'asset', 'Workbench', NULL, false, 'The asset this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-021', 'valuation', 'appraisal_no', 'TEXT', 'varchar(20)', true, NULL, NULL, 'SVAF', 'Appraisal No.', false, 'Appraisal number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-022', 'valuation', 'appraisal_type', 'LOV', 'varchar(15)', true, 'LOV-APPRAISAL', NULL, 'SVAF', NULL, false, 'Market, official, forced sale, desktop, agent estimate');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-023', 'valuation', 'appraised_value', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'SVAF', 'Appraised Value', false, 'Appraised value, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-024', 'valuation', 'forced_sale_value', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'SVAF', 'Forced Sale Value', false, 'Forced sale value, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-025', 'valuation', 'appraisal_date', 'DATE', 'date', true, NULL, NULL, 'SVAF', 'Appraisal Date', false, 'Appraisal date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-026', 'valuation', 'valuer_partner_id', 'CROSS_REF', 'uuid', false, NULL, 'partner', 'Workbench', NULL, false, 'The valuer');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-027', 'valuation', 'accepted', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True once accepted for the route decision');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-043', 'valuation', 'stale_flag', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when the appraisal is older than appraisal.max.age at the load business date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-044', 'valuation', 'age_days', 'FORMULA', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Age of the appraisal in days at the load business date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-028', 'asset', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the asset');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-029', 'asset', 'case_id', 'CROSS_REF', 'uuid', false, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-030', 'asset', 'collateral_id', 'CROSS_REF', 'uuid', false, NULL, 'collateral', 'Workbench', NULL, false, 'The collateral this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-031', 'asset', 'asset_ref', 'TEXT', 'varchar(20)', true, NULL, NULL, 'AMIS', 'Asset ID', false, 'Asset reference');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-032', 'asset', 'asset_code', 'TEXT', 'varchar(20)', false, NULL, NULL, 'AMIS', 'Asset Code', false, 'Asset code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-033', 'asset', 'asset_type', 'LOV', 'varchar(20)', true, 'LOV-ASSET-TYPE', NULL, 'AMIS', 'Asset Type', false, 'Detached house, townhouse, condominium, land, vehicle');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-034', 'asset', 'transfer_in_type', 'LOV', 'varchar(20)', true, 'LOV-TRANSFER-IN', NULL, 'AMIS', 'Transfer-in Type', false, 'Auction purchase, deed in lieu, repossession');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-035', 'asset', 'from_segment', 'LOV', 'varchar(20)', false, 'LOV-SEGMENT', NULL, 'AMIS', 'From Segment', false, 'Segment the asset came from');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-036', 'asset', 'transfer_in_date', 'DATE', 'date', true, NULL, NULL, 'AMIS', 'Ownership Transfer in Date', false, 'Date ownership passed to the bank');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-037', 'asset', 'book_value', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'AMIS', 'Book  Value', false, 'Book value, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-038', 'asset', 'auction_purchase_price', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'AMIS', 'Auction Purchase Price', false, 'Price paid at auction, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-039', 'asset', 'repossessed_date', 'DATE', 'date', false, NULL, NULL, 'RPS', 'ReposessedCarDate', false, 'Date the vehicle was repossessed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-040', 'asset', 'stock_date', 'DATE', 'date', false, NULL, NULL, 'RPS', 'STOCK_DATE', false, 'Date the vehicle entered stock');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-041', 'asset', 'holding_status', 'LOV', 'varchar(15)', true, 'LOV-HOLDING', NULL, 'Workbench', NULL, false, 'Held, listed, under offer, sold, transferred, rented');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-COL-042', 'asset', 'holding_cost_to_date', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Holding cost to date, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-001', 'treatment', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the treatment');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-002', 'treatment', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-003', 'treatment', 'decision_log_id', 'CROSS_REF', 'uuid', false, NULL, 'decision_log_entry', 'Workbench', NULL, false, 'The decision that approved it');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-004', 'treatment', 'treatment_type', 'LOV', 'varchar(20)', true, 'LOV-TREATMENT', NULL, 'Workbench', NULL, false, 'Restructure, settlement, deed in lieu, buy-back, guarantee claim, repossession, auction, debt sale, write-off, RAMC transfer, rental');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-005', 'treatment', 'proposed_by', 'LOV', 'varchar(10)', true, 'LOV-PROPOSER', NULL, 'Workbench', NULL, false, 'Agent, rule, person');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-006', 'treatment', 'proposed_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When proposed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-007', 'treatment', 'offer_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Amount offered or agreed, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-008', 'treatment', 'haircut_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Amount forgiven, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-009', 'treatment', 'installments', 'NUMBER', 'integer', false, NULL, NULL, 'ACE', NULL, false, 'Number of installments in a plan');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-010', 'treatment', 'valid_until', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Offer validity');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-011', 'treatment', 'approval_level', 'LOV', 'varchar(4)', false, 'LOV-APPROVAL-LEVEL', NULL, 'Workbench', NULL, false, 'Approval level that approved it');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-012', 'treatment', 'booked_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Core bank (ALS) via COLLINS', NULL, false, 'When booked in the core');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-013', 'treatment', 'outcome', 'LOV', 'varchar(12)', false, 'LOV-TRT-OUTCOME', NULL, 'Workbench', NULL, false, 'Kept, broken, completed, canceled, declined');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-014', 'treatment', 'outcome_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the outcome was recorded');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-023', 'treatment', 'nleads_ref', 'TEXT', 'varchar(30)', false, NULL, NULL, 'NLEADS', NULL, false, 'NLEADS reference of the credit approval');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-024', 'treatment', 'credit_result', 'LOV', 'varchar(10)', false, 'LOV-CREDIT-RESULT', NULL, 'NLEADS', NULL, false, 'Approved or refused, from NLEADS');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-025', 'treatment', 'credit_result_reason', 'TEXT', 'varchar(1000)', false, NULL, NULL, 'NLEADS', NULL, false, 'Reason given by NLEADS; required when refused');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-026', 'treatment', 'credit_result_at', 'DATE', 'timestamptz', false, NULL, NULL, 'NLEADS', NULL, false, 'When the result was given in NLEADS');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-027', 'treatment', 'interest_rate', 'NUMBER', 'numeric(7,4)', false, NULL, NULL, 'Workbench', NULL, false, 'Approved interest rate of the plan, percent');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-028', 'treatment', 'booking_difference', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Each term that differs between approval and booking: term, approved, booked, business date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-029', 'treatment', 'first_due_date', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Date the first installment is due');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-030', 'treatment', 'signature_status', 'LOV', 'varchar(12)', false, 'LOV-TRT-SIGNATURE', NULL, 'Workbench', NULL, false, 'Pending, signed or not signed, read by the routing rules');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-031', 'treatment', 'installment_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Amount due per plan installment, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-032', 'treatment', 'installments_paid', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Installments matched so far');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-033', 'treatment', 'installment_shortfall', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Shortfall left on the plan by a partial payment, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-015', 'guarantee_claim', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the guarantee claim');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-016', 'guarantee_claim', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-017', 'guarantee_claim', 'claim_type', 'LOV', 'varchar(25)', true, 'LOV-CLAIM-TYPE', NULL, 'Workbench', NULL, false, 'TCG, credit life insurance, mortgage insurance, collateral insurance');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-018', 'guarantee_claim', 'claim_deadline', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Last date the claim can be filed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-019', 'guarantee_claim', 'claimed_amount', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'Workbench', NULL, false, 'Amount claimed, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-020', 'guarantee_claim', 'filed_at', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Date filed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-021', 'guarantee_claim', 'paid_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Amount paid, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-022', 'guarantee_claim', 'status', 'LOV', 'varchar(12)', true, 'LOV-CLAIM-STATUS', NULL, 'Workbench', NULL, false, 'Preparing, filed, defect, paid, rejected');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-001', 'legal_action', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the legal action');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-002', 'legal_action', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-003', 'legal_action', 'law_firm_id', 'CROSS_REF', 'uuid', false, NULL, 'partner', 'Workbench', NULL, false, 'The law firm instructed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-004', 'legal_action', 'action_type', 'LOV', 'varchar(20)', true, 'LOV-LEGAL-TYPE', NULL, 'Workbench', NULL, false, 'Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-005', 'legal_action', 'lawsuit_no', 'TEXT', 'varchar(30)', false, NULL, NULL, 'LIT', 'LAWSUIT_NO / LAWSUIT_RUN', false, 'Lawsuit reference in LIT');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-006', 'legal_action', 'black_case_no', 'TEXT', 'varchar(30)', false, NULL, NULL, 'LIT', 'เลขที่คดีดำ', false, 'Court black case number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-007', 'legal_action', 'red_case_no', 'TEXT', 'varchar(30)', false, NULL, NULL, 'LIT', NULL, false, 'Court red case number after judgment');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-008', 'legal_action', 'court_name', 'TEXT', 'varchar(120)', false, NULL, NULL, 'LIT', 'NCOURT', false, 'Court');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-009', 'legal_action', 'claim_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'LIT', 'AAMT_SUIT', false, 'Amount sued for, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-010', 'legal_action', 'filed_date', 'DATE', 'date', false, NULL, NULL, 'LIT', NULL, false, 'Date filed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-011', 'legal_action', 'judgment_date', 'DATE', 'date', false, NULL, NULL, 'LIT', 'Judgment date', false, 'Date of judgment');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-012', 'legal_action', 'judgment_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'LIT', NULL, false, 'Amount awarded, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-013', 'legal_action', 'lit_status', 'TEXT', 'varchar(200)', false, NULL, NULL, 'LIT via COLLINS', 'STATE_RES_NAME', false, 'Latest status text in LIT');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-014', 'legal_action', 'status', 'LOV', 'varchar(15)', true, 'LOV-LEGAL-STATUS', NULL, 'Workbench', NULL, false, 'Open, filed, judgment, enforcing, closed, withdrawn');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-015', 'notice', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the notice');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-016', 'notice', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-017', 'notice', 'document_id', 'CROSS_REF', 'uuid', false, NULL, 'document', 'Workbench', NULL, false, 'The generated notice');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-018', 'notice', 'notice_type', 'LOV', 'varchar(25)', true, 'LOV-NOTICE', NULL, 'Workbench', NULL, false, 'Demand, recall, statutory sale notice, guarantor notice');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-019', 'notice', 'sent_date', 'DATE', 'date', false, NULL, NULL, 'WIN', 'DDMMYYYY', false, 'Date sent');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-020', 'notice', 'barcode', 'TEXT', 'varchar(40)', false, NULL, NULL, 'WIN', 'Barcode', false, 'Registered mail barcode');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-021', 'notice', 'callback_date', 'DATE', 'date', false, NULL, NULL, 'WIN', 'DDMMYYYY_callBack', false, 'Date the proof of delivery came back');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-022', 'notice', 'delivery_status', 'LOV', 'varchar(15)', false, 'LOV-DELIVERY', NULL, 'WIN', NULL, false, 'Delivered, refused, undeliverable, pending');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-023', 'notice', 'sent_type', 'LOV', 'varchar(10)', false, 'LOV-SENT-TYPE', NULL, 'WIN', 'Sent Type', false, 'Before NPL or NPL');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-030', 'notice', 'party_id', 'CROSS_REF', 'uuid', false, NULL, 'party', 'Workbench', NULL, false, 'Party the notice is addressed to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-031', 'notice', 'template_id', 'CROSS_REF', 'uuid', false, NULL, 'template', 'Workbench', NULL, false, 'Template version the notice was generated from');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-032', 'notice', 'hold_reason', 'TEXT', 'varchar(30)', false, NULL, NULL, 'Workbench', NULL, false, 'Why the notice is held: missing merge field, TEMPLATE_WITHDRAWN, CONTACT_STOP_Xn, LEGAL_HOLD');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-033', 'notice', 'dispatch_file_id', 'CROSS_REF', 'uuid', false, NULL, 'outbound_item', 'Workbench', NULL, false, 'WIN file the notice was last written to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-034', 'notice', 'dispatch_attempts', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Number of WIN files the notice has been sent in without acknowledgment');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-024', 'hearing', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the hearing');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-025', 'hearing', 'legal_action_id', 'CROSS_REF', 'uuid', true, NULL, 'legal_action', 'Workbench', NULL, false, 'The legal_action this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-026', 'hearing', 'hearing_date', 'DATE', 'timestamptz', true, NULL, NULL, 'LIT', NULL, false, 'Hearing date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-027', 'hearing', 'hearing_type', 'LOV', 'varchar(20)', false, 'LOV-HEARING', NULL, 'LIT', NULL, false, 'First hearing, witness, judgment reading, mediation');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-028', 'hearing', 'outcome', 'LOV', 'varchar(20)', false, 'LOV-HEARING-OUTCOME', NULL, 'Workbench', NULL, false, 'Held, adjourned, settled, judgment');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-LEG-029', 'hearing', 'next_date', 'DATE', 'timestamptz', false, NULL, NULL, 'LIT', NULL, false, 'Next date set');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-001', 'partner', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the partner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-002', 'partner', 'partner_code', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', 'OACode', false, 'Partner code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-003', 'partner', 'partner_name', 'TEXT', 'varchar(160)', true, NULL, NULL, 'Workbench', 'REPOSS_NAME / Investor', false, 'Registered name');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-004', 'partner', 'partner_type', 'LOV', 'varchar(15)', true, 'LOV-PARTNER-TYPE', NULL, 'Workbench', NULL, false, 'Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-005', 'partner', 'panel_status', 'LOV', 'varchar(12)', true, 'LOV-PANEL', NULL, 'Workbench', NULL, false, 'Active, on notice, suspended, exited');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-006', 'partner', 'contract_end', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Contract end date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-007', 'partner', 'score', 'NUMBER', 'numeric(5,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Latest scorecard result');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-008', 'partner_instruction', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the partner instruction');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-009', 'partner_instruction', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-010', 'partner_instruction', 'partner_id', 'CROSS_REF', 'uuid', true, NULL, 'partner', 'Workbench', NULL, false, 'The partner this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-011', 'partner_instruction', 'instruction_type', 'LOV', 'varchar(20)', true, 'LOV-INSTRUCTION', NULL, 'Workbench', NULL, false, 'Collect, file suit, enforce, appraise, repossess, list, sell');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-012', 'partner_instruction', 'instructed_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When instructed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-013', 'partner_instruction', 'due_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the result is due');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-014', 'partner_instruction', 'status', 'LOV', 'varchar(12)', true, 'LOV-INSTR-STATUS', NULL, 'Workbench', NULL, false, 'Sent, accepted, declined, in progress, done, recalled');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-015', 'partner_instruction', 'result_code', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Workbench', NULL, false, 'Result reported by the partner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PRT-016', 'partner_instruction', 'fee_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Fee payable, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-001', 'listing', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the listing');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-002', 'listing', 'asset_id', 'CROSS_REF', 'uuid', true, NULL, 'asset', 'Workbench', NULL, false, 'The asset this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-003', 'listing', 'sale_channel', 'LOV', 'varchar(15)', true, 'LOV-SALE-CHANNEL', NULL, 'Workbench', 'Sale By', false, 'Dutch auction, broker, direct, LED auction, RAMC');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-004', 'listing', 'start_price', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'Workbench', NULL, false, 'Start price, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-005', 'listing', 'floor_price', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'Workbench', NULL, false, 'Floor price approved, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-006', 'listing', 'round_no', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Current price round');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-007', 'listing', 'listed_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When listed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-008', 'listing', 'status', 'LOV', 'varchar(12)', true, 'LOV-LISTING', NULL, 'Workbench', NULL, false, 'Draft, live, under offer, sold, withdrawn');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-009', 'asset_sale', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the asset sale');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-010', 'asset_sale', 'asset_id', 'CROSS_REF', 'uuid', true, NULL, 'asset', 'Workbench', NULL, false, 'The asset this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-011', 'asset_sale', 'listing_id', 'CROSS_REF', 'uuid', false, NULL, 'listing', 'Workbench', NULL, false, 'The listing this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-012', 'asset_sale', 'contract_date', 'DATE', 'date', true, NULL, NULL, 'AMIS', 'Contract Date', false, 'Sale contract date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-013', 'asset_sale', 'sale_date', 'DATE', 'date', true, NULL, NULL, 'AMIS', 'Sale Date', false, 'Sale date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-014', 'asset_sale', 'sale_price', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'AMIS', 'Sale Price', false, 'Sale price, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-015', 'asset_sale', 'transfer_fee', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'AMIS', 'Sale Transfer Fee', false, 'Transfer fee, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-016', 'asset_sale', 'specific_business_tax', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'AMIS', 'Specific Business Tax', false, 'Specific business tax, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-017', 'asset_sale', 'corporate_income_tax', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'AMIS', 'Corporate Income Tax', false, 'Corporate income tax, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-018', 'asset_sale', 'gain_loss', 'FORMULA', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Sale price less book value and costs');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-019', 'asset_sale', 'incentive_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'AMIS', 'Incentive Amount', false, 'Incentive paid on the sale, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-020', 'debt_sale_lot', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the debt sale lot');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-021', 'debt_sale_lot', 'lot_no', 'TEXT', 'varchar(15)', true, NULL, NULL, 'Workbench', 'Lot', false, 'Lot number, for example 1/2024');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-022', 'debt_sale_lot', 'cut_off_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Balance cut-off date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-023', 'debt_sale_lot', 'segment', 'LOV', 'varchar(20)', true, 'LOV-SEGMENT', NULL, 'Workbench', 'Segment', false, 'Segment of the lot');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-024', 'debt_sale_lot', 'reserve_price', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Reserve price, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-025', 'debt_sale_lot', 'buyer_partner_id', 'CROSS_REF', 'uuid', false, NULL, 'partner', 'Workbench', 'Investor', false, 'Winning buyer');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-026', 'debt_sale_lot', 'buyer_class', 'LOV', 'varchar(10)', false, 'LOV-BUYER-CLASS', NULL, 'Workbench', 'AMC/NON AMC', false, 'AMC or non-AMC');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-027', 'debt_sale_lot', 'signing_date', 'DATE', 'date', false, NULL, NULL, 'Workbench', 'SigningYear', false, 'Date the sale was signed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-028', 'debt_sale_lot', 'approval_authority', 'TEXT', 'varchar(60)', false, NULL, NULL, 'Workbench', 'Debt Sale Approval Authority', false, 'Authority that approved the sale');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-029', 'debt_sale_lot', 'payment_terms', 'TEXT', 'varchar(400)', false, NULL, NULL, 'Workbench', 'Payment Terms and Conditions', false, 'Deposit and payment terms');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-030', 'debt_sale_lot', 'status', 'LOV', 'varchar(12)', true, 'LOV-LOT-STATUS', NULL, 'Workbench', NULL, false, 'Building, offered, awarded, transferred, closed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-031', 'debt_sale_account', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the debt sale account');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-032', 'debt_sale_account', 'lot_id', 'CROSS_REF', 'uuid', true, NULL, 'debt_sale_lot', 'Workbench', NULL, false, 'The debt_sale_lot this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-033', 'debt_sale_account', 'account_id', 'CROSS_REF', 'uuid', true, NULL, 'loan_account', 'Workbench', NULL, false, 'The loan_account this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-034', 'debt_sale_account', 'borrower_code', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', 'BorrCode', false, 'Borrower code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-035', 'debt_sale_account', 'outstanding', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'OS By Acct', false, 'Outstanding at cut-off, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-036', 'debt_sale_account', 'selling_price', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', 'SellingPriceByAcct', false, 'Price allocated to the account, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-SAL-037', 'debt_sale_account', 'put_back_status', 'LOV', 'varchar(12)', false, 'LOV-PUTBACK', NULL, 'Workbench', NULL, false, 'None, claimed, accepted, rejected');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-001', 'interaction', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the interaction');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-002', 'interaction', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-003', 'interaction', 'party_id', 'CROSS_REF', 'uuid', false, NULL, 'party', 'Workbench', NULL, false, 'The party this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-004', 'interaction', 'occurred_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When it happened');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-005', 'interaction', 'channel', 'LOV', 'varchar(15)', false, 'LOV-CHANNEL', NULL, 'Workbench', NULL, false, 'Call, visit, SMS, LINE, email, letter, portal, branch; empty for Workbench events such as CASE_CREATED');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-006', 'interaction', 'direction', 'LOV', 'varchar(8)', false, 'LOV-DIRECTION', NULL, 'Workbench', NULL, false, 'Inbound or outbound; empty for Workbench events such as CASE_CREATED');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-007', 'interaction', 'action_code', 'LOV', 'varchar(10)', false, 'LOV-ACTION-CODE', NULL, 'EFS via COLLINS', 'Actioncode ID', false, 'Action code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-008', 'interaction', 'contact_result', 'LOV', 'varchar(20)', false, 'LOV-CONTACT-RESULT', NULL, 'EFS via COLLINS', 'Call Result', false, 'Right party, third party, no answer, wrong number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-009', 'interaction', 'promise_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Amount promised, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-010', 'interaction', 'promise_date', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Date promised');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-011', 'interaction', 'summary', 'TEXT', 'varchar(2000)', false, NULL, NULL, 'Workbench', NULL, true, 'Summary of what was said');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-012', 'interaction', 'conduct_check', 'LOV', 'varchar(15)', false, 'LOV-CONDUCT', NULL, 'Workbench', NULL, false, 'Passed, blocked, not applicable');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-013', 'interaction', 'source_system', 'LOV', 'varchar(10)', true, 'LOV-SOURCE', NULL, 'Workbench', NULL, false, 'EFS for collections history, or the Workbench');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-014', 'interaction', 'event_code', 'LOV', 'varchar(40)', false, 'LOV-LEDGER-EVENT', NULL, 'Workbench', NULL, false, 'Ledger event');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-015', 'interaction', 'actor_type', 'LOV', 'varchar(10)', false, 'LOV-ACTOR-TYPE', NULL, 'Workbench', NULL, false, 'User, service or partner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-016', 'interaction', 'actor_ref', 'TEXT', 'varchar(64)', false, NULL, NULL, 'Workbench', NULL, false, 'User ID or service identity code that acted');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-017', 'interaction', 'source_ref', 'TEXT', 'varchar(60)', false, NULL, NULL, 'Workbench', NULL, false, 'Producing module and event, or the interface, for example EV-02 CaseAllocated or INT-07');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-018', 'interaction', 'idempotency_key', 'TEXT', 'varchar(120)', false, NULL, NULL, 'Workbench', NULL, false, 'Unique key of the event or request; repeats are rejected; unique on its own');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-019', 'interaction', 'case_seq', 'NUMBER', 'bigint', false, NULL, NULL, 'Workbench', NULL, false, 'Gap-free sequence of the entry within its case; unique with case_id');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-020', 'interaction', 'decision_log_id', 'CROSS_REF', 'uuid', false, NULL, 'decision_log_entry', 'Workbench', NULL, false, 'Decision log entry the entry records, for DECISION_TAKEN');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-021', 'interaction', 'corrects_entry_id', 'CROSS_REF', 'uuid', false, NULL, 'interaction', 'Workbench', NULL, false, 'Entry this entry corrects');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-022', 'interaction', 'contact_point_id', 'CROSS_REF', 'uuid', false, NULL, 'contact_point', 'Workbench', NULL, false, 'The contact point reached; the number or address stays masked in contact_point');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-023', 'interaction', 'from_holder_ref', 'TEXT', 'varchar(60)', false, NULL, NULL, 'Workbench', NULL, false, 'Who held the case before a hand-over: USER:<user id> or PARTNER:<partner code>');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-024', 'interaction', 'to_holder_ref', 'TEXT', 'varchar(60)', false, NULL, NULL, 'Workbench', NULL, false, 'Who holds the case after a hand-over: USER:<user id> or PARTNER:<partner code>');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-025', 'interaction', 'treatment_id', 'CROSS_REF', 'uuid', false, NULL, 'treatment', 'Workbench', NULL, false, 'The treatment offered, for an OFFER entry');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-026', 'interaction', 'proceeds_id', 'CROSS_REF', 'uuid', false, NULL, 'proceeds', 'Workbench', NULL, false, 'The proceeds matched, for a PAYMENT entry');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-027', 'interaction', 'retention_class', 'LOV', 'varchar(10)', false, 'LOV-RETENTION', NULL, 'Workbench', NULL, false, 'Retention class of the entry, set by entry type');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-028', 'interaction', 'delivery_status', 'LOV', 'varchar(15)', false, 'LOV-SEND-STATUS', NULL, 'Workbench', NULL, false, 'Delivery state of an outbound SMS, LINE message or letter');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-029', 'interaction', 'external_ref', 'TEXT', 'varchar(60)', false, NULL, NULL, 'Workbench', NULL, false, 'Reference returned by NSS, LINE OA or WIN');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-001', 'document', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the document');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-002', 'document', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-003', 'document', 'party_id', 'CROSS_REF', 'uuid', false, NULL, 'party', 'Workbench', NULL, false, 'The party this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-004', 'document', 'document_type', 'LOV', 'varchar(30)', true, 'LOV-DOC-TYPE', NULL, 'Workbench', NULL, false, 'Type from the document checklist');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-005', 'document', 'source', 'LOV', 'varchar(12)', true, 'LOV-DOC-SOURCE', NULL, 'Workbench', NULL, false, 'Scan, upload, generated, partner, email');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-006', 'document', 'storage_ref', 'ATTACHMENT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'Reference to the stored file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-007', 'document', 'classification_confidence', 'NUMBER', 'numeric(5,4)', false, NULL, NULL, 'Workbench', NULL, false, 'OCR classification confidence');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-008', 'document', 'review_status', 'LOV', 'varchar(12)', true, 'LOV-REVIEW', NULL, 'Workbench', NULL, false, 'Not needed, pending, confirmed, corrected');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-009', 'document', 'retention_class', 'LOV', 'varchar(10)', true, 'LOV-RETENTION', NULL, 'Workbench', NULL, false, 'Retention class');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-010', 'document', 'write_once', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True for legal documents held write-once');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-011', 'document', 'doc_version', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Document version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-025', 'document', 'previous_version_id', 'CROSS_REF', 'uuid', false, NULL, 'document', 'Workbench', NULL, false, 'The document row this version supersedes; empty for version 1');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-026', 'document', 'content_sha256', 'TEXT', 'char(64)', true, NULL, NULL, 'Workbench', NULL, false, 'SHA-256 of the stored file, for the duplicate check and the integrity check');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-027', 'document', 'captured_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'Device time when the field app captured the file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-028', 'document', 'capture_latitude', 'NUMBER', 'numeric(9,6)', false, NULL, NULL, 'Workbench', NULL, true, 'GPS latitude at capture');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-029', 'document', 'capture_longitude', 'NUMBER', 'numeric(9,6)', false, NULL, NULL, 'Workbench', NULL, true, 'GPS longitude at capture');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-030', 'document', 'client_file_id', 'TEXT', 'varchar(64)', false, NULL, NULL, 'Workbench', NULL, false, 'Field app file ID, unique per case, for repeat syncs');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-031', 'document', 'capture_kind', 'LOV', 'varchar(12)', false, 'LOV-CAPTURE-KIND', NULL, 'Workbench', NULL, false, 'Photo, bill or checklist');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-032', 'document', 'template_id', 'CROSS_REF', 'uuid', false, NULL, 'template', 'Workbench', NULL, false, 'Template version a generated document was made from');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-033', 'document', 'treatment_id', 'CROSS_REF', 'uuid', false, NULL, 'treatment', 'Workbench', NULL, false, 'Treatment a generated document belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-012', 'document_field', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the document field');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-013', 'document_field', 'document_id', 'CROSS_REF', 'uuid', true, NULL, 'document', 'Workbench', NULL, false, 'The document this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-014', 'document_field', 'field_name', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Field name from the document type');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-015', 'document_field', 'field_value', 'TEXT', 'varchar(1000)', false, NULL, NULL, 'Workbench', NULL, true, 'Value read, masked where personal');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-016', 'document_field', 'confidence', 'NUMBER', 'numeric(5,4)', false, NULL, NULL, 'Workbench', NULL, false, 'Extraction confidence');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-017', 'document_field', 'confirmed_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Who confirmed a low confidence value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-034', 'document_field', 'extracted_value', 'TEXT', 'varchar(1000)', false, NULL, NULL, 'Workbench', NULL, true, 'The value as first read by the extractor, kept when a person corrects field_value; masked by role');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-035', 'document_field', 'extractor_version', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Workbench', NULL, false, 'Extraction approach and model version that produced the value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-018', 'document_custody', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the custody movement');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-019', 'document_custody', 'document_id', 'CROSS_REF', 'uuid', true, NULL, 'document', 'Workbench', NULL, false, 'The document this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-020', 'document_custody', 'moved_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When it moved');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-021', 'document_custody', 'from_location', 'LOV', 'varchar(20)', true, 'LOV-CUSTODY', NULL, 'Workbench', NULL, false, 'Vault, branch, post, lawyer, court, land office');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-022', 'document_custody', 'to_location', 'LOV', 'varchar(20)', true, 'LOV-CUSTODY', NULL, 'Workbench', NULL, false, 'Where it went');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-023', 'document_custody', 'held_by', 'TEXT', 'varchar(120)', true, NULL, NULL, 'Workbench', NULL, false, 'Person or firm holding it');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-024', 'document_custody', 'due_back', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'When it is due back');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-001', 'decision_log_entry', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the decision log entry');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-002', 'decision_log_entry', 'case_id', 'CROSS_REF', 'uuid', false, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-003', 'decision_log_entry', 'decision_code', 'LOV', 'varchar(8)', true, 'LOV-DECISION', NULL, 'Workbench', NULL, false, 'D5.1 to D9.3, X1 to X7, or an access event');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-004', 'decision_log_entry', 'rule_id', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Rule that fired');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-005', 'decision_log_entry', 'rule_version', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Rule version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-006', 'decision_log_entry', 'model_version', 'TEXT', 'varchar(40)', false, NULL, NULL, 'COLLINS', NULL, false, 'Model version used');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-007', 'decision_log_entry', 'agent_version', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Workbench', NULL, false, 'Agent and prompt version used');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-008', 'decision_log_entry', 'inputs_ref', 'TEXT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'Reference to the inputs snapshot, with the freshness of each input');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-009', 'decision_log_entry', 'recommendation', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Option, reasons, confidence and alternatives');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-010', 'decision_log_entry', 'approver_user_id', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Who approved');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-011', 'decision_log_entry', 'approval_level', 'LOV', 'varchar(4)', false, 'LOV-APPROVAL-LEVEL', NULL, 'Workbench', NULL, false, 'Approval level applied');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-012', 'decision_log_entry', 'final_call', 'TEXT', 'varchar(40)', true, NULL, NULL, 'Workbench', NULL, false, 'The option decided');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-013', 'decision_log_entry', 'override_reason', 'TEXT', 'varchar(1000)', false, NULL, NULL, 'Workbench', NULL, false, 'Reason when the person did not follow the recommendation');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-014', 'decision_log_entry', 'actions', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Target system, result and timestamps of each action');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-015', 'decision_log_entry', 'outcome', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Cash, cure, loss and time, written when known');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-016', 'decision_log_entry', 'decided_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When decided');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-017', 'decision_log_entry', 'prev_hash', 'TEXT', 'char(64)', true, NULL, NULL, 'Workbench', NULL, false, 'Hash of the previous entry');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-018', 'decision_log_entry', 'entry_hash', 'TEXT', 'char(64)', true, NULL, NULL, 'Workbench', NULL, false, 'Hash of this entry');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-028', 'decision_log_entry', 'chain_seq', 'NUMBER', 'bigint', true, NULL, NULL, 'Workbench', NULL, false, 'Position of the entry in the hash chain; prev_hash is the entry_hash of chain_seq minus 1; unique on its own');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-029', 'decision_log_entry', 'corrects_entry_id', 'CROSS_REF', 'uuid', false, NULL, 'decision_log_entry', 'Workbench', NULL, false, 'The entry this entry corrects');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-030', 'decision_log_entry', 'actor_user_id', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'The person or service identity whose action, preparation or access the entry records');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-031', 'decision_log_entry', 'idempotency_key', 'TEXT', 'varchar(80)', false, NULL, NULL, 'Workbench', NULL, false, 'Event ID of the calling module; a repeat returns the first entry; unique on its own');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-019', 'score', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the score');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-020', 'score', 'account_id', 'CROSS_REF', 'uuid', false, NULL, 'loan_account', 'Workbench', NULL, false, 'The loan_account this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-021', 'score', 'case_id', 'CROSS_REF', 'uuid', false, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-022', 'score', 'model_code', 'TEXT', 'varchar(30)', true, NULL, NULL, 'COLLINS', NULL, false, 'Model, for example CRR_RET_380 asset pricing');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-023', 'score', 'model_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'COLLINS', NULL, false, 'Model version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-024', 'score', 'score_value', 'NUMBER', 'numeric(12,4)', false, NULL, NULL, 'COLLINS', NULL, false, 'Score');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-025', 'score', 'estimate_value', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'COLLINS', NULL, false, 'Estimated amount, baht, for example return by route or sale price');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-026', 'score', 'route_code', 'LOV', 'varchar(4)', false, 'LOV-ROUTE', NULL, 'COLLINS', NULL, false, 'Route the estimate is for');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-027', 'score', 'scored_at', 'DATE', 'date', true, NULL, NULL, 'COLLINS', NULL, false, 'Score date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-001', 'proceeds', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the proceeds');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-002', 'proceeds', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-003', 'proceeds', 'treatment_id', 'CROSS_REF', 'uuid', false, NULL, 'treatment', 'Workbench', NULL, false, 'The treatment this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-004', 'proceeds', 'account_payment_id', 'CROSS_REF', 'uuid', false, NULL, 'account_payment', 'Workbench', NULL, false, 'The account_payment this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-005', 'proceeds', 'source', 'LOV', 'varchar(12)', true, 'LOV-PROCEEDS-SRC', NULL, 'Workbench', NULL, false, 'Customer, LED, auction, buyer, agency, insurer, guarantor');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-006', 'proceeds', 'amount', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'Payment_Amount', false, 'Amount, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-007', 'proceeds', 'received_date', 'DATE', 'date', true, NULL, NULL, 'Core bank (ALS) via COLLINS', 'Payment_Date', false, 'Date received');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-008', 'proceeds', 'matched_to', 'LOV', 'varchar(15)', true, 'LOV-MATCH', NULL, 'Workbench', NULL, false, 'Installment, settlement, fee, sale proceeds, unmatched');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-009', 'proceeds', 'posting_ref', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Core bank (ALS) via COLLINS', NULL, false, 'Posting reference in the core or GL');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-010', 'write_off', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the write-off');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-011', 'write_off', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The recovery_case this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-012', 'write_off', 'decision_log_id', 'CROSS_REF', 'uuid', false, NULL, 'decision_log_entry', 'Workbench', NULL, false, 'The decision_log_entry this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-013', 'write_off', 'amount', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'GL', 'AMT', false, 'Amount written off, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-014', 'write_off', 'tax_criteria_met', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when the tax criteria are met');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-015', 'write_off', 'committee_date', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Committee approval date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-016', 'write_off', 'posted_date', 'DATE', 'date', false, NULL, NULL, 'GL', 'DATE', false, 'Posting date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-017', 'write_off', 'responsibility_center', 'TEXT', 'varchar(10)', false, NULL, NULL, 'GL', 'RC', false, 'Responsibility center');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-018', 'write_off', 'cost_center', 'TEXT', 'varchar(10)', false, NULL, NULL, 'GL', 'OC', false, 'Operating cost center');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-019', 'write_off', 'gl_product', 'TEXT', 'varchar(10)', false, NULL, NULL, 'GL', 'PRODUCT', false, 'GL product code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-FIN-020', 'write_off', 'recovered_after', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'Workbench', NULL, false, 'Recovered after charge-off to date, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-001', 'rule_row', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the rule row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-002', 'rule_row', 'rule_id', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Rule ID, for example R-LIT-12');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-003', 'rule_row', 'rule_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-004', 'rule_row', 'route_set', 'LOV', 'varchar(15)', true, 'LOV-ROUTE-SET', NULL, 'Workbench', NULL, false, 'Route set');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-005', 'rule_row', 'from_state', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'From state');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-006', 'rule_row', 'event_code', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Event');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-007', 'rule_row', 'condition_expr', 'TEXT', 'varchar(1000)', false, NULL, NULL, 'Workbench', NULL, false, 'Condition');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-008', 'rule_row', 'action_text', 'TEXT', 'varchar(1000)', true, NULL, NULL, 'Workbench', NULL, false, 'Action');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-009', 'rule_row', 'to_state', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'To state');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-010', 'rule_row', 'owner_role', 'LOV', 'varchar(20)', true, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Owner of the next state');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-011', 'rule_row', 'timer_spec', 'TEXT', 'varchar(60)', false, NULL, NULL, 'Workbench', NULL, false, 'Timer');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-012', 'rule_row', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Valid from');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-013', 'rule_row', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Valid to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-014', 'rule_row', 'approved_by', 'USER_REF', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Who approved the version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-015', 'rule_row', 'test_case_id', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Test case that proves the rule');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-052', 'rule_row', 'rule_table', 'LOV', 'varchar(15)', false, 'LOV-RULE-TABLE', NULL, 'Workbench', NULL, false, 'The Epic 1 rule table a row belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-053', 'rule_row', 'row_order', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Order in which rows of one rule table are evaluated; first match wins');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-054', 'rule_row', 'target_queue_code', 'TEXT', 'varchar(30)', false, NULL, NULL, 'Workbench', NULL, false, 'The queue an allocation or transfer row places the case in');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-016', 'delegation_limit', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the delegation limit');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-017', 'delegation_limit', 'decision_code', 'LOV', 'varchar(8)', true, 'LOV-DECISION', NULL, 'Workbench', NULL, false, 'Decision the limit applies to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-018', 'delegation_limit', 'approval_level', 'LOV', 'varchar(4)', true, 'LOV-APPROVAL-LEVEL', NULL, 'Workbench', NULL, false, 'Level 1 to 6 under Regulation กกค.540031');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-019', 'delegation_limit', 'product_group', 'LOV', 'varchar(15)', true, 'LOV-PRODUCT', NULL, 'Workbench', NULL, false, 'Product group');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-020', 'delegation_limit', 'principal_limit', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Principal limit, baht; empty means no limit');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-021', 'delegation_limit', 'loss_pct_limit', 'NUMBER', 'numeric(5,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Loss limit as a percentage');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-022', 'delegation_limit', 'min_price_pct_fmv', 'NUMBER', 'numeric(5,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Lowest sale price as a percentage of fair market value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-023', 'delegation_limit', 'holder_user_id', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Person holding the level');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-024', 'delegation_limit', 'substitute_user_id', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Substitute when the holder is absent');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-025', 'delegation_limit', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Valid from');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-026', 'delegation_limit', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Valid to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-055', 'delegation_limit', 'limit_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Delegation version the row belongs to, for example DOA-2026.11');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-056', 'delegation_limit', 'regulation_item', 'TEXT', 'varchar(10)', true, NULL, NULL, 'Workbench', NULL, false, 'Item of Regulation กกค.540031, for example 2.1.1; one decision code covers several items');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-057', 'delegation_limit', 'applies_when', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Workbench', NULL, false, 'Case condition that selects the row, WO_CRITERIA_MET or WO_CRITERIA_NOT_MET for item 2.1.10');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-058', 'delegation_limit', 'max_loss_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Maximum loss the level may approve, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-059', 'delegation_limit', 'max_delay_count', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Most delays of legal action, seizure or auction the level may approve on a case');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-060', 'delegation_limit', 'min_price_pct_principal', 'NUMBER', 'numeric(5,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Lowest sale price as a percentage of principal outstanding');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-061', 'delegation_limit', 'min_received_pct', 'NUMBER', 'numeric(5,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Lowest amount received against the total debt, percent');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-062', 'delegation_limit', 'max_term_years', 'NUMBER', 'numeric(4,1)', false, NULL, NULL, 'Workbench', NULL, false, 'Longest lease term the level may approve, years');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-027', 'lov_value', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the list value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-028', 'lov_value', 'lov_code', 'TEXT', 'varchar(30)', true, NULL, NULL, 'Workbench', NULL, false, 'List code, for example LOV-ROUTE');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-029', 'lov_value', 'value_code', 'TEXT', 'varchar(30)', true, NULL, NULL, 'Workbench', NULL, false, 'Value code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-030', 'lov_value', 'label_en', 'TEXT', 'varchar(120)', true, NULL, NULL, 'Workbench', NULL, false, 'English label');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-031', 'lov_value', 'label_th', 'TEXT', 'varchar(120)', false, NULL, NULL, 'Workbench', NULL, false, 'Thai label');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-032', 'lov_value', 'sort_order', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Display order');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-033', 'lov_value', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Valid from');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-034', 'role', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the role');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-035', 'role', 'role_code', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Role code, for example RW-CASEOWN');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-036', 'role', 'role_name', 'TEXT', 'varchar(80)', true, NULL, NULL, 'Workbench', NULL, false, 'Role name');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-037', 'role', 'role_class', 'LOV', 'varchar(15)', true, 'LOV-ROLE-CLASS', NULL, 'Workbench', NULL, false, 'Bank user, partner user, non-human actor');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-038', 'role', 'default_scope', 'LOV', 'varchar(8)', true, 'LOV-SCOPE', NULL, 'Workbench', NULL, false, 'Own, team, region, all');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-039', 'role', 'entra_group', 'TEXT', 'varchar(120)', false, NULL, NULL, 'Entra ID', NULL, false, 'Entra ID group mapped to the role');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-040', 'permission', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the permission');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-041', 'permission', 'role_id', 'CROSS_REF', 'uuid', true, NULL, 'role', 'Workbench', NULL, false, 'The role this record belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-042', 'permission', 'capability_area', 'LOV', 'varchar(30)', true, 'LOV-CAPABILITY', NULL, 'Workbench', NULL, false, 'One of the 14 capability areas');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-043', 'permission', 'letters', 'TEXT', 'varchar(5)', true, NULL, NULL, 'Workbench', NULL, false, 'C, R, U, D and A, or a dash for none');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-044', 'permission', 'matrix_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Permission matrix version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-045', 'template', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the template');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-046', 'template', 'template_code', 'TEXT', 'varchar(30)', true, NULL, NULL, 'Workbench', NULL, false, 'Template code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-047', 'template', 'template_version', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Version; unique with template_code, since a template holds several versions');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-048', 'template', 'language', 'LOV', 'varchar(2)', true, 'LOV-LANG', NULL, 'Workbench', NULL, false, 'Thai or English');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-049', 'template', 'product_group', 'LOV', 'varchar(15)', false, 'LOV-PRODUCT', NULL, 'Workbench', NULL, false, 'Product group it applies to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-050', 'template', 'body_ref', 'ATTACHMENT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'Stored template body');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-051', 'template', 'approved_by_legal', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True once Legal approves the wording');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-063', 'template', 'approved_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Legal counsel who approved the version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-064', 'template', 'approved_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the version was approved');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-065', 'template', 'valid_from', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Date from which the approved version is current');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-066', 'template', 'channel', 'LOV', 'varchar(15)', false, 'LOV-CHANNEL', NULL, 'Workbench', NULL, false, 'Channel the template is for: letter, SMS or LINE');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-067', 'template', 'notice_type', 'LOV', 'varchar(25)', false, 'LOV-NOTICE', NULL, 'Workbench', NULL, false, 'Notice type for a notice template; empty for other documents');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-068', 'template', 'signature_basis', 'LOV', 'varchar(20)', false, 'LOV-SIGNATURE-BASIS', NULL, 'Workbench', NULL, false, 'How Legal allows the document to be signed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-069', 'template', 'merge_codes', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'The merge codes the template body uses');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-070', 'data_product', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the data product');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-071', 'data_product', 'product_code', 'LOV', 'varchar(25)', true, 'LOV-DATA-PRODUCT', NULL, 'Workbench', NULL, false, 'Data product code DP01 to DP14');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-072', 'data_product', 'product_name', 'TEXT', 'varchar(80)', true, NULL, NULL, 'Workbench', NULL, false, 'Data product name, for example Account and arrears');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-073', 'data_product', 'definition', 'TEXT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'Definition of the product');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-074', 'data_product', 'system_of_record', 'TEXT', 'varchar(120)', true, NULL, NULL, 'Workbench', NULL, false, 'The one system of record for the product');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-075', 'data_product', 'owner_role', 'LOV', 'varchar(20)', true, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role of the owner, normally RW-DATASTEW');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-076', 'data_product', 'owner_user_id', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'The named owner of the product; required by the catalog load, empty in the seed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-077', 'data_product', 'refresh_cycle', 'LOV', 'varchar(10)', true, 'LOV-REFRESH', NULL, 'Workbench', NULL, false, 'Daily, weekly, monthly or on change');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-078', 'data_product', 'expected_by', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Time the load is expected by, for example 08:00 or MON 08:00');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-079', 'data_product', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the catalog version comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-080', 'data_product_access', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the data product access row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-081', 'data_product_access', 'product_code', 'LOV', 'varchar(25)', true, 'LOV-DATA-PRODUCT', NULL, 'Workbench', NULL, false, 'Data product the row grants');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-082', 'data_product_access', 'role_code', 'LOV', 'varchar(20)', true, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role the row applies to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-083', 'data_product_access', 'can_read', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when the role may read the product');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-084', 'data_product_access', 'access_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Version of the access table, for example DPA-2026.11');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-085', 'data_product_access', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the row comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-086', 'data_product_access', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Date the row ends');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-001', 'data_product_load', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the freshness stamp');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-002', 'data_product_load', 'product_code', 'LOV', 'varchar(25)', true, 'LOV-DATA-PRODUCT', NULL, 'Workbench', NULL, false, 'Data product loaded');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-003', 'data_product_load', 'source_system', 'TEXT', 'varchar(40)', true, NULL, NULL, 'Workbench', NULL, false, 'Source system of the load');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-004', 'data_product_load', 'business_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Business date of the load');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-005', 'data_product_load', 'source_extracted_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When the source extract was taken, from the COLLINS control record or the file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-006', 'data_product_load', 'loaded_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When the load committed in the Workbench');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-007', 'data_product_load', 'status', 'LOV', 'varchar(10)', true, 'LOV-FRESHNESS', NULL, 'Workbench', NULL, false, 'Loaded or stale');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-008', 'data_product_load', 'stale_flagged_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the product was flagged stale');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-009', 'data_product_load', 'duplicate_count', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Repeat stamps ignored for the same product and business date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-010', 'data_contract', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the data contract');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-011', 'data_contract', 'contract_code', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Contract code per source system, for example DC-ALS');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-012', 'data_contract', 'source_system', 'TEXT', 'varchar(80)', true, NULL, NULL, 'Workbench', NULL, false, 'Source system');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-013', 'data_contract', 'interface_id', 'TEXT', 'varchar(40)', true, NULL, NULL, 'Workbench', NULL, false, 'Interfaces covered, for example INT-01, INT-02');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-014', 'data_contract', 'contract_version', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Contract version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-015', 'data_contract', 'status', 'LOV', 'varchar(10)', true, 'LOV-CONTRACT-STATUS', NULL, 'Workbench', NULL, false, 'Draft, published or superseded');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-016', 'data_contract', 'confirmed_by_role', 'TEXT', 'varchar(80)', false, NULL, NULL, 'Workbench', NULL, false, 'Role of the system owner who confirmed, for example ALS system owner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-017', 'data_contract', 'confirmed_on', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Date of the confirmation');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-018', 'data_contract', 'confirmation_document_ref', 'ATTACHMENT', 'varchar(400)', false, NULL, NULL, 'Workbench', NULL, false, 'Stored confirmation from the system owner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-019', 'data_contract', 'published_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the contract was published');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-020', 'data_contract', 'published_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Who published the contract');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-087', 'sys_objects', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the registered object');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-088', 'sys_objects', 'object_name', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Table name');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-089', 'sys_objects', 'business_name', 'TEXT', 'varchar(120)', true, NULL, NULL, 'Workbench', NULL, false, 'Business name of the object');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-090', 'sys_objects', 'subject_area', 'TEXT', 'varchar(10)', true, NULL, NULL, 'Workbench', NULL, false, 'Subject area code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-091', 'sys_objects', 'data_product', 'TEXT', 'varchar(10)', true, NULL, NULL, 'Workbench', NULL, false, 'Data product the object belongs to, DP01 to DP14 or None');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-092', 'sys_objects', 'system_of_record', 'TEXT', 'varchar(120)', true, NULL, NULL, 'Workbench', NULL, false, 'System of record of the object');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-093', 'sys_objects', 'description', 'TEXT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'What the object holds');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-094', 'sys_fields', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the registered field');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-095', 'sys_fields', 'field_id', 'TEXT', 'varchar(16)', true, NULL, NULL, 'Workbench', NULL, false, 'BR Field ID, for example DF-CAS-001');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-096', 'sys_fields', 'object_name', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Table the field belongs to, from sys_objects');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-097', 'sys_fields', 'field_name', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Column name; unique with object_name');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-098', 'sys_fields', 'data_type', 'TEXT', 'varchar(12)', true, NULL, NULL, 'Workbench', NULL, false, 'TSD data type: TEXT, NUMBER, DATE, BOOLEAN, LOV, USER_REF, CROSS_REF, FORMULA or ATTACHMENT');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-099', 'sys_fields', 'physical_type', 'TEXT', 'varchar(30)', true, NULL, NULL, 'Workbench', NULL, false, 'PostgreSQL type');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-100', 'sys_fields', 'is_mandatory', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when the field is required');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-101', 'sys_fields', 'lov_code', 'TEXT', 'varchar(30)', false, NULL, NULL, 'Workbench', NULL, false, 'List of values the field takes its values from');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-102', 'sys_fields', 'references_object', 'TEXT', 'varchar(60)', false, NULL, NULL, 'Workbench', NULL, false, 'Table a cross-reference field points to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-103', 'sys_fields', 'source_system', 'TEXT', 'varchar(80)', true, NULL, NULL, 'Workbench', NULL, false, 'Source system of the value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-104', 'sys_fields', 'source_field', 'TEXT', 'varchar(80)', false, NULL, NULL, 'Workbench', NULL, false, 'Field name in the source system');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-105', 'sys_fields', 'is_personal', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True for personal data under PDPA');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-106', 'sys_fields', 'description', 'TEXT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'Meaning of the field');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-107', 'sys_fields', 'owner_role', 'LOV', 'varchar(20)', false, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Owner of the field definition');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-108', 'sys_fields', 'refresh_cycle', 'TEXT', 'varchar(30)', false, NULL, NULL, 'Workbench', NULL, false, 'Refresh frequency, for example Daily, end of day');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-109', 'sys_fields', 'late_behavior', 'TEXT', 'varchar(200)', false, NULL, NULL, 'Workbench', NULL, false, 'What the Workbench does when the value is missing or late');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-110', 'sys_fields', 'interface_id', 'TEXT', 'varchar(10)', false, NULL, NULL, 'Workbench', NULL, false, 'Interface that carries the field, INT-01 to INT-34; empty for Workbench fields');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-111', 'sys_field_version', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the field version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-112', 'sys_field_version', 'field_id', 'TEXT', 'varchar(16)', true, NULL, NULL, 'Workbench', NULL, false, 'Field the version belongs to, from sys_fields');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-113', 'sys_field_version', 'field_version', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Version number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-114', 'sys_field_version', 'definition', 'TEXT', 'jsonb', true, NULL, NULL, 'Workbench', NULL, false, 'The full field definition at this version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-115', 'sys_field_version', 'change_reason', 'TEXT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'Reason for the change');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-021', 'load_run', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the load or job run');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-022', 'load_run', 'interface_id', 'TEXT', 'varchar(10)', false, NULL, NULL, 'Workbench', NULL, false, 'Interface loaded, for example INT-01; TRACKER for tracker loads; empty for job steps');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-023', 'load_run', 'job_code', 'TEXT', 'varchar(6)', false, NULL, NULL, 'Workbench', NULL, false, 'Job the run belongs to, for example JOB-01');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-024', 'load_run', 'product_code', 'LOV', 'varchar(25)', false, 'LOV-DATA-PRODUCT', NULL, 'Workbench', NULL, false, 'Data product loaded or built');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-025', 'load_run', 'business_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Business date of the load');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-026', 'load_run', 'status', 'LOV', 'varchar(12)', true, 'LOV-LOAD-STATUS', NULL, 'Workbench', NULL, false, 'Running, completed, refused, late, failed or superseded');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-027', 'load_run', 'started_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When the run started');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-028', 'load_run', 'ended_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the run ended');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-029', 'load_run', 'rows_read', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Records read from the source');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-030', 'load_run', 'rows_loaded', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Records written');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-031', 'load_run', 'rows_held', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Records held in the exception list');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-032', 'load_run', 'rows_rejected', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Rows rejected');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-033', 'load_run', 'failed_check', 'TEXT', 'varchar(8)', false, NULL, NULL, 'Workbench', NULL, false, 'Check that refused the load, for example DQ-003');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-034', 'load_run', 'check_results', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Result per check code, plus the sample and other counts');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-035', 'load_run', 'mapping_version', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Source field mapping version used');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-036', 'load_run', 'interface_run_id', 'CROSS_REF', 'uuid', false, NULL, 'interface_run', 'Workbench', NULL, false, 'The P2 interface run the file load belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-037', 'load_run', 'tracker_id', 'CROSS_REF', 'uuid', false, NULL, 'tracker_inventory', 'Workbench', NULL, false, 'Tracker of a tracker load');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-038', 'load_run', 'loaded_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'User who uploaded the file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-039', 'load_run', 'source_file_name', 'TEXT', 'varchar(200)', false, NULL, NULL, 'Workbench', NULL, false, 'Name of the loaded file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-040', 'load_run', 'source_file_hash', 'TEXT', 'char(64)', false, NULL, NULL, 'Workbench', NULL, false, 'SHA-256 of the loaded file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-041', 'dq_exception', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the data quality exception');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-042', 'dq_exception', 'load_run_id', 'CROSS_REF', 'uuid', true, NULL, 'load_run', 'Workbench', NULL, false, 'The load run that raised it');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-043', 'dq_exception', 'product_code', 'LOV', 'varchar(25)', true, 'LOV-DATA-PRODUCT', NULL, 'Workbench', NULL, false, 'Data product of the record');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-044', 'dq_exception', 'check_code', 'TEXT', 'varchar(8)', true, NULL, NULL, 'Workbench', NULL, false, 'Load check (DQ-nnn), row rule (DQnn), reconciliation (REC-nn) or tracker check (TRK-nn)');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-045', 'dq_exception', 'record_key', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Business key of the failing record, for example the account number; never personal data');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-046', 'dq_exception', 'reason_code', 'TEXT', 'varchar(8)', true, NULL, NULL, 'Workbench', NULL, false, 'Reason code shown to the data product owner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-047', 'dq_exception', 'detail', 'TEXT', 'varchar(400)', false, NULL, NULL, 'Workbench', NULL, false, 'Short reason without personal data');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-048', 'dq_exception', 'raised_on', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Business date raised');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-049', 'dq_exception', 'status', 'LOV', 'varchar(10)', true, 'LOV-DQ-STATUS', NULL, 'Workbench', NULL, false, 'Open or cleared');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-050', 'dq_exception', 'rule_version', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Rule version that raised the exception');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-051', 'dq_exception', 'cleared_on', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Date the record passed again');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-052', 'dq_rule', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the data quality rule');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-053', 'dq_rule', 'rule_code', 'TEXT', 'varchar(8)', true, NULL, NULL, 'Workbench', NULL, false, 'Rule code, for example DQ02');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-054', 'dq_rule', 'rule_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Rule version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-055', 'dq_rule', 'rule_name', 'TEXT', 'varchar(120)', true, NULL, NULL, 'Workbench', NULL, false, 'Rule name');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-056', 'dq_rule', 'product_code', 'LOV', 'varchar(25)', true, 'LOV-DATA-PRODUCT', NULL, 'Workbench', NULL, false, 'Data product the rule runs for');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-057', 'dq_rule', 'target_entity', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'P1 table the rule checks');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-058', 'dq_rule', 'rule_type', 'LOV', 'varchar(15)', true, 'LOV-DQ-RULE-TYPE', NULL, 'Workbench', NULL, false, 'Not null, unique across, range, sum equals, exists link, maximum age in days, field before');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-059', 'dq_rule', 'rule_params', 'TEXT', 'jsonb', true, NULL, NULL, 'Workbench', NULL, false, 'Fields and values for the rule type');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-060', 'dq_rule', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the version comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-061', 'dq_rule', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the version is in force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-062', 'dq_rule', 'approved_by', 'USER_REF', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Who approved the version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-063', 'dq_rule', 'test_case_id', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Test case that proves the rule');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-064', 'source_field_map', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the source field mapping');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-065', 'source_field_map', 'interface_id', 'TEXT', 'varchar(10)', true, NULL, NULL, 'Workbench', NULL, false, 'Interface the mapping is for');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-066', 'source_field_map', 'mapping_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Mapping version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-067', 'source_field_map', 'source_field', 'TEXT', 'varchar(80)', true, NULL, NULL, 'Workbench', NULL, false, 'Field name in the source');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-068', 'source_field_map', 'target_entity', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Workbench entity');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-069', 'source_field_map', 'target_field', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Workbench field');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-070', 'source_field_map', 'transformation', 'TEXT', 'varchar(200)', true, NULL, NULL, 'Workbench', NULL, false, 'Transformation type and parameters: COPY_TRIM, SUM, TO_DATE_BE, TO_NUMERIC_2, BOOLEAN_YN, CODE_MAP, BUSINESS_DATE');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-071', 'source_field_map', 'approved_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Who approved the mapping version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-072', 'source_field_map', 'approved_on', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Approval date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-073', 'source_field_map', 'approval_ref', 'TEXT', 'varchar(200)', false, NULL, NULL, 'Workbench', NULL, false, 'Reference of the system owner''s sign-off on the mapping version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-074', 'source_field_map', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the version comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-075', 'source_code_map', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the source code mapping');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-076', 'source_code_map', 'interface_id', 'TEXT', 'varchar(10)', true, NULL, NULL, 'Workbench', NULL, false, 'Interface the code map is for');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-077', 'source_code_map', 'lov_code', 'TEXT', 'varchar(30)', true, NULL, NULL, 'Workbench', NULL, false, 'Target list of values');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-078', 'source_code_map', 'source_code', 'TEXT', 'varchar(30)', true, NULL, NULL, 'Workbench', NULL, false, 'Code in the source');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-079', 'source_code_map', 'value_code', 'TEXT', 'varchar(30)', true, NULL, NULL, 'Workbench', NULL, false, 'Workbench list value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-080', 'source_code_map', 'map_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Code map version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-081', 'source_code_map', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the version comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-082', 'source_code_map', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the version is in force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-083', 'tracker_inventory', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the tracker');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-084', 'tracker_inventory', 'tracker_code', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Tracker code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-085', 'tracker_inventory', 'inventory_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Inventory version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-086', 'tracker_inventory', 'team_code', 'LOV', 'varchar(20)', true, 'LOV-TEAM', NULL, 'Workbench', NULL, false, 'Owning team');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-087', 'tracker_inventory', 'tracker_name', 'TEXT', 'varchar(120)', true, NULL, NULL, 'Workbench', NULL, false, 'Tracker name');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-088', 'tracker_inventory', 'location_type', 'LOV', 'varchar(12)', true, 'LOV-TRACKER-LOCATION', NULL, 'Workbench', NULL, false, 'Excel, SharePoint, local file or none');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-089', 'tracker_inventory', 'location_ref', 'TEXT', 'varchar(400)', false, NULL, NULL, 'Workbench', NULL, false, 'Where the tracker is kept');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-090', 'tracker_inventory', 'owner_user_id', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Tracker owner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-091', 'tracker_inventory', 'field_list', 'TEXT', 'jsonb', true, NULL, NULL, 'Workbench', NULL, false, 'Field names with the personal data tag and the optional mapped-to field');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-092', 'tracker_inventory', 'update_cycle', 'LOV', 'varchar(10)', false, 'LOV-UPDATE-CYCLE', NULL, 'Workbench', NULL, false, 'Daily, weekly, monthly or ad hoc');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-093', 'tracker_inventory', 'target_product', 'LOV', 'varchar(25)', false, 'LOV-DATA-PRODUCT', NULL, 'Workbench', NULL, false, 'Target data product for a LOAD decision');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-094', 'tracker_inventory', 'decision', 'LOV', 'varchar(8)', false, 'LOV-TRACKER-DECISION', NULL, 'Workbench', NULL, false, 'Load, retire or keep');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-095', 'tracker_inventory', 'decision_reason', 'TEXT', 'varchar(400)', false, NULL, NULL, 'Workbench', NULL, false, 'Reason for the decision');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-096', 'tracker_inventory', 'status', 'LOV', 'varchar(12)', true, 'LOV-TRACKER-STATUS', NULL, 'Workbench', NULL, false, 'Listed, loaded, signed off, retired or kept');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-097', 'tracker_inventory', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the inventory version comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-098', 'tracker_inventory', 'file_rows', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Rows in the loaded file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-099', 'tracker_inventory', 'loaded_rows', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Rows loaded');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-100', 'tracker_inventory', 'rejected_rows', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Rows rejected');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-101', 'tracker_inventory', 'last_load_run_id', 'CROSS_REF', 'uuid', false, NULL, 'load_run', 'Workbench', NULL, false, 'Latest load run of the tracker');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-102', 'tracker_inventory', 'signed_off_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Team manager who signed off the load');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-103', 'tracker_inventory', 'signed_off_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'Sign-off time');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-104', 'tracker_inventory', 'source_file_ref', 'ATTACHMENT', 'varchar(400)', false, NULL, NULL, 'Workbench', NULL, false, 'Stored tracker file in the write-once store');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-105', 'tracker_inventory', 'archive_ref', 'TEXT', 'varchar(400)', false, NULL, NULL, 'Workbench', NULL, false, 'Read-only archive location of the retired tracker');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-106', 'tracker_inventory', 'retired_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'Retirement time');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-107', 'tracker_inventory', 'retire_confirmed_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Team manager who confirmed the retirement');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-108', 'tracker_inventory', 'unfed_fields', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Non-personal tracker fields no data product field carries');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-109', 'tracker_row', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the tracker row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-110', 'tracker_row', 'tracker_id', 'CROSS_REF', 'uuid', true, NULL, 'tracker_inventory', 'Workbench', NULL, false, 'Tracker the row came from');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-111', 'tracker_row', 'load_run_id', 'CROSS_REF', 'uuid', true, NULL, 'load_run', 'Workbench', NULL, false, 'Load run that loaded the row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-112', 'tracker_row', 'row_no', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Row number in the file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-113', 'tracker_row', 'account_no', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Account number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-114', 'tracker_row', 'target_product', 'LOV', 'varchar(25)', true, 'LOV-DATA-PRODUCT', NULL, 'Workbench', NULL, false, 'Target data product');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-115', 'tracker_row', 'source_file_name', 'TEXT', 'varchar(200)', true, NULL, NULL, 'Workbench', NULL, false, 'Source file name');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-116', 'tracker_row', 'field_values', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Non-personal tracker fields of the row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-117', 'tracker_row', 'loaded_on', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Load date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-001', 'case_list_row', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the case list row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-002', 'case_list_row', 'business_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Business date of the list');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-003', 'case_list_row', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'Case');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-004', 'case_list_row', 'case_no', 'TEXT', 'varchar(18)', true, NULL, NULL, 'Workbench', NULL, false, 'Case number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-005', 'case_list_row', 'account_id', 'CROSS_REF', 'uuid', true, NULL, 'loan_account', 'Workbench', NULL, false, 'Loan account; unique with business_date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-006', 'case_list_row', 'account_no', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Account number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-007', 'case_list_row', 'product_group', 'LOV', 'varchar(15)', true, 'LOV-PRODUCT', NULL, 'Workbench', NULL, false, 'Product group');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-008', 'case_list_row', 'stage_code', 'LOV', 'varchar(20)', false, 'LOV-STAGE', NULL, 'Workbench', NULL, false, 'Stage');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-009', 'case_list_row', 'status', 'LOV', 'varchar(20)', true, 'LOV-CASE-STATUS', NULL, 'Workbench', NULL, false, 'Case status');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-010', 'case_list_row', 'owner_user_id', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Case owner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-011', 'case_list_row', 'queue_code', 'TEXT', 'varchar(30)', false, NULL, NULL, 'Workbench', NULL, false, 'Queue code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-012', 'case_list_row', 'team_code', 'LOV', 'varchar(20)', false, 'LOV-TEAM', NULL, 'Workbench', NULL, false, 'Team');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-013', 'case_list_row', 'route_code', 'LOV', 'varchar(4)', false, 'LOV-ROUTE', NULL, 'Workbench', NULL, false, 'Route');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-014', 'case_list_row', 'total_balance', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'Workbench', NULL, false, 'Total balance, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-015', 'case_list_row', 'days_past_due', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Days past due');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-016', 'case_list_row', 'refreshed_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When the row was built');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-017', 'case_list_row', 'last_contact_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'Latest EFS contact across the case''s accounts');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-018', 'case_list_row', 'last_action_code', 'LOV', 'varchar(10)', false, 'LOV-ACTION-CODE', NULL, 'Workbench', NULL, false, 'Action code of the latest contact');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-019', 'case_list_row', 'publish_status', 'LOV', 'varchar(10)', true, 'LOV-PUBLISH-STATUS', NULL, 'Workbench', NULL, false, 'Pending, held or released for the date''s extract');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-030', 'collections_history', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the collections history record');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-031', 'collections_history', 'account_no', 'TEXT', 'varchar(20)', true, NULL, NULL, 'EFS via COLLINS', NULL, false, 'Account number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-032', 'collections_history', 'efs_record_key', 'TEXT', 'varchar(40)', true, NULL, NULL, 'EFS via COLLINS', NULL, false, 'EFS record key');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-033', 'collections_history', 'contact_at', 'DATE', 'timestamptz', true, NULL, NULL, 'EFS via COLLINS', NULL, false, 'Contact date and time');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-034', 'collections_history', 'action_code', 'LOV', 'varchar(10)', true, 'LOV-ACTION-CODE', NULL, 'EFS via COLLINS', 'Actioncode ID', false, 'EFS action code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-035', 'collections_history', 'action_contact_status', 'TEXT', 'varchar(20)', false, NULL, NULL, 'EFS via COLLINS', NULL, false, 'EFS action contact status');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-036', 'collections_history', 'contact_result', 'LOV', 'varchar(20)', false, 'LOV-CONTACT-RESULT', NULL, 'EFS via COLLINS', 'Call Result', false, 'Call result');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-037', 'collections_history', 'promise_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'EFS via COLLINS', NULL, false, 'Amount promised, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-038', 'collections_history', 'promise_date', 'DATE', 'date', false, NULL, NULL, 'EFS via COLLINS', NULL, false, 'Date promised');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-INT-039', 'collections_history', 'business_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Business date of the load');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-118', 'reconciliation_result', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the reconciliation result');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-119', 'reconciliation_result', 'rec_code', 'TEXT', 'varchar(6)', true, NULL, NULL, 'Workbench', NULL, false, 'Reconciliation, REC-01 or REC-02');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-120', 'reconciliation_result', 'business_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Business date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-121', 'reconciliation_result', 'product_group', 'LOV', 'varchar(15)', true, 'LOV-PRODUCT', NULL, 'Workbench', NULL, false, 'Product group');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-122', 'reconciliation_result', 'source_count', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'ALS count');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-123', 'reconciliation_result', 'workbench_count', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Case list count');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-124', 'reconciliation_result', 'source_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'ALS balance sum, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-125', 'reconciliation_result', 'workbench_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Case list balance sum, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-126', 'reconciliation_result', 'variance_count', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Count difference');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-127', 'reconciliation_result', 'variance_pct', 'NUMBER', 'numeric(9,4)', true, NULL, NULL, 'Workbench', NULL, false, 'Variance, percent');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-128', 'reconciliation_result', 'tolerance_pct', 'NUMBER', 'numeric(9,4)', true, NULL, NULL, 'Workbench', NULL, false, 'Tolerance used, percent');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-129', 'reconciliation_result', 'result', 'LOV', 'varchar(8)', true, 'LOV-REC-RESULT', NULL, 'Workbench', NULL, false, 'Pass or break');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-130', 'lake_copy_watermark', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the lake copy watermark');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-131', 'lake_copy_watermark', 'copy_name', 'TEXT', 'varchar(40)', true, NULL, NULL, 'Workbench', NULL, false, 'Name of the copy; DECISION_LOG for the decision log lake copy');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-132', 'lake_copy_watermark', 'last_entry_hash', 'TEXT', 'char(64)', false, NULL, NULL, 'Workbench', NULL, false, 'Entry hash of the last decision log entry copied and matched');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-133', 'lake_copy_watermark', 'last_decided_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'decided_at of the last entry copied');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-134', 'lake_copy_watermark', 'rows_copied_total', 'NUMBER', 'bigint', true, NULL, NULL, 'Workbench', NULL, false, 'Cumulative count of entries in the lake copy');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-135', 'lake_copy_watermark', 'business_date', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Business date of the last complete partition');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-116', 'retention_rule', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the retention rule');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-117', 'retention_rule', 'product_code', 'LOV', 'varchar(25)', true, 'LOV-DATA-PRODUCT', NULL, 'Workbench', NULL, false, 'Data product the rule applies to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-118', 'retention_rule', 'table_name', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Table the rule applies to, from sys_objects; never decision_log_entry');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-119', 'retention_rule', 'record_class', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Retention class from LOV-RETENTION, or LAKE_COPY for the decision log lake copy');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-120', 'retention_rule', 'retention_months', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Retention period in months, 1 to 600');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-121', 'retention_rule', 'age_basis_field', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Field the age is measured from, for example interaction.occurred_at');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-122', 'retention_rule', 'end_action', 'LOV', 'varchar(12)', true, 'LOV-RETENTION-END', NULL, 'Workbench', NULL, false, 'Archive or review at the end of the period');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-123', 'retention_rule', 'rule_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Version, for example RET-2026.11');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-124', 'retention_rule', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the version comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-125', 'retention_rule', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the version is in force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-126', 'retention_rule', 'approved_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Who approved the version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-127', 'retention_rule', 'reference_version_id', 'CROSS_REF', 'uuid', false, NULL, 'reference_version', 'Workbench', NULL, false, 'Reference version that brought the row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-034', 'dp_treatment', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the treatment copy');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-035', 'dp_treatment', 'treatment_id', 'CROSS_REF', 'uuid', true, NULL, 'treatment', 'Workbench', 'treatment.id', false, 'The treatment copied; unique with business_date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-036', 'dp_treatment', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', 'treatment.case_id', false, 'The case of the treatment');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-037', 'dp_treatment', 'decision_log_id', 'CROSS_REF', 'uuid', false, NULL, 'decision_log_entry', 'Workbench', 'treatment.decision_log_id', false, 'The decision that approved the treatment');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-038', 'dp_treatment', 'treatment_type', 'LOV', 'varchar(20)', true, 'LOV-TREATMENT', NULL, 'Workbench', 'treatment.treatment_type', false, 'Treatment type');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-039', 'dp_treatment', 'proposed_by', 'LOV', 'varchar(10)', true, 'LOV-PROPOSER', NULL, 'Workbench', 'treatment.proposed_by', false, 'Agent, rule or person');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-040', 'dp_treatment', 'proposed_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', 'treatment.proposed_at', false, 'When proposed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-041', 'dp_treatment', 'offer_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', 'treatment.offer_amount', false, 'Amount offered or agreed, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-042', 'dp_treatment', 'haircut_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', 'treatment.haircut_amount', false, 'Amount forgiven, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-043', 'dp_treatment', 'installments', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', 'treatment.installments', false, 'Number of installments in a plan');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-044', 'dp_treatment', 'valid_until', 'DATE', 'date', false, NULL, NULL, 'Workbench', 'treatment.valid_until', false, 'Offer validity');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-045', 'dp_treatment', 'approval_level', 'LOV', 'varchar(4)', false, 'LOV-APPROVAL-LEVEL', NULL, 'Workbench', 'treatment.approval_level', false, 'Approval level that approved it');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-046', 'dp_treatment', 'booked_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', 'treatment.booked_at', false, 'When booked in the core');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-047', 'dp_treatment', 'outcome', 'LOV', 'varchar(12)', false, 'LOV-TRT-OUTCOME', NULL, 'Workbench', 'treatment.outcome', false, 'Kept, broken, completed, canceled or declined');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-048', 'dp_treatment', 'outcome_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', 'treatment.outcome_at', false, 'When the outcome was recorded');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-049', 'dp_treatment', 'business_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Business date of the build');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-050', 'dp_treatment', 'contract_no', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Core bank (ALS) via COLLINS', 'ContractNo', false, 'Contract number of the case''s primary account');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-051', 'dp_treatment', 'contract_date', 'DATE', 'date', false, NULL, NULL, 'Core bank (ALS) via COLLINS', 'CONTRACT_DATE', false, 'Contract date of the case''s primary account');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-052', 'dp_guarantee_claim', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the guarantee claim copy');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-053', 'dp_guarantee_claim', 'guarantee_claim_id', 'CROSS_REF', 'uuid', true, NULL, 'guarantee_claim', 'Workbench', 'guarantee_claim.id', false, 'The guarantee claim copied; unique with business_date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-054', 'dp_guarantee_claim', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', 'guarantee_claim.case_id', false, 'The case of the claim');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-055', 'dp_guarantee_claim', 'claim_type', 'LOV', 'varchar(25)', true, 'LOV-CLAIM-TYPE', NULL, 'Workbench', 'guarantee_claim.claim_type', false, 'TCG, credit life insurance, mortgage insurance or collateral insurance');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-056', 'dp_guarantee_claim', 'claim_deadline', 'DATE', 'date', true, NULL, NULL, 'Workbench', 'guarantee_claim.claim_deadline', false, 'Last date the claim can be filed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-057', 'dp_guarantee_claim', 'claimed_amount', 'NUMBER', 'numeric(18,2)', true, NULL, NULL, 'Workbench', 'guarantee_claim.claimed_amount', false, 'Amount claimed, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-058', 'dp_guarantee_claim', 'filed_at', 'DATE', 'date', false, NULL, NULL, 'Workbench', 'guarantee_claim.filed_at', false, 'Date filed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-059', 'dp_guarantee_claim', 'paid_amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', 'guarantee_claim.paid_amount', false, 'Amount paid, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-060', 'dp_guarantee_claim', 'status', 'LOV', 'varchar(12)', true, 'LOV-CLAIM-STATUS', NULL, 'Workbench', 'guarantee_claim.status', false, 'Preparing, filed, defect, paid or rejected');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-TRT-061', 'dp_guarantee_claim', 'business_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Business date of the build');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-136', 'interface_config', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the interface setting');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-137', 'interface_config', 'interface_id', 'TEXT', 'varchar(10)', true, NULL, NULL, 'Workbench', NULL, false, 'Interface ID, for example INT-10');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-138', 'interface_config', 'direction', 'LOV', 'varchar(8)', true, 'LOV-DIRECTION', NULL, 'Workbench', NULL, false, 'Inbound or outbound');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-139', 'interface_config', 'transport', 'LOV', 'varchar(10)', true, 'LOV-TRANSPORT', NULL, 'Workbench', NULL, false, 'SFTP or COLLINS');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-140', 'interface_config', 'inbound_path', 'TEXT', 'varchar(200)', false, NULL, NULL, 'Workbench', NULL, false, 'Inbound or outbound folder');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-141', 'interface_config', 'file_pattern', 'TEXT', 'varchar(120)', false, NULL, NULL, 'Workbench', NULL, false, 'File name pattern with the business date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-142', 'interface_config', 'data_product', 'LOV', 'varchar(25)', false, 'LOV-DATA-PRODUCT', NULL, 'Workbench', NULL, false, 'Data product the file feeds, for example DP06');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-143', 'interface_config', 'max_attempts', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Most send attempts before the exception queue');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-144', 'interface_config', 'retry_intervals_min', 'TEXT', 'varchar(60)', false, NULL, NULL, 'Workbench', NULL, false, 'Minutes between attempts, comma separated, for example 5,15,45');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-145', 'interface_config', 'owner_role', 'LOV', 'varchar(20)', true, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role that receives the exception task');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-146', 'interface_config', 'alert_role', 'LOV', 'varchar(20)', false, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role alerted on a refused or missing file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-147', 'interface_config', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the version comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-148', 'interface_config', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the version is in force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-149', 'interface_run', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the interface run');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-150', 'interface_run', 'interface_id', 'TEXT', 'varchar(10)', true, NULL, NULL, 'Workbench', NULL, false, 'Interface ID');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-151', 'interface_run', 'file_name', 'TEXT', 'varchar(200)', true, NULL, NULL, 'Workbench', NULL, false, 'File name');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-152', 'interface_run', 'file_hash', 'TEXT', 'char(64)', true, NULL, NULL, 'Workbench', NULL, false, 'SHA-256 of the file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-153', 'interface_run', 'business_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Business date of the file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-154', 'interface_run', 'record_count', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Records read');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-155', 'interface_run', 'control_total', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Control total from the trailer');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-156', 'interface_run', 'status', 'LOV', 'varchar(12)', true, 'LOV-INTERFACE-RUN', NULL, 'Workbench', NULL, false, 'Received, loaded, refused, missing, duplicate or failed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-157', 'interface_run', 'failed_check', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Workbench', NULL, false, 'Load check ID and name that refused the file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-158', 'interface_run', 'checks', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Result of each check and the run summary counts');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-159', 'interface_run', 'started_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'Run start');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-160', 'interface_run', 'ended_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'Run end');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-161', 'interface_signoff', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the interface sign-off');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-162', 'interface_signoff', 'interface_id', 'TEXT', 'varchar(10)', true, NULL, NULL, 'Workbench', NULL, false, 'Interface whose manual handling is retired');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-163', 'interface_signoff', 'from_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'First clean day counted');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-164', 'interface_signoff', 'to_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Last clean day counted');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-165', 'interface_signoff', 'clean_days', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Clean days in a row at sign-off');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-166', 'interface_signoff', 'signed_by', 'USER_REF', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Data steward who signed off');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-167', 'interface_signoff', 'signed_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When signed off');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-168', 'outbound_item', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the outbound item');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-169', 'outbound_item', 'interface_id', 'TEXT', 'varchar(10)', true, NULL, NULL, 'Workbench', NULL, false, 'Interface ID');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-170', 'outbound_item', 'idempotency_key', 'TEXT', 'varchar(120)', true, NULL, NULL, 'Workbench', NULL, false, 'Unique key of the outbound work');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-171', 'outbound_item', 'payload_ref', 'ATTACHMENT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'Stored file to send');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-172', 'outbound_item', 'case_ids', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Cases whose step waits on the file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-173', 'outbound_item', 'attempt_count', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Attempts made');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-174', 'outbound_item', 'next_attempt_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the next attempt is due');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-175', 'outbound_item', 'status', 'LOV', 'varchar(12)', true, 'LOV-OUTBOUND-STATUS', NULL, 'Workbench', NULL, false, 'Pending, sent, retry, exception or acknowledged');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-176', 'outbound_item', 'last_error', 'TEXT', 'varchar(400)', false, NULL, NULL, 'Workbench', NULL, false, 'Last transfer error, no personal data');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-177', 'outbound_item', 'owner_role', 'LOV', 'varchar(20)', true, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role that owns the exception task');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-178', 'processed_event', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the processed event');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-179', 'processed_event', 'consumer', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Consumer name');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-180', 'processed_event', 'idempotency_key', 'TEXT', 'varchar(120)', true, NULL, NULL, 'Workbench', NULL, false, 'Event or work key');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-181', 'processed_event', 'event_id', 'CROSS_REF', 'uuid', false, NULL, 'outbox_event', 'Workbench', NULL, false, 'Outbox event of the first delivery, where the key came from an event');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-182', 'processed_event', 'hit_count', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Deliveries seen, 1 on first');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-183', 'processed_event', 'last_seen_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the last repeat arrived');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-184', 'idempotency_key', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the idempotent request');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-185', 'idempotency_key', 'idempotency_key', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Idempotency-Key header value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-186', 'idempotency_key', 'endpoint', 'TEXT', 'varchar(100)', true, NULL, NULL, 'Workbench', NULL, false, 'Method and path of the request');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-187', 'idempotency_key', 'request_hash', 'TEXT', 'char(64)', true, NULL, NULL, 'Workbench', NULL, false, 'SHA-256 of the request body');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-188', 'idempotency_key', 'response', 'TEXT', 'jsonb', true, NULL, NULL, 'Workbench', NULL, false, 'Stored response returned to a repeat');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-189', 'outbox_event', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the outbox event');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-190', 'outbox_event', 'event_type', 'TEXT', 'varchar(40)', true, NULL, NULL, 'Workbench', NULL, false, 'Event name from EV-01 to EV-28, or an outbound work request type such as WIN_DISPATCH');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-191', 'outbox_event', 'schema_version', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Schema version of the payload; consumers accept the current and previous version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-192', 'outbox_event', 'case_id', 'CROSS_REF', 'uuid', false, NULL, 'recovery_case', 'Workbench', NULL, false, 'The case the event belongs to; empty for events with no case; unique with case_seq');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-193', 'outbox_event', 'case_seq', 'NUMBER', 'bigint', false, NULL, NULL, 'Workbench', NULL, false, 'Order of the event among the events of its case');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-194', 'outbox_event', 'idempotency_key', 'TEXT', 'varchar(120)', true, NULL, NULL, 'Workbench', NULL, false, 'Key passed to every consumer so a repeat is dropped; unique on its own');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-195', 'outbox_event', 'payload', 'TEXT', 'jsonb', true, NULL, NULL, 'Workbench', NULL, false, 'References and codes only; no personal data');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-196', 'outbox_event', 'actor_ref', 'TEXT', 'varchar(64)', false, NULL, NULL, 'Workbench', NULL, false, 'User ID or service identity that caused the event');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-197', 'outbox_event', 'occurred_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When the change happened');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-198', 'outbox_delivery', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the outbox delivery');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-199', 'outbox_delivery', 'event_id', 'CROSS_REF', 'uuid', true, NULL, 'outbox_event', 'Workbench', NULL, false, 'The outbox event delivered');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-200', 'outbox_delivery', 'consumer', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Consumer name from the consumer list; unique with event_id');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-201', 'outbox_delivery', 'status', 'LOV', 'varchar(12)', true, 'LOV-OUTBOX-DELIVERY', NULL, 'Workbench', NULL, false, 'Pending, retrying, delivered or exception');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-202', 'outbox_delivery', 'attempt_count', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Delivery attempts made');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-203', 'outbox_delivery', 'next_attempt_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When the next attempt is due');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-204', 'outbox_delivery', 'last_error_code', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Workbench', NULL, false, 'Code of the last failure returned by the consumer');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-205', 'outbox_delivery', 'delivered_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the consumer succeeded');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-206', 'outbox_delivery', 'task_id', 'CROSS_REF', 'uuid', false, NULL, 'task', 'Workbench', NULL, false, 'The RESOLVE_OUTBOX_DELIVERY task raised when the delivery entered the exception queue');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-207', 'feature_flag', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the feature flag');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-208', 'feature_flag', 'flag_key', 'TEXT', 'varchar(80)', true, NULL, NULL, 'Workbench', NULL, false, 'Flag key rwb.<module>.<short-name>');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-209', 'feature_flag', 'description', 'TEXT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'What the flag switches');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-210', 'feature_flag', 'owner_user_id', 'USER_REF', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Owner of the flag');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-211', 'feature_flag', 'owner_team', 'TEXT', 'varchar(60)', false, NULL, NULL, 'Workbench', NULL, false, 'Owning squad');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-212', 'feature_flag', 'default_on', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'Default value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-213', 'feature_flag', 'dev_on', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'Value in DEV');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-214', 'feature_flag', 'sit_on', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'Value in SIT');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-215', 'feature_flag', 'uat_on', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'Value in UAT');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-216', 'feature_flag', 'prod_on', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'Value in PROD');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-217', 'feature_flag', 'removal_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date by which the flag and its old path are removed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-218', 'feature_flag_change', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the feature flag change');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-219', 'feature_flag_change', 'flag_key', 'TEXT', 'varchar(80)', true, NULL, NULL, 'Workbench', NULL, false, 'Flag changed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-220', 'feature_flag_change', 'environment', 'LOV', 'varchar(4)', true, 'LOV-ENVIRONMENT', NULL, 'Workbench', NULL, false, 'DEV, SIT, UAT or PROD');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-221', 'feature_flag_change', 'old_value', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'Value before');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-222', 'feature_flag_change', 'new_value', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'Value after');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-223', 'feature_flag_change', 'reason', 'TEXT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'Reason for the change');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-224', 'job_catalog', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the job');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-225', 'job_catalog', 'job_id', 'TEXT', 'varchar(6)', true, NULL, NULL, 'Workbench', NULL, false, 'Job ID JOB-nn');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-226', 'job_catalog', 'job_name', 'TEXT', 'varchar(80)', true, NULL, NULL, 'Workbench', NULL, false, 'Job name from the batch schedule');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-227', 'job_catalog', 'owner_role', 'LOV', 'varchar(20)', true, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role that owns failures');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-228', 'job_catalog', 'schedule_text', 'TEXT', 'varchar(120)', true, NULL, NULL, 'Workbench', NULL, false, 'Schedule as in the batch schedule');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-229', 'job_catalog', 'runbook_path', 'TEXT', 'varchar(200)', false, NULL, NULL, 'Workbench', NULL, false, 'Path of the run book in the repository');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-230', 'job_catalog', 'expected_minutes', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Expected duration in minutes');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-231', 'job_catalog', 'alert_after_minutes', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Duration after which the owner is alerted');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-OPS-232', 'job_catalog', 'first_release', 'TEXT', 'varchar(3)', false, NULL, NULL, 'Workbench', NULL, false, 'Epic of first release, for example E1');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-022', 'party_product', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the party product');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-023', 'party_product', 'party_id', 'CROSS_REF', 'uuid', true, NULL, 'party', 'Workbench', NULL, false, 'The party that holds the product');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-024', 'party_product', 'product_type', 'TEXT', 'varchar(20)', true, NULL, NULL, 'SCBPDM via COLLINS', NULL, false, 'Product type from the customer profile');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-025', 'party_product', 'account_no', 'TEXT', 'varchar(20)', true, NULL, NULL, 'SCBPDM via COLLINS', NULL, false, 'Account number of the product, masked by role');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-026', 'party_product', 'product_status', 'LOV', 'varchar(15)', true, 'LOV-PRODUCT-STATUS', NULL, 'SCBPDM via COLLINS', NULL, false, 'Active, delinquent, closed or written off');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-PTY-027', 'party_product', 'data_as_of', 'DATE', 'date', true, NULL, NULL, 'SCBPDM via COLLINS', NULL, false, 'Business date of the customer profile load');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-128', 'efs_ledger_outcome', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the EFS ledger outcome row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-129', 'efs_ledger_outcome', 'action_code', 'LOV', 'varchar(10)', true, 'LOV-ACTION-CODE', NULL, 'Workbench', NULL, false, 'EFS action code named for the ledger');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-130', 'efs_ledger_outcome', 'channel', 'LOV', 'varchar(15)', true, 'LOV-CHANNEL', NULL, 'Workbench', NULL, false, 'Ledger channel for the action code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-131', 'efs_ledger_outcome', 'in_ledger', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when rows with this action code enter the ledger');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-056', 'case_entry_exclusion', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the case entry exclusion');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-057', 'case_entry_exclusion', 'account_id', 'CROSS_REF', 'uuid', true, NULL, 'loan_account', 'Workbench', NULL, false, 'The account excluded; unique with business_date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-058', 'case_entry_exclusion', 'business_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Business date of the exclusion');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-059', 'case_entry_exclusion', 'reason_code', 'LOV', 'varchar(20)', true, 'LOV-EXCLUSION-REASON', NULL, 'Workbench', NULL, false, 'Deceased, fraud, bankruptcy, active plan or open dispute');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-060', 'case_entry_exclusion', 'rule_id', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Exclusion rule that blocked the entry');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-CAS-061', 'case_entry_exclusion', 'rule_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Version of that rule');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-045', 'queue_member', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the queue member');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-046', 'queue_member', 'queue_id', 'CROSS_REF', 'uuid', true, NULL, 'queue', 'Workbench', NULL, false, 'The queue');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-047', 'queue_member', 'user_id', 'USER_REF', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'The person');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-048', 'queue_member', 'capacity', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Most open cases the person may hold in the queue');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-049', 'queue_member', 'skill_codes', 'TEXT', 'varchar(200)', false, NULL, NULL, 'Workbench', NULL, false, 'Skills of the person, comma separated');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-050', 'queue_member', 'table_version', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'QUEUE_MEMBER reference version the row belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-051', 'queue_member', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the row comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-WRK-052', 'queue_member', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the row is in force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-020', 'queue_measure', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the queue measure');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-021', 'queue_measure', 'queue_id', 'CROSS_REF', 'uuid', true, NULL, 'queue', 'Workbench', NULL, false, 'The queue measured; unique with as_of');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-022', 'queue_measure', 'as_of', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When the snapshot was taken');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-023', 'queue_measure', 'depth', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Open cases in the queue');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-024', 'queue_measure', 'unassigned', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Open cases with no owner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-025', 'queue_measure', 'avg_age_days', 'NUMBER', 'numeric(7,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Average age of the open cases, days');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-026', 'queue_measure', 'max_age_days', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Age of the oldest open case, days');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-027', 'queue_measure', 'owner_min', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Fewest open cases held by one owner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-028', 'queue_measure', 'owner_max', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Most open cases held by one owner');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-029', 'queue_measure', 'breached', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Open cases past their service level');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-030', 'queue_measure', 'status', 'LOV', 'varchar(15)', true, 'LOV-SNAPSHOT-STATUS', NULL, 'Workbench', NULL, false, 'Taken, published or held');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-132', 'parameter_catalog', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the parameter definition');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-133', 'parameter_catalog', 'param_key', 'TEXT', 'varchar(100)', true, NULL, NULL, 'Workbench', NULL, false, 'Parameter key, for example case.entry.dpd');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-134', 'parameter_catalog', 'kind', 'TEXT', 'varchar(15)', true, NULL, NULL, 'Workbench', NULL, false, 'Kind of parameter, for example ENVIRONMENT for an environment setting');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-135', 'parameter_catalog', 'value_type', 'TEXT', 'varchar(15)', true, NULL, NULL, 'Workbench', NULL, false, 'Type of the value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-136', 'parameter_catalog', 'unit', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Unit, for example CALENDAR_DAYS, WORKING_DAYS, BAHT, PERCENT, COUNT, CODE_LIST');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-137', 'parameter_catalog', 'min_value', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Workbench', NULL, false, 'Lowest allowed value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-138', 'parameter_catalog', 'max_value', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Workbench', NULL, false, 'Highest allowed value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-139', 'parameter_catalog', 'default_value', 'TEXT', 'varchar(400)', false, NULL, NULL, 'Workbench', NULL, false, 'Default value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-140', 'parameter_catalog', 'scope', 'LOV', 'varchar(10)', true, 'LOV-PARAM-SCOPE', NULL, 'Workbench', NULL, false, 'Product, when the parameter is keyed by product group, or global');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-141', 'parameter_catalog', 'required', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when every product in force must have a row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-142', 'parameter_catalog', 'owner_role', 'LOV', 'varchar(20)', true, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role that owns the parameter');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-143', 'parameter_catalog', 'environments', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Workbench', NULL, false, 'Environments the parameter is set in');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-144', 'parameter_catalog', 'used_by', 'TEXT', 'varchar(400)', false, NULL, NULL, 'Workbench', NULL, false, 'Modules and stories that read the parameter');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-145', 'parameter_catalog', 'secret', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True for a secret; its value is never returned');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-146', 'parameter_catalog', 'description', 'TEXT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'What the parameter controls');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-147', 'parameter_value', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the parameter value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-148', 'parameter_value', 'param_key', 'TEXT', 'varchar(100)', true, NULL, NULL, 'Workbench', NULL, false, 'Parameter, from parameter_catalog');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-149', 'parameter_value', 'environment', 'LOV', 'varchar(4)', true, 'LOV-ENVIRONMENT', NULL, 'Workbench', NULL, false, 'DEV, SIT, UAT or PROD');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-150', 'parameter_value', 'param_value', 'TEXT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'Value as text');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-151', 'parameter_value', 'product_group', 'LOV', 'varchar(15)', false, 'LOV-PRODUCT', NULL, 'Workbench', NULL, false, 'Product group for a product-scoped parameter');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-152', 'parameter_value', 'version_no', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Version number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-153', 'parameter_value', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the value comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-154', 'parameter_value', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the value is in force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-155', 'parameter_value', 'status', 'LOV', 'varchar(15)', true, 'LOV-VERSION-STATUS', NULL, 'Workbench', NULL, false, 'Validated, approved, in force, superseded, rolled back or refused');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-156', 'parameter_value', 'author_user_id', 'USER_REF', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Who loaded the value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-157', 'parameter_value', 'approver_user_id', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Who approved the value; never the author');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-158', 'parameter_value', 'approved_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the value was approved');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-159', 'reference_version', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the reference version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-160', 'reference_version', 'table_code', 'LOV', 'varchar(30)', true, 'LOV-REF-TABLE', NULL, 'Workbench', NULL, false, 'The reference or rule table the version belongs to, for example EXPOSURE_BAND or ALLOCATION');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-161', 'reference_version', 'version_no', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Version number, one above the previous version of the table');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-162', 'reference_version', 'version_label', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Version label the rows carry, for example DOCTYPE-2026.11');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-163', 'reference_version', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the version comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-164', 'reference_version', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the version is in force; set when the next version is approved');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-165', 'reference_version', 'status', 'LOV', 'varchar(15)', true, 'LOV-VERSION-STATUS', NULL, 'Workbench', NULL, false, 'Validated, approved, in force, superseded, rolled back or refused');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-166', 'reference_version', 'author_user_id', 'USER_REF', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Who loaded the version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-167', 'reference_version', 'approver_user_id', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Who approved the version; never the author');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-168', 'reference_version', 'approved_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the version was approved');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-169', 'reference_version', 'row_count', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Rows in the version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-170', 'reference_version', 'content_hash', 'TEXT', 'char(64)', true, NULL, NULL, 'Workbench', NULL, false, 'SHA-256 of the rows sorted by key; used for idempotency');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-171', 'reference_version', 'load_id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Identifier of the reference load request that created the version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-172', 'reference_version', 'dry_run_counts', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Counts of live cases each changed rule row would move, from the dry run');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-173', 'reference_version', 'rollback_reason', 'TEXT', 'varchar(400)', false, NULL, NULL, 'Workbench', NULL, false, 'Reason given for a rollback');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-174', 'reference_version', 'change_request_ref', 'TEXT', 'varchar(30)', false, NULL, NULL, 'Workbench', NULL, false, 'Reference of the change request in the bank''s request tool');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-175', 'reference_version', 'impact_summary', 'TEXT', 'varchar(1000)', false, NULL, NULL, 'Workbench', NULL, false, 'What the change affects, for example the open cases it touches');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-176', 'reference_version', 'test_result', 'LOV', 'varchar(10)', false, 'LOV-TEST-RESULT', NULL, 'Workbench', NULL, false, 'Passed or failed, from the load checks or the rule table test harness');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-177', 'reference_version', 'rollback_plan', 'TEXT', 'varchar(1000)', false, NULL, NULL, 'Workbench', NULL, false, 'How to return to the previous version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-178', 'reference_version', 'verified_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Who verified the change after it took effect');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-179', 'reference_version', 'verified_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the change was verified');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-180', 'reference_version', 'verify_note', 'TEXT', 'varchar(1000)', false, NULL, NULL, 'Workbench', NULL, false, 'What was checked');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-181', 'reference_row', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the reference row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-182', 'reference_row', 'version_id', 'CROSS_REF', 'uuid', true, NULL, 'reference_version', 'Workbench', NULL, false, 'The reference version the row belongs to; unique with row_key');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-183', 'reference_row', 'row_key', 'TEXT', 'varchar(200)', true, NULL, NULL, 'Workbench', NULL, false, 'Key of the row inside its table');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-184', 'reference_row', 'row_data', 'TEXT', 'jsonb', true, NULL, NULL, 'Workbench', NULL, false, 'Column values of the row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-185', 'rule_test_case', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the rule test case');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-186', 'rule_test_case', 'test_case_id', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'The test case named by rule_row.test_case_id');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-187', 'rule_test_case', 'route_set', 'LOV', 'varchar(15)', true, 'LOV-ROUTE-SET', NULL, 'Workbench', NULL, false, 'Route set');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-188', 'rule_test_case', 'rule_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Rule version tested');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-189', 'rule_test_case', 'rule_id', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Rule the test expects to hit');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-190', 'rule_test_case', 'from_state', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Input state');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-191', 'rule_test_case', 'event_code', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Input event');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-192', 'rule_test_case', 'facts', 'TEXT', 'jsonb', true, NULL, NULL, 'Workbench', NULL, false, 'Synthetic case file facts the condition reads');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-193', 'rule_test_case', 'expected_to_state', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Expected to state');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-194', 'rule_test_case', 'expected_owner_role', 'LOV', 'varchar(20)', false, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Expected owner role');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-195', 'rule_test_case', 'expected_timer_spec', 'TEXT', 'varchar(60)', false, NULL, NULL, 'Workbench', NULL, false, 'Expected timer');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-196', 'rule_test_case', 'result', 'LOV', 'varchar(10)', false, 'LOV-TEST-RESULT', NULL, 'Workbench', NULL, false, 'Passed or failed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-197', 'rule_test_case', 'result_detail', 'TEXT', 'varchar(1000)', false, NULL, NULL, 'Workbench', NULL, false, 'Expected against actual, and the rows that hit');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-198', 'masking_rule', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the masking rule');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-199', 'masking_rule', 'role_code', 'LOV', 'varchar(20)', true, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role the rule applies to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-200', 'masking_rule', 'field_id', 'TEXT', 'varchar(16)', true, NULL, NULL, 'Workbench', NULL, false, 'BR Field ID of a personal data field (sys_fields.is_personal true)');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-201', 'masking_rule', 'unmasked', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when the role sees the field unmasked; no row means masked');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-202', 'masking_rule', 'masking_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Version of the masking rules, for example MASK-2026.11');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-203', 'masking_rule', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the version comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-204', 'masking_rule', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the version is in force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-205', 'role_conflict', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the role conflict');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-206', 'role_conflict', 'role_code', 'LOV', 'varchar(20)', true, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role that may not be held with the other');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-207', 'role_conflict', 'conflicts_with', 'TEXT', 'varchar(30)', true, NULL, NULL, 'Workbench', NULL, false, 'Role code, or ANY_BUSINESS_ROLE or ANY_OTHER_ROLE, per the Separation of duty sheet');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-208', 'role_conflict', 'reason', 'TEXT', 'varchar(200)', true, NULL, NULL, 'Workbench', NULL, false, 'Why the pair is not allowed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-209', 'role_conflict', 'conflict_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Version of the conflict table, for example SOD-2026.11');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-210', 'role_conflict', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the version comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-211', 'role_conflict', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the version is in force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-212', 'partner_user', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the partner user');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-213', 'partner_user', 'identity_ref', 'TEXT', 'varchar(64)', true, NULL, NULL, 'Workbench', NULL, false, 'Partner identity directory ID');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-214', 'partner_user', 'partner_id', 'CROSS_REF', 'uuid', true, NULL, 'partner', 'Workbench', NULL, false, 'The firm the partner user works for');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-215', 'partner_user', 'role_code', 'LOV', 'varchar(20)', true, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'The one partner role held, for example PT-LAWFIRM');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-216', 'partner_user', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the binding starts');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-217', 'partner_user', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Date the binding ends; no later than the firm''s contract end');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-218', 'document_type', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the document type');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-219', 'document_type', 'doc_type_code', 'TEXT', 'varchar(30)', true, NULL, NULL, 'Workbench', NULL, false, 'Document type code, the value set of LOV-DOC-TYPE');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-220', 'document_type', 'label_en', 'TEXT', 'varchar(120)', true, NULL, NULL, 'Workbench', NULL, false, 'English label');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-221', 'document_type', 'label_th', 'TEXT', 'varchar(120)', false, NULL, NULL, 'Workbench', NULL, false, 'Thai label');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-222', 'document_type', 'write_once', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True for a legal type held in the write-once container');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-223', 'document_type', 'retention_class', 'LOV', 'varchar(10)', true, 'LOV-RETENTION', NULL, 'Workbench', NULL, false, 'Retention class of the type');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-224', 'document_type', 'field_definitions', 'TEXT', 'jsonb', true, NULL, NULL, 'Workbench', NULL, false, 'Fields extracted from the type: name, label, data type, personal flag, required flag, extraction method (TEMPLATE or MODEL), review only flag and optional pattern');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-225', 'document_type', 'legal_signoff_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Legal counsel user who signed the type and its fields');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-226', 'document_type', 'legal_signoff_date', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Date of the Legal sign-off');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-227', 'document_type', 'npa_signoff_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Head of NPA user who signed the type and its fields');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-228', 'document_type', 'npa_signoff_date', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Date of the NPA sign-off');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-229', 'document_type', 'table_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Version of the type table, for example DOCTYPE-2026.11');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-230', 'document_type', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the version comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-231', 'document_type', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the version is in force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-232', 'document_type', 'reference_version_id', 'CROSS_REF', 'uuid', false, NULL, 'reference_version', 'Workbench', NULL, false, 'Reference version that brought the row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-233', 'document_type', 'classify_threshold', 'NUMBER', 'numeric(4,3)', false, NULL, NULL, 'Workbench', NULL, false, 'Confidence below which a document of this type goes to the review queue');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-234', 'document_checklist_item', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the checklist item');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-235', 'document_checklist_item', 'stage_code', 'LOV', 'varchar(20)', true, 'LOV-STAGE', NULL, 'Workbench', NULL, false, 'Case stage the row applies to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-236', 'document_checklist_item', 'route_code', 'LOV', 'varchar(4)', false, 'LOV-ROUTE', NULL, 'Workbench', NULL, false, 'Route the row applies to; empty for every route');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-237', 'document_checklist_item', 'document_type', 'LOV', 'varchar(30)', true, 'LOV-DOC-TYPE', NULL, 'Workbench', NULL, false, 'Document type');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-238', 'document_checklist_item', 'required', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when the type is required for the stage and route');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-239', 'document_checklist_item', 'sort_order', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Order of the item on the checklist');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-240', 'document_checklist_item', 'table_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Version of the checklist, for example CHK-2026.11');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-241', 'document_checklist_item', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the version comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-242', 'document_checklist_item', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the version is in force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-243', 'document_checklist_item', 'reference_version_id', 'CROSS_REF', 'uuid', false, NULL, 'reference_version', 'Workbench', NULL, false, 'Reference version that brought the row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-036', 'case_document_check', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the completeness check');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-037', 'case_document_check', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'Case checked; one row per case; unique');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-038', 'case_document_check', 'checklist_version', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Checklist version used');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-039', 'case_document_check', 'required_count', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Number of required types');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-040', 'case_document_check', 'present_count', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Number of required types present');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-041', 'case_document_check', 'missing_types', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Required types not present');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-042', 'case_document_check', 'complete', 'BOOLEAN', 'boolean', false, NULL, NULL, 'Workbench', NULL, false, 'True when every required type is present; empty when the stage has no checklist');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-043', 'case_document_check', 'checked_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When the check last ran');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-044', 'case_document_check', 'last_event_id', 'CROSS_REF', 'uuid', false, NULL, 'outbox_event', 'Workbench', NULL, false, 'Event that triggered the last check, for repeat detection');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-244', 'document_hub_parameter', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the document hub parameter');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-245', 'document_hub_parameter', 'param_code', 'TEXT', 'varchar(40)', true, NULL, NULL, 'Workbench', NULL, false, 'Parameter code, for example INTAKE_MAX_FILE_MB, OCR_MIN_QUALITY, CLASSIFY_THRESHOLD, CASE_NO_PATTERN, SEARCH_MAX_RESULTS');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-246', 'document_hub_parameter', 'param_value', 'TEXT', 'varchar(200)', true, NULL, NULL, 'Workbench', NULL, false, 'Parameter value as text, typed by the reader');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-247', 'document_hub_parameter', 'unit', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Unit of the value, for example MB, seconds, ratio');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-248', 'document_hub_parameter', 'table_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Version of the parameter load');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-249', 'document_hub_parameter', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the value comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-250', 'document_hub_parameter', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the value is in force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-251', 'document_hub_parameter', 'reference_version_id', 'CROSS_REF', 'uuid', false, NULL, 'reference_version', 'Workbench', NULL, false, 'Reference version that brought the row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-045', 'document_intake', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the intake item');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-046', 'document_intake', 'source', 'LOV', 'varchar(12)', true, 'LOV-DOC-SOURCE', NULL, 'Workbench', NULL, false, 'Source of the file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-047', 'document_intake', 'source_ref', 'TEXT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'Path, partner reference or email message ID at the channel');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-048', 'document_intake', 'channel_code', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Workbench', NULL, false, 'Branch code, MAILROOM, partner code or mailbox code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-049', 'document_intake', 'file_name', 'TEXT', 'varchar(255)', false, NULL, NULL, 'Workbench', NULL, true, 'File name as received; personal where it names a customer');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-050', 'document_intake', 'file_size', 'NUMBER', 'bigint', false, NULL, NULL, 'Workbench', NULL, false, 'File size in bytes');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-051', 'document_intake', 'captured_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'Scan time recorded by the scanner, for scanner files');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-052', 'document_intake', 'sender_address', 'TEXT', 'varchar(320)', false, NULL, NULL, 'Workbench', NULL, true, 'Sender email address for mailbox items; masked by role');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-053', 'document_intake', 'partner_id', 'CROSS_REF', 'uuid', false, NULL, 'partner', 'Workbench', NULL, false, 'Partner that sent the file by SFTP');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-054', 'document_intake', 'run_id', 'CROSS_REF', 'uuid', false, NULL, 'load_run', 'Workbench', NULL, false, 'JOB-12 run that took the item in');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-055', 'document_intake', 'received_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When the Workbench received the file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-056', 'document_intake', 'file_sha256', 'TEXT', 'char(64)', true, NULL, NULL, 'Workbench', NULL, false, 'SHA-256 of the file');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-057', 'document_intake', 'intake_ref', 'ATTACHMENT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'Received file in the intake container');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-058', 'document_intake', 'scan_result', 'LOV', 'varchar(10)', false, 'LOV-SCAN-RESULT', NULL, 'Workbench', NULL, false, 'Malware scan result: clean or infected; empty until scanned');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-059', 'document_intake', 'scanned_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the malware scan ran');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-060', 'document_intake', 'case_id', 'CROSS_REF', 'uuid', false, NULL, 'recovery_case', 'Workbench', NULL, false, 'Case the item belongs to once known');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-061', 'document_intake', 'document_id', 'CROSS_REF', 'uuid', false, NULL, 'document', 'Workbench', NULL, false, 'Document created from the item, or the uploaded document');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-062', 'document_intake', 'ocr_ref', 'ATTACHMENT', 'varchar(400)', false, NULL, NULL, 'Workbench', NULL, false, 'OCR JSON output (text and layout) in the standard container');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-063', 'document_intake', 'ocr_status', 'LOV', 'varchar(12)', true, 'LOV-OCR-STATUS', NULL, 'Workbench', NULL, false, 'Pending, done, rescan or failed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-064', 'document_intake', 'ocr_attempts', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Number of OCR calls made for the item');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-065', 'document_intake', 'page_count', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Number of pages read');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-066', 'document_intake', 'rescan_pages', 'TEXT', 'varchar(200)', false, NULL, NULL, 'Workbench', NULL, false, 'Page numbers below the OCR quality threshold');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-067', 'document_intake', 'ocr_quality', 'NUMBER', 'numeric(5,4)', false, NULL, NULL, 'Workbench', NULL, false, 'Lowest page quality of the item');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-068', 'document_intake', 'languages', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Languages found, for example th,en');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-069', 'document_intake', 'ocr_engine_version', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Workbench', NULL, false, 'Version of the OCR service that read the item');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-070', 'document_intake', 'predicted_type', 'LOV', 'varchar(30)', false, 'LOV-DOC-TYPE', NULL, 'Workbench', NULL, false, 'Type with the highest classification score');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-071', 'document_intake', 'classification_confidence', 'NUMBER', 'numeric(5,4)', false, NULL, NULL, 'Workbench', NULL, false, 'Score of the predicted type');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-072', 'document_intake', 'type_candidates', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Top two types with their scores');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-073', 'document_intake', 'classifier_version', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Workbench', NULL, false, 'Model version that classified the item');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-074', 'document_intake', 'classify_fallback', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when the classifier did not answer and the item went to a person');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-075', 'document_intake', 'match_status', 'LOV', 'varchar(12)', true, 'LOV-INTAKE-MATCH', NULL, 'Workbench', NULL, false, 'Pending, matched, no match, multiple, conflict, case closed or no type');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-076', 'document_intake', 'candidate_case_ids', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Cases found for the item when more than one or none can be chosen by rule');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-077', 'document_intake', 'extracted_fields', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, true, 'Fields read before the item is attached: field name, value, extracted value, confidence, state, extractor version, personal flag');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-078', 'document_intake', 'extract_status', 'LOV', 'varchar(12)', false, 'LOV-EXTRACT-STATUS', NULL, 'Workbench', NULL, false, 'Pending, done or failed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-079', 'document_intake', 'extract_attempts', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Number of extraction attempts');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-080', 'document_intake', 'review_reason', 'LOV', 'varchar(20)', false, 'LOV-INTAKE-REVIEW', NULL, 'Workbench', NULL, false, 'Why the item needs a person: rescan, unreadable file, low confidence, model unavailable, unknown type');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-081', 'document_intake', 'review_outcome', 'LOV', 'varchar(12)', false, 'LOV-INTAKE-OUTCOME', NULL, 'Workbench', NULL, false, 'Attached or discarded once a person resolves the review item');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-082', 'document_intake', 'resolved_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Who resolved the review item');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-083', 'document_intake', 'resolved_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the review item was resolved');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-084', 'document_intake', 'discard_reason', 'TEXT', 'varchar(400)', false, NULL, NULL, 'Workbench', NULL, false, 'Reason given when a review item is discarded');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-085', 'document_text', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the page text');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-086', 'document_text', 'intake_id', 'CROSS_REF', 'uuid', true, NULL, 'document_intake', 'Workbench', NULL, false, 'Intake item the page belongs to; unique with page_no');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-087', 'document_text', 'document_id', 'CROSS_REF', 'uuid', false, NULL, 'document', 'Workbench', NULL, false, 'Document the page belongs to once attached');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-088', 'document_text', 'page_no', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Page number');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-089', 'document_text', 'text_content', 'TEXT', 'text', true, NULL, NULL, 'Workbench', NULL, true, 'OCR text of the page; masked by role on read');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-090', 'document_text', 'quality', 'NUMBER', 'numeric(5,4)', false, NULL, NULL, 'Workbench', NULL, false, 'Mean word confidence of the page');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-091', 'retention_action', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the retention action');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-092', 'retention_action', 'document_id', 'CROSS_REF', 'uuid', true, NULL, 'document', 'Workbench', NULL, false, 'Document acted on; unique with run_month');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-093', 'retention_action', 'run_month', 'TEXT', 'char(7)', true, NULL, NULL, 'Workbench', NULL, false, 'Month of the JOB-17 run, YYYY-MM');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-094', 'retention_action', 'action', 'LOV', 'varchar(12)', true, 'LOV-RETENTION-ACTION', NULL, 'Workbench', NULL, false, 'Archived, listed, held or exception');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-095', 'retention_action', 'decision_log_id', 'CROSS_REF', 'uuid', false, NULL, 'decision_log_entry', 'Workbench', NULL, false, 'DOCRET decision log entry for an archive');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-252', 'merge_field', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the merge field');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-253', 'merge_field', 'merge_code', 'TEXT', 'varchar(40)', true, NULL, NULL, 'Workbench', NULL, false, 'Code written in the template body, for example CASE_NO');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-254', 'merge_field', 'source_entity', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Entity that holds the value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-255', 'merge_field', 'source_field', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Field that holds the value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-256', 'merge_field', 'field_id', 'TEXT', 'varchar(16)', true, NULL, NULL, 'Workbench', NULL, false, 'BR Field ID of the source field in the data dictionary');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-257', 'merge_field', 'is_required', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when generation holds on an empty value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-258', 'merge_field', 'personal_data', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when the value is personal data, detokenized only at generation');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-259', 'merge_field', 'catalog_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Version of the catalog load');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-260', 'merge_field', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the catalog version comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-096', 'signature_request', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the signature request');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-097', 'signature_request', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'Case');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-098', 'signature_request', 'treatment_id', 'CROSS_REF', 'uuid', false, NULL, 'treatment', 'Workbench', NULL, false, 'Treatment the agreement belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-099', 'signature_request', 'document_id', 'CROSS_REF', 'uuid', true, NULL, 'document', 'Workbench', NULL, false, 'Generated document sent for signature');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-100', 'signature_request', 'party_id', 'CROSS_REF', 'uuid', true, NULL, 'party', 'Workbench', NULL, false, 'Signing party');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-101', 'signature_request', 'method', 'LOV', 'varchar(15)', true, 'LOV-SIGN-METHOD', NULL, 'Workbench', NULL, false, 'E-signature, branch or paper');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-102', 'signature_request', 'status', 'LOV', 'varchar(15)', true, 'LOV-SIGN-STATUS', NULL, 'Workbench', NULL, false, 'Queued, sent, signed, declined or expired');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-103', 'signature_request', 'external_ref', 'TEXT', 'varchar(60)', false, NULL, NULL, 'EasyApp', NULL, false, 'EasyApp reference');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-104', 'signature_request', 'sent_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the request was sent');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-105', 'signature_request', 'signed_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the party signed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-106', 'signature_request', 'signed_document_id', 'CROSS_REF', 'uuid', false, NULL, 'document', 'Workbench', NULL, false, 'Signed copy or branch scan');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DOC-107', 'signature_request', 'expires_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'End of the offer validity');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-032', 'approval', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the approval');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-033', 'approval', 'case_id', 'CROSS_REF', 'uuid', true, NULL, 'recovery_case', 'Workbench', NULL, false, 'The case');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-034', 'approval', 'decision_code', 'LOV', 'varchar(8)', true, 'LOV-DECISION', NULL, 'Workbench', NULL, false, 'Decision to approve');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-035', 'approval', 'regulation_item', 'TEXT', 'varchar(10)', false, NULL, NULL, 'Workbench', NULL, false, 'Delegation item, for example 2.1.1');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-036', 'approval', 'capability_area', 'LOV', 'varchar(30)', true, 'LOV-CAPABILITY', NULL, 'Workbench', NULL, false, 'Area whose A letter the approver needs');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-037', 'approval', 'route_role_code', 'LOV', 'varchar(20)', false, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role for a decision with no amount limit, for example RW-LITOFF');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-038', 'approval', 'approval_level', 'LOV', 'varchar(4)', false, 'LOV-APPROVAL-LEVEL', NULL, 'Workbench', NULL, false, 'Required level L1 to L6');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-039', 'approval', 'delegation_limit_id', 'CROSS_REF', 'uuid', false, NULL, 'delegation_limit', 'Workbench', NULL, false, 'Delegation row that covers the item');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-040', 'approval', 'limit_version', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Delegation version the item routed under');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-041', 'approval', 'product_group', 'LOV', 'varchar(15)', true, 'LOV-PRODUCT', NULL, 'Workbench', NULL, false, 'Product group');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-042', 'approval', 'amount', 'NUMBER', 'numeric(18,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Principal used for the limit, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-043', 'approval', 'terms', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Proposed and changed terms');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-044', 'approval', 'prepared_by', 'USER_REF', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Person or service identity that prepared the item');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-045', 'approval', 'assigned_user_id', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Holder the item is assigned to; empty for a role route');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-046', 'approval', 'status', 'LOV', 'varchar(20)', true, 'LOV-APPROVAL-STATUS', NULL, 'Workbench', NULL, false, 'Waiting, held with no limit, approved, refused or returned');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-047', 'approval', 'due_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the service level ends');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-048', 'approval', 'escalation_level', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Times escalated');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-049', 'approval', 'source_type', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'What asked for approval, for example NOTICE or TREATMENT');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-050', 'approval', 'source_ref', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'ID of the source record, for example the notice ID');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-051', 'approval', 'rule_id', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Rule that asked for approval');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-052', 'approval', 'rule_version', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Version of that rule');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-DEC-053', 'approval', 'decision_log_id', 'CROSS_REF', 'uuid', false, NULL, 'decision_log_entry', 'Workbench', NULL, false, 'Decision log entry of the outcome');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-261', 'payment_match_rule', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the payment match rule');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-262', 'payment_match_rule', 'rule_code', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Row code, for example EXACT');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-263', 'payment_match_rule', 'rule_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Parameter version, for example PM-2026.12');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-264', 'payment_match_rule', 'match_type', 'LOV', 'varchar(15)', true, 'LOV-MATCH-TYPE', NULL, 'Workbench', NULL, false, 'Exact, window or partial');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-265', 'payment_match_rule', 'amount_tolerance_pct', 'NUMBER', 'numeric(5,2)', true, NULL, NULL, 'Workbench', NULL, false, 'Allowed difference from the installment, 0 to 100 percent');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-266', 'payment_match_rule', 'window_days_before', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Days before the due date a payment may arrive');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-267', 'payment_match_rule', 'window_days_after', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Days after the due date a payment may arrive');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-268', 'payment_match_rule', 'grace_days', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Days after the due date before PaymentMissed is raised');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-269', 'payment_match_rule', 'partial_floor_pct', 'NUMBER', 'numeric(5,2)', false, NULL, NULL, 'Workbench', NULL, false, 'Lowest share of the installment matched as partial, percent');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-270', 'payment_match_rule', 'priority', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Order in which rows are tried');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-271', 'payment_match_rule', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the version comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-272', 'payment_match_rule', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the version is in force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-REF-273', 'payment_match_rule', 'approved_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Credit Administration approver');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-031', 'measure_definition', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the measure definition');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-032', 'measure_definition', 'measure_code', 'TEXT', 'varchar(40)', true, NULL, NULL, 'Workbench', NULL, false, 'Measure code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-033', 'measure_definition', 'name', 'TEXT', 'varchar(120)', true, NULL, NULL, 'Workbench', NULL, false, 'Measure name');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-034', 'measure_definition', 'formula', 'TEXT', 'varchar(1000)', true, NULL, NULL, 'Workbench', NULL, false, 'Formula in plain terms');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-035', 'measure_definition', 'data_product', 'LOV', 'varchar(25)', true, 'LOV-DATA-PRODUCT', NULL, 'Workbench', NULL, false, 'Data product the measure reads');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-036', 'measure_definition', 'unit', 'LOV', 'varchar(10)', true, 'LOV-MEASURE-UNIT', NULL, 'Workbench', NULL, false, 'Count, baht, days or percent');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-037', 'measure_definition', 'definition_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Definition version, for example MD-2026.11');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-038', 'measure_definition', 'approved_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Tribe lead who approved');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-039', 'measure_definition', 'approved_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'Approval time');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-040', 'measure_definition', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the definition comes into force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-041', 'measure_snapshot', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the measure snapshot');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-042', 'measure_snapshot', 'measure_code', 'TEXT', 'varchar(40)', true, NULL, NULL, 'Workbench', NULL, false, 'Measure, from measure_definition');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-043', 'measure_snapshot', 'definition_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Definition version used');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-044', 'measure_snapshot', 'business_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Business date measured');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-045', 'measure_snapshot', 'product_group', 'LOV', 'varchar(15)', false, 'LOV-PRODUCT', NULL, 'Workbench', NULL, false, 'Product group');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-046', 'measure_snapshot', 'dimension_code', 'LOV', 'varchar(20)', false, 'LOV-MEASURE-DIM', NULL, 'Workbench', NULL, false, 'Dimension: route, age band, queue, stage or agent');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-047', 'measure_snapshot', 'dimension_value', 'TEXT', 'varchar(60)', false, NULL, NULL, 'Workbench', NULL, false, 'Value of the dimension');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-048', 'measure_snapshot', 'value', 'NUMBER', 'numeric(18,4)', true, NULL, NULL, 'Workbench', NULL, false, 'Measure value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-049', 'measure_snapshot', 'case_count', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Cases behind the value');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-050', 'measure_snapshot', 'is_baseline', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True for a row of the baseline date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-051', 'measure_snapshot', 'frozen', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when the row may not change');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-052', 'measure_snapshot', 'published_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When published');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-053', 'measure_publish', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the measure publish');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-054', 'measure_publish', 'business_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Business date');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-055', 'measure_publish', 'status', 'LOV', 'varchar(10)', true, 'LOV-MEASURE-PUBLISH', NULL, 'Workbench', NULL, false, 'Published or held');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-056', 'measure_publish', 'case_list_count', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Open cases on the case list at the cut-off');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-057', 'measure_publish', 'dashboard_count', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Open cases in the dashboard facts');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-RPT-058', 'measure_publish', 'held_reason', 'TEXT', 'varchar(200)', false, NULL, NULL, 'Workbench', NULL, false, 'Why the publish is held');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-001', 'agent_policy', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the agent policy version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-002', 'agent_policy', 'agent_code', 'LOV', 'varchar(30)', true, 'LOV-AGENT', NULL, 'Workbench', NULL, false, 'Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-003', 'agent_policy', 'policy_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Policy version, for example P1');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-004', 'agent_policy', 'model_code', 'TEXT', 'varchar(40)', true, NULL, NULL, 'Workbench', NULL, false, 'Model deployment the agent calls through the gateway');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-005', 'agent_policy', 'model_version', 'TEXT', 'varchar(40)', true, NULL, NULL, 'Workbench', NULL, false, 'Model version the policy uses');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-006', 'agent_policy', 'output_schema_ref', 'TEXT', 'varchar(400)', true, NULL, NULL, 'Workbench', NULL, false, 'Reference to the JSON Schema the answer must meet');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-007', 'agent_policy', 'allowed_tools', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Tools the agent may call through the tool gateway');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-008', 'agent_policy', 'autonomy_mode', 'LOV', 'varchar(10)', true, 'LOV-AUTONOMY', NULL, 'Workbench', NULL, false, 'Off, shadow or L1');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-009', 'agent_policy', 'segment_product_group', 'LOV', 'varchar(15)', false, 'LOV-PRODUCT', NULL, 'Workbench', NULL, false, 'Product group the mode applies to; empty for all');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-010', 'agent_policy', 'segment_region_code', 'LOV', 'varchar(10)', false, 'LOV-REGION', NULL, 'Workbench', NULL, false, 'Region the mode applies to; empty for all');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-011', 'agent_policy', 'confidence_floor', 'NUMBER', 'numeric(5,4)', true, NULL, NULL, 'Workbench', NULL, false, 'Answers below this confidence fall back or are marked for review');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-012', 'agent_policy', 'timeout_seconds', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Seconds the gateway waits before the rule result is used');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-013', 'agent_policy', 'daily_cost_cap_thb', 'NUMBER', 'numeric(12,2)', true, NULL, NULL, 'Workbench', NULL, false, 'Daily model cost limit per agent, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-014', 'agent_policy', 'price_per_1k_tokens_thb', 'NUMBER', 'numeric(10,4)', true, NULL, NULL, 'Workbench', NULL, false, 'Model price per 1,000 tokens, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-015', 'agent_policy', 'alert_role', 'LOV', 'varchar(20)', true, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role that receives cost and drift alerts');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-016', 'agent_policy', 'review_date', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Date the version is reviewed again, for a parked or shadow agent');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-017', 'agent_policy', 'evaluation_run_id', 'CROSS_REF', 'uuid', false, NULL, 'agent_evaluation_run', 'Workbench', NULL, false, 'Evaluation run an autonomy step is based on');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-018', 'agent_policy', 'promotion_conditions', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Conditions the evaluation must meet for the stated mode');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-019', 'agent_policy', 'watch_measures', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Measures and limits to watch after the step, including drift points and minimum feedback');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-020', 'agent_policy', 'fallback_rule', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Rule applied when the agent does not answer, for example R-UNI-32');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-021', 'agent_policy', 'status', 'LOV', 'varchar(12)', true, 'LOV-CONFIG-STATUS', NULL, 'Workbench', NULL, false, 'Loaded, approved or retired');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-022', 'agent_policy', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the version takes effect');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-023', 'agent_policy', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the version is in force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-024', 'agent_policy', 'loaded_by', 'USER_REF', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Who loaded the version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-025', 'agent_policy', 'approved_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Who approved the version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-026', 'agent_prompt', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the agent prompt version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-027', 'agent_prompt', 'agent_code', 'LOV', 'varchar(30)', true, 'LOV-AGENT', NULL, 'Workbench', NULL, false, 'Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-028', 'agent_prompt', 'prompt_version', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'Prompt version, for example PR1');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-029', 'agent_prompt', 'body_text', 'TEXT', 'text', true, NULL, NULL, 'Workbench', NULL, false, 'Prompt text with placeholders; no personal data');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-030', 'agent_prompt', 'body_hash', 'TEXT', 'char(64)', true, NULL, NULL, 'Workbench', NULL, false, 'SHA-256 of the prompt text');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-031', 'agent_prompt', 'status', 'LOV', 'varchar(12)', true, 'LOV-CONFIG-STATUS', NULL, 'Workbench', NULL, false, 'Loaded, approved or retired');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-032', 'agent_prompt', 'valid_from', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Date the version takes effect');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-033', 'agent_prompt', 'valid_to', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Last date the version is in force');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-034', 'agent_prompt', 'loaded_by', 'USER_REF', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Who loaded the version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-035', 'agent_prompt', 'approved_by', 'USER_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Who approved the version');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-036', 'agent_run', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the agent run');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-037', 'agent_run', 'agent_code', 'LOV', 'varchar(30)', true, 'LOV-AGENT', NULL, 'Workbench', NULL, false, 'Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-038', 'agent_run', 'agent_version', 'TEXT', 'varchar(40)', true, NULL, NULL, 'Workbench', NULL, false, 'Agent, policy and prompt version as <agent>@<policy>/<prompt>');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-039', 'agent_run', 'prompt_version', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Prompt version used');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-040', 'agent_run', 'model_version', 'TEXT', 'varchar(40)', true, NULL, NULL, 'Workbench', NULL, false, 'Model version used');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-041', 'agent_run', 'case_id', 'CROSS_REF', 'uuid', false, NULL, 'recovery_case', 'Workbench', NULL, false, 'The case the run is for');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-042', 'agent_run', 'subject_id', 'CROSS_REF', 'uuid', false, NULL, NULL, 'Workbench', NULL, false, 'Document, legal action or treatment the run is about, where not the case');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-043', 'agent_run', 'autonomy_mode', 'LOV', 'varchar(10)', true, 'LOV-AUTONOMY', NULL, 'Workbench', NULL, false, 'Mode the run used: shadow or L1');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-044', 'agent_run', 'trigger_event', 'TEXT', 'varchar(30)', true, NULL, NULL, 'Workbench', NULL, false, 'CaseCreated, DocumentStored, STEP or EVALUATION');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-045', 'agent_run', 'idempotency_key', 'TEXT', 'varchar(120)', true, NULL, NULL, 'Workbench', NULL, false, 'Unique key of the run request');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-046', 'agent_run', 'status', 'LOV', 'varchar(20)', true, 'LOV-AGENT-RUN', NULL, 'Workbench', NULL, false, 'Answered, timed out, guardrail failed, below floor, tool unavailable, model error or disabled');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-047', 'agent_run', 'fallback', 'BOOLEAN', 'boolean', true, NULL, NULL, 'Workbench', NULL, false, 'True when the rule result was used instead of the answer');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-048', 'agent_run', 'guardrail_result', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Failed check codes and details');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-049', 'agent_run', 'output', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Checked answer, masked; never returned for shadow runs');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-050', 'agent_run', 'confidence', 'NUMBER', 'numeric(5,4)', false, NULL, NULL, 'Workbench', NULL, false, 'Confidence of the answer');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-051', 'agent_run', 'latency_ms', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Time from call to answer or timeout, milliseconds');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-052', 'agent_run', 'tokens_in', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Input tokens returned by the endpoint');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-053', 'agent_run', 'tokens_out', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Output tokens returned by the endpoint');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-054', 'agent_run', 'cost_thb', 'NUMBER', 'numeric(12,4)', false, NULL, NULL, 'Workbench', NULL, false, 'Cost of the run, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-055', 'agent_run', 'data_as_of', 'DATE', 'date', false, NULL, NULL, 'Workbench', NULL, false, 'Oldest business date of the inputs used');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-056', 'agent_run', 'run_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When the run started');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-057', 'agent_run', 'evaluation_run_id', 'CROSS_REF', 'uuid', false, NULL, 'agent_evaluation_run', 'Workbench', NULL, false, 'Evaluation run the run belongs to, if any');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-058', 'agent_run', 'decision_log_id', 'CROSS_REF', 'uuid', false, NULL, 'decision_log_entry', 'Workbench', NULL, false, 'Decision log entry written for the step that used the run');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-059', 'agent_run', 'segment_product_group', 'LOV', 'varchar(15)', false, 'LOV-PRODUCT', NULL, 'Workbench', NULL, false, 'Product group of the case at run time');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-060', 'agent_run', 'segment_region_code', 'LOV', 'varchar(10)', false, 'LOV-REGION', NULL, 'Workbench', NULL, false, 'Region of the case at run time');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-061', 'agent_sample', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the sample row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-062', 'agent_sample', 'agent_code', 'LOV', 'varchar(30)', true, 'LOV-AGENT', NULL, 'Workbench', NULL, false, 'Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-063', 'agent_sample', 'sample_code', 'TEXT', 'varchar(30)', true, NULL, NULL, 'Workbench', NULL, false, 'Sample code, for example INTAKE-S1');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-064', 'agent_sample', 'sample_version', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Version of the sample');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-065', 'agent_sample', 'subject_type', 'LOV', 'varchar(15)', true, 'LOV-SUBJECT-TYPE', NULL, 'Workbench', NULL, false, 'Case, document or legal action');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-066', 'agent_sample', 'subject_id', 'CROSS_REF', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'The case, document or legal action labeled');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-067', 'agent_sample', 'label_key', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Gap type, deviation code, field name or checklist item');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-068', 'agent_sample', 'expected_value', 'TEXT', 'varchar(1000)', false, NULL, NULL, 'Workbench', NULL, false, 'Labeled value; SHA-256 hash for personal values');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-069', 'agent_sample', 'labeled_by', 'USER_REF', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Who labeled the row');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-070', 'agent_evaluation_run', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the evaluation run');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-071', 'agent_evaluation_run', 'agent_code', 'LOV', 'varchar(30)', true, 'LOV-AGENT', NULL, 'Workbench', NULL, false, 'Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-072', 'agent_evaluation_run', 'sample_code', 'TEXT', 'varchar(30)', true, NULL, NULL, 'Workbench', NULL, false, 'Sample used');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-073', 'agent_evaluation_run', 'sample_version', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Sample version used');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-074', 'agent_evaluation_run', 'policy_version', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Policy version evaluated');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-075', 'agent_evaluation_run', 'prompt_version', 'TEXT', 'varchar(20)', false, NULL, NULL, 'Workbench', NULL, false, 'Prompt version evaluated');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-076', 'agent_evaluation_run', 'model_version', 'TEXT', 'varchar(40)', false, NULL, NULL, 'Workbench', NULL, false, 'Model version evaluated');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-077', 'agent_evaluation_run', 'status', 'LOV', 'varchar(12)', true, 'LOV-EVAL-STATUS', NULL, 'Workbench', NULL, false, 'Running, done or failed');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-078', 'agent_evaluation_run', 'started_at', 'DATE', 'timestamptz', true, NULL, NULL, 'Workbench', NULL, false, 'When the run started');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-079', 'agent_evaluation_run', 'finished_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the run ended');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-080', 'agent_evaluation_run', 'requested_by', 'USER_REF', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Who started the run');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-081', 'agent_evaluation_run', 'total_cost_thb', 'NUMBER', 'numeric(12,4)', false, NULL, NULL, 'Workbench', NULL, false, 'Cost of all runs in the evaluation, baht');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-082', 'agent_evaluation_run', 'p95_latency_ms', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, '95th percentile latency, milliseconds');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-083', 'agent_evaluation_run', 'failure_counts', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Count of runs by failure status and check code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-084', 'agent_evaluation_run', 'proposal', 'TEXT', 'jsonb', false, NULL, NULL, 'Workbench', NULL, false, 'Proposed approach and confidence threshold per document type');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-085', 'agent_evaluation_run', 'review_count', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'Proposals below the confidence floor, scored separately');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-086', 'agent_evaluation', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the evaluation score');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-087', 'agent_evaluation', 'evaluation_run_id', 'CROSS_REF', 'uuid', true, NULL, 'agent_evaluation_run', 'Workbench', NULL, false, 'Evaluation run the score belongs to');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-088', 'agent_evaluation', 'approach', 'LOV', 'varchar(20)', true, 'LOV-EXTRACT-APPROACH', NULL, 'Workbench', NULL, false, 'Agent, OCR template, model, or OCR and model');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-089', 'agent_evaluation', 'label_key', 'TEXT', 'varchar(60)', true, NULL, NULL, 'Workbench', NULL, false, 'Gap type, code, field or item scored');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-090', 'agent_evaluation', 'sample_size', 'NUMBER', 'integer', true, NULL, NULL, 'Workbench', NULL, false, 'Labeled subjects scored');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-091', 'agent_evaluation', 'true_positive', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'True positives');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-092', 'agent_evaluation', 'false_positive', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'False positives');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-093', 'agent_evaluation', 'false_negative', 'NUMBER', 'integer', false, NULL, NULL, 'Workbench', NULL, false, 'False negatives');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-094', 'agent_evaluation', 'agreement_rate', 'NUMBER', 'numeric(5,4)', false, NULL, NULL, 'Workbench', NULL, false, 'Share of subjects where the answer equals the label');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-095', 'agent_evaluation', 'precision_value', 'FORMULA', 'numeric(5,4)', false, NULL, NULL, 'Workbench', NULL, false, 'TP / (TP + FP)');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-096', 'agent_evaluation', 'recall_value', 'FORMULA', 'numeric(5,4)', false, NULL, NULL, 'Workbench', NULL, false, 'TP / (TP + FN)');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-097', 'agent_feedback', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the feedback');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-098', 'agent_feedback', 'agent_run_id', 'CROSS_REF', 'uuid', true, NULL, 'agent_run', 'Workbench', NULL, false, 'Agent run the feedback is on');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-099', 'agent_feedback', 'item_key', 'TEXT', 'varchar(20)', true, NULL, NULL, 'Workbench', NULL, false, 'SUMMARY for the intake summary, or the deviation code');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-100', 'agent_feedback', 'verdict', 'LOV', 'varchar(10)', true, 'LOV-FEEDBACK', NULL, 'Workbench', NULL, false, 'Accepted, corrected or rejected');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-101', 'agent_feedback', 'reason', 'TEXT', 'varchar(1000)', false, NULL, NULL, 'Workbench', NULL, false, 'Reason for a correction or a rejection');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-102', 'agent_feedback', 'decision_log_id', 'CROSS_REF', 'uuid', false, NULL, 'decision_log_entry', 'Workbench', NULL, false, 'Decision log entry written for the feedback');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-103', 'agent_alert', 'id', 'TEXT', 'uuid', true, NULL, NULL, 'Workbench', NULL, false, 'Record identifier of the alert');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-104', 'agent_alert', 'agent_code', 'LOV', 'varchar(30)', true, 'LOV-AGENT', NULL, 'Workbench', NULL, false, 'Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-105', 'agent_alert', 'alert_type', 'LOV', 'varchar(12)', true, 'LOV-AGENT-ALERT', NULL, 'Workbench', NULL, false, 'Cost cap or drift');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-106', 'agent_alert', 'segment', 'TEXT', 'varchar(30)', true, NULL, NULL, 'Workbench', NULL, false, 'Product group and region, or ALL');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-107', 'agent_alert', 'business_date', 'DATE', 'date', true, NULL, NULL, 'Workbench', NULL, false, 'Business date measured');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-108', 'agent_alert', 'measured_value', 'NUMBER', 'numeric(14,4)', true, NULL, NULL, 'Workbench', NULL, false, 'Cost in baht or acceptance rate measured');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-109', 'agent_alert', 'threshold_value', 'NUMBER', 'numeric(14,4)', true, NULL, NULL, 'Workbench', NULL, false, 'Limit the value was compared with');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-110', 'agent_alert', 'sent_to_role', 'LOV', 'varchar(20)', true, 'LOV-ROLE', NULL, 'Workbench', NULL, false, 'Role notified');
INSERT INTO sys_fields (field_id, object_name, field_name, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, description) VALUES ('DF-AGT-111', 'agent_alert', 'sent_at', 'DATE', 'timestamptz', false, NULL, NULL, 'Workbench', NULL, false, 'When the notification was sent; empty until sent');

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

-- Seed: approval levels with no limits until the delegation of authority table is signed (DL18)
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L1', 'MORTGAGE', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L1', 'HIRE_PURCHASE', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L1', 'SSME', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L1', 'UNSECURED', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L2', 'MORTGAGE', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L2', 'HIRE_PURCHASE', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L2', 'SSME', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L2', 'UNSECURED', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L3', 'MORTGAGE', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L3', 'HIRE_PURCHASE', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L3', 'SSME', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L3', 'UNSECURED', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L4', 'MORTGAGE', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L4', 'HIRE_PURCHASE', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L4', 'SSME', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L4', 'UNSECURED', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L5', 'MORTGAGE', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L5', 'HIRE_PURCHASE', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L5', 'SSME', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L5', 'UNSECURED', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L6', 'MORTGAGE', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L6', 'HIRE_PURCHASE', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L6', 'SSME', DATE '2026-11-30');
INSERT INTO delegation_limit (decision_code, approval_level, product_group, valid_from) VALUES ('ALL', 'L6', 'UNSECURED', DATE '2026-11-30');

