SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench P7 Decision center and log

**Change log.** D-RCV-60, 26 November 2026: cross-document changes under the programme directive. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Functional specification. SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD P7 Decision center and log |
| Document ID | P7-RWB-FSD-v4 |
| Service | `rwb-decision` (Decision and rules) |
| Version | 4 |
| Status | Draft |
| Classification | Confidential |
| Date | 15 November 2026 |
| Change note | v3, 15 November 2026: re-based on the ACE database under D-RCV-35 (ADR-010). Source data is read only through `recovery.v_ace_*` views and lands through ACE ingestion; no inbound load, load run or data quality exception in the Workbench. Proof of delivery reads `v_ace_pod` (INT-15 and JOB-09 removed); EFS interactions read `v_ace_efs_action`; JOB-01 restart example moved to JOB-02; freshness from `v_ace_batch_status`. Everything else unchanged from v2. |
| FSD owner | Business analyst, P7 |
| Business owner | Business lead |
| Change | 4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

| Module code | Module name | First in |
|---|---|---|
| P7 | Decision center and log | E1 log; E2 routing; E3 center |

**Feature scope.** Recommendation with reasons, approval within delegation, decision log store and writer.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification P7 Decision center and log | TSD | Pair |
| Recovery Workbench User Stories Epic 1 and Epic 2 | Backlog | Traceability |

### Note, Architecture v5 (D-RCV-60)

| Item | Value |
|---|---|
| Service | `rwb-decision` (Decision and rules) |
| Owns in Architecture v5 | approvals, central decision ledger, DMN model registry |
| Service epic | `RWB-SVC-P7` |
| Wave | 1 |
| Schema | `rwb_decision` |
| REST base | `/api/recovery/decision/v1` |
| Kafka topic | `rwb.decision.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.decision.<Event>.v1` |
| Temporal task queue | `rwb-decision` |
| Java package | `th.co.scb.ace.workbench.recovery.decision` |

Version 4 adds the Service row, the Change row and this note above; nothing else in this document changes. Under Architecture v5 the module is delivered as the service `rwb-decision` of the 19 services inside ACE (ADR-013), with its own schema `rwb_decision` and login (ADR-014), in wave 1, service epic `RWB-SVC-P7`; the realignment is D-RCV-60 (DL44), and DL46 keeps team-type ownership soft. The functional content of this document is the content of version 3, kept word for word: every feature, requirement, rule, field, list, message, screen, count and date.

Every owner named in this document is the owner recorded in the Microservice Ownership Map v1, and where the map carries a ruling of Template and Rules §R3 the ruling is followed: parameters and reference data with `rwb-case` (DP-06, DP-07), the rule package registry with `rwb-decision` (DP-04), the interaction ledger with `rwb-source-data` (DP-18) and feature flags with the platform library. Where this document names a table, endpoint, event, job, workflow or screen that the map gives to another service, that service owns it and this module reaches it only through the owner's contract (DP-01, DP-11; ADR-020).

The extracts, feeds and copies this document addresses to a data lake are removed by Architecture v5: reporting reads events into `rwb-reporting` (DP-17, ADR-018). The wording of those extracts is kept as written and carried by GAP-1861.

As an exception to the two paragraphs above, FEAT-DRI-06 (A2.6) with its acceptance criteria and REQ-DRI-009 are retired with story RWB-E1-014 and removed from this document (GAP-1613). The section number A2.6 is not reused. The audit path is the population query of the decision log in this service (REQ-DRI-012).

The scheduler references of this document are replaced by Temporal Schedules and event-started workflows through the workflow kit, with the task queue above (DP-10, ADR-016). The wording is kept as written and carried by GAP-1862.

Release dates stay as written and are tentative (DL48). No approval of version 4 is recorded (ASM-3046); the version is Draft.

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit and PII logging | REUSE | ACE common module | No build in this module |
| Case record and shared entities | REUSE | ACE common module; Case and Workflow Model | Read through the P3 interfaces |
| Notification path | REUSE | ACE notification path | Recovery templates only |
| Workflow and state machine | REUSE | Workflow Engine Design | Stages and sentries from P3 |
| Decision record and audit trail | NEW | Audit and Logging Design | Decision log store and writer |
| Attachments and evidence | REUSE | Document Management Design | Through P5 |
| Role and permission matrix | REUSE | Users Roles and Permissions | Capability areas from P4 |
| Restructure calculator | REUSE | ACE common module | Not used |

## A1. Context and scope

### A1.1 Scope of work and deliverables

**In scope.** Recommendation with reasons, approval within delegation, decision log store and writer.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-ACA-06; FEAT-APD-01; FEAT-APD-01, FEAT-DRI-14; FEAT-APD-02; FEAT-CWC-13; FEAT-CWC-23; FEAT-DRI-01; FEAT-DRI-02

**Constraints.** Built in the ACE service as part of the recovery module; source data read only from the ACE database through the SELECT-only `recovery.v_ace_*` views, landed by ACE's own ingestion, with no inbound load in the Workbench (D-RCV-35); every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| P7 | FEAT-DRI-01 | Store decision log entries append-only and hash-chained | System | Holds every decision entry in a store that cannot be altered, with each record hashed to the one before it. | E1 | A2.1 |
| P7 | FEAT-DRI-02 | Write a decision log entry for every decision | System | Writes one entry for every decision the Workbench or a person takes, with no exception. | E1 | A2.2 |
| P7 | FEAT-DRI-03 | Record the rule ID, rule version and inputs on each entry | System | Captures which rule fired, which version was in force and the inputs it read, so a decision is reproducible. | E1 | A2.3 |
| P7 | FEAT-DRI-04 | Record the approver and the limit applied | System | Captures who approved, under which delegated limit, and any override reason. | E1 | A2.4 |
| P7 | FEAT-DRI-05 | Block an action when the decision log write fails | System | Stops the action and raises an incident when the log entry cannot be written. No action proceeds unlogged. | E1 | A2.5 |
| P7 | FEAT-DRI-07 | Run the rules component on versioned rule tables | System | Evaluates allocation, assignment, transfer, routing and approval rules from the versioned tables. | E1 | A2.7 |
| P7 | FEAT-DRI-08 | Expose the decision service to the workflow | System | Gives the workflow one call for a recommendation, which runs the rules and returns the result with its reasons. | E1 | A2.8 |
| P7 | FEAT-DRI-12 | Carry a freshness stamp on every decision input | System | Attaches the age of each input to the decision, so a decision taken on stale data is visible. | E1 | A2.9 |
| P7 | FEAT-DRI-14 | Generate notices from approved templates to WIN | System | Produces demand, recall and guarantor notices from Legal-approved templates and sends them to WIN. | E1 | A2.10 |
| P7 | FEAT-DRI-15 | Manage letter templates with Legal approval | Admin | Holds every letter and notice template with its version and the Legal approval that put it in force. | E1 | A2.11 |
| P7 | FEAT-DRI-16 | Hold the template catalog with merge fields | Admin | Keeps the catalog of templates and the merge fields each one draws from the case. | E1 | A2.12 |
| P7 | FEAT-DRI-17 | Capture proof of delivery from WIN | System | Takes the delivery confirmation back from WIN and records it against the notice on the case. | E1 | A2.13 |
| P7 | FEAT-DRI-18 | Run run books and monitoring for every job | Admin | Gives every scheduled job a run book, an alert and an owner, so a failed job is noticed the same day. | E1 | A2.14 |
| P7 | FEAT-APD-01 | Route a recommendation to the approver by limit | System | Reads the delegation of authority table and sends the recommendation to the role that can approve it. | E2 | A2.15 |
| P7 | FEAT-APD-02 | Approve inside the limit | User | Lets the approver accept the recommendation, which books the decision and starts the next step. | E2 | A2.16 |
| P7 | FEAT-APD-03 | Change a recommendation before approving | User | Lets the approver change the terms within their limit, and records what changed and why. | E2 | A2.17 |
| P7 | FEAT-APD-04 | Reject a recommendation with a reason | User | Lets the approver reject, with a coded reason that returns the case to the point the rule names. | E2 | A2.18 |
| P7 | FEAT-APD-05 | Escalate above the limit | System | Sends a recommendation beyond the approver's limit to the next role in the matrix. | E2 | A2.19 |
| P7 | FEAT-APD-06 | Escalate an overdue approval | System | Raises an approval that has passed its service level to the named escalation point. | E2 | A2.20 |
| P7 | FEAT-APD-07 | Record an override with a coded reason | User | Lets an authorized user take a different route from the recommendation, with the reason recorded on the decision. | E2 | A2.21 |
| P7 | FEAT-APD-08 | Approve demand and recall notices | User | Gives the first production use of approval routing: the D7.1 demand and recall notices. | E2 | A2.22 |
| P7 | FEAT-APD-09 | Show the approval queue | User | Gives each approver one queue of what is waiting on them, with the limit and the age of each item. | E2 | A2.23 |
| P7 | FEAT-APD-10 | Apply the delegation of authority limits | System | Reads the limits from the versioned table at the moment of the decision, and records the version used. | E2 | A2.24 |
| P7 | FEAT-APD-11 | Record the outcome of an approved decision | System | Writes the result of the decision back to the log: what was done, by which system, and when. | E2 | A2.25 |
| P7 | FEAT-ILG-01 | Write every Workbench event to the ledger | System | Captures case created, allocated, transferred, escalated, document attached and decision taken as ledger entries as they happen. | E1 | A2.26 |
| P7 | FEAT-ILG-02 | Hold the ledger beside the decision log | System | An append-only store sharing infrastructure with the decision log, with its own retention. The decision log says why the system acted; the ledger says what happened with the customer. | E1 | A2.27 |
| P7 | FEAT-ILG-03 | Read the ledger in one ordered sequence | System | A read interface returning a case's entries in order with their source named, filterable by channel, actor and date range. | E1 | A2.28 |
| P7 | FEAT-ILG-04 | Reject a duplicate ledger entry | System | The same event arriving twice with the same key produces one entry, and the repeat is counted. | E1 | A2.29 |
| P7 | FEAT-ILG-05 | Raise an incident when the ledger cannot be written | System | A ledger write failure raises an incident rather than being discarded, so the history never has a silent gap. | E1 | A2.30 |
| P7 | FEAT-ILG-06 | Bring contact outcomes into the ledger | System | Contact attempts and their outcomes from EFS are written to the ledger with channel, time and who was reached. | E2 | A2.31 |
| P7 | FEAT-ILG-07 | Bring dispatch outcomes into the ledger | System | Letter, SMS and LINE dispatch, and proof of delivery, are written to the ledger. | E2 | A2.32 |
| P7 | FEAT-ILG-08 | Record a hand-over in the ledger | System | A case moving between owners or out to a partner records who had it, who has it now and when. | E2 | A2.33 |
| P7 | FEAT-ILG-09 | Read the ledger as a timeline on the case | User | The case record shows the ledger as an ordered history the case owner reads before deciding anything. | E2 | A2.34 |
| P7 | FEAT-ILG-10 | Set the retention class for ledger entries | Admin | Ledger retention is set independently of the decision log, as reference data. | E2 | A2.35 |

### A1.3 Background

Why a route was chosen, who approved it and on what figures is spread across emails and files.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Store decision log entries append-only and hash-chained

#### A2.1.1 Intent

**Business objective.** Holds every decision entry in a store that cannot be altered, with each record hashed to the one before it.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Holds every decision entry in a store that cannot be altered, with each record hashed to the one before it.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Store decision log entries append-only and hash-chained | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database, PostgreSQL

**Prerequisites.** None

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-001-1 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-001-2 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| VR-P7-001-3 | A decision input is past its age limit | MSG-P7-006 {input} is {days} days old, past its limit. Refresh it before you decide. |
| BR-P7-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Internal audit, Compliance and PDPA officer | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-001-01 | Append only | an entry with chain_seq 1 and final call "OWNER_ASSIGNED" is stored for case "RW-2026-000123" | an UPDATE setting final_call to "CASE_TRANSFERRED" and a DELETE of the entry are attempted through the ACE service's database role and again through the schema owner role | all four statements are refused: by the missing grant for the service role, and with "decision_log_entry is append only" from tr_declog_append_only for the schema owner And the entry is unchanged And the refused attempts are written to the ACE audit log with the table, the operation and the entry ID | RWB-E1-008 |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-001-01 | Hash chain | 100 entries are appended | the chain verifier runs from chain_seq 1 to 100 | every entry_hash equals the SHA-256 of the entry's canonical form And every prev_hash equals the entry_hash of the entry before it, and the first prev_hash is 64 zeros And the result holds count 100, last chain_seq 100 and that entry's entry_hash | RWB-E1-008 |
| AC-ALT-P7-001-02 | Seven field groups | an entry is appended for decision "D6" on case "RW-2026-000123" with rule "R-UNI-14", rule version "UNI-2026.11", inputs reference "inputs/2026-12-03/7f3a", recommendation, approver "U-6101", approval level "L6", final call "APPROVED", actions and outcome | it is read with GET /decision-log/{entryId} | the response holds inputsRef, ruleId and ruleVersion, recommendation, approverUserId and approvalLevel, finalCall, actions and outcome And decidedAt, prevHash and entryHash are present | RWB-E1-008 |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-001-01 | A failed append leaves nothing behind | the database connection for the store is closed in the test double | a writer appends an entry inside a transaction that also changes the case owner | DecisionLogUnavailableException is raised And no entry is stored, the case owner is unchanged and chain_seq is not used | RWB-E1-008 |
| AC-EXC-P7-001-02 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-001-03 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-001-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.2 Write a decision log entry for every decision

#### A2.2.1 Intent

**Business objective.** Writes one entry for every decision the Workbench or a person takes, with no exception.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Writes one entry for every decision the Workbench or a person takes, with no exception.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Write a decision log entry for every decision | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-DRI-01

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-002-1 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-002-2 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| VR-P7-002-3 | A decision input is past its age limit | MSG-P7-006 {input} is {days} days old, past its limit. Refresh it before you decide. |
| BR-P7-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Internal audit | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-002-01 | Record per event | case "RW-2026-000123" is created by JOB-02 and given owner "U-7101" by row "ALLOC-MTG-BKK-01" of "ALLOC-2026.11" in JOB-03 | the two events are written | two entries exist for the case with final calls "CASE_CREATED" and "OWNER_ASSIGNED" And the second entry carries rule ID "ALLOC-MTG-BKK-01", rule version "ALLOC-2026.11", actor "SY-CASEWF" and an inputs reference And both entries pass the schema check and two DecisionRecorded events are in the outbox | RWB-E1-027 |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-002-01 | Schema enforced | a record for case "RW-2026-000123" with final call "CASE_TRANSFERRED" and no rule version, model version or agent version | it is written | it is refused with message MSG-P7-009 naming "versions" And the writer logs the error with the case ID and the missing field And the transfer in the same transaction is rolled back | RWB-E1-027 |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-002-01 | A rule ID with no rule version is refused | a record with rule ID "R-UNI-14" and an empty rule version | it is written | it is refused with message MSG-P7-009 naming "ruleVersion" | RWB-E1-027 |
| AC-EXC-P7-002-02 | A failed write stops the action | the decision log store is unavailable | JOB-03 gives case "RW-2026-000124" to owner "U-7102" | the write raises DecisionLogUnavailableException And the case owner stays empty and the case status stays "New" And an incident is raised to the platform administrator queue | RWB-E1-027 |
| AC-EXC-P7-002-03 | A repeated event gives one entry | event "EV-7f3a-0001" for document "DOC-2026-0009981" attached to case "RW-2026-000123" was written | the same event with idempotency key "EV-7f3a-0001" arrives again | one entry exists for the event And the writer returns the first entry's ID and adds 1 to the repeat count for R-UNI-40 | RWB-E1-027 |
| AC-EXC-P7-002-04 | A write outside a transaction is refused | a caller without an open transaction | it calls the writer | the call is refused with IllegalTransactionStateException and nothing is written | RWB-E1-027 |
| AC-EXC-P7-002-05 | An unknown decision code is refused | a record with decision code "D99" | it is written | it is refused with message MSG-P7-009 naming "decisionCode" | RWB-E1-027 |
| AC-EXC-P7-002-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-002-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-002-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.3 Record the rule ID, rule version and inputs on each entry

#### A2.3.1 Intent

**Business objective.** Captures which rule fired, which version was in force and the inputs it read, so a decision is reproducible.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Captures which rule fired, which version was in force and the inputs it read, so a decision is reproducible.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Record the rule ID, rule version and inputs on each entry | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-DRI-02

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-003-1 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-003-2 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| VR-P7-003-3 | A decision input is past its age limit | MSG-P7-006 {input} is {days} days old, past its limit. Refresh it before you decide. |
| BR-P7-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Internal audit, Center of excellence analyst | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-003-01 | Record per event | case "RW-2026-000123" is created by JOB-02 and given owner "U-7101" by row "ALLOC-MTG-BKK-01" of "ALLOC-2026.11" in JOB-03 | the two events are written | two entries exist for the case with final calls "CASE_CREATED" and "OWNER_ASSIGNED" And the second entry carries rule ID "ALLOC-MTG-BKK-01", rule version "ALLOC-2026.11", actor "SY-CASEWF" and an inputs reference And both entries pass the schema check and two DecisionRecorded events are in the outbox | RWB-E1-027 |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-003-01 | Schema enforced | a record for case "RW-2026-000123" with final call "CASE_TRANSFERRED" and no rule version, model version or agent version | it is written | it is refused with message MSG-P7-009 naming "versions" And the writer logs the error with the case ID and the missing field And the transfer in the same transaction is rolled back | RWB-E1-027 |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-003-01 | A rule ID with no rule version is refused | a record with rule ID "R-UNI-14" and an empty rule version | it is written | it is refused with message MSG-P7-009 naming "ruleVersion" | RWB-E1-027 |
| AC-EXC-P7-003-02 | A failed write stops the action | the decision log store is unavailable | JOB-03 gives case "RW-2026-000124" to owner "U-7102" | the write raises DecisionLogUnavailableException And the case owner stays empty and the case status stays "New" And an incident is raised to the platform administrator queue | RWB-E1-027 |
| AC-EXC-P7-003-03 | A repeated event gives one entry | event "EV-7f3a-0001" for document "DOC-2026-0009981" attached to case "RW-2026-000123" was written | the same event with idempotency key "EV-7f3a-0001" arrives again | one entry exists for the event And the writer returns the first entry's ID and adds 1 to the repeat count for R-UNI-40 | RWB-E1-027 |
| AC-EXC-P7-003-04 | A write outside a transaction is refused | a caller without an open transaction | it calls the writer | the call is refused with IllegalTransactionStateException and nothing is written | RWB-E1-027 |
| AC-EXC-P7-003-05 | An unknown decision code is refused | a record with decision code "D99" | it is written | it is refused with message MSG-P7-009 naming "decisionCode" | RWB-E1-027 |
| AC-EXC-P7-003-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-003-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-003-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.4 Record the approver and the limit applied

