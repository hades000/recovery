-- Recovery Workbench ACE source views
-- SCB Collections and Recovery. Henka Group, 15 November 2026. Version 1.
-- (C) Siam Commercial Bank and Henka Pte Ltd
--
-- Purpose: the only read path from the recovery module into the ACE database (D-RCV-35, U4).
-- Boundary rule: the recovery module reads ACE only through recovery.v_ace_* views. No direct
-- table read, no foreign key into a public.* table, no write.
--
-- Two migrations, because a view cannot be created over a table that does not exist yet:
--   Section A  Tier 1 views over ACE tables that exist today. Ships with RWB-E1-069 as the next
--              free sequence after the V0001 baseline (D-RCV-28).
--   Section B  Tier 2 views over the tables and columns owned by the ACE team (RWB-ACE-001).
--              Ships as a later sequence the week the ACE change lands; until then the Workbench
--              features that need them stay behind their feature flag.
--
-- Grants: SELECT only, to the recovery service identity. No INSERT, UPDATE, DELETE, TRUNCATE.
-- The views are defined with security_invoker so the caller must hold SELECT on the base table;
-- the recovery role is granted SELECT on the base tables through a dedicated ACE role, not PUBLIC.

CREATE SCHEMA IF NOT EXISTS recovery;

-- ---------------------------------------------------------------------------
-- Helper functions. Immutable, no side effects, safe in a view definition.
-- ---------------------------------------------------------------------------

-- ACE stores some dates as text. Accept ISO, YYYYMMDD and DD/MM/YYYY; return NULL on anything else
-- so a dirty source row can never break a Workbench read.
CREATE OR REPLACE FUNCTION recovery.ace_to_date(p_text text)
RETURNS date
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT CASE
        WHEN p_text IS NULL OR btrim(p_text) = '' THEN NULL
        WHEN btrim(p_text) ~ '^\d{4}-\d{2}-\d{2}$' THEN btrim(p_text)::date
        WHEN btrim(p_text) ~ '^\d{8}$' THEN to_date(btrim(p_text), 'YYYYMMDD')
        WHEN btrim(p_text) ~ '^\d{2}/\d{2}/\d{4}$' THEN to_date(btrim(p_text), 'DD/MM/YYYY')
        ELSE NULL
    END
$$;

COMMENT ON FUNCTION recovery.ace_to_date(text) IS
    'Converts an ACE text date to date. Returns NULL rather than failing on an unrecognised value.';

-- ACE holds Y/N flags as text.
CREATE OR REPLACE FUNCTION recovery.ace_to_boolean(p_text text)
RETURNS boolean
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT CASE upper(btrim(coalesce(p_text, '')))
        WHEN 'Y' THEN true
        WHEN 'YES' THEN true
        WHEN 'TRUE' THEN true
        WHEN '1' THEN true
        WHEN 'N' THEN false
        WHEN 'NO' THEN false
        WHEN 'FALSE' THEN false
        WHEN '0' THEN false
        ELSE NULL
    END
$$;

COMMENT ON FUNCTION recovery.ace_to_boolean(text) IS
    'Converts an ACE Y/N text flag to boolean. Returns NULL rather than failing.';

-- PDPA masking for display values. Keeps the last four characters.
CREATE OR REPLACE FUNCTION recovery.ace_mask_value(p_value text)
RETURNS text
LANGUAGE sql
IMMUTABLE
AS $$
    SELECT CASE
        WHEN p_value IS NULL OR btrim(p_value) = '' THEN NULL
        WHEN position('@' in p_value) > 1
            THEN left(p_value, 1) || '***' || substring(p_value from position('@' in p_value))
        WHEN length(p_value) <= 4 THEN repeat('*', length(p_value))
        ELSE repeat('*', length(p_value) - 4) || right(p_value, 4)
    END
$$;

COMMENT ON FUNCTION recovery.ace_mask_value(text) IS
    'PDPA display mask. Keeps the last four characters, or the first character and the domain of an email address.';

-- ---------------------------------------------------------------------------
-- Section A - Tier 1 views over ACE tables that exist today.
-- Proposed migration: V0002__rwb_e1_069_ace_source_views.sql (next free sequence at merge).
-- ---------------------------------------------------------------------------

