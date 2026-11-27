SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD P1 rwb-source-data v3
description: Product requirements for the Recovery Workbench source data service (P1 rwb-source-data) in the 19-service realignment; capabilities, functional and non-functional requirements, data and integration requirements, release slices by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v4.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 1 v4.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v2.docx
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v8/Recovery Workbench FSD P1 Recovery data engine v5.md
service: P1 rwb-source-data
epic: RWB-SVC-P1
wave: 1
decision: D-RCV-60
---

# Recovery Workbench PRD P1 rwb-source-data v3

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD P1 rwb-source-data |
| Document ID | P1-RWB-PRD-v3 |
| Version | 3 |
| Status | Draft |
| Classification | Confidential |
| Date | 27 November 2026 |
| Service | P1 rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epics | EP01 (Epic 1, wave 1); EP02 (Epic 2, wave 2) |
| Schema | `rwb_source_data` |
| REST base | `/api/recovery/source-data/v1` |
| Topic | `rwb.source-data.events.v1` |
| Temporal task queue | `rwb-source-data` |
| Java package | `th.co.scb.ace.workbench.recovery.sourcedata` |
| Product owner role | Product Owner (approval table, section 13) |
| Requirement owner role | Data steward and data product owner |
| Decision | D-RCV-60 (microservice realignment); inherits D-RCV-35 (U1 to U5) and ADR-010 |
| Upstream artifacts | Business Requirements Program v4; Business Requirements Epic 1 v4; Business Requirements Epic 2 v2; FSD P1 Recovery data engine v5; Architecture v5 |
| Upstream requirement IDs | REQ-RDF-001 to REQ-RDF-014; REQ-CWC-001, REQ-CWC-004; REQ-DRI-006, REQ-DRI-008, REQ-DRI-011; REQ-ILG-001 to REQ-ILG-008, REQ-ILG-014; REQ-ACA-006; NFR-001, NFR-007, NFR-008, NFR-009, NFR-013, NFR-014, NFR-015, NFR-018, NFR-020, NFR-021, NFR-022, NFR-023, NFR-025, NFR-026, NFR-027, NFR-033, NFR-034, NFR-035, NFR-039, NFR-040, NFR-042, NFR-046, NFR-047, NFR-049, NFR-051, NFR-052, NFR-053, NFR-054, NFR-059, NFR-064, NFR-067, NFR-068, NFR-070, NFR-077 |
| Upstream acceptance criteria | AC-P1-001-01, AC-ALT-P1-001-01 to -04, AC-EXC-P1-001-01 to -06; AC-P1-002-01, AC-ALT-P1-002-01 to -02, AC-EXC-P1-002-01 to -03; AC-P1-011-01, AC-ALT-P1-011-01 to -03, AC-EXC-P1-011-01 to -02; AC-P1-012-01, AC-ALT-P1-012-01 to -02; AC-P1-013-01, AC-ALT-P1-013-01 to -02, AC-EXC-P1-013-01; AC-P1-014-01, AC-ALT-P1-014-01 to -03, AC-EXC-P1-014-01 to -03; AC-P1-015-01, AC-ALT-P1-015-01 to -02, AC-EXC-P1-015-01 to -04; AC-P1-016-01, AC-ALT-P1-016-01 to -02, AC-EXC-P1-016-01 to -03; AC-P1-017-01, AC-ALT-P1-017-01 to -02, AC-EXC-P1-017-01 to -04; AC-P1-018-01, AC-ALT-P1-018-01 to -03, AC-EXC-P1-018-01 to -05 |
| Generated IDs | CAP-P1-001 to CAP-P1-014; FR-P1-001 to FR-P1-032; NFR-P1-001 to NFR-P1-027; AC-P1-001 to AC-P1-024; JRN-P1-01 to JRN-P1-05; ROL-P1-01 to ROL-P1-13; OQ-P1-01 to OQ-P1-15 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD P1 Recovery data engine v5 (27 November 2026) and the BRD Program v4 / Epic 1 v4 (15 November 2026), realigned to Architecture v5 under D-RCV-60 |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| v2 | 26 November 2026 | D-RCV-60: cross-document changes under the programme directive (R-09177) | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| v3 | 27 November 2026 | D-RCV-60 P1 developer readiness (RD-P1 register) · targeted edits | W8-reqs-security |

## 1.3 Inherited history and ID continuity

The product baseline is FSD P1 Recovery data engine v3. Its history and ID set are carried unchanged; the microservice realignment changes the owner, the read path and the delivery wave, not the requirement substance.