#### A2.4.1 Intent

**Business objective.** Captures who approved, under which delegated limit, and any override reason.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Captures who approved, under which delegated limit, and any override reason.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Record the approver and the limit applied | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-DRI-02

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-004-1 | Approval above the approver's limit | MSG-P7-001 This needs approval at level {level}. It has been sent to {approver}. |
| VR-P7-004-2 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-004-3 | Override without a reason | MSG-P7-005 Enter the reason you are not following the recommendation. |
| BR-P7-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Internal audit | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-004-01 | Record per event | case "RW-2026-000123" is created by JOB-02 and given owner "U-7101" by row "ALLOC-MTG-BKK-01" of "ALLOC-2026.11" in JOB-03 | the two events are written | two entries exist for the case with final calls "CASE_CREATED" and "OWNER_ASSIGNED" And the second entry carries rule ID "ALLOC-MTG-BKK-01", rule version "ALLOC-2026.11", actor "SY-CASEWF" and an inputs reference And both entries pass the schema check and two DecisionRecorded events are in the outbox | RWB-E1-027 |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-004-01 | Schema enforced | a record for case "RW-2026-000123" with final call "CASE_TRANSFERRED" and no rule version, model version or agent version | it is written | it is refused with message MSG-P7-009 naming "versions" And the writer logs the error with the case ID and the missing field And the transfer in the same transaction is rolled back | RWB-E1-027 |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-004-01 | A rule ID with no rule version is refused | a record with rule ID "R-UNI-14" and an empty rule version | it is written | it is refused with message MSG-P7-009 naming "ruleVersion" | RWB-E1-027 |
| AC-EXC-P7-004-02 | A failed write stops the action | the decision log store is unavailable | JOB-03 gives case "RW-2026-000124" to owner "U-7102" | the write raises DecisionLogUnavailableException And the case owner stays empty and the case status stays "New" And an incident is raised to the platform administrator queue | RWB-E1-027 |
| AC-EXC-P7-004-03 | A repeated event gives one entry | event "EV-7f3a-0001" for document "DOC-2026-0009981" attached to case "RW-2026-000123" was written | the same event with idempotency key "EV-7f3a-0001" arrives again | one entry exists for the event And the writer returns the first entry's ID and adds 1 to the repeat count for R-UNI-40 | RWB-E1-027 |
| AC-EXC-P7-004-04 | A write outside a transaction is refused | a caller without an open transaction | it calls the writer | the call is refused with IllegalTransactionStateException and nothing is written | RWB-E1-027 |
| AC-EXC-P7-004-05 | An unknown decision code is refused | a record with decision code "D99" | it is written | it is refused with message MSG-P7-009 naming "decisionCode" | RWB-E1-027 |
| AC-EXC-P7-004-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-004-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-004-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.5 Block an action when the decision log write fails

#### A2.5.1 Intent

**Business objective.** Stops the action and raises an incident when the log entry cannot be written. No action proceeds unlogged.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Stops the action and raises an incident when the log entry cannot be written. No action proceeds unlogged.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Block an action when the decision log write fails | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-DRI-02

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-005-1 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-005-2 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| VR-P7-005-3 | A decision input is past its age limit | MSG-P7-006 {input} is {days} days old, past its limit. Refresh it before you decide. |
| BR-P7-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-005-01 | Record per event | case "RW-2026-000123" is created by JOB-02 and given owner "U-7101" by row "ALLOC-MTG-BKK-01" of "ALLOC-2026.11" in JOB-03 | the two events are written | two entries exist for the case with final calls "CASE_CREATED" and "OWNER_ASSIGNED" And the second entry carries rule ID "ALLOC-MTG-BKK-01", rule version "ALLOC-2026.11", actor "SY-CASEWF" and an inputs reference And both entries pass the schema check and two DecisionRecorded events are in the outbox | RWB-E1-027 |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-005-01 | Schema enforced | a record for case "RW-2026-000123" with final call "CASE_TRANSFERRED" and no rule version, model version or agent version | it is written | it is refused with message MSG-P7-009 naming "versions" And the writer logs the error with the case ID and the missing field And the transfer in the same transaction is rolled back | RWB-E1-027 |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-005-01 | A rule ID with no rule version is refused | a record with rule ID "R-UNI-14" and an empty rule version | it is written | it is refused with message MSG-P7-009 naming "ruleVersion" | RWB-E1-027 |
| AC-EXC-P7-005-02 | A failed write stops the action | the decision log store is unavailable | JOB-03 gives case "RW-2026-000124" to owner "U-7102" | the write raises DecisionLogUnavailableException And the case owner stays empty and the case status stays "New" And an incident is raised to the platform administrator queue | RWB-E1-027 |
| AC-EXC-P7-005-03 | A repeated event gives one entry | event "EV-7f3a-0001" for document "DOC-2026-0009981" attached to case "RW-2026-000123" was written | the same event with idempotency key "EV-7f3a-0001" arrives again | one entry exists for the event And the writer returns the first entry's ID and adds 1 to the repeat count for R-UNI-40 | RWB-E1-027 |
| AC-EXC-P7-005-04 | A write outside a transaction is refused | a caller without an open transaction | it calls the writer | the call is refused with IllegalTransactionStateException and nothing is written | RWB-E1-027 |
| AC-EXC-P7-005-05 | An unknown decision code is refused | a record with decision code "D99" | it is written | it is refused with message MSG-P7-009 naming "decisionCode" | RWB-E1-027 |
| AC-EXC-P7-005-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-005-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-005-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.6 Retired

Retired under Architecture v5, which has no data lake (ADR-018, DP-17; GAP-1613). The section number is kept so that later sections keep their numbers.

---

### A2.7 Run the rules component on versioned rule tables

#### A2.7.1 Intent

**Business objective.** Evaluates allocation, assignment, transfer, routing and approval rules from the versioned tables.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Evaluates allocation, assignment, transfer, routing and approval rules from the versioned tables.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the rules component on versioned rule tables | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Rules component, Workbench

**Prerequisites.** FEAT-CWC-23

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-007-1 | Approval above the approver's limit | MSG-P7-001 This needs approval at level {level}. It has been sent to {approver}. |
| BR-P7-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Center of excellence analyst | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-007-01 | Valid load | a template for table ALLOCATION version "ALLOC-2026.12" with 26 rows and 50 test cases that passes every check | U-41 loads it with valid from 2026-12-15 and U-51 approves it | version "ALLOC-2026.12" is in force from 2026-12-15 And the change log records author U-41, approver U-51, the load and approval times, "50 of 50 test cases passed" and the dry run count | RWB-E1-029 |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-007-01 | Test cases | the 50 test cases with expected queues And test cases "TA-07" and "TA-19" expect queue "MTG-BKK-CO" and the new rows return "MTG-CEN-CO" | validation runs | the load is refused with MSG-P3-027 for the test case check naming "TA-07" and "TA-19" | RWB-E1-029 |
| AC-ALT-P7-007-02 | Rollback | version 7, "ALLOC-2026.13", is in force and version 6, "ALLOC-2026.12", was in force before it | U-41 calls rollback once for version 7 | version 6 is in force And the change log holds the rollback with U-41, the time and the reason And a case allocated under version 7 keeps rule version "ALLOC-2026.13" on its decision log entry | RWB-E1-029 |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-007-01 | Overlap refused | rows "ALLOC-031" and "ALLOC-032" both match product group "MORTGAGE" and region "BKK" at row order 12 | validation runs | the load is refused with MSG-P3-027 for the overlap check naming "ALLOC-031" and "ALLOC-032" And version "ALLOC-2026.11" stays in force | RWB-E1-029 |
| AC-EXC-P7-007-02 | Schema error | row 9 has assignment reason "QUICK" that is not in its list | validation runs | the load is refused with MSG-P3-027 for the schema check naming row 9 and its column | RWB-E1-029 |
| AC-EXC-P7-007-03 | Missing default | the allocation rows have no last row that matches every case | validation runs | the load is refused with MSG-P3-027 for the default row check | RWB-E1-029 |
| AC-EXC-P7-007-04 | Author cannot approve | U-41 loaded version "ALLOC-2026.12" | U-41 calls approve | the call is refused with MSG-P7-002 And the version stays LOADED | RWB-E1-029 |
| AC-EXC-P7-007-05 | Rollback with no earlier version | table TRANSFER has only version "TRF-2026.11" | rollback is called for "TRF-2026.11" | the call is refused with MSG-P3-015 And "TRF-2026.11" stays in force | RWB-E1-029 |
| AC-EXC-P7-007-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-007-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-007-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.8 Expose the decision service to the workflow

#### A2.8.1 Intent

**Business objective.** Gives the workflow one call for a recommendation, which runs the rules and returns the result with its reasons.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Gives the workflow one call for a recommendation, which runs the rules and returns the result with its reasons.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Expose the decision service to the workflow | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Rules component

**Prerequisites.** FEAT-DRI-07

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-008-1 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-008-2 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| VR-P7-008-3 | Override without a reason | MSG-P7-005 Enter the reason you are not following the recommendation. |
| BR-P7-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-008-01 | Record per event | case "RW-2026-000123" is created by JOB-02 and given owner "U-7101" by row "ALLOC-MTG-BKK-01" of "ALLOC-2026.11" in JOB-03 | the two events are written | two entries exist for the case with final calls "CASE_CREATED" and "OWNER_ASSIGNED" And the second entry carries rule ID "ALLOC-MTG-BKK-01", rule version "ALLOC-2026.11", actor "SY-CASEWF" and an inputs reference And both entries pass the schema check and two DecisionRecorded events are in the outbox | RWB-E1-027 |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-008-01 | Schema enforced | a record for case "RW-2026-000123" with final call "CASE_TRANSFERRED" and no rule version, model version or agent version | it is written | it is refused with message MSG-P7-009 naming "versions" And the writer logs the error with the case ID and the missing field And the transfer in the same transaction is rolled back | RWB-E1-027 |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-008-01 | A rule ID with no rule version is refused | a record with rule ID "R-UNI-14" and an empty rule version | it is written | it is refused with message MSG-P7-009 naming "ruleVersion" | RWB-E1-027 |
| AC-EXC-P7-008-02 | A failed write stops the action | the decision log store is unavailable | JOB-03 gives case "RW-2026-000124" to owner "U-7102" | the write raises DecisionLogUnavailableException And the case owner stays empty and the case status stays "New" And an incident is raised to the platform administrator queue | RWB-E1-027 |
| AC-EXC-P7-008-03 | A repeated event gives one entry | event "EV-7f3a-0001" for document "DOC-2026-0009981" attached to case "RW-2026-000123" was written | the same event with idempotency key "EV-7f3a-0001" arrives again | one entry exists for the event And the writer returns the first entry's ID and adds 1 to the repeat count for R-UNI-40 | RWB-E1-027 |
| AC-EXC-P7-008-04 | A write outside a transaction is refused | a caller without an open transaction | it calls the writer | the call is refused with IllegalTransactionStateException and nothing is written | RWB-E1-027 |
| AC-EXC-P7-008-05 | An unknown decision code is refused | a record with decision code "D99" | it is written | it is refused with message MSG-P7-009 naming "decisionCode" | RWB-E1-027 |
| AC-EXC-P7-008-06 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-008-07 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-008-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.9 Carry a freshness stamp on every decision input

#### A2.9.1 Intent

**Business objective.** Attaches the age of each input to the decision, so a decision taken on stale data is visible.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Attaches the age of each input to the decision, so a decision taken on stale data is visible.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Carry a freshness stamp on every decision input | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, ACE database

**Prerequisites.** FEAT-RDF-14

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-009-1 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-009-2 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| VR-P7-009-3 | A decision input is past its age limit | MSG-P7-006 {input} is {days} days old, past its limit. Refresh it before you decide. |
| BR-P7-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Center of excellence analyst | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-009-01 | Freshness on the row | the ACE batch for the account and arrears product (DP01) for business date 2026-11-30 completed at 06:50 on 2026-12-01 in `v_ace_batch_status` from an extract taken at 23:30 on 2026-11-30 And account "ACC-SYN-000101" has data_as_of 2026-11-30 in `v_ace_account` | the row is read through FreshnessQuery.stampForRow("DP01", 2026-11-30) and GET /data-products/freshness?product=DP01 | the row carries source time 2026-11-30T23:30+07:00 and load time 2026-12-01T06:50+07:00 And the status is "LOADED" | RWB-E1-015 |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-009-01 | Stale product flagged | no COMPLETED ACE batch for the DP01 sources for business date 2026-11-30 exists in `v_ace_batch_status` at 08:00 on 2026-12-01 | the freshness step runs at 08:00 | the product is flagged "STALE" And `data_product_load` records the STALE stamp for "DP01" with check "FRESHNESS" on 2026-12-01 And the alert goes to the operations channel And the case record view shows the stamp in the data panel with "Account and arrears is from 2026-11-30. Today's ACE batch has not arrived." | RWB-E1-015 |
| AC-ALT-P7-009-02 | Freshness in the decision log | a decision log entry for case "RW-2026-000101" read DP01 for 2026-11-30 and DP06 for 2026-11-23 | the entry and its inputs snapshot are read | the snapshot lists DP01 with load time 2026-12-01T06:50+07:00 and status "LOADED" And the snapshot lists DP06 with load time 2026-11-24T04:40+07:00 and status "LOADED" | RWB-E1-015 |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-009-01 | A failed ACE batch marks the product stale at once | the ACE batch for a DP01 source for 2026-11-30 has status FAILED in `v_ace_batch_status` at 05:20 | the freshness step reads the batch status | DP01 is "STALE" from 05:20 And the stamp for business date 2026-11-30 stays the one in use | RWB-E1-015 |
| AC-EXC-P7-009-02 | A late ACE batch clears the stale flag | DP01 was flagged "STALE" at 08:00 on 2026-12-01 | the ACE batch for DP01 for 2026-11-30 completes at 08:40 in `v_ace_batch_status` | DP01 status is "LOADED" with load time 2026-12-01T08:40+07:00 And the FRESHNESS exception for DP01 on 2026-12-01 is closed | RWB-E1-015 |
| AC-EXC-P7-009-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-009-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-009-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.10 Generate notices from approved templates to WIN

#### A2.10.1 Intent

**Business objective.** Produces demand, recall and guarantor notices from Legal-approved templates and sends them to WIN.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Produces demand, recall and guarantor notices from Legal-approved templates and sends them to WIN.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Generate notices from approved templates to WIN | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** WIN, Workbench

**Prerequisites.** FEAT-DRI-15

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-010-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P7-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner, Legal counsel | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-010-01 | Generated | party "P-0001" has a postal address contact point | NoticeApi.generate is called for case "RC-2026-000123", notice type "DEMAND", party "P-0001" and language "TH" | a PDF is stored on the case with source "GENERATED" and write_once true And the PDF shows "RC-2026-000123" and 1,250,000.00 THB And the footer reads "RC-2026-000123 DEMAND-MTG v2 2026-11-25" And a notice row exists with notice type "DEMAND", sent type "NPL", the document ID and state "Generated" And one decision log entry exists with decision code "D7.1", rule "R-LIT-03" and template "DEMAND-MTG" version 2 And NoticeGenerated is written to the outbox with the notice ID and template version 2 | RWB-E1-052 |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-010-01 | Stale account data | the account data product is from 2026-11-24 because the ACE batch of 2026-11-25 has not completed | NoticeApi.generate is called for case "RC-2026-000123", notice type "DEMAND" | the notice is generated from the 2026-11-24 data And the decision log entry records data date 2026-11-24 And the result carries MSG-P1-001 naming "DP01 Account and arrears" and 2026-11-24 | RWB-E1-052 |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-010-01 | Template approval checked | template "RECALL-HP" "TH" has only version 1 in state "Draft" And case "RC-2026-000456" has product group "HIRE_PURCHASE" | NoticeApi.generate is called for case "RC-2026-000456", notice type "RECALL" and language "TH" | it is refused with MSG-P6-005 naming "RECALL-HP" version 1 And no notice row and no document are created | RWB-E1-052 |
| AC-EXC-P7-010-02 | Missing field | party "P-0001" on case "RC-2026-000123" has no postal address contact point | NoticeApi.generate is called for notice type "DEMAND" | a notice row exists in state "Held" with hold reason "POSTAL_ADDRESS" And no document is stored And a task "Complete notice data" is raised to the case owner of "RC-2026-000123" with MSG-P6-007 naming "POSTAL_ADDRESS" | RWB-E1-052 |
| AC-EXC-P7-010-03 | Withdrawn template holds the notice | template "DEMAND-MTG" "TH" version 2 is Withdrawn and no later version is Approved | NoticeApi.generate is called for case "RC-2026-000123", notice type "DEMAND" | a notice row exists in state "Held" with hold reason "TEMPLATE_WITHDRAWN" And a task is raised to the litigation officer team with MSG-P6-003 naming "DEMAND-MTG" | RWB-E1-052 |
| AC-EXC-P7-010-04 | Decision log write fails | the decision log store is unavailable | NoticeApi.generate is called for case "RC-2026-000123", notice type "DEMAND" | the call fails with MSG-P7-003 And no notice row and no document are created And an incident is raised under rule R-UNI-39 | RWB-E1-052 |
| AC-EXC-P7-010-05 | Repeated request on the same business date | a notice for case "RC-2026-000123", notice type "DEMAND", party "P-0001" was generated on 2026-11-25 | NoticeApi.generate is called again with the same values on 2026-11-25 | the existing notice is returned And the case still has one DEMAND notice and one generated document for 2026-11-25 | RWB-E1-052 |
| AC-EXC-P7-010-06 | Party not on the case | party "P-0999" is not a party on case "RC-2026-000123" | NoticeApi.generate is called with party "P-0999" | it is refused with MSG-P4-003 | RWB-E1-052 |
| AC-EXC-P7-010-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-010-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-010-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.11 Manage letter templates with Legal approval

