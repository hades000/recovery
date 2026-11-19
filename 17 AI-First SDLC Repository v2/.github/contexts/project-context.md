# Recovery Workbench — project context

**Context ID:** `CTX-PROJECT-RWB-V2`
**Version:** 2.0, 16 November 2026 (document set v14)
**Owner:** Recovery tech lead (Jesniphat Pukkham) with the solution architect
**Source of truth:** `requirement/legacy/` (converted 16 November 2026). This file is the business
truth; technical realisation is in `backend-context.md`, `frontend-context.md` and `testing-standards.md`.
**Status:** `IMPLEMENTED`, `DOCUMENTED/REQUIRED`, `USER-PROVIDED`, `RECOMMENDED` and `N/A` are used as
evidence labels. The Workbench code is in the ACE monorepo, a separate repository.

## 1. Business overview

The Recovery Workbench is the recovery module of SCB's ACE collections service. It gives recovery
staff one case from 90 days past due to close: a case list, a case record, documents, decisions,
treatment plans, legal and partner work, reporting and AI assistance. It is not a standalone product;
it reuses ACE sign-in, IAM, access control, audit, PII and SOC logging, the database and the front end.

| Item | Value | Evidence |
|---|---|---|
| Product | Recovery Workbench, module `recovery` of ACE | `CTX-BUSINESS-001`, ADR-001 |
| Business owner | SCB Collections and Recovery | Project Overview v4 |
| Delivery partner | Henka Group with TechX squads | Ways of Working v3 |
| Release 1 | Epic 1 Foundation 1, 30 November 2026 | Build Sequence v6 |
| Release 2 | Epic 2 Foundation 2, 31 December 2026 | Build Sequence v6 |
| Programme | Epic 3–8 monthly releases to June 2027 | Release Plan v4 |
| Case volume | ~45,000 recovery cases a year at steady state | Volume and Scale Forecast v3 |
| Staff | ~180 recovery users across 12 roles | Users, Roles and Permissions v4 |
| Build scope | 115 items: 72 in Epic 1 and 43 in Epic 2 | Build Sequence v6 |

**Business outcome.** One case view across collection and recovery; one copy of source data; no
hand-built load estate; a rule change without a release; a decision record for every action; recovery
documents in one system of record; and AI assistance that stays in shadow until its measured quality
clears the promotion gate.

## 2. Actors, roles and stakeholders

| Actor / role | Purpose | Authority | Evidence |
|---|---|---|---|
| Recovery officer (RW-OFFICER) | Work cases in a queue | Read/write own cases; no approval | Users, Roles and Permissions v4 |
| Recovery team lead (RW-LEAD) | Allocate, reassign, approve within limit | Case and queue administration | Delegation of Authority Matrix v2 |
| Recovery manager (RW-MGR) | Approve deviations and high-value treatments | DoA level 2 | Delegation of Authority Matrix v2 |
| Risk (RW-RISK) | Approve rule packages, TDR and write-off exceptions | Rule package approval; cannot author | D-RCV-36 T4 |
| Compliance / audit (RW-AUDIT) | Read the decision log and access log | Read-only; no case edit | Admin and Access Model v5 |
| Central operations (RW-COE) | Author rules and reference data | Author, not approve | D-RCV-36 T4 |
| Platform administrator (RW-PLATADM) | Operate Temporal, flags, jobs | Platform admin, break-glass logged | ADR-011 |
| Security administrator (RW-SECADM) | Decode Temporal payloads on break-glass | Logged, time-boxed | ADR-011 |
| Partner user (RW-PARTNER) | Act on instructed cases | Scoped to partner cases | Partner Operating Model v2 |
| Customer | Receives notices, pays, agrees a treatment | No Workbench login | Case Journeys v3 |
| Agent runtime (SY-AGENT) | Intake, extraction, deviation review | Shadow only in Epic 1 | Agent Catalog v2 |
| Case workflow worker (SY-CASEWF) | Runs Temporal workflows | From Epic 3 | ADR-011 |
| Rules worker (SY-RULES) | Evaluates Drools packages | Evaluates, does not approve | D-RCV-36 T3 |
| Product Owner | Chitchaya Muanchonchana | Intake, requirements, backlog, deployment gates | D-RCV-46 |
| Recovery tech lead / FDA | Jesniphat Pukkham | Context, design, plan, PR, release gates | D-RCV-15 |
| ACE tech lead | Pipat Saengow | ACE schema, MR review, shared files | OPEN-028 |
| ACE and Recovery lead | Pongchai Charoenrungrodkun (K. Tee) | Jenkins, environment, dependency approval | D-RCV-14, OPEN-019 |