| Version | Date | Change carried from the FSD |
|---|---|---|
| 2 | 28 October 2026 | COLLINS and file loads, load checks, tracker loads, reconciliation to ALS, freshness from the Workbench load |
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 and ADR-010. The module loads no source data: it reads ACE through the 30 `recovery.v_ace_*` views and owns only the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext`. Freshness is stamped in `data_product_load` from `ace_batch_run`, read through `v_ace_batch_status` (EV-26 AceDataReady, EV-27 AceDataLate). The case list reconciles to `v_ace_account`. The data dictionary covers the views and the extension tables; systems of record read "ACE (ingested from X)". The load, load-check, tracker and feed-job functions FEAT-RDF-03 to 10 and FEAT-RDF-22 keep their IDs and are marked removed with their later home. JOB-01 and JOB-09 are retired. |
| 1 (PRD) | 22 November 2026 | First PRD of this family. CAP, FR, NFR, AC and journey IDs are new; the FSD requirement IDs (REQ-RDF-xxx), feature IDs (FEAT-RDF-xx), acceptance criteria IDs (AC-P1-xxx), open question IDs (OQ-P1-xx), data product codes (DP01 to DP14), reconciliation checks (REC-01, REC-02, REC-05), job ID (JOB-04), event IDs (EV-26, EV-27) and message IDs (MSG-P1-001, MSG-P1-002, MSG-P1-003, MSG-P1-004, MSG-P1-012, MSG-P1-019, MSG-P1-020) are preserved character for character |

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v4 | BRD | Source of the business requirements and the non-functional requirements |
| Recovery Workbench Business Requirements Epic 1 v4 | BRD | Source of the Epic 1 requirements the service serves |
| Recovery Workbench Business Requirements Epic 2 v2 | BRD | Source of the Epic 2 requirement (REQ-RDF-014) |
| Recovery Workbench Functional Specifications by Module v8, FSD P1 Recovery data engine v5 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services, one schema and login per service, Kafka, Temporal, no data lake, edge and gateway |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: task queue, workflow kit, event-started work |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, operation, event, job and workflow |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, placeholder and register rules |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-source-data (P1) is the recovery module's single read path to ACE data and the owner of the Workbench records that describe ACE data. It turns "the Workbench reads ACE" into a product: a published, versioned view contract; the extension tables that hold a Workbench decision about an ACE record; the 14 data products with one system of record each; the freshness of every data product from the ACE batch record; P1 reconciliation using rwb-case case keys; the access, masking and catalog position; and the interaction ledger.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-source-data | One deployable with its own API and worker, schema `rwb_source_data`, login, topic `rwb.source-data.events.v1`, task queue `rwb-source-data` and lifecycle | Source data becomes one owned contract instead of a module inside a single deployable |
| The 30-view contract as a published product | 16 Section A views over ACE tables that exist today, 14 Section B views over the RWB-ACE-001 additions, each field in the data dictionary | A change in ACE is absorbed in one place; nobody else reads ACE's tables |
| Freshness as a product behaviour | A stamp per data product from `v_ace_batch_status`, published as AceDataReady and AceDataLate | Every decision states how old its data is |
| Reconciliation as a service duty | REC-01, REC-02 and REC-05 run after the ALS stamp and rwb-case allocation; they produce P1 reconciliation results and do not gate a P1 case-list publish | P3 rwb-case owns the case list and its publication |
| The interaction ledger owner | One ledger for every interaction on a case, owned here | The history of a case is never assembled after the fact |
| Data contract with the ACE team | A versioned contract per data product and view, published | The 30 views are a contract with a named owner, not an accident |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| ACE database, its tables and its backups | REUSE | ACE team |
| ACE ingestion of every source system (ALS, EFS, SCBPDM, CCMS, SVAF, AMIS, RPS, LIT, WIN, GL, COLLINS, NLEADS, EasyApp, Entra ID) | REUSE | ACE team |
| The 30 read-only `recovery.v_ace_*` views and their grant | REUSE, owned here | P1 |
| Sign-in, access check, field masking policy and DoA | REUSE | ACE common sign-in; P4 rwb-access for masking policy |
| Decision record, audit trail, hash chain | REUSE | P7 rwb-decision through the local decision-record library |
| Documents, notices, payments, case and workflow, reporting, agents | REUSE | P5, P6, P8, P3, P9, P10 |
| Source loads, staging tables, load checks, load sign-off (FEAT-RDF-03 to FEAT-RDF-10) | REMOVED from this service | ACE ingestion; RWB-ACE-001 |
| Excel and SharePoint tracker inventory, load and retirement (FEAT-RDF-07 to FEAT-RDF-09) | REMOVED from system scope | Cutover plan (U5) |
| Legacy feed jobs on ADF and Control-M (FEAT-RDF-22), JOB-01 and JOB-09 | RETIRED | None. ACE ingestion; freshness read through the view contract |
| Retention and archive job (JOB-17) | MOVED | P5 rwb-document (the retention class stays declared here as data) |
| Baseline measures and regulatory/reporting extracts (JOB-15) | MOVED | P9 rwb-reporting (this service serves the measure snapshot) |
| Decision log copy to the data lake (JOB-13) | REMOVED | None. No data lake in v5; decision-log ingest is continuous from Kafka in P7 |
| Case list screen and case list API | REUSE, elsewhere | P3 rwb-case owns case-list rows and operations; P1 supplies account-page reads through its contract |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; only rwb-source-data reads the 30 `recovery.v_ace_*` views (ADR-010, ADR-014).
2. The service writes only schema `rwb_source_data`; no cross-schema join, no foreign key into `public` (ADR-014, DP-01).
3. REST is one hop from gateway-bff, with a 2 s timeout; anything longer is a workflow (ADR-020, DP-11).
4. Events are CloudEvents on Kafka with outbox and inbox; topic `rwb.source-data.events.v1`; retry and `.dlt` topics (ADR-015, DP-09, DP-14).
5. Temporal namespace `rwb-recovery`, task queue `rwb-source-data`; Schedules replace Quartz; the shared Quartz tables are not used (ADR-016, DP-10).
6. There is no data lake and no Power BI connection: INT-19 and INT-20 are removed; reporting reads events into rwb-reporting (ADR-018, DP-17).
7. Personal data stays out of events, workflow inputs and logs; masking is applied by this service (Arch v5 slide 45).
8. Dead-letter and replay rules, typed failures and the non-retryable list follow the platform standard (Arch v5 slide 13).

# 3. Personas and roles

Roles only; no person is named anywhere in this document.

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-P1-01 | Data steward and data product owner | One system of record and one owner per data product, freshness and reconciliation they can act on, access rows they can version | JRN-P1-01, JRN-P1-03, JRN-P1-04 |
| ROL-P1-02 | Reference data administrator | A full-file load that is refused whole rather than half applied, with the version in force kept | JRN-P1-04 |
| ROL-P1-03 | Compliance and PDPA officer | Masking that holds by default, a read log that cannot be skipped, retention that states its class | JRN-P1-04 |
| ROL-P1-04 | Security administrator | Role access rows and refusal evidence | JRN-P1-04 |
| ROL-P1-05 | Center of excellence analyst | The catalog, the measures and the reasons behind a break | JRN-P1-03, JRN-P1-05 |
| ROL-P1-06 | Case owner | Case facts read through one contract, and a case history in one ordered sequence | JRN-P1-02, JRN-P1-05 |
| ROL-P1-07 | Team manager | Cases with owners and queues, served by P3 rwb-case on the account facts this service reads from a complete ACE batch | JRN-P1-02 |
| ROL-P1-08 | Phone collector | Contact points with consent and verification state | JRN-P1-02 |
| ROL-P1-09 | Reporting and BI analyst | Reconciliation results, freshness and the six quality measures | JRN-P1-03 |
| ROL-P1-10 | Internal audit | A read of the decision history and the ledger without touching the live log | JRN-P1-05 |
| ROL-P1-11 | Platform administrator | Business-date ready and status, job and reconciliation reruns, an exception queue with a named owner | JRN-P1-01, JRN-P1-03 |
| ROL-P1-12 | Developer | A typed, sourced and owned field for every view and table, and a build that fails on a direct ACE read | JRN-P1-05 |
| ROL-P1-13 | ACE team lead (external) | A versioned data contract per view and the scope of the ACE additions | JRN-P1-05 |

Non-human actors: the bank scheduler (Airflow) calling the business-date contract; the outbox relay; the Temporal worker; the consumers of the published events. The bank Airflow sits outside the 19 services and calls APIs only (Arch v5 slide 32).

# 4. User journeys

## 4.1 Current state (as built in the monolith)

1. Eleven Workbench tables are loaded nightly from ALS, EFS, CCMS and SVAF, with nine more tables to load them.
2. Data quality rules run on every load; a refused load keeps the previous load in use.
3. Freshness is inferred from the Workbench load, not from the source.
4. Teams keep their own lists in Excel and SharePoint.
5. A developer who needs a field goes looking in the source system or in a copy.

Consequence: two copies of the same account, two answers, and an owner for neither.

## 4.2 Target state (this product)

### JRN-P1-01 Business date made ready (unattended, daily)

1. ACE finishes ingesting a source system and records one `ace_batch_run` row per source and business date.
2. The bank scheduler calls the business-date ready operation for the date; the call is idempotent on the date and answered 202.
3. The service reads `v_ace_batch_status`, writes or updates the `data_product_load` stamp of every data product fed by the completed source, and publishes AceDataReady.
4. AceDataReady starts the daily case run in rwb-case, payment matching and booking confirmation in rwb-payment, deviation screening in rwb-deviation, and the reconciliation in this service.
5. If a product's expected-by time passes without its batch, or the batch fails, AceDataLate is published at 05:30 and the product is flagged STALE; the banner and the alarm follow.
6. Fallback while ACE ingestion is still on Control-M at go-live: the service polls the ACE batch record instead of being called.

### JRN-P1-02 Case facts and reconciliation (daily, before 07:00)

1. P1 starts reconciliation as a child of AceIngestCheck after the ALS stamp; REC-01 waits for rwb-case allocation until caselist.allocation.wait.until.
2. P1 writes no case-list row. P3 rwb-case owns case-list data and operations; P1 reads required ACE account facts through its account-page contract.
3. A REC-01 or REC-02 result is PASS only when its absolute variance percent is at most recon.tolerance.pct (version 1, 0.00); otherwise it is BREAK, MSG-P1-012 and the Reconciliation break alert are raised, and P1 sets no publish status. The effect of a BREAK on the rwb-case case list is Pending, owner Solution architect with the data lead (NEW-GAP-X3).
4. P3 rwb-case serves the case list. P1 does not publish case-list rows, status or checks.
5. Every screen read of a personal field writes one PII access log entry.

### JRN-P1-03 Reconciliation and freshness reviewed (daily, data steward)

1. The steward opens the data quality view: reconciliation results by check and product group, the freshness of the 14 data products, and the six quality measures.
2. Each break carries its reason and its owner; an orphan business key names the row that has no ACE record and is never deleted or changed.
3. A held publish is cleared by rerunning the reconciliation after the cause is fixed; the result and the rerun are recorded.

### JRN-P1-04 Catalog, access and retention maintained (on change, versioned)

1. The steward defines the 14 data products, their systems of record ("ACE (ingested from X)" or the Workbench) and their owners; the load is refused whole if any row is missing or ambiguous.
2. The steward sets read access per role and data product; field masking policy comes from rwb-access; a personal field with no masking row is returned masked.
3. The compliance officer sets the retention class per data product and recovery table; the archive run itself belongs to rwb-document.
4. Every change is a new version with a valid-from date, an author and an approver, and writes a decision record.

### JRN-P1-05 Field contract and ledger read (developer and auditor)

1. A developer queries the data dictionary for an object and field: field ID, data type, physical type, source system, source field, data product, refresh cycle and owner role.
2. A view field names its ACE source column; an extension field names the Workbench as its source; the ACE table name appears only as the source field.
3. A build that adds a field without a dictionary entry, reads a `public` table directly, writes a view, or adds a foreign key into ACE fails the pipeline.
4. The ACE team signs a versioned data contract per view; a change to a view is a contract change, not a silent fix.
5. An auditor reads a case's ledger in one ordered sequence and the decision history through the reporting and decision paths, never against the live log store.

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour. Priorities follow the BRD: Must is needed for the epic to release; Should is planned in the epic.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Wave | FSD features |
|---|---|---|---|---|---|---|
| CAP-P1-001 | Read-only ACE view contract and boundary | Source data has one copy and one read path; a wrong read fails the build instead of being found in test | REQ-RDF-001, REQ-RDF-002, REQ-RDF-003, REQ-RDF-004, REQ-DRI-006 | Must | 1 | FEAT-RDF-01 (A2.1) |
| CAP-P1-002 | Workbench extension tables | A Workbench decision about an ACE record is held once, by business key, without touching ACE | REQ-RDF-001, REQ-RDF-004, REQ-CWC-004 | Must | 1 | FEAT-RDF-01 (A2.1) |
| CAP-P1-003 | 14 data products with one system of record and one owner | Every number on every screen has one named source | REQ-RDF-001, REQ-RDF-011 | Must | 1 | FEAT-RDF-02 (A2.2) |
| CAP-P1-004 | Freshness stamp and the business-date gate | Every decision states the business date and load time of the data it used; a late batch is visible, not silent | REQ-RDF-009 | Must | 1 | FEAT-RDF-14 (A2.14) |
| CAP-P1-005 | Reconcile P3 case keys to ACE | P1 records REC-01, REC-02 and REC-05 results using the ACE business date and rwb-case keys | REQ-RDF-007, REQ-RDF-008 | Must | 1 | FEAT-RDF-11 (A2.11) |
| CAP-P1-006 | Reconciliation, freshness and quality output | A break or a stale product is seen by the person who can act on it, with its reason | REQ-RDF-008 | Must | 2 | FEAT-RDF-12 (A2.12) |
| CAP-P1-007 | Retired from P1 by RD-P1-024 | P3 rwb-case owns case-list publication and status; P1 creates no publish status or case-list check | REQ-RDF-007 | Retired | P3 | RD-P1-024 |
| CAP-P1-008 | Access control and masking per data product | Personal data is read only by the roles that need it, and every read is logged | REQ-RDF-010, REQ-ACA-006 | Must | 1 | FEAT-RDF-15 (A2.15) |
| CAP-P1-009 | Data dictionary and catalog entry per data product | Every field is typed, sourced and owned; a data contract with ACE can be agreed field by field | REQ-RDF-011, REQ-DRI-011 | Must | 1 | FEAT-RDF-16 (A2.16) |
| CAP-P1-010 | Retired from P1 by RD-P1-024 | P3 rwb-case owns case-list rows and operations; P1 supplies account-page reads | REQ-RDF-007, REQ-CWC-001 | Retired | P3 | RD-P1-024 |
| CAP-P1-011 | Retention class per data product and table | The store holds what the policy allows and nothing older; ACE data stays under ACE's retention | REQ-RDF-013 | Should | 1 | FEAT-RDF-17 (A2.17) |
| CAP-P1-012 | Interaction ledger | The history of a case is written as it happens and read in one ordered sequence | REQ-ILG-001, REQ-ILG-002, REQ-ILG-003, REQ-ILG-004, REQ-ILG-005, REQ-ILG-006, REQ-ILG-007, REQ-ILG-008, REQ-ILG-014 | Must | 1 | Epic 1 RWB-E1-066, RWB-E1-067, RWB-E1-068; DP-18 |
| CAP-P1-013 | Stage 2 data products for contracts, plans and treatments | The plan and treatment data products exist before the first treatment goes live | REQ-RDF-014 | Must | 2 | FSD P1 A2.2 (DP04), Epic 2 |
| CAP-P1-014 | Portfolio measure snapshot for reporting | The baseline is taken from checked data, once, and is frozen | REQ-RDF-012 | Must | 1 | FEAT-RDF-19 (A2.19) |

## 5.1 Capabilities not carried into the product

| Capability | Status | Later home |
|---|---|---|
| Load account and arrears daily from ALS (FEAT-RDF-03) | Removed | ACE ingestion; read through `v_ace_account` and `v_ace_payment` |
| Load collections status and contact history from EFS (FEAT-RDF-04) | Removed | ACE ingestion; read through `v_ace_efs_action`, `v_ace_efs_action_code`, `v_ace_efs_assignment` |
| Load collateral records from CCMS (FEAT-RDF-05) | Removed | ACE ingestion; read through `v_ace_collateral`, `v_ace_collateral_detail`, `v_ace_asset` |
| Load appraisal values from SVAF (FEAT-RDF-06) | Removed | ACE ingestion; read through `v_ace_valuation`; the Workbench acceptance sits in `valuation_ext` |
| Inventory the Excel and SharePoint trackers (FEAT-RDF-07) | Removed from system scope | Cutover plan |
| Load the tracker data into the data store (FEAT-RDF-08) | Removed from system scope | Cutover plan |
| Retire a local tracker copy (FEAT-RDF-09) | Removed from system scope | Cutover plan |
| Run data quality rules on every load (FEAT-RDF-10) | Removed | ACE ingestion; the daily gate moves into CAP-P1-004 |
| Copy the decision log to the data lake (FEAT-RDF-20) | Removed | No data lake in v5; decision-log ingest is continuous from Kafka in rwb-decision (GAP-1499; ASM-2617) |
| Run legacy feed jobs on ADF and Control-M (FEAT-RDF-22) | Removed | ACE ingestion; JOB-01 and JOB-09 retired |

# 6. Functional requirements

Every requirement is specific and testable. The FSD requirement column keeps the trace to the source. Priorities follow the BRD.

| FR ID | Requirement | CAP | BR | FSD REQ | Priority | Wave |
|---|---|---|---|---|---|---|
| FR-P1-001 | The service SHALL read ACE data only through the 30 read-only `recovery.v_ace_*` views. A read of a `public` table, a write to any view or any ACE table, and a constraint in schema `rwb_source_data` that references a table outside it SHALL fail the build. | CAP-P1-001 | REQ-RDF-001, REQ-DRI-006 | REQ-RDF-001 | Must | 1 |
| FR-P1-002 | The service SHALL provide the 16 Section A views over the ACE tables that exist today, in the view families account/payment/plan, customer/contact/relations, collateral/asset, collections activity and reference, shipped with the RWB-E1-069 migration; each view SHALL compile against the ACE schema and pass the boundary conformance test. | CAP-P1-001 | REQ-RDF-002, REQ-RDF-003, REQ-RDF-004 | REQ-RDF-002, REQ-RDF-003, REQ-RDF-004 | Must | 1 |
| FR-P1-003 | The service SHALL provide the 14 Section B views over the RWB-ACE-001 additions when those additions land, and until then SHALL keep every feature that needs a Section B view behind its feature flag; a Section B migration applied before its ACE table exists SHALL fail and create no view. | CAP-P1-001 | REQ-RDF-004 | REQ-RDF-004 | Must | 1 |
| FR-P1-004 | The service SHALL expose, for every table and view it reads or owns, one data dictionary entry per field with field ID, data type, physical type, source system, source field, data product, refresh cycle and owner role, covering 122 objects and 1,366 fields; a field without an entry SHALL fail the build. | CAP-P1-009 | REQ-RDF-011 | REQ-RDF-011 | Must | 1 |
| FR-P1-005 | The service SHALL return a text date in ACE as a date and a Y/N flag as a boolean, and SHALL return NULL rather than fail when the source value cannot be converted. | CAP-P1-001 | REQ-RDF-002 | REQ-RDF-002 | Must | 1 |
| FR-P1-006 | The service SHALL never return a customer identification number in clear; the view SHALL expose only a masked value and the last four digits. | CAP-P1-008 | REQ-RDF-010 | REQ-RDF-010 | Must | 1 |
| FR-P1-007 | The service SHALL hold each Workbench decision about an ACE record in one extension table row, 1:1 with the ACE record by business key, with no copy of an ACE column and no foreign key into ACE. | CAP-P1-002 | REQ-RDF-001 | REQ-RDF-001 | Must | 1 |
| FR-P1-008 | The service SHALL hold on `party_ext`, keyed by the ACE person key: vulnerable, deceased override, bankruptcy and fraud flags. | CAP-P1-002 | REQ-CWC-004, REQ-RDF-001 | REQ-RDF-001 | Must | 1 |
| FR-P1-009 | The service SHALL hold on `contact_point_ext`, keyed by the ACE contact key with its contact type: consent given and when, when last verified, consecutive failed attempts and the row's source. | CAP-P1-002 | REQ-RDF-003, REQ-ILG-003 | REQ-RDF-003 | Must | 1 |
| FR-P1-010 | The service SHALL hold on `account_ext`, keyed by the ACE account key, the open-dispute flag that drives an entry exclusion. | CAP-P1-002 | REQ-CWC-004 | REQ-RDF-001 | Must | 1 |
| FR-P1-011 | The service SHALL hold on `valuation_ext`, keyed by the ACE appraisal key: acceptance, when accepted, who accepted, the panel valuer, the stale flag and the appraisal age in days; the function that writes the flag and the age is open (GAP-1509; ASM-2627). | CAP-P1-002 | REQ-RDF-004 | REQ-RDF-004 | Must | 1 |
| FR-P1-012 | The service SHALL name 14 data products, each with exactly one system of record written as an exact match to `^ACE \(ingested from [^)]+\)$`, as "Recovery Workbench", as one sentence of at most 200 characters that contains both "ACE (ingested from " and "Recovery Workbench", or as a text that starts with "Recovery Workbench, with " and contains "ACE" (all four forms are case sensitive), one owner role and one named owner, one refresh cycle and, for a source-fed product, its expected-by time. | CAP-P1-003 | REQ-RDF-001 | REQ-RDF-001 | Must | 1 |
| FR-P1-013 | The service SHALL refuse a catalog load whole when a product is missing, a product names two systems of record, a product names a bare source system or a system of record that matches none of the forms of FR-P1-012, or a product has no owner; the version in force SHALL stay in force. | CAP-P1-003 | REQ-RDF-001, REQ-RDF-011 | REQ-RDF-011 | Must | 1 |
| FR-P1-014 | The service SHALL write the freshness stamp of each data product from the ACE batch record read through the batch-status view: product, source system, business date, source time, load time, status LOADED or STALE, when the product was flagged stale, and the count of repeated reads of the same completed batch that were ignored. | CAP-P1-004 | REQ-RDF-009 | REQ-RDF-009 | Must | 1 |
| FR-P1-015 | The service SHALL carry, for a product fed by more than one source, the oldest business date among its sources and SHALL mark the product STALE while any of its sources is late. | CAP-P1-004 | REQ-RDF-009 | REQ-RDF-009 | Must | 1 |
| FR-P1-016 | EV-26 is published once per source system and business date with status COMPLETED; downstream daily work starts only for sourceSystem ALS. The service reads freshness from v_ace_batch_status and never infers it from a row count, file or view data date. | CAP-P1-004 | REQ-RDF-009 | REQ-RDF-009 | Must | 1 |
| FR-P1-017 | The service SHALL answer a business-date ready call for a date idempotently and SHALL report the date's state as RUNNING, DONE or LATE for the calling scheduler, and SHALL keep polling the ACE batch record as the fallback while ACE ingestion is scheduled outside the bank scheduler. | CAP-P1-004 | REQ-RDF-009, REQ-DRI-008 | REQ-RDF-009 | Must | 1 |
| FR-P1-018 | The service SHALL write REC-01 and REC-02 results for the ACE business date and perform REC-05 on P1-owned keys and rwb-case case_account/case_party keys. REC-01 waits for rwb-case allocation; the paged rwb-case key-list path is Pending, owner rwb-case service owner, tracked as NEW-GAP-B2. | CAP-P1-005 | REQ-RDF-007 | REQ-RDF-007 | Must | 1 |
| FR-P1-019 | The service SHALL take every reconciliation tolerance from versioned reference data and SHALL treat zero unexplained variance as the target; a tolerance change SHALL take effect from its valid-from date without a code release. | CAP-P1-005 | REQ-RDF-007 | REQ-RDF-007 | Must | 1 |
| FR-P1-020 | The service SHALL list every REC-05 orphan with its table and key for the data steward and, where the row is missing in ACE, for the ACE team, and SHALL never delete or change a Workbench record because of an orphan. | CAP-P1-005 | REQ-RDF-007, REQ-RDF-008 | REQ-RDF-007 | Must | 1 |
| FR-P1-021 | Withdrawn from P1 by RD-P1-024. P3 rwb-case owns case-list publication, publish status and case-list checks. | CAP-P1-007 | REQ-RDF-007 | REQ-RDF-007 | Retired | P3 |
| FR-P1-022 | Withdrawn from P1 by RD-P1-024. P3 rwb-case owns case-list rows and operations; P1 creates no case_list_row. | CAP-P1-010 | REQ-RDF-007, REQ-CWC-001 | REQ-RDF-007 | Retired | P3 |
| FR-P1-023 | The service SHALL produce, for the data steward, the reconciliation results by check and product group, the freshness of all 14 data products and the six quality measures of completeness, validity, timeliness, accuracy, uniqueness and referential completeness, each break carrying its reason. | CAP-P1-006 | REQ-RDF-008 | REQ-RDF-008 | Must | 2 |
| FR-P1-024 | The service SHALL control read access to each data product by role, SHALL return a personal field masked where the role has no unmasked masking row, and SHALL log a refused read with the role and the product. | CAP-P1-008 | REQ-RDF-010, REQ-ACA-006 | REQ-RDF-010 | Must | 1 |
| FR-P1-025 | The service SHALL write one PII access log entry per read of a personal field, with the reader, the data product, the case and the time, and SHALL refuse the read rather than return a personal field when the access log cannot be written. | CAP-P1-008 | REQ-RDF-010, REQ-ACA-006 | REQ-RDF-010 | Must | 1 |
| FR-P1-026 | The service SHALL serve the catalog entry per data product: definition, owner role, system of record, the views and tables behind it, refresh cycle, expected-by time, retention class, the reconciliation checks that apply and the access rows, with the field list carrying its personal-data tag. | CAP-P1-009 | REQ-RDF-011 | REQ-RDF-011 | Must | 1 |
| FR-P1-027 | The service SHALL hold and publish a versioned data contract with the ACE team for each data product and view, and SHALL refuse a contract update that names an unknown data product or marks a view as Workbench. | CAP-P1-009 | REQ-RDF-011, REQ-DRI-011 | REQ-RDF-011 | Must | 1 |
| FR-P1-028 | The service SHALL require a retention class per data product and recovery table, SHALL refuse a retention row that names a read-only ACE view or the decision log, and SHALL apply no archive of its own; the archive run belongs to rwb-document and ACE applies its own retention. | CAP-P1-011 | REQ-RDF-013 | REQ-RDF-013 | Should | 1 |
| FR-P1-029 | The service SHALL write to one interaction ledger every interaction on a case with case, event, timestamp, actor and source, and with channel, whom or what was reached and outcome where the interaction had one, SHALL write one entry when the same event arrives twice with the same key and count the repeat, and SHALL read a case's ledger back in one ordered sequence filterable by channel, actor and date range. | CAP-P1-012 | REQ-ILG-001, REQ-ILG-002, REQ-ILG-003, REQ-ILG-006, REQ-ILG-007 | REQ-RDF-001 | Must | 1 |
| FR-P1-030 | The service SHALL write every ledger-eligible action the Workbench takes on a case to the ledger as it happens, SHALL mask personal data in the ledger by the same role rules as the case record, and SHALL raise an incident rather than discard an entry when a ledger write fails. Reads go to the access log only. The screening agent receives masked call-note summaries. | CAP-P1-012 | REQ-ILG-005, REQ-ILG-008, REQ-ILG-014 | REQ-RDF-010 | Must | 1 |
| FR-P1-031 | The service SHALL hold the Stage 2 data products for treatment and guarantee as dated read-only copies built from their owning services’ REST changed-window reads before the first treatment goes live, while the live treatment and guarantee records stay with their owning services. Contract and plan facts are read live from ACE by P1. | CAP-P1-013 | REQ-RDF-014 | REQ-RDF-014 | Must | 2 |
| FR-P1-032 | The service SHALL serve the portfolio measure snapshot for a business date whose ACE batches are complete, covering cases by route, age and queue, realized recovery, time in stage and turnaround per route, from definitions in force; the publication of the measures belongs to rwb-reporting. | CAP-P1-014 | REQ-RDF-012 | REQ-RDF-012 | Must | 1 |
| FR-P1-033 | The service SHALL provide a paged account-page read of ACE account facts, published in RWB-P1-E1015-CON and built by RWB-P1-E1002-APP, which rwb-case uses to build the case list that it owns. Path and maximum keys per call: Pending, owner Solution architect, tracked as GAP-3274 (NEW-GAP-B3); RD-P1-060 publishes a separate single-account read. | CAP-P1-001 | REQ-CWC-001 | REQ-CWC-001 | Must | 1 |

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3 and the BRDs. A target marked open is carried as an open question, never as a value.

| NFR ID | Requirement | Target | BR | Priority | Test |
|---|---|---|---|---|---|
| NFR-P1-001 | A read through the view contract answers inside the user's wait under the busiest-hour load, including reads where ACE and recovery data are joined. | Under 2 seconds at the 95th percentile | NFR-008, NFR-009 | Must | Performance test in SIT |
| NFR-P1-002 | P1 freshness is available from the latest stamped data-product business date; the case list is owned and served by P3 rwb-case. | Confirm the stamped date and alert under the P1 freshness contract | NFR-013 | Must | Hold the batch in SIT; confirm the date and the alert |
| NFR-P1-003 | The service holds no load window: a late ACE batch delays the output and raises an alert, and never starts a load, a catch-up job or a staging table. | Visible as soon as the ACE batch completes; no service lag | NFR-015 | Must | Hold and release the batch |
| NFR-P1-004 | The ACE batch for the business date is complete when the service reads it. | 99 percent of days | NFR-014 | Must | Freshness report over a month |
| NFR-P1-005 | P1 writes daily reconciliation results for ACE and rwb-case keys; it does not publish or hold the case list. | No unexplained variance in P1 reconciliation results | NFR-018 | Must | Reconciliation run with a seeded difference |
| NFR-P1-006 | A reconciliation break is cleared within one day of being raised. | 100 percent | NFR-018 | Must | Break list ageing over a month |
| NFR-P1-007 | The service is available during business hours and outside them, when the batch and the reconciliation run. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window | NFR-020, NFR-021 | Must | Availability read monthly from monitoring |
| NFR-P1-008 | The service inherits the ACE recovery point and recovery time. | The ACE recovery point objective and recovery time objective | NFR-022, NFR-023 | Must | Failover and restore test before the first release |
| NFR-P1-009 | Every read of a personal field is logged. | 100 percent of personal field reads | NFR-042 | Must | Access log reconciliation against reads |
| NFR-P1-010 | A personal field with no masking row for the role is returned masked, and the identification number never leaves in clear. | Masked by default; masked and last four only | NFR-039, NFR-040 | Must | Masking matrix test across roles |
| NFR-P1-011 | Each consumer and each screen receives only the personal data it needs. | Data minimization per consumer | NFR-040 | Must | Contract review per consumer |
| NFR-P1-012 | Data is encrypted at rest and in transit, and secrets live in the key store. | Encrypted; no secret in code, configuration or prompt | NFR-052, NFR-053 | Must | Security review and secret scan |
| NFR-P1-013 | Staff authenticate with single sign-on and multi-factor authentication; non-human callers use their own service identity. | Entra ID single sign-on with multi-factor; service identities | NFR-049, NFR-051 | Must | Sign-in and identity test |
| NFR-P1-014 | The recovery service identity holds read rights on the views and its own schema and nothing else: no insert, update, delete or truncate on a view or on any ACE table. | Read-only on views; no data change outside `rwb_source_data` | NFR-054 | Must | Permission test in SIT |
| NFR-P1-015 | The build fails on a direct ACE table read, a write to a view, a foreign key into ACE, and a field without a dictionary entry. | Build fails on any violation | NFR-054 | Must | Negative pipeline test |
| NFR-P1-016 | The build blocks a change carrying a secret, personal data in code, tests or logs, or an unapproved dependency. | Pipeline checks pass | NFR-054 | Must | Pipeline run with a seeded violation |
| NFR-P1-017 | Every decision records the product, business date, load time and status of each data product it read. | Every decision | NFR-033, NFR-034 | Must | Decision record inspection |
| NFR-P1-018 | Every decision is written to an append-only, hash-chained log whose chain is checked daily and whose break is reported the same day. | Reproducible; daily check | NFR-033, NFR-035 | Must | Chain break drill |
| NFR-P1-019 | Logs, traces and metrics are produced for the freshness and reconciliation work, and every scheduled or triggered job has a run book, monitoring and an alert. | Every job covered | NFR-064, NFR-067 | Must | Observability review |
| NFR-P1-020 | A failing interface or job raises an alert to a named owner. | Within 15 minutes | NFR-068 | Must | Alert drill |
| NFR-P1-021 | A call is one hop with a 2 s timeout; a failure is retried on a schedule and, after three retries, moves to an exception queue with a task for a named owner; events that cannot be processed go to the dead-letter topic and are replayed. | One hop; 2 s timeout; three retries then the exception queue | NFR-025, NFR-026 | Must | Failure injection |
| NFR-P1-022 | The interaction ledger holds every interaction within its retention period and reads one case history inside the user wait. | One case history under 2 seconds with the ledger at its 2031 size; about 36 GB for the decision log and the ledger by 2031 | NFR-070, NFR-007 | Must | Volume test at the 2031 size |
| NFR-P1-023 | The service carries the stated volume: the accounts at 90 or more days past due, the monthly inflow and the open case count. | 28,119 accounts in the active inventory; 3,110 new accounts a month; about 23,600 open cases at go-live and 26,500 at the end of 2027 | NFR-001 | Must | Volume test with data at the stated volume |
| NFR-P1-024 | Workbench data stays in the bank's own cloud tenancy in the agreed region, and every data product carries a data classification that sets its handling. | SCB Azure, Southeast Asia; classification applied per data product | NFR-046, NFR-047 | Must | Tenancy and classification review |
| NFR-P1-025 | A failed ledger or decision write raises an incident and no entry is discarded. | No silent gaps | NFR-077 | Must | Write failure drill |
| NFR-P1-026 | Screen labels, validation messages and error messages served with this service's operations are available in Thai and in English. | Every label and message in Thai and English | NFR-059 | Must | Label and message review |
| NFR-P1-027 | A production release rolls back by redeploying the previous tag, and each service carries its own migration sequence in its own schema. | Rollback by previous tag; per-service migration | NFR-027 | Must | Rollback rehearsal |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_source_data`. Every table carries the seven standard record columns of the platform library. Retention is stated by class; the periods are open (GAP-1510; ASM-2628).
All 14 data products (DP01 to DP14) are owned by this service for Epic 1, and the freshness stamp stays in this service for Epic 1. Each product's owner role and named owner are catalog fields (FR-P1-012); no owner name is set in this document (GAP-3154).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `party_ext` | Extension table (1:1 with an ACE person) | `person_key`; vulnerable, deceased override, bankruptcy, fraud flag | [PII] | Workbench decision about an ACE customer | Workbench record class; archived by rwb-document |
| `contact_point_ext` | Extension table (1:1 with an ACE contact point) | `contact_key`, `contact_type`; consent given and when, verified at, failed count, source | [PII] | Workbench decision about an ACE contact point | Workbench record class; archived by rwb-document |
| `account_ext` | Extension table (1:1 with an ACE account) | `account_key`; dispute open | [CONFIDENTIAL] | Workbench decision about an ACE account | Workbench record class; archived by rwb-document |
| `valuation_ext` | Extension table (1:1 with an ACE appraisal) | `valuation_key`; accepted, accepted at, accepted by, panel valuer, stale flag, age in days | [CONFIDENTIAL] | Workbench decision about an ACE appraisal | Workbench record class; archived by rwb-document |
| `data_product` | Versioned reference | `product_code` (DP01 to DP14), name, definition, system of record, owner role, owner, refresh cycle, expected by, valid from | [CONFIDENTIAL] | Workbench reference data | Versioned; superseded versions kept |
| `data_product_access` | Versioned reference | `role_code`, `can_read`, valid from | [CONFIDENTIAL] | Workbench reference data | Versioned; superseded versions kept |
| `data_product_load` | Transaction | `product_code`, `source_system`, `business_date`, source time, load time, status, when flagged stale, duplicate count | [CONFIDENTIAL] | ACE batch record through the batch-status view | Workbench record class |
| `data_contract` | Versioned reference | Versioned contract per data product and view. Fields: Not specified in the source documents (GAP-1512; ASM-2630) | [CONFIDENTIAL] | Workbench reference data | Versioned; superseded versions kept |
| `reconciliation_result` | Transaction | Check code (REC-01, REC-02, REC-05), product group, business date, counts, balance sums, variance, variance percent, result | [CONFIDENTIAL] | Workbench computation | Workbench record class |
| `case_list_row` | Retired from P1 by RD-P1-024; dictionary history only, table not created | P3 rwb-case owns case-list data and operations | Not a P1 data asset | P3 case data | Not created in P1 |
| `interaction` | Ledger | Case number, event, timestamp, actor, source, channel, whom or what was reached, outcome | [PII] | Every interaction on a case | Its own retention period, set independently of the decision log (open, NFR-075) |
| `efs_ledger_outcome` | Ledger intake rule | Fields: Not specified in the source documents (GAP-1512; ASM-2630) | [PII] | ACE collections activity handed to the ledger | Its own retention period (open) |
| `dp_treatment` | Dated read-only copy (data product DP04) | Fields: Not specified in the source documents (GAP-1512; ASM-2630) | [SENSITIVE_FINANCIAL] | Built from events; live records stay with rwb-treatment | Workbench record class |
| `dp_guarantee_claim` | Dated read-only copy (data product DP04) | Fields: Not specified in the source documents (GAP-1512; ASM-2630) | [SENSITIVE_FINANCIAL] | Built from events; live records stay with rwb-guarantee | Workbench record class |
| `sys_objects` | Metadata | Object name, subject area, data product, system of record | [CONFIDENTIAL] | Workbench metadata | Versioned |
| `sys_fields` | Metadata | Field ID, source system, source field, personal-data flag | [CONFIDENTIAL] | Workbench metadata | Versioned |
| `sys_field_version` | Metadata | Versioned field metadata | [CONFIDENTIAL] | Workbench metadata | Versioned |

