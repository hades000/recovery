# Step 1 verification defects (coordinator log)

## ACE Architecture Decision v3.docx — PASS, minor
- §8 DL06 row not marked superseded by D-RCV-35
- §3.4 "Spring Batch for loads and automated chains" -> drop "loads"
- §2 option 1 Against: "recovery takes ACE's end of day data position" -> no longer a con (ADR-001 calls it an asset)
## ADR v2.md — PASS
## Lean BRD Epic 1 v3.docx — PASS, minor
- §2.2 Out of scope: add row "Excel and SharePoint tracker inventory, load and retirement – Cutover plan (U5; E1-005, E1-010, E1-012 removed)"
- §7 measure "Team Excel and SharePoint lists retired" / "ten clean days in parallel": point to Cutover plan retirement procedure
## Non Functional Specification v3.docx — PASS, minor
- §3.2: state NFR-008/NFR-009 targets include reads through v_ace_* views (ACE+recovery joins at busiest hour)
- NFR-015 target: "Visible as soon as the ACE batch completes; no Workbench lag; same-day needs under DL06"; status "Proposed, DL43"
- §1 Freshness row: "reconciled to the core bank every day" -> reconciled to the ACE account view (match NFR-018)
## Batch and Scheduling v3 (docx+xlsx) — PASS, minor
- D1 neither file states Quartz/Spring Batch tables are shared with ACE (no new qrtz_ tables) — add
- D2 docx §1 "no job starts on a fixed clock time" -> "no data job"
- D3 docx §3 runs JOB-07/08 after JOB-02; xlsx Depends on = ACE batch only — align (xlsx add JOB-02 or docx change)
- D4 docx core.xml modified date 2026-10-27 -> 2026-11-15; "19 jobs run" vs "17 run" wording
## Event and Messaging v3 (md+xlsx) — PASS, minor
- D5 xlsx Events B2 cites "(DT12, DL06)" -> D-RCV-35
- D6 AsyncAPI info.version 1.0.0 -> 2.0.0; xlsx Rules "Transactions" rule must exempt EV-26/EV-27 like md
## ACE Team Stories v1 (md+xlsx) — FAIL, 11 defects (fix after Docker schema verify; same fix agent owns views SQL + gap list + schema v5 view section)
1 md has 15 sections; add 12 Contract, 14 Validation and messages, 15 Screens and states, 17 Guardrails, 19 Out of scope; renumber 1–19
2 needed-by 2026-11-21 (30 Nov release) missing in md + xlsx Story sheet
3 md §11 lacks per-column DDL (166 cols) — add §11.4 or state xlsx Tables sheet normative
4 Type blank for 13 appendix rows (DF-PTY-003/006/009, DF-ACC-006/009/010/011/015/030/031, DF-INT-008/035/036); Frequency blank for 7 DF-ACC rows (ALS daily, end of day)
5 xlsx Tables + gap list: PK id Nullable=YES -> NO
6 xlsx Tables: no UK markers for business keys/composites
7 iam_group business key (entra_group, role_code) vs iam_group_key column — align
8 grant count "21 listed tables" (§10, §12.4) vs AC4 "14 new tables and no other" — one number
9 grantee: state ace_view_owner gets SELECT; :recovery_role nothing on public; cite SQL grant block
10 xlsx ACs shortened (AC4, AC6, AC8) — copy full md Gherkin
11 BLOCKING: no Section A/B view selects the 12 new columns (account 7, customer 3, efs_action 2) though appendix routes them via v_ace_account/v_ace_customer/v_ace_efs_action — add to Section B (ALTER/replace view) in views SQL and schema v5; point story flow step 6/AC at them
minor: §11.3 efs_action 3 fields vs 2 columns — footnote
## Target Architecture v5 (docx+pptx) — docx 4 small defects, pptx minor
- docx §12 Open decisions: add DL43 row
- docx §6.1 "Event arrives": "A load, a screen action" -> "An ACE refresh, a screen action"
- docx §8.2 Masking: use slide 12 wording "masked in the views and at the API"
- docx §8.1.1: add the tier diagram figure (slide 11) or note the table replaces it
- both §2/slide 3 "No legacy enhancement" status -> "Taken; D-RCV-35 (supersedes DL12 option A)"
- both §9 E1/slide 15: add "(RWB-E1-069)" and "Tier 2 after RWB-ACE-001"
- both §11/slide 17: add risk "RWB-ACE-001 lands late" -> Tier 2 features behind flags
- pptx slides 2, 11 "In: ACE ingestion": add "ALS, EFS, COLLINS (today)"
## Feature List v4 — FAIL 7
- (coordinator) tracker G5 says 03..13 retired; actual 03..10 + 22 retired, 11–13 re-worded (correct)
- D61 FEAT-CHO-01: still "EFS data in the COLLINS daily batch", depends FEAT-RDF-21 -> read v_ace_account/v_ace_efs_action; Systems "ACE database, Workbench"; Depends FEAT-RDF-25
- D69 FEAT-CHO-09 "read models to the data store" -> "to the recovery schema"
- D63–D65 FEAT-CHO-03/04/05 "COLLINS batch"/"COLLINS load"; CHO-03 Systems "Integration adapters", depends FEAT-DRI-09 -> ACE batch (v_ace_batch_status), depend FEAT-RDF-25/26
- D68 FEAT-CHO-08 "next day's ALS load", Systems "ALS and GL, Integration adapters" -> v_ace_account, ACE database
- D70 FEAT-CHO-10 "Automate the EFS file load" -> retire under U1 (E2-023 removed); update A2 counts (368 live / 10 retired)
- minor: A2 "two cover the ACE read path" -> "Two new features (FEAT-RDF-25, 26) cover…"; D29 Systems still lists COLLINS
## Business Glossary v3 — PASS (optional: Key "Maps to" add "or ACE view"; row 72 POD add v_ace_pod)
## Role to System Access Matrix v3 — PASS w/ notes
- CCMS column now 0 roles: note "via ACE" (or drop)
- data steward given R on ACE (Y35): register grants SELECT only to recovery service identity — remove or align with Admin model v5
- OUT OF STEP: 02/Users Roles and Permissions v3.xlsx still has SY-DATALOAD (Roles, Permissions, SSO sheets), no SY-RECOVERY -> new v4 (not in tracker; add row)
## Decision Log v9 — PASS, 1 defect
- By owner sheet: add "ACE team lead, 1, 2026-11-21, DL43"; remove ruled DL41 row (K. Book with the data architect)
- workbook title property says v8 -> v9
- check: DL06 recommendation changed to "B for named same-day triggers" — keep only if consistent with D-RCV-35 (ACE batch; same-day triggers DL06 B is fine) — leave, note in edit log
## Specification Rulings v2.md — defects
- header "| Superseded by | D-RCV-35 |" -> "Counts superseded by D-RCV-35 (section 0)"
- seed table lines ~193–206: copy definitions + systems of record from CDM v6 Data products (DP02 "identity masked to last four", SoR "ACE (ingested from SCBPDM and the core bank)"; DP05 ACE (ingested from EFS); DP06 ACE (ingested from CCMS, SVAF, AMIS and RPS); DP07 ACE (ingested from LIT and WIN)…Workbench for notices and enforcement; DP04 CDM v6 split wording)
- §10 verification steps: re-base to v5 counts (92 tables, 30 views, 122/1,366) and v_ace_account.days_past_due / ACE (ingested from ALS)
## Pre-Build Rulings v2.md — defects
- same header fix
- Q4 cites CDM v5 (lines ~32, 80, 100) -> v6
- §0 add: Q4 (= R4) holds; systems of record become "ACE (ingested from X)"
## Admin and Access Model v5.docx — 1 defect
- para ~497: "recovery service identity … has no write on any table"/"fails in the catalog" -> "…no write on any ACE table or view, so a direct read of a public table fails at the database."
## Interface Specifications v3 (md+xlsx) + System Disposition v3 — FAIL
1 field-map targets INT-01,02,04,09–13,16 still Workbench entities (loan_account, account_payment, party, collateral, valuation, asset, legal_action, write_off) -> ACE table.column (account.delay_days, payment.pay_date, customer.person_key, lawsuit.*, gl_write_off.*, npa_asset.* …) + v_ace_* view column; source: LDM v7 "ACE mapping" sheet + Field Gap List v1
2 INT-02->proceeds, INT-07->interaction, INT-12->asset_sale, INT-15->notice -> payment.*, efs_action.*, npa_sale.*, pod_receipt.*
3 NLEADS/EasyApp maps target treatment.nleads_ref/credit_result*/signature_request.external_ref -> credit_decision.*, esign_request.*
4 placeholder "New ACE interface (number in Interface Specifications v3)" -> assign INT-35 (NLEADS credit decision in) and INT-36 (EasyApp e-sign in) [check numbers free]; add to Disposition Interfaces; keep INT-26 on NLEADS row 23
5 Disposition "In ACE today" INT-03,19,20,26,33 "No" -> restore "Not applicable"
6 "In ACE today" rule per Tier Map: Partly = Tier1 + Tier2 cols/tables; No = Tier2 only -> INT-08 No, INT-11 No, INT-09 No, INT-10 Partly, INT-01 Partly, INT-04 Partly
7 Disposition Interfaces row 2 "outbound paths stay with the Workbench" but INT-17/18/22 owned by ACE team -> reword
minor: INT-21 name iam_group / v_ace_iam_group; add "supersedes v2" line
## CDM v6 xlsx — defect
- D1 ACE gaps table efs_action "Fields read"=2, gap list says 3 (contact_result serves 2) -> 3 (column sums to 80)
- minor: Data products Entities counts typed numbers vs v5 COUNTIF formulas (restore formulas); G12 "All loaded data products" reword
## CDM v6 pptx — defect
- D2 slide 9 G5 "The model holds what COLLINS carries" -> match xlsx ("the ACE account at its current state and the monthly bucket snapshot")
- D3 title property says v5 -> v6; minor slide 10 G11 "once read" -> "once received"
## DQ and Reconciliation Rules v3 — defect
- D4 REC-05 reused (v2 REC-05 = Notices to WIN vs barcodes, now REC-09). Fix: restore REC-05 = WIN barcodes; new business-key check gets REC-09 (other live docs use REC-05 for barcodes)
## Party and Customer MDM v3 docx+xlsx — defects
- D5/D8 M5 partner tax ID given to ACE ingestion but partner is a Workbench record -> M5 stays with Workbench partner master
- D6 restore rule "A case is never merged by the party match; duplicate cases follow R-UNI-17"
- D7 xlsx: add v_ace_ca_relation rows (person_key, account_key, relation_type, amount_of_guarantee, date_of_guarantee)
- D9 xlsx v_ace_customer lists party_type, id_type, segment (Tier 2) but views SQL has no such columns -> ties to ACE story defect 11 (Section B view must add them)
## Physical Schema v5 (found in passing)
- sys_objects v_ace_customer data_product DP01 -> DP02 (CDM)
- v_ace_customer.deceased_flag (DF-ACE-061) typed TEXT varchar(255) but view casts boolean -> boolean
## LDM v7 — FAIL 8
- A1 title property says v6; add version/date line (Entities row 2) v7 15 November 2026
- A2 Relationships!A2 "119 references" -> 100
- A3 DF-DOC-054 document_intake.run_id refers to removed load_run -> job_run (JOB-12) or clear; same in schema v5 sys_fields
- A4 Source field nonexistent cols: DF-CAS-004 public.customer.primary_person_key -> customer.person_key; DF-FIN-004 public.payment.payment_code -> payment.pay_key; DF-INT-022 public.contact.contact_key -> phone_key/email_key/address_key (composite contact_type:key)
- A5 flag the 42 DEF-05 fields (Note "DEF-05")
- A6 view field types/sources from view SQL (payment_date date, tdr_flag boolean, deceased_flag boolean; sources for v_ace_contact.contact_type/city/post_code/country, v_ace_plan.installments/recommended_installment/recommended_package)
- A7 personal-data flags on view fields (v_ace_customer names, DOB, id_no_*, v_ace_contact.contact_value) + Entities Personal data counts
- A8 Sources rows 5–7 sum 1,324 ≠ 1,366; re-derive
## STTM v4 — 3
- B1 ACE gaps Type blank for 50/80 rows -> fill from gap list ACE additions (also RWB-ACE-001 Fields 13 blanks)
- B2 Source field literal "None" -> empty
- B3 add title/version/date header row + Title property
## Gap list (advisory, coordinator/data fix)
- DF-DEC-006 classed ACE reuse but maps to collins_score.model_version (Tier 2) -> ACE new; split becomes 51 reuse / 81 new — cascades: register, gap list, LDM, STTM, ACE story (decide)
- DF-PTY-016 gap list read path v_ace_contact.value -> contact_value
## COORDINATOR DECISION (applies to all agents)
- The 12 new ACE columns (account 7, customer 3, efs_action 2) are exposed in the EXISTING view names v_ace_account, v_ace_customer, v_ace_efs_action through a Section B CREATE OR REPLACE VIEW (ships after RWB-ACE-001). References like v_ace_customer.party_type / id_type / segment, v_ace_account.business_unit / daily_bucket, v_ace_efs_action.contact_result are CORRECT; annotate "(Section B, after RWB-ACE-001)" where useful. The views SQL / schema v5 / ACE story fix agent adds them.
## All five upgraded data xlsx — docProps dc:title still old version (Data Classification v4, Reference Data v4, Reporting v3, Volume v3.xlsx, Ownership v3) -> set to new filename
## Data Migration Approach v3.docx — defects
1 §1 "Recovery team spreadsheets" "then retired (RWB-E1-012)" -> "then retired through the Cutover plan (U5)"
2 §2 "Lawsuits, hearings, notices and proof of delivery": notice is Workbench Tier 4 -> drop "notices"
3 §8 add DL43; re-word DL12 (option A superseded by D-RCV-35)
## Data Classification v4.xlsx — defects
1 14 re-keyed fields keep old names (DF-CAS-004 primary_customer_id, DF-CAS-026 account_id, DF-INT-022 contact_point_id, DF-FIN-004 account_payment_id, DF-DOC-100 party_id …) -> rename per LDM v7 (primary_person_key, account_key, contact_key, payment_code, person_key), reclassify Indirect identifier/Confidential, fix DF-INT-022 meaning, update Summary (91/843) and Identifiers
2 Handling "Restricted / Stored": "Stored in ACE only" -> "ACE source fields stored in ACE only; Workbench Restricted fields encrypted at rest"
3 minor: restore COUNTIF formulas in Summary
## Reference Data v4.xlsx — defects
1 LOV-ROUTE used by score.route_code -> v_ace_score.route_code; LOV-CREDIT-RESULT used by treatment.credit_result -> v_ace_credit_decision.credit_result (check exact view names in views SQL)
2 six Tier-2 column refs — keep, annotate "(Section B, after RWB-ACE-001)" per coordinator decision
3 upstream: LDM v7 "Loaded lists" tab still says loan_account, collections_history, "loaded from" -> LDM fix agent
## Reporting and Analytics v3 — PASS (title prop; optional "Load or refresh" -> "Refresh"; dim_date v_ace_holiday, dim_product v_ace_product if those views exist)
## Volume and Scale v3 xlsx+pptx — PASS minor
1 pptx slide 8 assumptions table: add I33, I34
2 "the only freshness stamp the Workbench holds" -> data_product_load is the stamp, sourced from ace_batch_run
3 cosmetic: ACE growth rows 21–23 column alignment
## Data Ownership v3 — defects
1 Tier column: DP01 "1 and 2"; DP02 "1, 2 and 3"; DP04 "1 and 4"; DP05 "1, 2 and 4"; DP06 "1, 2, 3 and 4"
2 System of record owner DP01, 02, 06, 11, 13 -> ACE team lead (per Roles tab) for Tier 1/2
3 DP07 add pod_receipt
4 Quality measures: add Workbench checks for Tier 3/4 (completeness/validity) and case uniqueness rule (DL17) checked by Workbench
## Physical Schema v5 + ACE Source Views v1.sql (Docker verify) — 4 FAIL
1 Section B views embedded in v5 (lines ~6071–6762) -> v5 fails single-file load (28 errors) until RWB-ACE-001
2 ace_view_owner grant (views file ~721–725, v5 ~6771–6775) lists only Section A tables -> Section B unreadable
3 GRANT SELECT ON ALL TABLES IN SCHEMA recovery (views ~729, v5 ~6779) contradicts header; register 10.2 "no INSERT/UPDATE/DELETE on any table" would block Workbench writes
4 177/304 view fields physical_type wrong in v5 sys_fields DF-ACE-* (mirrored LDM v7): regenerate from information_schema after compile
5 document_intake.run_id references load_run (v5 ~4397 DF-DOC-054) -> references_object NULL; describe as "JOB-12 Spring Batch job execution id"
6 descriptions: "The loan_account/account_payment/party/asset this record belongs to" (2500, 2675, 3655, 3830, 2769, 3924, 2506, 2644, 2652, 2682, 2711) -> "The ACE account (account_key) / ACE payment (payment_code) / ACE customer (person_key) / ACE NPA asset (asset_key) this record belongs to"; "detokenized only at generation" (3290, 4445 DF-REF-258) -> reword per masking design; 2914 "INT-01 to INT-34" check
## COORDINATOR DECISIONS — data model (binding for DM1/DM2)
D1 Migration blocks in Physical Schema v5: three delimited blocks.
   V0001 baseline (RWB-E1-001): tables, extension tables, helper functions, dictionary rows for tables + Section A views.
   V0002 Section A (RWB-E1-069): 16 views over existing ACE tables + grants. Loads standalone on today's ACE.
   V0003 Section B (after RWB-ACE-001): 14 Tier 2 views + CREATE OR REPLACE of v_ace_account, v_ace_customer, v_ace_efs_action adding the 12 new columns + their sys_objects/sys_fields rows + Tier 2 grants. Requires the Tier 2 tables.
   V0001+V0002 must load with 0 errors on ACE Schema PostgreSQL v1.sql alone; V0003 after ace_tier2_probe.sql. Report per-migration and end-state dictionary counts.
