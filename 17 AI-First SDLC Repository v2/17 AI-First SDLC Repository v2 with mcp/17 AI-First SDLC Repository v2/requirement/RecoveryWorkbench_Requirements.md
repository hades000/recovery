# Recovery Workbench — canonical requirements

**Document ID:** `REQ-RWB-002`
**Version:** 2.0, 16 November 2026
**Supersedes:** `REQ-RWB-001` (v1, 4 November 2026)
**Sources:** Business Requirements Program v4, Business Requirements Epic 1 v4, Business Requirements
Epic 2 v4, Lean BRD Epic 1 v3, FSD v6, NFR v3, Business Rules v4, Case and Workflow Model v5,
Physical Schema v6, API Specification v4.
**Status:** Baseline for Epic 1 specification and planning. The 10 removed/retired stories are not in
scope.

## 0. Trace metadata

| Field | Value |
|---|---|
| BRD | `requirement/BRD_RecoveryWorkbench.md` |
| Context | `.github/contexts/project-context.md` |
| Story index | `docs/increments/INDEX.md` |
| Traceability | `requirement/Traceability_Matrix.md` |
| Source ID crosswalk | `BR-RWB-*` → `REQ-*` in §12 |

## 1. Project overview

The Workbench is the recovery module of ACE. It gives recovery staff one case from 90 DPD to close:
case list, case record, documents, decisions, treatments, legal and partner work, reporting and
measured AI assistance. Source data is owned by ACE and read through SELECT-only views. Rules are
versioned data, evaluated by embedded Drools. From Epic 3 the case lifecycle runs on Temporal.

## 2. Actors and personas

| Actor | Goal | Main stories |
|---|---|---|
| Recovery officer | Work assigned cases, attach documents, issue notices | E1-002/023/026/052 |
| Recovery team lead | Allocate, transfer, approve within limit | E1-020/021/031/038 |
| Recovery manager | Approve deviations and high-value treatments | E2-013/014 |
| Risk | Approve rule packages and high-risk treatments | E1-073, E2-041 |
| Compliance / audit | Read decisions and access evidence | E1-039, TE-008, E2-005 |
| Central operations | Maintain rules, reference data and parameters | E1-042/043/073 |
| Platform / security admin | Operate Temporal, flags and break-glass | E1-070/071, E2-037/038 |
| Partner | Act on instructed cases | E2-019 |
| Agent runtime | Recommend intake, extraction and deviation | E1-058/059/062 |
| ACE team | Own source tables and views | E1-069, RWB-ACE-001 |

## 3. Story groups and scope

| Group | Active stories | Outcome |
|---|---|---|
| Data and views | E1-001, E1-069, E1-064, E1-065, TE-004 | Recovery tables, 30 views, dictionary, sandbox |
| Configuration | E1-042, E1-043, E1-045, E1-047 | Parameter catalog, reference data, flags |
| Case core | E1-018, E1-020, E1-021, E1-028, E1-030, E1-031, E1-023, E1-035 | Case ID, allocation, transfer, SLA, rebalancing, list, record |
| Access | E1-019, E1-022, E1-037, E1-038, E1-039 | Roles, SSO, matrix, DoA, access log |
| Documents | E1-024, E1-025, E1-026, E1-032, E1-033, E1-040, E1-041, E1-049, E1-050, E1-053, E1-054, E1-057, TE-012 | Store, index, OCR, classify, extract, review, retention, intake |
| Communications | E1-034, E1-046, E1-052, E1-055 | Templates, notices, proof of delivery |
| Decision log | E1-008, E1-027, TE-008 | Append-only store, writer, hash check |
| Integration | E1-007, TE-006, E1-056 | Outbound adapters, outbox, run books |
| Interaction ledger | E1-066, E1-067, E1-068 | Store, write every action, read interface |
| Reporting | E1-013 | Baseline measures |
| AI | E1-058, E1-059, E1-060, E1-061, E1-062, E1-063, TE-013 | Platform, shadow agents, evaluation, dashboard |
| Temporal | E1-070, E1-071 | Platform and worker |
| Drools | E1-072, E1-073 | Runtime, package store, authoring/validation/rollback |
| Data quality | E1-011, E1-015, E1-016, E1-017 | Reconciliation, freshness, access, retention |

## 4. Functional requirements

### FR-RWB-001 Case list and queue

The user sees one row per case with case ID, customer (masked by role), product, stage, queue, owner,
DPD, ageing and next action. Filters: queue, owner, stage, product, ageing bucket. Sort: ageing, DPD,
case ID. Pagination: server-side. Bulk transfer/reassignment with a reason.

