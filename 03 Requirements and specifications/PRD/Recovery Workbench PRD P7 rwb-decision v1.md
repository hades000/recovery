SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench PRD P7 rwb-decision v1
description: Product requirements for the Recovery Workbench decision center and log (P7 rwb-decision) in the 19-service realignment; the central decision ledger, approval routing within authority, the rule registry and its local evaluation, release slices by wave and acceptance criteria.
status: Draft
brd: 03 Requirements and specifications/Recovery Workbench Business Requirements Program v4.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 1 v4.docx; 03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v2.docx
fsd: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD P7 Decision center and log v3.md
service: P7 rwb-decision
epic: RWB-SVC-P7
wave: 1
decision: D-RCV-60
---

# Recovery Workbench PRD P7 rwb-decision v1

# 1. Document control and change log

## 1.1 Document control

| Attribute | Value |
|---|---|
| Document title | Recovery Workbench PRD P7 rwb-decision |
| Document ID | P7-RWB-PRD-v1 |
| Version | 1 |
| Status | Draft |
| Classification | Confidential |
| Date | 22 November 2026 |
| Service | P7 rwb-decision (Decision center and log) |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epics served | EP01 (Epic 1, wave 1); EP02 (Epic 2, wave 2); EP04 (Epic 4, wave 3); EP08 (Epic 8, wave 4) |
| Schema | `rwb_decision` |
| REST base | `/api/recovery/decision/v1` |
| Topic published | `rwb.decision.events.v1` (ApprovalRequested, ApprovalDecided, RulePackageInForce) |
| Topic consumed | `rwb.decision-record.v1` (DecisionRecorded, from all 19 services) |
| Temporal task queue | `rwb-decision` |
| Java package | `th.co.scb.ace.workbench.recovery.decision` |
| Product owner role | Product owner for decision and rules (the BRD owner roles are Center of excellence, Risk with Credit, Compliance, Internal audit, Business lead, Legal counsel, Team manager) |
| Requirement owner role | Center of excellence analyst with the compliance and PDPA officer |
| Decision | D-RCV-60 (microservice realignment); inherits ADR-017 (embedded Drools, registry in rwb-decision), ADR-022 (local decision record plus central ledger) and ADR-020 (contract-first REST) |
| Upstream artifacts | Business Requirements Program v4; Business Requirements Epic 1 v4; Business Requirements Epic 2 v2; FSD P7 Decision center and log v3; TSD P7 Decision center and log v2; Architecture v5; Temporal and Drools Design v1 |
| Upstream requirement IDs | REQ-DRI-001 to REQ-DRI-005, REQ-DRI-009 to REQ-DRI-012; REQ-APD-001 to REQ-APD-011; REQ-ILG-001 to REQ-ILG-014 (served by rwb-source-data, §5.1); NFR-007, NFR-008, NFR-011, NFR-013, NFR-020, NFR-021, NFR-022, NFR-023, NFR-024, NFR-025, NFR-026, NFR-027, NFR-030, NFR-033, NFR-034, NFR-035, NFR-036, NFR-039, NFR-040, NFR-042, NFR-046, NFR-047, NFR-049, NFR-051, NFR-052, NFR-053, NFR-054, NFR-059, NFR-064, NFR-065, NFR-067, NFR-068, NFR-078 |
| Upstream acceptance criteria | AC-P7-001-01, AC-ALT-P7-001-01 to -02, AC-EXC-P7-001-01 to -03; AC-P7-002-01, AC-ALT-P7-002-01, AC-EXC-P7-002-01 to -07; AC-P7-007-01, AC-ALT-P7-007-01 to -02, AC-EXC-P7-007-01 to -05; AC-P7-009-01, AC-ALT-P7-009-01 to -02, AC-EXC-P7-009-01 to -02; AC-P7-015-01, AC-ALT-P7-015-01 to -02, AC-ALT-P7-016-02, AC-EXC-P7-015-01 to -06; AC-P7-022-01, AC-ALT-P7-022-01 to -02, AC-EXC-P7-022-01 to -02; AC-P7-024-01, AC-ALT-P7-024-01 to -02, AC-EXC-P7-024-01 to -05; AC-BG-P7-001-01 |
| Generated IDs | CAP-P7-001 to CAP-P7-018; FR-P7-001 to FR-P7-036; NFR-P7-001 to NFR-P7-022; AC-P7-001 to AC-P7-022; JRN-P7-01 to JRN-P7-06; ROL-P7-01 to ROL-P7-10; OQ-P7-01 to OQ-P7-12 |
| Run ID, branch, commit, pull request | Not applicable. This run writes documents only: no repository branch, commit or pull request is created, and no issue tracker is read or updated (rule 3, U6) |
| Source baseline | FSD P7 Decision center and log v3 (15 November 2026), TSD P7 Decision center and log v2 (28 October 2026) and the BRD Program v4 / Epic 1 v4 / Epic 2 v2 (15 November 2026), realigned to Architecture v5 under D-RCV-60 |

## 1.2 Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## 1.3 Inherited history and ID continuity

The product baseline is FSD P7 Decision center and log v3. Its requirement set, feature codes and acceptance criteria are carried unchanged; the realignment changes the owner of the interaction ledger, the rule evaluation position, the notice pipeline and the delivery wave, not the requirement substance.

| Version | Date | Change carried from the FSD |
|---|---|---|
| 2 | 28 October 2026 | Decision log store and writer, approval routing with the delegation of authority table, the approval screen for D7.1 notices, and the interaction ledger held beside the decision log |
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 (ADR-010). The module reads no source data directly: freshness comes from `v_ace_batch_status` through the source-data contract, EFS interactions are read through `v_ace_efs_action`, and proof of delivery reads `v_ace_pod` (INT-15 and JOB-09 removed). FEAT-DRI-06 and JOB-13 keep their IDs and are marked removed with their later home. |
| 1 (PRD) | 22 November 2026 | First PRD of this family. CAP, FR, NFR, AC, journey and role IDs are new. The FSD requirement IDs (REQ-DRI-xxx, REQ-APD-xxx, REQ-ILG-xxx), feature IDs (FEAT-DRI-xx, FEAT-APD-xx, FEAT-ILG-xx), acceptance criteria IDs (AC-P7-xxx, AC-ALT-P7-xxx, AC-EXC-P7-xxx), validation rule IDs (VR-P7-xxx), business rule IDs (BR-P7-xxx), message IDs (MSG-P7-001 to MSG-P7-011), decision codes (D5.1 to D9.3, X1 to X7), rule package codes, table names, event IDs (EV-08, EV-09, EV-13, EV-28, EV-30), job IDs (JOB-13, JOB-14, JOB-20), API operation IDs (API-P7-001 to API-P7-008) and screen IDs (SCR-10, SCR-11, SCR-12, SCR-38) are preserved character for character |

## 1.4 Documents this PRD is read against

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program v4 | BRD | Source of the P7 requirements (REQ-DRI-xxx, REQ-APD-xxx, REQ-ILG-xxx) and the non-functional requirements |
| Recovery Workbench Business Requirements Epic 1 v4 | BRD | Source of the Epic 1 requirement text and the story refs RWB-E1-008, RWB-E1-014, RWB-E1-027, RWB-E1-029, RWB-E1-038, RWB-E1-052, RWB-E1-066 to RWB-E1-068 |
| Recovery Workbench Business Requirements Epic 2 v2 | BRD | Source of the Epic 2 requirements REQ-DRI-012 and REQ-APD-001 to REQ-APD-011 |
| Recovery Workbench Functional Specifications by Module v6, FSD P7 Decision center and log v3 | FSD | Pair: the functional baseline this PRD re-expresses as product behaviour |
| Recovery Workbench Technical Specifications by Module v5, TSD P7 Decision center and log v2 | TSD | Source of the field lists, the lists of values and the operation inventory (API-P7-001 to API-P7-008) |
| Recovery Workbench Architecture v5 | Architecture | Constraint: 19 services with one schema and login each, Kafka with outbox and inbox, Temporal, embedded Drools with a central registry, no data lake, edge and gateway |
| Recovery Workbench Temporal and Drools Design v1 | Design | Constraint: workflow kit, ApprovalWorkflow, Schedules 00:01 and 02:00, four-eyes rule approval, checksum and atomic swap, strict mode at the four points of no return |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, operation, event, job and workflow used in this document |
| Recovery Workbench Non Functional Specification v3 | Non-functional | Source of the numeric targets |
| Recovery Workbench Microservice Story Template and Rules v1 | Rules | Header, versioning, placeholder and register rules |

# 2. Product overview and relationship to ACE

## 2.1 Purpose

rwb-decision (P7) is the recovery module's central decision ledger, its approval authority and its rule registry. It turns three separate promises into one product: every decision the Workbench or a person takes is recorded once and cannot be changed; every decision that needs authority is approved by the role that holds it; every rule that decides anything is authored, tested, approved and dated in one place and runs inside the service that owns the decision.

## 2.2 What is new in this release

| New | What it is | Business reason |
|---|---|---|
| The service rwb-decision | One deployable with its own API and worker, schema `rwb_decision`, login, topic `rwb.decision.events.v1`, task queue `rwb-decision` and lifecycle | Decision authority and evidence become one owned contract instead of a module inside a single deployable |
| The central ledger fed from the event stream | Each of the 19 services writes its decision record in its own schema in the same transaction as the state change and publishes DecisionRecorded (EV-08); this service consumes it idempotently into the central ledger | A synchronous central log write across 19 services would be a distributed transaction; the local record keeps the action safe and the central ledger makes it searchable |
| Strict mode at the four points of no return | Debt transfer, write-off posting, auction sale and title transfer wait for the ledger acknowledgement; everything else carries on | The four irreversible steps are the only ones where "recorded" must be true before the act |
| The daily WORM seal | The ledger fingerprint is stored in write-once storage every day | Evidence that the log was not rewritten, to the standard an auditor or a court applies |
| Approval as a product behaviour | DoA routing, approve, change, return, refuse, override, escalation and the committee record, on one workflow template | Authority is exercised and evidenced in one place, with the limit and its version on every item |
| The rule registry | Package, version, rows, at least 50 test scenarios, four-eyes approval, effective dating, one-call rollback, promotion at 00:01 | A rule change is a governed business act, not a code release |
| Rule packages published for local evaluation | RulePackageInForce (EV-30) plus `GET /rule-models/{packageCode}/{version}` with its checksum | Each service keeps its own approved copy and no shared rule server sits on the hot path |