#### A2.11.1 Intent

**Business objective.** Holds every letter and notice template with its version and the Legal approval that put it in force.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Holds every letter and notice template with its version and the Legal approval that put it in force.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Legal counsel | Opens the screen and manage letter templates with Legal approval | Checks the role, the capability area and the scope |
| 2 | Legal counsel | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-23

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-011-1 | Approval above the approver's limit | MSG-P7-001 This needs approval at level {level}. It has been sent to {approver}. |
| BR-P7-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| decision_log_entry.case_id | The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case | uuid | No | None | No |
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | No |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| Legal counsel | Primary |
| Center of excellence analyst, Compliance and PDPA officer | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-011-01 | New version | "LIT-0101" uploads "demand-mtg-th-v3.docx" for "DEMAND-MTG" "TH" using merge codes "CASE_NO" and "TOTAL_OUTSTANDING" And version 3 is created in state "Draft" | "LEG-0001" approves version 3 with valid from 2026-11-20 | version 3 has state "Approved", approver "LEG-0001" and an approval time on 2026-11-20 And TemplateCatalog returns version 3 as current for "DEMAND-MTG" "TH" on 2026-11-20 And version 2 stays readable on SCR-33 with approver "LEG-0001" | RWB-E1-034 |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-011-01 | Approval required | version 3 of "DEMAND-MTG" "TH" is in state "Draft" with no approver | "LIT-0101" chooses set current on version 3 | it is refused with MSG-P6-005 naming "DEMAND-MTG" version 3 And version 2 stays current | RWB-E1-034 |
| AC-ALT-P7-011-02 | Required field empty | "LIT-0101" uploads a body with no template code | the upload is sent | it is refused with status 422 and MSG-GEN-001 naming "template code" | RWB-E1-034 |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-011-01 | The uploader cannot approve the version | "LEG-0001" uploaded version 4 of "RECALL-SSME" "TH" | "LEG-0001" approves version 4 | it is refused with status 409 and MSG-P7-002 And version 4 stays "Draft" | RWB-E1-034 |
| AC-EXC-P7-011-02 | Unknown merge code refused at upload | "LIT-0101" uploads a body for "DEMAND-HP" "TH" that uses the merge code "LINE_ID" And "LINE_ID" is not in the merge field catalog | the upload is sent | it is refused with status 422 and MSG-P6-006 naming "LINE_ID" And no version of "DEMAND-HP" is created and no file is stored | RWB-E1-034 |
| AC-EXC-P7-011-03 | File type not allowed | "LIT-0101" uploads "demand.pdf" for "DEMAND-MTG" "TH" | the upload is sent | it is refused with status 415 and MSG-P6-010 naming "DOCX" | RWB-E1-034 |
| AC-EXC-P7-011-04 | Repeated approval request | "LEG-0001" approved version 3 with Idempotency-Key "7f1c0d2e-0001" | the same request is sent again with Idempotency-Key "7f1c0d2e-0001" | the response is the first response with status 200 And the audit log holds one approval for version 3 | RWB-E1-034 |
| AC-EXC-P7-011-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-011-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-011-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.12 Hold the template catalog with merge fields

#### A2.12.1 Intent

**Business objective.** Keeps the catalog of templates and the merge fields each one draws from the case.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Keeps the catalog of templates and the merge fields each one draws from the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Reference data administrator | Opens the screen and hold the template catalog with merge fields | Checks the role, the capability area and the scope |
| 2 | Reference data administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-DRI-15

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-012-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-P7-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| decision_log_entry.case_id | The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case | uuid | No | None | No |
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | No |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| Reference data administrator | Primary |
| Legal counsel | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-012-01 | Merge fields checked | a load file for template "GUARANTOR-SSME" whose body uses the merge code "GUARANTOR_EMAIL" And "GUARANTOR_EMAIL" is not in the catalog | it is loaded | the load is refused whole with MSG-P6-006 naming "GUARANTOR_EMAIL" And no version of "GUARANTOR-SSME" is created | RWB-E1-046 |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-012-01 | Future valid from date keeps the earlier version current | version 3 of "DEMAND-MTG" "TH" is Approved with valid from 2026-12-01 | TemplateCatalog is asked on 2026-11-30 and on 2026-12-01 | it returns version 2 on 2026-11-30 And it returns version 3 on 2026-12-01 | RWB-E1-046 |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-012-01 | Template versioned | a load file for template "DEMAND-MTG" language "TH" approved by user "LEG-0001" on 2026-11-10 with valid from 2026-11-10 | it is loaded on 2026-11-10 | version 2 of "DEMAND-MTG" is created with state "Approved", approver "LEG-0001" and approval date 2026-11-10 And TemplateCatalog returns version 2 as current for "DEMAND-MTG", "TH" on 2026-11-10 And version 1 stays readable with its own approver and approval date | RWB-E1-046 |
| AC-EXC-P7-012-02 | Unapproved template blocked | template "RECALL-HP" in language "TH" has only version 1 in state "Draft" | the letter engine asks TemplateCatalog for the current version of "RECALL-HP", "TH" | the catalog refuses with TemplateNotApprovedException And the refusal carries MSG-P6-005 naming "RECALL-HP" version 1 | RWB-E1-046 |
| AC-EXC-P7-012-03 | Catalog row with an unknown field ID is refused | a catalog load file of 12 rows where row 7 names a BR Field ID "XX-CAS-999" that is not in the data dictionary | it is loaded | the load is refused whole with MSG-P1-002 naming the check "field ID not in the data dictionary" And catalog version "MF-2026.11" stays in force | RWB-E1-046 |
| AC-EXC-P7-012-04 | Template row with a missing required field is refused | a template load file whose row has no body reference | it is loaded | the load is refused whole with MSG-GEN-001 naming "body_ref" | RWB-E1-046 |
| AC-EXC-P7-012-05 | Repeated load creates no new version | the load file of AC1 has been loaded once and version 2 exists | the same file with the same file hash is loaded again | the load is refused with MSG-P1-002 naming the check "repeat of load" And "DEMAND-MTG" still has 2 versions | RWB-E1-046 |
| AC-EXC-P7-012-06 | Withdrawn current version leaves no current version | version 2 of "DEMAND-MTG" "TH" was Approved and current and is now in state "Withdrawn" | the letter engine asks TemplateCatalog for the current version of "DEMAND-MTG", "TH" on 2026-11-20 | TemplateCatalog returns no current version and throws TemplateWithdrawnException And the refusal carries MSG-P6-003 naming "DEMAND-MTG" | RWB-E1-046 |
| AC-EXC-P7-012-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-012-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-012-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.13 Capture proof of delivery from WIN

#### A2.13.1 Intent

**Business objective.** Takes the delivery confirmation back from WIN and records it against the notice on the case.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.13.2 Description

**Functional overview.** Takes the delivery confirmation back from WIN and records it against the notice on the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Capture proof of delivery from WIN | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** WIN, Workbench

**Prerequisites.** FEAT-DRI-14

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-013-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P7-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-013-01 | Dispatched | JOB-10 runs at 16:00 on 2026-11-25 | WIN acknowledges the file with sent date 26112026, barcode "RR123456789TH" and sent type "NPL" for contract "CT-77001" | notice "N-0001" has state "Sent", sent date 2026-11-26 and barcode "RR123456789TH" And the interaction ledger has an outbound "LETTER" entry for case "RC-2026-000123" on 2026-11-26 And NoticeDispatched is written to the outbox with notice "N-0001", barcode "RR123456789TH" and sent date 2026-11-26 And the case record shows MSG-P6-004 "DEMAND was sent for registered mail on 26 November 2026." | RWB-E1-055 |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-013-01 | Proof of delivery | notice "N-0001" is "Sent" with barcode "RR123456789TH" | `v_ace_pod` for business date 2026-11-30 holds barcode "RR123456789TH" with call-back date 28112026 | notice "N-0001" has state "Delivered", delivery status "DELIVERED" and callback date 2026-11-28 And NoticeDelivered is written to the outbox with delivered date 2026-11-28 And case "RC-2026-000123" has a running "NOTICE_PERIOD" timer started on 2026-11-28 | RWB-E1-055 |
| AC-ALT-P7-013-02 | Proof of delivery read from ACE | the sample WIN file "WIN-POD-SAMPLE-v1" of 25 records supplied by the WIN owner is ingested by ACE into `pod_receipt` in SIT | the Workbench reads `v_ace_pod` for that business date | 25 rows are returned with barcode, call-back date and delivery status And `v_ace_batch_status` shows source WIN COMPLETED for that business date | RWB-E1-055 |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-013-01 | File not acknowledged | the WIN file of 2026-11-25 holding "N-0001" is not acknowledged | JOB-10 runs on 2026-11-26, 2026-11-27 and 2026-11-28 and none is acknowledged | "N-0001" is sent in each of the three files and stays "Generated" And after the third failure a task is raised to the litigation officer team with MSG-GEN-006 naming "WIN" | RWB-E1-055 |
| AC-EXC-P7-013-02 | Proof of delivery batch not complete | the ACE batch for source WIN for the business date is not COMPLETED in `v_ace_batch_status` | the delivery step runs | no `v_ace_pod` row of that business date is applied And no notice changes state | RWB-E1-055 |
| AC-EXC-P7-013-03 | Repeated dispatch run | JOB-10 has written notice "N-0001" in the file of 2026-11-25 | JOB-10 is rerun on 2026-11-25 from the job monitor | the second file does not hold "N-0001" | RWB-E1-055 |
| AC-EXC-P7-013-04 | Barcode missing after three days | notice "N-0002" was in the file of 2026-11-25 and no barcode has returned | the daily reconciliation REC-05 runs on 2026-11-28 | "N-0002" is listed as a break for the platform administrator on SCR-45 | RWB-E1-055 |
| AC-EXC-P7-013-05 | Repeated delivery record | notice "N-0001" is "Delivered" with callback date 2026-11-28 | `v_ace_pod` for business date 2026-12-07 repeats barcode "RR123456789TH" with call-back date 28112026 | the notice is unchanged And no second NoticeDelivered is written And the repeat is counted under rule R-UNI-40 | RWB-E1-055 |
| AC-EXC-P7-013-06 | Proof of delivery file late | the ACE batch for source WIN due on 2026-11-30 has not completed in `v_ace_batch_status` | a litigation officer opens case "RC-2026-000123" on 2026-12-01 | the notice section shows MSG-P1-001 naming "DP07 Legal" and 2026-11-23 | RWB-E1-055 |
| AC-EXC-P7-013-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-013-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-013-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.14 Run run books and monitoring for every job

#### A2.14.1 Intent

**Business objective.** Gives every scheduled job a run book, an alert and an owner, so a failed job is noticed the same day.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.14.2 Description

**Functional overview.** Gives every scheduled job a run book, an alert and an owner, so a failed job is noticed the same day.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Platform administrator | Opens the screen and run run books and monitoring for every job | Checks the role, the capability area and the scope |
| 2 | Platform administrator | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Log Analytics, Control-M

**Prerequisites.** FEAT-RDF-22

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-014-1 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| BR-P7-014 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.14.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| decision_log_entry.case_id | The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case | uuid | No | None | No |
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | No |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| Platform administrator | Primary |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-014-01 | Run book present | the list of Epic 1 jobs and services in job_catalog | RunbookCompletenessTest runs in the pipeline | each of the 13 jobs has a file in docs/operations/runbooks And each file has the sections purpose, schedule, owner, failure signs, restart steps and escalation | RWB-E1-056 |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-014-01 | Restart by run book | JOB-02 failed at 05:20 on business date 2026-11-26 while it read `v_ace_efs_action` after the ACE batch for source EFS completed | a platform administrator follows the restart steps and calls POST /admin/jobs/{jobId}/rerun at 06:05 | JOB-02 restarts from its failed step and ends with status "COMPLETED" at 06:25 And the case list shows cases with data as of 2026-11-26 And no developer action is recorded in the run | RWB-E1-056 |
| AC-ALT-P7-014-02 | Monitoring in place | every job in job_catalog ran at least once in SIT | the platform administrator opens the workbook "Recovery jobs" | each of the 13 jobs shows its last run time, status and duration And GET /admin/jobs returns the same last run, status, startedAt and endedAt for each job | RWB-E1-056 |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-014-01 | Missing run book blocks the build | a developer adds a Quartz job "JOB-12" with a run book that has no "Escalation" section | the pipeline runs | the build fails with message MSG-P2-005 naming job "JOB-12" and section "Escalation" | RWB-E1-056 |
| AC-EXC-P7-014-02 | Rerun while running refused | JOB-03 started at 06:40 and is running | a platform administrator calls POST /admin/jobs/{jobId}/rerun for JOB-03 at 06:45 | the response is 409 with message MSG-P2-006 And JOB-03 continues its run | RWB-E1-056 |
| AC-EXC-P7-014-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-014-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-014-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.15 Route a recommendation to the approver by limit

#### A2.15.1 Intent

**Business objective.** Reads the delegation of authority table and sends the recommendation to the role that can approve it.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.15.2 Description

**Functional overview.** Reads the delegation of authority table and sends the recommendation to the role that can approve it.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Route a recommendation to the approver by limit | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Rules component

**Prerequisites.** FEAT-ACA-06

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-015-1 | Approval above the approver's limit | MSG-P7-001 This needs approval at level {level}. It has been sent to {approver}. |
| VR-P7-015-2 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-015-3 | Override without a reason | MSG-P7-005 Enter the reason you are not following the recommendation. |
| BR-P7-015 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner, Product head (Mortgage, HP, SSME) | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-015-01 | Routed | a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12" and prepared by "U-9211" | the router runs for decision D7.1 at 09:00 on 14 December 2026 | an approval appears in the queue of role RW-LITOFF with decision D7.1, area "LITIGATION", no amount limit and due at 09:00 on 15 December 2026 And it is not shown to "U-9211", who prepared it And the routing entry records rule "R-LIT-03", version "LIT-2026.12" and route parameter "rwb.approval.route.D7.1.role" And the case status becomes "Waiting approval" | RWB-E2-013 |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-015-01 | Limit changed | approval "A-1" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 was routed to L6 under "DOA-2026.11" And version "DOA-2027.01" from 1 January 2027 moves that amount to L5 | a new D6.4 approval with the same amounts routes on 2 January 2027 | the new approval goes to L5 holder "U-9202" and its entry records "DOA-2027.01" And approval "A-1" stays with L6 and "DOA-2026.11" | RWB-E2-013 |
| AC-ALT-P7-015-02 | Routed by limit | restructure officer "U-9210" prepared a settlement at a discount on case "RW-2026-000124", decision D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00, loss 20.00 percent, loss amount 480,000.00 | the router runs | the approval is assigned to L6 holder "U-9201" with the delegation row ID and version "DOA-2026.11" And GET /approvals for "U-9201" lists it with amount 2,400,000.00, level "L6" and its age | RWB-E2-013 |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-015-01 | Escalated | the approval of AC1 is still WAITING at 09:00 on 15 December 2026 | JOB-05 publishes TimerBreached for its service level timer | the approval moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026 And one entry with final call "ESCALATED" is written and "U-9213" is told with MSG-P7-011 And the case stays "Waiting approval" | RWB-E2-013 |
| AC-EXC-P7-015-02 | The preparer cannot approve | "U-9210" also holds RW-PRODHEAD at L6 as substitute | "U-9210" approves the approval of AC4 | the call is refused with status 409 and message MSG-P7-002 and the approval stays "WAITING" | RWB-E2-013 |
| AC-EXC-P7-015-03 | A change above the limit goes up | the approval of AC4 is WAITING with "U-9201" | "U-9201" changes the principal to 120,000,000.00 with coded reason "CUSTOMER_REVISED_OFFER" and approves | the call returns MSG-P7-001 with level "L5" and approver "U-9202" And the approval moves to L5 with the changed terms and status "WAITING", and no approval at L6 is recorded | RWB-E2-013 |
| AC-EXC-P7-015-04 | Refuse needs a reason | the approval of AC4 is WAITING | "U-9201" refuses it with no reason | the call is refused with status 422 and message MSG-GEN-001 for field "reason" And when "U-9201" refuses it with reason "Collateral appraisal older than one year" the status becomes "REFUSED", the entry records the reason, and the case returns to the state the rule names | RWB-E2-013 |
| AC-EXC-P7-015-05 | No holder means escalation, not a stall | the L6 row for SSME has no holder and no substitute | an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes | it is assigned to the L5 holder at once And the routing entry records reason "NO_HOLDER" for L6 | RWB-E2-013 |
| AC-EXC-P7-015-06 | No limit covers the decision | "DOA-2026.11" holds no row for HIRE_PURCHASE | an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes | the approval is stored with status "HELD_NO_LIMIT" and the case stays "Waiting approval" And an incident is raised to RW-RISK with message MSG-P7-010 | RWB-E2-013 |
| AC-EXC-P7-015-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-015-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-015-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.16 Approve inside the limit

#### A2.16.1 Intent

**Business objective.** Lets the approver accept the recommendation, which books the decision and starts the next step.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.16.2 Description

**Functional overview.** Lets the approver accept the recommendation, which books the decision and starts the next step.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and approve inside the limit | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-APD-01

#### A2.16.3 Business rules and structure

##### A2.16.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-016-1 | Approval above the approver's limit | MSG-P7-001 This needs approval at level {level}. It has been sent to {approver}. |
| VR-P7-016-2 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-016-3 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| BR-P7-016 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.16.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| decision_log_entry.case_id | The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case | uuid | No | None | No |
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | No |

##### A2.16.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Product head (Mortgage, HP, SSME), Credit approval committee member | Also uses |

#### A2.16.4 Acceptance criteria

##### A2.16.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-016-01 | Routed | a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12" and prepared by "U-9211" | the router runs for decision D7.1 at 09:00 on 14 December 2026 | an approval appears in the queue of role RW-LITOFF with decision D7.1, area "LITIGATION", no amount limit and due at 09:00 on 15 December 2026 And it is not shown to "U-9211", who prepared it And the routing entry records rule "R-LIT-03", version "LIT-2026.12" and route parameter "rwb.approval.route.D7.1.role" And the case status becomes "Waiting approval" | RWB-E2-013 |