**Stories:** E1-002, E1-031. **Source:** `REQ-CAS-001..012`.

### FR-RWB-002 Case record

The user sees a read-only record with header, accounts, parties, documents, history, decisions,
treatments, legal and notes. The history is an append-only timeline with actor, time, action and
decision-log reference. Documents open in the document viewer. Personal data is masked by role.

**Stories:** E1-023, E1-035. **Source:** `REQ-CAS-013..026`.

### FR-RWB-003 Case creation

A case is created at 90 DPD or by an authorised manual action. It carries a case number, product group,
primary account, entry date, DPD at entry, stage `NEW` and a queue. The primary account rule is
`case_account.is_primary` (D-RCV-30). Duplicate account + product + open case is refused.

**Stories:** E1-018. **Source:** `REQ-CAS-027..039`.

### FR-RWB-004 Allocation and assignment

Allocation selects a queue; assignment selects an owner. Rules consider product, segment, queue
capacity, officer skill, leave and priority. A manual override needs a reason. The decision log records
the rule ID and version.

**Stories:** E1-020. **Source:** `REQ-CAS-040..052`.

### FR-RWB-005 Transfer and reassignment

A lead moves a case between queues or owners. The reason is mandatory. The previous owner, new owner,
time and reason are in the history and the decision log. A transfer does not reset the stage clock.

**Stories:** E1-021. **Source:** `REQ-CAS-053..060`.

### FR-RWB-006 Service levels, timers and prescription

Each stage has a clock. Timers raise an alert and then escalate. The prescription date is calculated
from the legal route and is visible on the case. Timers are Quartz jobs in Epic 1–2, behind
`TimerScheduler`.

**Stories:** E1-028, E1-030. **Source:** `REQ-CAS-061..075`.

### FR-RWB-007 Documents

A document is stored in Blob, indexed by case, type, date and extracted fields, virus-scanned, assigned
a retention class and, for legal types, stored write-once. OCR produces text; classification assigns a
type; extraction fills fields with confidence; low confidence goes to the review queue. The user can
search by case, type, date and extracted field.

**Stories:** E1-024, E1-025, E1-026, E1-032, E1-033, E1-040, E1-041, E1-049, E1-050, E1-053, E1-054,
E1-057, TE-012. **Source:** `REQ-DOC-001..040`.

### FR-RWB-008 Notices and templates

A notice is generated from a template and merge fields, previewed, approved where required, dispatched
and recorded with a proof-of-delivery reference. The template catalog is reference data.

**Stories:** E1-034, E1-046, E1-052, E1-055. **Source:** `REQ-COM-001..018`.

### FR-RWB-009 Decision log

Every decision writes an append-only entry before the action: case ID, actor, action, inputs, rule ID,
rule version, approver, outcome and the hash of the previous entry. A failed write blocks the action.
A correction is a new entry naming the original. The hash chain is checked daily.

**Stories:** E1-008, E1-027, TE-008. **Source:** `REQ-DEC-001..015`.

### FR-RWB-010 Configuration service and parameter catalog

Every environment setting and business parameter has a name, type, default, owner, environment, range,
where used and approval state. Code reads by key; a literal business value fails the build. Values are
versioned per environment and effective from a valid-from date; rollback is one call. Secrets are listed
but never served.

**Stories:** E1-042. **Source:** `REQ-DRI-010`.

### FR-RWB-011 Reference data service

Lists of values (roles, queues, document types, checklists, DoA, product parameters) are versioned
tables with valid-from/valid-to, maker-checker and a load/rollback path. A new list is data, not a
release.

**Stories:** E1-043, E1-045. **Source:** `REQ-DRI-011`.

### FR-RWB-012 Access control and masking

Sign-in is Entra ID SSO with MFA. Roles map to permissions as data. Personal data is masked by role at
the API. Every personal-data read and every admin action writes an access-log entry. Break-glass is
time-boxed and logged.

**Stories:** E1-019, E1-022, E1-037, E1-038, E1-039. **Source:** `REQ-ACC-001..025`.

### FR-RWB-013 ACE source views

The recovery module reads ACE source data only through 30 SELECT-only `recovery.v_ace_*` views. The
view owner holds SELECT on the ACE tables; the recovery service role holds SELECT on the views and no
privilege in `public`. No FK into `public`. A direct `public` read fails in the catalog and in BND-6.

**Stories:** E1-069, RWB-ACE-001. **Source:** `REQ-RDF-002`, `REQ-DRI-006`.

### FR-RWB-014 Temporal platform and worker