-- A1. Loan account. The Workbench account row, with product, branch and the ACE batch date.
CREATE OR REPLACE VIEW recovery.v_ace_account
WITH (security_invoker = true) AS
SELECT
    a.account_key::varchar(255)                       AS account_key,
    a.account_code::varchar(255)                      AS account_code,
    a.account_name::varchar(255)                      AS account_name,
    a.account_status::varchar(255)                    AS account_status,
    a.account_status_date                             AS account_status_date,
    a.contract_number::varchar(255)                   AS contract_no,
    a.contract_date                                   AS contract_date,
    a.product_key::varchar(255)                       AS product_key,
    p.product_type::varchar(255)                      AS product_type,
    p.product_category::varchar(255)                  AS product_category,
    p.product_category_efs::varchar(255)              AS product_category_efs,
    a.current_branch::varchar(255)                    AS branch_code,
    b.branch_name::varchar(255)                       AS branch_name,
    a.oc_code::varchar(255)                           AS oc_code,
    a.company_code::varchar(255)                      AS company_code,
    a.collection_officer::varchar(255)                AS collection_officer,
    a.collection_phase::varchar(255)                  AS collection_phase,
    a.delay_days                                      AS days_past_due,
    a.loan_classification::varchar(255)               AS classification,
    a.total_balance                                   AS total_balance,
    a.accounting_balance                              AS accounting_balance,
    a.past_due_amount                                 AS past_due_amount,
    a.total_interest_fin_charge                       AS total_interest_fin_charge,
    a.collections_fee                                 AS collections_fee,
    a.interest_rate                                   AS interest_rate,
    a.last_payment_date                               AS last_payment_date,
    a.last_payment_amount                             AS last_payment_amount,
    a.next_installment_date                           AS next_installment_date,
    a.next_installment_amount                         AS next_installment_amount,
    a.last_tdr_date                                   AS last_tdr_date,
    recovery.ace_to_boolean(a.is_restructured)        AS tdr_flag,
    recovery.ace_to_boolean(a.is_rescheduled)         AS rescheduled_flag,
    a.number_reschedules                              AS number_reschedules,
    a.tdr_aging                                       AS tdr_aging,
    a.principle_not_reduce::varchar(255)              AS principle_not_reduce,
    a.core_banking_system_date                        AS data_as_of,
    a.days_since_last_contact                         AS days_since_last_contact,
    a.days_since_last_collection_activity             AS days_since_last_collection_activity,
    a.rm_name::varchar(255)                           AS relationship_manager,
    a.rm_phone_number::varchar(255)                   AS relationship_manager_phone,
    a.special_memo::varchar(255)                      AS special_memo,
    a.expiry_date                                     AS expiry_date
FROM public.account a
LEFT JOIN public.product p ON p.product_key = a.product_key
LEFT JOIN public.branch  b ON b.oc_code     = a.current_branch;

COMMENT ON VIEW recovery.v_ace_account IS
    'ACE account as the Workbench reads it. delay_days maps to days_past_due; core_banking_system_date is the data_as_of.';

-- A2. Payment. pay_date is text in ACE; the view casts it and never fails on a bad value.
CREATE OR REPLACE VIEW recovery.v_ace_payment
WITH (security_invoker = true) AS
SELECT
    p.pay_key::varchar(255)                           AS payment_code,
    p.account_key::varchar(255)                       AS account_key,
    recovery.ace_to_date(p.pay_date)                  AS payment_date,
    p.total_amount                                    AS payment_amount,
    p.capital_amount::varchar(255)                    AS capital_amount,
    p.payinterest::varchar(255)                       AS interest_amount,
    p.payexpenses::varchar(255)                       AS expense_amount,
    p.paycommission::varchar(255)                     AS commission_amount,
    p.pay_type::varchar(255)                          AS payment_channel,
    p.description::varchar(255)                       AS description,
    p.comments::varchar(255)                          AS comments,
    a.core_banking_system_date                        AS data_as_of
FROM public.payment p
LEFT JOIN public.account a ON a.account_key = p.account_key;

COMMENT ON VIEW recovery.v_ace_payment IS
    'ACE payment as the Workbench reads it. pay_date is varchar in ACE, cast to date by ace_to_date.';

