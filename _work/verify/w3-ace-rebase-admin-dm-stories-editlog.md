# Wave 3 edit log: Administration stories v3 and Data Migration stories v3 (ACE re-base)

Agent: Wave 3 writer (ACE re-base). Date: 15 November 2026.

Inputs read: D-RCV-35 and ADR-010 (Change Register v1, Data Tier Map v1, ACE Source Views v1, ACE Schema PostgreSQL v1), Physical Schema v5 (`_work/data/v5_objects.csv`, `v5_fields.csv`), LDM and Data Dictionary v7 field IDs, FSD P1 Recovery data engine v3, Epic 1 story files v6 (RWB-E1-011, E1-037, E1-056), Data Migration Approach v3, API Specification v3 (`api_build_v3.py`), Administration Stories v2 (.md and .xlsx), Data Migration Stories v2 (.md and .xlsx).

## 1. Files written

| File | Change |
|---|---|
| `04 User stories\Recovery Workbench Administration Stories v2.md` / `.xlsx` | Superseded; left in place |
| `04 User stories\Recovery Workbench Administration Stories v3.md` | New. 22 stories, 49 acceptance criteria, 88 test cases, ASCII |
| `04 User stories\Recovery Workbench Administration Stories v3.xlsx` | New. 22 Stories rows, 22 Gherkin rows, 88 test rows, Related backlog sheet unchanged |
| `04 User stories\Recovery Workbench Data Migration Stories v2.md` / `.xlsx` | Superseded; left in place |
| `04 User stories\Recovery Workbench Data Migration Stories v3.md` | New. 14 stories (12 live, 2 removed), 36 acceptance criteria, 49 test cases, ASCII |
| `04 User stories\Recovery Workbench Data Migration Stories v3.xlsx` | New. 14 Stories rows with Entities, Depends on, Messages, Criteria and Test cases refreshed |

Counts: Administration acceptance criteria 47 to 49 (AD-018 and AD-019 each gain one); test cases 88 to 88. Data migration acceptance criteria 42 to 36 (six withdrawn with DM-001 and DM-002); test cases 57 to 49.

## 2. Administration stories

### 2.1 Rewritten

| Story | What changed |
|---|---|
| RWB-AD-018 Interface and job monitor | The monitor shows Workbench jobs from `job_catalog` (job ID, business date, status, duration, checks) and the ACE batch status per source from `v_ace_batch_status` (business date, status, record count, completion time). No inbound load, no file row, no load rerun. AC1 workbench jobs and their ACE date, AC2 rerun a Workbench job from its run book, AC3 a late ACE batch leaves the dependent job WAITING and the product STALE with MSG-P1-001. Data becomes job_catalog, data_product_load and v_ace_batch_status (was document and decision_log_entry). Endpoints: GET /admin/jobs, POST /admin/jobs/{jobId}/rerun, GET /data-products/freshness. SCR-45 removed from the screen table; SCR-44 gains the state "waiting for the ACE batch". MSG-P1-002 (refused load) withdrawn. Depends on adds RWB-E1-069; Decision becomes D-RCV-35. |
| RWB-AD-019 Data quality and reconciliation console | The console shows the reconciliation breaks of REC-01 to REC-05, the REC-05 referential completeness and stale data products. No `dq_exception` row, no exception endpoint. AC1 a REC-01 break with variance 12, 0.41 percent and the 12 account keys, AC2 a REC-05 orphan that never changes the case, AC3 a stale product. Data becomes reconciliation_result, data_product_load, case_list_row and v_ace_account (was recovery_case and the account copy table). Endpoints: none; the text states the endpoint is withdrawn and that the console reads the reconciliation and data quality extract plus the freshness stamp. MSG-P1-012 added, MSG-P1-002 withdrawn. Depends on adds RWB-E1-015 and RWB-E1-069; Decision becomes D-RCV-35. |

Test ID mapping in the two rewritten stories (IDs kept, meanings refreshed): AD-018 and AD-019 both now run TC-01 AC1, TC-02 AC2, TC-03 AC3, TC-04 Access. The v2 Principle 5 rows are withdrawn: neither story writes a decision log entry, and the Epic 1 parents (RWB-E1-056, RWB-E1-011) carry no such test.