##### A2.16.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-016-01 | Limit changed | approval "A-1" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 was routed to L6 under "DOA-2026.11" And version "DOA-2027.01" from 1 January 2027 moves that amount to L5 | a new D6.4 approval with the same amounts routes on 2 January 2027 | the new approval goes to L5 holder "U-9202" and its entry records "DOA-2027.01" And approval "A-1" stays with L6 and "DOA-2026.11" | RWB-E2-013 |
| AC-ALT-P7-016-02 | Routed by limit | restructure officer "U-9210" prepared a settlement at a discount on case "RW-2026-000124", decision D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00, loss 20.00 percent, loss amount 480,000.00 | the router runs | the approval is assigned to L6 holder "U-9201" with the delegation row ID and version "DOA-2026.11" And GET /approvals for "U-9201" lists it with amount 2,400,000.00, level "L6" and its age | RWB-E2-013 |

##### A2.16.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-016-01 | Escalated | the approval of AC1 is still WAITING at 09:00 on 15 December 2026 | JOB-05 publishes TimerBreached for its service level timer | the approval moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026 And one entry with final call "ESCALATED" is written and "U-9213" is told with MSG-P7-011 And the case stays "Waiting approval" | RWB-E2-013 |
| AC-EXC-P7-016-02 | The preparer cannot approve | "U-9210" also holds RW-PRODHEAD at L6 as substitute | "U-9210" approves the approval of AC4 | the call is refused with status 409 and message MSG-P7-002 and the approval stays "WAITING" | RWB-E2-013 |
| AC-EXC-P7-016-03 | A change above the limit goes up | the approval of AC4 is WAITING with "U-9201" | "U-9201" changes the principal to 120,000,000.00 with coded reason "CUSTOMER_REVISED_OFFER" and approves | the call returns MSG-P7-001 with level "L5" and approver "U-9202" And the approval moves to L5 with the changed terms and status "WAITING", and no approval at L6 is recorded | RWB-E2-013 |
| AC-EXC-P7-016-04 | Refuse needs a reason | the approval of AC4 is WAITING | "U-9201" refuses it with no reason | the call is refused with status 422 and message MSG-GEN-001 for field "reason" And when "U-9201" refuses it with reason "Collateral appraisal older than one year" the status becomes "REFUSED", the entry records the reason, and the case returns to the state the rule names | RWB-E2-013 |
| AC-EXC-P7-016-05 | No holder means escalation, not a stall | the L6 row for SSME has no holder and no substitute | an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes | it is assigned to the L5 holder at once And the routing entry records reason "NO_HOLDER" for L6 | RWB-E2-013 |
| AC-EXC-P7-016-06 | No limit covers the decision | "DOA-2026.11" holds no row for HIRE_PURCHASE | an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes | the approval is stored with status "HELD_NO_LIMIT" and the case stays "Waiting approval" And an incident is raised to RW-RISK with message MSG-P7-010 | RWB-E2-013 |
| AC-EXC-P7-016-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-016-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.16.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-016-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.17 Change a recommendation before approving

#### A2.17.1 Intent

**Business objective.** Lets the approver change the terms within their limit, and records what changed and why.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.17.2 Description

**Functional overview.** Lets the approver change the terms within their limit, and records what changed and why.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and change a recommendation before approving | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-APD-02

#### A2.17.3 Business rules and structure

##### A2.17.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-017-1 | Approval above the approver's limit | MSG-P7-001 This needs approval at level {level}. It has been sent to {approver}. |
| VR-P7-017-2 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-017-3 | Override without a reason | MSG-P7-005 Enter the reason you are not following the recommendation. |
| BR-P7-017 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.17.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| decision_log_entry.case_id | The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case | uuid | No | None | No |
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | No |

##### A2.17.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Product head (Mortgage, HP, SSME) | Also uses |

#### A2.17.4 Acceptance criteria

##### A2.17.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-017-01 | Routed | a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12" and prepared by "U-9211" | the router runs for decision D7.1 at 09:00 on 14 December 2026 | an approval appears in the queue of role RW-LITOFF with decision D7.1, area "LITIGATION", no amount limit and due at 09:00 on 15 December 2026 And it is not shown to "U-9211", who prepared it And the routing entry records rule "R-LIT-03", version "LIT-2026.12" and route parameter "rwb.approval.route.D7.1.role" And the case status becomes "Waiting approval" | RWB-E2-013 |

##### A2.17.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-017-01 | Limit changed | approval "A-1" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 was routed to L6 under "DOA-2026.11" And version "DOA-2027.01" from 1 January 2027 moves that amount to L5 | a new D6.4 approval with the same amounts routes on 2 January 2027 | the new approval goes to L5 holder "U-9202" and its entry records "DOA-2027.01" And approval "A-1" stays with L6 and "DOA-2026.11" | RWB-E2-013 |
| AC-ALT-P7-017-02 | Routed by limit | restructure officer "U-9210" prepared a settlement at a discount on case "RW-2026-000124", decision D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00, loss 20.00 percent, loss amount 480,000.00 | the router runs | the approval is assigned to L6 holder "U-9201" with the delegation row ID and version "DOA-2026.11" And GET /approvals for "U-9201" lists it with amount 2,400,000.00, level "L6" and its age | RWB-E2-013 |

##### A2.17.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-017-01 | Escalated | the approval of AC1 is still WAITING at 09:00 on 15 December 2026 | JOB-05 publishes TimerBreached for its service level timer | the approval moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026 And one entry with final call "ESCALATED" is written and "U-9213" is told with MSG-P7-011 And the case stays "Waiting approval" | RWB-E2-013 |
| AC-EXC-P7-017-02 | The preparer cannot approve | "U-9210" also holds RW-PRODHEAD at L6 as substitute | "U-9210" approves the approval of AC4 | the call is refused with status 409 and message MSG-P7-002 and the approval stays "WAITING" | RWB-E2-013 |
| AC-EXC-P7-017-03 | A change above the limit goes up | the approval of AC4 is WAITING with "U-9201" | "U-9201" changes the principal to 120,000,000.00 with coded reason "CUSTOMER_REVISED_OFFER" and approves | the call returns MSG-P7-001 with level "L5" and approver "U-9202" And the approval moves to L5 with the changed terms and status "WAITING", and no approval at L6 is recorded | RWB-E2-013 |
| AC-EXC-P7-017-04 | Refuse needs a reason | the approval of AC4 is WAITING | "U-9201" refuses it with no reason | the call is refused with status 422 and message MSG-GEN-001 for field "reason" And when "U-9201" refuses it with reason "Collateral appraisal older than one year" the status becomes "REFUSED", the entry records the reason, and the case returns to the state the rule names | RWB-E2-013 |
| AC-EXC-P7-017-05 | No holder means escalation, not a stall | the L6 row for SSME has no holder and no substitute | an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes | it is assigned to the L5 holder at once And the routing entry records reason "NO_HOLDER" for L6 | RWB-E2-013 |
| AC-EXC-P7-017-06 | No limit covers the decision | "DOA-2026.11" holds no row for HIRE_PURCHASE | an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes | the approval is stored with status "HELD_NO_LIMIT" and the case stays "Waiting approval" And an incident is raised to RW-RISK with message MSG-P7-010 | RWB-E2-013 |
| AC-EXC-P7-017-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-017-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.17.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-017-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.18 Reject a recommendation with a reason

#### A2.18.1 Intent

**Business objective.** Lets the approver reject, with a coded reason that returns the case to the point the rule names.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.18.2 Description

**Functional overview.** Lets the approver reject, with a coded reason that returns the case to the point the rule names.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and reject a recommendation with a reason | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-APD-02

#### A2.18.3 Business rules and structure

##### A2.18.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-018-1 | Approval above the approver's limit | MSG-P7-001 This needs approval at level {level}. It has been sent to {approver}. |
| VR-P7-018-2 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-018-3 | Override without a reason | MSG-P7-005 Enter the reason you are not following the recommendation. |
| BR-P7-018 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.18.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| decision_log_entry.case_id | The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case | uuid | No | None | No |
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | No |

##### A2.18.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Product head (Mortgage, HP, SSME) | Also uses |

#### A2.18.4 Acceptance criteria

##### A2.18.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-018-01 | Routed | a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12" and prepared by "U-9211" | the router runs for decision D7.1 at 09:00 on 14 December 2026 | an approval appears in the queue of role RW-LITOFF with decision D7.1, area "LITIGATION", no amount limit and due at 09:00 on 15 December 2026 And it is not shown to "U-9211", who prepared it And the routing entry records rule "R-LIT-03", version "LIT-2026.12" and route parameter "rwb.approval.route.D7.1.role" And the case status becomes "Waiting approval" | RWB-E2-013 |

##### A2.18.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-018-01 | Limit changed | approval "A-1" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 was routed to L6 under "DOA-2026.11" And version "DOA-2027.01" from 1 January 2027 moves that amount to L5 | a new D6.4 approval with the same amounts routes on 2 January 2027 | the new approval goes to L5 holder "U-9202" and its entry records "DOA-2027.01" And approval "A-1" stays with L6 and "DOA-2026.11" | RWB-E2-013 |
| AC-ALT-P7-018-02 | Routed by limit | restructure officer "U-9210" prepared a settlement at a discount on case "RW-2026-000124", decision D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00, loss 20.00 percent, loss amount 480,000.00 | the router runs | the approval is assigned to L6 holder "U-9201" with the delegation row ID and version "DOA-2026.11" And GET /approvals for "U-9201" lists it with amount 2,400,000.00, level "L6" and its age | RWB-E2-013 |

##### A2.18.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-018-01 | Escalated | the approval of AC1 is still WAITING at 09:00 on 15 December 2026 | JOB-05 publishes TimerBreached for its service level timer | the approval moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026 And one entry with final call "ESCALATED" is written and "U-9213" is told with MSG-P7-011 And the case stays "Waiting approval" | RWB-E2-013 |
| AC-EXC-P7-018-02 | The preparer cannot approve | "U-9210" also holds RW-PRODHEAD at L6 as substitute | "U-9210" approves the approval of AC4 | the call is refused with status 409 and message MSG-P7-002 and the approval stays "WAITING" | RWB-E2-013 |
| AC-EXC-P7-018-03 | A change above the limit goes up | the approval of AC4 is WAITING with "U-9201" | "U-9201" changes the principal to 120,000,000.00 with coded reason "CUSTOMER_REVISED_OFFER" and approves | the call returns MSG-P7-001 with level "L5" and approver "U-9202" And the approval moves to L5 with the changed terms and status "WAITING", and no approval at L6 is recorded | RWB-E2-013 |
| AC-EXC-P7-018-04 | Refuse needs a reason | the approval of AC4 is WAITING | "U-9201" refuses it with no reason | the call is refused with status 422 and message MSG-GEN-001 for field "reason" And when "U-9201" refuses it with reason "Collateral appraisal older than one year" the status becomes "REFUSED", the entry records the reason, and the case returns to the state the rule names | RWB-E2-013 |
| AC-EXC-P7-018-05 | No holder means escalation, not a stall | the L6 row for SSME has no holder and no substitute | an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes | it is assigned to the L5 holder at once And the routing entry records reason "NO_HOLDER" for L6 | RWB-E2-013 |
| AC-EXC-P7-018-06 | No limit covers the decision | "DOA-2026.11" holds no row for HIRE_PURCHASE | an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes | the approval is stored with status "HELD_NO_LIMIT" and the case stays "Waiting approval" And an incident is raised to RW-RISK with message MSG-P7-010 | RWB-E2-013 |
| AC-EXC-P7-018-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-018-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.18.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-018-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.19 Escalate above the limit

#### A2.19.1 Intent

**Business objective.** Sends a recommendation beyond the approver's limit to the next role in the matrix.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.19.2 Description

**Functional overview.** Sends a recommendation beyond the approver's limit to the next role in the matrix.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Escalate above the limit | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-APD-01

#### A2.19.3 Business rules and structure

##### A2.19.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-019-1 | Approval above the approver's limit | MSG-P7-001 This needs approval at level {level}. It has been sent to {approver}. |
| VR-P7-019-2 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-019-3 | Override without a reason | MSG-P7-005 Enter the reason you are not following the recommendation. |
| BR-P7-019 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.19.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Product head (Mortgage, HP, SSME), Credit approval committee member | Also uses |

#### A2.19.4 Acceptance criteria

##### A2.19.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-019-01 | Routed | a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12" and prepared by "U-9211" | the router runs for decision D7.1 at 09:00 on 14 December 2026 | an approval appears in the queue of role RW-LITOFF with decision D7.1, area "LITIGATION", no amount limit and due at 09:00 on 15 December 2026 And it is not shown to "U-9211", who prepared it And the routing entry records rule "R-LIT-03", version "LIT-2026.12" and route parameter "rwb.approval.route.D7.1.role" And the case status becomes "Waiting approval" | RWB-E2-013 |

##### A2.19.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-019-01 | Limit changed | approval "A-1" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 was routed to L6 under "DOA-2026.11" And version "DOA-2027.01" from 1 January 2027 moves that amount to L5 | a new D6.4 approval with the same amounts routes on 2 January 2027 | the new approval goes to L5 holder "U-9202" and its entry records "DOA-2027.01" And approval "A-1" stays with L6 and "DOA-2026.11" | RWB-E2-013 |
| AC-ALT-P7-019-02 | Routed by limit | restructure officer "U-9210" prepared a settlement at a discount on case "RW-2026-000124", decision D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00, loss 20.00 percent, loss amount 480,000.00 | the router runs | the approval is assigned to L6 holder "U-9201" with the delegation row ID and version "DOA-2026.11" And GET /approvals for "U-9201" lists it with amount 2,400,000.00, level "L6" and its age | RWB-E2-013 |

##### A2.19.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-019-01 | Escalated | the approval of AC1 is still WAITING at 09:00 on 15 December 2026 | JOB-05 publishes TimerBreached for its service level timer | the approval moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026 And one entry with final call "ESCALATED" is written and "U-9213" is told with MSG-P7-011 And the case stays "Waiting approval" | RWB-E2-013 |
| AC-EXC-P7-019-02 | The preparer cannot approve | "U-9210" also holds RW-PRODHEAD at L6 as substitute | "U-9210" approves the approval of AC4 | the call is refused with status 409 and message MSG-P7-002 and the approval stays "WAITING" | RWB-E2-013 |
| AC-EXC-P7-019-03 | A change above the limit goes up | the approval of AC4 is WAITING with "U-9201" | "U-9201" changes the principal to 120,000,000.00 with coded reason "CUSTOMER_REVISED_OFFER" and approves | the call returns MSG-P7-001 with level "L5" and approver "U-9202" And the approval moves to L5 with the changed terms and status "WAITING", and no approval at L6 is recorded | RWB-E2-013 |
| AC-EXC-P7-019-04 | Refuse needs a reason | the approval of AC4 is WAITING | "U-9201" refuses it with no reason | the call is refused with status 422 and message MSG-GEN-001 for field "reason" And when "U-9201" refuses it with reason "Collateral appraisal older than one year" the status becomes "REFUSED", the entry records the reason, and the case returns to the state the rule names | RWB-E2-013 |
| AC-EXC-P7-019-05 | No holder means escalation, not a stall | the L6 row for SSME has no holder and no substitute | an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes | it is assigned to the L5 holder at once And the routing entry records reason "NO_HOLDER" for L6 | RWB-E2-013 |
| AC-EXC-P7-019-06 | No limit covers the decision | "DOA-2026.11" holds no row for HIRE_PURCHASE | an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes | the approval is stored with status "HELD_NO_LIMIT" and the case stays "Waiting approval" And an incident is raised to RW-RISK with message MSG-P7-010 | RWB-E2-013 |
| AC-EXC-P7-019-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-019-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.19.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-019-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.20 Escalate an overdue approval

#### A2.20.1 Intent

**Business objective.** Raises an approval that has passed its service level to the named escalation point.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.20.2 Description

**Functional overview.** Raises an approval that has passed its service level to the named escalation point.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Escalate an overdue approval | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-13

#### A2.20.3 Business rules and structure

##### A2.20.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-020-1 | Approval above the approver's limit | MSG-P7-001 This needs approval at level {level}. It has been sent to {approver}. |
| BR-P7-020 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.20.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Team manager | Also uses |

#### A2.20.4 Acceptance criteria

##### A2.20.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-020-01 | Routed | a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12" and prepared by "U-9211" | the router runs for decision D7.1 at 09:00 on 14 December 2026 | an approval appears in the queue of role RW-LITOFF with decision D7.1, area "LITIGATION", no amount limit and due at 09:00 on 15 December 2026 And it is not shown to "U-9211", who prepared it And the routing entry records rule "R-LIT-03", version "LIT-2026.12" and route parameter "rwb.approval.route.D7.1.role" And the case status becomes "Waiting approval" | RWB-E2-013 |

##### A2.20.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-020-01 | Limit changed | approval "A-1" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 was routed to L6 under "DOA-2026.11" And version "DOA-2027.01" from 1 January 2027 moves that amount to L5 | a new D6.4 approval with the same amounts routes on 2 January 2027 | the new approval goes to L5 holder "U-9202" and its entry records "DOA-2027.01" And approval "A-1" stays with L6 and "DOA-2026.11" | RWB-E2-013 |
| AC-ALT-P7-020-02 | Routed by limit | restructure officer "U-9210" prepared a settlement at a discount on case "RW-2026-000124", decision D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00, loss 20.00 percent, loss amount 480,000.00 | the router runs | the approval is assigned to L6 holder "U-9201" with the delegation row ID and version "DOA-2026.11" And GET /approvals for "U-9201" lists it with amount 2,400,000.00, level "L6" and its age | RWB-E2-013 |