-- A3. Customer. The identity number is never exposed in clear: last four only.
CREATE OR REPLACE VIEW recovery.v_ace_customer
WITH (security_invoker = true) AS
SELECT
    c.person_key::varchar(255)                        AS cif_no,
    c.person_key::varchar(255)                        AS person_key,
    c.first_name::varchar(255)                        AS first_name,
    c.surname::varchar(255)                           AS last_name,
    c.birth_date                                      AS date_of_birth,
    c.deceased_date                                   AS deceased_date,
    recovery.ace_to_boolean(c.is_deceased)            AS deceased_flag,
    c.gender::varchar(255)                            AS gender,
    c.nationality::varchar(255)                       AS nationality,
    c.marital_status::varchar(255)                    AS marital_status,
    c.occupation::varchar(255)                        AS occupation,
    c.spouse_name::varchar(255)                       AS spouse_name,
    c.status::varchar(255)                            AS customer_status,
    c.category::varchar(255)                          AS category,
    c.country_of_residence::varchar(255)              AS country_of_residence,
    recovery.ace_to_boolean(c.is_staff)               AS is_staff,
    c.branch::varchar(255)                            AS branch_code,
    c.vat_number::varchar(255)                        AS vat_number,
    recovery.ace_mask_value(c.identification_number)  AS id_no_masked,
    right(coalesce(c.identification_number, ''), 4)   AS id_no_last4
FROM public.customer c;

COMMENT ON VIEW recovery.v_ace_customer IS
    'ACE customer as the Workbench reads it. identification_number is masked in the view; the clear value is never exposed.';

-- A4. Contact points. Phone, email and address in one view, with a type and a display mask.
CREATE OR REPLACE VIEW recovery.v_ace_contact
WITH (security_invoker = true) AS
SELECT
    'PHONE'::varchar(10)                              AS contact_type,
    ph.phone_key::varchar(255)                        AS contact_key,
    ph.person_key::varchar(255)                       AS person_key,
    ph.phone_number::varchar(256)                     AS contact_value,
    recovery.ace_mask_value(ph.phone_number)          AS contact_value_masked,
    ph.contact_usage::varchar(255)                    AS usage_code,
    NULL::varchar(255)                                AS city,
    NULL::varchar(20)                                 AS post_code,
    NULL::varchar(255)                                AS country
FROM public.phone ph
UNION ALL
SELECT
    'EMAIL'::varchar(10),
    em.email_key::varchar(255),
    em.person_key::varchar(255),
    em.email::varchar(256),
    recovery.ace_mask_value(em.email),
    NULL::varchar(255),
    NULL::varchar(255),
    NULL::varchar(20),
    NULL::varchar(255)
FROM public.email em
UNION ALL
SELECT
    'ADDRESS'::varchar(10),
    ad.address_key::varchar(255),
    ad.person_key::varchar(255),
    ad.address::varchar(256),
    recovery.ace_mask_value(ad.address),
    NULL::varchar(255),
    ad.city::varchar(255),
    ad.zip_code::varchar(20),
    ad.country::varchar(255)
FROM public.address ad;

COMMENT ON VIEW recovery.v_ace_contact IS
    'ACE phone, email and address as one contact-point view. contact_value is the full value notices and calls need; contact_value_masked is for display (E1-037).';

-- A5. Customer to account relations. Borrower, guarantor, co-borrower and related roles.
CREATE OR REPLACE VIEW recovery.v_ace_ca_relation
WITH (security_invoker = true) AS
SELECT
    r.person_key::varchar(255)                        AS person_key,
    r.account_key::varchar(255)                       AS account_key,
    r.relation_type::varchar(255)                     AS relation_type,
    r.amount_of_guarantee                             AS amount_of_guarantee,
    r.date_of_guarantee                               AS date_of_guarantee
FROM public.ca_relation r;

COMMENT ON VIEW recovery.v_ace_ca_relation IS
    'ACE customer-account relation: who is borrower, guarantor or co-borrower on which account.';

-- A6. Account to account relations. Parent and child accounts for grouped facilities.
CREATE OR REPLACE VIEW recovery.v_ace_aa_relation
WITH (security_invoker = true) AS
SELECT
    r.parent_account_key::varchar(255)                AS parent_account_key,
    r.child_account_key::varchar(255)                 AS child_account_key
FROM public.aa_relation r;

COMMENT ON VIEW recovery.v_ace_aa_relation IS
    'ACE account-account relation, used to group a facility with its sub-accounts.';

-- A7. Collateral. The ACE collateral link with the asset it points at.
CREATE OR REPLACE VIEW recovery.v_ace_collateral
WITH (security_invoker = true) AS
SELECT
    col.asset_key::varchar(255)                       AS collateral_no,
    col.asset_key::varchar(255)                       AS asset_key,
    col.account_key::varchar(255)                     AS account_key,
    col.collateral_value                              AS collateral_value,
    col.register_date                                 AS register_date,
    col.in_active                                     AS in_active,
    ast.asset_type::varchar(255)                      AS collateral_type,
    ast.description::varchar(1000)                    AS description