A self-hosted Temporal cluster per environment in the ACE namespace, namespace `rwb-recovery`, task
queues `rwb-case`, `rwb-integration`, `rwb-platform`, workflow ID `case-{caseId}`. The worker runs under
`SY-CASEWF`; the feature flag `rwb.p3.temporal` starts or stops it. Case data stays in the recovery
schema. Epic 1–2 jobs stay Quartz/Spring Batch.

**Stories:** E1-070, E1-071. **Source:** `D-RCV-36 T1/T2`, `REQ-WF-001..015`.

### FR-RWB-015 Drools rule packages

RW-COE uploads an XLS decision-table workbook. The service compiles it to a KieBase, runs checks, runs
the scenarios and a dry run, stores `rule_package_version` with workbook, DRL and checksum. RW-RISK
approves; the author cannot approve. The package is in force from its valid-from date; rollback is one
call. `rule_row` stays the queryable catalog. `payment_match_rule` is not created.

**Stories:** E1-072, E1-073, E2-041, E2-042. **Source:** `D-RCV-36 T3–T7, T10`.

### FR-RWB-016 Interaction ledger

Every Workbench action writes an interaction record: case, actor, channel, action, time, outcome and
reference. The read interface supports audit and reporting. The ledger is append-only.

**Stories:** E1-066, E1-067, E1-068. **Source:** `REQ-AUD-001..010`.

### FR-RWB-017 Reporting

Baseline measures (time in stage, TAT by route, recovery rate, queue ageing, case count) and a steering
dashboard. Definitions are versioned; the data is read from the case and decision stores, not a copy.

**Stories:** E1-013, E2-009. **Source:** `REQ-RPT-001..012`, D-RCV-32.

### FR-RWB-018 AI agents

The agent platform, an intake agent in shadow, extraction evaluation, a deviation screening agent in
shadow and a monitoring dashboard. Agents write recommendations, not decisions. The promotion gate uses
the D-RCV-33 grammar. The runtime client falls back to the manual path.

**Stories:** E1-058, E1-059, E1-060, E1-061, E1-062, E1-063, TE-013. **Source:** `REQ-AI-001..020`.

### FR-RWB-019 Treatment and plan

A treatment is a restructure, settlement, legal, asset sale, debt sale or write-off. It has a plan, a
timeline, approvals by DoA, and outcome. Plan timers are visible on the case.

**Stories:** E2-002, E2-004, E2-013, E2-014. **Source:** `REQ-TRT-001..020`.

### FR-RWB-020 Payments and booking

Payment matching is Drools package `PAYMENT_MATCH` (EXACT, PARTIAL, WINDOW) with tolerance, window,
grace and partial floor as columns. Booking match is package `BOOKING_MATCH`. A matched payment updates
the case and the ledger; an unmatched payment goes to the exception queue.

**Stories:** E2-007, E2-008, E2-027. **Source:** `REQ-PAY-001..015`.

## 5. Non-functional requirements

| ID | Area | Requirement |
|---|---|---|
| `NFR-RWB-001` | Availability | 99.5% service hours; 99.9% decision log write |
| `NFR-RWB-002` | Performance | Case list p95 ≤ 2 s, case record ≤ 3 s, document search ≤ 2 s |
| `NFR-RWB-003` | Throughput | 45,000 cases/year; 180 concurrent users; 1,500 documents/day peak |
| `NFR-RWB-004` | Recovery | RPO 15 min, RTO 4 h (design baseline) |
| `NFR-RWB-005` | Security | Entra ID, MFA, RBAC, method security, audit |
| `NFR-RWB-006` | Privacy | PDPA classification, masking, retention, no personal data in Temporal history |
| `NFR-RWB-007` | Accessibility | WCAG 2.2 AA |
| `NFR-RWB-008` | Observability | Logs, metrics, traces, health, run book per job |
| `NFR-RWB-009` | Operability | Rolling deploy, flag-off path, rollback by tag |
| `NFR-RWB-010` | Retention | 10 years case/decision; legal hold; e-discovery |

Full NFRs: Non-Functional Specification v3.

## 6. Data requirements

- Schema `recovery`, `${recoverySchema}`, 93 tables, 30 views, 122 objects, 1,366 fields.
- Four extension tables keyed by ACE business key; no FK into `public`.
- 20 removed copy/load tables and 243 fields; no inbound load.
- Flyway: V0001 tables/dictionary, V0002 Tier 1 views, V0003 Tier 2 views.
- Migration naming D-RCV-28; one file per story; forward-only.

Full model: Logical Data Model and Data Dictionary v8; Physical Schema v6.

## 7. Integration points