### 2.2 Minor edit

| Story | What changed |
|---|---|
| RWB-AD-004 Masking profiles per role | The profile is `masking_rule` (field_id, unmasked, masking_version, valid_from, valid_to) and it names view field IDs. AC1 reads `v_ace_customer.id_no_masked` and `v_ace_contact.contact_value_masked`; AC2 unmasks the contact value from `contact_value` and logs it, while the identity number stays `id_no_masked`; AC3 a new masking_rule version. Data: `contact_point` replaced by v_ace_contact and v_ace_customer, `masking_rule` added. Endpoints move from rule-versions to /admin/reference-loads and /reference-loads/{loadId}/approve with RW-COMPLY as approver. Decision becomes DL26, D-RCV-35. |

### 2.3 File-wide edits (all 22 stories)

- Guardrail: "No read of another module's tables" now ends "; ACE data only through recovery.v_ace_* views." AD-018 adds "and ACE batch status only through v_ace_batch_status" plus the no-ACE-batch-rerun rule; AD-019 adds the no-change-to-a-break rule; AD-004 adds the no-clear-identity-number rule.
- `role` rows: `entra_group` removed (DF-REF-034 to DF-REF-038); the group-to-role mapping now reads `v_ace_iam_group` (DF-ACE-301 to DF-ACE-304) and that row is added to AD-001, which is the story about the mapping.
- `document.party_id` becomes `person_key` (DF-DOC-003) in all 8 rows.
- `recovery_case.primary_customer_id` becomes `primary_person_key` (DF-CAS-004) in all 7 rows.
- Intro text: "interface monitoring" becomes "job and ACE batch monitoring", with a version note on the re-base.
- Summary table: RWB-AD-018 depends on RWB-E1-056 and RWB-E1-069; RWB-AD-019 on RWB-E1-011, RWB-E1-015 and RWB-E1-069. Related-backlog title of RWB-E1-056 follows the Epic 1 v6 file ("... every Epic 1 Workbench job").
- No `SY-DATALOAD`, `load_run`, `dq_exception`, tracker, source-copy table or JOB-01/JOB-09 wording remains. Reference and rule "load" wording is kept: those are configuration loads with an approver, not source loads.

## 3. Data migration stories

### 3.1 Removed

| Story | Disposition |
|---|---|
| RWB-DM-001 Migrate account and arrears | Removed, D-RCV-35 U1. The data is in ACE and is read through v_ace_account, v_ace_bucket_log, v_ace_product and v_ace_branch. Its AC1 to AC3 and TC-DM-001-01 to TC-DM-001-04 are withdrawn, named in the removed block. DP01 stays in the catalog with system of record "ACE (ingested from ALS)". |
| RWB-DM-002 Migrate customer and party | Removed, D-RCV-35 U1. The data is in ACE and is read through v_ace_customer, v_ace_contact, v_ace_ca_relation, plus party_ext and contact_point_ext for the Workbench flags and consent. AC1 to AC3 and TC-DM-002-01 to TC-DM-002-04 withdrawn. DP02 stays with "ACE (ingested from SCBPDM)". |

### 3.2 Reduced to the Workbench-only part

| Story | Workbench part kept | Read from ACE instead |
|---|---|---|
| RWB-DM-005 Migrate contact and promises | interaction (promise amount and date, contact_key, person_key) and contact_point_ext | v_ace_efs_action |
| RWB-DM-006 Migrate collateral and assets | listing, asset_sale, valuation_ext | v_ace_collateral, v_ace_valuation, v_ace_asset, v_ace_npa_asset, v_ace_npa_sale |
| RWB-DM-011 Migrate scores and route economics | the route on the case, case_list_row and the baseline measure_snapshot | v_ace_score |
| RWB-DM-013 Migrate money and closure | proceeds (payment_code) and the write-off decision | v_ace_payment, v_ace_write_off |

### 3.3 Kept, with the template fixed

RWB-DM-003, 004, 007, 008, 009, 010, 012 and 014 keep their scope, re-worded to the Workbench tables and the ACE business keys.

