-- Recovery Workbench ACE source views
-- SCB Collections and Recovery. Henka Group, 27 November 2026. Version 2.
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
-- Grants: SELECT only, and only on the views. The views are owned by a dedicated ACE role
-- (ace_view_owner) that holds SELECT on the ACE tables. The recovery service identity holds SELECT
-- on recovery.v_ace_* and on nothing else, so a direct read of a public table fails at the database,
-- not only in code review. This is the boundary rule, enforced by the catalog.
-- Trade-off recorded for the security review: a view owned by a definer role runs with that role's
-- privileges, so any row-level security ACE adds later must be applied inside the view.

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
AS
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
    a.interest_rate::numeric(7,4)                     AS interest_rate,
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
AS
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
AS
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
AS
SELECT
    'PHONE'::varchar(10)                              AS contact_type,
    ('PHONE:' || ph.phone_key)::varchar(255)          AS contact_key,
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
    ('EMAIL:' || em.email_key)::varchar(255),
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
    ('ADDRESS:' || ad.address_key)::varchar(255),
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
AS
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
AS
SELECT
    r.parent_account_key::varchar(255)                AS parent_account_key,
    r.child_account_key::varchar(255)                 AS child_account_key
FROM public.aa_relation r;

COMMENT ON VIEW recovery.v_ace_aa_relation IS
    'ACE account-account relation, used to group a facility with its sub-accounts.';

-- A7. Collateral. The ACE collateral link with the asset it points at.
CREATE OR REPLACE VIEW recovery.v_ace_collateral
AS
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
AS
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
AS
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
AS
SELECT
    c.action_code::varchar(255)                       AS action_code,
    c.description::varchar(255)                       AS action_name,
    c.category::varchar(100)                          AS category
FROM public.efs_action_code c;

COMMENT ON VIEW recovery.v_ace_efs_action_code IS
    'ACE EFS action code reference. The loaded LIST-ACTION-CODE list (1,106 values) reads this.';

-- A11. Assignment history. Which officer or agency held the account, and when.
CREATE OR REPLACE VIEW recovery.v_ace_efs_assignment
AS
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
AS
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
AS
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
AS
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
AS
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
AS
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
-- Section B - Tier 2 views. These depend on RWB-ACE-001 and are applied only when the ACE
-- change is live. Until then the dependent Workbench features stay behind their flags.
-- Proposed migration: the next free sequence after RWB-ACE-001 is deployed.
-- ---------------------------------------------------------------------------

-- B1. Batch completion and business date per source. The Workbench freshness stamp reads this.
CREATE OR REPLACE VIEW recovery.v_ace_batch_status
AS
SELECT
    r.source_system::varchar(20)                      AS source_system,
    r.business_date                                   AS business_date,
    r.started_at                                      AS started_at,
    r.completed_at                                    AS completed_at,
    r.status::varchar(12)                             AS status,
    r.record_count                                    AS record_count,
    r.checksum::varchar(64)                           AS checksum,
    r.feed_version::varchar(20)                       AS feed_version,
    (r.status = 'COMPLETED')                          AS is_complete
FROM public.ace_batch_run r;

COMMENT ON VIEW recovery.v_ace_batch_status IS
    'Per-source ACE batch completion and business date. The Workbench freshness stamp (E1-015) reads this.';

-- B2. Valuation. SVAF appraisals, held in ACE after RWB-ACE-001.
CREATE OR REPLACE VIEW recovery.v_ace_valuation
AS
SELECT
    v.valuation_key::varchar(255)                     AS valuation_key,
    v.asset_key::varchar(255)                         AS asset_key,
    v.appraisal_no::varchar(20)                       AS appraisal_no,
    v.appraisal_type::varchar(15)                     AS appraisal_type,
    v.appraised_value                                 AS appraised_value,
    v.forced_sale_value                               AS forced_sale_value,
    v.appraisal_date                                  AS appraisal_date,
    v.source_system::varchar(20)                      AS source_system,
    v.business_date                                   AS data_as_of
FROM public.valuation v;

COMMENT ON VIEW recovery.v_ace_valuation IS
    'SVAF appraisal as ingested into ACE. Accepted, stale and valuer fields stay in recovery.valuation_ext.';

-- B3. Collateral detail from CCMS.
CREATE OR REPLACE VIEW recovery.v_ace_collateral_detail
AS
SELECT
    d.asset_key::varchar(255)                         AS asset_key,
    d.title_doc_no::varchar(40)                       AS title_doc_no,
    d.plot_no::varchar(20)                            AS plot_no,
    d.area_text::varchar(20)                          AS area_text,
    d.province::varchar(40)                           AS province,
    d.district::varchar(60)                           AS district,
    d.subdistrict::varchar(60)                        AS subdistrict,
    d.insured_value                                   AS insured_value,
    d.insurance_expiry                                AS insurance_expiry,
    d.lien_rank                                       AS lien_rank,
    d.source_system::varchar(20)                      AS source_system,
    d.business_date                                   AS data_as_of