## 3. Process, case and rules model

- **Case vocabulary:** CMMN 1.1 — case, stage, milestone, task, sentry, event listener, case file item.
  The collection module uses the same terms (DT10).
- **Case model:** 10 stages, 30 milestones, 150 tasks, 53 event listeners and 448 sentries.
- **Rules:** 448 routing rules. In Epic 1 and Epic 2, rules are versioned data evaluated by embedded
  Drools from XLS decision-table packages (D-RCV-36, ADR-012). The rule catalog `rule_row` remains
  queryable; the package version is the version of record.
- **Workflow:** from Epic 3, one Temporal workflow per case, workflow ID `case-{caseId}`. Case data
  stays in the ACE database recovery schema; Temporal holds no case of record (D-RCV-36 T1, ADR-011).
  Epic 1 and Epic 2 scheduled jobs stay on Quartz and Spring Batch; JOB-05 runs behind the
  `TimerScheduler` port (T2).
- **Determinism:** a Temporal workflow calls Drools only inside an activity. The package version is
  chosen at evaluation time, returned in the rule result and written to the decision log (T7).
- **First match:** each decision table has RuleSet = package code, one row per rule, one
  activation-group, salience derived from row order, default row last (T5).
- **Decision log:** append-only, hash-chained, written before the action; a failed write blocks the
  action (ADR-009). `rule_id` and `rule_version` carry the Drools rule name and package version label.

## 4. Functional scope by module

### P1 Recovery data engine

Recovery tables, read-only ACE source views, data dictionary, synthetic sandbox, access control per
data product, freshness, reconciliation, interaction ledger and the data-quality gate.

- **D-RCV-35 U1:** the Workbench loads no source data. ACE ingests ALS, EFS, CCMS, SVAF, COLLINS,
  NLEADS, EasyApp and Entra ID data. The Workbench reads it through 30 SELECT-only
  `recovery.v_ace_*` views (16 Tier 1 over ACE tables that exist today, 14 Tier 2 over RWB-ACE-001).
- **D-RCV-35 U3:** Workbench-only fields live in four 1:1 extension tables keyed by ACE business keys.
  Existing ACE tables are never altered by the Workbench.
- **D-RCV-35 U5:** Excel and SharePoint trackers leave system scope; their retirement is in the
  Cutover Plan v3 section 8.
- **RWB-E1-069** builds the 16 Section A views and the boundary rule BND-6. **RWB-ACE-001** is the ACE
  team's delivery of 14 Tier 2 tables, 12 columns and 14 views.

### P2 Integration

Outbound-only integration adapters, outbox and retry, run books and monitoring. The inbound half of
RWB-E1-007 is removed; the story survives as outbound adapters. ADF and Control-M jobs are removed
(RWB-E1-051), because ACE ingestion replaces them.

### P3 Case and workflow

Configuration service and parameter catalog, reference data service, case ID and case record,
allocation and assignment, transfer, service levels and timers, rebalancing, case list and read-only
case record, Temporal platform and worker, Drools runtime and package store, rule authoring and
rollback. From Epic 3 the case lifecycle runs on Temporal.

### P4 Access and administration

Entra ID SSO/MFA, roles, role-to-permission matrix, PDPA field masking, delegation of authority,
access log into the decision log, break-glass admin.

### P5 Document hub

Document store and index, six document types, OCR, classification, field extraction, review queue,
retention classes and virus scan, intake from branches, mailroom, partner SFTP and email. The document
hub is the system of record for recovery documents (ADR-007).

### P6 Communications

Notice generation v1, template and merge-field catalog, proof-of-delivery capture design with WIN,
letter dispatch, SMS and LINE dispatch (Epic 2).

### P7 Decision centre and log

Append-only hash-chained decision log store and writer, query API for audit (Epic 2), hash-chain check.

### P8 Payments and posting

Payment matching in Drools package `PAYMENT_MATCH`, booking match in `BOOKING_MATCH`; no
`payment_match_rule` table (D-RCV-36 T10).

### P9 Reporting

Baseline measures, steering dashboard, queue and ageing views, reporting data model.