The template artifact is gone from all 14 sections: every Data table starts from `recovery_case` with `primary_person_key`, and account and person links are `case_account.account_key` (DF-CAS-026) and `case_party.person_key` (DF-CAS-032). There is no account copy table and no party table anywhere in the file. Story-specific entities added where the v2 template had none: case_account and case_party (DM-003), v_ace_plan (DM-004), debt_sale_lot and debt_sale_account (DM-009), case_list_row and measure_snapshot (DM-011), proceeds and write_off (DM-013), reference_version and reference_row (DM-014). `document_field` is kept only in DM-010, where documents are the subject.

Common Gherkin (all 12 live stories): AC1 extract the Workbench records and name the keys, AC2 reconcile every business key through REC-05, AC3 cut over with the legacy tables read-only. DM-014 replaces AC2 with the reference version check (row count, content hash, approver, a test case for every rule row). Endpoints: none; the tracker retire endpoint and the data quality exception endpoint are withdrawn with the tracker and exception estate. Depends on becomes RWB-E1-001 and RWB-E1-069. MSG-P1-002 withdrawn; MSG-P1-012 added where SCR-45 is named.

### 3.4 Workbook

- Stories: Entities regenerated from each section's Data table; Depends on, Messages, Criteria and Test cases recomputed; the two removed rows read "Removed by D-RCV-35. The data is already in ACE and is read from the views." with Entities, Screens, Permission and Messages None and Decision D-RCV-35; the subtitle records the two removals. This is the template list the v2 workbook repeated in every row: it now names only Workbench tables and the views.
- No new sheet, no merged cell, no non-ASCII cell; autofilter and freeze panes kept.

## 4. Verification run

| Check | Result |
|---|---|
| Stories present, keys unchanged | Administration 22; Data migration 14 (2 marked removed) |
| Acceptance criteria and test cases against the header | 49 / 88 and 36 / 49; every AC has a test and every AC-covering test names an existing AC |
| Gherkin | one `When` per scenario, `Given` and `Then` present, Feature line equals the story title, no fence mismatch |
| Entities in Data tables against Physical Schema v5 objects | Administration 67 rows, Data migration 39 rows, 0 not found |
| Field IDs against Physical Schema v5 | every ID and every range end exists, and each range belongs to its entity; 0 defects |
| `v_ace_*` names used | 5 in Administration, 21 in Data migration; all 26 are in the 30-view list |
| Forbidden tokens (`SY-DATALOAD`, `load_run`, `dq_exception`, tracker, account copy, party table, `JOB-01`, `JOB-09`, `LoadCompleted`, token columns) | 0 in both files |
| Removed-story references (E1-003/004/005/006/009/010/012/051, E2-023) | 0 |
| Message IDs | 14 IDs, one wording each; texts match FSD P1 v3 (MSG-P1-001, MSG-P1-012) |
| Workbook against Markdown | Gherkin 0 mismatches; Entities 0 mismatches (the two removed rows carry None by design) |
| Non-ASCII characters | 0 in both Markdown files and 0 cells in both workbooks |

## 5. Open questions

1. **AD-019 has no endpoint.** API v3 withdraws `/admin/data-quality/exceptions` and defines no replacement, and RWB-E1-011 v6 states there is no exception endpoint. The console reads the published reconciliation extract. If E8 needs a live read for SCR-45, API v3 and FSD P4 v3 must add one, and both must name it.
2. **Per-account break rows.** OQ-P1-06 in FSD P1 v3 is still open: `reconciliation_result` holds totals and the break list lives in the extract. The console is written to that, and no new table is assumed.
3. **ACE batch rerun.** AD-018 allows a rerun only of a Workbench job. If operations ask for an ACE batch rerun from the Workbench, it contradicts U1 and would need an ACE-owned endpoint.
4. **DM-011 route economics.** The Data table takes `case_list_row` and `measure_snapshot` as the Workbench-calculated expected-return and sale-estimate record, following Data Migration Approach v3. If a dedicated expected-return table is added, DM-011's Data table changes with it.
5. **DM-002 title.** The word "party" survives only in this removed story's title, because Change Register Appendix A names it that way. Its body names no party table.
6. **Residual template rows in other Administration stories.** AD-002, AD-009, AD-010 and the rest still carry Data rows the story does not strictly need (assignment, document, lov_value). They are valid v5 entities and were out of this edit's scope; a later pass may trim them.
