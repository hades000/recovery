# RWB-ITG-E1008-ITG Decision log store v1, append only and hash chained — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1008-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Size | To be sized by the squad at refinement |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP09, DP10, DP13, DP15, DP17, DP19 |
| DP-09 library objects | Created by RWB-P7-E1008-DB; the consumer is built against the published RWB-PLT-TE006-CON template |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P1-E1001-APP, RWB-P4-E1008-APP, RWB-P7-E1008-APP |
| Contract dependencies | None |
| Contract version | API Specification v5, path version /v1 |
| Integration dependencies | RWB-P1-E1001-APP, RWB-P7-E1008-APP, RWB-P4-E1008-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-008 for the wave-1 integration epic. The monolith store becomes one local record per service plus the central ledger of rwb-decision, the shared topic carries the record, the data lake copy is retired (DP-17) and the chain check becomes the 02:00 Temporal Schedule JOB-14. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-ITG-E1008-ITG-L152). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 27 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the decision-record chain of wave 1 exercised end to end on the real services: every wave-1 service writing its own local decision record in its own schema in the same transaction as its state change, publishing exactly one `rwb.decision.DecisionRecorded.v1` on the shared topic `rwb.decision-record.v1`, rwb-decision ingesting it into the central append-only hash-chained ledger, and the 02:00 chain check naming the first break and telling Compliance within 15 minutes**, so that **every decision in the wave is recorded once, cannot be changed or deleted, and the chain is proven on the services that will run it rather than on a fake**.

### 2. Business rationale

Documentation and audit trail findings (5 of 29 in the audit summary behind CTL-06) show that why a route was chosen, who approved it and on what figures is spread across e-mails and files. RWB-E1-008 builds the store that every later decision writes to, and it meets REQ-DRI-001, REQ-DRI-002 and REQ-DRI-003; the measure is every decision reproducible from the log (NFR-033).

In the target the store is split by decision. Each service writes its own decision record in its own schema in the same transaction as its state change, and publishes it once on the shared topic (DP-03); rwb-decision collects the record into the central ledger it owns (ADR-022) and checks the chain at 02:00 as a Temporal Schedule, which replaces the Quartz job (DP-10, JOB-14); the copy of the log to the data lake is retired because there is no data lake (DP-17, RWB-E1-014 retired), and rwb-reporting builds its read model from the same topic. None of those pieces is proven by any single service story: a local record that commits without its event, an event without an entry, an entry outside the chain, a break no one reports and a lake copy that survives are all failures that only appear across services. This story builds and runs the harness that proves the five properties together, on the real services and the real topic, and it publishes no operation of its own.

### 3. Preconditions

- The nine wave-1 services are deployed in DEV and SIT, each with its own schema and login: rwb_source_data, rwb_case, rwb_access, rwb_document, rwb_comms, rwb_decision, rwb_reporting, rwb_agent and rwb_integration (Arch v5 slide 41, wave 1).
- Every wave-1 schema holds the local library objects of DP-03: `decision_record`, `outbox_event`, `processed_event` and the append-only rule on the local record (RWB-P7-E1008-DB for rwb_decision and the DB story of each service).
- rwb-decision holds `decision_log_entry` with `chain_seq`, `prev_hash`, `entry_hash` and `corrects_entry_id`, the chain lock, the canonical form and the append-only trigger; the service role holds INSERT and SELECT and no UPDATE or DELETE grant (RWB-P7-E1008-APP, RWB-P7-E1008-DB).
- The topic `rwb.decision-record.v1` exists with its retry and `.dlt` topics and 12 partitions, and queue `rwb-decision` is registered in namespace `rwb-recovery` (RWB-PLT-EVT, RWB-PLT-WF).
- The 02:00 Schedule of JOB-14 is registered by the operations story and can be triggered once by the harness (RWB-P7-E1008-OPS).
- rwb-access answers the authorise call and holds the test roles RW-AUDIT, RW-COMPLY, RW-COE and RW-PHONECOL with their Decision log letters (RWB-P4-E1008-APP).
- The DEV synthetic data set holds case "RW-2026-000123" with a customer reference and an account reference reachable through rwb-source-data (RWB-P1-E1001-APP).
- The decision codes, the outcome codes and the approval levels used by the fixtures are reference data read through the rwb-case reference-data contract, never values in the harness code (DP-07).
- The event payload and the ingest rule are Not specified in the source documents (GAP-0332; ASM-0426).
- This story is Day 1 by rule (Template and Rules §R5.7). The harness is written on Day 1 against the three integration services and is run when they are in DEV, so the builds listed under Depends on (build) are needed for the run; a fake is never used in their place.
- Open decision DL26 (retention, and the masking paired with it) applies and is still open; it is carried by assumptions ASM-0247, ASM-0264, ASM-0275 and ASM-0355 (Assumptions Register v1).

