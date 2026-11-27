SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench P1 Recovery data engine

Functional specification. SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD P1 Recovery data engine |
| Document ID | P1-RWB-FSD-v5 |
| Service | `rwb-source-data` (Source data) |
| Version | 5 |
| Status | Draft |
| Classification | Confidential |
| Date | 27 November 2026 |
| FSD owner | Business analyst, P1 |
| Business owner | Business lead |
| Decision | D-RCV-35 (U1 to U5); ADR-010 |
| Change | 5, 27 November 2026, D-RCV-60 P1 developer readiness (RD-P1 register), targeted edits |

| Module code | Module name | First in |
|---|---|---|
| P1 | Recovery data engine | E1 |

**Feature scope.** Read-only ACE source views, the four Workbench extension tables, the data product catalog and data dictionary, freshness from the ACE batch record, P1 reconciliation using rwb-case keys, access and retention. P3 rwb-case owns case-list rows and operations.

| Version | Date | Change |
|---|---|---|
| 2 | 28 October 2026 | COLLINS and file loads, load checks, tracker loads, reconciliation to ALS, freshness from the Workbench load |
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 and ADR-010. The module loads no source data: it reads ACE through the 30 `recovery.v_ace_*` views and owns only the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext`. Freshness is stamped in `data_product_load` from `ace_batch_run`, read through `v_ace_batch_status` (EV-26 AceDataReady, EV-27 AceDataLate). The case list reconciles to `v_ace_account`. The data dictionary covers the views and the extension tables; systems of record read "ACE (ingested from X)". The load, load-check, tracker and feed-job functions FEAT-RDF-03 to 10 and FEAT-RDF-22 keep their IDs and are marked removed with their later home. JOB-01 and JOB-09 are retired. |
| 5 | 27 November 2026 | D-RCV-60 P1 developer readiness (RD-P1 register) · targeted edits |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification P1 Recovery data engine | TSD | Pair |
| Recovery Workbench User Stories Epic 1 and Epic 2 | Backlog | Traceability |
| Recovery Workbench ACE DB Alignment Change Register v1 | Decision record | Source of D-RCV-35, ADR-010, DL43 |
| Recovery Workbench ACE Data Tier Map v1 | Frozen input | Tiers, extension tables, removed tables, re-keyed links |
| Recovery Workbench ACE Source Views v1.sql | Frozen input | The 30 view definitions, grants and conformance test |
| Recovery Workbench Physical Schema v5 | Data | Tables, views and dictionary seed this module deploys |
| Recovery Workbench ACE Team Stories v1 (RWB-ACE-001) | Backlog | The ACE tables and columns the Section B views read |
| Recovery Workbench Batch and Scheduling Design v3 | Design | JOB-01 and JOB-09 retired; data jobs start on the ACE batch record |
| Recovery Workbench Event and Messaging Design v3 | Design | EV-26 AceDataReady, EV-27 AceDataLate |

**Open points carried by this version.**

| ID | Point | Owner | Blocks |
|---|---|---|---|
| OQ-P1-01 | DL43: the ACE team accepts the RWB-ACE-001 scope and dates (needed by 2026-11-21). `v_ace_batch_status` is a Section B view, so freshness (A2.14) and every job that starts on the ACE batch record depend on it. | ACE team lead | A2.1 Section B, A2.11, A2.14, A2.18 |
| OQ-P1-02 | Does the ACE team accept the RWB-ACE-001 scope and dates? Section B remains behind its dependency gate and flag until accepted. | ACE team lead | A2.14 |
| OQ-P1-03 | Physical Schema v5 maps all 30 `v_ace_*` rows in `sys_objects` to DP01, gives several Section B view fields data type TEXT and physical type integer, and marks personal view fields (`v_ace_contact.contact_value`, `v_ace_customer.first_name`) as not personal. A2.2, A2.15 and A2.16 assume the corrected mapping. | Data architect | A2.2, A2.15, A2.16 |
| OQ-P1-04 | `ace_batch_run` holds no extract time. This version maps `data_product_load.source_extracted_at` to `started_at`; the column comment in Physical Schema v5 still names the COLLINS control record. | Data architect | A2.14 |
| OQ-P1-05 | The appraisal age rule (stale over 365 days) moved from the SVAF load to `valuation_ext.stale_flag` and `age_days`. Which function writes it, P1 or S1 Valuation and route, is not yet set. | Business analyst, P1 and S1 | A2.6 removed |
| OQ-P1-06 | The reconciliation break rows were written to `dq_exception`, which leaves the schema. `reconciliation_result` holds only the totals. Where the per-account break list is kept needs a decision. | Data architect | A2.11, A2.12 |
| OQ-P1-07 | Message wording: MSG-P1-001 and MSG-P1-012 now name the ACE batch and ACE rather than a load and ALS. The Error and Message Standard needs the same change. | Business analyst, P1 | All |
| OQ-P1-08 | The Physical Schema v5 seed writes systems of record as "ACE (from ALS via COLLINS)", but the rulings say "ACE (ingested from X)". This document uses the rulings' wording. The register's section 8.2 also counts 15 and 11 views, while the frozen list has 16 and 14. | Data architect | A2.2 |

### Note, Architecture v5 (D-RCV-60)

| Item | Value |
|---|---|
| Service | `rwb-source-data` (Source data) |
| Owns in Architecture v5 | ACE view contract, extension tables, freshness, reconciliation |
| Service epic | `RWB-SVC-P1` |
| Wave | 1 |
| Schema | `rwb_source_data` |
| REST base | `/api/recovery/source-data/v1` |
| Kafka topic | `rwb.source-data.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.source-data.<Event>.v1` |
| Temporal task queue | `rwb-source-data` |
| Java package | `th.co.scb.ace.workbench.recovery.sourcedata` |

Version 4 adds the Service row, the Change row and this note above; nothing else in this document changes. Under Architecture v5 the module is delivered as the service `rwb-source-data` of the 19 services inside ACE (ADR-013), with its own schema `rwb_source_data` and login (ADR-014), in wave 1, service epic `RWB-SVC-P1`; the realignment is D-RCV-60 (DL44), and DL46 keeps team-type ownership soft. The functional content of this document is the content of version 3, kept word for word: every feature, requirement, rule, field, list, message, screen, count and date.

Every owner named in this document is the owner recorded in the Microservice Ownership Map v1, and where the map carries a ruling of Template and Rules §R3 the ruling is followed: parameters and reference data with `rwb-case` (DP-06, DP-07), the rule package registry with `rwb-decision` (DP-04), the interaction ledger with `rwb-source-data` (DP-18) and feature flags with the platform library. Where this document names a table, endpoint, event, job, workflow or screen that the map gives to another service, that service owns it and this module reaches it only through the owner's contract (DP-01, DP-11; ADR-020).

The extracts, feeds and copies this document addresses to a data lake are removed by Architecture v5: reporting reads events into `rwb-reporting` (DP-17, ADR-018). The wording of those extracts is kept as written and carried by GAP-1861.

Release dates stay as written and are tentative (DL48). No approval of version 4 is recorded (ASM-3046); the version is Draft.

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit and PII logging | REUSE | ACE common module | No build in this module |
| Case record and shared entities | REUSE | ACE common module; Case and Workflow Model | Read through the P3 interfaces |
| Notification path | REUSE | ACE notification path | Recovery templates only |
| Workflow and state machine | REUSE | Workflow Engine Design | Stages and sentries from P3 |
| Decision record and audit trail | REUSE | Audit and Logging Design | Writes through P7 |
| Attachments and evidence | REUSE | Document Management Design | Through P5 |
| Role and permission matrix | REUSE | Users Roles and Permissions | Capability areas from P4 |
| Restructure calculator | REUSE | ACE common module | Read as plan data through `v_ace_plan` |
| Source data: account, payment, customer, contact, relations, collateral, asset, EFS actions and assignments, buckets, products, branches, holidays, restructure plan | REUSE | ACE database; ACE Data Tier Map v1 Tier 1 | Read only through the 16 Section A `recovery.v_ace_*` views; never copied, never altered |
| Source data ACE does not hold today: batch record, valuation, collateral detail, NPA asset and sale, lawsuit, hearing, proof of delivery, GL write-off, COLLINS score, party product, credit decision, e-signature, Entra ID group | REUSE once delivered | RWB-ACE-001 (ACE team); Tier Map v1 Tier 2 | Read only through the 14 Section B views once ACE has added them |
| Source ingestion and ingestion checks | REUSE | ACE ingestion; RWB-ACE-001 | No load, staging table or load check in this module (D-RCV-35, U1) |
| Scheduler and batch | REUSE | Quartz and Spring Batch in ACE | No new `qrtz_` table; JOB-01 and JOB-09 retired |
| Holiday calendar | REUSE | `v_ace_holiday` over `bot_holiday` | Replaces a Workbench holiday list |

## A1. Context and scope

### A1.1 Scope of work and deliverables

**In scope.** The read-only `recovery.v_ace_*` views and their grants, the four extension tables, the data dictionary, 14 data products, freshness from ACE batch status, P1 reconciliation using rwb-case keys, the reconciliation and freshness report, access and masking per data product, the catalog, retention of Workbench records, baseline measures and the decision log copy. P3 rwb-case owns the case list, publication and checks.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces. Removed by D-RCV-35: every inbound source load, staging table and load check (later home ACE ingestion, RWB-ACE-001); the Excel and SharePoint tracker inventory, load and retirement (later home Cutover plan, U5); the legacy feed jobs on ADF and Control-M (later home ACE ingestion; no ADF job remains).

**Dependencies.** FEAT-DRI-01; FEAT-RDF-01; FEAT-RDF-02; FEAT-RDF-11; FEAT-RDF-14; FEAT-CWC-01; RWB-E1-069; RWB-ACE-001; DL43

**Constraints.** Built in the ACE service as part of the recovery module. Source data is read only through the `recovery.v_ace_*` views (D-RCV-35 U4, ADR-010). The module creates no foreign key into a `public` table, because ACE cascades deletes on `account`. It links to a source record by business key (`account_key`, `person_key`, `asset_key`, `payment_code`, `contact_key`) and never alters an ACE table. Every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| P1 | FEAT-RDF-01 | Create the recovery tables, extension tables and read-only ACE views | System | Creates the 92 recovery tables, the four extension tables among them, and the 30 SELECT-only `recovery.v_ace_*` views with their grant and boundary test. | E1 | A2.1 |
| P1 | FEAT-RDF-02 | Define the 14 data products and their systems of record | Admin | Names each data product, its owner, its system of record ("ACE (ingested from X)" or Workbench), the views and tables behind it and its definition, so one number has one source. | E1 | A2.2 |
| P1 | FEAT-RDF-03 | Load account and arrears daily from ALS | System | Removed by D-RCV-35 — later home: ACE ingestion. | E1 | A2.3 |
| P1 | FEAT-RDF-04 | Load collections status and contact history from EFS | System | Removed by D-RCV-35 — later home: ACE ingestion. | E1 | A2.4 |
| P1 | FEAT-RDF-05 | Load collateral records from CCMS | System | Removed by D-RCV-35 — later home: ACE ingestion. | E1 | A2.5 |
| P1 | FEAT-RDF-06 | Load appraisal values from SVAF | System | Removed by D-RCV-35 — later home: ACE ingestion. | E1 | A2.6 |
| P1 | FEAT-RDF-07 | Inventory the Excel and SharePoint trackers | Admin | Removed by D-RCV-35 — later home: Cutover plan. | E1 | A2.7 |
| P1 | FEAT-RDF-08 | Load the tracker data into the data store | System | Removed by D-RCV-35 — later home: Cutover plan. | E1 | A2.8 |
| P1 | FEAT-RDF-09 | Retire a local tracker copy | Admin | Removed by D-RCV-35 — later home: Cutover plan. | E1 | A2.9 |
| P1 | FEAT-RDF-10 | Run data quality rules on every load | System | Removed by D-RCV-35 — later home: ACE ingestion. The daily gate moves into FEAT-RDF-14. | E1 | A2.10 |
| P1 | FEAT-RDF-11 | Reconcile rwb-case keys to ACE daily | System | Writes P1 reconciliation results for ACE account facts and rwb-case keys after the ALS stamp and P3 allocation. | E1 | A2.11 |
| P1 | FEAT-RDF-12 | Publish the daily reconciliation and freshness report | System | Produces the daily report of reconciliation results, the freshness of each data product and the quality measures, for the data steward. | E1 | A2.12 |
| P1 | FEAT-RDF-13 | Retired by RD-P1-024 | P3 rwb-case owns case-list publication and checks; P1 has no publish status or case-list hold. | Retired | RD-P1-024 |
| P1 | FEAT-RDF-14 | Stamp each data product with its freshness | System | Writes the freshness stamp in `data_product_load` from the ACE batch record, so a decision carries the age of the data it used, and gates the daily data jobs on a complete ACE batch. | E1 | A2.14 |
| P1 | FEAT-RDF-15 | Set access control per data product for PDPA | Admin | Sets who can read each data product and which fields are masked, under the PDPA minimization rule, over the views and the extension tables. | E1 | A2.15 |
| P1 | FEAT-RDF-16 | Maintain the data catalog entry per data product | Admin | Keeps the catalog entry for each data product: definition, owner, system of record, views and tables, refresh, reconciliation rules and access. | E1 | A2.16 |
| P1 | FEAT-RDF-17 | Apply the retention and archive rule to the data store | Admin | Applies the retention class to each Workbench table and archives records past their period. ACE data is retained by ACE. | E1 | A2.17 |
| P1 | FEAT-RDF-18 | Retired from P1 by RD-P1-024 | P3 rwb-case owns and serves the case list. | Retired | RD-P1-024 |
| P1 | FEAT-RDF-19 | Publish baseline measures for the recovery portfolio | System | Calculates and publishes the starting measures the benefit model is tracked against. | E1 | A2.19 |
| P1 | FEAT-RDF-20 | Copy the decision log to the lake | System | Streams decision log entries to the data lake so reporting and audit read them without touching the log store. | E1 | A2.20 |
| P1 | FEAT-RDF-22 | Run legacy feed jobs on ADF and Control-M | System | Removed by D-RCV-35 — later home: ACE ingestion. JOB-01 and JOB-09 are retired; no ADF job remains. | E1 | A2.21 |

### A1.3 Background

Recovery source data is held in the ACE database. ACE ingests the core bank (ALS), EFS, SCBPDM and product and branch data today. Under RWB-ACE-001 it adds CCMS, SVAF, AMIS, RPS, LIT, WIN, GL, COLLINS, NLEADS, EasyApp and Entra ID. The Workbench is a module of ACE (ADR-001). The v2 design copied 121 fields of that data into eleven Workbench tables and ran nine more tables to load them. Two copies of the same account disagree sooner or later. In v3 the module reads ACE through views and holds only the case and its own decisions: **ACE holds the data, the Workbench holds the case, and a view joins them.**

| Tier | Owner | What this module does with it |
|---|---|---|
| 1. 22 ACE tables that exist today | ACE team, read only | Reads through 16 Section A views |
| 2. 14 new ACE tables and 12 new columns (RWB-ACE-001) | ACE team | Reads through 14 Section B views once they land |
| 3. 4 extension tables | Workbench | Writes Workbench decisions about an ACE record, keyed by its business key |
| 4. 88 Workbench tables | Workbench | Case, workflow, treatment, legal, partner, debt sale, documents, decision log, reference, outbox, flags, agents |

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date from the ACE batch record, or show their date as stale.
- The ACE schema, with the tables named in the Section A grant, is present in the target environment before V0002 runs. The Section B tables of RWB-ACE-001 are present before V0003 runs.

## A2. Functional decomposition

### A2.1 Create the recovery tables, extension tables and read-only ACE views

#### A2.1.1 Intent

**Business objective.** Creates the 92 recovery tables in the ACE database and the 30 SELECT-only `recovery.v_ace_*` views over ACE, so the Workbench reads one copy of source data and adds only its own records.

**Problem.** Source data is held in ACE. A Workbench copy of it would disagree with ACE and would be owned by no one who maintains the source.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Views compile and the boundary test passes | 100 percent of pipeline runs | Conformance test in the pipeline | Each release |

#### A2.1.2 Description

**Functional overview.** V0001 creates the recovery tables and the dictionary. V0002 (RWB-E1-069) creates the 16 Section A views over the ACE tables that exist today. V0003 creates the 14 Section B views over the RWB-ACE-001 additions the week they land. The views are owned by a dedicated `ace_view_owner` role that holds SELECT on the ACE tables. The recovery service identity holds SELECT on the views and nothing else.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a pipeline deployment | Reads the migration set and the dictionary seed |
| 2 | System | Creates the tables, the extension tables and the views, and applies the grant | Runs the conformance test |
| 3 | System | Records the result | Writes the Flyway history; fails the stage and names the statement or the check where a test fails |

| View family | Section | Views |
|---|---|---|
| Account, payment, plan | A | `v_ace_account`, `v_ace_payment`, `v_ace_plan`, `v_ace_bucket_log` |
| Customer and contact | A | `v_ace_customer`, `v_ace_contact`, `v_ace_ca_relation`, `v_ace_aa_relation` |
| Collateral and asset | A | `v_ace_collateral`, `v_ace_asset` |
| Collections activity | A | `v_ace_efs_action`, `v_ace_efs_action_code`, `v_ace_efs_assignment` |
| Reference | A | `v_ace_product`, `v_ace_branch`, `v_ace_holiday` |
| Batch record | B | `v_ace_batch_status` |
| Collateral, valuation, NPA | B | `v_ace_valuation`, `v_ace_collateral_detail`, `v_ace_npa_asset`, `v_ace_npa_sale` |
| Legal and delivery | B | `v_ace_lawsuit`, `v_ace_hearing`, `v_ace_pod` |
| Money, score, party product | B | `v_ace_write_off`, `v_ace_score`, `v_ace_party_product` |
| Treatment, signature, access | B | `v_ace_credit_decision`, `v_ace_esign`, `v_ace_iam_group` |

**Integration points.** ACE database (public schema, read through views), Flyway pipeline

**Prerequisites.** RWB-ACE-001 for Section B only (DL43)

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-001-1 | Data product stale when the ACE batch is late or failed | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-001 | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR-P1-001-2 | The recovery module reads ACE only through `recovery.v_ace_*`. A direct `public.*` read in a story, spec or query is a defect | None |
| BR-P1-001-3 | No constraint in schema `recovery` references a table outside it. A link to a source record is a business-key column of type `varchar(255)` with no foreign key | None |
| BR-P1-001-4 | The recovery service identity holds SELECT on the views and the recovery tables it needs, and no INSERT, UPDATE, DELETE or TRUNCATE on any view or any `public` table | None |
| BR-P1-001-5 | An extension table holds a Workbench decision about an ACE record and never a copy of an ACE column. It is 1:1 with the ACE record and carries the seven standard record columns | None |
| BR-P1-001-6 | A view never exposes `customer.identification_number` in clear; it returns `id_no_masked` and `id_no_last4` only | None |
| BR-P1-001-7 | A text date in ACE becomes a date through `recovery.ace_to_date`, and a Y/N flag becomes a boolean through `recovery.ace_to_boolean`. Both return NULL rather than fail | None |

##### A2.1.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| party_ext.person_key | ACE customer key the flags belong to (DF-EXT-001) | varchar(255) | Yes | None | No |
| party_ext.vulnerable | True while the customer is treated as vulnerable (DF-EXT-002) | boolean | Yes | None | Yes |
| party_ext.deceased_override | True when a person confirms death against the ACE record (DF-EXT-003) | boolean | Yes | None | Yes |
| party_ext.bankruptcy | True while a bankruptcy is registered (DF-EXT-004) | boolean | Yes | None | Yes |
| party_ext.fraud_flag | True while fraud is confirmed or under investigation (DF-EXT-005) | boolean | Yes | None | Yes |
| contact_point_ext.contact_key | ACE phone, email or address key, composite `contact_type:key` (DF-EXT-013) | varchar(255) | Yes | None | No |
| contact_point_ext.contact_type | PHONE, EMAIL or ADDRESS (DF-EXT-014) | varchar(10) | Yes | None | No |
| contact_point_ext.consent_given | True while the customer consents to contact (DF-EXT-015) | boolean | Yes | None | Yes |
| contact_point_ext.consent_at | When consent was given or withdrawn (DF-EXT-016) | timestamptz | No | None | No |
| contact_point_ext.verified_at | When the contact point was last verified (DF-EXT-017) | timestamptz | No | None | No |
| contact_point_ext.failed_count | Consecutive failed attempts on this contact point (DF-EXT-018) | integer | Yes | None | No |
| contact_point_ext.source | Where the row came from (DF-EXT-019) | varchar(20) | Yes | None | No |
| account_ext.account_key | ACE account key the state belongs to (DF-EXT-027) | varchar(255) | Yes | None | No |
| account_ext.dispute_open | True while a dispute is open on the account (DF-EXT-028) | boolean | Yes | None | No |
| valuation_ext.valuation_key | ACE appraisal key the decision belongs to (DF-EXT-036) | varchar(255) | Yes | None | No |
| valuation_ext.accepted | True when the appraisal is accepted for the case (DF-EXT-037) | boolean | Yes | None | No |
| valuation_ext.accepted_at | When the appraisal was accepted (DF-EXT-038) | timestamptz | No | None | No |
| valuation_ext.accepted_by | Who accepted the appraisal (DF-EXT-039) | uuid | No | None | No |
| valuation_ext.valuer_partner_id | The panel valuer who carried out the appraisal (DF-EXT-040) | uuid | No | None | No |
| valuation_ext.stale_flag | True when the appraisal is older than its cycle (DF-EXT-041) | boolean | Yes | None | No |
| valuation_ext.age_days | Days from the appraisal date to today (DF-EXT-042) | integer | No | None | No |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner, Platform administrator | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-001-01 | Schema and Section A views deployed | the ACE schema in DEV and SIT, the migrations V0001__recovery_schema.sql and V0002__rwb_e1_069_ace_source_views.sql, and the parameter recoverySchema = "recovery" | the pipeline applies them in DEV and then in SIT | the recovery schema in each environment holds 92 tables, among them party_ext, contact_point_ext, account_ext and valuation_ext And it holds the 16 Section A views, each compiling against the ACE schema And no table named loan_account, account_payment, party, contact_point, collateral, collections_history, valuation, score, asset, load_run, dq_exception, dq_rule, source_field_map, source_code_map, interface_run, interface_signoff, tracker_inventory or tracker_row exists And the conformance test reports 1,062 of the 1,062 table fields and 177 of the 177 Section A view fields matched by name and physical type | RWB-E1-001, RWB-E1-069 |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-001-01 | Dictionary published for a view field | the data dictionary and the data product seed loaded by V0001 | a developer queries v_data_dictionary for entity "v_ace_account" and field "days_past_due" | the row holds field ID "DF-ACE-018", data type "NUMBER", physical type "integer" And source system "ACE", source field "public.account.delay_days" And data product "DP01", refresh cycle "DAILY" and owner role "RW-DATASTEW" | RWB-E1-001, RWB-E1-069 |
| AC-ALT-P1-001-02 | Section B views after RWB-ACE-001 | RWB-ACE-001 is deployed in SIT and public.ace_batch_run, public.valuation and the other 12 new ACE tables exist | the pipeline applies V0003 | the 14 Section B views compile with 127 fields And sys_objects holds 122 rows, 92 tables and 30 views, and sys_fields holds 1,366 rows And the features behind the Section B flag can be switched on | RWB-E1-069 |
| AC-ALT-P1-001-03 | Extension row written, ACE untouched | person_key "P0000123" exists in v_ace_customer and has no party_ext row | a fraud specialist confirms fraud on the case and the Workbench writes party_ext with fraud_flag true | party_ext holds one row for "P0000123" with fraud_flag true and the seven standard columns And public.customer for "P0000123" is unchanged And no foreign key links party_ext to public.customer | RWB-E1-069 |
| AC-ALT-P1-001-04 | Type rules in the view | ACE payment "PAY-0001" carries pay_date "20261130" and account "ACC0000017" carries is_restructured "Y" | the developer reads v_ace_payment and v_ace_account | payment_date is the date 2026-11-30 And tdr_flag is true And a pay_date "31-11-2026" returns payment_date NULL without an error | RWB-E1-069 |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-001-01 | Failed migration leaves no partial schema | a copy of V0001 in which the statement creating table valuation_ext fails | the pipeline applies it in DEV | the pipeline stage fails and names the failing statement And the recovery schema holds none of the tables of that migration And the Flyway history has no successful row for V0001 | RWB-E1-001 |
| AC-EXC-P1-001-02 | Column without a dictionary entry fails the build | a branch that adds the column account_ext.branch_code with no sys_fields row | the conformance test runs in the pipeline | the test fails with "account_ext.branch_code has no data dictionary entry" And a sys_fields row DF-EXT-028 whose column is changed to type text fails the test with "DF-EXT-028 physical type boolean expected, text found" | RWB-E1-001 |
| AC-EXC-P1-001-03 | Repeated migration has no effect | V0001 and V0002 already applied in SIT | the pipeline runs again in SIT | Flyway reports both versions as already applied And the row counts of sys_objects (122) and sys_fields (1,366) are unchanged | RWB-E1-001 |
| AC-EXC-P1-001-04 | Foreign key into ACE fails the build | a branch that adds a foreign key from case_account.account_key to public.account | the conformance test runs in the pipeline | the test fails with "fk_case_account_account_key references public.account; no constraint in recovery may reference another schema" And the merge is blocked | RWB-E1-069 |
| AC-EXC-P1-001-05 | Recovery identity cannot read ACE directly or write a view | the recovery service identity in SIT | it runs SELECT on public.account, and INSERT on recovery.v_ace_account | both statements are refused with permission denied And the conformance test step 4 passes | RWB-E1-069 |
| AC-EXC-P1-001-06 | Section B before RWB-ACE-001 | public.valuation does not exist in SIT | the pipeline applies V0003 | the stage fails and names "relation public.valuation does not exist" And no Section B view is created And the 16 Section A views and the features that use them are unchanged And the features that need a Section B view stay behind their flag | RWB-E1-069 |
| AC-EXC-P1-001-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-001-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-001-01 | ACE data ready (EV-26 AceDataReady) | v_ace_batch_status shows the ALS batch COMPLETED for the business date | Daily, on the ACE batch | Stamps freshness and starts JOB-02, JOB-04, JOB-07 and JOB-08 | Data products current by 08:00 | Every decision uses current ACE data |
| AC-BG-P1-001-02 | Daily reconciliation (JOB-04) | AceDataReady for ALS, after JOB-02 | Daily | Compares accounts at 90 days past due in v_ace_account with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.2 Define the 14 data products and their systems of record

#### A2.2.1 Intent

**Business objective.** Names each data product, its owner, its system of record, the views and Workbench tables behind it, and its definition, so one number has one source.

**Problem.** Source data now comes from ACE and Workbench records come from the Workbench. Without a catalog that says which is which, two screens can show two answers.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Data products with one system of record and one named owner | 14 of 14 | data_product catalog | Monthly |

#### A2.2.2 Description

**Functional overview.** The reference data administrator loads the catalog as a versioned reference load and the data steward approves it. A product fed from source data names ACE as its system of record, with the source ACE ingests it from. A product of Workbench records names the Workbench.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Data steward and data product owner | Opens the catalog and defines the 14 data products and their systems of record | Checks the role, the capability area and the scope |
| 2 | Data steward and data product owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the catalog version and the decision log entry |

| Product | Name | System of record | Read from ACE through | Workbench tables | Refresh | Expected by |
|---|---|---|---|---|---|---|
| DP01 | Account and arrears | ACE (ingested from ALS) | v_ace_account, v_ace_payment, v_ace_aa_relation, v_ace_bucket_log, v_ace_product, v_ace_branch | account_ext | DAILY | 08:00 |
| DP02 | Customer and party | ACE (ingested from SCBPDM and the core bank) | v_ace_customer, v_ace_contact, v_ace_ca_relation, v_ace_party_product | party_ext, contact_point_ext | DAILY | 08:00 |
| DP03 | Case and ownership | P3 rwb-case | None | P3 case/account/party records; not served as P1 records | ON_CHANGE | As it changes |
| DP04 | Treatment and offers | Workbench; plan data from ACE; credit decision ACE (ingested from NLEADS) | v_ace_plan, v_ace_credit_decision, v_ace_esign | treatment, guarantee_claim | ON_CHANGE | As it changes |
| DP05 | Contact and promises | ACE (ingested from EFS) and the Workbench | v_ace_efs_action, v_ace_efs_action_code, v_ace_efs_assignment | interaction | DAILY | 08:00 |
| DP06 | Collateral and assets | ACE (ingested from CCMS, SVAF, AMIS and RPS) | v_ace_collateral, v_ace_asset, v_ace_collateral_detail, v_ace_valuation, v_ace_npa_asset, v_ace_npa_sale | valuation_ext, listing, asset_sale | WEEKLY | MON 08:00 |
| DP07 | Legal events and cases | ACE (ingested from LIT and WIN) and the Workbench | v_ace_lawsuit, v_ace_hearing, v_ace_pod | legal_action, notice, hearing | DAILY | 08:00 |
| DP08 | Partner performance | Workbench | None | partner, partner_instruction | ON_CHANGE | As it changes |
| DP09 | Debt sale | Workbench | None | debt_sale_lot, debt_sale_account | ON_CHANGE | As it changes |
| DP10 | Documents and extracted fields | Workbench | None | document, document_field, document_custody | ON_CHANGE | As it changes |
| DP11 | Scores and route economics | ACE (ingested from COLLINS) | v_ace_score | None | DAILY | 08:00 |
| DP12 | Decision log | Workbench | None | decision_log_entry | ON_CHANGE | As it changes |
| DP13 | Money and closure | ACE (ingested from ALS and GL) | v_ace_payment, v_ace_write_off | proceeds, write_off | DAILY | 08:00 |
| DP14 | Reference data | Workbench; ACE lists read through views | v_ace_product, v_ace_branch, v_ace_holiday, v_ace_efs_action_code, v_ace_iam_group | rule_row, lov_value, role, permission, template | ON_CHANGE | As it changes |

**Integration points.** ACE database

**Prerequisites.** FEAT-RDF-01

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-002-1 | Data product stale when the ACE batch is late or failed | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| VR-P1-002-2 | Reference load refused at a check | MSG-P1-002 The {source} load for {date} was refused: {check}. The previous load is still in use. |
| VR-P1-002-3 | A system of record is ACE, written "ACE (ingested from X)", or the Workbench. A source system on its own, for example "CCMS", is refused because no source reaches the Workbench except through ACE | MSG-P1-003 |
| BR-P1-002 | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR-P1-002-2 | Every `v_ace_*` view belongs to the data product of its object family and carries system of record "ACE". Every extension table belongs to the data product of the ACE record it extends and carries system of record "Workbench" | None |

##### A2.2.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| data_product.product_code | Data product code DP01 to DP14 | varchar(25) | Yes | LOV-DATA-PRODUCT | No |
| data_product.product_name | Data product name, for example Account and arrears | varchar(80) | Yes | None | No |
| data_product.definition | Definition of the product | varchar(400) | Yes | None | No |
| data_product.system_of_record | The one system of record, "ACE (ingested from X)" or "Workbench" | varchar(120) | Yes | None | No |
| data_product.owner_role | Role of the owner, normally RW-DATASTEW | varchar(20) | Yes | None | No |
| data_product.owner_user_id | The named owner of the product; required by the catalog load | uuid | Yes | None | No |
| data_product.refresh_cycle | Daily, weekly, monthly or on change | varchar(10) | Yes | None | No |
| data_product.expected_by | Time the ACE batch is expected by, for example 08:00 or MON 08:00 | varchar(20) | No | None | No |
| data_product.valid_from | Date the catalog version comes into force | date | Yes | None | No |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| Data steward and data product owner | Primary |
| Center of excellence analyst | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-002-01 | Catalog loaded with one system of record each | a catalog load file with the 14 rows DP01 to DP14, each with one system of record and one owner user ID | the reference data administrator loads it with valid from 2026-11-30 and the data steward approves it | data_product holds 14 rows And DP01 names system of record "ACE (ingested from ALS)" And DP03 names "Workbench" And DP06 names "ACE (ingested from CCMS, SVAF, AMIS and RPS)", refresh cycle "WEEKLY" and expected by "MON 08:00" | RWB-E1-001 |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-002-01 | Product resolves to its views and extension tables | the catalog in force | a developer queries v_data_dictionary for data product "DP02" | the rows include the fields of v_ace_customer, v_ace_contact, v_ace_ca_relation and v_ace_party_product with source system "ACE" And the fields of party_ext and contact_point_ext with source system "Workbench" And no row names a removed table party or contact_point | RWB-E1-001 |
| AC-ALT-P1-002-02 | ACE wording for every source product | the catalog in force | a data steward calls GET /admin/data-products | every product whose data comes from a source names a system of record beginning "ACE (ingested from" And no product names COLLINS staging or a file load as its source | RWB-E1-001 |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-002-01 | Source system named as system of record is refused | a catalog load file in which DP06 names system of record "CCMS" | the reference data administrator loads it | the load is refused whole with MSG-P1-003 for DP06 And data_product keeps the rows of the version in force | RWB-E1-001 |
| AC-EXC-P1-002-02 | Two systems of record or no owner is refused | a catalog load file in which DP06 names "ACE (ingested from CCMS); SVAF" And DP11 has no owner user ID | the reference data administrator loads it | the load is refused whole with MSG-P1-003 for DP06 and for DP11 And data_product keeps the rows of the version in force | RWB-E1-001 |
| AC-EXC-P1-002-03 | Catalog with a missing product is refused | a catalog load file with 13 rows and no row for DP09 | the reference data administrator loads it | the load is refused whole with MSG-P1-004 naming "DP09" And no row is written | RWB-E1-001 |
| AC-EXC-P1-002-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-002-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-002-01 | ACE data ready (EV-26 AceDataReady) | v_ace_batch_status shows the ALS batch COMPLETED for the business date | Daily, on the ACE batch | Stamps freshness and starts JOB-02, JOB-04, JOB-07 and JOB-08 | Data products current by 08:00 | Every decision uses current ACE data |
| AC-BG-P1-002-02 | Daily reconciliation (JOB-04) | AceDataReady for ALS, after JOB-02 | Daily | Compares accounts at 90 days past due in v_ace_account with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.3 Load account and arrears daily from ALS

**Removed by D-RCV-35 — later home: ACE ingestion.**

| Item | Value |
|---|---|
| Feature | FEAT-RDF-03 |
| Decision | D-RCV-35 (U1); ADR-010 supersedes ADR-005; DT12 superseded |
| Story | RWB-E1-003, removed; content parked in Data Load Story Removals v1 |
| Later home | ACE ingestion. ACE ingests ALS into public.account and public.payment. Load checks DQ-001 to DQ-014 are moved to ACE ingestion (RWB-ACE-001) |
| What this module does instead | Reads account and arrears through v_ace_account and payments through v_ace_payment (A2.1); stamps DP01 from v_ace_batch_status (A2.14) |
| Withdrawn IDs | VR-P1-003-1, BR-P1-003, AC-P1-003-01, AC-ALT-P1-003-01 to 02, AC-EXC-P1-003-01 to 09, AC-BG-P1-003-01 to 02 |
| Removed objects | loan_account, account_payment, load_run, dq_exception, source_code_map, INT-01 and INT-02 inbound, JOB-01, LoadCompleted, LoadRefused |

---

### A2.4 Load collections status and contact history from EFS

**Removed by D-RCV-35 — later home: ACE ingestion.**

| Item | Value |
|---|---|
| Feature | FEAT-RDF-04 |
| Decision | D-RCV-35 (U1) |
| Story | RWB-E1-004, removed |
| Later home | ACE ingestion. ACE already ingests public.efs_action, efs_action_code and efs_assignment. The EFS mapping sign-off moves to the ACE team under RWB-ACE-001. contact_result and action_contact_status are new efs_action columns in RWB-ACE-001 |
| What this module does instead | Reads collections history through v_ace_efs_action (contact_at from action_timestamp), action codes through v_ace_efs_action_code and hand-overs through v_ace_efs_assignment; stamps DP05 from v_ace_batch_status |
| Withdrawn IDs | VR-P1-004-1, BR-P1-004, AC-P1-004-01, AC-ALT-P1-004-01 to 02, AC-EXC-P1-004-01 to 06, AC-BG-P1-004-01 to 02 |
| Removed objects | collections_history, source_field_map, interface_signoff, INT-07 inbound, load checks DQ-037 to DQ-041 |

---

### A2.5 Load collateral records from CCMS

**Removed by D-RCV-35 — later home: ACE ingestion.**

| Item | Value |
|---|---|
| Feature | FEAT-RDF-05 |
| Decision | D-RCV-35 (U1, U2) |
| Story | RWB-E1-009, removed |
| Later home | ACE ingestion. CCMS detail lands in the new ACE table collateral_detail (RWB-ACE-001); ACE already holds collateral and asset |
| What this module does instead | Reads the collateral link and value through v_ace_collateral and v_ace_asset (Section A), and title deed, plot, area, location, insurance and lien rank through v_ace_collateral_detail (Section B); stamps DP06 |
| Withdrawn IDs | VR-P1-005-1, BR-P1-005, AC-P1-005-01, AC-ALT-P1-005-01 to 02, AC-EXC-P1-005-01 to 08, AC-BG-P1-005-01 to 02 |
| Removed objects | collateral, account_collateral, asset (copy), INT-10 inbound, JOB-09, load checks DQ-059 to DQ-062 |

---

### A2.6 Load appraisal values from SVAF

**Removed by D-RCV-35 — later home: ACE ingestion.**

| Item | Value |
|---|---|
| Feature | FEAT-RDF-06 |
| Decision | D-RCV-35 (U1, U2, U3) |
| Story | RWB-E1-009, removed |
| Later home | ACE ingestion. SVAF appraisals land in the new ACE table valuation (RWB-ACE-001) |
| What this module does instead | Reads appraisals through v_ace_valuation (Section B). The Workbench decision about an appraisal (accepted, accepted by, valuer, stale flag, age in days) is held in valuation_ext, keyed by valuation_key |
| Carried rule | Appraisal age: stale when more than 365 days old at the business date. It moves to valuation_ext.stale_flag and age_days; the owning function is open (OQ-P1-05) |
| Withdrawn IDs | VR-P1-006-1, BR-P1-006, AC-P1-006-01, AC-ALT-P1-006-01 to 02, AC-EXC-P1-006-01 to 08, AC-BG-P1-006-01 to 02 |
| Removed objects | valuation (copy), INT-11 inbound, the load path through ValuationRecordApi, JOB-09, load check DQ-068 |

---

### A2.7 Inventory the Excel and SharePoint trackers

**Removed by D-RCV-35 — later home: Cutover plan.**

| Item | Value |
|---|---|
| Feature | FEAT-RDF-07 |
| Decision | D-RCV-35 (U5): Excel and SharePoint trackers leave system scope |
| Story | RWB-E1-005, removed |
| Later home | Cutover plan: the tracker retirement procedure, with the team owners |
| Withdrawn IDs | VR-P1-007-1, BR-P1-007, AC-P1-007-01, AC-ALT-P1-007-01 to 02, AC-EXC-P1-007-01 to 03, AC-BG-P1-007-01 to 02, MSG-P1-016, GET /admin/trackers |
| Removed objects | tracker_inventory |
| Requirement | REQ-RDF-005 removed from system scope |

---

### A2.8 Load the tracker data into the data store

**Removed by D-RCV-35 — later home: Cutover plan.**

| Item | Value |
|---|---|
| Feature | FEAT-RDF-08 |
| Decision | D-RCV-35 (U5) |
| Story | RWB-E1-010, removed |
| Later home | Cutover plan. A tracker field that has a source is in ACE through RWB-ACE-001; one that has none is recorded by the team in the Workbench screen that owns it |
| Withdrawn IDs | VR-P1-008-1, BR-P1-008, AC-P1-008-01, AC-ALT-P1-008-01 to 02, AC-EXC-P1-008-01 to 07, AC-BG-P1-008-01 to 02, checks TRK-01 and TRK-02, MSG-P1-008, MSG-P1-009, MSG-P1-018, POST /admin/trackers/{trackerId}/loads, POST /admin/trackers/{trackerId}/sign-off |
| Removed objects | tracker_row |
| Requirement | REQ-RDF-006 removed from system scope |

---

### A2.9 Retire a local tracker copy

**Removed by D-RCV-35 — later home: Cutover plan.**

| Item | Value |
|---|---|
| Feature | FEAT-RDF-09 |
| Decision | D-RCV-35 (U5) |
| Story | RWB-E1-012, removed |
| Later home | Cutover plan: the team confirmation, the parallel period, the archive location and the retirement report move to the cutover retirement procedure |
| Withdrawn IDs | VR-P1-009-1, BR-P1-009, AC-P1-009-01, AC-ALT-P1-009-01 to 02, AC-EXC-P1-009-01 to 06, AC-BG-P1-009-01 to 02, MSG-P1-013, MSG-P1-014, POST /admin/trackers/{trackerId}/retire, GET /admin/trackers/retirement-report |
| Requirement | REQ-RDF-006 removed from system scope |

---

### A2.10 Run data quality rules on every load

**Removed by D-RCV-35 — later home: ACE ingestion.**

| Item | Value |
|---|---|
| Feature | FEAT-RDF-10 |
| Decision | D-RCV-35 (U1) |
| Story | RWB-E1-006, removed |
| Later home | ACE ingestion checks (RWB-ACE-001). The 98 load checks in Data Quality and Reconciliation Rules v3 are marked moved to ACE ingestion. The daily gate moves into FEAT-RDF-14 (A2.14): no data job starts until the ACE batch is complete |
| What this module does instead | Runs the reconciliations REC-01 to REC-05 (A2.11) and reports the quality measures on Workbench records and on the views the screens read (A2.12) |
| Withdrawn IDs | VR-P1-010-1, BR-P1-010, AC-P1-010-01, AC-ALT-P1-010-01 to 02, AC-EXC-P1-010-01 to 04, AC-BG-P1-010-01 to 02, Workbench rules DQ01 to DQ11, rule version DQR-2026.11, MSG-P1-015 |
| Removed objects | dq_rule, dq_exception |

---

### A2.11 Reconcile rwb-case account keys to ACE daily

**P1 developer readiness (27 November 2026).** Where the tables and criteria below name the case list, case_list_row or a publish hold, read the rwb-case account-key set; P1 holds no case list. PASS means an absolute variance percent of at most recon.tolerance.pct (0.00); there is no NOT_RUN result.

#### A2.11.1 Intent

**Business objective.** P1 writes daily reconciliation results for ACE account facts and rwb-case keys. P1 does not build, publish or hold the case list.

**Problem.** An account that reaches 90 days past due in ACE and has no case is recovery work nobody does. A business key with no ACE row means a broken link, and there is no foreign key to catch it.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Case list reconciled to ACE with no unexplained variance | 100 percent of days (DL25) | reconciliation_result | Monthly |

#### A2.11.2 Description

**Functional overview.** ReconciliationWorkflow is a child of AceIngestCheck after the ALS stamp. REC-01 waits for rwb-case allocation until `caselist.allocation.wait.until`. REC-01 and REC-05 use the paged rwb-case key-list read; its path remains Pending, owner rwb-case service owner, tracked as NEW-GAP-B2. The exact business-date match for current `v_ace_account.data_as_of` remains Pending, owner Data architect, tracked as NEW-GAP-W8-004.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: AceDataReady for ALS and JOB-02 complete | Reads the tolerance version in force |
| 2 | System | Runs REC-01 count, REC-02 balance and REC-05 business-key resolution | Applies the tolerances |
| 3 | System | Records the result | Writes reconciliation_result per check and product group; lists the breaks for the data steward; releases or holds the publish (A2.13) |

| Check | ACE side, read through a view | Workbench side | Compared on | Tolerance |
|---|---|---|---|---|
| REC-01 | Accounts at 90 days past due or more in v_ace_account, less the accounts excluded at entry | rwb-case account-key set after allocation (paged path Pending: NEW-GAP-B2) | Count by product | Zero unexplained |
| REC-02 | Balances in v_ace_account | P1 account facts associated with rwb-case account keys | Sum by product | Zero |
| REC-05 | v_ace_account, v_ace_customer, v_ace_asset and v_ace_payment | Every account_key, person_key, asset_key and payment_code on a Workbench table | Business key, count and amount | Zero orphans; every one listed |

**Integration points.** ACE database (v_ace_account, v_ace_customer, v_ace_asset, v_ace_payment, v_ace_batch_status)

**Prerequisites.** FEAT-RDF-01, FEAT-RDF-14

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-011-1 | Data product stale when the ACE batch is late or failed | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-011 | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR-P1-011-2 | The reconciliation reads ACE for the business date of the ACE batch it was started by, and never a mix of two business dates | None |
| BR-P1-011-3 | A REC-05 orphan never deletes or changes a Workbench record; it is listed for the data steward and, where the row is missing in ACE, for the ACE team | None |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-011-01 | Variance under limit | ALS is COMPLETED for 2026-11-30 and rwb-case account keys are available after allocation | ReconciliationWorkflow runs as a child of AceIngestCheck | REC-01 and REC-02 results are written with variance 0 and PASS; P1 creates no case-list extract or publish status | RWB-E1-011 |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-011-01 | Variance over limit | v_ace_account and rwb-case account keys differ by 12 SSME accounts (0.41 percent) | the reconciliation step runs | REC-01 is BREAK with variance 12 and 0.41 percent; the keys are on the break list for the data steward; P1 does not set P3 case-list status | RWB-E1-011 |
| AC-ALT-P1-011-02 | Variance equal to the tolerance | the parameter recon.tolerance.pct for REC-01 is changed by a reference load to 0.10 from 2026-11-30 And the MORTGAGE variance is 0.10 percent and the SSME variance is 0.11 percent | the reconciliation step runs | the MORTGAGE result is PASS and the SSME result is BREAK | RWB-E1-011 |
| AC-ALT-P1-011-03 | Business key without an ACE row | case_party on case "RW-2026-000140" carries person_key "P0099881", which has no row in v_ace_customer | the REC-05 step runs | the REC-05 result is BREAK with 1 orphan And "case_party.person_key P0099881" is on the break list for the data steward and the ACE team And the case and its case_party row are unchanged | RWB-E1-011, RWB-E1-069 |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-011-01 | ACE batch not complete | Section B is enabled but ALS is not COMPLETED for 2026-11-30 by expected-by | the expected-by time passes | P1 does not start reconciliation; no reconciliation_result is written; the run is LATE and freshness is STALE per RD-P1-041 | RWB-E1-011 |
| AC-EXC-P1-011-02 | View unavailable during the run | v_ace_account returns an error after the MORTGAGE count is read | the reconciliation step runs | no reconciliation_result for 2026-11-30 is written And the job record shows FAILED with MSG-GEN-006 for system "ACE database" And the rerun from the job monitor writes all six rows | RWB-E1-011 |
| AC-EXC-P1-011-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-011-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-011-01 | ACE data ready (EV-26 AceDataReady) | v_ace_batch_status shows the ALS batch COMPLETED for the business date | Daily, on the ACE batch | Stamps freshness and starts JOB-02, JOB-04, JOB-07 and JOB-08 | Data products current by 08:00 | Every decision uses current ACE data |
| AC-BG-P1-011-02 | Daily reconciliation (JOB-04) | AceDataReady for ALS, after JOB-02 | Daily | Compares accounts at 90 days past due in v_ace_account with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.12 Publish the daily reconciliation and freshness report

**P1 developer readiness (27 November 2026).** P1 writes reconciliation results and breaks and serves them to the console. Statements below about a case-list publish, a case-list extract or a data lake copy are nonnormative for P1.

#### A2.12.1 Intent

**Business objective.** Produces the daily report of reconciliation results, the freshness of each data product and the data quality measures, for the data steward.

**Problem.** A break or a stale product that nobody sees is a wrong decision waiting to happen.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Reconciliation breaks cleared within one day | 100 percent | reconciliation_result and the break list | Monthly |

#### A2.12.2 Description

**Functional overview.** The publish step of JOB-04 writes the data quality extract for the business date. Power BI refreshes from it at 07:30. The source-data checks now run in ACE ingestion and are not reported here.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the reconciliation step of JOB-04 completes | Reads the measure definitions in force |
| 2 | System | Builds the extract: REC results by product, freshness of the 14 data products from data_product_load, quality measures | Applies the rules |
| 3 | System | Records the result | Writes the extract to the data lake; the job monitor records the run |

| Measure | Meaning | Target |
|---|---|---|
| Completeness | Mandatory fields filled on the Workbench tables and in the views the screens read | 99.9 percent |
| Validity | Codes in their lists, including the ACE lists read through v_ace_efs_action_code and v_ace_product | 99.5 percent |
| Timeliness | The ACE batch for the business date is complete when the Workbench reads it | 99 percent of days |
| Accuracy | Reconciliation breaks cleared within one day | 100 percent |
| Uniqueness | One case per customer per product | 100 percent |
| Referential completeness | Every business key on a Workbench table resolves to a v_ace_* row (REC-05) | 100 percent |

**Integration points.** Power BI, Data lake

**Prerequisites.** FEAT-RDF-11, FEAT-RDF-14

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-012-1 | Data product stale when the ACE batch is late or failed | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner, Reporting and BI analyst | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-012-01 | Report published | the six REC-01 and REC-02 results for 2026-11-30 are PASS And data_product_load shows DP01, DP02, DP05, DP07, DP11 and DP13 LOADED for 2026-11-30 and DP06 LOADED for 2026-11-27 | the publish step of JOB-04 writes the data quality extract for 2026-11-30 | the extract holds the REC results by product, the freshness of the 14 data products and the six quality measures And the report after the 07:30 refresh shows all three products green and every data product with its business date and load time | RWB-E1-011 |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-012-01 | Break rows on the report | the REC-01 result for SSME on 2026-11-30 is BREAK with 12 account keys | the report refreshes at 07:30 | the report shows SSME red with the 12 account keys and their v_ace_account days past due And MORTGAGE and HIRE_PURCHASE green | RWB-E1-011 |
| AC-ALT-P1-012-02 | Referential completeness reported | REC-05 for 2026-11-30 found 3 case_account rows whose account_key has no row in v_ace_account | the report refreshes at 07:30 | the referential completeness measure is below target And the 3 keys are listed with "missing in ACE" and the ACE team as the second owner | RWB-E1-011 |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-012-01 | ACE batch not complete | the ALS batch for 2026-11-30 is not COMPLETED in v_ace_batch_status | the report refreshes at 07:30 | the report shows every product as not run with the reason "DP01 is from 2026-11-27" And DP01 shows STALE | RWB-E1-011 |
| AC-EXC-P1-012-02 | Data lake unavailable | the data lake load area does not answer | the publish step runs | the extract is held and an alert goes to the operations channel with MSG-GEN-006 naming "Data lake" And the extract is sent by the next run | RWB-E1-011 |
| AC-EXC-P1-012-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-012-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-012-01 | ACE data ready (EV-26 AceDataReady) | v_ace_batch_status shows the ALS batch COMPLETED for the business date | Daily, on the ACE batch | Stamps freshness and starts JOB-02, JOB-04, JOB-07 and JOB-08 | Data products current by 08:00 | Every decision uses current ACE data |
| AC-BG-P1-012-02 | Daily reconciliation (JOB-04) | AceDataReady for ALS, after JOB-02 | Daily | Compares accounts at 90 days past due in v_ace_account with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.13 Retired from P1 by RD-P1-024


**Status.** This former P1 feature is withdrawn. P3 rwb-case owns case-list publication, publish status and case-list checks. The following legacy details are nonnormative for P1.

#### A2.13.1 Intent

**Business objective.** Stops the case list being published when the reconciliation difference is over tolerance, and lists the breaks.

**Problem.** A case list that does not match ACE sends teams to work the wrong accounts.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Case list published only when reconciled | 100 percent of days | case_list_row.publish_status and reconciliation_result | Monthly |

#### A2.13.2 Description

**Functional overview.** After the reconciliation step, JOB-04 sets the publish status of the case list rows for the business date to RELEASED when every REC-01 and REC-02 result is PASS, and to HELD otherwise. A held list keeps the lake on the previous released date.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the reconciliation step completes | Reads the results for the business date |
| 2 | System | Holds or releases the case list | Sets case_list_row.publish_status |
| 3 | System | Records the result | Sends MSG-P1-012 on a hold; writes the job record |

**Integration points.** ACE database, Data lake

**Prerequisites.** FEAT-RDF-11

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-013-1 | Reconciliation over tolerance | MSG-P1-012 The case list for {date} does not reconcile to ACE for {product}: a difference of {n} accounts, {pct} percent. |
| BR-P1-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-013-01 | Released when reconciled | the six REC-01 and REC-02 results for 2026-11-30 are PASS | the publish step of JOB-04 runs | every case_list_row for 2026-11-30 has publish_status RELEASED And the extract for 2026-11-30 is sent to the lake | RWB-E1-011 |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-013-01 | Held when over tolerance | the REC-01 result for SSME on 2026-11-30 is BREAK with variance 12, 0.41 percent | the publish step runs | every case_list_row for 2026-11-30 has publish_status HELD and the lake keeps the case list of 2026-11-27 And the data steward, platform administrator and team manager groups receive MSG-P1-012 "The case list for 2026-11-30 does not reconcile to ACE for SSME: a difference of 12 accounts, 0.41 percent." | RWB-E1-011 |
| AC-ALT-P1-013-02 | Variance equal to the tolerance | recon.tolerance.pct for REC-01 is 0.10 from 2026-11-30 And the MORTGAGE variance is 0.10 percent and every other result is PASS | the publish step runs | the list for 2026-11-30 is RELEASED | RWB-E1-011 |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-013-01 | Released after the break is cleared | the list for 2026-11-30 is HELD for 12 SSME accounts And JOB-02 has since created cases for the 12 accounts | the platform administrator reruns JOB-04 for 2026-11-30 from the job monitor | the REC-01 result for SSME is PASS And the list is RELEASED and sent to the lake | RWB-E1-011 |
| AC-EXC-P1-013-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-013-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-013-01 | ACE data ready (EV-26 AceDataReady) | v_ace_batch_status shows the ALS batch COMPLETED for the business date | Daily, on the ACE batch | Stamps freshness and starts JOB-02, JOB-04, JOB-07 and JOB-08 | Data products current by 08:00 | Every decision uses current ACE data |
| AC-BG-P1-013-02 | Daily reconciliation (JOB-04) | AceDataReady for ALS, after JOB-02 | Daily | Compares accounts at 90 days past due in v_ace_account with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.14 Stamp each data product with its freshness

**P1 developer readiness (27 November 2026).** A stamp row is written only when every source mapped to the product in data_product_source is COMPLETED; only RWB-P1-E1015-APP writes data_product_load. Where text below differs, RD-P1-041 and RD-P1-043 apply.

#### A2.14.1 Intent

**Business objective.** Writes the freshness stamp of each data product in `data_product_load` from the ACE batch record, so a decision carries the age of the data it used. Gates the daily data jobs on a complete ACE batch; this gate replaces the daily gate of the retired load checks.

**Problem.** The Workbench no longer loads, so it cannot time its own load. Without the ACE batch record, it cannot tell today's data from Friday's.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| ACE batch complete when the Workbench reads it | 99 percent of days | v_ace_batch_status and data_product_load | Monthly |

#### A2.14.2 Description

**Functional overview.** ACE writes one `ace_batch_run` row per source system and business date (RWB-ACE-001). The module reads it through `v_ace_batch_status`. When a source batch completes, EV-26 AceDataReady is raised: the stamp of every data product fed by that source is written, and the data jobs for the business date start. When the cut-off for a product (`data_product.expected_by`) passes before its batch completes, or the batch fails, EV-27 AceDataLate is published and the product is flagged STALE.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a new or changed row in v_ace_batch_status, or a product cut-off | Reads the product-to-source map in force |
| 2 | System | Writes or updates the data_product_load stamp | Raises EV-26 or publishes EV-27 |
| 3 | System | Records the result | Starts JOB-02, JOB-04, JOB-07 and JOB-08 on ALS ready; alerts the data steward on late |

| Data product | Source systems in v_ace_batch_status |
|---|---|
| DP01 Account and arrears | ALS |
| DP02 Customer and party | SCBPDM |
| DP05 Contact and promises | EFS |
| DP06 Collateral and assets | CCMS, SVAF, AMIS, RPS |
| DP07 Legal events and cases | LIT, WIN |
| DP11 Scores and route economics | COLLINS |
| DP13 Money and closure | ALS, GL |
| DP03, DP04, DP08, DP09, DP10, DP12, DP14 | None; Workbench records, current on change |

| data_product_load field | From v_ace_batch_status |
|---|---|
| product_code | The product-to-source map above |
| source_system | source_system |
| business_date | business_date |
| source_extracted_at | started_at (OQ-P1-04) |
| loaded_at | completed_at |
| status | LOADED when is_complete; STALE on EV-27 |
| stale_flagged_at | Time EV-27 was published |
| duplicate_count | Repeat reads of the same COMPLETED row, ignored and counted |

**Integration points.** ACE database (v_ace_batch_status); outbox (EV-26, EV-27)

**Prerequisites.** FEAT-RDF-02; RWB-ACE-001 (v_ace_batch_status is a Section B view; OQ-P1-01, OQ-P1-02)

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-014-1 | Data product stale when the ACE batch is late or failed | MSG-P1-001 {product} is from {date}. Today's load has not arrived. Pending: wording when the product has never been stamped, owner Error and Message Standard owner (NEW-GAP-D2). |
| BR-P1-014 | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR-P1-014-2 | Freshness is read from v_ace_batch_status only. The Workbench never infers it from a row count, a file or a view's data_as_of | None |
| BR-P1-014-3 | A product fed by more than one source is stamped for a business date only when every mapped source is COMPLETED for that date; the stamp in use is the greatest stamped business date, and it is STALE when the expected date has no complete set by expected_by or a source reads FAILED (RD-P1-041) | None |
| BR-P1-014-4 | A data job for a business date starts only when DailyCompletenessGate answers COMPLETE: every source mapped to a DAILY product read by JOB-02, JOB-04, JOB-07 or JOB-08 is COMPLETED for the date. Event-started daily runs start on ALS/COMPLETED AceDataReady. JOB-02 is rwb-case, JOB-07 is rwb-payment, and JOB-08 is rwb-integration (RD-P1-003, RD-P1-041, RD-P1-066) | None |
| BR-P1-014-5 | Every decision log entry records, in its inputs snapshot, the product, business date, load time and status of each data product it read | None |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Data steward and data product owner | Also uses |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-014-01 | Freshness from the ACE batch | v_ace_batch_status holds source "ALS", business date 2026-11-30, started 2026-11-30T23:30+07:00, completed 2026-12-01T05:40+07:00, status COMPLETED and record count 184,500 And loan account "ACC-SYN-000101" in v_ace_account has data_as_of 2026-11-30 | EV-26 AceDataReady is processed and GET /data-products/freshness?product=DP01 is called | data_product_load holds DP01 for 2026-11-30 with source time 2026-11-30T23:30+07:00, load time 2026-12-01T05:40+07:00 and status "LOADED" And FreshnessQuery.stampForRow("DP01", 2026-11-30) returns the same stamp And JOB-02, JOB-04, JOB-07 and JOB-08 are started for 2026-11-30 | RWB-E1-015 |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-014-01 | Stale product flagged at the cut-off | no COMPLETED ALS row for 2026-11-30 is in v_ace_batch_status at 08:00 on 2026-12-01, the DP01 expected-by time | the cut-off passes | EV-27 AceDataLate is in the outbox with sourceSystem "ALS", businessDate 2026-11-30 and the latest status And DP01 is "STALE" with stale_flagged_at 2026-12-01T08:00+07:00 And the alert goes to the data steward and the operations channel And the case record view shows "Account and arrears is from 2026-11-27. Today's load has not arrived." | RWB-E1-015 |
| AC-ALT-P1-014-02 | Freshness in the decision log | a decision log entry for case "RW-2026-000101" read DP01 for 2026-11-30 and DP06 for 2026-11-23 | the entry and its inputs snapshot are read | the snapshot lists DP01 with load time 2026-12-01T05:40+07:00 and status "LOADED" And the snapshot lists DP06 with load time 2026-11-24T04:40+07:00 and status "LOADED" | RWB-E1-015 |
| AC-ALT-P1-014-03 | Product with several sources | for DP06, v_ace_batch_status shows CCMS COMPLETED for 2026-11-27 and SVAF COMPLETED only up to 2026-11-20 | the MON 08:00 cut-off passes on 2026-11-30 | DP06 carries business date 2026-11-20 and status "STALE" And EV-27 names sourceSystem "SVAF" | RWB-E1-015 |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-014-01 | A failed ACE batch marks the product stale at once | v_ace_batch_status shows ALS for 2026-11-30 with status FAILED at 05:20 | the row is read | DP01 is "STALE" from 05:20 and EV-27 is published And the stamp for business date 2026-11-27 stays the one in use And no data job is started for 2026-11-30 | RWB-E1-015 |
| AC-EXC-P1-014-02 | A late batch clears the stale flag | DP01 was flagged "STALE" at 08:00 on 2026-12-01 | the ALS batch for 2026-11-30 completes at 08:40 | EV-26 is raised And DP01 is "LOADED" with load time 2026-12-01T08:40+07:00 And JOB-02, JOB-04, JOB-07 and JOB-08 start for 2026-11-30 | RWB-E1-015 |
| AC-EXC-P1-014-03 | The same batch read twice | the DP01 stamp for 2026-11-30 is LOADED | the same COMPLETED ALS row is read again | data_product_load still holds one DP01 row for 2026-11-30 with duplicate_count 1 And no second EV-26 is processed and no data job starts twice | RWB-E1-015 |
| AC-EXC-P1-014-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-014-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-014-01 | ACE data ready (EV-26 AceDataReady) | v_ace_batch_status shows a source batch COMPLETED for the business date | On each ACE batch | Stamps the products of that source; on ALS starts JOB-02, JOB-04, JOB-07 and JOB-08 | Data products current by their expected-by time | Every decision uses current ACE data |
| AC-BG-P1-014-02 | Daily reconciliation (JOB-04) | AceDataReady for ALS, after JOB-02 | Daily | Compares accounts at 90 days past due in v_ace_account with open cases | Breaks listed for the data steward | No account is left without a case |
| AC-BG-P1-014-03 | ACE data late (EV-27 AceDataLate) | The expected-by time of a product passes with its source batch not COMPLETED, or the batch FAILED | Each cut-off | Flags the product STALE and alerts the data steward | The stale date is shown wherever the product is read | No decision uses old data without saying so |

---

### A2.15 Set access control per data product for PDPA

**P1 developer readiness (27 November 2026).** P4 rwb-access owns roles, permissions and masking rules; P1 owns data_product_access, whose version DPA-2026.11 holds seven rows including the RW-COMPLY read of DP02.

DP02 records expose contactKey, contactType, consentStatus and verifiedAt only. GET /customers/{personKey} serves customer and contact facts under FieldMasker. Pending: masking rule rows for clear firstName, lastName and the ADDRESS contactValue, city, postCode and country, selected by contactKey, owner data protection officer with the rwb-access owner (NEW-GAP-D1). Every case-record, data-product, customer and authorise read is written to the access log only. Only a decision under DP-03 emits DecisionRecorded. A decision with caseId becomes a DECISION_TAKEN interaction. Screening-agent call-note summary is masked. Pending: agent unmasking rule, owner data protection officer (NEW-GAP-F03-2).

#### A2.15.1 Intent

**Business objective.** Sets who can read each data product and which fields are masked, under the PDPA minimization rule, across the views and the extension tables.

**Problem.** Personal data now comes straight from ACE through the views. There is no load-time tokenization, so the controls are the view, the grant, role masking (E1-037) and the PII access log.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Personal field reads logged | 100 percent | PII access log | Monthly |

#### A2.15.2 Description

**Functional overview.** The data steward loads access rows by role and data product (`data_product_access`) and masking rows by role and field ID (`masking_rule`), each versioned. The identity number is masked in `v_ace_customer` itself. Phone, email and address come in full from `v_ace_contact`, because notices and calls need them, and are masked at the API by role.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Data steward and data product owner | Opens the access screen and sets access control per data product for PDPA | Checks the role, the capability area and the scope |
| 2 | Data steward and data product owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the access version and the decision log entry |

**Integration points.** ACE database, ACE sign-in; Entra ID group mapping read through v_ace_iam_group

**Prerequisites.** FEAT-RDF-02

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-015-1 | Reference load refused at a check | MSG-P1-002 The {source} load for {date} was refused: {check}. The previous load is still in use. |
| BR-P1-015 | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR-P1-015-2 | A personal field with no masking row for the role is returned masked | None |
| BR-P1-015-3 | The clear identity number is never returned; only id_no_masked and id_no_last4 exist in the view | None |
| BR-P1-015-4 | A personal field is not returned when the PII access log cannot be written | None |

##### A2.15.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| v_ace_customer.cif_no | Customer number, from customer.person_key (DF-ACE-055) | varchar(255) | Yes | None | Yes |
| v_ace_customer.first_name | First name (DF-ACE-057) | varchar(255) | No | None | Yes |
| v_ace_customer.last_name | Last name, from customer.surname (DF-ACE-058) | varchar(255) | No | None | Yes |
| v_ace_customer.date_of_birth | Date of birth (DF-ACE-059) | date | No | None | Yes |
| v_ace_customer.id_no_masked | Identity number masked to the last four (DF-ACE-073) | varchar(255) | No | None | Yes |
| v_ace_contact.contact_value | Full phone, email or address, for notices and calls (DF-ACE-078) | varchar(256) | No | None | Yes |
| v_ace_contact.contact_value_masked | Display mask of the contact value (DF-ACE-079) | varchar(255) | No | None | Yes |
| party_ext.vulnerable | Vulnerable customer flag (DF-EXT-002) | boolean | Yes | None | Yes |
| data_product_access.role_code | Role the row applies to | varchar(20) | Yes | None | No |
| data_product_access.can_read | True when the role may read the product | boolean | Yes | None | No |
| masking_rule.field_id | Field the masking row applies to | varchar(16) | Yes | None | No |
| masking_rule.unmasked | True when the role sees the field unmasked | boolean | Yes | None | No |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| Data steward and data product owner | Primary |
| Compliance and PDPA officer, Security administrator | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-015-01 | Role access | user "u-audit-01" holds read-only role RW-AUDIT, which reads DP02 And the customer on case "RW-2026-000102" has identity number "1234567890123" in ACE and mobile "0812345678" | the user calls GET /data-products/DP02/records?caseId=RW-2026-000102 | the mobile number shows as "******5678" and the identity number as "*********0123" And no response field holds the clear identity number And the PII access log holds one entry with user "u-audit-01", product "DP02", case "RW-2026-000102" and the time of the read | RWB-E1-016 |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-015-01 | Unmasked for a role that needs it | masking version "MSK-2026.11" gives RW-NOTICE unmasked on DF-ACE-078 contact_value | a notice officer reads the address for a notice on case "RW-2026-000102" | the full address is returned And the read is in the PII access log | RWB-E1-016 |
| AC-ALT-P1-015-02 | Access denied | user "u-phone-01" holds RW-PHONECOL, which has no access row for DP06 | the user calls GET /data-products/DP06/records?caseId=RW-2026-000102 | the call is refused with status 403 and MSG-P4-002 And the refusal is written to the access log with user "u-phone-01" and product "DP06" | RWB-E1-016 |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-015-01 | An access load with an unknown role is refused | an access load version "DPA-2026.12" with a row for role "RW-UNKNOWN" and product "DP02" | the load is validated | the load is refused whole with MSG-P1-002 and check "unknown role RW-UNKNOWN" And version "DPA-2026.11" stays in force | RWB-E1-016 |
| AC-EXC-P1-015-02 | No masking rule loaded keeps every personal field masked | user "u-comply-01" holds RW-COMPLY, which reads DP02 and has no masking row | the user calls GET /data-products/DP02/records?caseId=RW-2026-000102 | first_name, last_name, cif_no, date_of_birth and the contact value are returned masked | RWB-E1-016 |
| AC-EXC-P1-015-03 | The PII access log is unavailable | the PII access log rejects every write | user "u-audit-01" calls GET /data-products/DP02/records?caseId=RW-2026-000102 | the call is refused with status 503 and MSG-GEN-006 for system "PII access log" And no personal field is returned | RWB-E1-016 |
| AC-EXC-P1-015-04 | An access row not yet in force | access version "DPA-2026.12" gives RW-PHONECOL read on DP06 from 2026-12-15 And today is 2026-12-14 | user "u-phone-01" calls GET /data-products/DP06/records?caseId=RW-2026-000102 | the call is refused with status 403 and MSG-P4-002 | RWB-E1-016 |
| AC-EXC-P1-015-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-015-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-015-01 | ACE data ready (EV-26 AceDataReady) | v_ace_batch_status shows the ALS batch COMPLETED for the business date | Daily, on the ACE batch | Stamps freshness and starts JOB-02, JOB-04, JOB-07 and JOB-08 | Data products current by 08:00 | Every decision uses current ACE data |
| AC-BG-P1-015-02 | Daily reconciliation (JOB-04) | AceDataReady for ALS, after JOB-02 | Daily | Compares accounts at 90 days past due in v_ace_account with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.16 Maintain the data catalog entry per data product

#### A2.16.1 Intent

**Business objective.** Keeps the catalog entry for each data product: definition, owner, system of record, the views and tables behind it, refresh, reconciliation rules and access. The data dictionary covers the views and the extension tables as well as the recovery tables.

**Problem.** A developer must be able to see that `days_past_due` comes from `public.account.delay_days` through `v_ace_account`, and must never go looking in `public`.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Objects and fields in the dictionary | 122 objects and 1,366 fields, matched to the schema | Conformance test; v_data_dictionary | Each release |

#### A2.16.2 Description

**Functional overview.** The dictionary is `sys_objects` (one row per table or view) and `sys_fields` (one row per field), read through `v_data_dictionary`. A view field carries source system "ACE" and its ACE source column as source field. An extension field carries source system "Workbench". The catalog entry joins the dictionary to `data_product`, `data_product_access` and `retention_rule`.

| Object kind | Objects | Fields | Source system |
|---|---:|---:|---|
| Recovery tables (Tiers 3 and 4) | 92 | 1,062 | Workbench |
| of which extension tables | 4 | 49 | Workbench |
| Section A views | 16 | 177 | ACE |
| Section B views | 14 | 127 | ACE |
| **Total** | **122** | **1,366** | |

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Data steward and data product owner | Opens the catalog and maintains the entry for a data product | Checks the role, the capability area and the scope |
| 2 | Data steward and data product owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the catalog version and the decision log entry |

**Integration points.** ACE database

**Prerequisites.** FEAT-RDF-02

#### A2.16.3 Business rules and structure

##### A2.16.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-016-1 | Data product stale when the ACE batch is late or failed | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| VR-P1-016-2 | Reference load refused at a check | MSG-P1-002 The {source} load for {date} was refused: {check}. The previous load is still in use. |
| BR-P1-016 | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR-P1-016-2 | A view field is named for the Workbench; the ACE name appears only as its source field and in the STTM | None |

##### A2.16.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| sys_objects.object_name | Table or view name, for example v_ace_account | varchar | Yes | None | No |
| sys_objects.subject_area | Subject area; ACE for a v_ace_* view | varchar | Yes | None | No |
| sys_objects.data_product | Data product the object belongs to; empty for OPS, AGT and RPT objects | varchar(25) | No | LOV-DATA-PRODUCT | No |
| sys_objects.system_of_record | ACE for a view; Workbench for a table | varchar | Yes | None | No |
| sys_fields.field_id | Field ID, for example DF-ACE-018 or DF-EXT-005 | varchar | Yes | None | No |
| sys_fields.source_system | ACE or Workbench | varchar | Yes | None | No |
| sys_fields.source_field | ACE source column of a view field, for example public.account.delay_days | varchar | No | None | No |
| sys_fields.is_personal | True for a personal data field | boolean | Yes | None | No |

##### A2.16.3.3 Roles and permissions

| Role | Use |
|---|---|
| Data steward and data product owner | Primary |
| Center of excellence analyst | Also uses |

#### A2.16.4 Acceptance criteria

##### A2.16.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-016-01 | Catalog entry with views and extension tables | the catalog and dictionary in force | a data steward calls GET /admin/data-products/DP01 | the entry lists the views v_ace_account, v_ace_payment, v_ace_aa_relation, v_ace_bucket_log, v_ace_product and v_ace_branch with system of record "ACE", and account_ext with system of record "Workbench" And the field days_past_due shows field ID "DF-ACE-018", source system "ACE" and source field "public.account.delay_days" And the entry shows owner role, system of record "ACE (ingested from ALS)", refresh cycle, expected-by time, retention class, REC-01 and REC-02, and the access rows | RWB-E1-016 |

##### A2.16.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-016-01 | All 14 entries | the 14 data products DP01 to DP14 | a data steward calls GET /admin/data-products | 14 entries are returned And each has an owner role, a system of record, a refresh cycle, an expected-by time, a retention class and the field list with PDPA tags | RWB-E1-016 |
| AC-ALT-P1-016-02 | Dictionary totals | V0001, V0002 and V0003 applied | a developer counts v_data_dictionary by source system | 1,366 fields over 122 objects are returned: 304 view fields with source system "ACE" and 1,062 table fields with source system "Workbench", 49 of them on the four extension tables | RWB-E1-016, RWB-E1-069 |

##### A2.16.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-016-01 | View column without a dictionary entry fails the build | a branch that adds the column special_memo_2 to v_ace_account with no sys_fields row | the conformance test runs in the pipeline | the test fails with "v_ace_account.special_memo_2 has no data dictionary entry" | RWB-E1-016 |
| AC-EXC-P1-016-02 | A view marked as Workbench is refused | a catalog update that sets system of record "Workbench" on v_ace_customer | the reference data administrator loads it | the load is refused whole with MSG-P1-003 for v_ace_customer | RWB-E1-016 |
| AC-EXC-P1-016-03 | Unknown data product refused | a catalog update that names data product "DP15" for valuation_ext | the load is validated | the load is refused whole with MSG-P1-002 and check "unknown data product DP15" | RWB-E1-016 |
| AC-EXC-P1-016-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-016-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.16.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-016-01 | ACE data ready (EV-26 AceDataReady) | v_ace_batch_status shows the ALS batch COMPLETED for the business date | Daily, on the ACE batch | Stamps freshness and starts JOB-02, JOB-04, JOB-07 and JOB-08 | Data products current by 08:00 | Every decision uses current ACE data |
| AC-BG-P1-016-02 | Daily reconciliation (JOB-04) | AceDataReady for ALS, after JOB-02 | Daily | Compares accounts at 90 days past due in v_ace_account with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.17 Apply the retention and archive rule to the data store

**P1 developer readiness (27 November 2026).** rwb-document owns the retention rules and starts the P1 run with POST /retention-runs; P1 checks holds with the rwb-case retention-exclusions read. Periods are Pending, owner Compliance (GAP-1029); the proposed values are data only. P1 scope is interaction (ARCHIVE) and six REVIEW tables; no destruction step is built. Age is measured from the case closure date of rwb-case, not from a 24-month occurred_at value.

#### A2.17.1 Intent

**Business objective.** Applies the retention class to each Workbench table and archives records past their period. Source data read through the views stays under ACE's retention.

**Problem.** Workbench records kept past their period break PDPA. A Workbench job that tried to archive ACE data would break the boundary rule.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Workbench records past retention archived or on legal hold | 100 percent each month | JOB-17 run record | Monthly |

#### A2.17.2 Description

**Functional overview.** The compliance officer loads retention rows by data product and table (`retention_rule`), each versioned and approved. JOB-17 runs monthly on the first Sunday.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Compliance and PDPA officer | Opens the retention screen and applies the retention and archive rule to the data store | Checks the role, the capability area and the scope |
| 2 | Compliance and PDPA officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the rule version and the decision log entry; JOB-17 applies it |

**Integration points.** ACE database (recovery schema only), archive container

**Prerequisites.** FEAT-RDF-01

#### A2.17.3 Business rules and structure

##### A2.17.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-017-1 | Reference load refused at a check | MSG-P1-002 The {source} load for {date} was refused: {check}. The previous load is still in use. |
| BR-P1-017 | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR-P1-017-2 | A retention row names a recovery table only. A v_ace_* view or a public table is refused, because ACE applies its own retention. decision_log_entry is never archived by the retention job | None |

##### A2.17.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| retention_rule.product_code | Data product the rule applies to (DF-REF-117) | varchar(25) | Yes | LOV-DATA-PRODUCT | No |
| retention_rule.table_name | Recovery table the rule applies to, from sys_objects (DF-REF-118) | varchar(60) | Yes | None | No |
| retention_rule.record_class | Retention class from LOV-RETENTION (DF-REF-119) | varchar(20) | Yes | None | No |
| retention_rule.retention_months | Retention period in months, 1 to 600 (DF-REF-120) | integer | Yes | None | No |
| retention_rule.age_basis_field | Field the age is measured from, for example interaction.occurred_at (DF-REF-121) | varchar(60) | Yes | None | No |
| retention_rule.end_action | Archive or review at the end of the period (DF-REF-122) | varchar(12) | Yes | LOV-RETENTION-END | No |
| retention_rule.rule_version | Version, for example RET-2026.11 (DF-REF-123) | varchar(20) | Yes | None | No |
| retention_rule.valid_from | Date the version comes into force (DF-REF-124) | date | Yes | None | No |

##### A2.17.3.3 Roles and permissions

| Role | Use |
|---|---|
| Compliance and PDPA officer | Primary |
| Data steward and data product owner | Also uses |

#### A2.17.4 Acceptance criteria

##### A2.17.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-017-01 | Retention rule applied | 1,250 interaction rows with occurred_at before 2024-12-06 and 4,800 rows from 2024-12-06 onward | JOB-17 runs | 1,250 rows move to the archive container under "retention/2026-12-06/interaction/" And the 1,250 rows are no longer in the live interaction table And the job run logs count 1,250 for DP05 interaction under rule version "RET-2026.11" And no row in v_ace_efs_action changes | RWB-E1-017 |

##### A2.17.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-017-01 | Rule changed as data | retention rule version "RET-2027.01" changes DP05 interaction to 36 months, approved and valid from 2027-01-01 And interaction rows with occurred_at on 2024-01-15 and on 2023-12-20 | JOB-17 runs on Sunday 2027-01-03 | the row from 2024-01-15 stays in the live table And the row from 2023-12-20 moves to the archive container And the job run logs rule version "RET-2027.01" | RWB-E1-017 |
| AC-ALT-P1-017-02 | Legal hold | case "RW-2024-000311" is marked legal hold and has 40 interaction rows older than 24 months | JOB-17 runs | its 40 rows are kept in the live table And the hold report lists case "RW-2024-000311" with 40 rows kept And the summary alert to Compliance reads MSG-P1-020 with 1 case on legal hold kept | RWB-E1-017 |

##### A2.17.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-017-01 | The archive write fails | the archive container refuses writes | JOB-17 runs | no interaction row is deleted And the job run ends "FAILED" with MSG-GEN-006 for system "Archive container" | RWB-E1-017 |
| AC-EXC-P1-017-02 | A repeat run in the same month | JOB-17 archived 1,250 rows on 2026-12-06 | JOB-17 is rerun on 2026-12-06 | 0 rows are archived And the archive container still holds one set of the 1,250 rows | RWB-E1-017 |
| AC-EXC-P1-017-03 | A rule for the decision log is refused | a retention load version "RET-2026.12" with a row for product "DP12", table "decision_log_entry" | the load is validated | the load is refused whole with MSG-P1-002 and check "decision_log_entry is not archived by the retention job" | RWB-E1-017 |
| AC-EXC-P1-017-04 | A rule for an ACE view is refused | a retention load version "RET-2026.12" with a row for product "DP05", table "v_ace_efs_action" | the load is validated | the load is refused whole with MSG-P1-002 and check "v_ace_efs_action is ACE data; ACE applies its own retention" | RWB-E1-017 |
| AC-EXC-P1-017-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-017-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.17.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-017-01 | Retention job (JOB-17) | First Sunday of the month | Monthly | Applies the retention rules in force to the recovery tables | Records past retention archived or kept on legal hold | PDPA retention |
| AC-BG-P1-017-02 | Daily reconciliation (JOB-04) | AceDataReady for ALS, after JOB-02 | Daily | Compares accounts at 90 days past due in v_ace_account with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.18 Retired from P1 by RD-P1-024


**Status.** This former P1 feature is withdrawn. P3 rwb-case owns the case list; P1 does not create its rows, screen, extract or operations. The following legacy details are nonnormative for P1.

#### A2.18.1 Intent

**Business objective.** Gives every recovery team one list of all 90 plus days past due accounts across Mortgage, HP and SSME, built from the cases and `v_ace_account`.

**Problem.** Teams kept their own lists in spreadsheets. The case list replaces them with one list that is checked against ACE every day.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Case list built and released by 07:30 | 99 percent of days | case_list_row.refreshed_at and publish_status | Monthly |

#### A2.18.2 Description

**Functional overview.** The case list step of JOB-04 runs after AceDataReady for ALS and JOB-03 allocation. It writes one `case_list_row` per case account for the business date. Balance and days past due come from `v_ace_account`; last contact and action code come from `v_ace_efs_action`; case, owner, queue, stage and route come from the case. The link is `account_key`, with no foreign key.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the case list with case ID, owner and queue | Checks the role, the capability area and the scope |
| 2 | Case owner | Filters by team, queue and product | Shows the rows for the latest released business date with its freshness |
| 3 | System | Records the action | Writes the PII access log entry where a personal field is shown |

**Integration points.** Workbench, ACE database (v_ace_account, v_ace_efs_action, v_ace_batch_status), Data lake, Power BI

**Prerequisites.** FEAT-RDF-01, FEAT-RDF-14, FEAT-CWC-01

#### A2.18.3 Business rules and structure

##### A2.18.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-018-1 | Data product stale when the ACE batch is late or failed | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-018 | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR-P1-018-2 | The list for a business date holds one row per case account; a rerun replaces the rows of that date | None |

##### A2.18.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| case_list_row.business_date | Business date of the list, the data_as_of of v_ace_account (DF-RPT-002) | date | Yes | None | No |
| case_list_row.case_no | Case number (DF-RPT-004) | varchar(18) | Yes | None | No |
| case_list_row.account_key | ACE account key; no foreign key (DF-RPT-005) | varchar(255) | Yes | None | No |
| case_list_row.account_no | Account number, from v_ace_account.account_code (DF-RPT-006) | varchar(20) | Yes | None | No |
| case_list_row.product_group | Product group (DF-RPT-007) | varchar(15) | Yes | LOV-PRODUCT | No |
| case_list_row.status | Case status (DF-RPT-009) | varchar(20) | Yes | LOV-CASE-STATUS | No |
| case_list_row.owner_user_id | Case owner (DF-RPT-010) | uuid | No | None | No |
| case_list_row.queue_code | Queue code (DF-RPT-011) | varchar(30) | No | None | No |
| case_list_row.total_balance | Total balance, baht, from v_ace_account.total_balance (DF-RPT-014) | numeric(18,2) | Yes | None | No |
| case_list_row.days_past_due | Days past due, from v_ace_account.days_past_due (DF-RPT-015) | integer | Yes | None | No |
| case_list_row.last_contact_at | Latest contact, from v_ace_efs_action.contact_at (DF-RPT-017) | timestamptz | No | None | No |
| case_list_row.last_action_code | Action code of the latest contact (DF-RPT-018) | varchar(10) | No | LOV-ACTION-CODE | No |
| case_list_row.publish_status | Pending, held or released (DF-RPT-019) | varchar(10) | Yes | LOV-PUBLISH-STATUS | No |

##### A2.18.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Team manager, Phone collector | Also uses |

#### A2.18.4 Acceptance criteria

##### A2.18.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-018-01 | List reconciles | v_ace_account holds 28,140 accounts at 90 days past due or more with data_as_of 2026-11-30 And P3 excluded 21 of them at entry, so the ACE count to match is 28,119 And the open cases link 28,119 accounts at 90 days past due or more and 37 accounts below 90 days past due | the case list step of JOB-04 runs | case_list_row holds 28,156 rows for 2026-11-30 And REC-01 compares 28,119 with 28,119 and is PASS And the job record shows 37 rows below 90 days past due | RWB-E1-002 |

##### A2.18.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-018-01 | Columns present | the case list for 2026-11-30 is built | the extract file for 2026-11-30 is written | each row holds case number, account number, product, stage, status, owner, queue, route, total balance and days past due, in that order And each row also holds team, business date and refresh time And the Power BI data set "Case list v1" offers filters on team, queue and product And the row for case "RW-2026-000123" shows account "ACC0000123", product "MORTGAGE", status "ASSIGNED", queue "MTG-BKK-CO", total balance 1,250,000.00 and days past due 96, the values of v_ace_account for that account_key | RWB-E1-002 |
| AC-ALT-P1-018-02 | Daily refresh | the ALS batch for 2026-11-30 completed at 05:40 and JOB-03 completed at 06:52 | the case list step runs and completes at 07:12 | every row for 2026-11-30 carries refresh time 2026-12-01 07:12 And the report after the 07:30 data set refresh shows "Refreshed 1 Dec 2026 07:12, data as of 30 Nov 2026" | RWB-E1-002 |
| AC-ALT-P1-018-03 | Last contact from EFS through ACE | v_ace_efs_action holds an action "PTP" for an account of case "RW-2026-000123" with contact_at 2026-11-30 15:42 | the case list step runs | the row of case "RW-2026-000123" shows last contact 2026-11-30 15:42 and action code "PTP" | RWB-E1-002 |

##### A2.18.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-018-01 | ACE batch not complete | the ALS batch for 2026-11-30 is not COMPLETED in v_ace_batch_status | the DP01 cut-off passes | the case list step does not run and no case_list_row for 2026-11-30 is written And the lake keeps the extract file for 2026-11-27 And the team manager group receives MSG-P1-001 "DP01 Account and arrears is from 2026-11-27. Today's load has not arrived." | RWB-E1-002 |
| AC-EXC-P1-018-02 | Allocation not finished | JOB-03 for 2026-11-30 has not completed at 07:15 | the case list step starts at 07:15 | the list is built with the owner and queue as they are at 07:15 And the job record shows ALLOCATION_COMPLETE NO And the report shows "Owners and queues may be incomplete for 30 Nov 2026" | RWB-E1-002 |
| AC-EXC-P1-018-03 | Run repeated for the same date | the case list for 2026-11-30 holds 28,156 rows | the platform administrator reruns the step for 2026-11-30 | case_list_row still holds 28,156 rows for 2026-11-30 and no case account appears twice And the refresh time is the time of the rerun | RWB-E1-002 |
| AC-EXC-P1-018-04 | Case interface error | CaseQueryApi raises an error after 12,000 accounts are read | the case list step runs | no case_list_row for 2026-11-30 is written And the job record shows FAILED And the rows for 2026-11-27 are unchanged | RWB-E1-002 |
| AC-EXC-P1-018-05 | Transfer to the lake fails | the outbound file adapter fails all its retries for the 2026-11-30 extract file | the case list step completes | the job record shows COMPLETED with PUBLISHED NO And the transfer is in the exception queue with a task for the platform administrator | RWB-E1-002 |
| AC-EXC-P1-018-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-018-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.18.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-018-01 | ACE data ready (EV-26 AceDataReady) | v_ace_batch_status shows the ALS batch COMPLETED for the business date | Daily, on the ACE batch | Stamps freshness and starts JOB-02, JOB-04, JOB-07 and JOB-08 | Data products current by 08:00 | Every decision uses current ACE data |
| AC-BG-P1-018-02 | Daily reconciliation (JOB-04) | AceDataReady for ALS, after JOB-02 | Daily | Compares accounts at 90 days past due in v_ace_account with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.19 Publish baseline measures for the recovery portfolio

#### A2.19.1 Intent

**Business objective.** Calculates and publishes the starting measures the benefit model is tracked against.

**Problem.** Without a frozen baseline from checked data, nobody can show what the Workbench changed.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Baseline published from a complete ACE batch | Once, frozen | measure_snapshot | At baseline |

#### A2.19.2 Description

**Functional overview.** Calculates and publishes the starting measures the benefit model is tracked against. JOB-15 reads the cases and, through the views, the payments in `v_ace_payment`, for a business date whose ACE batches are complete.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: JOB-15 at 01:30 | Reads the measure definitions in force |
| 2 | System | Publishes baseline measures for the recovery portfolio | Applies the rules |
| 3 | System | Records the result | Writes measure_snapshot and the extract; the job monitor records the run |

**Integration points.** Power BI, Data lake, ACE database (v_ace_payment, v_ace_batch_status)

**Prerequisites.** FEAT-RDF-11, FEAT-RDF-14

#### A2.19.3 Business rules and structure

##### A2.19.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-019-1 | Data product stale when the ACE batch is late or failed | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-P1-019 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.19.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Reporting and BI analyst, Finance and CFO delegate | Also uses |

#### A2.19.4 Acceptance criteria

##### A2.19.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-019-01 | Definitions agreed | a definition file of 6 rows for "CASES_BY_ROUTE", "CASES_BY_AGE", "CASES_BY_QUEUE", "REALIZED_RECOVERY", "TIME_IN_STAGE" and "TAT_BY_ROUTE" And each row names its data product, formula, unit and approver "TRB-0001" with approval date 2026-11-20 | it is loaded with valid from 2026-11-21 | definition version "MD-2026.11" is in force with 6 measures And each measure returns its data product and formula through MeasureCatalog | RWB-E1-013 |

##### A2.19.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-019-01 | Baseline published | the ACE batches for business date 2026-11-27 are COMPLETED in v_ace_batch_status and REC-01 and REC-02 passed | JOB-15 runs at 01:30 on 2026-11-28 | measure_snapshot holds rows for business date 2026-11-27 marked baseline and frozen with definition version "MD-2026.11" And "CASES_BY_ROUTE" totals 120 cases, of which 60 are Mortgage And "REALIZED_RECOVERY" equals the sum of synthetic payments in v_ace_payment since entry, 4,350,000.00 THB | RWB-E1-013 |
| AC-ALT-P1-019-02 | Power BI data set | the baseline measures are published | JOB-15 runs at 01:30 on 2026-12-02 | the INT-19 extract for business date 2026-12-01 is in the data lake with freshness stamp 2026-12-01 and the record count in its trailer And the extract holds the baseline rows of 2026-11-27 unchanged And the job monitor records the JOB-15 run with its row count, start and end time | RWB-E1-013 |

##### A2.19.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-019-01 | Definition without a formula refused | a definition file where row "TIME_IN_STAGE" has no formula | it is loaded | the load is refused whole with MSG-GEN-001 naming "formula" And no definition version is put in force | RWB-E1-013 |
| AC-EXC-P1-019-02 | ACE batch of the baseline date not complete | the ALS batch for 2026-11-27 is FAILED in v_ace_batch_status | JOB-15 runs at 01:30 on 2026-11-28 | no baseline rows are written for 2026-11-27 And the run record shows MSG-P1-001 naming "DP01 Account and arrears" and 2026-11-26 And the baseline is published by the first JOB-15 run after the 2026-11-27 batch completes | RWB-E1-013 |
| AC-EXC-P1-019-03 | Data lake unavailable | the data lake load area does not answer | JOB-15 runs at 01:30 on 2026-11-30 | measure_snapshot rows for 2026-11-28 are written in the Workbench And the extract is held and an alert goes to the operations channel with MSG-GEN-006 naming "Data lake" And the extract is sent by the next JOB-15 run | RWB-E1-013 |
| AC-EXC-P1-019-04 | Measure with no definition in force | the extract configuration lists measure "COST_PER_CASE" with no definition in force | JOB-15 runs at 01:30 on 2026-11-30 | no value for "COST_PER_CASE" is written And the run record shows MSG-P9-003 naming "COST_PER_CASE" | RWB-E1-013 |
| AC-EXC-P1-019-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-019-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.19.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-019-01 | Reporting extract (JOB-15) | Nightly 01:30 | Daily | Writes case, queue, decision and outcome data and the measures to the data lake | Reports current to the previous business date | One set of numbers for the Tribe |
| AC-BG-P1-019-02 | Daily reconciliation (JOB-04) | AceDataReady for ALS, after JOB-02 | Daily | Compares accounts at 90 days past due in v_ace_account with open cases | Breaks listed for the data steward | No account is left without a case |

---

### A2.20 Copy the decision log to the lake

#### A2.20.1 Intent

**Business objective.** Streams decision log entries to the data lake so reporting and audit read them without touching the log store.

**Problem.** Reporting and audit reads on the live log would load the store and risk the chain.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Lake copy matches the live log (REC-08) | 100 percent of nights | lake_copy_watermark and the manifest | Monthly |

#### A2.20.2 Description

**Functional overview.** Streams decision log entries to the data lake so reporting and audit read them without touching the log store. No ACE data is copied.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: JOB-13 at 01:00 | Reads the watermark |
| 2 | System | Copies the decision log to the lake | Checks the count and last hash (REC-08) |
| 3 | System | Records the result | Moves the watermark; writes the job record |

**Integration points.** Data lake

**Prerequisites.** FEAT-DRI-01

#### A2.20.3 Business rules and structure

##### A2.20.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P1-020-1 | Copy does not match the live log | MSG-P1-019 |
| BR-P1-020 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.20.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Internal audit, Reporting and BI analyst | Also uses |

#### A2.20.4 Acceptance criteria

##### A2.20.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P1-020-01 | Daily copy | 380 entries were written on business date 2026-11-30 | JOB-13 runs at 01:00 on 2026-12-01 | the partition "business_date=2026-11-30" holds 380 rows And the manifest shows cumulative count 12,480 and last hash "a3f1...09c2" And the data lake copy has the same row count and the same last hash as the live log And the watermark moves to 12,480 and "a3f1...09c2" | RWB-E1-014 |

##### A2.20.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P1-020-01 | Retention rule | lake partitions for business dates 2024-11-29 and 2024-11-30 exist | the retention step of JOB-13 runs on 2026-12-01 | the partition "business_date=2024-11-29" moves to the archive tier And the job run records 1 partition archived under rule version "RET-2026.11" | RWB-E1-014 |
| AC-ALT-P1-020-02 | Two runs at the same time | JOB-13 is running for 2026-11-30 | a platform administrator posts a rerun of JOB-13 | the rerun is refused with status 409 and MSG-P2-006 And one run continues | RWB-E1-014 |

##### A2.20.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P1-020-01 | A copy that does not match is not published | the lake write for 2026-11-30 stops after 379 of 380 rows | the reconciliation step compares the copy with the live log | the partition is not marked complete And the watermark stays at 12,100 and "77be...41d0" And the job run shows check "REC-08" failed with MSG-P1-019 | RWB-E1-014 |
| AC-EXC-P1-020-02 | A repeat run for the same date writes no duplicates | JOB-13 completed for 2026-11-30 with 380 rows | JOB-13 is rerun for 2026-11-30 | the partition "business_date=2026-11-30" still holds 380 rows And the cumulative count stays 12,480 | RWB-E1-014 |
| AC-EXC-P1-020-03 | The decision log interface is unavailable | DecisionLogExport returns an error for every call | JOB-13 runs for 2026-11-30 | the job run ends with status "FAILED" and MSG-GEN-006 for system "Decision log" And the watermark and the previous partitions are unchanged | RWB-E1-014 |
| AC-EXC-P1-020-04 | A day with no new decisions | no entry was written after "77be...41d0" | JOB-13 runs for 2026-11-30 | the partition holds 0 rows and the manifest shows cumulative count 12,100 And check "REC-08" passes | RWB-E1-014 |
| AC-EXC-P1-020-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P1-020-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.20.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P1-020-01 | Decision log copy (JOB-13) | Nightly 01:00 | Daily | Copies new decision log entries to the lake and checks REC-08 | Lake copy equal to the live log | Audit reads without touching the log store |
| AC-BG-P1-020-02 | Hash chain check (JOB-14) | Nightly 02:00, after JOB-13 | Daily | Checks the decision log chain | Break reported to Compliance | The log cannot be changed unseen |

---

### A2.21 Run legacy feed jobs on ADF and Control-M

**Removed by D-RCV-35 — later home: ACE ingestion.**

| Item | Value |
|---|---|
| Feature | FEAT-RDF-22 |
| Decision | D-RCV-35 (U1); DL06 option A and DL12 option A superseded |
| Story | RWB-E1-051, removed |
| Later home | ACE ingestion; no ADF job remains. The source feeds are scheduled, run, restarted and contract-tested by the ACE team under RWB-ACE-001; ACE ingestion reports its status through v_ace_batch_status |
| Jobs | JOB-01 COLLINS load check and intake: retired. JOB-09 File loads: retired (Batch and Scheduling Design v3). The data jobs JOB-02, JOB-04, JOB-07, JOB-08 and JOB-16 start on the ACE batch-complete record (A2.14) |
| Withdrawn IDs | VR-P1-021-1, BR-P1-021, AC-P1-021-01, AC-ALT-P1-021-01 to 02, AC-EXC-P1-021-01 to 04, AC-BG-P1-021-01 to 02; run books for JOB-01 and JOB-09; the INT-10 and INT-11 contract tests; MSG-P2-004 for an inbound feed |
| Removed objects | interface_run for inbound runs; Control-M definitions for the ALS and EFS extracts; ADF pipelines for CCMS and SVAF |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-RDF-001 | Recovery data is held in 14 data products, each with exactly one named system of record, "ACE (ingested from X)" or the Workbench, and one named owner. | Must | E1 |
| REQ-RDF-002 | Account balance, arrears, payments and classification for every account at 90 or more days past due are read from ACE through v_ace_account and v_ace_payment, current to the previous working day. | Must | E1 |
| REQ-RDF-003 | Collections contact history, promises and case status from EFS, ingested by ACE, are read through v_ace_efs_action so that the case carries what happened before day 90. | Must | E1 |
| REQ-RDF-004 | Collateral records and appraisal values, ingested by ACE from CCMS and SVAF, are available on the case through v_ace_collateral, v_ace_collateral_detail and v_ace_valuation, without a person looking them up. | Must | E1 |
| REQ-RDF-005 | Removed from system scope by D-RCV-35 (U5) — later home: Cutover plan. | - | - |
| REQ-RDF-006 | Removed from system scope by D-RCV-35 (U5) — later home: Cutover plan. | - | - |
| REQ-RDF-007 | The case list reconciles daily to the ACE count of accounts at 90 or more days past due in v_ace_account, with no variance (DL25), and every business key on a Workbench table resolves to an ACE row.  P1 part under RD-P1-024: P1 reconciles ACE facts with the rwb-case keys; the case list is P3 rwb-case's. | Must | E1 |
| REQ-RDF-008 | Data quality checks on source data run in ACE ingestion (RWB-ACE-001). The Workbench reports reconciliation breaks, referential completeness and its quality measures, each break with a reason visible to the data product owner. | Must | E1 |
| REQ-RDF-009 | Every data product carries a freshness stamp from the ACE batch record, and every decision records the freshness of the data it used. | Must | E1 |
| REQ-RDF-010 | Access to each data product is controlled per role, and personal data is masked by role in line with PDPA; the identity number is never exposed in clear. | Must | E1 |
| REQ-RDF-011 | Every data product has a catalog entry stating its definition, owner, system of record, views and tables, refresh cycle and retention. | Must | E1 |
| REQ-RDF-012 | Baseline measures for cases by route, age and queue, realized recovery, time in stage and turnaround per route are published, with definitions agreed by the Tribe. | Must | E1 |
| REQ-RDF-013 | Workbench recovery records carry a retention and archive rule by record class; ACE data is retained by ACE. | Should | E1 |
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live. | Must | E2 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-44 Interface and job monitor | ACE batch status per source and business date, Workbench jobs and outbound actions with status and reruns | E2; E8 full |
| SCR-45 Data quality | Reconciliation breaks, referential completeness (REC-05), quality measures and stale data products | E2; E8 full |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| FSD owner, business analyst | | | |
| Business owner | | | |
| Solution architect | | | |
| QA lead | | | |

## Appendix A. Business glossary

Terms follow the Recovery Workbench Business Glossary.

| Term | Thai | Meaning |
|---|---|---|
| Score | คะแนนจากแบบจำลอง | A value COLLINS returns for an account or a case, such as a risk score or a price estimate, ingested by ACE and read through v_ace_score |
| Return by route | ผลตอบแทนตามแนวทาง | The expected recovery after cost of each route for a case |
| Party | บุคคลที่เกี่ยวข้อง | A person or company with a role on a case, held in ACE as a customer and read through v_ace_customer |
| Borrower | ผู้กู้ | The party the loan was made to |
| Co-borrower | ผู้กู้ร่วม | A party who borrowed jointly with the borrower |
| Guarantor | ผู้ค้ำประกัน | A party who guaranteed the loan |
| Heir | ทายาท | A party who represents a deceased borrower's estate |
| Vulnerable customer | ลูกหนี้กลุ่มเปราะบาง | A customer with hardship or vulnerability confirmed, treated under X2; the flag is held in party_ext |
| Contact point | ช่องทางการติดต่อ | A phone, email or address in ACE, read through v_ace_contact, with its consent and whether it works held in contact_point_ext |
| Loan account | บัญชีสินเชื่อ | An account in the core bank, ingested by ACE and read through v_ace_account |
| Days past due | จำนวนวันค้างชำระ | Days since the oldest unpaid installment fell due; ACE account.delay_days |
| Non-performing loan | หนี้ที่ไม่ก่อให้เกิดรายได้ | A loan at 90 days past due or more |
| Total balance | ยอดหนี้คงค้างรวม | Principal, interest and fees outstanding |
| Collateral | หลักประกัน | Property or a vehicle securing one or more accounts |
| ACE batch record | บันทึกรอบประมวลผลของ ACE | One row per source system and business date in ACE (ace_batch_run), read through v_ace_batch_status; the source of freshness |
| Read-only view | วิวแบบอ่านอย่างเดียว | A recovery.v_ace_* view, the only path by which the recovery module reads ACE |
| Extension table | ตารางส่วนขยาย | A Workbench table, 1:1 with an ACE record and keyed by its business key, that holds a Workbench decision about that record |
| Business key | คีย์ทางธุรกิจ | The ACE key a Workbench record links to, such as account_key or person_key, held without a foreign key |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.

## P1 developer-readiness amendments (27 November 2026)

These amendments apply the final RD-P1 rulings. They supersede earlier descriptions of P1 scope where they conflict.

- P1 is the only service that reads recovery.v_ace_*; the rwb_source_data database login has SELECT on those 30 views only. Every other service reads ACE data through the P1 contract.
- P1 does not create case_list_row, a case-list workflow, Schedule, publish status, case-list operation or case-list checks. P3 rwb-case owns the case list. RWB-P1-E1002-APP builds the account-page read; RWB-P1-E1015-CON publishes it. RWB-P1-E1002-CON is retired with a pointer and RWB-P1-E1002-OPS is a delta. The path and maximum keys per call are Pending, owner Solution architect, tracked as NEW-GAP-B3.
- contact_point_ext is DP02 and its cutover writer is RWB-P1-DM005-APP. RWB-P1-DM002-APP is read-only for this table; its cardinality is zero or one row per contact_key, and an absent row uses the defaults. DM004 uses (plan_ref, account_key) as its key. DP08 partner data is owned by S9 rwb-partner; P1 keeps only its reconciliation and catalog responsibilities.
- AceIngestCheck is started by the readiness handler, the 05:30 late-check Schedule and the fallback poll. After the ALS stamp it starts ReconciliationWorkflow and Stage2ProductWorkflow as child workflows. No P1 workflow consumes its own AceDataReady topic. With Section B flag off, the run writes no stamp, publishes nothing, starts no child workflow, reports LATE and freshness STALE with a null date.
- P4 rwb-access owns authorization and masking policy. The owning service enforces the permission and field mask on its API response. Every personal-field read uses the ACE Common PII audit path; personal values do not enter business events, workflow inputs, logs, traces or metrics. ACE view-masked values are never unmasked. Product/source seed codes remain provisional pending ACE confirmation (NEW-ASM-B3).
- P1 retention periods remain Pending, owner Compliance, tracked as GAP-1029. P1 retention scope is interaction (ARCHIVE) and party_ext, account_ext, contact_point_ext, valuation_ext, dp_treatment and dp_guarantee_claim (REVIEW); case_list_row is excluded. contact_point_ext and valuation_ext stay REVIEW only while the hold join key is Pending, owner Data architect, tracked as NEW-GAP-C3. No P1 destruction is authorised.
- Migration uses the Source to Target Mapping v7 Migration packages sheet as the normative allow-list. Carry only Workbench system-of-record fields and linking ACE keys; ACE fields are ACE_READ and never carried. Every migrated table has migration_source varchar(20) and migrated_at timestamptz (UTC). LOV-MIGRATION-SOURCE values remain Pending, owner Data owner, tracked as NEW-GAP-B4.

- Data-product stamping: write one `data_product_load` row per `(product_code, business_date)` only after every mapped `data_product_source` is COMPLETED. `source_system` is the completing source, `source_extracted_at` is the latest source `completed_at`, and `loaded_at` is the write instant. The greatest business date is in use; out-of-order dates remain history; restatements increment `duplicate_count` without a new event. RWB-P1-E1015-APP is the sole writer.
- EV-26 is one event per source system/business date with status COMPLETED; downstream daily work starts only on ALS/COMPLETED. With the Section B flag off, no stamp, event or child is written; status is LATE and freshness STALE with null date. P1 has no consumer group on its own `rwb.source-data.events.v1` topic.
- Pending ACE behavior: current account date matching and null/mismatch/past/future handling (owner Data architect, NEW-GAP-W8-004); `v_ace_ca_relation` orphan-detection set/query (owner Data architect, NEW-GAP-W8-003); TDR and settlement null handling (owner Data architect, NEW-GAP-W8-005).

Further rulings that bind this module:

- Every POST requires an Idempotency-Key (UUID); PUT and PATCH require If-Match (RD-P1-001, RD-P1-006).
- Only rwb-source-data writes the interaction ledger; other services append over REST and rwb-comms is the one caller for delivery entries (RD-P1-007, RD-P1-009).
- rwb-case reads entry candidates through the activity listEligibleAccounts; caseId is the case uuid and P1 offers no case-number lookup (RD-P1-010, RD-P1-023).
- The P1 job monitor lists and reruns P1 runs only; only a FAILED run can be rerun (RD-P1-012, RD-P1-024). Other services' job reads are Pending, owner Solution architect (NEW-GAP-A1).
- Reconciliation tolerance recon.tolerance.pct version 1 is 0.00 (RD-P1-042).