##### A2.20.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-020-01 | Escalated | the approval of AC1 is still WAITING at 09:00 on 15 December 2026 | JOB-05 publishes TimerBreached for its service level timer | the approval moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026 And one entry with final call "ESCALATED" is written and "U-9213" is told with MSG-P7-011 And the case stays "Waiting approval" | RWB-E2-013 |
| AC-EXC-P7-020-02 | The preparer cannot approve | "U-9210" also holds RW-PRODHEAD at L6 as substitute | "U-9210" approves the approval of AC4 | the call is refused with status 409 and message MSG-P7-002 and the approval stays "WAITING" | RWB-E2-013 |
| AC-EXC-P7-020-03 | A change above the limit goes up | the approval of AC4 is WAITING with "U-9201" | "U-9201" changes the principal to 120,000,000.00 with coded reason "CUSTOMER_REVISED_OFFER" and approves | the call returns MSG-P7-001 with level "L5" and approver "U-9202" And the approval moves to L5 with the changed terms and status "WAITING", and no approval at L6 is recorded | RWB-E2-013 |
| AC-EXC-P7-020-04 | Refuse needs a reason | the approval of AC4 is WAITING | "U-9201" refuses it with no reason | the call is refused with status 422 and message MSG-GEN-001 for field "reason" And when "U-9201" refuses it with reason "Collateral appraisal older than one year" the status becomes "REFUSED", the entry records the reason, and the case returns to the state the rule names | RWB-E2-013 |
| AC-EXC-P7-020-05 | No holder means escalation, not a stall | the L6 row for SSME has no holder and no substitute | an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes | it is assigned to the L5 holder at once And the routing entry records reason "NO_HOLDER" for L6 | RWB-E2-013 |
| AC-EXC-P7-020-06 | No limit covers the decision | "DOA-2026.11" holds no row for HIRE_PURCHASE | an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes | the approval is stored with status "HELD_NO_LIMIT" and the case stays "Waiting approval" And an incident is raised to RW-RISK with message MSG-P7-010 | RWB-E2-013 |
| AC-EXC-P7-020-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-020-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.20.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-020-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.21 Record an override with a coded reason

#### A2.21.1 Intent

**Business objective.** Lets an authorized user take a different route from the recommendation, with the reason recorded on the decision.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.21.2 Description

**Functional overview.** Lets an authorized user take a different route from the recommendation, with the reason recorded on the decision.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and record an override with a coded reason | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-APD-02

#### A2.21.3 Business rules and structure

##### A2.21.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-021-1 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-021-2 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| VR-P7-021-3 | Override without a reason | MSG-P7-005 Enter the reason you are not following the recommendation. |
| BR-P7-021 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.21.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| decision_log_entry.case_id | The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case | uuid | No | None | No |
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | No |

##### A2.21.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Product head (Mortgage, HP, SSME), Risk and model risk officer | Also uses |

#### A2.21.4 Acceptance criteria

##### A2.21.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-021-01 | Routed | a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12" and prepared by "U-9211" | the router runs for decision D7.1 at 09:00 on 14 December 2026 | an approval appears in the queue of role RW-LITOFF with decision D7.1, area "LITIGATION", no amount limit and due at 09:00 on 15 December 2026 And it is not shown to "U-9211", who prepared it And the routing entry records rule "R-LIT-03", version "LIT-2026.12" and route parameter "rwb.approval.route.D7.1.role" And the case status becomes "Waiting approval" | RWB-E2-013 |

##### A2.21.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-021-01 | Limit changed | approval "A-1" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 was routed to L6 under "DOA-2026.11" And version "DOA-2027.01" from 1 January 2027 moves that amount to L5 | a new D6.4 approval with the same amounts routes on 2 January 2027 | the new approval goes to L5 holder "U-9202" and its entry records "DOA-2027.01" And approval "A-1" stays with L6 and "DOA-2026.11" | RWB-E2-013 |
| AC-ALT-P7-021-02 | Routed by limit | restructure officer "U-9210" prepared a settlement at a discount on case "RW-2026-000124", decision D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00, loss 20.00 percent, loss amount 480,000.00 | the router runs | the approval is assigned to L6 holder "U-9201" with the delegation row ID and version "DOA-2026.11" And GET /approvals for "U-9201" lists it with amount 2,400,000.00, level "L6" and its age | RWB-E2-013 |

##### A2.21.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-021-01 | Escalated | the approval of AC1 is still WAITING at 09:00 on 15 December 2026 | JOB-05 publishes TimerBreached for its service level timer | the approval moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026 And one entry with final call "ESCALATED" is written and "U-9213" is told with MSG-P7-011 And the case stays "Waiting approval" | RWB-E2-013 |
| AC-EXC-P7-021-02 | The preparer cannot approve | "U-9210" also holds RW-PRODHEAD at L6 as substitute | "U-9210" approves the approval of AC4 | the call is refused with status 409 and message MSG-P7-002 and the approval stays "WAITING" | RWB-E2-013 |
| AC-EXC-P7-021-03 | A change above the limit goes up | the approval of AC4 is WAITING with "U-9201" | "U-9201" changes the principal to 120,000,000.00 with coded reason "CUSTOMER_REVISED_OFFER" and approves | the call returns MSG-P7-001 with level "L5" and approver "U-9202" And the approval moves to L5 with the changed terms and status "WAITING", and no approval at L6 is recorded | RWB-E2-013 |
| AC-EXC-P7-021-04 | Refuse needs a reason | the approval of AC4 is WAITING | "U-9201" refuses it with no reason | the call is refused with status 422 and message MSG-GEN-001 for field "reason" And when "U-9201" refuses it with reason "Collateral appraisal older than one year" the status becomes "REFUSED", the entry records the reason, and the case returns to the state the rule names | RWB-E2-013 |
| AC-EXC-P7-021-05 | No holder means escalation, not a stall | the L6 row for SSME has no holder and no substitute | an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes | it is assigned to the L5 holder at once And the routing entry records reason "NO_HOLDER" for L6 | RWB-E2-013 |
| AC-EXC-P7-021-06 | No limit covers the decision | "DOA-2026.11" holds no row for HIRE_PURCHASE | an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes | the approval is stored with status "HELD_NO_LIMIT" and the case stays "Waiting approval" And an incident is raised to RW-RISK with message MSG-P7-010 | RWB-E2-013 |
| AC-EXC-P7-021-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-021-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.21.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-021-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.22 Approve demand and recall notices

#### A2.22.1 Intent

**Business objective.** Gives the first production use of approval routing: the D7.1 demand and recall notices.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.22.2 Description

**Functional overview.** Gives the first production use of approval routing: the D7.1 demand and recall notices.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and approve demand and recall notices | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, WIN

**Prerequisites.** FEAT-APD-01, FEAT-DRI-14

#### A2.22.3 Business rules and structure

##### A2.22.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-022-1 | Approval above the approver's limit | MSG-P7-001 This needs approval at level {level}. It has been sent to {approver}. |
| VR-P7-022-2 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| BR-P7-022 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.22.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| decision_log_entry.case_id | The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case | uuid | No | None | No |
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | No |

##### A2.22.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Legal counsel | Also uses |

#### A2.22.4 Acceptance criteria

##### A2.22.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-022-01 | Approve | "U-9212" opens "A-0201" on SCR-11 at 10:00 on 14 December 2026 | "U-9212" approves | notice "N-0201" moves to state "Approved" and is in the 16:00 dispatch run And the decision log entry holds the inputs reference with each input's business date, rule "R-LIT-03" version "LIT-2026.12", template "DEMAND-MTG" version 2, approver "U-9212" and decided at 10:00 And the screen shows MSG-P7-004 and state "Decided" | RWB-E2-014 |

##### A2.22.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-022-01 | Change | "U-9212" opens "A-0201" | "U-9212" picks template variant "DEMAND-MTG-B" with coded reason "TEMPLATE_VARIANT" and approves | a new notice version is generated from "DEMAND-MTG-B" and is the one approved And the entry records final call "APPROVED_CHANGED", the proposed template "DEMAND-MTG", the chosen "DEMAND-MTG-B" and the reason code And only the changed notice reaches the dispatch run | RWB-E2-014 |
| AC-ALT-P7-022-02 | Reject | "U-9212" opens "A-0201" | "U-9212" rejects with reason "Addressee is a guarantor; a guarantor notice is needed" | the approval status becomes "REFUSED" and notice "N-0201" is held with reason "REFUSED_BY_APPROVER" And a task with the reason appears in the case owner's queue And the decision log entry shows final call "REFUSED" and the reason | RWB-E2-014 |

##### A2.22.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-022-01 | The preparer cannot decide | "U-9211" also sees "A-0201" through RW-LEGAL | "U-9211" opens it | approve and reject are not shown and the screen states MSG-P7-002 And a direct POST /approvals/{approvalId}/approve by "U-9211" is refused with status 409 and message MSG-P7-002 | RWB-E2-014 |
| AC-EXC-P7-022-02 | A withdrawn template blocks approval | template "DEMAND-MTG" version 2 is withdrawn at 09:30 on 14 December 2026 | "U-9212" opens "A-0201" at 10:00 | the screen shows MSG-P6-003 and the notice is held under R-LIT-04 And an approve call is refused with status 409 and message MSG-P6-003 | RWB-E2-014 |
| AC-EXC-P7-022-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-022-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.22.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-022-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.23 Show the approval queue

#### A2.23.1 Intent

**Business objective.** Gives each approver one queue of what is waiting on them, with the limit and the age of each item.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.23.2 Description

**Functional overview.** Gives each approver one queue of what is waiting on them, with the limit and the age of each item.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Product head (Mortgage, HP, SSME) | Opens the screen and show the approval queue | Checks the role, the capability area and the scope |
| 2 | Product head (Mortgage, HP, SSME) | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-APD-01

#### A2.23.3 Business rules and structure

##### A2.23.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-023-1 | Approval above the approver's limit | MSG-P7-001 This needs approval at level {level}. It has been sent to {approver}. |
| VR-P7-023-2 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-023-3 | A decision input is past its age limit | MSG-P7-006 {input} is {days} days old, past its limit. Refresh it before you decide. |
| BR-P7-023 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.23.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| decision_log_entry.case_id | The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case | uuid | No | None | No |
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | No |

##### A2.23.3.3 Roles and permissions

| Role | Use |
|---|---|
| Product head (Mortgage, HP, SSME) | Primary |
| Case owner, Credit approval committee member | Also uses |

#### A2.23.4 Acceptance criteria

##### A2.23.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-023-01 | Routed | a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12" and prepared by "U-9211" | the router runs for decision D7.1 at 09:00 on 14 December 2026 | an approval appears in the queue of role RW-LITOFF with decision D7.1, area "LITIGATION", no amount limit and due at 09:00 on 15 December 2026 And it is not shown to "U-9211", who prepared it And the routing entry records rule "R-LIT-03", version "LIT-2026.12" and route parameter "rwb.approval.route.D7.1.role" And the case status becomes "Waiting approval" | RWB-E2-013 |

##### A2.23.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-023-01 | Limit changed | approval "A-1" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 was routed to L6 under "DOA-2026.11" And version "DOA-2027.01" from 1 January 2027 moves that amount to L5 | a new D6.4 approval with the same amounts routes on 2 January 2027 | the new approval goes to L5 holder "U-9202" and its entry records "DOA-2027.01" And approval "A-1" stays with L6 and "DOA-2026.11" | RWB-E2-013 |
| AC-ALT-P7-023-02 | Routed by limit | restructure officer "U-9210" prepared a settlement at a discount on case "RW-2026-000124", decision D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00, loss 20.00 percent, loss amount 480,000.00 | the router runs | the approval is assigned to L6 holder "U-9201" with the delegation row ID and version "DOA-2026.11" And GET /approvals for "U-9201" lists it with amount 2,400,000.00, level "L6" and its age | RWB-E2-013 |

##### A2.23.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-023-01 | Escalated | the approval of AC1 is still WAITING at 09:00 on 15 December 2026 | JOB-05 publishes TimerBreached for its service level timer | the approval moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026 And one entry with final call "ESCALATED" is written and "U-9213" is told with MSG-P7-011 And the case stays "Waiting approval" | RWB-E2-013 |
| AC-EXC-P7-023-02 | The preparer cannot approve | "U-9210" also holds RW-PRODHEAD at L6 as substitute | "U-9210" approves the approval of AC4 | the call is refused with status 409 and message MSG-P7-002 and the approval stays "WAITING" | RWB-E2-013 |
| AC-EXC-P7-023-03 | A change above the limit goes up | the approval of AC4 is WAITING with "U-9201" | "U-9201" changes the principal to 120,000,000.00 with coded reason "CUSTOMER_REVISED_OFFER" and approves | the call returns MSG-P7-001 with level "L5" and approver "U-9202" And the approval moves to L5 with the changed terms and status "WAITING", and no approval at L6 is recorded | RWB-E2-013 |
| AC-EXC-P7-023-04 | Refuse needs a reason | the approval of AC4 is WAITING | "U-9201" refuses it with no reason | the call is refused with status 422 and message MSG-GEN-001 for field "reason" And when "U-9201" refuses it with reason "Collateral appraisal older than one year" the status becomes "REFUSED", the entry records the reason, and the case returns to the state the rule names | RWB-E2-013 |
| AC-EXC-P7-023-05 | No holder means escalation, not a stall | the L6 row for SSME has no holder and no substitute | an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes | it is assigned to the L5 holder at once And the routing entry records reason "NO_HOLDER" for L6 | RWB-E2-013 |
| AC-EXC-P7-023-06 | No limit covers the decision | "DOA-2026.11" holds no row for HIRE_PURCHASE | an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes | the approval is stored with status "HELD_NO_LIMIT" and the case stays "Waiting approval" And an incident is raised to RW-RISK with message MSG-P7-010 | RWB-E2-013 |
| AC-EXC-P7-023-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-023-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.23.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-023-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.24 Apply the delegation of authority limits

#### A2.24.1 Intent

**Business objective.** Reads the limits from the versioned table at the moment of the decision, and records the version used.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.24.2 Description

**Functional overview.** Reads the limits from the versioned table at the moment of the decision, and records the version used.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Apply the delegation of authority limits | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-ACA-06

#### A2.24.3 Business rules and structure

##### A2.24.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-024-1 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-024-2 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| VR-P7-024-3 | A decision input is past its age limit | MSG-P7-006 {input} is {days} days old, past its limit. Refresh it before you decide. |
| BR-P7-024 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.24.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Security administrator | Also uses |

#### A2.24.4 Acceptance criteria

##### A2.24.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-024-01 | Table loaded | the delegation of authority file "DOA-2026.11" built from Regulation กกค.540031 as amended by กกค.690070, with 95 limits | "U-3101" loads it with table "delegation_limit" and validFrom "2026-11-30" and "U-3102" approves it | 218 rows are stored: 109 decision and limit rows for MORTGAGE and 109 for SSME And every row has a decision code, an approval level and a product, and no two rows repeat the same decision, regulation item, product, level and limits And item 2.1.1 at level L4 is stored as two rows: principal 300,000,000.00 with loss up to 45.00 percent and maximum loss 150,000,000.00, and principal 50,000,000.00 with no loss limit | RWB-E1-038 |

##### A2.24.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-024-01 | Lookup | "DOA-2026.11" is in force | the router asks who may approve decision D6.4, item 2.1.1, product MORTGAGE, principal 2,400,000.00, loss 20.00 percent and loss amount 480,000.00 on 15 December 2026 | the lookup returns level L6, the row ID of item 2.1.1 at L6 and version "DOA-2026.11" | RWB-E1-038 |
| AC-ALT-P7-024-02 | Change | "DOA-2026.11" is in force And file "DOA-2027.01" adds a row for item 2.1.5 at level L5 with principal up to 10,000,000.00, validFrom "2027-01-01" | "U-3101" loads it and "U-3102" approves it | the rows of "DOA-2026.11" stay readable with valid_to "2026-12-31" And a lookup for D6.6, item 2.1.5, MORTGAGE, principal 8,000,000.00 dated 2 January 2027 returns L5 and version "DOA-2027.01" And one decision log entry records the approval of "DOA-2027.01" with its valid from date | RWB-E1-038 |

##### A2.24.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-024-01 | A file with an error is refused whole | file "DOA-2026.12" gives item 2.1.1 at L5 a principal limit of 400,000,000.00, above the 300,000,000.00 of L4 And it gives one row the decision code "D6.9" | "U-3101" loads it | the load is refused with message MSG-P1-002 naming the falling limit and the unknown decision code And no row of "DOA-2026.12" is stored and "DOA-2026.11" stays in force | RWB-E1-038 |
| AC-EXC-P7-024-02 | The loader cannot approve and only Risk may | load "DOA-2027.01" was loaded by "U-3101" | "U-3101" calls approve on it | the call is refused with message MSG-P7-002 And when test user "U-3103" holding RW-PRODHEAD calls approve on it the call is refused with status 403 and message MSG-P4-002 | RWB-E1-038 |
| AC-EXC-P7-024-03 | An approval that cannot be recorded does not take effect | the decision log store is unavailable | "U-3102" approves load "DOA-2027.01" | the call returns status 503 with message MSG-P7-003 and the load stays "Loaded" | RWB-E1-038 |
| AC-EXC-P7-024-04 | No limit covers the request | "DOA-2026.11" holds no row for product HIRE_PURCHASE | the router asks who may approve decision D6.4, item 2.1.1, for HIRE_PURCHASE, principal 900,000.00 | the lookup returns "NOT_COVERED" And an incident is raised to the RW-RISK queue with message MSG-P7-010 naming D6.4 and HIRE_PURCHASE | RWB-E1-038 |
| AC-EXC-P7-024-05 | A write-off for a related party goes to the Board | "DOA-2026.11" is in force | the router asks who may approve decision D9.2, item 2.1.10, criteria met, product SSME, principal 300,000.00, with related party flag true | the lookup returns level L1 with reason "RELATED_PARTY" | RWB-E1-038 |
| AC-EXC-P7-024-06 | Escalated | the approval of AC1 is still WAITING at 09:00 on 15 December 2026 | JOB-05 publishes TimerBreached for its service level timer | the approval moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026 And one entry with final call "ESCALATED" is written and "U-9213" is told with MSG-P7-011 And the case stays "Waiting approval" | RWB-E2-013 |
| AC-EXC-P7-024-07 | The preparer cannot approve | "U-9210" also holds RW-PRODHEAD at L6 as substitute | "U-9210" approves the approval of AC4 | the call is refused with status 409 and message MSG-P7-002 and the approval stays "WAITING" | RWB-E2-013 |
| AC-EXC-P7-024-08 | A change above the limit goes up | the approval of AC4 is WAITING with "U-9201" | "U-9201" changes the principal to 120,000,000.00 with coded reason "CUSTOMER_REVISED_OFFER" and approves | the call returns MSG-P7-001 with level "L5" and approver "U-9202" And the approval moves to L5 with the changed terms and status "WAITING", and no approval at L6 is recorded | RWB-E2-013 |
| AC-EXC-P7-024-09 | Refuse needs a reason | the approval of AC4 is WAITING | "U-9201" refuses it with no reason | the call is refused with status 422 and message MSG-GEN-001 for field "reason" And when "U-9201" refuses it with reason "Collateral appraisal older than one year" the status becomes "REFUSED", the entry records the reason, and the case returns to the state the rule names | RWB-E2-013 |
| AC-EXC-P7-024-10 | No holder means escalation, not a stall | the L6 row for SSME has no holder and no substitute | an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes | it is assigned to the L5 holder at once And the routing entry records reason "NO_HOLDER" for L6 | RWB-E2-013 |
| AC-EXC-P7-024-11 | No limit covers the decision | "DOA-2026.11" holds no row for HIRE_PURCHASE | an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes | the approval is stored with status "HELD_NO_LIMIT" and the case stays "Waiting approval" And an incident is raised to RW-RISK with message MSG-P7-010 | RWB-E2-013 |
| AC-EXC-P7-024-12 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-024-13 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.24.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-024-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.25 Record the outcome of an approved decision