### 4. Flow

1. Pipeline and harness: reads the service list, the topic and the queue from configuration, and runs the preflight of section 13; a missing local record object, ledger table, chain object, topic, retry topic, task queue or Schedule stops the run before any test.
2. Harness: drives one real state change in each wave-1 service through that service's own write path, on the synthetic case "RW-2026-000123", with the rule ID and the rule version of the fixture package.
3. Service: writes the state change, the local `decision_record` row and the `outbox_event` row in one transaction in its own schema; the append is the last statement of the transaction and the chain lock orders concurrent appends.
4. Service: on a failed append the transaction rolls back, the state change does not happen and the caller shows MSG-P7-003; the harness records the refused chain_seq and confirms that it is not used.
5. Relay: publishes one CloudEvents 1.0 event `rwb.decision.DecisionRecorded.v1` per append on `rwb.decision-record.v1`, binary mode, key caseId, with the payload of ASM-0426.
6. rwb-decision: the consumer records the event id in `processed_event`, ignores a repeated delivery, and the ingest activity appends the entry to `decision_log_entry` with `chain_seq`, `prev_hash` and `entry_hash`.
7. Harness: reads the entry back through `GET /api/recovery/decision/v1/decision-log/{entryId}` as a Decision log R holder, and again as RW-PHONECOL, with the `POST /api/recovery/access/v1/authorise` call in between.
8. Harness: loads the 100-entry and the 10,000-entry fixtures through the chain, changes the actions of the entry with `chain_seq` 7,412 in the DEV database with the trigger disabled, restores the trigger, and triggers the 02:00 Schedule once.
9. Harness: reads the chain-check result, waits for the incident and MSG-P7-008 and records the elapsed time from the run start.
10. Harness: inspects the job map, the topic list, the schemas and the interfaces for a copy of the decision log to a data lake and fails on any element found.
11. Harness: reconciles the counts — one append, one event, one entry, one chain — and writes the run report.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local append fails inside the caller's transaction | The transaction rolls back, the state change does not happen, the chain_seq is not used, and the caller shows MSG-P7-003 | MSG-P7-003 | AC1 |
| X2 | The same event is delivered twice to rwb-decision | The consumer inbox `processed_event` ignores the second delivery; the ledger holds one entry and no second chain_seq | None | AC2 |
| X3 | A role without Decision log R calls the read | rwb-access refuses the authorise call and the read answers 403 | MSG-P4-002 | AC3 |
| X4 | The entry belongs to a case outside the caller's scope | The read answers 404 and the entry is not returned | MSG-P4-003 | AC3 |
| X5 | The chain check finds a break | The workflow names the first failing entry, raises an incident and sends MSG-P7-008 within 15 minutes of the run start | MSG-P7-008 | AC4 |
| X6 | A job, topic, table, interface or file that copies the decision log to a data lake is found | The run fails and the element is named in the report; the ledger stays the single copy | None | AC5 |
| X7 | An event carries a customer value or a person's name | The schema registry validation fails the build and the event is never published | None | AC2 |

X1 to X5 are the exception paths of the legacy story carried onto the real services; X6 is the regression that keeps the retired lake copy out (DP-17); X7 is the guardrail of section 17 in testable form.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The harness is a test project of its own; it needs the three integration services, the shared topic and the Schedule, and it owns no schema and no table |
| Negotiable | Fixture size, wait intervals, retry counts and report layout are configuration; the chain values, the message IDs and the run order are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: one record per append, one event, one entry, one chain, a reported break and no lake copy |
| Estimable | One harness project, five test classes, four fixtures, one tamper step, one Schedule trigger and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a row, an event, a response, a workflow result, an incident, a scan result |

### 7. Acceptance criteria