### P10 Agent runtime

Agent platform set-up, case intake agent in shadow, extraction evaluation, deviation screening in
shadow, monitoring dashboard; live agents from Epic 2 after the promotion gate.

## 5. Data requirements

| Item | Value | Evidence |
|---|---|---|
| Database | PostgreSQL, schema `recovery` in the ACE database | Physical Schema v6; D-RCV-28 |
| Schema reference | `${recoverySchema}` in every migration; value `recovery` in every environment | D-RCV-28, RWB-E1-044 §13 |
| Tables | 93 tables in schema `recovery` | Physical Schema v6 |
| Views | 30 `recovery.v_ace_*` SELECT-only views | ADR-010; RWB-E1-069 |
| Extension tables | 4, 1:1 by ACE business key | D-RCV-35 U3 |
| Removed tables | 20 source-copy and load tables, 243 fields | D-RCV-35 U1 |
| Dictionary | 122 `sys_objects` and 1,366 `sys_fields` in V0001 | D-RCV-29 |
| Flyway split | V0001 tables and dictionary; V0002 Tier 1 views; V0003 Tier 2 views | Physical Schema v6 |
| Migration naming | `V<seq>__<story>_<name>.sql`, 4-digit contiguous sequence, line 1 `-- Story: <key>` | D-RCV-28 |
| Personal data | Classified in the Personal Data Inventory v4; masked at API by role | CTX-COMPLIANCE-004 |

**Data ownership.** ACE team: Tier 1 and Tier 2 source tables and columns, plus the 30 views' base
tables. Workbench: case, workflow, treatment, legal, partner, debt sale, documents, decision log,
reference data, outbox, flags, agents, and the four extension tables. One copy of source data.

## 6. Integration points

| Integration | Direction | Mechanism | Owner |
|---|---|---|---|
| ACE DB (account, payment, customer, collateral, asset, collections, product, branch, scores) | Inbound, read-only | `recovery.v_ace_*` views | ACE team |
| ALS, EFS, CCMS, SVAF, COLLINS, NLEADS, EasyApp, Entra ID | Inbound to ACE | ACE ingestion | ACE team |
| COLLINS / outbound files | Outbound | Integration adapter and outbox | Recovery squad |
| Blob storage | Both | Document storage containers | Recovery squad |
| Entra ID | Inbound | OIDC / SSO / MFA | ACE identity |
| Jira, Confluence, GitLab | Delivery | MCP servers | Delivery |
| Temporal | Runtime | gRPC, namespace `rwb-recovery` | SCB IT / ACE platform |
| WIN, NSS, LINE OA, e-signature | Outbound | Adapters | Recovery squad |

No component calls a system of record directly. A direct read of an ACE `public` table fails in the
catalog and in boundary rule BND-6.

## 7. Non-functional requirements

| Area | Target | Source |
|---|---|---|
| Availability | 99.5% in service hours; 99.9% for the decision log write | NFR v3 |
| Performance | Case list p95 ≤ 2 s; case record p95 ≤ 3 s; document search p95 ≤ 2 s | NFR v3 |
| Throughput | 45,000 cases a year; 180 concurrent users; 1,500 documents/day peak | Volume and Scale Forecast v3 |
| RPO / RTO | RPO 15 min, RTO 4 h (assumed; DL11/DL26 open) | NFR v3 |
| Retention | 10 years for case and decision records; legal documents per retention class | Controls Catalog v3 |
| Security | Entra ID, MFA, RBAC, method security on every endpoint, audit of every access | Security and Access Design v4 |
| Privacy | PDPA classification, masking by role, no personal data in Temporal history | D-RCV-36; PDPA design |
| Accessibility | WCAG 2.2 AA for the recovery screens | NFR v3; RWB-TE-010 |
| Observability | Structured logs, metrics, traces, health; run book per job | Observability and Monitoring Design v3 |

## 8. Compliance, controls and policy

| Obligation | Control | Evidence |
|---|---|---|
| PDPA | Classification, masking, retention, consent where required | Personal Data Inventory v4; Controls Catalog v3 |
| Audit | Append-only decision log; access log; hash-chain check | ADR-009; RWB-TE-008 |
| Model risk | Rule package approval by RW-RISK; author cannot approve | D-RCV-36 T4 |
| AI governance | Shadow mode, measured promotion grammar, no personal data in prompts | D-RCV-33; AI Assisted Development Approach v1 |
| Change control | PR review, named reviewer, story → plan → code trace | AGENTS.md |
| Records retention | 10 years; legal hold; e-discovery | Controls Catalog v3 |