#### A2.25.1 Intent

**Business objective.** Writes the result of the decision back to the log: what was done, by which system, and when.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.25.2 Description

**Functional overview.** Writes the result of the decision back to the log: what was done, by which system, and when.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Record the outcome of an approved decision | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-DRI-02

#### A2.25.3 Business rules and structure

##### A2.25.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-025-1 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-025-2 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| VR-P7-025-3 | A decision input is past its age limit | MSG-P7-006 {input} is {days} days old, past its limit. Refresh it before you decide. |
| BR-P7-025 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.25.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Internal audit | Also uses |

#### A2.25.4 Acceptance criteria

##### A2.25.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-025-01 | Routed | a demand notice for case "RW-2026-000123" was generated under rule "R-LIT-03" version "LIT-2026.12" and prepared by "U-9211" | the router runs for decision D7.1 at 09:00 on 14 December 2026 | an approval appears in the queue of role RW-LITOFF with decision D7.1, area "LITIGATION", no amount limit and due at 09:00 on 15 December 2026 And it is not shown to "U-9211", who prepared it And the routing entry records rule "R-LIT-03", version "LIT-2026.12" and route parameter "rwb.approval.route.D7.1.role" And the case status becomes "Waiting approval" | RWB-E2-013 |

##### A2.25.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-025-01 | Limit changed | approval "A-1" for D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00 was routed to L6 under "DOA-2026.11" And version "DOA-2027.01" from 1 January 2027 moves that amount to L5 | a new D6.4 approval with the same amounts routes on 2 January 2027 | the new approval goes to L5 holder "U-9202" and its entry records "DOA-2027.01" And approval "A-1" stays with L6 and "DOA-2026.11" | RWB-E2-013 |
| AC-ALT-P7-025-02 | Routed by limit | restructure officer "U-9210" prepared a settlement at a discount on case "RW-2026-000124", decision D6.4 item 2.1.1, MORTGAGE, principal 2,400,000.00, loss 20.00 percent, loss amount 480,000.00 | the router runs | the approval is assigned to L6 holder "U-9201" with the delegation row ID and version "DOA-2026.11" And GET /approvals for "U-9201" lists it with amount 2,400,000.00, level "L6" and its age | RWB-E2-013 |

##### A2.25.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-025-01 | Escalated | the approval of AC1 is still WAITING at 09:00 on 15 December 2026 | JOB-05 publishes TimerBreached for its service level timer | the approval moves to role RW-HEADLIT with escalation level 1 and a new due time of 09:00 on 16 December 2026 And one entry with final call "ESCALATED" is written and "U-9213" is told with MSG-P7-011 And the case stays "Waiting approval" | RWB-E2-013 |
| AC-EXC-P7-025-02 | The preparer cannot approve | "U-9210" also holds RW-PRODHEAD at L6 as substitute | "U-9210" approves the approval of AC4 | the call is refused with status 409 and message MSG-P7-002 and the approval stays "WAITING" | RWB-E2-013 |
| AC-EXC-P7-025-03 | A change above the limit goes up | the approval of AC4 is WAITING with "U-9201" | "U-9201" changes the principal to 120,000,000.00 with coded reason "CUSTOMER_REVISED_OFFER" and approves | the call returns MSG-P7-001 with level "L5" and approver "U-9202" And the approval moves to L5 with the changed terms and status "WAITING", and no approval at L6 is recorded | RWB-E2-013 |
| AC-EXC-P7-025-04 | Refuse needs a reason | the approval of AC4 is WAITING | "U-9201" refuses it with no reason | the call is refused with status 422 and message MSG-GEN-001 for field "reason" And when "U-9201" refuses it with reason "Collateral appraisal older than one year" the status becomes "REFUSED", the entry records the reason, and the case returns to the state the rule names | RWB-E2-013 |
| AC-EXC-P7-025-05 | No holder means escalation, not a stall | the L6 row for SSME has no holder and no substitute | an approval for D6.4 item 2.1.1, SSME, principal 1,000,000.00, loss 10.00 percent routes | it is assigned to the L5 holder at once And the routing entry records reason "NO_HOLDER" for L6 | RWB-E2-013 |
| AC-EXC-P7-025-06 | No limit covers the decision | "DOA-2026.11" holds no row for HIRE_PURCHASE | an approval for D6.4 item 2.1.1, HIRE_PURCHASE, principal 900,000.00 routes | the approval is stored with status "HELD_NO_LIMIT" and the case stays "Waiting approval" And an incident is raised to RW-RISK with message MSG-P7-010 | RWB-E2-013 |
| AC-EXC-P7-025-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-025-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.25.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-025-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.26 Write every Workbench event to the ledger

#### A2.26.1 Intent

**Business objective.** Captures case created, allocated, transferred, escalated, document attached and decision taken as ledger entries as they happen.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.26.2 Description

**Functional overview.** Captures case created, allocated, transferred, escalated, document attached and decision taken as ledger entries as they happen.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Write every Workbench event to the ledger | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-DRI-02

#### A2.26.3 Business rules and structure

##### A2.26.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-026-1 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-026-2 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| VR-P7-026-3 | A decision input is past its age limit | MSG-P7-006 {input} is {days} days old, past its limit. Refresh it before you decide. |
| BR-P7-026 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.26.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.26.4 Acceptance criteria

##### A2.26.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-026-01 | The ledger exists and is written to | the case owner records an outbound call on 2026-12-02 at 10:15 with result RIGHT_PARTY and a promise of 25,000.00 baht for 2026-12-15 | the action completes | the ledger holds entry case_seq 7 for case "RW-2026-000201" with event "CONTACT", occurred at 2026-12-02T10:15+07:00, actor "u-owner-02", channel "CALL" and direction "OUTBOUND" And the entry carries promise amount 25,000.00 and promise date 2026-12-15 And the entry names source system "WORKBENCH" | RWB-E1-066 |

##### A2.26.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-026-01 | It is ordered and complete | case "RW-2026-000201" has 4 EFS history entries from 2026-08-03 to 2026-11-28, a CASE_CREATED entry on 2026-12-01 and a CASE_ALLOCATED entry on 2026-12-01 | the ledger is read | the 6 entries are in one sequence ordered by occurred time And case_seq runs 1 to 6 with no gap | RWB-E1-066 |
| AC-ALT-P7-026-02 | It is distinct from the decision log | owner reassignment of case "RW-2026-000201" was decided under rule "R-UNI-18" version "2026.11" by approver "u-teammgr-01" | both are read | the decision log entry holds decision code "D6", rule "R-UNI-18", version "2026.11", the inputs reference and the approver And the ledger entry holds event "DECISION_TAKEN", the time, the actor and the decision log entry ID, with no rule, version or inputs | RWB-E1-066 |

##### A2.26.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-026-01 | A write failure is visible | the ledger insert fails with a database error | the case owner records a call on case "RW-2026-000201" | the call is refused with status 503 and MSG-P1-022 And the ledger still holds 6 entries and no contact is saved And an incident "LEDGER_WRITE_FAILED" is raised with case "RW-2026-000201" | RWB-E1-066 |
| AC-EXC-P7-026-02 | A required value is missing | None | a service calls append() for case "RW-2026-000201" with no event code | the call is refused with MSG-GEN-001 for field "event code" And no entry is written | RWB-E1-066 |
| AC-EXC-P7-026-03 | A case that does not exist | None | the case owner posts an interaction for case ID "00000000-0000-0000-0000-000000000999" | the call is refused with status 404 and MSG-P4-003 And no entry is written | RWB-E1-066 |
| AC-EXC-P7-026-04 | An entry cannot be changed | ledger entry case_seq 3 of case "RW-2026-000201" | any process issues an UPDATE or DELETE on it | the database refuses the statement And a correction is written as a new entry with event "CORRECTION" naming entry case_seq 3 | RWB-E1-066 |
| AC-EXC-P7-026-05 | The ledger write fails for an event | every ledger insert fails | DocumentStored for case "RW-2026-000301" is delivered | the delivery is tried 4 times in all And the event is in the exception queue with owner RW-PLATADM And incident "LEDGER_WRITE_FAILED" is raised for case "RW-2026-000301" | RWB-E1-067 |
| AC-EXC-P7-026-06 | An event for a case that does not exist | None | DocumentStored arrives for case ID "00000000-0000-0000-0000-000000000998" | no entry is written And the event is in the exception queue with reason "case not found" | RWB-E1-067 |
| AC-EXC-P7-026-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-026-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.26.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-026-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.27 Hold the ledger beside the decision log

#### A2.27.1 Intent

**Business objective.** An append-only store sharing infrastructure with the decision log, with its own retention. The decision log says why the system acted; the ledger says what happened with the customer.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.27.2 Description

**Functional overview.** An append-only store sharing infrastructure with the decision log, with its own retention. The decision log says why the system acted; the ledger says what happened with the customer.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Hold the ledger beside the decision log | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, ACE database

**Prerequisites.** FEAT-DRI-02

#### A2.27.3 Business rules and structure

##### A2.27.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-027-1 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-027-2 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| VR-P7-027-3 | A decision input is past its age limit | MSG-P7-006 {input} is {days} days old, past its limit. Refresh it before you decide. |
| BR-P7-027 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.27.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Internal audit, Compliance and PDPA officer | Also uses |

#### A2.27.4 Acceptance criteria

##### A2.27.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-027-01 | The ledger exists and is written to | the case owner records an outbound call on 2026-12-02 at 10:15 with result RIGHT_PARTY and a promise of 25,000.00 baht for 2026-12-15 | the action completes | the ledger holds entry case_seq 7 for case "RW-2026-000201" with event "CONTACT", occurred at 2026-12-02T10:15+07:00, actor "u-owner-02", channel "CALL" and direction "OUTBOUND" And the entry carries promise amount 25,000.00 and promise date 2026-12-15 And the entry names source system "WORKBENCH" | RWB-E1-066 |

##### A2.27.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-027-01 | It is ordered and complete | case "RW-2026-000201" has 4 EFS history entries from 2026-08-03 to 2026-11-28, a CASE_CREATED entry on 2026-12-01 and a CASE_ALLOCATED entry on 2026-12-01 | the ledger is read | the 6 entries are in one sequence ordered by occurred time And case_seq runs 1 to 6 with no gap | RWB-E1-066 |
| AC-ALT-P7-027-02 | It is distinct from the decision log | owner reassignment of case "RW-2026-000201" was decided under rule "R-UNI-18" version "2026.11" by approver "u-teammgr-01" | both are read | the decision log entry holds decision code "D6", rule "R-UNI-18", version "2026.11", the inputs reference and the approver And the ledger entry holds event "DECISION_TAKEN", the time, the actor and the decision log entry ID, with no rule, version or inputs | RWB-E1-066 |

##### A2.27.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-027-01 | A write failure is visible | the ledger insert fails with a database error | the case owner records a call on case "RW-2026-000201" | the call is refused with status 503 and MSG-P1-022 And the ledger still holds 6 entries and no contact is saved And an incident "LEDGER_WRITE_FAILED" is raised with case "RW-2026-000201" | RWB-E1-066 |
| AC-EXC-P7-027-02 | A required value is missing | None | a service calls append() for case "RW-2026-000201" with no event code | the call is refused with MSG-GEN-001 for field "event code" And no entry is written | RWB-E1-066 |
| AC-EXC-P7-027-03 | A case that does not exist | None | the case owner posts an interaction for case ID "00000000-0000-0000-0000-000000000999" | the call is refused with status 404 and MSG-P4-003 And no entry is written | RWB-E1-066 |
| AC-EXC-P7-027-04 | An entry cannot be changed | ledger entry case_seq 3 of case "RW-2026-000201" | any process issues an UPDATE or DELETE on it | the database refuses the statement And a correction is written as a new entry with event "CORRECTION" naming entry case_seq 3 | RWB-E1-066 |
| AC-EXC-P7-027-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-027-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.27.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-027-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.28 Read the ledger in one ordered sequence

#### A2.28.1 Intent

**Business objective.** A read interface returning a case's entries in order with their source named, filterable by channel, actor and date range.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.28.2 Description

**Functional overview.** A read interface returning a case's entries in order with their source named, filterable by channel, actor and date range.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Read the ledger in one ordered sequence | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-ILG-02

#### A2.28.3 Business rules and structure

##### A2.28.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-028-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P7-028 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.28.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner, Conduct and QA officer | Also uses |

#### A2.28.4 Acceptance criteria

##### A2.28.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-028-01 | The ledger reads in order | a case with entries from several sources | user "u-owner-04" calls GET /cases/{caseId}/interactions for case "RW-2026-000401" | 9 entries come back ordered by occurred time, earliest first And each entry names its source system and source reference, for example "EFS, `v_ace_efs_action`" or "WORKBENCH, P3 case and workflow" | RWB-E1-068 |

##### A2.28.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-028-01 | It can be filtered | the 9-entry ledger | it is read three times: filtered by channel "CALL", by actor "u-owner-04", and from 2026-12-01 to 2026-12-06 | the first read returns only the 3 EFS call entries And the second read returns only the 2 VISIT entries And the third read returns only the 4 Workbench entries | RWB-E1-068 |
| AC-ALT-P7-028-02 | It is available to the case record | the case record view SCR-03 for case "RW-2026-000401" | it loads | its history panel shows the 9 entries from GET /cases/{caseId}/interactions And the architecture test finds no class outside the ledger package that queries the interaction table | RWB-E1-068 |

##### A2.28.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-028-01 | Summary masked when no masking rule allows it | no masking rule from Compliance is loaded for interaction.summary | user "u-owner-04" reads the ledger | the summary of each entry is returned as "MASKED" And the channel, result, promise amount and promise date are returned in full | RWB-E1-068 |
| AC-EXC-P7-028-02 | Page size at and above the limit | None | the case owner reads once with size 200 and once with size 201 | the read with size 200 returns the 9 entries with size 200 And the read with size 201 is refused with status 422 and MSG-GEN-002 for "size" between 1 and 200 | RWB-E1-068 |
| AC-EXC-P7-028-03 | A case with no entries | case "RW-2026-000402" has no ledger entries | its owner reads the ledger | the response holds 0 items and total 0 And the history panel shows the Empty state | RWB-E1-068 |
| AC-EXC-P7-028-04 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-028-05 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.28.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-028-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.29 Reject a duplicate ledger entry

#### A2.29.1 Intent

**Business objective.** The same event arriving twice with the same key produces one entry, and the repeat is counted.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.29.2 Description

**Functional overview.** The same event arriving twice with the same key produces one entry, and the repeat is counted.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Reject a duplicate ledger entry | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-ILG-01

#### A2.29.3 Business rules and structure

##### A2.29.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-029-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P7-029 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.29.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.29.4 Acceptance criteria

##### A2.29.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-029-01 | Workbench events are captured | the case is created at 2026-12-01T06:10+07:00 by SY-CASEWF And allocated to queue "MTG-BKK-CO" at 06:40 by SY-RULES And transferred by user "u-teammgr-03" at 2026-12-03T14:05+07:00 And has document "DOC-SYN-3011" attached at 2026-12-04T09:30+07:00 by SY-OCR And has timer "SLA-ASSIGNED" breached at 2026-12-05T08:00+07:00 And has decision log entry "DLE-SYN-3012" recorded at 2026-12-05T11:20+07:00 | each action completes | the ledger holds 6 entries for the case with events CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, DOCUMENT_ATTACHED, CASE_ESCALATED and DECISION_TAKEN And each entry carries the case identifier, the event, the timestamp and the actor | RWB-E1-067 |

##### A2.29.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-029-01 | The entry names its source | the CASE_ALLOCATED entry of case "RW-2026-000301" | it is read | it names source system "WORKBENCH", source reference "P3 case and workflow, EV-02 CaseAllocated" and actor "SY-RULES" And the CASE_TRANSFERRED entry names actor type "USER" and actor "u-teammgr-03" | RWB-E1-067 |
| AC-ALT-P7-029-02 | Nothing is written twice | CaseAllocated for case "RW-2026-000301" with idempotency key "EV-02-RW-2026-000301-20261201" was written to the ledger | the same event arrives again with the same key | one CASE_ALLOCATED entry exists And the hit count for key "EV-02-RW-2026-000301-20261201" is 1 | RWB-E1-067 |

##### A2.29.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-029-01 | The ledger write fails for an event | every ledger insert fails | DocumentStored for case "RW-2026-000301" is delivered | the delivery is tried 4 times in all And the event is in the exception queue with owner RW-PLATADM And incident "LEDGER_WRITE_FAILED" is raised for case "RW-2026-000301" | RWB-E1-067 |
| AC-EXC-P7-029-02 | An event for a case that does not exist | None | DocumentStored arrives for case ID "00000000-0000-0000-0000-000000000998" | no entry is written And the event is in the exception queue with reason "case not found" | RWB-E1-067 |
| AC-EXC-P7-029-03 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-029-04 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.29.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-029-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.30 Raise an incident when the ledger cannot be written

#### A2.30.1 Intent

**Business objective.** A ledger write failure raises an incident rather than being discarded, so the history never has a silent gap.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.30.2 Description

**Functional overview.** A ledger write failure raises an incident rather than being discarded, so the history never has a silent gap.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Raise an incident when the ledger cannot be written | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-ILG-01