## 2.3 What is reused, and what leaves the service

| Capability | Verdict | Owner in v5 |
|---|---|---|
| ACE database, sign-in, multi-factor authentication, audit and PII logging to ACE common | REUSE | ACE common |
| Role, permission, scope, masking policy and the delegation of authority table | REUSE | P4 rwb-access |
| Case record, case state, case queue and the case timeline screen | REUSE | P3 rwb-case |
| Documents behind an approval (demand, recall and guarantor notices) | REUSE | P5 rwb-document |
| Notice generation, letter templates, the template catalog with merge fields and proof of delivery from WIN | REUSE, elsewhere | P6 rwb-comms (document generation and the WIN file through P2 rwb-integration) |
| Data product freshness behind a decision input | REUSE | P1 rwb-source-data |
| Agent runs, prompts and model versions | REUSE | P10 rwb-agent |
| Reporting measures from the decision log | REUSE, elsewhere | P9 rwb-reporting (this service publishes the events and serves the population query) |
| Embedded Drools runtime and the workflow kit | REUSE | Platform library and Temporal workflow kit |
| The interaction ledger (FEAT-ILG-01 to FEAT-ILG-10; REQ-ILG-001 to REQ-ILG-014) | MOVED out of this service | P1 rwb-source-data (R-PREC default ruling, DP-18; GAP-1612; ASM-2748) |
| The nightly decision log copy to the data lake (FEAT-DRI-06, REQ-DRI-009, JOB-13 at 01:00) | REMOVED | None. There is no data lake; ingest is continuous from Kafka (GAP-1613; ASM-2749) |
| Notice generation, template management, the template catalog and proof of delivery (FEAT-DRI-14 to FEAT-DRI-17, A2.10 to A2.13) | MOVED out of this service | P6 rwb-comms; P5 for the document; P2 for the WIN file (GAP-1614; ASM-2750) |
| Rule evaluation and the decision answer inside the workflow (FEAT-DRI-07 evaluation, FEAT-DRI-08) | MOVED out of this service | Each owning service with the platform Drools kit (DP-04); this service keeps the registry and the approval (GAP-1615; ASM-2751) |
| Approval limits table load and approval (A2.24 load path) | MOVED out of this service | P4 rwb-access owns the table; this service reads it at decision time (GAP-1616; ASM-2752) |

## 2.4 Constraints confirmed in Architecture v5 that bound the product

1. One ACE PostgreSQL server; a schema and a login per service; this service writes only `rwb_decision` and reads no other service's tables (ADR-014, DP-01, DP-02).
2. REST is one hop from gateway-bff with a 2 s timeout; anything longer is a workflow (ADR-020, DP-11).
3. Events are CloudEvents on Kafka with outbox and inbox; this service publishes on `rwb.decision.events.v1` and consumes `rwb.decision-record.v1`, with retry and `.dlt` topics (ADR-015, DP-09, DP-14).
4. Temporal namespace `rwb-recovery`, task queue `rwb-decision`; ApprovalWorkflow comes from the kit; Schedules replace Quartz: rule promotion 00:01 (JOB-20) and chain check 02:00 (JOB-14) (ADR-016, DP-10).
5. Rule governance is central here and evaluation is local; each model has exactly one owning service, which loads it, verifies the checksum and swaps it atomically, keeping the last good model (ADR-017, DP-04).
6. There is no data lake and no Power BI connection: INT-19 and INT-20 are removed and reporting reads events into rwb-reporting (ADR-018, DP-17).
7. The decision ledger is hash-chained and sealed daily to immutable (WORM) storage; personal data stays out of events, workflow inputs and logs (Arch v5 slides 28 and 45).
8. Dead-letter and replay rules, typed failures and the non-retryable list follow the platform standard (Arch v5 slide 13).

# 3. Personas and roles

Roles only; no person is named anywhere in this document.

| ID | Persona | What they need from this product | Primary journeys |
|---|---|---|---|
| ROL-P7-01 | Approver within authority (case owner, product head for Mortgage, HP and SSME, head of litigation, head of NPA, head of asset liquidity) | One queue, the recommendation with its reasons and inputs, the limit that applies, and a decision that is recorded | JRN-P7-02, JRN-P7-03 |
| ROL-P7-02 | Preparer of a decision (restructuring officer, litigation officer, sale officer, write-off team member) | A preparer who can see what is waiting and cannot approve their own work | JRN-P7-02 |
| ROL-P7-03 | Credit approval committee member and write-off committee member | A committee decision recorded with the members present and the decision taken | JRN-P7-05 |
| ROL-P7-04 | Center of excellence analyst (rule author) | A rule package they can author, test against at least 50 scenarios, and hand to a second pair of eyes | JRN-P7-04 |
| ROL-P7-05 | Risk and model risk officer (rule approver) | Four-eyes approval, effective dating, and one-call rollback with the version kept | JRN-P7-04 |
| ROL-P7-06 | Internal audit | One place to search every decision, with the rule and model versions, the approver and the final call, and a chain that is checked daily | JRN-P7-05 |
| ROL-P7-07 | Compliance and PDPA officer | A break reported the same day, retention stated by class, and personal data masked | JRN-P7-04, JRN-P7-05 |
| ROL-P7-08 | Platform administrator | A gap alert when a record does not reach the ledger, run books for every job, and a rerun path | JRN-P7-01 |
| ROL-P7-09 | Owning service (rwb-case, rwb-valuation, rwb-treatment, rwb-litigation, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-payment, rwb-deviation, rwb-comms, rwb-document) | A typed record contract, an idempotent seal, the model fetch with its checksum, and a strict-mode acknowledgement | JRN-P7-01, JRN-P7-06 |
| ROL-P7-10 | Developer and solution architect | One schema, one topic, one event contract, and a build that fails on a cross-schema read or an unrecorded action | JRN-P7-06 |

Non-human actors: the outbox relay, the inbox consumer, the Temporal worker, the Schedule triggers at 00:01 and 02:00, the WORM seal writer, and the 19 services that publish DecisionRecorded.

# 4. User journeys

## 4.1 Current state (as built in the monolith)

1. The decision log is written synchronously inside the call, in the same schema as everything else, so one slow log write slows every action.
2. A decision that needs approval is found by asking the approver, by mail or by telephone; the limit is a spreadsheet and the version of the limit used is rarely recorded.
3. A rule change is a code release, or a database update made by hand with no test evidence kept.
4. The decision log is copied nightly at 01:00 to a data lake; when the copy fails, nobody notices until a report is short.
5. The chain is checked by a job that writes a row, and a break is found by a person reading a report.

Consequence: the reason for a route, the authority for it and the rule that produced it are three separate answers, and no one can prove they belong together.

## 4.2 Target state (this product)

### JRN-P7-01 A decision is taken and sealed (continuous, every service)

1. A service takes a decision — a case created, an owner assigned, a case transferred, a document attached, a route proposed, an offer approved — and writes its own decision record in its own schema inside the same transaction as the change.
2. It publishes DecisionRecorded (EV-08) through its outbox to `rwb.decision-record.v1`, holding the decision code, the case, the rule and model versions, the inputs reference, the recommendation, the approver and the final call.
3. This service consumes the event idempotently and appends one entry to the central ledger, with the chain sequence, the hash of the previous entry and its own hash.
4. The completeness check sees the record in the ledger inside the completeness target; a record missing after that target raises a gap alert naming the case and the publishing service.
5. At the four points of no return the step waits for the acknowledgement; everywhere else the work carries on at full speed.

### JRN-P7-02 An approval is routed and decided (within the working day)

1. A prepared decision that needs authority creates an approval with its decision code, capability area, product group, amount, terms and preparer.
2. The router reads the delegation of authority limits through the access service, at the moment of the decision, and assigns the approval to the level and holder the table names; the row ID and the version are written on the item.
3. The item appears in the approver's queue with its amount, level, due time and age, and never in the queue of the person who prepared it.
4. The approver approves, changes the terms within the limit, returns it with a question, or refuses it with a coded reason; the change above the limit re-routes upward rather than approving.
5. The decision is written to the ledger with the approver, the level, the limit version and the final call, and the case moves on.

### JRN-P7-03 An approval is overdue (unattended, every service level)

1. The service level timer breaches for an approval that is still waiting.
2. The item moves to the next role in the matrix with an escalation level and a new due time, one ledger entry records the escalation, and the new holder is told.
3. A level with no holder and no substitute escalates at once with the reason recorded; it never stalls a case.

### JRN-P7-04 A rule is changed (on change, four eyes)

1. The center of excellence analyst authors the decision table, loads it with a valid-from date and runs it against at least 50 test scenarios.
2. The load checks run: compile, schema, overlap, unreachable row, default row, scenario count and a dry run; a refused load stores nothing and the version in force stays.
3. The author cannot approve their own package; the risk officer approves it.
4. At 00:01 the promotion job puts the version in force and publishes RulePackageInForce (EV-30); each owning service fetches the model, verifies the checksum and swaps it in.
5. A rollback is one call with a reason; a decision taken under the earlier version keeps that version on its record.

### JRN-P7-05 A decision is audited (on request)

1. The auditor searches the ledger by case, decision, rule, approver and date range and reads one entry with its inputs reference, versions, approver, final call, actions and outcome.
2. The auditor asks for a population of cases and receives the decision history with the inputs, versions, approver and final call, and the document references behind it.
3. The chain check result of the business date proves the log was not rewritten; the daily WORM seal proves the fingerprint of that date.

### JRN-P7-06 The service is operated (unattended, daily)

1. The chain check runs at 02:00 over every entry; a break is reported to Compliance the same day and raises an incident.
2. The WORM seal stores the fingerprint of the ledger every business date.
3. The rule promotion runs at 00:01; a package that fails to load on a consumer leaves the last good model in place and raises an alert.
4. Every job has a run book, an alert and a named owner role, and a rerun is idempotent for its business date.

# 5. Capabilities and features

Each capability is one releasable slice of product behaviour. Priorities follow the BRD: Must is needed for the epic to release; Should is planned in the epic.