## 9. Delivery model

- Delivery runs as Kanban (DT04). The two-week point is a sponsor review, not a sprint boundary.
- 115 items: 72 Epic 1, 43 Epic 2. Pull the next item whose dependencies are done.
- Epic 1 window 1 (2–13 Nov 2026): 15 items. Window 2 (16–27 Nov 2026): 57 items.
- Story keys: `RWB-E1-001..073` (not all numbers exist), `RWB-TE-001..013`, `RWB-E2-001..043`,
  `RWB-ACE-001`. `RWB-E1-036` has no story file.
- 10 stories are removed or retired; see `docs/retirements/story-retirement-register.md`.
- Two repositories, one story: recovery module code and migrations go to the ACE monorepo; AISDLC
  artefacts stay in this repository. Branches: `feature/<JIRA-KEY>-<slug>` from `develop-recovery`,
  MR into `develop-recovery`, batch MR into `develop` (D-RCV-50).

## 10. AI and agents

- AI is used for intake classification, field extraction, deviation screening and decision support.
- Epic 1: all agents in shadow. Epic 2: case intake agent live at L1 on one segment after the
  promotion gate (D-RCV-33).
- The agent runtime is behind `rwb.p10.agents`; a failure falls back to the manual path.
- No personal data, production data or credentials in prompts. Only synthetic or masked data.
- The repository holds prompts, subagents and standards; they are reviewed like code.
- Claude Code subagents are in `.claude/agents/` and are generated from `.github/agents/`.

## 11. Constraints

1. One service, one repository, one front end (ADR-001, ADR-002).
2. Recovery code only in `th.co.scb.ace.demo.recovery` and `frontend/src/modules/recovery/`.
3. No inbound source load (D-RCV-35 U1); no direct ACE table read (ADR-010, BND-6).
4. Schema `recovery`, `${recoverySchema}`, no schema literal, no `SET search_path` (D-RCV-28).
5. One migration file per story; forward-only; corrective file with `-- Fix:` (D-RCV-28).
6. Temporal only from Epic 3; Quartz/Spring Batch for Epic 1–2 jobs (D-RCV-36 T1/T2).
7. Embedded Drools only; no KIE Server, Business Central or KJAR (D-RCV-36 T3).
8. No new dependency without plan approval (D-RCV-49 precedent).
9. No personal data in code, tests, logs or prompts.
10. Feature flags for unfinished or cross-squad work (ADR-008).

## 12. Assumptions and open decisions

| ID | Assumption / open item | Default used here | Owner |
|---|---|---|---|
| A1 | AMIS, RPS, LIT, WIN, GL and COLLINS scores follow the same ACE ingestion route as SVAF/CCMS | Treated as ACE-ingested; if not, the source reopens U1 for that source | ACE team lead |
| A2 | Temporal server and Java SDK versions are pinned at build | Recorded in Environment and Deployment Design v4 | SCB IT |
| A3 | Temporal closed-workflow retention is 30 days | Assumed; DL26 confirms | Compliance |
| A4 | Availability, RPO/RTO and retention are not signed | NFR targets above are the design baseline | Product Owner |
| A5 | Thai labels and messages are proposed, pending DL10 | English canonical, Thai draft | BA |
| A6 | Jira keys are not assigned to every Epic 1 story | Local keys are authoritative; Jira import later | Product Owner |
| A7 | `RWB-E1-036` has no story file | Not created; not in the build sequence | BA |
| A8 | The 21 Tier 1 ACE tables are at the baseline head in DEV/SIT | `RWB-E1-069` checks before views compile | ACE team |
| A9 | Named approvers are recorded for the source set; per-story Jira approval comments are not | Per-story gates use the source set approval and are re-confirmed at plan | Product Owner |

## 13. Feature catalogue