#### A2.30.3 Business rules and structure

##### A2.30.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-030-1 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-030-2 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| VR-P7-030-3 | An action outside the role's permission | MSG-P4-002 You cannot {action} here. Your role does not include it. |
| BR-P7-030 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.30.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Platform administrator | Also uses |

#### A2.30.4 Acceptance criteria

##### A2.30.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-030-01 | The ledger exists and is written to | the case owner records an outbound call on 2026-12-02 at 10:15 with result RIGHT_PARTY and a promise of 25,000.00 baht for 2026-12-15 | the action completes | the ledger holds entry case_seq 7 for case "RW-2026-000201" with event "CONTACT", occurred at 2026-12-02T10:15+07:00, actor "u-owner-02", channel "CALL" and direction "OUTBOUND" And the entry carries promise amount 25,000.00 and promise date 2026-12-15 And the entry names source system "WORKBENCH" | RWB-E1-066 |

##### A2.30.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-030-01 | It is ordered and complete | case "RW-2026-000201" has 4 EFS history entries from 2026-08-03 to 2026-11-28, a CASE_CREATED entry on 2026-12-01 and a CASE_ALLOCATED entry on 2026-12-01 | the ledger is read | the 6 entries are in one sequence ordered by occurred time And case_seq runs 1 to 6 with no gap | RWB-E1-066 |
| AC-ALT-P7-030-02 | It is distinct from the decision log | owner reassignment of case "RW-2026-000201" was decided under rule "R-UNI-18" version "2026.11" by approver "u-teammgr-01" | both are read | the decision log entry holds decision code "D6", rule "R-UNI-18", version "2026.11", the inputs reference and the approver And the ledger entry holds event "DECISION_TAKEN", the time, the actor and the decision log entry ID, with no rule, version or inputs | RWB-E1-066 |

##### A2.30.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-030-01 | A write failure is visible | the ledger insert fails with a database error | the case owner records a call on case "RW-2026-000201" | the call is refused with status 503 and MSG-P1-022 And the ledger still holds 6 entries and no contact is saved And an incident "LEDGER_WRITE_FAILED" is raised with case "RW-2026-000201" | RWB-E1-066 |
| AC-EXC-P7-030-02 | A required value is missing | None | a service calls append() for case "RW-2026-000201" with no event code | the call is refused with MSG-GEN-001 for field "event code" And no entry is written | RWB-E1-066 |
| AC-EXC-P7-030-03 | A case that does not exist | None | the case owner posts an interaction for case ID "00000000-0000-0000-0000-000000000999" | the call is refused with status 404 and MSG-P4-003 And no entry is written | RWB-E1-066 |
| AC-EXC-P7-030-04 | An entry cannot be changed | ledger entry case_seq 3 of case "RW-2026-000201" | any process issues an UPDATE or DELETE on it | the database refuses the statement And a correction is written as a new entry with event "CORRECTION" naming entry case_seq 3 | RWB-E1-066 |
| AC-EXC-P7-030-05 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-030-06 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.30.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-030-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.31 Bring contact outcomes into the ledger

#### A2.31.1 Intent

**Business objective.** Contact attempts and their outcomes from EFS are written to the ledger with channel, time and who was reached.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.31.2 Description

**Functional overview.** Contact attempts and their outcomes from EFS are written to the ledger with channel, time and who was reached.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Bring contact outcomes into the ledger | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** EFS, Workbench

**Prerequisites.** FEAT-ILG-01

#### A2.31.3 Business rules and structure

##### A2.31.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-031-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P7-031 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.31.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner, Phone collector | Also uses |

#### A2.31.4 Acceptance criteria

##### A2.31.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-031-01 | An interaction is recorded | `v_ace_efs_action` for business date 14 December 2026 holds an EFS action for account "ACC-SYN-0301" with action code "PTP", call result RIGHT_PARTY, contact time 14 December 2026 10:15, promise amount 12,500.00 and promise date 20 December 2026 And case owner "U-2001" records a call on 15 December 2026 09:30 to contact point "CP-SYN-0301-M" with result NO_ANSWER | the ACE batch for source EFS completes and the call is saved | the ledger holds a CONTACT entry with source EFS, channel CALL, occurred 14 December 2026 10:15, result RIGHT_PARTY, promise 12,500.00 for 20 December 2026 and retention class "ILG-STD" And the ledger holds a CONTACT entry with source WORKBENCH, channel CALL, occurred 15 December 2026 09:30, contact point "CP-SYN-0301-M" and result NO_ANSWER | RWB-E2-034 |

##### A2.31.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-031-01 | A hand-over is recorded | case "RW-2026-000301" is transferred from "U-2001" to "U-2002" on 16 December 2026 11:00 And instruction "INS-SYN-0301" is issued to partner "LF-SYN-01" on 17 December 2026 14:00 | both moves complete | the CASE_TRANSFERRED entry of 16 December 2026 11:00 holds from "USER:U-2001" and to "USER:U-2002" And the ledger holds a HANDOVER entry with channel PORTAL, direction OUTBOUND, from "USER:U-2002", to "PARTNER:LF-SYN-01", occurred 17 December 2026 14:00 | RWB-E2-034 |
| AC-ALT-P7-031-02 | The ledger is one place | the EFS entry of 14 December 2026, the Workbench call of 15 December 2026 and a partner result from "LF-SYN-01" entered in the partner portal on 18 December 2026 16:00 | the case is read | GET /cases/{caseId}/interactions returns the 3 entries in the order 14, 15 and 18 December 2026 And each entry names its source: EFS, WORKBENCH, and WORKBENCH with channel PORTAL and event code PARTNER_RESULT | RWB-E2-034 |

##### A2.31.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-031-01 | EFS rows outside the list or outside a case are not written | the `v_ace_efs_action` rows for 14 December 2026 hold 3 rows: action code "PTP" for "ACC-SYN-0301", action code "SYS" not on the list for "ACC-SYN-0301", and action code "PTP" for account "ACC-SYN-0999" on no open case | the ACE batch for source EFS completes | the ledger holds 1 new EFS entry And the import summary shows 3 read, 1 written, 1 excluded by the outcome list and 1 not on a case | RWB-E2-034 |
| AC-EXC-P7-031-02 | A ledger write failure loses nothing | the ledger store is unavailable | event NoticeDispatched for "NT-SYN-0301" is delivered the ledger store is available again and the outbox retries | no entry is written, the delivery stays in the outbox with status RETRYING and an incident is raised When the ledger store is available again and the outbox retries the ledger holds one LETTER entry for "NT-SYN-0301" | RWB-E2-034 |
| AC-EXC-P7-031-03 | An event for an unknown case goes to the exception queue | event InstructionIssued names an instruction whose case does not exist | the outbox has retried the delivery 3 times | no entry is written And the delivery is in the exception queue with a task for role RW-PLATADM | RWB-E2-034 |
| AC-EXC-P7-031-04 | A late EFS row reads in time order | the ledger holds the Workbench call of 15 December 2026 09:30 | the EFS row with contact time 14 December 2026 10:15 is processed on 15 December 2026 at 10:00 | the timeline shows the EFS entry before the call | RWB-E2-034 |
| AC-EXC-P7-031-05 | A case with no entry | open case "RW-2026-000302" with no ledger entry | the case owner opens the timeline | the timeline shows the empty state with message MSG-P3-024 | RWB-E2-034 |
| AC-EXC-P7-031-06 | A case outside the reader's scope is refused | case "RW-2026-000301" is owned by "U-2002" in team "MTG-BKK" | case owner "U-3001" of team "HP-NE" with Own scope reads its ledger | the response is 404 with message MSG-P4-003 | RWB-E2-034 |
| AC-EXC-P7-031-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-031-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.31.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-031-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.32 Bring dispatch outcomes into the ledger

#### A2.32.1 Intent

**Business objective.** Letter, SMS and LINE dispatch, and proof of delivery, are written to the ledger.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.32.2 Description

**Functional overview.** Letter, SMS and LINE dispatch, and proof of delivery, are written to the ledger.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Bring dispatch outcomes into the ledger | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** WIN, NSS, LINE OA, Workbench

**Prerequisites.** FEAT-ILG-01

#### A2.32.3 Business rules and structure

##### A2.32.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-032-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P7-032 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.32.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.32.4 Acceptance criteria

##### A2.32.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-032-01 | An interaction is recorded | `v_ace_efs_action` for business date 14 December 2026 holds an EFS action for account "ACC-SYN-0301" with action code "PTP", call result RIGHT_PARTY, contact time 14 December 2026 10:15, promise amount 12,500.00 and promise date 20 December 2026 And case owner "U-2001" records a call on 15 December 2026 09:30 to contact point "CP-SYN-0301-M" with result NO_ANSWER | the ACE batch for source EFS completes and the call is saved | the ledger holds a CONTACT entry with source EFS, channel CALL, occurred 14 December 2026 10:15, result RIGHT_PARTY, promise 12,500.00 for 20 December 2026 and retention class "ILG-STD" And the ledger holds a CONTACT entry with source WORKBENCH, channel CALL, occurred 15 December 2026 09:30, contact point "CP-SYN-0301-M" and result NO_ANSWER | RWB-E2-034 |

##### A2.32.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-032-01 | A hand-over is recorded | case "RW-2026-000301" is transferred from "U-2001" to "U-2002" on 16 December 2026 11:00 And instruction "INS-SYN-0301" is issued to partner "LF-SYN-01" on 17 December 2026 14:00 | both moves complete | the CASE_TRANSFERRED entry of 16 December 2026 11:00 holds from "USER:U-2001" and to "USER:U-2002" And the ledger holds a HANDOVER entry with channel PORTAL, direction OUTBOUND, from "USER:U-2002", to "PARTNER:LF-SYN-01", occurred 17 December 2026 14:00 | RWB-E2-034 |
| AC-ALT-P7-032-02 | The ledger is one place | the EFS entry of 14 December 2026, the Workbench call of 15 December 2026 and a partner result from "LF-SYN-01" entered in the partner portal on 18 December 2026 16:00 | the case is read | GET /cases/{caseId}/interactions returns the 3 entries in the order 14, 15 and 18 December 2026 And each entry names its source: EFS, WORKBENCH, and WORKBENCH with channel PORTAL and event code PARTNER_RESULT | RWB-E2-034 |

##### A2.32.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-032-01 | EFS rows outside the list or outside a case are not written | the `v_ace_efs_action` rows for 14 December 2026 hold 3 rows: action code "PTP" for "ACC-SYN-0301", action code "SYS" not on the list for "ACC-SYN-0301", and action code "PTP" for account "ACC-SYN-0999" on no open case | the ACE batch for source EFS completes | the ledger holds 1 new EFS entry And the import summary shows 3 read, 1 written, 1 excluded by the outcome list and 1 not on a case | RWB-E2-034 |
| AC-EXC-P7-032-02 | A ledger write failure loses nothing | the ledger store is unavailable | event NoticeDispatched for "NT-SYN-0301" is delivered the ledger store is available again and the outbox retries | no entry is written, the delivery stays in the outbox with status RETRYING and an incident is raised When the ledger store is available again and the outbox retries the ledger holds one LETTER entry for "NT-SYN-0301" | RWB-E2-034 |
| AC-EXC-P7-032-03 | An event for an unknown case goes to the exception queue | event InstructionIssued names an instruction whose case does not exist | the outbox has retried the delivery 3 times | no entry is written And the delivery is in the exception queue with a task for role RW-PLATADM | RWB-E2-034 |
| AC-EXC-P7-032-04 | A late EFS row reads in time order | the ledger holds the Workbench call of 15 December 2026 09:30 | the EFS row with contact time 14 December 2026 10:15 is processed on 15 December 2026 at 10:00 | the timeline shows the EFS entry before the call | RWB-E2-034 |
| AC-EXC-P7-032-05 | A case with no entry | open case "RW-2026-000302" with no ledger entry | the case owner opens the timeline | the timeline shows the empty state with message MSG-P3-024 | RWB-E2-034 |
| AC-EXC-P7-032-06 | A case outside the reader's scope is refused | case "RW-2026-000301" is owned by "U-2002" in team "MTG-BKK" | case owner "U-3001" of team "HP-NE" with Own scope reads its ledger | the response is 404 with message MSG-P4-003 | RWB-E2-034 |
| AC-EXC-P7-032-07 | Consent withdrawn does not stop a statutory notice | the borrower's postal address contact point has consent status "WITHDRAWN" And notice type "DEMAND" is a statutory notice | JOB-10 runs on 2026-12-14 | notice "N-0101" is written to the WIN file And the ledger entry has conduct check "PASSED" and summary "Statutory notice, consent withdrawn" | RWB-E2-021 |
| AC-EXC-P7-032-08 | Template withdrawn after approval | template "DEMAND-SSME" "TH" version 1 was withdrawn on 2026-12-13 | JOB-10 runs on 2026-12-14 | notice "N-0101" is "Held" with hold reason "TEMPLATE_WITHDRAWN" and is not in the WIN file And a task is raised to the litigation officer team with MSG-P6-003 | RWB-E2-021 |
| AC-EXC-P7-032-09 | Decision log write fails on a held notice | case "RC-2026-000321" has an open deviation "X2" with contact stop on And the decision log store is unavailable | JOB-10 runs on 2026-12-14 | notice "N-0101" stays "Approved" and is not in the WIN file And the job record shows MSG-P7-003 for "N-0101" And an incident is raised under rule R-UNI-39 | RWB-E2-021 |
| AC-EXC-P7-032-10 | Repeated request | "LIT-0101" sent POST /cases/RC-2026-000321/notices with notice type "RECALL" and Idempotency-Key "a1b2c3d4-0001" | the same request is sent again with Idempotency-Key "a1b2c3d4-0001" | the response is the first notice with status 201 And case "RC-2026-000321" has one RECALL notice | RWB-E2-021 |
| AC-EXC-P7-032-11 | Notice type missing | "LIT-0101" holds RW-LITOFF and case "RC-2026-000321" is in scope | "LIT-0101" sends POST /cases/RC-2026-000321/notices with no notice type | the response is status 422 with MSG-GEN-001 naming "notice type" | RWB-E2-021 |
| AC-EXC-P7-032-12 | No consent on the channel | party "P-0077" has a "MOBILE" contact point with consent "WITHDRAWN" | "CO-0201" sends a message with channel "SMS" | the response is status 409 with MSG-P6-002 naming "SMS" And nothing is sent to NSS And an interaction with conduct check "BLOCKED" is written | RWB-E2-022 |
| AC-EXC-P7-032-13 | Template withdrawn | template "SMS-REMIND" "TH" version 1 is Withdrawn and no later version is Approved | "CO-0201" sends a message with channel "SMS" and template "SMS-REMIND" | the response is status 409 with MSG-P6-003 naming "SMS-REMIND" | RWB-E2-022 |
| AC-EXC-P7-032-14 | NSS unavailable | the ACE notification path returns "unavailable" for NSS | "CO-0201" sends a message with channel "SMS" | the response is status 202 with MSG-GEN-006 naming "NSS" And JOB-11 retries the send on its schedule And after the retry limit of 5 the send is in the exception queue under rule R-UNI-34 and the interaction has delivery status "FAILED" | RWB-E2-022 |
| AC-EXC-P7-032-15 | NSS failure result | party "P-0077" has a verified "MOBILE" contact point with consent "GIVEN" and failed count 0 | NSS returns result "FAILED" for the message | the interaction has delivery status "FAILED" And the contact point has failed count 1 | RWB-E2-022 |
| AC-EXC-P7-032-16 | Repeated request | "CO-0201" sent a message with Idempotency-Key "c0ffee00-0001" | the same request is sent again with Idempotency-Key "c0ffee00-0001" | the response is the first response And NSS received one message | RWB-E2-022 |
| AC-EXC-P7-032-17 | Decision log write fails on a refusal | case "RC-2026-000777" has an open deviation "X6" And the decision log store is unavailable | "CO-0201" sends a message with channel "SMS" | the response is status 503 with MSG-P7-003 And nothing is sent to NSS And an incident is raised under rule R-UNI-39 | RWB-E2-022 |
| AC-EXC-P7-032-18 | Channel missing | template "SMS-REMIND" "TH" is current and party "P-0077" has a verified "MOBILE" contact point | "CO-0201" sends POST /cases/RC-2026-000777/messages with no channel | the response is status 422 with MSG-GEN-001 naming "channel" | RWB-E2-022 |
| AC-EXC-P7-032-19 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-032-20 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.32.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-032-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.33 Record a hand-over in the ledger

#### A2.33.1 Intent

**Business objective.** A case moving between owners or out to a partner records who had it, who has it now and when.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.33.2 Description

**Functional overview.** A case moving between owners or out to a partner records who had it, who has it now and when.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a completed ACE batch, an event or a timer | Reads the version of the rules in force |
| 2 | System | Record a hand-over in the ledger | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Partner portal, Workbench

**Prerequisites.** FEAT-ILG-01

#### A2.33.3 Business rules and structure

##### A2.33.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-033-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-P7-033 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.33.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Partner and agency manager | Also uses |

#### A2.33.4 Acceptance criteria

##### A2.33.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-033-01 | An interaction is recorded | `v_ace_efs_action` for business date 14 December 2026 holds an EFS action for account "ACC-SYN-0301" with action code "PTP", call result RIGHT_PARTY, contact time 14 December 2026 10:15, promise amount 12,500.00 and promise date 20 December 2026 And case owner "U-2001" records a call on 15 December 2026 09:30 to contact point "CP-SYN-0301-M" with result NO_ANSWER | the ACE batch for source EFS completes and the call is saved | the ledger holds a CONTACT entry with source EFS, channel CALL, occurred 14 December 2026 10:15, result RIGHT_PARTY, promise 12,500.00 for 20 December 2026 and retention class "ILG-STD" And the ledger holds a CONTACT entry with source WORKBENCH, channel CALL, occurred 15 December 2026 09:30, contact point "CP-SYN-0301-M" and result NO_ANSWER | RWB-E2-034 |

