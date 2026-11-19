# Wave 3 edit log: Epic 2 user stories v6 (ACE re-base)

Agent: Wave 3 writer (ACE re-base). Date: 15 November 2026.
Inputs read: D-RCV-35 and ADR-010 (change register v1, tier map v1, field gap list v1, source views v1), Physical Schema v5, LDM and Data Dictionary v7, TSD pack v4 (P1, P2, P8), Data Quality and Reconciliation Rules v3, Epic 2 user stories v5 (.md and .xlsx).

## 1. Files written

| File | Change |
|---|---|
| `04 User stories\Recovery Workbench User Stories Epic 2 v5.md` | Superseded; left in place |
| `04 User stories\Recovery Workbench User Stories Epic 2 v6.md` | New. 34 stories, 352 acceptance criteria, 406 test cases, 11,207 lines, ASCII |
| `04 User stories\Recovery Workbench User Stories Epic 2 v5.xlsx` | Superseded; left in place |
| `04 User stories\Recovery Workbench User Stories Epic 2 v6.xlsx` | New. 34 Stories rows, 34 Gherkin rows, 406 test rows, 85 traceability rows, 98 dependency rows |

## 2. Story removed

| Story | Disposition |
|---|---|
| RWB-E2-023 Automated EFS file load | Removed. D-RCV-35 U1: ACE ingestion owns the EFS load, so the Workbench no longer automates, reconciles or retires an inbound EFS file. 8 acceptance criteria and 9 test cases withdrawn. The later home of the automated file load is the ACE team backlog (RWB-ACE-001). The summary table carries a Removed note; the workbook subtitle repeats it. The two stories that relied on the manual EFS path (E2-001, E2-034) now read `v_ace_efs_action`. |

Counts after removal: stories 35 to 34; acceptance criteria 360 to 352; test cases 415 to 406; module P2 10 to 9; traceability 87 to 85 rows; dependencies 100 to 98 rows.

## 3. Stories rewritten around the read path

| Story | What changed |
|---|---|
| RWB-E2-001 EFS hand-over with full history | Title drops "from the COLLINS load". Case creation runs on AceDataReady (EV-26) from the ACE batch record; candidates from `v_ace_account`, person keys from `v_ace_customer`, history from `v_ace_efs_action`. No load, no JOB-01, no SY-DATALOAD. Late-batch hold reads the `data_product_load` stamps. Missing person key becomes a REC-05 business-key break. History entries keyed on `efs_record_key` so the daily read of E2-034 cannot double-write. Depends on RWB-E1-069, RWB-E1-015, RWB-E1-007. |
| RWB-E2-003 Customer's other products on the case | Products read from `v_ace_party_product` by `person_key`, excluding `account_key` already on the case; masking on `account_no`; stale marker on `data_as_of`. `CustomerProfileQuery` replaced by the P2 `CustomerProductsReader` over the view (API-P2-011). No P1 copy table; V0003 gate named. Depends on RWB-E1-069, RWB-E1-007. |
| RWB-E2-007 Booking confirmation from the ALS load | Match runs on AceDataReady for ALS when the ACE batch is COMPLETE; booking facts read from `v_ace_account` (`tdr_flag`, `last_tdr_date`, `interest_rate`, `principal_outstanding`, `settlement_booked_date`, `settlement_booked_amount`) and the batch from `v_ace_batch_status`. No load, no JOB-01. REC-03 result written to `reconciliation_result`. Section B columns flagged. Depends on RWB-E2-004, RWB-E1-069, RWB-E1-007. |
| RWB-E2-008 Payment matching with the missed payment event | Payments read from `v_ace_payment` by `payment_code` and `account_key`; proceeds link is `payment_code` (was `account_payment_id`); missed-payment detection uses the ACE batch business date; unmatched account becomes a REC-05 break; REC-04 written to `reconciliation_result`. No load, no JOB-01. Depends on RWB-E2-004, RWB-E1-069. |
| RWB-E2-010 Stage 2 data products | DP04 built from the Workbench treatment and guarantee claim; contract number and date read from `v_ace_account`, plan terms from `v_ace_plan` at read time. No copy of contract, plan or account data; `dp_treatment.contract_no` and `contract_date` dropped. Stage 2 step moves from JOB-01 to JOB-02 after case creation. Depends on RWB-E2-004, RWB-E1-069, RWB-E1-016, RWB-E1-015. |
| RWB-E2-034 Interaction ledger on the case and from every channel | EFS contact outcomes read from `v_ace_efs_action` on AceDataReady for EFS; contact keys resolved in `v_ace_contact`; no import step, no `load_run`, no SY-DATALOAD. AceDataReady replaces LoadCompleted in the consumed-event list. AC7 restructured to one When. Depends on RWB-E1-069 in place of RWB-E1-004. |