| Feature / CTX ID | Actor and purpose | Entry or trigger | Business behaviour and outcome | Evidence |
|---|---|---|---|---|
| `CTX-FEAT-001` Case list | Officer finds and works cases | Queue, owner, filters | One row per case with case ID, owner, queue, stage, ageing | RWB-E1-002, E1-031 |
| `CTX-FEAT-002` Case record | Officer sees the whole case | Case ID | Read-only header, accounts, parties, documents, history | RWB-E1-023, E1-035 |
| `CTX-FEAT-003` Case creation | System/officer opens a case | 90 DPD or manual | Case ID, primary account, stage, queue | RWB-E1-018 |
| `CTX-FEAT-004` Allocation and assignment | System assigns work | Job or event | Rule-driven owner and queue | RWB-E1-020 |
| `CTX-FEAT-005` Transfer | Lead moves a case | Manual or rule | Reason recorded; queue and owner change | RWB-E1-021 |
| `CTX-FEAT-006` Service levels and timers | System/lead tracks time | SLA clock | Timer, escalation, prescription date | RWB-E1-028 |
| `CTX-FEAT-007` Rebalancing | System balances queues | Daily job | Queue measures and reallocation | RWB-E1-030 |
| `CTX-FEAT-008` Documents | Officer stores and finds documents | Upload, intake, OCR | Store, index, classify, extract, review | RWB-E1-024/026/049/050/053/054 |
| `CTX-FEAT-009` Notices | Officer issues a notice | Template + merge fields | Generated notice and dispatch record | RWB-E1-052, E1-046 |
| `CTX-FEAT-010` Decision log | Officer/system records a decision | Any case action | Append-only entry with rule and approver | RWB-E1-008/027 |
| `CTX-FEAT-011` Configuration | Squad/COE changes a value | Parameter catalog | Versioned value per environment; no release | RWB-E1-042 |
| `CTX-FEAT-012` Reference data | COE maintains lists | Admin screen/load | Versioned table; effective dates | RWB-E1-043 |
| `CTX-FEAT-013` Access control | Security administers roles | Entra ID | SSO/MFA, role and permission matrix, masking | RWB-E1-022/037/039 |
| `CTX-FEAT-014` ACE source views | Developer reads source data | SQL view | One copy of source data, SELECT only | RWB-E1-069 |
| `CTX-FEAT-015` Temporal platform | Platform admin runs workflows | Worker start | Durable timers and retries from Epic 3 | RWB-E1-070/071 |
| `CTX-FEAT-016` Drools rules | COE authors, Risk approves | Upload workbook | Compile, test, approve, effective date, rollback | RWB-E1-072/073 |
| `CTX-FEAT-017` Interaction ledger | Audit reads every action | Any action | Append-only interaction record | RWB-E1-066/067/068 |
| `CTX-FEAT-018` Reporting | Manager reviews measures | Dashboard/report | Baseline and steering measures | RWB-E1-013, E2-009 |
| `CTX-FEAT-019` AI intake | System classifies and extracts | Document intake | Shadow recommendation, human confirms | RWB-E1-058/059/060 |
| `CTX-FEAT-020` AI deviation screening | Risk reviews deviations | Case event | Shadow flag, human decides | RWB-E1-062 |

## 14. Business rule catalogue

The full rule set is `Recovery Workbench Business Rules and Routing Logic v4`. This context keeps the
rules that shape the architecture and the story baseline; the rule tables remain the source of truth.

| Rule group | Rule IDs | Behaviour | Where |
|---|---|---|---|
| Entry and exclusion | ENTRY-*, EXCL-* | 90 DPD entry, exclusions, product scope | RWB-E1-018, package ENTRY/EXCLUSION |
| Allocation | ALLOC-001..031 | Queue, owner, capacity, priority | RWB-E1-020, package ALLOCATION |
| Assignment | ASSIGN-* | Officer skill, leave, capacity | RWB-E1-020, package ASSIGNMENT |
| Transfer | TRANSFER-* | Manual and rule transfer, reason | RWB-E1-021, package TRANSFER |
| Service level | SLA-*, TIMER-* | Stage clock, escalation, prescription | RWB-E1-028, E1-030 |
| Documents | DOC-* | Type, checklist, retention, extraction confidence | RWB-E1-024/041/050/054 |
| Decision log | DL-* | Every decision, rule and approver | RWB-E1-008/027 |
| Payments | PAYMENT_MATCH-* | Exact, partial, window, grace, floor | Epic 2 package PAYMENT_MATCH |
| Restructure | R-RES-* | TDR, settlement, deed in lieu | Epic 2 package RESTRUCTURE |
| Booking | BOOKING_MATCH-* | Booking confirmation | Epic 2 package BOOKING_MATCH |