| CAP ID | Capability | What changes for the user | BR IDs | MoSCoW | Wave | FSD features |
|---|---|---|---|---|---|---|
| CAP-P7-001 | Central decision ledger: one sealed entry per decision | Every decision is found in one place and cannot be quietly changed | REQ-DRI-001, REQ-DRI-002, REQ-DRI-004 | Must | 1 | FEAT-DRI-01, FEAT-DRI-02 (A2.1, A2.2); RWB-E1-008, RWB-E1-027 |
| CAP-P7-002 | Local record contract and the completeness duty | No action proceeds without a record, and a record that never arrives is noticed | REQ-DRI-005 | Must | 1 | FEAT-DRI-05 (A2.5); RWB-E1-027 |
| CAP-P7-003 | Hash chain, daily chain check and the WORM seal | The log can be relied on in an audit, including years later | REQ-DRI-003 | Must | 1 | FEAT-DRI-01 (A2.1); JOB-14 |
| CAP-P7-004 | Decision history read for audit and evidence | An auditor answers a population question without touching the live log | REQ-DRI-012 | Must | 2 | A2.1 read path; RWB-E2-005; SCR-38 |
| CAP-P7-005 | Freshness of every input on the record | A decision taken on stale data says so, and on which date | REQ-DRI-001, NFR-013 | Must | 1 | FEAT-DRI-12 (A2.9); RWB-E1-015 |
| CAP-P7-006 | Model, agent and prompt versions on the record | A model or agent answer is evidenced on the same terms as a person's | REQ-DRI-001, NFR-078 | Must | 1 | FEAT-DRI-03 (A2.3) |
| CAP-P7-007 | Rule registry with four eyes, effective dating and rollback | A rule change is a governed act with test evidence, not a release | REQ-DRI-010, REQ-DRI-011 | Must | 1 | FEAT-DRI-07 governance (A2.7); RWB-E1-029 |
| CAP-P7-008 | Rule package in force and the local model contract | Every service runs the same approved version, and the version is on the record | REQ-DRI-010 | Must | 2 | A2.7 publish path; EV-30; RWB-E2-042 |
| CAP-P7-009 | Approval routed by the delegation of authority | The right level sees the item, and the limit version is recorded | REQ-APD-001, REQ-APD-004, REQ-APD-009 | Must | 2 | FEAT-APD-01, FEAT-APD-05, FEAT-APD-10 (A2.15, A2.19, A2.24); RWB-E2-013 |
| CAP-P7-010 | Approve, change, return, refuse and override with reasons | An approver can act within their authority and every outcome is evidenced | REQ-APD-003, REQ-APD-005 | Must | 2 | FEAT-APD-02 to FEAT-APD-04, FEAT-APD-07 (A2.16 to A2.18, A2.21) |
| CAP-P7-011 | Escalation when an approval is overdue or unheld | A case never waits because a role is empty | REQ-APD-007, REQ-APD-011 | Must | 2 | FEAT-APD-06 (A2.20) |
| CAP-P7-012 | Approval queue and decision screen | The approver sees the recommendation, reasons, inputs and limit on one screen | REQ-APD-002 | Must | 2 | FEAT-APD-09 (A2.23); SCR-10, SCR-11 |
| CAP-P7-013 | D7.1 demand and recall notice approval | The first live use of approval routing, on the notice a customer receives | REQ-APD-006 | Must | 2 | FEAT-APD-08 (A2.22); RWB-E2-014 |
| CAP-P7-014 | Committee decision recorded | A committee decision carries its members and its outcome | REQ-APD-008 | Must | 3 | SCR-12; A2.16 committee path |
| CAP-P7-015 | Delegation of authority version per item | An open item keeps the limit it was decided under | REQ-APD-010 | Must | 2 | FEAT-APD-10 (A2.24) |
| CAP-P7-016 | Strict mode at the four points of no return | The irreversible step waits until the decision is provably sealed | REQ-DRI-005 | Must | 2 | A2.5; Arch v5 slide 28 |
| CAP-P7-017 | Rule change and override reporting | Overrides and rule changes are reviewed monthly, not discovered | REQ-APD-005, REQ-DRI-011 | Should | 4 | RWB-E2-041; A2.21 |
| CAP-P7-018 | Retention class for the ledger and the decision record | The store holds what policy allows and nothing older, stated once | NFR-030 | Should | 1 | A2.1; NFR-030 (open, DL26) |

## 5.1 Capabilities not carried into the product

| Capability | Status | Later home |
|---|---|---|
| Write every Workbench event to the ledger (FEAT-ILG-01) | Moved | P1 rwb-source-data, the one interaction ledger (GAP-1612; ASM-2748) |
| Hold the ledger beside the decision log (FEAT-ILG-02) | Moved | P1 rwb-source-data; the two stores stay separate and are not one table (GAP-1612; ASM-2748) |
| Read the ledger in one ordered sequence (FEAT-ILG-03) | Moved | P1 ledger read; the case timeline screen stays P3 (GAP-1612; ASM-2748) |
| Reject a duplicate ledger entry (FEAT-ILG-04) | Moved | P1 rwb-source-data (REQ-ILG-007) |
| Raise an incident when the ledger cannot be written (FEAT-ILG-05) | Moved | P1 rwb-source-data (REQ-ILG-008) |
| Bring contact, dispatch and hand-over outcomes into the ledger (FEAT-ILG-06 to FEAT-ILG-08) | Moved | P1 rwb-source-data with P2 and P8 as sources (REQ-ILG-009 to REQ-ILG-011) |
| Read the ledger as a timeline on the case (FEAT-ILG-09) | Moved | P3 rwb-case reads the P1 ledger; the screen is not this service's (GAP-1612; ASM-2748) |
| Set the retention class for ledger entries (FEAT-ILG-10) | Moved | P1 rwb-source-data (REQ-ILG-013) |
| Stream the decision log to the data lake (FEAT-DRI-06; REQ-DRI-009; JOB-13 nightly copy and REC-08 row counts) | Removed | None. No data lake in v5; ingest is continuous from Kafka (GAP-1613; ASM-2749) |
| Generate notices from approved templates to WIN (FEAT-DRI-14) | Moved | P6 rwb-comms with P5 for the document and P2 for the WIN file (GAP-1614; ASM-2750) |
| Manage letter templates with Legal approval (FEAT-DRI-15) | Moved | P6 rwb-comms (GAP-1614; ASM-2750) |
| Hold the template catalog with merge fields (FEAT-DRI-16) | Moved | P6 rwb-comms (GAP-1614; ASM-2750) |
| Capture proof of delivery from WIN (FEAT-DRI-17) | Moved | P6 rwb-comms reads `v_ace_pod`; the file is P2's (GAP-1614; ASM-2750) |
| Run the rules component on versioned rule tables for evaluation (FEAT-DRI-07, evaluation half) | Moved | Each owning service with the platform Drools kit (DP-04); this service keeps the registry (GAP-1615; ASM-2751) |
| Expose the decision service to the workflow (FEAT-DRI-08) | Moved | The owning service answers the recommendation; this service serves the approval and the sealed record (GAP-1615; ASM-2751) |
| Run run books and monitoring for every job (FEAT-DRI-18) | Reused | Platform observability (RWB-PLT-OBS); the run books for JOB-14 and JOB-20 are this service's duty (NFR-067) |
| Load and approve the delegation of authority file (A2.24 load path, AC-P7-024-01) | Moved | P4 rwb-access owns `delegation_limit`; this service reads it at decision time (GAP-1616; ASM-2752) |

# 6. Functional requirements

Every requirement is specific and testable. The FSD REQ column keeps the trace to the source requirement the FSD serves.

