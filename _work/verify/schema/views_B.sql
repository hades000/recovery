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
-- Grants. The recovery service identity may read the views and nothing else.
-- Replace :recovery_role and :ace_view_owner with the names fixed in the Environment and Deployment Design.
-- ---------------------------------------------------------------------------

-- CREATE ROLE :ace_view_owner NOLOGIN;
-- CREATE ROLE :recovery_role NOLOGIN;
-- GRANT USAGE ON SCHEMA public   TO :ace_view_owner;
-- GRANT SELECT ON public.account, public.payment, public.customer, public.phone, public.email,
--      public.address, public.ca_relation, public.aa_relation, public.collateral, public.asset,
--      public.efs_action, public.efs_action_code, public.efs_assignment, public.bucket_log_snapshot,
--      public.product, public.branch, public.bot_holiday, public.ace_case,
--      public.cfsc_mg_ssme_tdr_case, public.tdr_calculation, public.ai_recommended_plan
--      TO :ace_view_owner;
-- ALTER VIEW recovery.v_ace_account OWNER TO :ace_view_owner;   -- and every other v_ace_* view
-- GRANT USAGE ON SCHEMA recovery TO :recovery_role;
-- GRANT SELECT ON ALL TABLES IN SCHEMA recovery TO :recovery_role;
-- REVOKE ALL ON ALL TABLES IN SCHEMA recovery FROM PUBLIC;
-- No INSERT, UPDATE, DELETE or TRUNCATE is granted on any table, and no SELECT on a public table
-- is granted to :recovery_role.

-- Conformance test (added to RWB-E1-069 AC4 as a repeatable check):
-- 1. Every view in recovery whose name starts with v_ace_ compiles.
-- 2. No constraint in schema recovery references a table outside schema recovery.
-- 3. select * from recovery.v_ace_account where days_past_due > 90 returns rows in SIT.
-- 4. The recovery role cannot select a public table directly, and cannot insert, update or delete
--    on any public or recovery table.