## 15. Feature coverage reconciliation

| Source entry point | Feature / rule reference | Disposition | Evidence or gap |
|---|---|---|---|
| Case list, queue, filters | `CTX-FEAT-001`, ALLOC/ASSIGN | Covered | RWB-E1-002/020/031 |
| Case record, documents, history | `CTX-FEAT-002`, DOC | Covered | RWB-E1-023/035 |
| Case creation | `CTX-FEAT-003`, ENTRY | Covered | RWB-E1-018 |
| Transfer and approval | `CTX-FEAT-005`, TRANSFER, DoA | Covered | RWB-E1-021, E1-038 |
| Notices and letters | `CTX-FEAT-009`, templates | Covered | RWB-E1-046/052 |
| Intake from branches/SFTP/email | `CTX-FEAT-008`, DOC-INTAKE | Covered | RWB-E1-057/032 |
| OCR and extraction | `CTX-FEAT-008`, DOC-EXTRACT | Covered | RWB-E1-049/053 |
| Decision log and audit | `CTX-FEAT-010`, DL | Covered | RWB-E1-008/027, TE-008 |
| Configuration and reference data | `CTX-FEAT-011/012` | Covered | RWB-E1-042/043/045 |
| Access and masking | `CTX-FEAT-013` | Covered | RWB-E1-022/037/039 |
| ACE source data | `CTX-FEAT-014` | Covered | RWB-E1-069; RWB-ACE-001 |
| Temporal platform | `CTX-FEAT-015` | Covered in Epic 1; workflows from Epic 3 | RWB-E1-070/071 |
| Drools rules | `CTX-FEAT-016` | Covered | RWB-E1-072/073 |
| Interaction ledger | `CTX-FEAT-017` | Covered | RWB-E1-066/067/068 |
| Reporting | `CTX-FEAT-018` | Covered | RWB-E1-013, E2-009 |
| AI intake and screening | `CTX-FEAT-019/020` | Covered in shadow | RWB-E1-058/059/060/062/063 |
| Legacy loads and trackers | Removed | Out of scope | D-RCV-35; retirement register |
| Epic 3–8 journeys | Later epics | Not in this baseline | Release Plan v4 |

**Counts:** 20 business capabilities discovered; 20 mapped to an active story or an explicit
out-of-scope decision; 0 unresolved.

## 16. Gaps and contradictions

| ID | Gap / contradiction | Resolution | Status |
|---|---|---|---|
| `GAP-001` | ADR-003/004 and DT09/DT10 say no workflow or rules engine; the 16 Nov register adopts Temporal and Drools | ADR-011/012 and D-RCV-36 supersede them | Resolved |
| `GAP-002` | Older squad decision D-RCV-47 puts tables in schema `ace` with `rwb_` prefix; Physical Schema v6 and E1-069 use schema `recovery` | D-RCV-35 and ADR-010 win; D-RCV-47 is marked superseded | Resolved |
| `GAP-003` | Old D-RCV-35/36 IDs collide with the new client decisions | Renumbered to D-RCV-51/52 | Resolved |
| `GAP-004` | `RWB-E1-036` has no story file | Not created; not in the build sequence | Accepted |
| `GAP-005` | Thai labels and messages are proposed | DL10; English canonical | Open |
| `GAP-006` | Some story approvers are named only at the source-set level | Per-story plan gate records the named approver | Open |
| `GAP-007` | AMIS/RPS/LIT/WIN/GL/COLLINS ingestion by ACE is an assumption | ACE team lead confirms at the gate; otherwise U1 reopens for that source | Open |
| `GAP-008` | Temporal version, retention and RPO/RTO are not pinned | Environment Design v4 and DL26 | Open |
| `GAP-009` | The old 78 Epic 1 specs are against the pre-16 Nov baseline | They are archived; only the two implemented stories are re-specified in this run | Resolved for this baseline |

## 17. Source register