```gherkin
Feature: Decision log store v1, append only and hash chained, proven across the wave-1 services

  Background:
    Given the environment is DEV with synthetic data
    Given the nine wave-1 services run with their own schemas and login
    Given the shared topic rwb.decision-record.v1 exists with its retry and .dlt topics
    Given the ledger in rwb_decision is empty and the chain starts at chain_seq 1 with 64 zeros

  Scenario: AC1 The local record commits or rolls back with the caller's transaction (new, D-RCV-60)
    Given a wave-1 service holds its decision record in its own schema table decision_record, append only
    When the service changes its state and appends the record inside the same transaction
    Then the state change and the record are both visible after the commit
    Then the service role holds INSERT and SELECT on decision_record and no UPDATE or DELETE grant
    When the append fails inside the transaction
    Then the state change is not visible either
    Then the caller shows MSG-P7-003 and the chain_seq of the failed append is not used
    Then no entry of that append exists in the service schema or in the central ledger

  Scenario: AC2 Each append yields exactly one DecisionRecorded on the shared topic (new, D-RCV-60)
    Given a wave-1 service appends its decision record for case "RW-2026-000123"
    When the outbox relay publishes
    Then exactly one CloudEvents event rwb.decision.DecisionRecorded.v1 is on rwb.decision-record.v1, keyed caseId
    Then the event carries the fields of the design record fixed in ASM-0426 (entryId, caseId, decisionCode, ruleId, ruleVersion, inputsRef, recommendation, approverUserId, approvalLevel, finalCall, actions, outcome, decidedAt, entryHash, prevHash) and no customer value or person's name
    When the same event is delivered a second time
    Then the consumer inbox processed_event ignores the second delivery and rwb_decision holds one entry with one chain_seq

  Scenario: AC3 The central ledger stores one chain and the read needs the Decision log right (new, D-RCV-60)
    Given rwb-decision has ingested the record of case "RW-2026-000123"
    Then decision_log_entry in rwb_decision holds the entry with chain_seq, prev_hash and entry_hash, in one chain, append only
    Then the first entry has prev_hash of 64 zeros and every later prev_hash equals the entry_hash of the entry before it
    When a user holding Decision log R calls GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the response holds the entry with chain_seq, prevHash, entryHash and the design record fields
    When test user "U-6104" holds only RW-PHONECOL, whose Decision log letter is "-", and calls the same path
    Then rwb-access refuses through POST /api/recovery/access/v1/authorise and the answer is 403 with MSG-P4-002

  Scenario: AC4 The 02:00 Schedule recomputes the chain and reports the first break within 15 minutes (new, D-RCV-60)
    Given the store holds 10,000 entries
    Given the actions of the entry with chain_seq 7,412 were changed in the DEV database with the trigger disabled
    When the chain-check Schedule runs at 02:00 on queue rwb-decision as ChainCheckWorkflow
    Then the workflow recomputes every entry_hash and every prev_hash from chain_seq 1 to 10,000 and names chain_seq 7,412 and its entry ID as the first break
    Then an incident is raised and MSG-P7-008 is sent to the Compliance role (RW-COMPLY) within 15 minutes of the run start
    Then a run on an unbroken chain of 10,000 entries reports count 10,000, last chain_seq 10,000 and that entry_hash with no incident

  Scenario: AC5 No job, topic, table or interface copies the decision record to a data lake (new, D-RCV-60)
    Given the wave-1 environment is running
    When the job map, the topic list, the schemas and the interfaces are inspected
    Then no job that copies the decision record to a data lake exists, and ingestDecisionRecord is continuous Kafka ingest in rwb-decision (RWB-E1-014 retired, DP-17)
    Then no topic, table, interface or file carries a copy of the decision record to a data lake
    Then the ledger in rwb_decision is the single copy and the read model of rwb-reporting is fed only by rwb.decision-record.v1

  Scenario: AC9 Entries are kept under the bank retention schedule (new, D-RCV-60)
    Given the central ledger in rwb_decision holds entries
    When the retention of an entry is checked against the bank retention schedule (open decision DL26)
    Then the entry is kept for the period set by the bank retention schedule
    Then the retention period is Not specified in the source documents (NEWAC-RWB-ITG-E1008-ITG-AC9)

  Scenario: AC10 A consumed call fails or does not answer (new, D-RCV-60)
    Given a wave-1 service calls a consumed interface
    When the call fails or does not answer
    Then the handling of the failed call is Not specified in the source documents (NEWAC-RWB-ITG-E1008-ITG-AC10)

  Scenario: AC11 A status change the model does not allow is refused (new, D-RCV-60)
    Given a status change the model does not allow
    When the service requests that change
    Then the change is refused
    Then the refusal message is Not specified in the source documents (NEWAC-RWB-ITG-E1008-ITG-AC11)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every decision writes one entry holding the seven field groups: inputs, versions, recommendation, approver, final call, actions and outcome | REQ-DRI-001; DF-DEC-004 to DF-DEC-015 |
| BR2 | A stored entry is never updated or deleted; a correction is a new entry naming the entry it corrects | REQ-DRI-002; R-UNI-24; tr_declog_append_only in Recovery Workbench Physical Schema v7.sql; ADR-009 |
| BR3 | Each service chains its own decision records in chain_seq order and the central ledger chains its entries on ingest; prev_hash is the entry_hash of the entry before in the same chain, and 64 zeros for the first record of each chain; the ledger chain is the chain of record and the local chain serves replay | REQ-DRI-003; DF-DEC-017, DF-DEC-018 |
| BR4 | entry_hash is the SHA-256, in lower-case hexadecimal, of the canonical form: the entry's fields except entry_hash and the standard columns, as JSON with keys in alphabetical order, UTF-8, no spaces, timestamps in ISO 8601 UTC with microseconds, numbers as strings and empty fields as null | This story; ADR-009 |
| BR5 | The append is the last statement of the caller's transaction, so the action and its entry commit or roll back together | Principle 5; R-UNI-39; CTL-06 |
| BR6 | A break found by the verifier is reported to Compliance within 15 minutes and raises an incident | NFR-035; REQ-DRI-003 |
| BR7 | Retention of entries follows the bank retention schedule | DL26 |
| BR8 | The local record is written before the event: the state change, the local decision record and the outbox row commit in one transaction, the relay publishes one event per append, and the consumer inbox makes the effect exactly one ledger entry | DP-03; Arch v5 slide 11 (outbox and inbox) and slide 42 notes; Temporal design slides 11 and 14 |
| BR9 | One shared topic `rwb.decision-record.v1` carries one event type `rwb.decision.DecisionRecorded.v1` in the CloudEvents 1.0 envelope, keyed caseId, carrying codes, IDs and references only, never a customer value or a person's name; a user id such as approverUserId is a staff identifier, classed as personal data in Data Classification v5 | Arch v5 slides 11 and 42; ASM-0426 |
| BR10 | The central ledger in rwb_decision is append only and is the only copy of the decision log; no job, topic, table, interface or file copies it to a data lake, and rwb-reporting reads the topic instead | DP-17; Arch v5 slide 37 (no data lake); Template and Rules §R6 (RWB-E1-014 retired) |

### 9. State transitions

None for a case status. This story reads and asserts, and it changes no case status of its own.

The entry, chain and ingest states the harness observes:

| Item | States |
|---|---|
| `decision_log_entry` | Appended, from its append onward; no other state, never updated and never deleted |
| Correction | A new entry with `corrects_entry_id`; the corrected entry keeps its own state |
| Chain | Sequenced from `chain_seq` 1 (prev_hash 64 zeros) to the last chain_seq; unbroken or broken at the first entry whose entry_hash or prev_hash does not match |
| Local record | Appended with the caller's transaction; committed or rolled back with it, never present alone |
| Ingest | Received, deduplicated through `processed_event`, appended, retried through the retry topic, or dead-lettered |
| Chain check run | Started at 02:00, completed unbroken, or completed with a break and an incident raised with MSG-P7-008 sent |
| Harness run | Not started, running, passed, failed with the failing criterion named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of the integration harness | Owns the harness, the fixtures, the tamper step and the run report |
| Wave-1 service teams | Own the local decision record, its schema objects and the publish of DecisionRecorded |
| rwb-decision owner (RWB-P7-E1008-APP, RWB-P7-E1008-DB) | Owns the ledger, the ingest, the chain check and the two read endpoints |
| rwb-access owner (RWB-P4-E1008-APP) | Owns the Decision log right check and the refusal |
| rwb-reporting owner | Owns the read model fed by `rwb.decision-record.v1` |
| RW-AUDIT Internal audit | Reads entries (Decision log R) |
| RW-COMPLY Compliance and PDPA officer | Reads entries; receives the break report |
| RW-COE Center of excellence analyst | Reads entries |
| Every bank role holding Decision log R | Reads entries inside its scope |
| RW-PLATADM Platform administrator | Receives the incident on a break or on a failed append |
| No role | May update or delete an entry |

The tamper step of AC4 runs as the schema owner in DEV only, on the synthetic data set, and is switched off in SIT, UAT and production; it is the one place where the harness writes to a service schema directly, and it restores the trigger in the same run.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` (rwb_decision) | all fields | Write (append), read |
| DF-DEC-028 | `decision_log_entry` (rwb_decision) | chain_seq | Write, read |
| DF-DEC-029 | `decision_log_entry` (rwb_decision) | corrects_entry_id | Write, read |
| DF-DEC-030 | `decision_log_entry` (rwb_decision) | actor_user_id | Write, read |
| DF-DEC-001 to DF-DEC-018 | `decision_record` (each wave-1 service schema) | all fields | Write (append), read |
| DF-DEC-028 to DF-DEC-030 | `decision_record` (each wave-1 service schema) | chain_seq, corrects_entry_id, actor_user_id | Write (append), read |
| Not specified in the source documents (DOR-RWB-ITG-E1008-ITG-7) | `processed_event` (each consumer schema) | event id, consumer group, processed at | Write, read |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-E1-008. The harness owns no schema, no table and no field: it reads through the two decision read endpoints and calls the services' own write paths for every append it needs. Each wave-1 service holds its local record in the table decision_record, created through the decision-record library in its own schema; the DDL is set in the DB story of each service, and the case reference and the trace ID travel in inputsRef. The strict-mode confirmation is the read GET /api/recovery/decision/v1/decision-log/{entryId}, which returns 200 once the entry is sealed, together with the sealed-entry announcement on rwb.decision-record.v1 for the reporting projection. The ledger has no REST append operation: rwb_decision.decision_log_entry is written only by the ingest of rwb.decision-record.v1. decision_log_entry.case_id is a plain uuid with no foreign key, and the case is verified over the P3 case contract.