FROM public.collateral col
LEFT JOIN public.asset ast ON ast.asset_key = col.asset_key;

COMMENT ON VIEW recovery.v_ace_collateral IS
    'ACE collateral and the asset behind it. One row per account-collateral-asset link.';

-- A8. Asset. The collateral asset record.
CREATE OR REPLACE VIEW recovery.v_ace_asset
WITH (security_invoker = true) AS
SELECT
    ast.asset_key::varchar(255)                       AS asset_ref,
    ast.asset_key::varchar(255)                       AS asset_key,
    ast.asset_type::varchar(255)                      AS asset_type,
    ast.description::varchar(1000)                    AS description,
    ast.address::varchar(255)                         AS address,
    ast.town::varchar(255)                            AS town,
    ast.zipcode::varchar(255)                         AS post_code,
    ast.county::varchar(255)                          AS county,
    ast.country::varchar(255)                         AS country
FROM public.asset ast;

COMMENT ON VIEW recovery.v_ace_asset IS
    'ACE asset as the Workbench reads it, for collateral and for a held asset.';

-- A9. Collections activity. The EFS action log ACE already ingests.
CREATE OR REPLACE VIEW recovery.v_ace_efs_action
WITH (security_invoker = true) AS
SELECT
    e.action_id::varchar(255)                         AS efs_record_key,
    e.account_key::varchar(255)                       AS account_key,
    e.customer_key::varchar(255)                      AS person_key,
    e.action_code::varchar(255)                       AS action_code,
    e.action_code_name::varchar(255)                  AS action_code_name,
    e.action_date                                     AS action_date,
    e.action_timestamp                                AS contact_at,
    e.user_code::varchar(255)                         AS user_code,
    e.comments::varchar(2000)                         AS comments,
    e.is_call                                         AS is_call,
    e.is_rpc                                          AS is_rpc,
    e.is_ptp                                          AS is_ptp,
    e.promise_status::varchar(100)                    AS promise_status,
    e.promise_eval_status::varchar(100)               AS promise_eval_status,
    e.settlement_due_date                             AS promise_date,
    e.settle_total_amount                             AS promise_amount,
    e.collection_phase::varchar(100)                  AS collection_phase,
    e.act_date_bucket                                 AS act_date_bucket,
    e.act_date_past_due_days                          AS act_date_past_due_days,
    e.last_tdr_date                                   AS last_tdr_date
FROM public.efs_action e;

COMMENT ON VIEW recovery.v_ace_efs_action IS
    'ACE EFS action log. Replaces the collections_history copy; action_timestamp maps to contact_at.';

-- A10. Action code reference. The list of values behind the collections action code.
CREATE OR REPLACE VIEW recovery.v_ace_efs_action_code
WITH (security_invoker = true) AS
SELECT
    c.action_code::varchar(255)                       AS action_code,
    c.description::varchar(255)                       AS action_name,
    c.category::varchar(100)                          AS category
FROM public.efs_action_code c;

COMMENT ON VIEW recovery.v_ace_efs_action_code IS
    'ACE EFS action code reference. The loaded LIST-ACTION-CODE list (1,106 values) reads this.';

-- A11. Assignment history. Which officer or agency held the account, and when.
CREATE OR REPLACE VIEW recovery.v_ace_efs_assignment
WITH (security_invoker = true) AS
SELECT
    s.account_key::varchar(255)                       AS account_key,
    s.assignment_scheme::varchar(255)                 AS assignment_scheme,
    s.assignee_code::varchar(255)                     AS assignee_code,
    s.assignee_name::varchar(255)                     AS assignee_name,
    s.assignment_start_date                           AS assignment_start_date,
    s.assignment_end_date                             AS assignment_end_date,
    s.assignment_start_total_balance                  AS assignment_start_total_balance,
    s.assignment_end_total_balance                    AS assignment_end_total_balance,
    s.distribution_area::varchar(255)                 AS distribution_area
FROM public.efs_assignment s;

COMMENT ON VIEW recovery.v_ace_efs_assignment IS
    'ACE assignment history, used for hand-over and agency performance.';

-- A12. Monthly bucket history. The daily bucket is an ACE-new column (RWB-ACE-001).
CREATE OR REPLACE VIEW recovery.v_ace_bucket_log
WITH (security_invoker = true) AS
SELECT
    a.account_key::varchar(255)                       AS account_key,
    b.snapshot_year                                   AS snapshot_year,
    b.snapshot_month                                  AS snapshot_month,
    b.bucket                                          AS bucket,
    b.past_due_amount                                 AS past_due_amount,
    make_date(b.snapshot_year, b.snapshot_month, 1)   AS snapshot_month_start