| FR ID | Requirement | CAP | BR | FSD REQ | Priority | Wave |
|---|---|---|---|---|---|---|
| FR-P7-001 | The service SHALL consume DecisionRecorded (EV-08) from all 19 services on topic `rwb.decision-record.v1` and SHALL append one central ledger entry per decision, holding the case, the decision code, the rule ID and version, the model version, the agent and prompt version, the inputs reference, the recommendation, the approver and approval level, the final call, the actions, the outcome and the time decided. | CAP-P7-001 | REQ-DRI-001 | REQ-DRI-001 | Must | 1 |
| FR-P7-002 | The service SHALL accept and seal the Epic 1 record types — case creation, owner assignment, case transfer and document attachment — and SHALL accept any decision code in D5.1 to D9.3, X1 to X7 or an access event, refusing any other code. | CAP-P7-001 | REQ-DRI-004 | REQ-DRI-004 | Must | 1 |
| FR-P7-003 | The service SHALL keep the ledger append only: an UPDATE or a DELETE on an entry SHALL be refused both by the missing grant of the service role and by the append-only trigger, and a correction SHALL be a new entry naming the entry it corrects. | CAP-P7-001 | REQ-DRI-002 | REQ-DRI-002 | Must | 1 |
| FR-P7-004 | The service SHALL chain every entry: `chain_seq` SHALL run from 1 without a gap, `prev_hash` SHALL equal the `entry_hash` of the entry before it with 64 zeros for the first, and `entry_hash` SHALL be the SHA-256 of the entry's canonical form. | CAP-P7-003 | REQ-DRI-003 | REQ-DRI-003 | Must | 1 |
| FR-P7-005 | The service SHALL refuse a record that carries no decision code, no rule version where a rule is named, or no inputs reference, and SHALL return the refusal with MSG-P7-009 naming the missing field, leaving no entry and rolling back the change in the same transaction. | CAP-P7-001 | REQ-DRI-001 | REQ-DRI-001 | Must | 1 |
| FR-P7-006 | The service SHALL write one entry when the same event arrives twice with the same idempotency key, SHALL return the first entry's ID and SHALL count the repeat. | CAP-P7-001 | REQ-DRI-001 | REQ-DRI-001 | Must | 1 |
| FR-P7-007 | The service SHALL publish the local record contract: a decision record written in the caller's schema inside the same transaction as the state change, and no action that proceeds when its record cannot be written; a failed write SHALL return MSG-P7-003 and raise an incident. | CAP-P7-002 | REQ-DRI-005 | REQ-DRI-005 | Must | 1 |
| FR-P7-008 | The service SHALL answer a strict-mode acknowledgement for debt transfer, write-off posting, auction sale and title transfer, and SHALL apply strict mode to no other step. | CAP-P7-016 | REQ-DRI-005 | REQ-DRI-005 | Must | 2 |
| FR-P7-009 | The service SHALL raise a gap alert naming the case and the publishing service when a record present in a service does not reach the ledger inside the completeness target, and SHALL keep the alert open until the record arrives. | CAP-P7-002 | REQ-DRI-001, REQ-DRI-005 | REQ-DRI-001 | Must | 1 |
| FR-P7-010 | The service SHALL store on every entry the inputs reference and, in the inputs snapshot, the business date, load time and status of every data product the decision read, taken from rwb-source-data and never inferred. | CAP-P7-005 | REQ-DRI-001, NFR-013 | REQ-DRI-001 | Must | 1 |
| FR-P7-011 | The service SHALL carry the model, agent and prompt version on every entry where a model or an agent contributed, and SHALL treat an agent's write on the same terms as a person's decision. | CAP-P7-006 | REQ-DRI-001, NFR-078 | REQ-DRI-001 | Must | 1 |
| FR-P7-012 | The service SHALL check the whole chain once every business date at 02:00 (JOB-14) and SHALL report a break to Compliance the same day with the first broken `chain_seq`, the entry ID and the case, and SHALL raise an incident. | CAP-P7-003 | REQ-DRI-003 | REQ-DRI-003 | Must | 1 |
| FR-P7-013 | The service SHALL store the ledger fingerprint of each business date in write-once storage, holding the business date, the last `chain_seq`, the last `entry_hash`, the fingerprint, where it was stored and when. | CAP-P7-003 | REQ-DRI-003 | REQ-DRI-003 | Must | 1 |
| FR-P7-014 | The service SHALL return one entry with its inputs reference, rule and model versions, recommendation, approver and level, final call, actions, outcome, the time decided, `prev_hash`, `entry_hash` and the entry it corrects. | CAP-P7-004 | REQ-DRI-012 | REQ-DRI-012 | Must | 1 |
| FR-P7-015 | The service SHALL search the ledger by case, decision code, rule ID, approver and date range, paged, with an export, returning personal fields masked where the role holds no unmasked masking row. | CAP-P7-004 | REQ-DRI-012 | REQ-DRI-012 | Must | 2 |
| FR-P7-016 | The service SHALL answer a population query for audit with the decision history of every case in the population, holding each decision's inputs, versions, approver, final call and the references of the documents behind it. | CAP-P7-004 | REQ-DRI-012 | REQ-DRI-012 | Must | 2 |
| FR-P7-017 | The service SHALL route an approval to the level and holder the delegation of authority names for that decision, product and amount, read at the moment of the decision, SHALL write the delegation row ID and the limit version on the item, SHALL never assign it to the preparer, and SHALL set the case to Waiting approval. | CAP-P7-009 | REQ-APD-001, REQ-APD-009 | REQ-APD-001 | Must | 2 |
| FR-P7-018 | The service SHALL refuse an approval above the holder's limit, raise it to the next level with message MSG-P7-001 and record no approval at the lower level; where no limit covers the decision it SHALL store the item as HELD_NO_LIMIT and raise an incident with MSG-P7-010. | CAP-P7-009 | REQ-APD-004 | REQ-APD-004 | Must | 2 |
| FR-P7-019 | The service SHALL give the approver the recommendation, its reasons, the inputs used and the limit that applies on one screen, and SHALL return the current recommendation for a case with its reasons and expected return by route. | CAP-P7-012 | REQ-APD-002 | REQ-APD-002 | Must | 2 |
| FR-P7-020 | The service SHALL let an approver approve, change, return with a question or refuse, SHALL require a reason on a refusal and on an override, and SHALL record each outcome on the ledger entry with the change and its coded reason. | CAP-P7-010 | REQ-APD-003 | REQ-APD-003 | Must | 2 |
| FR-P7-021 | The service SHALL re-route an approval whose terms are changed above the approver's limit rather than approving it, and SHALL record the final call as APPROVED_CHANGED with the terms proposed, the terms chosen and the reason code. | CAP-P7-010 | REQ-APD-003, REQ-APD-005 | REQ-APD-003 | Must | 2 |
| FR-P7-022 | The service SHALL require a coded reason for an override of a recommendation and SHALL record it on the entry so that the overrides of a period can be reported with their reasons. | CAP-P7-010, CAP-P7-017 | REQ-APD-005 | REQ-APD-005 | Must | 2 |
| FR-P7-023 | The service SHALL escalate an approval that is not answered inside its service level to the named role, with an escalation level and a new due time, SHALL write the final call ESCALATED, and SHALL tell the new holder. | CAP-P7-011 | REQ-APD-007 | REQ-APD-007 | Must | 2 |
| FR-P7-024 | The service SHALL escalate an approval at once where the level has no holder and no substitute, SHALL record the reason NO_HOLDER, and SHALL never leave a case stalled on an empty role. | CAP-P7-011 | REQ-APD-011 | REQ-APD-011 | Should | 2 |
| FR-P7-025 | The service SHALL record a committee decision against the item with the members present and the decision taken, and SHALL write it to the ledger with its approver and level. | CAP-P7-014 | REQ-APD-008 | REQ-APD-008 | Must | 3 |
| FR-P7-026 | The service SHALL record the limit version on every approval and SHALL keep an open item on the version it was routed and decided under when the table changes. | CAP-P7-015 | REQ-APD-010 | REQ-APD-010 | Must | 2 |
| FR-P7-027 | The service SHALL list an approver's queue with the decision code, capability area, product group, amount, approval level, due time and age of each item, and SHALL show an item to no one who prepared it. | CAP-P7-012 | REQ-APD-002 | REQ-APD-002 | Must | 2 |
| FR-P7-028 | The service SHALL put a D7.1 demand or recall notice through the approval path, with the template and its version on the approval, and SHALL refuse the approval with MSG-P6-003 where the template has been withdrawn. | CAP-P7-013 | REQ-APD-006 | REQ-APD-006 | Must | 2 |
| FR-P7-029 | The service SHALL write back to the ledger the outcome of an approved decision — what was done, by which system and when — and SHALL keep the recommendation and the final call distinct on the entry. | CAP-P7-001 | REQ-DRI-001 | REQ-DRI-001 | Must | 2 |
| FR-P7-030 | The service SHALL hold the rule registry as package, version, parsed row and test case, SHALL require at least 50 test scenarios to pass before approval, SHALL refuse an approval by the author, and SHALL carry the version states LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED. | CAP-P7-007 | REQ-DRI-010, REQ-DRI-011 | REQ-DRI-010 | Must | 1 |
| FR-P7-031 | The service SHALL run every load check — compile, schema, overlap, unreachable row, default row, at least 50 scenarios and a dry run — and SHALL store nothing and keep the version in force when a check fails, refusing with MSG-P3-027 naming the row or the scenario. | CAP-P7-007 | REQ-DRI-010 | REQ-DRI-010 | Must | 1 |
| FR-P7-032 | The service SHALL roll back a rule package version in one call with a reason, SHALL record the rollback with its author and time, and SHALL leave the rule version on every decision already taken unchanged. | CAP-P7-007 | REQ-DRI-011 | REQ-DRI-011 | Must | 1 |
| FR-P7-033 | The service SHALL put an approved version in force at 00:01 (JOB-20), publish RulePackageInForce (EV-30) with the package, version and checksum, and serve the model for a package and version with its checksum for the owning service to verify and swap. | CAP-P7-008 | REQ-DRI-010 | REQ-DRI-010 | Must | 2 |
| FR-P7-034 | The service SHALL read every parameter, limit, threshold, name and route it uses from a versioned data row at run time, never from a constant in code, and SHALL apply a change from its valid-from date without a code release. | CAP-P7-007 | REQ-DRI-010 | REQ-DRI-010 | Must | 1 |
| FR-P7-035 | The service SHALL report the rule changes of a period — version, author, approver, valid-from date, rollback and reason — with the overrides of the same period. | CAP-P7-017 | REQ-APD-005, REQ-DRI-011 | REQ-DRI-011 | Should | 4 |
| FR-P7-036 | The service SHALL require a retention class per decision record class and per ledger entry class, SHALL refuse a retention row that carries no class, and SHALL run no archive of its own. | CAP-P7-018 | NFR-030 | REQ-DRI-002 | Should | 1 |

# 7. Non-functional requirements

Targets are copied from the Non Functional Specification v3 and the BRDs. A target marked open is carried as an open question, never as a value.