The payload of `rwb.decision.DecisionRecorded.v1` is Not specified in the source documents (GAP-0332; ASM-0426); ASM-0426 fixes it to the fields of the design record (entryId, caseId, decisionCode, ruleId, ruleVersion, inputsRef, recommendation, approverUserId, approvalLevel, finalCall, actions, outcome, decidedAt, entryHash, prevHash). Those are record references and codes, never a business value invented by this story. Ingest into the central ledger dedupes on the CloudEvents id, orders per case from the producer, and rwb-decision assigns chain_seq and prev_hash under the chain lock, with catch-up within five minutes.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test project and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Reads the entries of one case in chain order, page and size |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | Reads one entry by entry ID, with chain_seq, prevHash and entryHash |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Decision log R check for the reader, and the refusal of RW-PHONECOL |
| GET | `/api/recovery/source-data/v1/accounts/{id}` | P1 rwb-source-data | Case reference read for the synthetic case |
| GET | `/api/recovery/source-data/v1/customers/{id}` | P1 rwb-source-data | Case reference read for the synthetic case |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the harness calls no service through another service.

#### 12.3 Events published

None. The harness publishes no business event. Every event asserted in this story is produced by a wave-1 service and is listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | Produced by every wave-1 service; consumed by P7 rwb-decision and P9 rwb-reporting | CloudEvents 1.0 binary mode, key caseId, exactly one event per append, inbox dedupe in `processed_event`, retry 1 min, 10 min, 1 h then `.dlt` |