FROM public.collateral_detail d;

COMMENT ON VIEW recovery.v_ace_collateral_detail IS
    'CCMS collateral detail as ingested into ACE: title deed, plot, area, location, insurance and lien rank.';

-- B4. NPA asset from AMIS and RPS.
CREATE OR REPLACE VIEW recovery.v_ace_npa_asset
AS
SELECT
    n.asset_key::varchar(255)                         AS asset_ref,
    n.asset_key::varchar(255)                         AS asset_key,
    n.asset_code::varchar(20)                         AS asset_code,
    n.transfer_in_type::varchar(20)                   AS transfer_in_type,
    n.from_segment::varchar(20)                       AS from_segment,
    n.transfer_in_date                                AS transfer_in_date,
    n.book_value                                      AS book_value,
    n.auction_purchase_price                          AS auction_purchase_price,
    n.repossessed_date                                AS repossessed_date,
    n.stock_date                                      AS stock_date,
    n.source_system::varchar(20)                      AS source_system,
    n.business_date                                   AS data_as_of
FROM public.npa_asset n;

COMMENT ON VIEW recovery.v_ace_npa_asset IS
    'NPA asset from AMIS (property) and RPS (vehicles), as ingested into ACE.';

-- B5. NPA asset sale from AMIS.
CREATE OR REPLACE VIEW recovery.v_ace_npa_sale
AS
SELECT
    s.npa_sale_key::varchar(255)                      AS npa_sale_key,
    s.npa_asset_key::varchar(255)                     AS npa_asset_key,
    s.contract_date                                   AS contract_date,
    s.sale_date                                       AS sale_date,
    s.sale_price                                      AS sale_price,
    s.transfer_fee                                    AS transfer_fee,
    s.specific_business_tax                           AS specific_business_tax,
    s.corporate_income_tax                            AS corporate_income_tax,
    s.incentive_amount                                AS incentive_amount,
    s.source_system::varchar(20)                      AS source_system,
    s.business_date                                   AS data_as_of
FROM public.npa_sale s;

COMMENT ON VIEW recovery.v_ace_npa_sale IS
    'NPA sale contract and its taxes and fees, from AMIS, as ingested into ACE.';

-- B6. Lawsuit from LIT.
CREATE OR REPLACE VIEW recovery.v_ace_lawsuit
AS
SELECT
    l.lawsuit_key::varchar(255)                       AS lawsuit_key,
    l.account_key::varchar(255)                       AS account_key,
    l.lawsuit_no::varchar(30)                         AS lawsuit_no,
    l.black_case_no::varchar(30)                      AS black_case_no,
    l.red_case_no::varchar(30)                        AS red_case_no,
    l.court_name::varchar(120)                        AS court_name,
    l.claim_amount                                    AS claim_amount,
    l.filed_date                                      AS filed_date,
    l.judgment_date                                   AS judgment_date,
    l.judgment_amount                                 AS judgment_amount,
    l.lit_status::varchar(200)                        AS lit_status,
    l.source_system::varchar(20)                      AS source_system,
    l.business_date                                   AS data_as_of
FROM public.lawsuit l;

COMMENT ON VIEW recovery.v_ace_lawsuit IS
    'LIT lawsuit as ingested into ACE: case numbers, court, claim, judgment and status.';

-- B7. Hearing from LIT.
CREATE OR REPLACE VIEW recovery.v_ace_hearing
AS
SELECT
    h.hearing_key::varchar(255)                       AS hearing_key,
    h.lawsuit_key::varchar(255)                       AS lawsuit_key,
    h.hearing_date                                    AS hearing_date,
    h.hearing_type::varchar(20)                       AS hearing_type,
    h.next_date                                       AS next_date,
    h.source_system::varchar(20)                      AS source_system,
    h.business_date                                   AS data_as_of
FROM public.hearing h;

COMMENT ON VIEW recovery.v_ace_hearing IS
    'LIT court hearing as ingested into ACE.';

-- B8. Proof of delivery from WIN.
CREATE OR REPLACE VIEW recovery.v_ace_pod
AS
SELECT
    w.pod_key::varchar(255)                           AS pod_key,
    w.account_key::varchar(255)                       AS account_key,
    w.notice_ref::varchar(60)                         AS notice_ref,
    w.sent_date                                       AS sent_date,
    w.barcode::varchar(40)                            AS barcode,
    w.callback_date                                   AS callback_date,
    w.delivery_status::varchar(15)                    AS delivery_status,
    w.sent_type::varchar(10)                          AS sent_type,
    w.source_system::varchar(20)                      AS source_system,
    w.business_date                                   AS data_as_of