| Integration | Direction | Contract |
|---|---|---|
| ACE source tables | Read | `recovery.v_ace_*` views |
| COLLINS / outbound files | Outbound | SFTP/file adapter + outbox |
| Blob storage | Both | Azure Blob SDK |
| Entra ID | Inbound | OIDC |
| Temporal | Runtime | gRPC |
| WIN/NSS/LINE/e-sign | Outbound | Adapters (Epic 2) |

Full contracts: Interface Specifications v3; API Specification v4; Event and Messaging Design v4.

## 8. Business rules

| Family | IDs | Owner |
|---|---|---|
| Entry / exclusion | ENTRY-*, EXCL-* | RW-COE |
| Allocation / assignment | ALLOC-*, ASSIGN-* | RW-COE |
| Transfer | TRANSFER-* | RW-COE |
| Service level / timers | SLA-*, TIMER-* | RW-COE |
| Documents | DOC-* | RW-COE |
| Decision log | DL-* | Compliance |
| Payments | PAYMENT_MATCH-* | RW-COE / data team |
| Restructure | R-RES-* | RW-COE |
| Booking | BOOKING_MATCH-* | RW-COE |

The 448 rules are in the Business Rules and Routing Logic v4. Rule IDs and package versions are the
audit key. A rule change does not need a release (D-RCV-36).

## 9. Acceptance criteria

- Every story uses Given/When/Then with an AC ID.
- A story with no business AC (engineering enabler) is accepted on its business rules and test cases
  (D-RCV-16).
- Each AC has at least one test case; each test case names the AC, the data and the expected result.
- A rule, field or message ID in a story must exist in its source document.
- UI stories include the screen states: default, loading, empty, error, forbidden.
- Migration stories include apply, re-run, negative and lint tests.
- Temporal/Drools stories include the flag-off path and the rollback path.

## 10. Error handling

- Every error returns a message ID from the Error and Message Standard v4.
- 400 validation, 401 unauthenticated, 403 forbidden, 404 not found, 409 conflict, 422 business rule,
  500 unexpected with a trace ID.
- The message is exact; the UI displays the message ID and the text.
- A failed decision-log write returns 503 and the action is not performed.
- A failed outbound call retries through the outbox; a permanent failure goes to the dead-letter queue.

## 11. Out of scope

- Inbound source loads, source copies, tracker inventory, ADF/Control-M feed jobs.
- `RWB-E1-036`, `RWB-E1-029`, `RWB-TE-005`, `RWB-E1-048`, `RWB-E1-051` and the seven data-load/tracker
  stories.
- Epic 3–8 journeys and route screens.
- A commercial workflow engine other than Temporal; a KIE Server or Business Central.
- A second copy of source data or a direct ACE `public` table read.

## 12. Source ID crosswalk

| Canonical | Source | Note |
|---|---|---|
| `BR-RWB-001..020` | Lean BRD v3; Business Requirements v4 | 20 business requirements |
| `FR-RWB-001..020` | FSD v6, Business Requirements v4 | Functional groups |
| `NFR-RWB-001..010` | NFR v3 | Non-functional |
| `REQ-*` | Business Requirements Program/Epic 1/Epic 2 v4 | Original IDs preserved in the corpus |
| `CTX-FEAT-*` | Context feature catalogue | 20 capabilities |
| `SPEC-RWB-<story>-*` | Per-story specification | New v2 specs for E1-042/TE-001; old specs archived |
| `TASK-*` | Per-story plan | Plan files |

## 13. Open questions

| ID | Question | Default | Owner |
|---|---|---|---|
| `OPEN-005` | Thai wording | English canonical, Thai draft | BA / DL10 |
| `OPEN-010` | Availability, RPO/RTO, retention | NFR design baseline | Product Owner |
| `OPEN-016` | Per-story approver names | Source-set approval + plan gate | Product Owner |
| `OPEN-020` | Temporal version and retention | Pin at build; 30 days | SCB IT |
| `OPEN-021` | ACE Tier 2 ingestion assumption | Assume yes | ACE team lead |

## 14. Traceability summary

| Layer | Count | Document |
|---|---:|---|
| Business requirements | 20 | `BRD_RecoveryWorkbench.md` |
| Functional groups | 20 | this document |
| Non-functional | 10 | this document |
| Active Epic 1 stories | 72 | `docs/increments/INDEX.md` |
| Epic 2 stories | 43 | `docs/increments/epic-2-stories.md` |
| Retired / removed | 10 | `docs/retirements/story-retirement-register.md` |
| Full matrix | — | `requirement/Traceability_Matrix.md` |