The payload and the ingest rule are Not specified in the source documents (GAP-0332; ASM-0426). Under ASM-0426 the payload carries the design record fields (entryId, caseId, decisionCode, ruleId, ruleVersion, inputsRef, recommendation, approverUserId, approvalLevel, finalCall, actions, outcome, decidedAt, entryHash, prevHash); rwb-decision dedupes on the CloudEvents id, assigns chain_seq and prev_hash itself under the chain lock and catches up within 5 minutes of the commit.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| ChainCheckWorkflow | Workflow | `rwb-decision` | Input from chain_seq, to chain_seq and business date; output count checked, last chain_seq, last entry_hash, first break chain_seq and entry ID, and the incident reference |
| ingestDecisionRecord | Activity | `rwb-decision` | Input the DecisionRecorded envelope and payload; output entry ID, chain_seq and entry_hash; idempotent on the event id through `processed_event`; the chain lock, the canonical form and the hash are inside the activity |

Both are registered by the rwb-decision worker (RWB-P7-E1008-APP); this story drives them and asserts their output, and it adds no workflow of its own.

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| `decisionChainCheck` | Daily at 02:00, overlap policy SKIP, catch-up window | Registered by the rwb-decision release; started once by the harness through the Temporal client with the same input the cadence uses | JOB-14 Hash-chain check |