| NFR ID | Requirement | Target | BR | Priority | Test |
|---|---|---|---|---|---|
| NFR-P7-001 | A screen or read served by this service answers inside the user's wait under the busiest-hour load. | Under 2 seconds at the 95th percentile | NFR-008 | Must | Performance test in SIT at the stated volume |
| NFR-P7-002 | The ledger holds one entry for every decision across the full retention period without degrading query time, and one case history reads inside the user wait at the 2031 size. | About 36 GB for the decision log and the interaction ledger by the end of 2031; a single case history under 2 seconds | NFR-007 | Must | Volume test at the 2031 size |
| NFR-P7-003 | The rule model this service publishes is evaluated inside the user's wait in the owning service, in an activity, under the recorded model version. | Under 300 milliseconds per rule evaluation at the 95th percentile; 283,000 to 318,000 evaluations a month | NFR-011 | Must | Load test through one owning service with the published model |
| NFR-P7-004 | The service is available during business hours and outside them, when approvals and the nightly jobs run. | 99.9 percent in business hours; 99.5 percent outside business hours excluding the change window | NFR-020, NFR-021 | Must | Availability read monthly from monitoring |
| NFR-P7-005 | The service inherits the ACE recovery point and recovery time. | The ACE recovery point objective and recovery time objective (open: DL11) | NFR-022, NFR-023 | Must | Failover and restore test before the first release |
| NFR-P7-006 | A failing interface, job or consumer raises an alert to a named owner role. | Within 15 minutes | NFR-068 | Must | Alert drill on the ingest, the chain check and the promotion |
| NFR-P7-007 | A REST call is one hop with a 2 s timeout; a failure is retried and, after three retries, moves to an exception queue with a task for a named owner; an event that cannot be processed goes to the dead-letter topic and is replayed. | One hop; 2 s timeout; three retries then the exception queue | NFR-025, NFR-026 | Must | Failure injection on the ingest and the approval call |
| NFR-P7-008 | A production release rolls back by redeploying the previous tag, and each service carries its own migration sequence in its own schema. | Rollback by previous tag; per-service migration | NFR-027 | Must | Rollback rehearsal |
| NFR-P7-009 | Every decision is reproducible from the ledger, including the rule, model, agent and prompt versions and the inputs used. | Every decision reproducible | NFR-033 | Must | Reproduce a sampled decision from the ledger alone |
| NFR-P7-010 | Every action carries the rule version applied and the approver who allowed it. | Every action | NFR-034 | Must | Record inspection across a sample of decisions |
| NFR-P7-011 | The chain is checked every business date and a break is reported the same day. | Daily check; same-day report | NFR-035 | Must | Seeded break drill |
| NFR-P7-012 | An audit or regulatory request is answered inside its deadline with the decision history and its supporting documents. | Inside the deadline set by the requester; population query inside the user wait | NFR-036 | Must | Population query against a synthetic population |
| NFR-P7-013 | Personal data is returned masked by role on every read of the ledger and of an approval, and each consumer receives only the personal data it needs. | Masked by default; data minimisation per consumer | NFR-039, NFR-040 | Must | Masking matrix test across roles |
| NFR-P7-014 | Every read of a personal field in the ledger or an approval is logged. | 100 percent of personal field reads | NFR-042 | Must | Access log reconciliation against reads |
| NFR-P7-015 | Data is encrypted at rest and in transit, and secrets live in the key store. | Encrypted; no secret in code, configuration or prompt | NFR-052, NFR-053 | Must | Security review and secret scan |
| NFR-P7-016 | Staff authenticate with single sign-on and multi-factor authentication; non-human callers use their own service identity. | Entra ID single sign-on with multi-factor; service identities | NFR-049, NFR-051 | Must | Sign-in and identity test |
| NFR-P7-017 | The build blocks a change carrying a secret, personal data in code, tests or logs, an unapproved dependency, a cross-schema read or a write outside `rwb_decision`. | Pipeline checks pass | NFR-054 | Must | Pipeline run with a seeded violation |
| NFR-P7-018 | Workbench data stays in the bank's own cloud tenancy in the agreed region, and every entity carries a data classification that sets its handling. | SCB Azure, Southeast Asia; classification applied per entity | NFR-046, NFR-047 | Must | Tenancy and classification review |
| NFR-P7-019 | Labels, validation messages and error messages served with this service's operations are available in Thai and in English. | Every label and message in Thai and English | NFR-059 | Must | Label and message review |
| NFR-P7-020 | Logs, traces and metrics are produced for the ingest, the approval, the chain check and the promotion, and every scheduled job has a run book, monitoring and an alert to the operations channel. | Every job covered | NFR-064, NFR-067 | Must | Observability review and a job failure drill |
| NFR-P7-021 | Business measures per decision are produced from the ledger, not from a separate count. | From the ledger | NFR-065 | Must | Compare a measure against a ledger count |
| NFR-P7-022 | An agent or model outage falls back to the rule result and the case still routes, and the fallback is visible on the decision record. | Fallback always on | NFR-024 | Must | Agent outage drill |

# 8. Data requirements

## 8.1 Entities owned by the service

Schema `rwb_decision`. Every table carries the seven standard record columns of the platform library. Retention is stated by class; the periods are open (GAP-1618; ASM-2754).

| Entity | Kind | Key fields | Classification | Source | Retention |
|---|---|---|---|---|---|
| `decision_log_entry` | Append-only ledger | `id`, `chain_seq`, `case_id`, `decision_code`, `rule_id`, `rule_version`, `model_version`, `agent_version`, `inputs_ref`, `recommendation`, `approver_user_id`, `approval_level`, `final_call`, `override_reason`, `actions`, `outcome`, `decided_at`, `prev_hash`, `entry_hash`, `corrects_entry_id`, `actor_user_id`, `idempotency_key` | [CONFIDENTIAL]; approver, actor and override fields [PII]; recommendation and terms [SENSITIVE_FINANCIAL] | DecisionRecorded from the 19 services; approvals decided here | Decision-log retention class, set by Compliance (open: NFR-030; GAP-1618) |
| `approval` | Transaction | `id`, `case_id`, `decision_code`, `regulation_item`, `capability_area`, `route_role_code`, `approval_level`, `delegation_limit_id`, `limit_version`, `product_group`, `amount`, `terms`, `prepared_by`, `assigned_user_id`, `status`, `due_at`, `escalation_level`, `source_type`, `source_ref`, `rule_id`, `rule_version`, `decision_log_id` | [PII]; `amount` and `terms` [SENSITIVE_FINANCIAL] | Prepared decisions from the owning services | Workbench record class |
| `rule_package` | Versioned reference | `package_code`, package name, owning service, rule format, description | [CONFIDENTIAL] | Rule authoring | Versioned; superseded versions kept |
| `rule_package_version` | Versioned reference | `package_code`, version label, workbook, generated DRL, checksum, state, valid from, author, approver, test result, loaded at, approved at | [CONFIDENTIAL] | Rule authoring and approval | Versioned; every version kept |
| `rule_row` | Versioned reference | `package_code`, `rule_id`, row order, salience, activation group, parsed condition and action | [CONFIDENTIAL] | Parsed from the package workbook | Versioned with its package version |
| `rule_test_case` | Versioned reference | `package_code`, version label, scenario code, expected answer, actual answer, pass flag | [CONFIDENTIAL] | Rule authoring | Versioned with its package version |
| `ledger_seal` | Evidence | `business_date`, last `chain_seq`, last `entry_hash`, fingerprint, stored location, sealed at | [CONFIDENTIAL] | This service | Kept with the decision log |

Not carried: no interaction ledger table (moved to `rwb_source_data`, GAP-1612; ASM-2748), no data-lake watermark or lake copy (removed, GAP-1613; ASM-2749), no notice, template or proof-of-delivery table (moved to rwb-comms, GAP-1614; ASM-2750).

## 8.2 Data read but not owned

Read through contracts only; this service reads no other service's tables (DP-01).

| Source | Data | How it is read | Classification of the data read |
|---|---|---|---|
| All 19 services | Decision records on `rwb.decision-record.v1` (EV-08) | Kafka, CloudEvents, inbox, once per idempotency key | [CONFIDENTIAL]; case and actor fields [PII] |
| P4 rwb-access | Delegation of authority row and its version; role, capability area and masking policy | REST, cached | [CONFIDENTIAL]; limits and amounts [SENSITIVE_FINANCIAL] |
| P3 rwb-case | Case, case state, case queue and the case reference an entry points at | REST | [PII] |
| P1 rwb-source-data | Data product, business date, load time and status behind each input (DP01 to DP14) | REST | [CONFIDENTIAL] |
| P6 rwb-comms | NoticeGenerated (EV-13) and the notice and template version awaiting approval | Kafka and REST | [PII] |
| P10 rwb-agent | AgentRunCompleted (EV-28) with the agent/prompt version and confidence | Kafka | [CONFIDENTIAL] |
| P5 rwb-document | Document references behind an approval, for the population query | REST | [PII] |
| Immutable (WORM) storage | The daily seal, written only | Object write | [CONFIDENTIAL] |

## 8.3 Field-level requirements for personal and financial data

| Field | Meaning | Classification | Requirement |
|---|---|---|---|
| `decision_log_entry.approver_user_id`, `actor_user_id` | Who approved and who acted | [PII] | Returned only to roles that hold read on the decision log; masked in an export where the masking row does not allow it |
| `decision_log_entry.override_reason` | Why the recommendation was not followed | [PII] (free text that may name a person) | Returned by role; never carried in an event |
| `decision_log_entry.inputs_ref` | Reference to the inputs snapshot, held by the owning service | [CONFIDENTIAL] | A reference only: no personal or financial value is copied into the ledger |
| `decision_log_entry.recommendation` | Option, reasons, confidence and alternatives | [SENSITIVE_FINANCIAL] | Read by role; no financial value in a published event |
| `approval.prepared_by`, `assigned_user_id` | Preparer and holder | [PII] | The preparer is shown to the holder so the four-eyes rule can be applied |
| `approval.amount`, `terms` | Amount and terms awaiting approval | [SENSITIVE_FINANCIAL] | Read by role; the queue shows the amount to the holder and the level |
| `approval.regulation_item`, `limit_version` | The regulation item and the limit version applied | [CONFIDENTIAL] | Shown with the item and written to the ledger entry |

## 8.4 Data rules

1. A value a business person may change is a versioned data row read at run time, never a constant in code (BR-P7-001 to BR-P7-035).
2. The ledger is append only and hash chained; a correction is a new entry, never an edit (REQ-DRI-002).
3. A link to a case or to another service's record is a business-key value with no foreign key and no cross-schema constraint.
4. No personal or financial value is carried in an event; the entry holds the reference and the owning service holds the snapshot.
5. The ledger holds no copy of a case, a document or a customer record; it holds identifiers, versions, the final call and references.

# 9. Integration points

Paths and call types are the confirmed v5 constraints. Nothing here is a design decision of this document.

| System or consumer | Direction | Protocol and call | Owner | Notes |
|---|---|---|---|---|
| All 19 services | In | Kafka, CloudEvents, topic `rwb.decision-record.v1`, EV-08 DecisionRecorded, inbox with idempotency key | P7 for the topic and the ledger | The only path into the ledger; each service writes its own record first, in its own schema |
| rwb-case (P3) | In and out | REST and Temporal | P3 | Case facts, the Waiting approval state on ApprovalRequested, and the case timeline that reads the P1 ledger |
| rwb-access (P4) | In | REST, cached: authorise, role and scope, masking policy, DoA limits | P4 | The DoA table and its versions belong to P4 (GAP-1616; ASM-2752) |
| rwb-comms (P6) | In | Kafka, EV-13 NoticeGenerated | P6 | Starts the D7.1 notice approval; notice generation itself is P6's |
| rwb-agent (P10) | In | Kafka, EV-28 AgentRunCompleted | P10 | The agent and prompt version that wrote the entry |
| rwb-source-data (P1) | In | REST | P1 | Data product freshness for the inputs snapshot; the interaction ledger and its timeline |
| rwb-document (P5) | In and out | REST | P5 | Document references behind an approval |
| rwb-valuation, rwb-treatment, rwb-litigation, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-payment, rwb-deviation | In and out | REST, Temporal and Kafka | The owning service | `GET /rule-models/{packageCode}/{version}` with its checksum; RulePackageInForce (EV-30); the strict-mode acknowledgement; ApprovalWorkflow as a child of the stage workflow |
| gateway-bff | In | REST composite route, one hop, 2 s timeout | Platform edge | The approval queue (SCR-10), the decision screen (SCR-11), the committee pack (SCR-12) and the decision log query (SCR-38) (GAP-1621; ASM-2759) |
| Kafka topic `rwb.decision.events.v1` | Out | CloudEvents 1.0, AsyncAPI contract, retry and dead-letter topics | P7 | ApprovalRequested (EV-09), ApprovalDecided (Arch v5 slide 14) and RulePackageInForce (EV-30) |
| rwb-reporting (P9) | Out | Kafka and REST | P9 | Consumes DecisionRecorded for its read model and reads the population query for regulatory evidence |
| Immutable (WORM) storage | Out | Object write, daily | SCB IT infrastructure | The sealed ledger fingerprint of the business date |
| Data lake and Power BI (INT-19, INT-20) | Removed | None | None | Removed in v5; no extract leaves this service (GAP-1613; ASM-2749) |
| WIN (letters, notices and proof of delivery) | Removed from this service | None | P6 rwb-comms with P2 rwb-integration | Notice generation and delivery are not this service's paths (GAP-1614; ASM-2750) |