FROM public.pod_receipt w;

COMMENT ON VIEW recovery.v_ace_pod IS
    'WIN proof of delivery as ingested into ACE. The notice itself stays in recovery.notice.';

-- B9. Write-off from GL.
CREATE OR REPLACE VIEW recovery.v_ace_write_off
AS
SELECT
    g.write_off_key::varchar(255)                     AS write_off_key,
    g.account_key::varchar(255)                       AS account_key,
    g.amount                                          AS amount,
    g.posted_date                                     AS posted_date,
    g.responsibility_center::varchar(10)              AS responsibility_center,
    g.cost_center::varchar(10)                        AS cost_center,
    g.gl_product::varchar(10)                         AS gl_product,
    g.source_system::varchar(20)                      AS source_system,
    g.business_date                                   AS data_as_of
FROM public.gl_write_off g;

COMMENT ON VIEW recovery.v_ace_write_off IS
    'GL write-off posting as ingested into ACE. The write-off decision stays in recovery.write_off.';

-- B10. COLLINS score.
CREATE OR REPLACE VIEW recovery.v_ace_score
AS
SELECT
    s.score_key::varchar(255)                         AS score_key,
    s.account_key::varchar(255)                       AS account_key,
    s.model_code::varchar(30)                         AS model_code,
    s.model_version::varchar(20)                      AS model_version,
    s.score_value                                     AS score_value,
    s.estimate_value                                  AS estimate_value,
    s.route_code::varchar(4)                          AS route_code,
    s.scored_at                                       AS scored_at,
    s.source_system::varchar(20)                      AS source_system,
    s.business_date                                   AS data_as_of
FROM public.collins_score s;

COMMENT ON VIEW recovery.v_ace_score IS
    'COLLINS score and route estimate as ingested into ACE, if ACE does not already hold it.';

-- B11. Party product from SCBPDM.
CREATE OR REPLACE VIEW recovery.v_ace_party_product
AS
SELECT
    pp.person_key::varchar(255)                       AS person_key,
    pp.account_key::varchar(255)                      AS account_no,
    pp.account_key::varchar(255)                      AS account_key,
    pp.product_type::varchar(20)                      AS product_type,
    pp.product_status::varchar(15)                    AS product_status,
    pp.business_date                                  AS data_as_of
FROM public.party_product pp;

COMMENT ON VIEW recovery.v_ace_party_product IS
    'SCBPDM customer product holding as ingested into ACE. Replaces the Workbench party_product copy.';

-- B12. NLEADS credit decision.
CREATE OR REPLACE VIEW recovery.v_ace_credit_decision
AS
SELECT
    d.credit_decision_key::varchar(255)               AS credit_decision_key,
    d.account_key::varchar(255)                       AS account_key,
    d.nleads_ref::varchar(30)                         AS nleads_ref,
    d.credit_result::varchar(10)                      AS credit_result,
    d.credit_result_reason::varchar(1000)             AS credit_result_reason,
    d.decided_at                                      AS decided_at,
    d.source_system::varchar(20)                      AS source_system,
    d.business_date                                   AS data_as_of
FROM public.credit_decision d;

COMMENT ON VIEW recovery.v_ace_credit_decision IS
    'NLEADS credit approval as ingested into ACE. Replaces the four credit fields the Workbench used to record by hand.';

-- B13. EasyApp signature request.
CREATE OR REPLACE VIEW recovery.v_ace_esign
AS
SELECT
    s.esign_key::varchar(255)                         AS esign_key,
    s.account_key::varchar(255)                       AS account_key,
    s.external_ref::varchar(60)                       AS external_ref,
    s.requested_at                                    AS requested_at,
    s.status::varchar(20)                             AS status,
    s.source_system::varchar(20)                      AS source_system,
    s.business_date                                   AS data_as_of
FROM public.esign_request s;

COMMENT ON VIEW recovery.v_ace_esign IS
    'EasyApp signature request as ingested into ACE. The Workbench document still owns the signed file.';

-- B14. Entra ID group to role mapping.
CREATE OR REPLACE VIEW recovery.v_ace_iam_group
AS
SELECT
    g.entra_group::varchar(120)                       AS entra_group,
    g.role_code::varchar(20)                          AS role_code,
    g.source_system::varchar(20)                      AS source_system,
    g.business_date                                   AS data_as_of
FROM public.iam_group g;

COMMENT ON VIEW recovery.v_ace_iam_group IS
    'Entra ID group to Workbench role mapping as ingested into ACE. ACE performs the sign-in, so it owns the mapping.';

-- ---------------------------------------------------------------------------
-- Grants. Only the rwb_source_data database login may read the views and nothing else.
-- Replace :rwb_source_data_login and :ace_view_owner with the names fixed in the Environment and Deployment Design.
-- ---------------------------------------------------------------------------