#### 12.7 Tables owned

None. The harness owns no table. The tables it exercises belong to rwb_decision, to each wave-1 service schema and to the platform library, and are listed in section 11 with their owners.

#### 12.8 Contract fakes

None. This is the integration level: the real services, the real topic and the real Schedule replace the contract fakes of the app stories. The run calls the deployed rwb-access, rwb-decision and rwb-source-data services, not a fake of them, so this story needs no published contract fake and no contract fake library version. The fakes and their library versions are recorded in the contract stories of those services.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 5 | Two decision reads, the authorise call and two case reference reads; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | 1 event type | `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` from each wave-1 service, key caseId |
| Temporal | None | 1 workflow, 1 activity, 1 Schedule | ChainCheckWorkflow, ingestDecisionRecord; `decisionChainCheck` at 02:00 |
| File | None | None | No file in this story |

### 13. Solution plan

**Deliverables.** One test project `integration/recovery-w1/decision-record`, with the five test classes `TransactionalAppendIT`, `EventOnceIT`, `LedgerAndReadIT`, `ChainCheckScheduleIT` and `NoLakeCopyIT`, the fixture files and the run report writer.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| HarnessRunner | Runner | Preflight, run order, report and exit code |
| FixtureBuilder | Service | Builds the 100-entry and 10,000-entry chains deterministically through the real write path, with the golden canonical form |
| EventProbe | Service | Consumes `rwb.decision-record.v1` and asserts exactly one event per append, the key, the envelope and the payload fields |
| LedgerProbe | Service | Reads the two decision endpoints, compares chain_seq, prev_hash and entry_hash with the events |
| AccessProbe | Service | Calls the authorise path with the Decision log R holder and with RW-PHONECOL and asserts 200 and 403 with MSG-P4-002 |
| ChainCheckDriver | Service | Starts the `decisionChainCheck` Schedule once, reads the workflow result and times the incident and MSG-P7-008 |
| TamperTool | Service | DEV only: disables the trigger, changes the actions of the entry with chain_seq 7,412, restores the trigger and verifies the restore |
| LakeCopyScanner | Service | Reads the job map, the topic list, the schema list and the interface list and fails on any lake copy |
| ReportWriter | Service | One row per test case, with the evidence and the elapsed times |

**Database.** None of its own. The harness writes only through the services' own write paths, and the single direct write is the DEV tamper step of AC4.

**Configuration and reference data**

- The service list, the topic, the retry and `.dlt` topics, the queue, the namespace and the Schedule name, all as configuration.
- The synthetic case "RW-2026-000123", the rule ID, the rule version and the package code of the fixture package.
- The test roles RW-AUDIT, RW-COMPLY, RW-COE and RW-PHONECOL with their Decision log letters, from rwb-access.
- The decision codes, the outcome codes and the approval levels, read through the rwb-case reference-data contract (DP-07).
- The 15-minute report limit, the 2 s client budget and the catch-up wait.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; a gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The story carries no H, C or X dependency: the build dependencies of DP-03, DP-07, DP-10, DP-15 and DP-19 stay with the service, platform and operations stories this harness proves. The I list names the three services whose behaviour it exercises, and an integration dependency never blocks a build (Template and Rules §R5.4).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Chain of 100 entries | 100 synthetic entries through the real write path, chain_seq 1 to 100, first prev_hash 64 zeros | AC2, AC3, TC-E1-008-02-ITG |
| Chain of 10,000 entries | 10,000 synthetic entries, entry with chain_seq 7,412 changed with the trigger disabled and the trigger restored | AC4, TC-E1-008-04-ITG |
| Two parallel appends | Two writers appending after chain_seq 50 in parallel transactions | TC-E1-008-05-ITG |
| Correction pair | Entry "E-1" with the wrong owner reference and its correction naming it | TC-E1-008-06-ITG |
| Refused append | The connection closed in the test double inside a transaction that also changes a state | TC-E1-008-07-ITG, TC-E1-008-10-ITG |
| Role set | RW-AUDIT, RW-COMPLY, RW-COE and RW-PHONECOL, the last with Decision log "-" | AC3, TC-E1-008-08-ITG, TC-E1-008-09-ITG |