Not carried: `lake_copy_watermark`. It is a legacy table with no target: the data lake is removed and the decision-log copy no longer exists in this service.

## 8.2 Data read but not owned

The 30 `recovery.v_ace_*` views are read-only and owned by this service as a contract. The ACE tables behind them are owned by the ACE team and retained by ACE.

| View family | Section | Views | Classification of the data read |
|---|---|---|---|
| Account, payment, plan | A | `v_ace_account`, `v_ace_payment`, `v_ace_plan`, `v_ace_bucket_log` | [SENSITIVE_FINANCIAL] |
| Customer and contact | A | `v_ace_customer`, `v_ace_contact`, `v_ace_ca_relation`, `v_ace_aa_relation` | [PII] |
| Collateral and asset | A | `v_ace_collateral`, `v_ace_asset` | [CONFIDENTIAL] |
| Collections activity | A | `v_ace_efs_action`, `v_ace_efs_action_code`, `v_ace_efs_assignment` | [PII] |
| Reference | A | `v_ace_product`, `v_ace_branch`, `v_ace_holiday` | [CONFIDENTIAL] |
| Batch record | B | `v_ace_batch_status` | [CONFIDENTIAL] |
| Collateral, valuation, NPA | B | `v_ace_valuation`, `v_ace_collateral_detail`, `v_ace_npa_asset`, `v_ace_npa_sale` | [SENSITIVE_FINANCIAL] |
| Legal and delivery | B | `v_ace_lawsuit`, `v_ace_hearing`, `v_ace_pod` | [CONFIDENTIAL] |
| Money, score, party product | B | `v_ace_write_off`, `v_ace_score`, `v_ace_party_product` | [SENSITIVE_FINANCIAL] |
| Treatment, signature, access | B | `v_ace_credit_decision`, `v_ace_esign`, `v_ace_iam_group` | [CONFIDENTIAL] |