| ID | Source | Version | Used for |
|---|---|---|---|
| `SRC-01` | Project Overview | v4 | Business overview, outcomes |
| `SRC-02` | Business Architecture | v4 | Process and capability model |
| `SRC-03` | User Journeys / Case Journeys | v2 / v3 | Personas and journeys |
| `SRC-04` | Target Operating Model | v3 | Roles, queues, governance |
| `SRC-05` | Lean BRD Epic 1 / Epic 2 | v3 / v2 | Business requirements |
| `SRC-06` | Business Requirements Program / Epic 1 / Epic 2 | v4 / v4 / v4 | Requirement IDs |
| `SRC-07` | FSD P1–P10, S1–S9 | v6 (P3 v4) | Functional behaviour |
| `SRC-08` | TSD P1–P10, S1–S9 | v5 (P3/P4 v3) | Technical realisation |
| `SRC-09` | Target Architecture | v6 | Architecture |
| `SRC-10` | Architecture Decision Records | v3 | ADR-001–012 |
| `SRC-11` | Logical Data Model and Data Dictionary | v8 | Entities and fields |
| `SRC-12` | Physical Schema | v6 | 93 tables, 30 views |
| `SRC-13` | API Specification | v4 | Endpoints |
| `SRC-14` | Business Rules and Routing Logic | v4 | 448 rules |
| `SRC-15` | Case and Workflow Model | v5 | Stages, tasks, sentries |
| `SRC-16` | Users, Roles and Permissions | v4 | Roles and scopes |
| `SRC-17` | Error and Message Standard | v4 | Message IDs |
| `SRC-18` | Test Strategy / Test Cases / Regression Suite | v3 / v7 / v6 | Test levels and cases |
| `SRC-19` | Engineering Practices | v5 | Standards |
| `SRC-20` | ACE DB Alignment Change Register | v1, 15 Nov 2026 | D-RCV-35, views, tier map |
| `SRC-21` | Temporal and Drools Change Register | v1, 16 Nov 2026 | D-RCV-36, packages |
| `SRC-22` | Data Load Story Removals | v2, 15 Nov 2026 | Removed stories |
| `SRC-23` | Rule Story Retirements | v1, 16 Nov 2026 | Retired rule stories |
| `SRC-24` | RWB-E1-042 Migration and Clarifications | 10 Nov 2026 | Implemented migration |
| `SRC-25` | Build Sequence Epic 1 and Epic 2 | v6, 16 Nov 2026 | 115-item order |
| `SRC-26` | Decision Log | v10 | DT and D-RCV decisions |

## 18. Required guidance for SDD agents

1. Read this file, `domain-context.md`, `backend-context.md`, `frontend-context.md` and
   `testing-standards.md` before any story.
2. Treat `requirement/legacy/` as the source; `docs/` files are working copies. Do not edit a source
   document to make a story pass.
3. Treat D-RCV-35 and D-RCV-36 as binding. Do not rebuild an inbound load, tracker, `rule_row` loader,
   `payment_match_rule` table or a home-built workflow engine.
4. The schema is `recovery` and is always `${recoverySchema}`. Never write a schema literal.
5. Every endpoint has a Spring Security method check. Every decision writes the decision log with the
   rule ID and version.
6. Every threshold, limit, template, queue, role and route is reference data, not a literal.
7. A story with no business ACs is accepted on its business rules and test cases (D-RCV-16).
8. Record an open item; do not ask the user a question during an automated stage. The only exception
   is a safety or production-data issue, which stops the run.
9. If a source conflicts with a decision, the later decision wins; record the conflict in the story's
   `Clarification Log` and continue.

## 19. Decisions and open items

- Binding decisions: `docs/decisions/decision-register.md`.
- Open items: `docs/open-items.md`.
- Implemented stories: `RWB-E1-042` and `RWB-TE-001` (see `docs/increments/INDEX.md`).
- Planned and preserved: `RWB-E1-044`, `RWB-E1-043`.
- Retired: `RWB-E1-029`, `RWB-TE-005`, `RWB-E1-048`; removed: the seven data-load/tracker stories and
  `RWB-E1-051`.

## 20. Recent changes and version history

| Date | Change |
|---|---|
| 2026-11-16 | v2 context built from document set v14. D-RCV-35 (ACE DB views, no loads) and D-RCV-36 (Temporal, Drools) applied. 72 Epic 1 stories; 10 retired/removed. |
| 2026-11-15 | ACE DB alignment signed; U1–U5 and 30 views. |
| 2026-11-16 | Temporal and Drools signed; T1–T10, ADR-011/012, 11 new stories. |
| 2026-11-10 | RWB-E1-042 migration pack and RWB-TE-001 implementation evidence. |
| 2026-11-09 | Squad decisions D-RCV-34–50 carried into the baseline. |