**Run order.** Preflight; transactional append on one service (AC1); one event and a repeated delivery (AC2); ledger, reads and the refusals (AC3); the two chains and the tampered entry, then the 02:00 run (AC4); the lake-copy scan (AC5); cleanup of the DEV fixtures with the trigger confirmed restored. A failing step stops the run and the report names the criterion, the service and the evidence.

**Done when.** The 15 test cases of section 16 pass on the real services in DEV and SIT, the chain check on the 10,000-entry chain names chain_seq 7,412, the incident and MSG-P7-008 arrive within 15 minutes of the run start, exactly one event and one ledger entry exist per append, and the lake-copy scan finds nothing.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | A caller's action fails because the append failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-008 | The chain check finds a break | The decision log check for {date} found a break at entry {entryId}. Entries from that entry on cannot be relied on until Compliance reviews them. |
| MSG-P4-002 | Read without Decision log R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Entry of a case outside the caller's scope | This case is not in your scope. |

The four texts are copied unchanged from RWB-E1-008; the story adds no message text. Report lines of the harness are for developers and are not part of the message standard.

### 15. Screens and states

No screen in this story, and the harness renders nothing: the two read endpoints are called directly and are the only reader surface it uses. The Decision log query screen SCR-38 comes in RWB-E2-005 and is out of scope here. SCR-38 states: loading (Screen Specifications v1, which also lists results and export); no access: the refusal MSG-P4-002 (Screen Specifications v1, SCR-38 messages); empty and error: Not specified in the source documents (DOR-RWB-ITG-E1008-ITG-10). The states the harness observes are the entry, chain, ingest and run states of section 9.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-008-01-ITG | AC1, BR2 | Integration | One synthetic entry; update and delete statements |
| TC-E1-008-02-ITG | AC2, BR3, BR4 | Integration | 100 synthetic entries |
| TC-E1-008-03-ITG | AC3, BR1 | Integration | One entry with all seven field groups filled |
| TC-E1-008-04-ITG | AC4, BR6 | End to end | 10,000 synthetic entries with one changed in DEV |
| TC-E1-008-05-ITG | AC5, BR3 | Integration | Two parallel appends after chain_seq 50 |
| TC-E1-008-06-ITG | AC6, BR2 | Integration | Run by RWB-P7-E1008-APP, RWB-P7-E1008-DB, RWB-P4-E1008-APP: entry and its correction |
| TC-E1-008-07-ITG | AC7, BR5 | Integration | Run by RWB-P7-E1008-APP, RWB-P7-E1008-DB, RWB-P4-E1008-APP: closed connection in the test double |
| TC-E1-008-08-ITG | AC8 | Integration | Run by RWB-P7-E1008-APP, RWB-P7-E1008-DB, RWB-P4-E1008-APP: RW-PHONECOL test user |
| TC-E1-008-09-ITG | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E1-008-10-ITG | Principle 5 | Integration | The decision record write forced to fail; the caller's change rolls back |
| TC-ITG-E1008-01 | AC1, BR5, BR8 | Integration | One state change and its append in one transaction; one append forced to fail |
| TC-ITG-E1008-02 | AC2, BR3, BR9 | Integration | One append, one event on `rwb.decision-record.v1`, one repeated delivery |
| TC-ITG-E1008-03 | AC3, BR1, BR10 | End to end | One ingested entry read as a Decision log R holder and refused for RW-PHONECOL with MSG-P4-002 |
| TC-ITG-E1008-04 | AC4, BR6 | End to end | 10,000 entries with entry 7,412 tampered; the 02:00 run, the incident and MSG-P7-008 inside 15 minutes |
| TC-ITG-E1008-05 | AC5, BR10 | Component | The job map, the topic list, the schemas and the interfaces scanned for a lake copy |
| TC-ITG-E1008-06 | §12 operations, events and activities | Contract | Each operation, event and activity named in §12 checked against its published contract |
| TC-ITG-E1008-07 | AC9, BR7 | Not specified in the source documents (NEWAC-RWB-ITG-E1008-ITG-AC9) | Not specified in the source documents (NEWAC-RWB-ITG-E1008-ITG-AC9) |
| TC-ITG-E1008-08 | AC10 | Not specified in the source documents (NEWAC-RWB-ITG-E1008-ITG-AC10) | Not specified in the source documents (NEWAC-RWB-ITG-E1008-ITG-AC10) |
| TC-ITG-E1008-09 | AC11 | Not specified in the source documents (NEWAC-RWB-ITG-E1008-ITG-AC11) | Not specified in the source documents (NEWAC-RWB-ITG-E1008-ITG-AC11) |