## 9.1 Integration questions

| Question | Owner role | Why it blocks |
|---|---|---|
| What is the completeness target for the ledger, and what threshold raises the gap alert? Architecture v5 states five minutes; the BRD and the FSD state no numeric threshold. | Solution architect with the platform administrator | Sets the ingest SLO, the alert and the strict-mode wait bound (GAP-1617; ASM-2753) |
| Who owns the approval task and the "Waiting approval" case state — this service or rwb-case? | Solution architect with the rwb-case contract owner | Decides whether ApprovalRequested moves the case or whether P3 owns the transition (GAP-1623; ASM-2756) |
| Does the decision record on `rwb.decision-record.v1` carry a schema version, and who owns its evolution across 19 producers? | Platform event library owner | Decides whether the ledger can accept a new field without a coordinated release (GAP-1622; ASM-2755) |
| Which screens does this service build and which does gateway-bff compose from its contracts? | Solution architect with the platform edge owner | Sets the screen scope of the wave 2 slice (GAP-1621; ASM-2759) |

# 10. Release slicing proposal

The service is wave 1: it is created with Epic 1 (release 30 November 2026 (tentative)). Each slice is a list of capabilities, not stories. Where a business epic sits in a later wave than the service, the story keeps the business-epic wave (R5.6).

## 10.1 Wave 0 — platform prerequisites (no product capability of its own)

The service consumes platform contracts before its own work starts: the service template and repositories, the shared libraries including the outbox and inbox library and the decision-record library (RWB-PLT-E1027-CON), the Temporal workflow kit including ApprovalWorkflow and Schedules, the schema and login provision in `rwb_decision`, the Kafka event platform and naming library, the edge and gateway route, immutable (WORM) storage, and observability. These belong to the platform epics and are not capabilities of this product.

## 10.2 Wave 1 — Epic 1 (release 30 November 2026 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 1.1 Ledger store | CAP-P7-001 | Nothing can be sealed until the append-only, hash-chained store and the ingest exist, and the boundary test must fail the build from the first story |
| 1.2 Local record and completeness | CAP-P7-002 | The Epic 1 promise is that every decision is written; the contract and the gap alert make it true across 19 services |
| 1.3 Chain check and WORM seal | CAP-P7-003 | The evidence that the log was not rewritten must exist from the first business date |
| 1.4 Freshness and versions on the record | CAP-P7-005, CAP-P7-006 | A record that does not say how old its inputs are, or which model spoke, cannot be relied on in an audit |
| 1.5 Rule registry | CAP-P7-007 | The registry, its test evidence and its four-eyes rule replace the hand-made database update from the first rule change |
| 1.6 Retention class | CAP-P7-018 | The class must be declared with the store; the periods stay open |

Rationale: the wave-1 slice is the smallest set that delivers the Epic 1 outcome — a decision log store — and each slice is independently demonstrable. The rule package promotion (CAP-P7-008) is not needed until Epic 2's rule packages arrive, so wave 1 is not blocked by it.

## 10.3 Wave 2 — Epic 2 (release 31 December 2026 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 2.1 Approval routing and the limit version | CAP-P7-009, CAP-P7-015 | One owner and a timer on every case is the Epic 2 theme; authority must be routed and evidenced with the limit that applied |
| 2.2 Approve, change, return, refuse, override | CAP-P7-010 | The approver's four outcomes and the override reason are the Epic 2 approval promise |
| 2.3 Queue, decision screen and notice approval | CAP-P7-012, CAP-P7-013 | SCR-10 and SCR-11 are the working surface, and D7.1 notices are the first production use |
| 2.4 Escalation | CAP-P7-011 | A timer on every case is only true if an overdue approval moves by itself |
| 2.5 Rule package in force | CAP-P7-008 | The Epic 2 rule packages need promotion at 00:01 and the local model contract with its checksum |
| 2.6 Strict mode | CAP-P7-016 | The four points of no return need the acknowledgement before the first irreversible step is built |
| 2.7 Decision history read | CAP-P7-004 | The audit request arrives with the first approved population, and the search needs the second business date of the ledger |

Rationale: Epic 2 puts one owner and a timer on every case and adds approval routing. This service supplies the routing, the decision and the evidence, and the rule packages the other services evaluate.

## 10.4 Wave 3 — Epic 4 (release 28 February 2027 (tentative))

| Slice | Capabilities | Why now |
|---|---|---|
| 3.1 Committee decision | CAP-P7-014 | SCR-12 and the committee path are first in Epic 4; the route decision already runs through ApprovalWorkflow |

Rationale: the committee pack and the committee record are needed once the route decision is approved in production; nothing in Epic 3 needs them.

## 10.5 Wave 4 — Epic 8 and later increments

| Increment | What unlocks it |
|---|---|
| Rule change and override reporting (CAP-P7-017) | The Epic 8 governance report (RWB-E2-041, RWB-E8-013) and the monthly override review |
| Population query at the full audit scope (CAP-P7-004 continued) | The Epic 8 hardening and the first regulatory request |
| Retention in force | Compliance sets the decision-log and ledger periods under DL26 (GAP-1618; ASM-2754) |
| DMN 1.6 decision models | The table-by-table conversion on the same runtime; XLS decision tables stay supported until then (GAP-1620; ASM-2757) |

# 11. Acceptance criteria and validation evidence

Each criterion is written GIVEN/WHEN/THEN. The evidence column points at the source acceptance criterion that proves it, so a criterion is never invented where the source has one. Every criterion is verified in SIT against synthetic data; no production data is used.

## 11.1 Acceptance criteria