## 4. Minor edits

20 of the remaining 28 stories changed; 8 are unchanged in substance (their workbook Entities cell was regenerated from the same Data table and came out identical).

| Group | Stories | Edit |
|---|---|---|
| Data-table re-key to the views | E2-002, 006, 014, 018, 019, 021, 022, 026, 027, 029, 032 | `loan_account` to `v_ace_account` (DF-ACE-001/002/008/018/020/025/028/030/031/036), `account_payment` to `v_ace_payment` (DF-ACE-043/044/045/046), `party` to `v_ace_customer` (DF-ACE-056/057/058), `contact_point` to `v_ace_contact` (DF-ACE-075/076/077/078) and `contact_point_ext` (DF-EXT-015/017/018), `collateral` to `v_ace_collateral` and `v_ace_collateral_detail` (DF-ACE-091/097/197), `valuation` to `v_ace_valuation` (DF-ACE-191/193), `role.entra_group` to `v_ace_iam_group` (DF-ACE-301). Case keys: `account_id` to `account_key` (DF-CAS-026), `party_id` to `person_key` (DF-CAS-032, DF-INT-003, DF-DOC-100), `primary_customer_id` to `primary_person_key` (DF-CAS-004), `proceeds.account_payment_id` to `payment_code` (DF-FIN-004). |
| Job and actor wording | E2-002, 011, 014, 021, 022, 027 | JOB-01 and JOB-09 removed; SY-DATALOAD removed in favour of the recovery service identity; the COLLINS load phrasing replaced by the ACE batch where it described a Workbench load; the WIN proof-of-delivery read comes from `v_ace_pod`; REC-05 replaces the data quality exception table wording; leftover `account_payment_id` idempotency note corrected. |
| Gherkin one-When rule | E2-004, 015, 022 (AC1, AC2), 033 (AC3, AC4, AC8), 035 (AC12), 036 (AC2) | Scenarios with a second When, or with no When, reworded to one When per scenario. AC IDs, counts and intent unchanged. |
| ASCII rule | E2-017, 025, 026 | Four Thai-script test strings replaced with ASCII transliterations that keep the Buddhist-era dates and the baht amount in words. |

No `score` or NPA `asset` table reference exists in Epic 2, so there was nothing to re-key to `v_ace_score` or `v_ace_npa_asset`.

## 5. Workbook changes

- Stories: Entities regenerated from each story's Data table for all 34 stories; 17 differ from v5 (the 6 rewrites and 11 re-keyed stories). Criteria and Test cases columns recomputed.
- Acceptance criteria: Gherkin taken from the v6 Markdown, byte for byte (verified 0 mismatches); 34 rows.
- Test cases: 406 rows; Covers, Level and Data refreshed for the 6 rewritten stories; titles taken from the scenario name so they match the new AC headings; E2-023's 9 rows removed.
- Traceability: rebuilt from section 18; 85 rows. E2-030 now carries REQ-S4-002, which was missing from the v5 sheet.
- Dependencies: rebuilt from the summary table; 98 rows. RWB-E1-069 replaces RWB-E1-003, RWB-E1-004 and RWB-E1-051 in the six rewritten stories.
- Subtitles, autofilters and row heights reset; no merged cells; no non-ASCII cell.

## 6. Verification