The legacy acceptance criteria of RWB-E1-008 are owned by RWB-P7-E1008-APP, RWB-P7-E1008-DB and RWB-P4-E1008-APP and are re-exercised here end to end on the real services; the legacy test case IDs are kept as ITG copies with the suffix `-ITG`, and the new criteria AC1 to AC5 carry TC-ITG-E1008-01 to TC-ITG-E1008-05.

### 17. Guardrails

- No business value in code: the genesis hash, the fixture package, the report limit and the wait intervals are configuration; the decision codes and the approval levels are reference data (DP-07).
- Data Classification v5 classes ledger fields as personal data: customer data in inputs_ref, recommendation, override_reason, actions and outcome (DF-DEC-008, DF-DEC-009, DF-DEC-013 to DF-DEC-015) and staff identifiers in approver_user_id and actor_user_id (DF-DEC-010, DF-DEC-030). Events, workflow inputs, logs, fixtures and the report carry codes, IDs, references and hashes only, never a customer value or a person's name.
- Each service writes only its own schema and reads no other service's tables (DP-01); the harness reads through the contracts, and its single direct write is the DEV-only tamper step, which is refused in SIT, UAT and production and restores the trigger.
- No update and no delete path: no repository method, no database grant and no endpoint exists for either, and the harness asserts the refusal instead of relying on the review.
- One canonical form implementation serves writing and verifying (BR4); a second implementation would make a real break indistinguishable from a hash mismatch.
- One shared topic and one event type for the record (BR9); a service that publishes its own decision event on its own topic fails the run.
- No copy of the decision log leaves the ledger (BR10, DP-17); the scan of AC5 is a regression test, not a one-off check.
- The harness never uses production data and never points at a production namespace.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-001 | One record per decision with the seven field groups | `decision_record` in each service schema, `rwb.decision.DecisionRecorded.v1`, `decision_log_entry` | TC-E1-008-03-ITG, TC-ITG-E1008-01, TC-ITG-E1008-02 |
| REQ-DRI-002 | Append only; a correction is a new record naming the one it corrects | Append-only grant and trigger, `chain_seq`, `corrects_entry_id`, the two decision reads | TC-E1-008-01-ITG, TC-E1-008-06-ITG, TC-E1-008-07-ITG, TC-E1-008-10-ITG, TC-ITG-E1008-01, TC-ITG-E1008-03 |
| REQ-DRI-003 | Hash chained, checked, break reported to Compliance the same day | `prev_hash`, `entry_hash`, ChainCheckWorkflow, `decisionChainCheck`, MSG-P7-008 | TC-E1-008-02-ITG, TC-E1-008-04-ITG, TC-E1-008-05-ITG, TC-ITG-E1008-04 |

### 19. Out of scope

- The store, the ingest, the chain check and the two read endpoints (RWB-P7-E1008-APP).
- The contract and the AsyncAPI document of `rwb.decision-record.v1` (RWB-P7-E1008-CON).
- The `decision_log_entry` and `decision_record` schema design, the trigger and the grants (RWB-P7-E1008-DB).
- The deployment, the topic provisioning and the Schedule registration (RWB-P7-E1008-OPS).
- The Decision log right and its refusal in rwb-access (RWB-P4-E1008-APP); this story exercises it and owns none of it.
- The Decision log query screen SCR-38 and the audit filters by approver, rule version and date (RWB-E2-005).
- Retention periods and the retention run (DL26, RWB-P5 retention stories).
- The daily ledger seal to immutable storage (Arch v5 slide 14) and the minimal event payload and ingest rule until the shared-topic contract is published (GAP-0332).