Counts: 16 Section A views with 177 fields and 14 Section B views with 127 fields, over 92 tables with 1,062 fields, of which 49 fields sit on the four extension tables; 122 objects and 1,366 fields in total.

## 8.3 Field-level requirements for personal and financial data

| Field | Meaning | Classification | Requirement |
|---|---|---|---|
| `v_ace_customer.cif_no` | Customer number | [PII] | Masked unless the role holds an unmasked masking row |
| `v_ace_customer.first_name`, `last_name` | Customer name | [PII] | Masked by default |
| `v_ace_customer.date_of_birth` | Date of birth | [PII] | Masked by default |
| `v_ace_customer.id_no_masked` | Identification number masked to the last four | [PII] | The only identity value the views expose |
| `v_ace_contact.contact_value` | Full phone, email or address, for notices and calls | [PII] | Returned in full only where a masking row for the role allows it |
| `v_ace_contact.contact_value_masked` | Display mask of the contact value | [PII] | Default display |
| `party_ext.vulnerable` and the other extension flags | Vulnerability, deceased override, bankruptcy, fraud | [PII] | Read access by role; every read logged |
| `v_ace_account.total_balance`, `days_past_due` | Balance and arrears | [SENSITIVE_FINANCIAL] | Read access by role; no financial value in an event |
| `case_list_row.total_balance`, `days_past_due` | Retired P1 fields; P3 owns case-list values | Not classified as a P1 table field in this PRD | P3 response handling applies | Not carried in a P1 event |
| `reconciliation_result` counts, sums and variance | Portfolio position | [CONFIDENTIAL] | Aggregate only; no account-level personal data |