##### A2.33.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-033-01 | A hand-over is recorded | case "RW-2026-000301" is transferred from "U-2001" to "U-2002" on 16 December 2026 11:00 And instruction "INS-SYN-0301" is issued to partner "LF-SYN-01" on 17 December 2026 14:00 | both moves complete | the CASE_TRANSFERRED entry of 16 December 2026 11:00 holds from "USER:U-2001" and to "USER:U-2002" And the ledger holds a HANDOVER entry with channel PORTAL, direction OUTBOUND, from "USER:U-2002", to "PARTNER:LF-SYN-01", occurred 17 December 2026 14:00 | RWB-E2-034 |
| AC-ALT-P7-033-02 | The ledger is one place | the EFS entry of 14 December 2026, the Workbench call of 15 December 2026 and a partner result from "LF-SYN-01" entered in the partner portal on 18 December 2026 16:00 | the case is read | GET /cases/{caseId}/interactions returns the 3 entries in the order 14, 15 and 18 December 2026 And each entry names its source: EFS, WORKBENCH, and WORKBENCH with channel PORTAL and event code PARTNER_RESULT | RWB-E2-034 |

##### A2.33.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-033-01 | EFS rows outside the list or outside a case are not written | the `v_ace_efs_action` rows for 14 December 2026 hold 3 rows: action code "PTP" for "ACC-SYN-0301", action code "SYS" not on the list for "ACC-SYN-0301", and action code "PTP" for account "ACC-SYN-0999" on no open case | the ACE batch for source EFS completes | the ledger holds 1 new EFS entry And the import summary shows 3 read, 1 written, 1 excluded by the outcome list and 1 not on a case | RWB-E2-034 |
| AC-EXC-P7-033-02 | A ledger write failure loses nothing | the ledger store is unavailable | event NoticeDispatched for "NT-SYN-0301" is delivered the ledger store is available again and the outbox retries | no entry is written, the delivery stays in the outbox with status RETRYING and an incident is raised When the ledger store is available again and the outbox retries the ledger holds one LETTER entry for "NT-SYN-0301" | RWB-E2-034 |
| AC-EXC-P7-033-03 | An event for an unknown case goes to the exception queue | event InstructionIssued names an instruction whose case does not exist | the outbox has retried the delivery 3 times | no entry is written And the delivery is in the exception queue with a task for role RW-PLATADM | RWB-E2-034 |
| AC-EXC-P7-033-04 | A late EFS row reads in time order | the ledger holds the Workbench call of 15 December 2026 09:30 | the EFS row with contact time 14 December 2026 10:15 is processed on 15 December 2026 at 10:00 | the timeline shows the EFS entry before the call | RWB-E2-034 |
| AC-EXC-P7-033-05 | A case with no entry | open case "RW-2026-000302" with no ledger entry | the case owner opens the timeline | the timeline shows the empty state with message MSG-P3-024 | RWB-E2-034 |
| AC-EXC-P7-033-06 | A case outside the reader's scope is refused | case "RW-2026-000301" is owned by "U-2002" in team "MTG-BKK" | case owner "U-3001" of team "HP-NE" with Own scope reads its ledger | the response is 404 with message MSG-P4-003 | RWB-E2-034 |
| AC-EXC-P7-033-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-033-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.33.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-033-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.34 Read the ledger as a timeline on the case

#### A2.34.1 Intent

**Business objective.** The case record shows the ledger as an ordered history the case owner reads before deciding anything.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.34.2 Description

**Functional overview.** The case record shows the ledger as an ordered history the case owner reads before deciding anything.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and read the ledger as a timeline on the case | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-ILG-03

#### A2.34.3 Business rules and structure

##### A2.34.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-034-1 | A decision input is past its age limit | MSG-P7-006 {input} is {days} days old, past its limit. Refresh it before you decide. |
| BR-P7-034 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.34.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| decision_log_entry.case_id | The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case | uuid | No | None | No |
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | No |

##### A2.34.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Team manager, Conduct and QA officer | Also uses |

#### A2.34.4 Acceptance criteria

##### A2.34.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-034-01 | An interaction is recorded | `v_ace_efs_action` for business date 14 December 2026 holds an EFS action for account "ACC-SYN-0301" with action code "PTP", call result RIGHT_PARTY, contact time 14 December 2026 10:15, promise amount 12,500.00 and promise date 20 December 2026 And case owner "U-2001" records a call on 15 December 2026 09:30 to contact point "CP-SYN-0301-M" with result NO_ANSWER | the ACE batch for source EFS completes and the call is saved | the ledger holds a CONTACT entry with source EFS, channel CALL, occurred 14 December 2026 10:15, result RIGHT_PARTY, promise 12,500.00 for 20 December 2026 and retention class "ILG-STD" And the ledger holds a CONTACT entry with source WORKBENCH, channel CALL, occurred 15 December 2026 09:30, contact point "CP-SYN-0301-M" and result NO_ANSWER | RWB-E2-034 |

##### A2.34.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-034-01 | A hand-over is recorded | case "RW-2026-000301" is transferred from "U-2001" to "U-2002" on 16 December 2026 11:00 And instruction "INS-SYN-0301" is issued to partner "LF-SYN-01" on 17 December 2026 14:00 | both moves complete | the CASE_TRANSFERRED entry of 16 December 2026 11:00 holds from "USER:U-2001" and to "USER:U-2002" And the ledger holds a HANDOVER entry with channel PORTAL, direction OUTBOUND, from "USER:U-2002", to "PARTNER:LF-SYN-01", occurred 17 December 2026 14:00 | RWB-E2-034 |
| AC-ALT-P7-034-02 | The ledger is one place | the EFS entry of 14 December 2026, the Workbench call of 15 December 2026 and a partner result from "LF-SYN-01" entered in the partner portal on 18 December 2026 16:00 | the case is read | GET /cases/{caseId}/interactions returns the 3 entries in the order 14, 15 and 18 December 2026 And each entry names its source: EFS, WORKBENCH, and WORKBENCH with channel PORTAL and event code PARTNER_RESULT | RWB-E2-034 |

##### A2.34.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-034-01 | EFS rows outside the list or outside a case are not written | the `v_ace_efs_action` rows for 14 December 2026 hold 3 rows: action code "PTP" for "ACC-SYN-0301", action code "SYS" not on the list for "ACC-SYN-0301", and action code "PTP" for account "ACC-SYN-0999" on no open case | the ACE batch for source EFS completes | the ledger holds 1 new EFS entry And the import summary shows 3 read, 1 written, 1 excluded by the outcome list and 1 not on a case | RWB-E2-034 |
| AC-EXC-P7-034-02 | A ledger write failure loses nothing | the ledger store is unavailable | event NoticeDispatched for "NT-SYN-0301" is delivered the ledger store is available again and the outbox retries | no entry is written, the delivery stays in the outbox with status RETRYING and an incident is raised When the ledger store is available again and the outbox retries the ledger holds one LETTER entry for "NT-SYN-0301" | RWB-E2-034 |
| AC-EXC-P7-034-03 | An event for an unknown case goes to the exception queue | event InstructionIssued names an instruction whose case does not exist | the outbox has retried the delivery 3 times | no entry is written And the delivery is in the exception queue with a task for role RW-PLATADM | RWB-E2-034 |
| AC-EXC-P7-034-04 | A late EFS row reads in time order | the ledger holds the Workbench call of 15 December 2026 09:30 | the EFS row with contact time 14 December 2026 10:15 is processed on 15 December 2026 at 10:00 | the timeline shows the EFS entry before the call | RWB-E2-034 |
| AC-EXC-P7-034-05 | A case with no entry | open case "RW-2026-000302" with no ledger entry | the case owner opens the timeline | the timeline shows the empty state with message MSG-P3-024 | RWB-E2-034 |
| AC-EXC-P7-034-06 | A case outside the reader's scope is refused | case "RW-2026-000301" is owned by "U-2002" in team "MTG-BKK" | case owner "U-3001" of team "HP-NE" with Own scope reads its ledger | the response is 404 with message MSG-P4-003 | RWB-E2-034 |
| AC-EXC-P7-034-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-034-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.34.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-034-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

### A2.35 Set the retention class for ledger entries

#### A2.35.1 Intent

**Business objective.** Ledger retention is set independently of the decision log, as reference data.

**Problem.** Why a route was chosen, who approved it and on what figures is spread across emails and files.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Decisions within the delegation of authority | 100 percent | Decision log and Workbench records | Monthly |

#### A2.35.2 Description

**Functional overview.** Ledger retention is set independently of the decision log, as reference data.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Compliance and PDPA officer | Opens the screen and set the retention class for ledger entries | Checks the role, the capability area and the scope |
| 2 | Compliance and PDPA officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-ILG-02

#### A2.35.3 Business rules and structure

##### A2.35.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-P7-035-1 | Approver prepared the decision | MSG-P7-002 You prepared this decision, so you cannot approve it. |
| VR-P7-035-2 | Decision log write failed (principle 5) | MSG-P7-003 The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| VR-P7-035-3 | A decision input is past its age limit | MSG-P7-006 {input} is {days} days old, past its limit. Refresh it before you decide. |
| BR-P7-035 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.35.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| decision_log_entry.case_id | The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case | uuid | No | None | No |
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | No |

##### A2.35.3.3 Roles and permissions

| Role | Use |
|---|---|
| Compliance and PDPA officer | Primary |
| Reference data administrator | Also uses |

#### A2.35.4 Acceptance criteria

##### A2.35.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-P7-035-01 | An interaction is recorded | `v_ace_efs_action` for business date 14 December 2026 holds an EFS action for account "ACC-SYN-0301" with action code "PTP", call result RIGHT_PARTY, contact time 14 December 2026 10:15, promise amount 12,500.00 and promise date 20 December 2026 And case owner "U-2001" records a call on 15 December 2026 09:30 to contact point "CP-SYN-0301-M" with result NO_ANSWER | the ACE batch for source EFS completes and the call is saved | the ledger holds a CONTACT entry with source EFS, channel CALL, occurred 14 December 2026 10:15, result RIGHT_PARTY, promise 12,500.00 for 20 December 2026 and retention class "ILG-STD" And the ledger holds a CONTACT entry with source WORKBENCH, channel CALL, occurred 15 December 2026 09:30, contact point "CP-SYN-0301-M" and result NO_ANSWER | RWB-E2-034 |

##### A2.35.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-ALT-P7-035-01 | A hand-over is recorded | case "RW-2026-000301" is transferred from "U-2001" to "U-2002" on 16 December 2026 11:00 And instruction "INS-SYN-0301" is issued to partner "LF-SYN-01" on 17 December 2026 14:00 | both moves complete | the CASE_TRANSFERRED entry of 16 December 2026 11:00 holds from "USER:U-2001" and to "USER:U-2002" And the ledger holds a HANDOVER entry with channel PORTAL, direction OUTBOUND, from "USER:U-2002", to "PARTNER:LF-SYN-01", occurred 17 December 2026 14:00 | RWB-E2-034 |
| AC-ALT-P7-035-02 | The ledger is one place | the EFS entry of 14 December 2026, the Workbench call of 15 December 2026 and a partner result from "LF-SYN-01" entered in the partner portal on 18 December 2026 16:00 | the case is read | GET /cases/{caseId}/interactions returns the 3 entries in the order 14, 15 and 18 December 2026 And each entry names its source: EFS, WORKBENCH, and WORKBENCH with channel PORTAL and event code PARTNER_RESULT | RWB-E2-034 |

##### A2.35.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-P7-035-01 | EFS rows outside the list or outside a case are not written | the `v_ace_efs_action` rows for 14 December 2026 hold 3 rows: action code "PTP" for "ACC-SYN-0301", action code "SYS" not on the list for "ACC-SYN-0301", and action code "PTP" for account "ACC-SYN-0999" on no open case | the ACE batch for source EFS completes | the ledger holds 1 new EFS entry And the import summary shows 3 read, 1 written, 1 excluded by the outcome list and 1 not on a case | RWB-E2-034 |
| AC-EXC-P7-035-02 | A ledger write failure loses nothing | the ledger store is unavailable | event NoticeDispatched for "NT-SYN-0301" is delivered the ledger store is available again and the outbox retries | no entry is written, the delivery stays in the outbox with status RETRYING and an incident is raised When the ledger store is available again and the outbox retries the ledger holds one LETTER entry for "NT-SYN-0301" | RWB-E2-034 |
| AC-EXC-P7-035-03 | An event for an unknown case goes to the exception queue | event InstructionIssued names an instruction whose case does not exist | the outbox has retried the delivery 3 times | no entry is written And the delivery is in the exception queue with a task for role RW-PLATADM | RWB-E2-034 |
| AC-EXC-P7-035-04 | A late EFS row reads in time order | the ledger holds the Workbench call of 15 December 2026 09:30 | the EFS row with contact time 14 December 2026 10:15 is processed on 15 December 2026 at 10:00 | the timeline shows the EFS entry before the call | RWB-E2-034 |
| AC-EXC-P7-035-05 | A case with no entry | open case "RW-2026-000302" with no ledger entry | the case owner opens the timeline | the timeline shows the empty state with message MSG-P3-024 | RWB-E2-034 |
| AC-EXC-P7-035-06 | A case outside the reader's scope is refused | case "RW-2026-000301" is owned by "U-2002" in team "MTG-BKK" | case owner "U-3001" of team "HP-NE" with Own scope reads its ledger | the response is 404 with message MSG-P4-003 | RWB-E2-034 |
| AC-EXC-P7-035-07 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-P7-035-08 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.35.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| AC-BG-P7-035-01 | Hash chain check | Schedule | Nightly | Checks the decision log chain | Break reported the same day | The log can be relied on in audit |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-DRI-001 | Every decision writes one record holding case and decision, the rule, model, agent and prompt versions, an inputs snapshot, the recommendation, the approval, the actions taken and the outcome. | Must | E1 |
| REQ-DRI-002 | The decision log is append only. A record cannot be changed or deleted, and a correction is a new record naming the one it corrects. | Must | E1 |
| REQ-DRI-003 | The decision log is hash chained, and the chain integrity is checked every day with a break reported to Compliance the same day. | Must | E1 |
| REQ-DRI-004 | Records are written from Epic 1 for case creation, owner assignment, case transfer and document attachment. | Must | E1 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written. | Must | E1 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release. | Must | E1 |
| REQ-DRI-011 | A reference data service holds every versioned table with its valid from and valid to dates, author and approver. | Must | E1 |
| REQ-DRI-012 | Audit can query the decision log for a population of cases and receive the decision history with inputs, versions, approver and final call. | Must | E2 |
| REQ-APD-001 | A decision that needs approval is routed to the approver named by the delegation of authority table for that decision, product and amount. | Must | E2 |
| REQ-APD-002 | An approver sees the recommendation, the reasons behind it, the inputs used and the limit that applies, on one screen. | Must | E2 |
| REQ-APD-003 | An approver can accept, change, reject or return the item with a question, and each outcome is recorded. | Must | E2 |
| REQ-APD-004 | A request above the approver's limit is refused and raised to the next approver in the matrix, with no silent approval. | Must | E2 |
| REQ-APD-005 | An override of a recommendation needs a coded reason, and the reason is reported monthly. | Must | E2 |
| REQ-APD-006 | Demand and recall notices are approved through this path as the first use of approval routing. | Must | E2 |
| REQ-APD-007 | An approval that is not answered inside its service level escalates to the named role. | Must | E2 |
| REQ-APD-008 | A committee decision is recorded against the item with the members present and the decision taken. | Must | E2 |
| REQ-APD-009 | The limit, the rule version and the approver are written to the decision log with every approval. | Must | E2 |
| REQ-APD-010 | A change to the delegation of authority table is versioned, approved and dated, and open items keep the version they were decided under. | Must | E2 |
| REQ-APD-011 | Approval routing works with no person available in a role, by escalating rather than stalling. | Should | E2 |
| REQ-ILG-001 | One ledger holds every interaction on a case, and no other record is the authoritative history of what happened with the customer. | Must | E1 |
| REQ-ILG-002 | Every entry carries the case ID, the event, the timestamp, the actor and the source that produced it. | Must | E1 |
| REQ-ILG-003 | Entries carry the channel, who or what was reached, and the outcome, where the interaction had one. | Must | E1 |
| REQ-ILG-004 | An offer, a promise, a payment or a hand-over made during an interaction is recorded against that interaction. | Must | E1 |
| REQ-ILG-005 | Every action the Workbench takes on a case writes to the ledger as it happens: case creation, allocation, transfer, escalation, document attachment and decisions taken. | Must | E1 |
| REQ-ILG-006 | The ledger reads back in one ordered sequence, filterable by channel, actor and date range, through one interface. | Must | E1 |
| REQ-ILG-007 | The same event arriving twice with the same key produces one entry, and the repeat is counted. | Must | E1 |
| REQ-ILG-008 | A ledger write that fails raises an incident. An entry is never discarded, because a ledger with silent gaps is trusted and wrong. | Must | E1 |
| REQ-ILG-009 | Contact outcomes from collections reach the ledger, so that contactability found before day 90 is not lost at hand-over. | Must | E2 |
| REQ-ILG-010 | Letters, messages and calls dispatched by the Workbench write their result to the ledger, including proof of delivery where it returns. | Must | E2 |
| REQ-ILG-011 | A hand-over to or from a partner writes to the ledger, naming who held the case, who holds it now, and when. | Must | E2 |
| REQ-ILG-012 | The case record view shows the ledger as an ordered timeline. | Must | E2 |
| REQ-ILG-013 | Ledger entries carry their own retention class, set independently of the decision log. | Must | E2 |
| REQ-ILG-014 | Personal data in the ledger is masked by role on the same rules as the case record. | Must | E1 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-10 Approval queue | Decisions waiting for the person's approval level, with the facts and the recommendation | E2 |
| SCR-11 Decision screen | The recommendation with reasons, the expected return by route, the limit check and approve, return or refuse | E2 |
| SCR-12 Committee pack | The pack for a committee decision with each member's vote | E4 |
| SCR-38 Decision log query | Search the decision log by case, rule, approver and date, with export | E2 |

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
| Decision | การตัดสินใจ | One of D1 to D9 or their sub-decisions, made by a rule, a model, an agent or a person |
| Decision log | บันทึกการตัดสินใจ | The append-only, hash-chained record of every decision with its inputs, versions, approver and outcome |
| Recommendation | ข้อเสนอแนะ | The option a rule, model or agent proposes, with reasons and confidence |
| Override | การตัดสินใจต่างจากข้อเสนอแนะ | A decision that does not follow the recommendation, with the reason recorded |
| Approval level | ระดับอำนาจอนุมัติ | One of the six levels of the bank approval authority regulation that may approve a decision |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.