-- CREATE ROLE :ace_view_owner NOLOGIN;
-- CREATE ROLE :rwb_source_data_login NOLOGIN;
-- GRANT USAGE ON SCHEMA public   TO :ace_view_owner;
-- GRANT SELECT ON public.account, public.payment, public.customer, public.phone, public.email,
--      public.address, public.ca_relation, public.aa_relation, public.collateral, public.asset,
--      public.efs_action, public.efs_action_code, public.efs_assignment, public.bucket_log_snapshot,
--      public.product, public.branch, public.bot_holiday, public.ace_case,
--      public.cfsc_mg_ssme_tdr_case, public.tdr_calculation, public.ai_recommended_plan
--      TO :ace_view_owner;
-- ALTER VIEW recovery.v_ace_account OWNER TO :ace_view_owner;   -- and every other v_ace_* view
-- GRANT USAGE ON SCHEMA recovery TO :rwb_source_data_login;
-- GRANT SELECT ON recovery.v_ace_account, recovery.v_ace_payment, recovery.v_ace_customer, recovery.v_ace_contact, recovery.v_ace_ca_relation, recovery.v_ace_aa_relation, recovery.v_ace_collateral, recovery.v_ace_asset, recovery.v_ace_efs_action, recovery.v_ace_efs_action_code, recovery.v_ace_efs_assignment, recovery.v_ace_bucket_log, recovery.v_ace_product, recovery.v_ace_branch, recovery.v_ace_holiday, recovery.v_ace_plan, recovery.v_ace_batch_status, recovery.v_ace_valuation, recovery.v_ace_collateral_detail, recovery.v_ace_npa_asset, recovery.v_ace_npa_sale, recovery.v_ace_lawsuit, recovery.v_ace_hearing, recovery.v_ace_pod, recovery.v_ace_write_off, recovery.v_ace_score, recovery.v_ace_party_product, recovery.v_ace_credit_decision, recovery.v_ace_esign, recovery.v_ace_iam_group TO :rwb_source_data_login;
-- REVOKE ALL ON ALL TABLES IN SCHEMA recovery FROM PUBLIC;
-- No INSERT, UPDATE, DELETE or TRUNCATE is granted on any table, and no SELECT on a public table
-- is granted to :rwb_source_data_login.

-- Conformance test (added to RWB-E1-069 AC4 as a repeatable check):
-- 1. Every view in recovery whose name starts with v_ace_ compiles.
-- 2. No constraint in schema recovery references a table outside schema recovery.
-- 3. select * from recovery.v_ace_account where days_past_due > 90 returns rows in SIT.
-- 4. The recovery role cannot select a public table directly, and cannot insert, update or delete
--    on any public or recovery table.


-- P1 developer-readiness amendment, 27 November 2026 (D-RCV-60 P1 developer readiness; RD-P1 register)

-- RD-P1-060: rwb-source-data serves the customer, account and collateral entity contracts.
-- Only rwb_source_data selects these views. Consumers use the REST contract.
-- API-layer FieldMasker applies personal-field rules; notice/file rule rows are Pending
-- under NEW-GAP-D1, owner data protection officer with the rwb-access owner.
-- RD-P1-067: the service gate on GET /efs-history checks DP01 and DP05.
-- RWB-P1-E1069-DB owns the schema USAGE, ACE view-owner SELECT and P1 SELECT grants.
-- Only the rwb_source_data database login reads recovery.v_ace_*; other service logins have no
-- grant on schema recovery or ACE public tables and obtain ACE data from the P1 service contract.
-- Section B is deployed only after the ACE dependency gate; when its feature flag is off, P1 does
-- not write a freshness stamp, publish an event or start a child workflow.
-- The SQL view shapes follow the ACE Field Gap List: ace_batch_run has nine columns without
-- loaded_at; party_product has seven columns without source_system. Do not invent these columns.
-- v_ace_account exposes current rows and maps account.core_banking_system_date to data_as_of. Matching the
-- view date to the latest COMPLETED ALS businessDate and handling null, mismatched, past or future dates
-- remain Pending (owner Data architect; NEW-GAP-W8-004).
-- The v_ace_ca_relation input set and exact orphan-detection query remain Pending (owner Data architect;
-- NEW-GAP-W8-003); the view has no business_date. Null handling for TDR and settlement fields remains
-- Pending (owner Data architect; NEW-GAP-W8-005).

-- Grant-principal allow-list: ace_view_owner, rwb_source_data, rwb_sandbox_read (DEV only), and migrator.
-- Production runtime ACE reads remain limited to rwb_source_data; the named DEV-only sandbox is
-- excluded from the production single-reader assertion in the RWB-P1-E1069-DB conformance check.