| Check | Result |
|---|---|
| Stories, acceptance criteria, test cases against the header table | 34, 352, 406; header matches |
| Scenario count per story against the Gherkin | 352 scenarios, one When each, no orphans |
| Test IDs referenced in exception tables and traceability | all exist in their story's test table |
| Entities in Data tables against Physical Schema v5 objects | 58 distinct entities, 826 rows, 0 not found |
| Views used against ACE Source Views v1 | 12 in Data tables over `v_ace_account`, `v_ace_payment`, `v_ace_customer`, `v_ace_contact`, `v_ace_collateral`, `v_ace_collateral_detail`, `v_ace_efs_action`, `v_ace_valuation`, `v_ace_plan`, `v_ace_batch_status`, `v_ace_party_product`, `v_ace_iam_group`; all 12 exist |
| Field IDs against LDM v7 | every DF ID either matches its entity and field in v7, or is one of the five frozen Section B IDs listed below |
| Forbidden tokens: `loan_account`, `account_payment`, `party`, `contact_point`, `load_run`, `dq_exception`, `JOB-01`, `JOB-09`, `tracker`, `interface_run`, `interface_signoff` | 0 in table rows and prose (the `v_ace_party_product` view name is the only `party_product` match) |
| `public.*` references | 0 |
| Non-ASCII characters | 0 in the Markdown and 0 cells in the workbook |
| Markdown table integrity, section numbering 1 to 19 | clean in all 34 stories |

## 7. Open questions

1. **Section B field IDs.** `v_ace_account.principal_outstanding`, `interest_outstanding`, `settlement_booked_date`, `settlement_booked_amount` and `v_ace_efs_action.contact_result` have no DF-ACE IDs in LDM v7. The stories keep the frozen field-gap IDs (DF-ACC-009, DF-ACC-010, DF-ACC-030, DF-ACC-031, DF-INT-036) and mark the rows Section B. Assign DF-ACE IDs to the 12 added columns and update the three stories (E2-006, 007, 032, 034).
2. **E2-006 still records the NLEADS result on the treatment.** DF-TRT-023 to DF-TRT-026 are retired: LDM v7, the tier map and Physical Schema v5 move those four fields to `v_ace_credit_decision` (DF-ACE-288 to DF-ACE-291). The story is built around a manual result entry (8 of its 11 criteria), so it needs a re-base to read the result from the view, or a decision to reinstate the columns. Left unchanged here.
3. **E2-018 external reference.** `signature_request.external_ref` (DF-DOC-103) is gone from v5 and lives in `v_ace_esign.external_ref` (DF-ACE-296), but `v_ace_esign` carries no treatment or document link, so an EasyApp result cannot be correlated to its signature request. Needs an ACE column or a Workbench correlation key.
4. **RWB-ACE-001 is a gate, not a dependency.** Five stories read Section B objects (`v_ace_batch_status`, `v_ace_party_product`, the settlement columns, `contact_result`). The flags (`rwb.integration.efs-handover`, `rwb.payments.matching`, `rwb.integration.booking-confirmation`, `rwb.integration.customer-products`, `rwb.integration.ledger-channels`) hold them off until V0003 is applied; the dependency column does not list RWB-ACE-001.
5. **`dp_treatment` keys.** Physical Schema v5 has `UNIQUE (business_date)`, which allows one treatment row a day. E2-010 requires one row per treatment per business date; change the key to `(treatment_id, business_date)` or the product cannot hold 40 treatments.
6. **`dp_treatment.contract_no`, `contract_date`.** v5 keeps both columns; E2-010 drops them because a contract is read from `v_ace_account`. Confirm the drop in the migration so the story and the schema agree.
7. **E2-002 plan status.** The story still reads plan status through `RestructurePlanQuery` with a 2-second live read and a stored fallback, while the P2 TSD v3 names `v_ace_plan` for API-P2-010. Harmonise in the next pass; it was not one of the six rewrites.
8. **Consent model.** `contact_point_ext.consent_given` is boolean while LOV-CONSENT carries GIVEN, WITHDRAWN and UNKNOWN; WITHDRAWN and UNKNOWN both read as not given. E2-022's criteria keep the LOV labels. Consider a `consent_status` column or a view.
9. **E2-030 requirement.** The v5 summary table left E2-030's requirement cell blank while its story and traceability carry REQ-S4-002. The v6 summary and Traceability sheet now show REQ-S4-002.
10. **Separate test workbook.** Every story points to Recovery Workbench Test Cases v5.xlsx, which is not in this folder. The test data in this workbook is updated; if the separate file exists elsewhere it needs the six rewritten stories regenerated.