FROM public.bucket_log_snapshot b
JOIN public.account a ON a.id = b.account_id;

COMMENT ON VIEW recovery.v_ace_bucket_log IS
    'ACE monthly bucket snapshot, keyed by account_key. bucket is the month-end bucket, not the daily bucket.';

-- A13. Product reference.
CREATE OR REPLACE VIEW recovery.v_ace_product
WITH (security_invoker = true) AS
SELECT
    p.product_key::varchar(255)                       AS product_code,
    p.description::varchar(255)                       AS product_name,
    p.product_type::varchar(255)                      AS product_type,
    p.product_category::varchar(255)                  AS product_category,
    p.product_category_efs::varchar(255)              AS product_category_efs
FROM public.product p;

COMMENT ON VIEW recovery.v_ace_product IS
    'ACE product reference, used for the product and product group lists of values.';

-- A14. Branch reference.
CREATE OR REPLACE VIEW recovery.v_ace_branch
WITH (security_invoker = true) AS
SELECT
    br.oc_code::varchar(255)                          AS branch_code,
    br.branch_name::varchar(255)                      AS branch_name,
    br.address::varchar(255)                          AS address,
    br.phone::varchar(255)                            AS phone
FROM public.branch br;

COMMENT ON VIEW recovery.v_ace_branch IS
    'ACE branch reference, used for the branch and region lists of values.';

-- A15. Bank of Thailand holidays. Replaces the Workbench HOLIDAY reference list.
CREATE OR REPLACE VIEW recovery.v_ace_holiday
WITH (security_invoker = true) AS
SELECT
    h.holiday_date                                    AS holiday_date,
    h.holiday_year                                    AS holiday_year,
    h.holiday_description::varchar(255)               AS holiday_name,
    h.holiday_description_thai::varchar(255)          AS holiday_name_thai,
    h.holiday_weekday::varchar(20)                    AS holiday_weekday
FROM public.bot_holiday h;

COMMENT ON VIEW recovery.v_ace_holiday IS
    'ACE Bank of Thailand holiday calendar. E1-043 and E1-045 read this instead of a Workbench list.';

-- A16. Restructure plan. The ACE case plus its TDR calculation and recommended plan.
CREATE OR REPLACE VIEW recovery.v_ace_plan
WITH (security_invoker = true) AS
SELECT
    ac.case_business_id::varchar(255)                 AS plan_ref,
    ac.id                                             AS ace_case_id,
    ac.current_station_name::varchar(255)             AS plan_status,
    ac.created_timestamp                              AS plan_created_at,
    tc.id                                             AS tdr_calculation_id,
    tc.published_timestamp                            AS plan_published_at,
    tdr.associated_account_id                         AS associated_account_id,
    acc.account_key::varchar(255)                     AS account_key,
    tdr.plan_setup_completed_timestamp                AS booked_at,
    tdr.approval_completed_timestamp                  AS approved_at,
    tdr.submitted_for_approval_timestamp              AS submitted_at,
    tdr.closed_timestamp                              AS closed_at,
    tdr.closed_reason::varchar(255)                   AS closed_reason,
    tdr.ca_approved_timestamp                         AS ca_approved_at,
    rec.months                                       AS installments,
    rec.installment                                  AS recommended_installment,
    rec.package_type::varchar(255)                    AS recommended_package,
    coalesce(tdr.approval_completed_timestamp, tdr.submitted_for_approval_timestamp, ac.created_timestamp)
                                                      AS plan_status_as_of
FROM public.ace_case ac
LEFT JOIN public.cfsc_mg_ssme_tdr_case tdr ON tdr.id = ac.id
LEFT JOIN public.account acc ON acc.id = tdr.associated_account_id
LEFT JOIN public.tdr_calculation tc ON tc.case_id = tdr.id
LEFT JOIN LATERAL (
    SELECT r.months, r.installment, r.package_type
    FROM public.ai_recommended_plan r
    WHERE r.case_id = tdr.id
    ORDER BY r.rank
    LIMIT 1
) rec ON true;

COMMENT ON VIEW recovery.v_ace_plan IS
    'ACE restructure case, its TDR calculation and the top-ranked recommended plan. Replaces the plan fields the Workbench used to copy.';

-- ---------------------------------------------------------------------------