| AC ID | Covers | GIVEN | WHEN | THEN | Evidence |
|---|---|---|---|---|---|
| AC-P7-001 | FR-P7-001, FR-P7-003, FR-P7-004, NFR-P7-009 | an entry with `chain_seq` 1 and final call OWNER_ASSIGNED is stored for a case, and a second entry is appended | an UPDATE and a DELETE are attempted through the service role and through the schema owner, and the chain verifier runs from 1 to 2 | all attempts are refused with "decision_log_entry is append only"; each `entry_hash` equals the SHA-256 of its canonical form; the second `prev_hash` equals the first `entry_hash` and the first is 64 zeros | AC-P7-001-01, AC-ALT-P7-001-01 |
| AC-P7-002 | FR-P7-001, FR-P7-014, NFR-P7-009 | a decision D6 on a case with rule R-UNI-14, version UNI-2026.11, an inputs reference, a recommendation, an approver, a level, actions and an outcome | the entry is read through `GET /decision-log/{entryId}` | the response holds all seven field groups plus the time decided, `prev_hash` and `entry_hash` | AC-ALT-P7-001-02 |
| AC-P7-003 | FR-P7-002, FR-P7-005 | a record with a rule ID and an empty rule version, and a record with decision code D99 | each is written | each is refused with MSG-P7-009 naming ruleVersion and decisionCode; no entry is stored and the change in the same transaction is rolled back | AC-EXC-P7-002-01, AC-EXC-P7-002-05, AC-ALT-P7-002-01 |
| AC-P7-004 | FR-P7-006 | CaseAllocated for case RW-2026-000301 with idempotency key EV-02-RW-2026-000301-20261201 has been sealed | the same event arrives again with the same key | one entry exists, the first entry's ID is returned and the repeat count is 1 | AC-EXC-P7-002-03 |
| AC-P7-005 | FR-P7-007, FR-P7-009 | the ledger consumer is unavailable | an owner assignment is attempted, and a record does not reach the ledger inside the completeness target | the action is refused with MSG-P7-003 and an incident is raised; the case owner and status are unchanged; a gap alert names the case and the service | AC-EXC-P7-002-02, AC-EXC-P7-001-01; GAP-1617; ASM-2753 |
| AC-P7-006 | FR-P7-010, NFR-P7-009 | the DP01 batch for the business date completed and the DP06 batch of an earlier date is the one in use | a decision is taken and its entry is read | the inputs snapshot lists DP01 and DP06 with their load times and status, and states the business date each was used from | AC-P7-009-01, AC-ALT-P7-009-02 |
| AC-P7-007 | FR-P7-011 | an agent contributed the recommendation with a prompt version, and a person decided | the entry is read | the agent and prompt version are on the entry, the approver is recorded separately, and the agent's write is evidenced on the same terms as a person's | AC-ALT-P7-001-02; NFR-078; Arch v5 slide 27 |
| AC-P7-008 | FR-P7-012, FR-P7-013, NFR-P7-011 | a ledger with 100 entries, one of which has an altered `prev_hash` | the chain check runs at 02:00 and the seal runs for the business date | the check reports the first broken `chain_seq`, the entry and the case, and Compliance is told the same day; the seal stores the business date, the last `chain_seq` and the last `entry_hash` in write-once storage | AC-BG-P7-001-01; Arch v5 slide 28 |
| AC-P7-009 | FR-P7-014, FR-P7-015 | a ledger with entries across four cases, three decisions and two approvers | the log is searched by case, by rule, by approver and by date range, and exported | each search returns only its matches, paged, with personal fields masked for a role without an unmasked masking row, and the export carries the same rows | AC-ALT-P7-001-02; RWB-E2-005 |
| AC-P7-010 | FR-P7-016, NFR-P7-012 | a population of 40 cases with decisions taken by rules and by people | the population query runs | every case returns its decision history with inputs, versions, approver, final call and the references of its documents, inside the user wait | RWB-E2-005; NFR-036 |
| AC-P7-011 | FR-P7-017, FR-P7-026 | a demand notice prepared by one case owner under rule R-LIT-03 version LIT-2026.12, and a limit table version DOA-2026.11 in force | the router runs for decision D7.1 | the item appears in the queue of role RW-LITOFF with its area, its due time, the delegation row ID and the limit version; it is not shown to the preparer; the case is Waiting approval | AC-P7-015-01, AC-ALT-P7-015-02 |
| AC-P7-012 | FR-P7-018 | a limit version that moves a 2,400,000.00 MORTGAGE decision from L6 to L5 from 1 January 2027, and a product group with no row at all | two approvals route, one on each side of the valid-from date, and one for the uncovered product | the January item goes to L5 with DOA-2027.01 and the earlier item keeps L6 with DOA-2026.11; the uncovered item is HELD_NO_LIMIT with an incident to RW-RISK under MSG-P7-010 and no silent approval | AC-ALT-P7-015-01, AC-EXC-P7-015-06 |
| AC-P7-013 | FR-P7-019, FR-P7-027 | an approval waiting on an L6 holder | the approver opens the queue and the decision screen | the queue lists the item with amount, level, due time and age; the screen shows the recommendation, its reasons, the inputs used and the applicable limit | AC-ALT-P7-016-02; SCR-10, SCR-11 |
| AC-P7-014 | FR-P7-020, FR-P7-021 | an approval waiting with an L6 holder | the holder approves, changes the terms within the limit, changes them above the limit, returns it with a question, and refuses it with and without a reason | each outcome is written with its final call; the change above the limit re-routes to L5 with MSG-P7-001 and records no L6 approval; a refusal without a reason is refused with MSG-GEN-001 for the reason field | AC-P7-022-01, AC-ALT-P7-022-01, AC-ALT-P7-022-02, AC-EXC-P7-015-03, AC-EXC-P7-015-04 |
| AC-P7-015 | FR-P7-022, FR-P7-035 | an approver overrides a recommendation with and without a coded reason | the override is submitted, and the month is reported | the override without a reason is refused with MSG-P7-005; the coded override is recorded and appears in the monthly report with its reason and its count | VR-P7-017-3; MSG-P7-005; RWB-E2-041 |
| AC-P7-016 | FR-P7-023, FR-P7-024 | an approval still waiting at its due time, and a level with no holder and no substitute | the service level timer breaches, and an approval routes to the empty level | the first moves to the next role with escalation level 1 and a new due time, one entry records ESCALATED and the holder is told; the second escalates at once with reason NO_HOLDER | AC-EXC-P7-015-01, AC-EXC-P7-015-05 |
| AC-P7-017 | FR-P7-025 | a committee item with its members present | the committee decision is recorded | the entry holds the members present, the decision taken, the level and the approver; the committee pack shows each member's vote | SCR-12; REQ-APD-008; GAP-1619; ASM-2758 |
| AC-P7-018 | FR-P7-028 | an approval carrying template DEMAND-MTG version 2, which is withdrawn before the decision | the approver opens the item and calls approve | the screen shows MSG-P6-003 and the notice is held; the approve call is refused with status 409 and MSG-P6-003, and no approval is recorded | AC-P7-022-01, AC-EXC-P7-022-02 |
| AC-P7-019 | FR-P7-029 | an approved decision whose next step ran in another service | the outcome is written back and the entry is read | the entry holds what was done, by which system and when, and keeps the recommendation and the final call distinct | A2.25; Arch v5 slide 27 |
| AC-P7-020 | FR-P7-030, FR-P7-031, FR-P7-032, NFR-P7-009 | an ALLOCATION package with 26 rows and 50 test cases, a package whose test cases fail, and a package that overlaps two rows | each is loaded, approved and then rolled back once | the valid load is in force from its valid-from date with "50 of 50 test cases passed"; the failing load and the overlapping load are refused with MSG-P3-027 and the version in force stays; the author cannot approve their own load; the rollback restores the earlier version and a decision taken under the later version keeps that version | AC-P7-007-01, AC-ALT-P7-007-01, AC-ALT-P7-007-02, AC-EXC-P7-007-01 to AC-EXC-P7-007-05 |
| AC-P7-021 | FR-P7-033, FR-P7-034 | an approved package version with a valid-from date of the next day, and a route parameter that is changed in reference data | the promotion runs at 00:01 and an owning service fetches the model | the version is IN_FORCE, RulePackageInForce (EV-30) is on the topic with the package, version and checksum, and the fetch returns the model with the same checksum; the parameter change takes effect from its valid-from date with no release | A2.7; EV-30; JOB-20; DP-04 |
| AC-P7-022 | FR-P7-035, FR-P7-036 | a period with three rule versions, one rollback and two overrides, and a retention row without a class | the report is produced and the retention row is loaded | the report lists each version with its author, approver, valid-from date and reason, and the overrides with their reasons; the retention row is refused and no archive runs from this service | RWB-E2-041; NFR-030; GAP-1618; ASM-2754 |

## 11.2 Requirement trace summary

| BR | Capability | Functional requirement | Non-functional requirement | Acceptance criteria |
|---|---|---|---|---|
| REQ-DRI-001 | CAP-P7-001, CAP-P7-002, CAP-P7-005, CAP-P7-006 | FR-P7-001, FR-P7-005, FR-P7-006, FR-P7-009, FR-P7-010, FR-P7-011, FR-P7-029 | NFR-P7-009, NFR-P7-010 | AC-P7-001, AC-P7-002, AC-P7-003, AC-P7-004, AC-P7-005, AC-P7-006, AC-P7-007 |
| REQ-DRI-002 | CAP-P7-001, CAP-P7-018 | FR-P7-003, FR-P7-036 | NFR-P7-009 | AC-P7-001, AC-P7-022 |
| REQ-DRI-003 | CAP-P7-003 | FR-P7-004, FR-P7-012, FR-P7-013 | NFR-P7-011 | AC-P7-001, AC-P7-008 |
| REQ-DRI-004 | CAP-P7-001 | FR-P7-002 | NFR-P7-009 | AC-P7-003 |
| REQ-DRI-005 | CAP-P7-002, CAP-P7-016 | FR-P7-007, FR-P7-008, FR-P7-009 | NFR-P7-006, NFR-P7-007 | AC-P7-005 |
| REQ-DRI-009 | Not carried (removed by D-RCV-60: no data lake; GAP-1613; ASM-2749) | None | None | None |
| REQ-DRI-010 | CAP-P7-007, CAP-P7-008 | FR-P7-030, FR-P7-031, FR-P7-033, FR-P7-034 | NFR-P7-003, NFR-P7-008, NFR-P7-017 | AC-P7-020, AC-P7-021 |
| REQ-DRI-011 | CAP-P7-007, CAP-P7-017 | FR-P7-030, FR-P7-032, FR-P7-035 | NFR-P7-009, NFR-P7-020 | AC-P7-020, AC-P7-022 |
| REQ-DRI-012 | CAP-P7-004 | FR-P7-014, FR-P7-015, FR-P7-016 | NFR-P7-001, NFR-P7-002, NFR-P7-012, NFR-P7-013, NFR-P7-014 | AC-P7-002, AC-P7-009, AC-P7-010 |
| REQ-APD-001 | CAP-P7-009 | FR-P7-017 | NFR-P7-007 | AC-P7-011 |
| REQ-APD-002 | CAP-P7-012 | FR-P7-019, FR-P7-027 | NFR-P7-001 | AC-P7-013 |
| REQ-APD-003 | CAP-P7-010 | FR-P7-020, FR-P7-021 | NFR-P7-010 | AC-P7-014 |
| REQ-APD-004 | CAP-P7-009 | FR-P7-018 | NFR-P7-007 | AC-P7-012 |
| REQ-APD-005 | CAP-P7-010, CAP-P7-017 | FR-P7-021, FR-P7-022, FR-P7-035 | NFR-P7-010 | AC-P7-014, AC-P7-015, AC-P7-022 |
| REQ-APD-006 | CAP-P7-013 | FR-P7-028 | NFR-P7-013 | AC-P7-018 |
| REQ-APD-007 | CAP-P7-011 | FR-P7-023 | NFR-P7-006 | AC-P7-016 |
| REQ-APD-008 | CAP-P7-014 | FR-P7-025 | NFR-P7-010 | AC-P7-017 |
| REQ-APD-009 | CAP-P7-009 | FR-P7-017 | NFR-P7-010 | AC-P7-011 |
| REQ-APD-010 | CAP-P7-015 | FR-P7-026 | NFR-P7-009 | AC-P7-011, AC-P7-012 |
| REQ-APD-011 | CAP-P7-011 | FR-P7-024 | NFR-P7-006 | AC-P7-016 |
| REQ-ILG-001 to REQ-ILG-014 | Not carried here: served by rwb-source-data (CAP-P1-012; GAP-1612; ASM-2748) | None | None | None |
| NFR-013 | CAP-P7-005 | FR-P7-010 | NFR-P7-009 | AC-P7-006 |
| NFR-078 | CAP-P7-006 | FR-P7-011 | NFR-P7-010 | AC-P7-007 |

BR coverage: 19 of the 34 P7 program requirements (REQ-DRI-001 to REQ-DRI-005, REQ-DRI-010 to REQ-DRI-012, REQ-APD-001 to REQ-APD-011) are covered by at least one functional requirement of this PRD. The other 15 are accounted for and not dropped: REQ-DRI-009 is removed with the data lake (GAP-1613; ASM-2749) and REQ-ILG-001 to REQ-ILG-014 are moved to rwb-source-data under the R-PREC default ruling (GAP-1612; ASM-2748). No live program requirement of this service is left without a functional requirement.

## 11.3 Validation evidence expected before approval

