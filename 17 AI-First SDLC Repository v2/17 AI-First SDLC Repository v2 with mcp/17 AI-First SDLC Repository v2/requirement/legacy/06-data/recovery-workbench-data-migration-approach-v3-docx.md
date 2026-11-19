<!-- source: 06 Data/Recovery Workbench Data Migration Approach v3.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `06 Data/Recovery Workbench Data Migration Approach v3.docx`  
> **Converted from:** DOCX

Recovery Workbench

Data migration approach

SCB Collections and Recovery. Henka Group, 15 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench data migration approach |
| Version | 3 |
| Date | 15 November 2026 |
| Prepared by | Henka Group |
| Structure | Henka word rules |
| Decision | D-RCV-35: ACE holds the source data; the Workbench migrates only its own case state, documents, decisions and reference data |

# 1. What moves

| What | Data product | Scope | History | How | When |
|---|---|---|---|---|---|
| Case and ownership state | DP03 | Open cases: status, stage, route, owner, queue, tasks, timers and deviations | Current position | Spreadsheet extract, re-keyed to person_key and account_key | E1 |
| Recovery team spreadsheets | DP03, DP04 | The Excel and SharePoint lists of open recovery work | Open items only | File extract, then retired through the Cutover plan (U5) | E1 |
| Treatment records | DP04 | Restructures, settlements and deeds agreed but not yet booked, with their approvals | Open only | Spreadsheet extract; the plan itself is read from v_ace_plan | E2 |
| Documents | DP10 | Documents for open cases in shared drives and the mailroom | Open cases only; originals tracked | Bulk intake through OCR | E1 and E2 |
| Decision log | DP12 | Decisions taken outside the Workbench on the open cases, with their rule and model version | Open cases only | Spreadsheet extract | E1 |
| Partners and open instructions | DP08 | Panel firms and their open work | Open instructions | Partner master load | E4 to E6 |
| Reference data | DP14 | Rules, approval limits, lists of values, roles and letter templates | Current versions | Validated load, versioned | E1 |

# 2. What does not move

These data products are already in ACE. Nothing of them moves into the recovery schema: the Workbench reads them through the view named beside each one and holds only its own decisions about them, in party_ext, contact_point_ext, account_ext and valuation_ext.

| Already in ACE | Read through |
|---|---|
| Account, arrears, balances, bucket and classification | v_ace_account |
| Payments and proceeds | v_ace_payment |
| Customer, identity and relations | v_ace_customer, v_ace_ca_relation |
| Phone, email and address | v_ace_contact |
| Collateral, assets and appraisals | v_ace_collateral, v_ace_asset, v_ace_valuation, v_ace_npa_asset, v_ace_npa_sale |
| Collections history from EFS | v_ace_efs_action |
| Lawsuits, hearings and proof of delivery | v_ace_lawsuit, v_ace_hearing, v_ace_pod |
| Write-offs and GL postings | v_ace_write_off |
| Scores and route economics | v_ace_score |

# 3. Principles

- ACE holds the source data. The Workbench runs no load of accounts, payments, customer, contact, collateral or collections history, and migrates none of it.

- Only open work and the history a decision needs move; closed history stays in its source.

- Every migrated record carries its source and migration date.

- Each migration reconciles to its source before cutover, and the case list reconciles to v_ace_account.

- Spreadsheets are retired with a read-only archive once their content is on the case.

- A link to a source record is a business key, never a copy of the record.

# 4. Cases in flight

| State today | On the Workbench |
|---|---|
| Account at 90 days past due with no recovery action | New case, allocated by rule; the account is read from v_ace_account |
| In restructure or settlement | Case with the treatment record and its status; the plan is read from v_ace_plan |
| In litigation | Case in the litigation stage, linked to v_ace_lawsuit and v_ace_hearing; the Workbench keeps the instruction |
| Asset held | Case linked by asset_key to v_ace_asset and v_ace_npa_asset where the case is open |
| In a partner's hands | Case with an open partner instruction |

# 5. Migration stories

Six of the fourteen migration stories change. The other eight, DM-003, DM-004, DM-007, DM-008, DM-009, DM-010, DM-012 and DM-014, keep their scope, with their sources re-worded to ACE where a read replaces a load.

| Story | New scope |
|---|---|
| RWB-DM-001 Migrate account and arrears | Out of scope. The data is in ACE and is read through v_ace_account. |
| RWB-DM-002 Migrate customer and party | Out of scope. The data is in ACE and is read through v_ace_customer, v_ace_ca_relation and v_ace_contact. |
| RWB-DM-005 Migrate contact and promises | Reduced to the Workbench part. EFS history is read through v_ace_efs_action; only the open promises and contact notes held outside EFS move. |
| RWB-DM-006 Migrate collateral and assets | Reduced to the Workbench part. Collateral, appraisals, NPA assets and sales are read through v_ace_collateral, v_ace_valuation, v_ace_asset, v_ace_npa_asset and v_ace_npa_sale; only listings, case asset links and sale instructions move. |
| RWB-DM-011 Migrate scores and route economics | Reduced to the Workbench part. COLLINS scores are read through v_ace_score; only the expected-return and sale-estimate records the Workbench calculates move. |
| RWB-DM-013 Migrate money and closure | Reduced to the Workbench part. Payments and GL postings are read through v_ace_payment and v_ace_write_off; only proceeds matching and closure records move. |

# 6. Parallel run

Each team runs its spreadsheet and the Workbench side by side for two weeks after its first release. The data steward reconciles daily. The spreadsheet retires when the business lead signs ten clean days.

# 7. Reconciliation and the cut-over check

Counts and balances per data product reconcile to the source within the tolerance under DL25. Breaks are listed for the data steward and cleared before cutover.

The cut-over check is the case list. Every case_list_row.account_key must resolve to a row in v_ace_account for the cut-over business date, and the count of open cases by product and bucket must agree with the view. A key that does not resolve is either a closed account or a key error; both are cleared before go-live, and the result is recorded against reconciliation rule REC-05. No case starts on the Workbench until this check passes.

# 8. Open decisions

| Decision | What is needed |
|---|---|
| DL12 | Which legacy systems are kept, and what the Workbench reads from each. Option A is superseded by D-RCV-35: the read path is the SELECT-only recovery.v_ace_* views, not a direct read of ACE or COLLINS |
| DL29 | Closed: EFS contact history is read through v_ace_efs_action, so no migration decision is needed |
| DL43 | Open with the ACE team lead, needed by 2026-11-21: the ACE team accepts the RWB-ACE-001 scope and dates (14 new ACE tables, 12 new columns). The Tier 2 reads this approach names depend on it |
