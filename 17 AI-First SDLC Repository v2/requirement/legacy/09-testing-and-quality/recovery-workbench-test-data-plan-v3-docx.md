<!-- source: 09 Testing and quality/Recovery Workbench Test Data Plan v3.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `09 Testing and quality/Recovery Workbench Test Data Plan v3.docx`  
> **Converted from:** DOCX

Recovery Workbench

Test data plan

SCB Collections and Recovery. Henka Group, 15 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench test data plan |
| Version | 3 |
| Date | 15 November 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC/IEEE 29119 |
| Decision | D-RCV-35 (U1, U4); ADR-010; DL43 |

# 1. Sources

Every environment below SIT is seeded from the ACE schema and the recovery schema. No environment holds a copy of a source table or a load table, because neither exists under D-RCV-35 (U1). SIT and UAT read source data through the 30 recovery.v_ace_* views; the Workbench schema holds no copy of a source row.

| Environment | Data | Source | Personal data |
|---|---|---|---|
| DEV | Synthetic ACE-shaped rows and synthetic Workbench rows, rebuilt from the DDL and the data dictionary | RWB-E1-065 SandboxGenerator, seed 20261128 | None |
| SIT | Masked copy of the ACE tables, ingested by ACE from the SIT sources, plus scripted cases | ACE ingestion; PII service (RWB-TE-004) | Masked |
| UAT | Masked ACE copy plus scripted cases | PII service; testers | Masked |
| Performance | Masked ACE copy scaled to the 2027 volume | PII service with scaling | Masked |

# 2. What the sandbox seeds

The sandbox is the only test data set below SIT. RWB-E1-065 builds it from the same DDL as SIT: ACE Schema PostgreSQL v1.sql for the 22 Tier 1 tables, the RWB-ACE-001 DDL for the 14 Tier 2 tables, then V0001 for the 92 recovery tables and the four extension tables, V0002 for the 16 Section A views and V0003 for the 14 Section B views. It seeds rows by reading sys_objects, sys_fields and lov_value, so a schema change reaches the sandbox with no generator edit.

| Object group | What is seeded |
|---|---|
| Tier 1 ACE tables (22) | One or more rows in account, payment, customer, phone, email, address, ca_relation, aa_relation, collateral, asset, efs_action, efs_action_code, efs_assignment, bucket_log_snapshot, product, branch, bot_holiday, iam_user, ace_case, cfsc_mg_ssme_tdr_case, tdr_calculation and ai_recommended_plan. 184,500 account rows carry the ALS business shape; 28,140 of them sit at 90 days past due or more, with accounts at 89 and at 90. |
| Tier 2 ACE tables (14) | ace_batch_run holds one row per source and business date, with COMPLETED, FAILED and LATE rows; valuation, collateral_detail, npa_asset, npa_sale, lawsuit, hearing, pod_receipt, gl_write_off, collins_score, party_product, credit_decision, esign_request and iam_group each hold rows for every Workbench read. The 12 new columns on account, customer and efs_action are filled. Behind DL43: until the DDL lands, the Section B views and their features stay behind their flags. |
| Recovery tables (92) | 2,812 cases with seed 20261128: 1,226 Mortgage, 1,296 Hire purchase and 290 SSME, plus 10 cases for each exception shape; their accounts, parties, contact points, collateral, valuations, payments, interactions and documents are linked by business key. |
| Extension tables (4) | party_ext, contact_point_ext, account_ext and valuation_ext, 49 columns in all, one row per ACE business key where a Workbench decision exists. |
| Views (30) | The 16 Section A and 14 Section B recovery.v_ace_* views; each returns at least one row; each has one sys_objects row and one sys_fields row per column. |
| Removed tables (20) | None. loan_account, account_payment, party, contact_point, collateral, account_collateral, collections_history, party_product, valuation, score, asset, load_run, dq_exception, dq_rule, source_field_map, source_code_map, interface_run, interface_signoff, tracker_inventory and tracker_row do not exist in schema recovery and are neither seeded nor read. |

There is no copy table and no load table in the sandbox. A test that needs a source value reads it through its view; the expected value comes from the ACE-shaped row, not from a Workbench copy.

# 3. What each test needs

| Test | Data |
|---|---|
| Allocation | Cases for every product group, region and exposure band; owners at and below the capacity limit and one owner above it. |
| Routing rules | One case per rule row in its from state, with its condition true and false. |
| Case list | v_ace_account at 89 and at 90 days past due; 21 entry exclusions; 37 case accounts below the threshold; v_ace_batch_status with COMPLETED and missing rows. |
| Reconciliation | Variances at zero, below and above recon.tolerance.pct; a person_key with no v_ace_customer row; a payment in v_ace_payment with no proceeds. |
| Freshness | One ace_batch_run row per source and business date, with COMPLETED, FAILED, LATE and duplicate rows; a weekly source between its batches. |
| Views and dictionary | One row per view; a view column with no sys_fields row; a recovery constraint that points at public; a role with no grant. |
| Approvals | Decisions at each level and amount boundary of the delegation table. |
| Deviations | Cases with each of X1 to X7. |
| Documents | The labeled sample of 180 documents across the six types. |
| Batch and job runs | JOB-02, JOB-03 and JOB-04 held by the daily gate, failed at a step and rerun; no inbound file and no file arrival. |
| Partners | A firm of each partner type with instructions in every status. |

# 4. Handling personal data

Masking follows RWB-E1-037. The rules, the masking version and the masking position are data; Compliance sets them and approves each version.

- No production data in DEV. The sandbox is synthetic and is rebuilt from the seed and the DDL.

- The ACE-shaped tables hold clear values where ACE holds them, because ACE is the system of record; the sandbox verifier allows a clear identity number only there.

- recovery.v_ace_customer exposes id_no_masked (DF-ACE-073) and id_no_last4 (DF-ACE-074) only. The clear identification number never leaves ACE, and there is no token and no token store.

- recovery.v_ace_contact exposes contact_value and contact_value_masked (DF-ACE-078, DF-ACE-079). Phone, email and address are clear in the view because notices and calls need them; display masking is applied at the API.

- Masking is applied by role under RWB-E1-037 with masking version MASK-SIT-01; a personal field with no masking rule is masked.

- No clear personal value is written to schema recovery. The sandbox verifier fails the build and names the table and column when one appears.

- Masked data never leaves SIT and UAT. Defect records and screenshots carry no personal data.

- The PDPA lint (RWB-TE-011) checks fixtures, code and logs in the pipeline. Test data is refreshed before each release and destroyed when the environment is rebuilt.

# 5. Owners

| Item | Owner |
|---|---|
| Synthetic seed and fixtures | QA engineers with the recovery squad |
| ACE-shaped seed and batch rows | Data engineering with the ACE team |
| Masked copies | Data engineering |
| Document sample | Autonomous Ops team |
| Approval of masking rules and masked copies | Compliance |
| View, dictionary and grant fixtures | Recovery squad |

# 6. Counts the build checks

| Item | Count |
|---|---|
| Tier 1 ACE tables | 22 |
| Tier 2 ACE tables | 14 |
| Recovery tables | 92 |
| Extension tables | 4 |
| recovery.v_ace_* views | 30 (16 Section A, 14 Section B) |
| Dictionary objects | 122 |
| Dictionary fields | 1,366 (304 on the views, 49 on the extension tables) |
| Removed tables | 0 seeded, 0 read; 20 do not exist |
| Cases in the sandbox | 2,812 plus 10 for each exception shape |