| Evidence | What it proves | Owner role |
|---|---|---|
| Append-only, chain and schema-refusal test output in system test | FR-P7-001 to FR-P7-006, NFR-P7-009 | Developer with the compliance and PDPA officer |
| Failed-write and completeness test with a missing record | FR-P7-007, FR-P7-009, NFR-P7-006 | Platform administrator with the QA team |
| Chain break drill and seal inspection | FR-P7-012, FR-P7-013, NFR-P7-011 | Compliance and PDPA officer with Internal audit |
| Decision history and population query test against a synthetic population | FR-P7-014 to FR-P7-016, NFR-P7-002, NFR-P7-012 | Internal audit with the QA team |
| DoA routing matrix test across levels, products and versions, including the empty level and the uncovered product | FR-P7-017, FR-P7-018, FR-P7-024, FR-P7-026 | Risk and model risk officer |
| Approval outcome test: approve, change within and above the limit, return, refuse, override | FR-P7-019 to FR-P7-022 | Business lead with the QA team |
| Escalation and notice approval test | FR-P7-023, FR-P7-028 | Team manager with the QA team |
| Rule load, refusal, four-eyes, rollback and promotion test | FR-P7-030 to FR-P7-035 | Center of excellence analyst with the risk and model risk officer |
| Performance and volume test at the 2031 size, and the 300 ms evaluation test through one owning service | NFR-P7-001, NFR-P7-002, NFR-P7-003 | QA team |
| Masking matrix and access log reconciliation | NFR-P7-013, NFR-P7-014 | Compliance and PDPA officer |

# 12. Open questions

The FSD's open questions are carried forward with their owners. Product-level questions follow. No question is answered by invention: where an answer is assumed, the assumption is named.

| ID | Question | Owner role | Needed by | Blocks | Source |
|---|---|---|---|---|---|
| OQ-P7-01 | Who owns the interaction ledger? The FSD P7 builds FEAT-ILG-01 to FEAT-ILG-10 and REQ-ILG-001 to REQ-ILG-014 here, while the ownership ruling and DP-18 give the one ledger to rwb-source-data. | Solution architect with the rwb-source-data and rwb-case contract owners | Before wave 1 system test | CAP list, §5.1, §11.2 | GAP-1612; ASM-2748; DP-18 |
| OQ-P7-02 | What replaces the daily lake copy of the decision log for reporting and model feedback now that there is no data lake? | Solution architect with the reporting and BI analyst | Before wave 2 | CAP-P7-004, CAP-P7-017 | GAP-1613; ASM-2749; REQ-DRI-009 |
| OQ-P7-03 | Who generates a notice and holds its template: rwb-comms, rwb-document or this service? This PRD leaves the whole notice pipeline outside P7 and keeps only the approval. | Business lead with Legal counsel | Before wave 2 release | CAP-P7-013 | GAP-1614; ASM-2750 |
| OQ-P7-04 | Which service publishes the rule-version operations in the API specification, and does the rule registry stay with P7? The API document marks the paths P3, the P3 and P4 technical specifications claim the tables, and the ownership ruling gives them to P7. | Solution architect with the platform contract owner | Before wave 1 release | CAP-P7-007, CAP-P7-008 | GAP-1615; ASM-2751; ASM-0069 |
| OQ-P7-05 | Who loads and approves the delegation of authority table? The FSD loads it here (AC-P7-024-01 to -02); the ownership ruling gives the table to rwb-access. | Risk and model risk officer with the rwb-access owner | Before wave 2 system test | CAP-P7-009, CAP-P7-015 | GAP-1616; ASM-2752 |
| OQ-P7-06 | What is the completeness target, and what threshold raises the gap alert? Architecture v5 states five minutes; no BRD or FSD value exists. | Solution architect with the platform administrator | Before wave 1 system test | CAP-P7-002, CAP-P7-016 | GAP-1617; ASM-2753 |
| OQ-P7-07 | How long are a decision record and a ledger entry kept, and does the WORM seal follow the same period? NFR-030 and NFR-075 are open under DL26. | Compliance and PDPA officer | Before wave 1 release | CAP-P7-003, CAP-P7-018 | GAP-1618; ASM-2754; DL26 |
| OQ-P7-08 | Which fields carry a committee's members present and their votes? REQ-APD-008 and SCR-12 need them; the field list has no member or vote. | Business lead with the center of excellence analyst | Before wave 3 | CAP-P7-014 | GAP-1619; ASM-2758 |
| OQ-P7-09 | Do rule packages stay as XLS decision tables or move to DMN 1.6? Architecture v5 proposes DMN; today's packages are XLS on the same runtime. | Center of excellence analyst with the solution architect | Before wave 2 | CAP-P7-007, CAP-P7-008 | GAP-1620; ASM-2757; ADR-012, ADR-017 |
| OQ-P7-10 | Which of SCR-10, SCR-11, SCR-12 and SCR-38 does this service build, and which does gateway-bff compose from its contracts? | Solution architect with the platform edge owner | Before wave 2 | CAP-P7-012, CAP-P7-014 | GAP-1621; ASM-2759; DP-19 |
| OQ-P7-11 | Does the decision-record event carry a schema version, and who owns its evolution across 19 producers? | Platform event library owner | Before wave 1 release | CAP-P7-001 | GAP-1622; ASM-2755 |
| OQ-P7-12 | Who moves the case to Waiting approval and owns the approval task: this service or rwb-case? | Solution architect with the rwb-case contract owner | Before wave 2 release | CAP-P7-009, CAP-P7-012 | GAP-1623; ASM-2756 |

## 12.1 Assumptions this PRD is written under

| ID | Assumption | Applied in |
|---|---|---|
| ASM-2746 | The BRDs and the FSD/TSD are treated as the approved baseline; the PRD is Draft and no approval is recorded. | Front matter; §1.1; §13 |
| ASM-2747 | Where sources disagree the Architecture v5 catalogue, the Temporal and Drools design, the Decision Log and the ownership rulings win, and the loser is a gap row. | §2.4; §5.1; §9; §12 |
| ASM-2748 | The interaction ledger is rwb-source-data's; this service owns the decision ledger only. | §2.3; §5.1; §11.2 |
| ASM-2749 | There is no data lake; the ledger is fed continuously from Kafka. | §2.3; §5.1; §9 |
| ASM-2750 | Notice generation, templates, the template catalog and proof of delivery are outside this service. | §2.3; §5.1; §9 |
| ASM-2751 | Rule governance is here and rule evaluation is in the owning service. | §2.2; §5; §6 |
| ASM-2752 | The DoA table is rwb-access's and is read at decision time with its version recorded. | §2.3; §9; §6 |
| ASM-2753 | The completeness target is read as the five minutes of Architecture v5, with the gap alert at the same threshold. | §6; §9.1; §11.1 |
| ASM-2754 | A retention class is required per class while the periods stay open. | §8.1; §10.5; §12 |
| ASM-2755 | The decision-record event is versioned by the platform event library. | §9.1; §12 |
| ASM-2756 | rwb-case sets the Waiting approval state on ApprovalRequested. | §9; §9.1; §12 |
| ASM-2757 | XLS decision tables are accepted today and DMN 1.6 is the target on the same runtime. | §5.1; §10.5; §12 |
| ASM-2758 | Committee members and votes are carried in the approval terms until the field list is agreed. | §11.1; §12 |
| ASM-2759 | Screens are composed by gateway-bff from this service's contracts. | §9; §9.1; §12 |

# 13. Approval

The approval table is deliberately empty: this version is Draft and no approval is recorded in this run. A missing approval is carried as an assumption, not as an answer (ASM-2746).

| Role | Name | Decision | Date | Notes |
|---|---|---|---|---|
| Product Owner | | | | |
| FDA | | | | |

## 13.1 Next step

Product Owner and FDA approval of this document, then the context update that adds the P7 business context and the backlog draft that turns these capabilities into stories. Nothing in this run starts a later lifecycle stage.

# Appendix A. Sources and evidence

| Source | Sections used |
|---|---|
| Recovery Workbench Business Requirements Program v4 | 5.7 (P7 requirements, REQ-DRI-001 to REQ-APD-011 and REQ-ILG-001 to REQ-ILG-014), 6.1 to 6.12 (NFR-001 to NFR-078), 7 (constraints), 8 (release plan), 9 (open decisions DL06, DL11, DL18, DL22, DL26, DL43) |
| Recovery Workbench Business Requirements Epic 1 v4 | Decision log store, decision log writer, rule version load and approval, approval routing and ledger story refs (RWB-E1-008, RWB-E1-014, RWB-E1-015, RWB-E1-027, RWB-E1-029, RWB-E1-052, RWB-E1-066 to RWB-E1-068) |
| Recovery Workbench Business Requirements Epic 2 v2 | REQ-DRI-012; REQ-APD-001 to REQ-APD-011; RWB-E2-005, RWB-E2-013, RWB-E2-014, RWB-E2-041 |
| Recovery Workbench FSD P7 Decision center and log v3 | Document control, existing capability check, A1.1 to A1.4, A2.1 to A2.35, Requirements served, Screens, Appendix A and B |
| Recovery Workbench TSD P7 Decision center and log v2 | T3.0 to T3.3 (field lists, lists of values, relationships), T6.1 and T6.2 (roles and authorisation), T7 (targets), appendix T-A (API-P7-001 to API-P7-008) |
| Recovery Workbench Architecture v5 | Slides 14 (P7 contract block), 20 (ledger), 26 and 28 (strict mode and the local record plus central seal), 27 (rule governance), 41 (service catalogue row P7), 42 and 43 (event catalogue EV-08, EV-09, EV-13, EV-28, EV-30), 44 (job map JOB-13, JOB-14, JOB-20), 45 (architect questions) |
| Recovery Workbench Temporal and Drools Design v1 | Rule governance block, JOB-20 promotion, EV-30 and cache refresh, checksum and atomic swap, ApprovalWorkflow, strict mode at the four points of no return |
| Recovery Workbench Microservice Ownership Map v1 | P7 tables (approval, decision_log_entry, rule_package, rule_package_version, rule_row, rule_test_case), events EV-08, EV-09 and EV-30, jobs JOB-13, JOB-14 and JOB-20, ApprovalWorkflow, and the rulings that move the interaction ledger, the DoA table and the notice pipeline |
| Recovery Workbench Non Functional Specification v3 | 1 (targets on one page), 2 (volumes and concurrency), 3.1 to 3.12 (requirements by quality characteristic) |
| Recovery Workbench Microservice Story Template and Rules v1 | R1, R3, R5 (R5.5 DP table, R5.6 wave map), R8.1, R8.2, R9 |