D2 Grants. RWB-ACE-001 (ACE team, owner of public) grants SELECT to ace_view_owner on every ACE table the 30 views read (Tier 1 tables used by Section A + the 14 Tier 2 tables) and nothing else. recovery_svc: SELECT on recovery.v_ace_* only for ACE data; no privilege at all on public; no write on any v_ace_* view. Workbench-owned recovery tables (Tier 3/4) get the normal service DML grant (SELECT, INSERT, UPDATE; DELETE only where the design allows; append-only tables keep their triggers). Conformance test: no recovery constraint references public; recovery_svc has no privilege on public; recovery_svc cannot write any v_ace_* view.
D3 The 12 new ACE columns use exactly the view column names in the gap list "read path" column (do not rename).
D4 DF-DEC-006 (collins_score.model_version) is ACE new, not reuse: split becomes 51 reuse / 81 ACE new / 1 extension = 133. Coordinator updates register; DM1 LDM/schema, DM2 gap list/STTM/ACE story.
D5 v_ace_customer sys_objects data_product = DP02; deceased_flag physical type boolean.
## COORDINATOR DECISION D6
- No interim freshness view before RWB-ACE-001. ace_batch_run (v_ace_batch_status, Section B) is a hard dependency of E1-015 and case intake (E1-018), already covered by DL43 / register R1. Features gated behind flags until V0003.
## OUT-OF-TRACKER FILES found (Wave 5 sweep must include)
- 02 Users Roles and Permissions v3 -> v4 (in progress, fix BA agent)
- 07 Error and Message Standard v3.docx: MSG-P1-001 text change ("Today's data is not yet complete."), load/tracker messages MSG-P1-002/008/009/010/013/014/016/017/018 retire
- 07 Screen Specifications / Screen Inventory: tracker and load screens (check)
- Batch xlsx C8 JOB-04 "balances against the core bank" -> ACE account view (minor)