## 8.4 Data rules

1. A source value a business person may change is a versioned data row read at run time, never a constant in code.
2. An extension table holds a Workbench decision, never a copy of an ACE column.
3. A link to an ACE record is a business-key column of type `varchar(255)` with no foreign key.
4. A personal field is not returned when the access log cannot be written.
5. ACE data is retained by ACE; the service archives nothing of its own.

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| ACE database, ACE tables behind the 30 views | In | SQL, read-only views, SELECT only, statement timeout | ACE team (tables); this service (views) | The only path to ACE data. No direct `public` read, no DML |
| Bank scheduler (Airflow) | In and out | REST, one hop, mutual TLS with client credentials | Bank platform team or Recovery (open: GAP-1513; ASM-2631) | Business-date ready (answered 202, idempotent on the date) and business-date status (RUNNING, DONE, LATE); the scheduler never reads a schema |
| gateway-bff | In | REST composite route, one hop, 2 s timeout | Platform edge (RWB-PLT-EDGE) | Customer, account, collateral and payment reads, freshness, data-product records; the composite route joins this service's answer with rwb-case |
| rwb-case (P3) | In and out | Temporal activity and REST | P3 | Activity to list eligible accounts for a business date and to snapshot a page for measures; the case account and party keys for reconciliation (path Pending, NEW-GAP-B2) and the case facts for the ledger |
| rwb-payment (P8) | In | Temporal activity | P8 | Payments for a business date |
| rwb-valuation (S1) | In | REST | S1 | Collateral and appraisals; the writer of the appraisal stale flag is open (GAP-1509; ASM-2627) |
| rwb-access (P4) | In | REST, cached | P4 | Authorise, role scope and field masking policy. Masking rows belong to rwb-access (GAP-1501; ASM-2619) |
| rwb-deviation (S8) | Out | REST | S8 | Party flags for screening |
| rwb-agent (P10) | Out | REST tool call, read-only | P10 | Case facts as a tool, masked |
| rwb-document (P5) | Out | REST and a schedule in its own service | P5 | Retention class handed over; the archive run is rwb-document's (GAP-1500; ASM-2618) |
| rwb-decision (P7) | Out | Kafka, decision-record library and the shared decision-record topic | P7 | One record per decision, with the inputs snapshot of data-product freshness |
| rwb-reporting (P9) | Out | Temporal activity and events | P9 | The measure snapshot; the measures, snapshots and regulatory extracts are published by P9 (GAP-1499; ASM-2617) |
| Kafka topic `rwb.source-data.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, retry and dead-letter topics, keyed by business date | This service | AceDataReady and AceDataLate; consumers rwb-case, rwb-payment, rwb-deviation, rwb-writeoff, and the gateway banner for the late alarm |
| ACE audit and PII logging path (Kafka to the SOC) | Out | Kafka through the ACE path | ACE common | Every audit and personal-data access entry |
| Data lake and Power BI (INT-19, INT-20) | Removed | None | None | Removed in v5; no extract leaves this service (GAP-1499; ASM-2617) |
| Cutover plan (trackers) | Out of scope | None | Programme | Tracker retirement is a cutover activity, not a product behaviour |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| Who owns the bank's scheduler DAGs, where the scheduler runs, and when the ACE ingestion chain moves off the current scheduler? | Solution architect with the bank platform team | Decides whether the business-date ready call or the poll is the live path at go-live (GAP-1513; ASM-2631) |
| Is the data-late alarm published at 05:30 by this service on every business date, or only when a cut-off is missed? | Solution architect | Sets the alert volume and the banner behaviour |
| Which service serves the job monitor and data-quality screens after the reporting move? | Solution architect | Both screens are first-in here in the FSD and in reporting in the architecture (GAP-1514; ASM-2632) |

# 10. Release slicing proposal

The service is wave 1: it is created with Epic 1 (release 30 November 2026 (tentative)). Each slice is a list of capabilities, not stories.

## 10.1 Wave 0 — platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox and inbox library, the Temporal workflow kit, the schema and login provision, the Kafka event platform and naming library, the edge and gateway route, and observability. These belong to the platform epics and are not capabilities of this product.

## 10.2 Wave 1 — Epic 1 (release 30 November 2026 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 1.1 Read path | CAP-P1-001, CAP-P1-002 | Nothing else can be read until the views and the extension tables exist, and the boundary test must fail the build from the first story |
| 1.2 Product catalog | CAP-P1-003, CAP-P1-009 | One system of record and one owner per product is the precondition for every later product decision, and the dictionary is the build gate |
| 1.3 Freshness and gate | CAP-P1-004 | The Epic 1 outcome (case facts reconciled to the core bank; the case list is P3 rwb-case's) depends on a complete ACE batch and a visible business date |
| 1.4 Reconciliation | CAP-P1-005 | The reconciliation is the Epic 1 promise: anyone can see whether the case keys agree with ACE; the publication hold (CAP-P1-007) is retired from P1 (RD-P1-024) |
| 1.5 Account-page read | CAP-P1-001 | rwb-case builds the case list on the account facts this read serves (FR-P1-033); the P1 case-list projection (CAP-P1-010) is retired (RD-P1-024) |
| 1.6 Access and masking | CAP-P1-008 | Personal data comes straight from ACE in v5, so the role and masking position must exist with the first read |
| 1.7 Interaction ledger | CAP-P1-012 | The case history is an Epic 1 requirement and cannot be assembled after the fact |
| 1.8 Baseline measures | CAP-P1-014 | The baseline is taken once, from checked data, and frozen |
| 1.9 Retention class | CAP-P1-011 | The class must be declared with the catalog; the archive run follows rwb-document |

Rationale: the wave-1 slice is the smallest set that delivers the Epic 1 outcome, and each slice is independently demonstrable. The Section B views and every Tier 2 feature stay behind their flags until the ACE additions land, so wave 1 is not blocked by them (GAP-1505; ASM-2623).

## 10.3 Wave 2 — Epic 2 (release 31 December 2026 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 2.1 Break and freshness output at full width | CAP-P1-006 | The six quality measures and the break reasons are needed once the steward is working the list daily, and the job monitor and data-quality screens reach full scope later in Epic 8 |
| 2.2 Stage 2 data products | CAP-P1-013 | Contracts, plans and treatments must exist before the first treatment goes live (REQ-RDF-014) |

Rationale: Epic 2 puts one owner and a timer on every case and adds the steering dashboard; the reconciliation and freshness output and the Stage 2 products are what that release needs from this service.

## 10.4 Later increments

| Increment | What unlocks it |
|---|---|
| Section B views and every Tier 2 feature | The ACE team accepts and delivers RWB-ACE-001 (DL43; GAP-1505; ASM-2623) |
| Job monitor and data-quality screens at full scope | Epic 8 (hardening, release 30 June 2027 (tentative)), with the screen owner fixed (GAP-1514; ASM-2632) |
| Retention archive in force | rwb-document's retention schedule live, with the class declared here (GAP-1500; ASM-2618) |
| Reporting output for the Tribe | rwb-reporting's read model and measures live, fed by this service's snapshot (GAP-1499; ASM-2617) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source acceptance criterion that proves it, so a criterion is never invented where the source has one. Every criterion is verified in SIT against synthetic data; no production data is used.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-P1-001 | FR-P1-001, FR-P1-002, NFR-P1-015 | the migrations and the parameter `recoverySchema` | the pipeline applies them in the development and system environments | the schema holds 92 tables including the four extension tables and the 16 Section A views, each compiling against ACE; no removed copy, load or tracker table exists; the boundary test reports 1,062 of 1,062 table fields and 177 of 177 Section A view fields matched | AC-P1-001-01 |
| AC-P1-002 | FR-P1-003 | the ACE additions are deployed in system test and the 14 new ACE tables exist | the Section B migration is applied | the 14 Section B views compile with 127 fields; the dictionary holds 122 objects, 92 tables and 30 views, and 1,366 fields; the features behind the Section B flag can be switched on | AC-ALT-P1-001-02 |
| AC-P1-003 | FR-P1-001, NFR-P1-014, NFR-P1-015 | a branch that adds a foreign key from a case account to an ACE account, and a service identity that tries a direct ACE read and a view insert | the pipeline and the permission tests run | the build fails naming the cross-schema constraint; both statements are refused; the conformance step passes | AC-EXC-P1-001-04, AC-EXC-P1-001-05 |
| AC-P1-004 | FR-P1-005 | an ACE payment carrying a text date and an account carrying a Y/N flag, and a text date that is not a date | a consumer reads the payment and the account views | the date is a date and the flag is a boolean; the invalid value returns NULL without an error | AC-ALT-P1-001-04 |
| AC-P1-005 | FR-P1-006, NFR-P1-010 | a customer with an identification number and a mobile number, and a read-only role | the role reads the customer through the contract | the mobile shows as masked digits and the identity as masked digits; no response field holds the clear number; one access log entry is written | AC-P1-015-01 |
| AC-P1-006 | FR-P1-007, FR-P1-008 | an ACE person exists and has no extension row | a specialist confirms fraud on the case | one extension row exists for that person with the fraud flag true and the standard columns; the ACE customer row is unchanged; no foreign key links the tables | AC-ALT-P1-001-03 |
| AC-P1-007 | FR-P1-011 | an appraisal older than 365 days at the business date | the appraisal is read for the case | the extension row carries the stale flag true and the age in days; the writer of the flag is confirmed before release | FSD P1 A2.6 carried rule; GAP-1509; ASM-2627 |
| AC-P1-008 | FR-P1-012, FR-P1-013 | a catalog load of 14 rows, each with one system of record and one owner | the reference data administrator loads it and the steward approves it | 14 rows are in force; the account product names the ACE system of record and the source ACE ingests from; the case product names the Workbench; the collateral product names the weekly cycle and its expected-by time | AC-P1-002-01 |
| AC-P1-009 | FR-P1-013 | a catalog load naming a bare source system, a product with two systems of record, and a load with 13 rows | the load is validated | each load is refused whole with its message and the version in force keeps its rows | AC-EXC-P1-002-01, AC-EXC-P1-002-02, AC-EXC-P1-002-03 |
| AC-P1-010 | FR-P1-014, NFR-P1-002 | the batch-status view holds a completed batch for a source and business date with its start and completion times, and an account carries the same business date | the data-ready event is processed and freshness is queried for the account product | the stamp holds the product, the business date, the source time, the load time and status LOADED; the same stamp is returned to the caller; the daily jobs are started | AC-P1-014-01 |
| AC-P1-011 | FR-P1-015, FR-P1-016, NFR-P1-003 | no completed batch for the business date at the product's expected-by time | the cut-off passes | the data-late event is in the outbox with the source system and business date; the product is STALE with the flag time; the steward and the operations channel are alerted; the case record states the last completed date | AC-ALT-P1-014-01, AC-EXC-P1-014-01 |
| AC-P1-012 | FR-P1-015 | one source of a multi-source product is complete to one date and another only to an earlier date | the cut-off passes | the product carries the oldest business date and is STALE, and the late event names the source that is behind | AC-ALT-P1-014-03 |
| AC-P1-013 | FR-P1-017 | the same business date is called ready twice | the scheduler calls the operation twice | both calls are answered 202 and the work runs once; the status read returns RUNNING then DONE; the on-call runbook confirms the poll fallback | Arch v5 slide 32 contract; GAP-1513; ASM-2631 |
| AC-P1-014 | FR-P1-018, FR-P1-019 | the ACE batch is COMPLETED for ALS and the rwb-case account-key set is available after allocation | ReconciliationWorkflow runs as an AceIngestCheck child | REC-01 and REC-02 results are written for the business date; P1 writes no case-list rows or publish status | AC-P1-011-01 |
| AC-P1-015 | FR-P1-020 | the P1 reconciliation detects a variance for a product group | ReconciliationWorkflow records the result | the result is BREAK with its variance and percent; P1 does not set P3 case-list publish status | AC-ALT-P1-011-01 |
| AC-P1-016 | FR-P1-020 | a case party carries a person key with no row in the customer view | the resolution step runs | the check is BREAK with one orphan; the row is listed for the steward and the ACE team; the case and its party row are unchanged | AC-ALT-P1-011-03 |
| AC-P1-017 | FR-P1-022 | Retired from P1 by RD-P1-024 | P1 case-list step is removed | P3 rwb-case owns the case-list acceptance criteria | AC-P1-018-01 |
| AC-P1-018 | FR-P1-022 | Retired from P1 by RD-P1-024 | P1 case-list extract is not built | P3 rwb-case owns the case-list acceptance criteria | AC-ALT-P1-018-01 |
| AC-P1-019 | FR-P1-024, NFR-P1-010 | a role with no access row for a data product | the role reads that data product for a case | the call is refused with the standard authorisation message; the refusal is written to the access log with the role and the product | AC-ALT-P1-015-02 |
| AC-P1-020 | FR-P1-025, NFR-P1-009 | the PII access log rejects every write | a role reads a personal field | the call is refused with the standard system message for the PII access log and no personal field is returned | AC-EXC-P1-015-03 |
| AC-P1-021 | FR-P1-004, FR-P1-026 | the catalog and the dictionary are in force | the steward reads one data product entry and a developer counts the dictionary by source system | the entry lists the views with the ACE system of record and the extension table with the Workbench, the field ID, source system, source field, owner role, refresh cycle, expected-by time, retention class, the checks and the access rows; the dictionary returns 1,366 fields over 122 objects, 304 view fields and 1,062 table fields of which 49 on the extension tables | AC-P1-016-01, AC-ALT-P1-016-02 |
| AC-P1-022 | FR-P1-027 | a contract update that names an unknown data product, and one that marks a view as Workbench | the load is validated | both are refused whole and the version in force stays | AC-EXC-P1-016-02, AC-EXC-P1-016-03 |
| AC-P1-023 | FR-P1-028 | a retention row that names a read-only ACE view, and one that names the decision log | the load is validated | both are refused whole; ACE applies its own retention and the decision log is never archived by a retention job | AC-EXC-P1-017-03, AC-EXC-P1-017-04 |
| AC-P1-024 | FR-P1-029, FR-P1-030, NFR-P1-022, NFR-P1-025 | a case with interactions on more than one channel, and an event delivered twice with the same key | the ledger is read and the duplicate is delivered | one entry exists for the duplicate and the repeat is counted; the ledger reads back in one ordered sequence filterable by channel, actor and date range; a failed write raises an incident and no entry is discarded | Epic 1 RWB-E1-066 to RWB-E1-068; REQ-ILG-006, REQ-ILG-007, REQ-ILG-008 |

## 11.2 Requirement trace summary

| BR | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|
| REQ-RDF-001 | CAP-P1-001, CAP-P1-002, CAP-P1-003 | FR-P1-001, FR-P1-007, FR-P1-012, FR-P1-013 | NFR-P1-015 | AC-P1-001, AC-P1-003, AC-P1-006, AC-P1-008 |
| REQ-RDF-002 | CAP-P1-001 | FR-P1-001, FR-P1-002, FR-P1-005 | NFR-P1-001 | AC-P1-001, AC-P1-004 |
| REQ-RDF-003 | CAP-P1-001, CAP-P1-002 | FR-P1-002, FR-P1-009 | NFR-P1-001 | AC-P1-001, AC-P1-006 |
| REQ-RDF-004 | CAP-P1-001, CAP-P1-002 | FR-P1-002, FR-P1-003, FR-P1-011 | NFR-P1-015 | AC-P1-002, AC-P1-003, AC-P1-007 |
| REQ-RDF-005 | Not carried (removed by D-RCV-35 U5; later home the Cutover plan) | None | None | None |
| REQ-RDF-006 | Not carried (removed by D-RCV-35 U5; later home the Cutover plan) | None | None | None |
| REQ-RDF-007 | CAP-P1-005 | FR-P1-018, FR-P1-019, FR-P1-020 | NFR-P1-005, NFR-P1-006 | AC-P1-014, AC-P1-015, AC-P1-016 |
| REQ-RDF-008 | CAP-P1-005, CAP-P1-006 | FR-P1-020, FR-P1-023 | NFR-P1-006 | AC-P1-015, AC-P1-021 |
| REQ-RDF-009 | CAP-P1-004 | FR-P1-014, FR-P1-015, FR-P1-016, FR-P1-017 | NFR-P1-002, NFR-P1-003, NFR-P1-004, NFR-P1-017 | AC-P1-010, AC-P1-011, AC-P1-012, AC-P1-013 |
| REQ-RDF-010 | CAP-P1-008 | FR-P1-006, FR-P1-024, FR-P1-025, FR-P1-030 | NFR-P1-009, NFR-P1-010, NFR-P1-011, NFR-P1-013, NFR-P1-014 | AC-P1-005, AC-P1-019, AC-P1-020, AC-P1-024 |
| REQ-RDF-011 | CAP-P1-003, CAP-P1-009 | FR-P1-004, FR-P1-012, FR-P1-013, FR-P1-026, FR-P1-027 | NFR-P1-015 | AC-P1-008, AC-P1-009, AC-P1-021, AC-P1-022 |
| REQ-RDF-012 | CAP-P1-014 | FR-P1-032 | NFR-P1-017 | AC-P1-010 |
| REQ-RDF-013 | CAP-P1-011 | FR-P1-028 | NFR-P1-024 | AC-P1-023 |
| REQ-RDF-014 | CAP-P1-013 | FR-P1-031 | NFR-P1-017 | AC-P1-012 |
| REQ-CWC-001 | CAP-P1-001 | FR-P1-033 (FR-P1-022 retired, RD-P1-024) | NFR-P1-005 | Acceptance criteria of RWB-P1-E1002-APP |
| REQ-CWC-004 | CAP-P1-002 | FR-P1-008, FR-P1-010 | NFR-P1-010 | AC-P1-006 |
| REQ-DRI-006 | CAP-P1-001 | FR-P1-001 | NFR-P1-014, NFR-P1-015 | AC-P1-001, AC-P1-003 |
| REQ-DRI-008 | CAP-P1-004 | FR-P1-017 | NFR-P1-021 | AC-P1-013 |
| REQ-DRI-011 | CAP-P1-009 | FR-P1-027 | NFR-P1-017 | AC-P1-022 |
| REQ-ILG-001 to REQ-ILG-008, REQ-ILG-014 | CAP-P1-012 | FR-P1-029, FR-P1-030 | NFR-P1-022, NFR-P1-025 | AC-P1-024 |
| REQ-ACA-006 | CAP-P1-008 | FR-P1-024, FR-P1-025 | NFR-P1-009, NFR-P1-013 | AC-P1-019, AC-P1-020 |

BR coverage: 12 of the 12 live P1 program requirements (REQ-RDF-001 to REQ-RDF-014 less REQ-RDF-005 and REQ-RDF-006, which are removed) are covered by at least one functional requirement. REQ-RDF-005 and REQ-RDF-006 have no functional requirement by design: they are removed from system scope and their later home is the Cutover plan.

## 11.3 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Conformance test output for the two view migrations and the dictionary counts | FR-P1-002, FR-P1-003, FR-P1-004, NFR-P1-015 | Developer |
| Boundary and permission test output in system test | FR-P1-001, NFR-P1-014, NFR-P1-015 | Developer with the security administrator |
| Freshness drill: hold and release an ACE batch | FR-P1-014 to FR-P1-017, NFR-P1-002, NFR-P1-003, NFR-P1-004 | Data steward with the QA team |
| Reconciliation run with a seeded difference, a cleared break and a rerun | FR-P1-018 to FR-P1-022, NFR-P1-005, NFR-P1-006 | Data steward with the QA team |
| Masking matrix and access log reconciliation | FR-P1-024, FR-P1-025, NFR-P1-009, NFR-P1-010 | Compliance and PDPA officer |
| Catalog, contract and retention load refusals | FR-P1-012, FR-P1-013, FR-P1-027, FR-P1-028 | Reference data administrator |
| Ledger duplicate and read-order test | FR-P1-029, FR-P1-030, NFR-P1-022 | QA team |
| Performance and volume test at the stated volume | NFR-P1-001, NFR-P1-023 | QA team |

# 12. Open questions

The FSD's open questions are carried forward with their IDs and owners. Product-level questions follow. No question is answered by invention: where an answer is assumed, the assumption is named.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-P1-01 | Does the ACE team accept the RWB-ACE-001 scope and dates? The batch-status view is a Section B view, so freshness and every job that starts on the ACE batch record depend on it. | ACE team lead | 21 November 2026 | CAP-P1-001 (Section B), CAP-P1-004, CAP-P1-010 | FSD OQ-P1-01; DL43 |
| OQ-P1-02 | What is the freshness source before the ACE additions land? The fallback costs Tier 1 views plus the case list, and names no freshness source for it. | Solution architect | Before wave 1 system test | CAP-P1-004 | FSD OQ-P1-02; GAP-1507; ASM-2625 |
| OQ-P1-03 | Does the physical schema mapping get corrected before the dictionary is loaded? It maps all 30 view rows to one data product, gives several view fields a text data type where the physical type is integer, and marks two personal view fields as not personal. | Data architect | Before wave 1 dictionary load | CAP-P1-009, CAP-P1-008 | FSD OQ-P1-03; GAP-1506; ASM-2624 |
| OQ-P1-04 | Where does the extraction time come from, given the batch record holds none? This version maps the source extraction time to the batch start time. | Data architect | Before wave 1 system test | CAP-P1-004 | FSD OQ-P1-04 |
| OQ-P1-05 | Which function writes the appraisal stale flag and age, this service or the valuation service? | Business analyst, P1 and S1 | Before wave 1 system test | CAP-P1-002 | FSD OQ-P1-05; GAP-1509; ASM-2627 |
| OQ-P1-06 | Where is the per-account reconciliation break list kept? The removed quality-exception table leaves the schema and the result table holds only the totals. | Data architect | Before wave 1 system test | CAP-P1-005, CAP-P1-006 | FSD OQ-P1-06; GAP-1508; ASM-2626 |
| OQ-P1-07 | Do the standard error and message wordings take the ACE batch and ACE wording, as the two messages here now do? | Business analyst, P1 | Before wave 1 release | All messages | FSD OQ-P1-07 |
| OQ-P1-08 | Which system-of-record wording and which view counts are correct? The seed writes "ACE (from ALS via COLLINS)" where the rulings say "ACE (ingested from X)", and the register's section 8.2 counts 15 and 11 views while the frozen list has 16 and 14. | Data architect | Before wave 1 dictionary load | CAP-P1-003, CAP-P1-009 | FSD OQ-P1-08; GAP-1506; ASM-2624 |
| OQ-P1-09 | Where does the reconciliation and freshness output go now that the data lake and the dashboard connection are removed? | Solution architect | Before wave 2 | CAP-P1-006 | GAP-1499; ASM-2617 |
| OQ-P1-10 | Which service serves the job monitor and data-quality screens, and where should they route from? | Solution architect | Before Epic 8 | CAP-P1-006 | GAP-1514; ASM-2632 |
| OQ-P1-11 | Who accepts that the retention class is declared here while the archive run and its rule table belong to the document service? | Compliance and PDPA officer | Before wave 1 release | CAP-P1-011 | GAP-1500; ASM-2618 |
| OQ-P1-12 | Who confirms that masking rules live with the access service while role access per data product stays here? | Compliance and PDPA officer | Before wave 1 release | CAP-P1-008 | GAP-1501; ASM-2619 |
| OQ-P1-13 | Who owns the bank scheduler's DAGs, where does it run, and when does ACE ingestion move off the current scheduler? | Solution architect with the bank platform team | Before wave 1 release | CAP-P1-004, FR-P1-017 | GAP-1513; ASM-2631; Arch v5 slide 32 |
| OQ-P1-14 | What are the field lists for the data contract, the two Stage 2 data-product copies and the ledger intake rule? | Data architect | Before wave 2 | CAP-P1-003, CAP-P1-009, CAP-P1-013 | GAP-1512; ASM-2630 |
| OQ-P1-15 | Which classification applies to each data product and document type, and who sets the retention periods? | Compliance with Security | Before wave 1 release | CAP-P1-008, CAP-P1-011 | GAP-1510; ASM-2628; NFR-047; DL26 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. A missing approval is carried as an assumption, not as an answer (GAP-1515; ASM-2633).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v4 | 2 (business outcomes), 5.1 (P1 requirements, REQ-RDF-001 to REQ-RDF-014), 6.1 to 6.12 (NFR-001 to NFR-078), 7 (constraints), 8 (release plan), 9 (open decisions) |
| Recovery Workbench Business Requirements Epic 1 v4 | 3.1 (P1 requirements at development detail, RWB-E1-001 to RWB-E1-069), 4 (program requirements met), 6 (acceptance), 7 (open decisions) |
| Recovery Workbench Business Requirements Epic 2 v2 | REQ-RDF-014 |
| Recovery Workbench FSD P1 Recovery data engine v5 | Document control, existing capability check, A1 (context and scope), A2.1, A2.2, A2.11 to A2.20 (functional decomposition), Requirements served, Screens, Appendix A and B |
| Recovery Workbench Architecture v5 | Slides 13 to 20 (service contracts), 31 and 32 (overnight chain and the bank scheduler), 37 (no data lake), 41 (service catalogue), 42 and 43 (event catalogue), 44 (job map), 45 (architect questions) |
| Recovery Workbench Temporal and Drools Design v1 | Task queue, workflow kit and event-started work |
| Recovery Workbench Microservice Ownership Map v1 | Services, tables, operations, events, jobs and workflows owned by P1 |
| Recovery Workbench Non Functional Specification v3 | 1 (targets on one page), 2 (volumes and concurrency), 3.1 to 3.12 (requirements by quality characteristic) |
| Recovery Workbench Microservice Story Template and Rules v1 | R1 (user decisions), R3 (source precedence and default rulings), R5 (target structure), R8 (outputs), R9 (gaps and assumptions) |

# Appendix B. P1 developer-readiness amendments

This appendix records the final P1 rulings applied on 27 November 2026. Where earlier text conflicts with this appendix, this appendix and the final RD-P1 register ruling apply.

- ACE boundary: only the P1 database login rwb_source_data has SELECT on the 30 recovery.v_ace_* views. The view owner reads ACE source tables. No other service or user reads ACE through SQL; other services use the rwb-source-data contract. P1 reads and writes only its own rwb_source_data schema.
- Case list: P1 does not create or own case_list_row, case-list operations, a case-list Schedule, publish status or case-list checks. P3 rwb-case owns the case list. RWB-P1-E1002-APP builds the account-page read; RWB-P1-E1015-CON publishes it. RWB-P1-E1002-CON is retired with a pointer and RWB-P1-E1002-OPS is a delta. Its path and maximum keys per call remain Pending, owner Solution architect, tracked as NEW-GAP-B3. P1 reconciliation starts as a child of AceIngestCheck after the ALS stamp; REC-01 waits for rwb-case allocation until caselist.allocation.wait.until.
- Data products: product/source seed values are provisional until confirmed against ace_batch_run.source_system; owner ACE team lead, tracked as NEW-ASM-B3.
- Access and personal data: P4 rwb-access owns roles, permissions, masking rules, scope, DoA limits and the access log. Each service authorises its own objects against cached P4 policy and applies masking at its API. Every personal-field read is audited through the ACE Common PII path. Clear personal data is excluded from business events, Temporal inputs and application logs/traces/metrics; IDs and permitted business facts follow the Data Classification and Personal Data Inventory. P1 never unmasks a value already masked in an ACE view. One workload identity per service is required with no static credentials; the exact P1 workload identity identifier is provisioned by the platform. The P1 database login remains rwb_source_data.
- Retention: P1 scope is interaction (ARCHIVE) and party_ext, account_ext, contact_point_ext, valuation_ext, dp_treatment and dp_guarantee_claim (REVIEW). case_list_row is excluded because it is not created. Periods remain Pending, owner Compliance, tracked as GAP-1029. contact_point_ext and valuation_ext remain REVIEW only while the hold join key is Pending, owner Data architect, tracked as NEW-GAP-C3. No P1 destruction step is authorised.
- Migration: use Source to Target Mapping v7, sheet Migration packages, as the normative allow-list. Carry only fields whose LDM system of record is Workbench plus linking ACE business keys; ACE-sourced fields are ACE_READ and are not carried. Every migrated table carries migration_source varchar(20) and migrated_at timestamptz in UTC. The LOV-MIGRATION-SOURCE values remain Pending, owner Data owner, tracked as NEW-GAP-B4.

- Freshness: `data_product_load` uses `(product_code, business_date)`. A row is written as LOADED only after every source mapped in `data_product_source` is COMPLETED for that date; `source_system` is the completing source, `source_extracted_at` is the latest source `completed_at`, and `loaded_at` is the write instant. The stamp in use is the greatest business date; out-of-order dates remain history, restatements increment `duplicate_count` without a new event, and only RWB-P1-E1015-APP writes the table.
- Events and deployment: EV-26 is published once per source system and business date with status COMPLETED; downstream daily work starts only on ALS/COMPLETED. EV-27 is published per affected source at expected-by or on failure, as governed by RD-P1-003/041. With the Section B flag off, AceIngestCheck writes no stamp, publishes no event and starts no child; the run is LATE and freshness is STALE with a null date. P1 has no consumer group on its own `rwb.source-data.events.v1` topic.
- Pending ACE behavior: matching current `v_ace_account.data_as_of` rows to a completed business date, and behavior for null/mismatched/past/future dates, remain Pending, owner Data architect, tracked as NEW-GAP-W8-004. The input set and exact query for `v_ace_ca_relation` orphan detection remain Pending, owner Data architect, tracked as NEW-GAP-W8-003. Null handling for TDR and settlement fields remains Pending, owner Data architect, tracked as NEW-GAP-W8-005.

## Further rulings that bind the requirements above

- REST writes (RD-P1-001, RD-P1-006): every POST requires an Idempotency-Key (UUID) and replays the stored response for 24 hours; a reused key with another request answers 409. PUT and PATCH carry no Idempotency-Key; they require If-Match (428 when missing, 409 when stale).
- Interaction ledger (RD-P1-007, RD-P1-009): only rwb-source-data writes the ledger; other services append through `POST /cases/{caseId}/interactions`; rwb-comms is the one caller for delivery entries. The intake reads six event types from the case, document and decision-record topics and ignores every other type.
- Case entry (RD-P1-010, RD-P1-023): rwb-case reads candidates through the Temporal activity listEligibleAccounts; P1 offers no case-number lookup and `caseId` is the case uuid.
- Job monitor (RD-P1-012 with RD-P1-024): P1 lists and reruns its own runs only (AceIngestCheck, ReconciliationWorkflow, Stage2ProductWorkflow, RetentionRunWorkflow); only a FAILED run can be rerun. The jobs of other services stay with their owners (NEW-GAP-A1).
- Access (RD-P1-026): access version DPA-2026.11 holds seven rows, including the RW-COMPLY read of DP02.
- Reconciliation (RD-P1-042): tolerance recon.tolerance.pct version 1 is 0.00; there is no NOT_RUN result; a run that cannot proceed writes no result row.
