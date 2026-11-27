# RWB-P7-E1008-CON Decision log store v1, append only and hash chained - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice of RWB-E1-008 for rwb-decision — the published baseline of the central decision ledger: the two read operations, the entry and page shapes, the error envelope, the `DecisionRecorded` envelope the ingest consumes, the tables the ledger owns and the fakes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 22 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-E1008-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Contract version | v1 (path `/api/recovery/decision/v1`) |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P7-E1008-CON-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP03, DP07, DP10, DP13, DP15, DP17, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-001, FR-P7-003, FR-P7-004, FR-P7-005, FR-P7-006, FR-P7-009, FR-P7-010, FR-P7-011, FR-P7-012, FR-P7-013, FR-P7-029, FR-P7-036) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **contract owner of rwb-decision**, I want **the published baseline of the central decision ledger — the two read operations on `/api/recovery/decision/v1`, the `DecisionLogEntry` and `DecisionLogPage` shapes field for field, the error envelope and its message identifiers, the `DecisionRecorded` envelope the ledger ingests, the tables the ledger owns, and a fake for each of them**, so that **the ledger implementation, the query API, the strict-mode waiters and rwb-reporting can build on Day 1 against one frozen description of what a decision entry is**.

This is the contract slice of legacy RWB-E1-008. It publishes no code and no row: it fixes the description that `RWB-P7-E1008-APP` implements, that `RWB-P7-E2005-APP` extends with filters, and that every service's record already satisfies on the shared topic. It owns **no legacy acceptance criterion**: AC1 to AC8 of RWB-E1-008 stay with `RWB-P7-E1008-APP`, and every criterion in section 7 is new (D-RCV-60) and tests only the published baseline.

### 2. Business rationale

The legacy story described its contract inside itself: two read paths on the monolith base (`decision-log` and `decision-log/{entryId}`), one response shape, four error codes, and a published Java interface for the writer. Under Architecture v5 the same description has three different readers on Day 1 and none of them can wait for the others:

- the **ledger implementation** of this service, which must know what an entry looks like before it can chain one (DP-03);
- the **strict-mode waiters** — debt transfer, write-off posting, auction sale, title transfer — which wait for the ledger to confirm a record before a point of no return (Architecture v5 slide 28), and which must know the shape they read back;
- **rwb-reporting** and the query API of Epic 2, which read the ledger rather than the events (ADR-018) and need the page shape and the paging rule before they can write an extract.

The contract is also where three architecture facts become binding rather than advisory. **The base is the service's**, `/api/recovery/decision/v1` (DP-13), so the monolith base disappears with no compatibility path. **The record comes from the shared topic**, `rwb.decision-record.v1`, with the `DecisionRecorded` envelope of RWB-PLT-E1027-CON, so the ledger's input is a CloudEvents message and not an in-process call (DP-03). And **the table belongs to `rwb_decision`** (Ownership Map, `decision_log_entry`, P7), so no other service reads it and the cases and limits it names arrive as identifiers (DP-01).

Two points are published as the working read because no source closes them, and both are recorded: the Ownership Map gives P7 the two `GET` paths and **no append operation**, so the baseline declares no write path and the ingest of the shared topic stays the only writer (GAP-1224; ASM-2188); and Architecture v5 slide 14 names the ledger read `GET /decisions?caseId=` while the Ownership Map names `GET /decision-log` — the Ownership Map wins under the source precedence of Template and Rules §R3 (GAP-1230; ASM-2194).

### 3. Preconditions

- The service name, schema, base, topic, event-name, task-queue and package conventions of Template and Rules §R4 are fixed: `rwb-decision`, `rwb_decision`, `/api/recovery/decision/v1`, `rwb.decision.events.v1` with its retry and `.dlt` topics, `rwb.decision.<Event>.v1`, `rwb-decision`, `th.co.scb.ace.workbench.recovery.decision`.
- The entry fields are the ones fixed by TSD P7 v2 T3.1 (`DF-DEC-001` to `DF-DEC-031`) and by the physical schema: `id`, `case_id`, `decision_code`, `rule_id`, `rule_version`, `model_version`, `agent_version`, `inputs_ref`, `recommendation`, `approver_user_id`, `approval_level`, `final_call`, `override_reason`, `actions`, `outcome`, `decided_at`, `prev_hash`, `entry_hash`, `chain_seq`, `corrects_entry_id`, `actor_user_id`, `idempotency_key`.
- The decision codes and approval levels are rows in force of the rwb-case reference contract, `LOV-DECISION` and `LOV-APPROVAL-LEVEL` (DP-07); the contract names them and carries no list of its own.
- The `DecisionRecorded` envelope is the one published by RWB-PLT-E1027-CON on the shared topic `rwb.decision-record.v1`; this contract consumes it and restates only the fields the ledger stores.
- The `decision_log_entry` owner is P7 and the schema is `rwb_decision` under the Ownership Map rulings; the library objects `outbox_event`, `processed_event` and `idempotency_key` are PLT objects created in that schema by the DB story of this key.
- The paging parameters, their defaults and their maximum, and the full error body of the two reads, are Not specified in the source documents: the baseline publishes them as the working read (GAP-1229; ASM-2193).
- No build dependency and no approval stop: a CON story has no build dependency, is Day 1 by rule and groups in `CG-W1` (Template and Rules §R5.7); it is released at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the two operations: method, path under `/api/recovery/decision/v1`, purpose, authorisation, paging and the error set, with owner `rwb-decision`. The read of one entry answers 200 once the entry is sealed; that read is the confirmation a strict-mode step waits on. The sealed-entry announcement on `rwb.decision-record.v1` feeds the reporting projection.
2. The author fixes `DecisionLogEntry`: every field of the entry with its type, its field identifier and whether it may be absent, in the order of TSD P7 v2 T3.1.
3. The author fixes `DecisionLogPage`: the entries, the paging block (page 1, size 50, maximum 200) and the ordering rule — `chain_seq` ascending, always; each error is an RFC 9457 problem body with type, title, status, detail and the message identifier.
4. The author fixes the error envelope: RFC 9457 `application/problem+json` with the message identifier, and the four cases of the legacy contract (401, 403 MSG-P4-002, 404 MSG-P4-003, 503 MSG-GEN-006).
5. The author fixes the consumed `DecisionRecorded` envelope: the CloudEvents attribute set, `ce_type` `rwb.decision.DecisionRecorded.v1`, the key rule, the contract version of the event, the payload fields the ledger stores, and the dedupe key (`ce_id` into `idempotency_key` and `processed_event`). The consumer accepts a known set of contract versions and sends an unknown version to the dead-letter topic. Events are ordered per case as the producer emits them; the ledger assigns `chain_seq` and `prev_hash` on ingest under the chain lock; the catch-up completes within five minutes (completeness target); the gap alert threshold is five minutes of lag; the maximum strict-mode wait is Not specified in the source documents (GAP-1617). Each service chains its own records in `chain_seq` order; the ledger chain is the chain of record and the local chain serves replay. The AsyncAPI document of `rwb.decision-record.v1` is published at the shared-topic contract review before the first SIT run.
6. The author fixes the owned tables: `decision_log_entry` in `rwb_decision`, plus the three library objects created there, and states explicitly what the ledger does not own. The `case_id` column is a plain identifier with no foreign key, because `rwb_case` is P3's table; it is verified on the read through P3's case contract. The only writer of `decision_log_entry` is the ingest of `rwb.decision-record.v1`; no append operation is declared.
7. The author writes the versioning rule: major version 1, a backward-compatible change versus a breaking change with a new major version, and the pinning rule for consumers.
8. The fake set is generated from the same examples: the ledger read fake, the `DecisionRecorded` fake, the reference fake, the authorise fake, the case fake and the seal target fake.
9. The contract test runs the fakes against the document on every change, and the drift test of each consumer fails the build on any difference from sections 12 and 13.
10. The baseline is published at v1 and every consumer pins it.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A published path is not under `/api/recovery/decision/v1`, or an append operation is invented | The lint fails the build; the base is the service's and the ledger has no write path | None | AC1 |
| X2 | A published shape drops a field, renames one or changes a type against TSD P7 v2 T3.1 | The schema validation fails the build; the field identifiers are the source | None | AC2 |
| X3 | An error is published without a message identifier, or with a status the legacy contract does not have | The validation fails the build; the four cases and their identifiers are fixed | None | AC3 |
| X4 | The `ce_type`, the key rule or a payload field of `DecisionRecorded` differs from RWB-PLT-E1027-CON | The envelope validation fails the build; the shared envelope is not redefined here | None | AC4 |
| X5 | A table of another owner is named as the ledger's, or a cross-schema key is published | The boundary check fails the build; the owned list is fixed | None | AC5 |
| X6 | A breaking change is made to a path, a field or the envelope | The change raises major version 2 and a new `ce_type`; v1 is never edited in place | None | AC7 |
| X7 | A value the consumers need is named by no source — the paging defaults, the maximum page size or the error body | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-1229; ASM-2193) | AC8, AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and a fake set; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The paging defaults and the fixture set are open until v1 is frozen; the paths, the shapes, the error identifiers and the envelope are fixed |
| Valuable | Unblocks the ledger implementation, the query API, the strict-mode waiters and rwb-reporting on Day 1 |
| Estimable | Two operations, two shapes, one error envelope, one consumed envelope, one owned-table list and six fakes |
| Small | One sprint for the document, the fakes and the lint rules |
| Testable | Each criterion below is one lint, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: published baseline of the central decision ledger

  Background:
    Given the contract document is published with major version 1
    Given the service base is /api/recovery/decision/v1 and the owner is rwb-decision
    Given the schema is rwb_decision and the task queue is rwb-decision

  Scenario: AC1 The two read operations are published and no write path is declared (new, D-RCV-60)
    Given the operation section of the document
    When it is validated and linted
    Then it declares GET /decision-log and GET /decision-log/{entryId} with the owner rwb-decision on base /api/recovery/decision/v1
    Then it declares no POST, PUT, PATCH or DELETE operation on the ledger, because the Ownership Map gives P7 no append operation and the ingest of rwb.decision-record.v1 is the only writer
    Then every path is one hop behind gateway-bff with a 2 s budget and no other service base appears

  Scenario: AC2 DecisionLogEntry carries every field of the entry with its identifier (new, D-RCV-60)
    Given the shape section of the document
    When DecisionLogEntry is validated against TSD P7 v2 T3.1
    Then it carries id, caseId, decisionCode, ruleId, ruleVersion, modelVersion, agentVersion, inputsRef, recommendation, approverUserId, approvalLevel, finalCall, overrideReason, actions, outcome, decidedAt, prevHash, entryHash and chainSeq
    Then it carries correctsEntryId and actorUserId, and every field names its DF-DEC identifier
    Then caseId is absent only for an access event whose decision code starts with "AC-"
    Then decisionCode is 8 characters, approvalLevel is 4, inputsRef is 400, prevHash and entryHash are 64 characters, and chainSeq is an integer
    Then an example in the document uses only legacy values: decision "D6", case "RW-2026-000123", rule "R-UNI-14", rule version "UNI-2026.11", inputs reference "inputs/2026-12-03/7f3a", approver "U-6101", approval level "L6", final call "APPROVED"

  Scenario: AC3 DecisionLogPage and the error envelope are fixed (new, D-RCV-60)
    Given the paging and error sections of the document
    When a page and each error are validated
    Then DecisionLogPage carries the entries, the page number, the page size and the total, and the entries are ordered by chainSeq ascending
    Then the page and size parameters are declared with their default and their maximum as the working read of the assumption, and an out-of-range value answers 400
    Then the error body is application/problem+json with type, title, status, detail and the message identifier
    Then 401 has no message identifier, 403 carries MSG-P4-002, 404 carries MSG-P4-003 and 503 carries MSG-GEN-006
    Then no other status and no other message identifier is published for the two reads

  Scenario: AC4 The consumed DecisionRecorded envelope is restated and not redefined (new, D-RCV-60)
    Given the envelope section of the document
    When one envelope is validated against it
    Then the event is rwb.decision.DecisionRecorded.v1 on the shared topic rwb.decision-record.v1 in CloudEvents 1.0 binary mode with ce_specversion 1.0, ce_id, ce_type, ce_source, ce_subject, ce_time and the trace header
    Then the key is caseId where the record has a case and the entry id where it does not
    Then the payload carries the entry id, the case where there is one, the decision code, the final call, the rule ID, the rule version, the chain sequence, the entry hash, the actor reference and the decided time
    Then the envelope is the one of RWB-PLT-E1027-CON and this document adds no attribute and no field to it
    Then ce_id is the dedupe key of the ingest and is stored in idempotency_key

  Scenario: AC5 The owned tables are named and the foreign ones are excluded (new, D-RCV-60)
    Given the owned-table section of the document
    When it is checked against the Ownership Map
    Then decision_log_entry is the ledger table, owned by P7, declared in schema rwb_decision
    Then outbox_event, processed_event and idempotency_key are declared as PLT library objects created in rwb_decision by RWB-P7-E1008-DB
    Then delegation_limit is named as P4 rwb-access and read over its contract, never stored here
    Then parameter_catalog, parameter_value, reference_row, reference_version and lov_value are named as P3 rwb-case and read over RWB-P3-E1043-CON
    Then approval, rule_package, rule_package_version, rule_row and rule_test_case are named as other stories of this service and not part of this contract
    Then recovery_case, task, timer and queue are named as P3's, and no foreign key, view or grant across a schema boundary is published
    Then no data-lake copy and no reporting table is declared, and reporting reads the events

  Scenario: AC6 The fake set answers the document on every change (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs
    Then the ledger read fake answers a page in chainSeq order, one entry with the seven field groups, 403 with MSG-P4-002, 404 with MSG-P4-003 and 503 with MSG-GEN-006
    Then the DecisionRecorded fake answers one valid envelope, one repeated ce_id, one refused body and one envelope with no case
    Then the reference fake answers LOV-DECISION with D6 and LOV-APPROVAL-LEVEL with L1 to L6
    Then the authorise fake answers allowed and a refusal with MSG-P4-002, and the case fake answers a case in scope and one out of scope
    Then the drift test of the ledger implementation, of the query API and of each strict-mode waiter fails on any difference from section 12

  Scenario: AC7 Versioning separates a compatible change from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element
    Then a backward-compatible change — a new optional field, a new message identifier, a wider type — keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a breaking change — a removed or renamed field, a changed type, a new path or a new event type — raises major version 2, and v1 is never edited in place
    Then a consuming service pins a published version and raises a change request rather than a private variant

  Scenario: AC8 A value no source names is published as the working read and its gap stays open (new, D-RCV-60)
    Given a value the consumers need is named by no source
    When the paging and error sections are validated
    Then the value is published as the working read of ASM-2193 and GAP-1229 stays open
    Then no value that no source names is published as settled

  Scenario: AC9 The paging defaults, the maximum page size and the error body are published as working reads (new, D-RCV-60)
    Given the paging defaults, the maximum page size and the error body are each named by no source
    When the paging and error sections are validated
    Then each of the three is published as the working read of ASM-2193 and GAP-1229 stays open for it
    Then no one of the three is published as settled

  Scenario: AC10 Each business rule of section 8 is covered by a criterion or a guardrail check (new, D-RCV-60)
    Given the business rules BR1 to BR9 of section 8
    When section 8 is compared with sections 7 and 16
    Then each of BR1 to BR9 is traced to a criterion of section 7 or to a guardrail or boundary check named in section 16

  Scenario: AC11 A retried or timed-out read answers 503 (new, D-RCV-60)
    Given a read of the ledger is retried or exceeds its 2 s budget
    When the operation is validated against AC1 and AC3
    Then the read answers 503 with MSG-GEN-006 and no other status or message identifier
    Then the retry count and the timeout value are Not specified in the source documents (NEWAC-RWB-P7-E1008-CON-AC11)
```

These criteria are new and test only the published baseline: no legacy acceptance criterion is repeated, AC1 to AC8 of RWB-E1-008 stay with RWB-P7-E1008-APP, and every identifier, field, path and value is the legacy or technical-specification value character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The ledger publishes two read operations on the service base and no write path; its rows are written by the ingest of the shared topic | Ownership Map (`GET /decision-log`, `GET /decision-log/{entryId}`); DP-03; Architecture v5 slides 14, 28 and 41 |
| BR2 | An entry carries the seven field groups of REQ-DRI-001, with the field identifiers and physical types of TSD P7 v2 T3.1 | REQ-DRI-001; DF-DEC-001 to DF-DEC-031 |
| BR3 | The page is ordered by `chain_seq` ascending, always, so a reader sees the chain in the order the verifier walks it | REQ-DRI-003; DF-DEC-028 |
| BR4 | The errors are RFC 9457 problem responses with the message identifier of the legacy contract; 403 carries MSG-P4-002 and 404 carries MSG-P4-003 | RWB-E1-008 section 12; Template and Rules §R7.2 |
| BR5 | The `DecisionRecorded` envelope is RWB-PLT-E1027-CON's; this contract consumes it and adds nothing to it | DP-03; Architecture v5 slides 20 and 42 |
| BR6 | The table is `decision_log_entry` in `rwb_decision`, owned by P7, with the library objects created there; no other owner's table is named | DP-01; DP-15; Ownership Map |
| BR7 | The decision codes and approval levels are rows of the P3 reference contract and never a list inside this document | DP-07; R-PREC default ruling |
| BR8 | A published version is never edited: a compatible change stays in major version 1 and a breaking change raises major version 2 with a new `ce_type` where the envelope changes | Template and Rules §R7.2; §R5.4 class C |
| BR9 | The contract declares no data-lake copy and no reporting table; reporting reads the events | DP-17; ADR-018 |

Coverage: BR1 by AC1 and TC-P7-E1008-CON-01; BR2 by AC2 and TC-P7-E1008-CON-02; BR3 and BR4 by AC3 and TC-P7-E1008-CON-03; BR5 by AC4 and TC-P7-E1008-CON-04; BR6 by AC5 and TC-P7-E1008-CON-05; BR7 by AC6 and TC-P7-E1008-CON-06; BR8 by AC7 and TC-P7-E1008-CON-06; BR9 by AC5 and TC-P7-E1008-CON-07.

### 9. State transitions

None in this story: a document has no runtime state. Two vocabularies are fixed here and implemented in RWB-P7-E1008-APP section 9 — the ingest states of an envelope (Received, Chained, Sealed, Refused, Repeated, Dead-lettered) and the chain-check states of a business date (Verified, Broken, Sealed).

| Object | State | Meaning in the contract |
|---|---|---|
| Contract version | v1 | The published version every consumer pins |
| Contract version | v2 | Raised by a breaking change; v1 stays readable and is never edited |
| Entry in a response | Present | The row exists in `rwb_decision` with its `chain_seq` and its two hashes |
| Entry in a response | Absent | The entry does not exist, or its case is outside the caller's scope; both answer 404 with MSG-P4-003 |
| Envelope | Accepted | `ce_type`, key and payload match section 12.4 and the ingest chains it |
| Envelope | Repeated | The `ce_id` is known; the first entry reference is answered and no row is written |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the shapes, the envelope section and the fakes |
| The service owner of rwb-decision | Approves a breaking change and freezes a version |
| The rwb-decision app story (RWB-P7-E1008-APP) | Implements the baseline and reports drift |
| The rwb-decision query story (RWB-P7-E2005-APP) | Extends the read with filters and SCR-38 under the same base and the same shapes |
| The rwb-case owner (P3) | Confirms the two reference operations the codes and levels are read from |
| The strict-mode waiters — debt sale, write-off, asset and litigation | Confirm the shape they read back before a point of no return |
| RW-AUDIT, RW-COE, RW-COMPLY | Audit the entries through the two operations, not through the document |
| No delegation of authority level applies | A contract is a technical artefact, not a credit decision |

No personal name, no e-mail address and no credential appears in the document, an example or a fake; a caller is a role code or a user reference only.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Business data published | None. The document publishes paths, field names, types, message identifiers and one legacy example | Not specified in the source documents (DOR-RWB-P7-E1008-CON-7) |
| Shapes published | `DecisionLogEntry` and `DecisionLogPage` of section 12.2, and the `DecisionRecorded` payload of section 12.4 | DF-DEC-001 to DF-DEC-031 |
| Personal data | The user references `approverUserId` and `actorUserId` are personal data; the entry names no name, account number, national identifier or document content, and names a case, a rule and a version | Not specified in the source documents (DOR-RWB-P7-E1008-CON-7) |
| Tables published | `decision_log_entry` in `rwb_decision` and the three library objects created in the same schema; the other owners' tables are named only to be excluded | Not specified in the source documents (DOR-RWB-P7-E1008-CON-7) |
| Field identifiers | DF-DEC-001 to DF-DEC-031, as in TSD P7 v2 T3.1 | DF-DEC-001 to DF-DEC-031 |
| Retention | The table is append-only and keeps every entry; the retention period is DL26's (open; assumptions ASM-0247, ASM-0264, ASM-0275, ASM-0355) and the daily seal keeps the last hash in immutable storage | Not specified in the source documents (DOR-RWB-P7-E1008-CON-7) |

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision`, base `/api/recovery/decision/v1`.

| Method | Path | Purpose | Authorisation | Errors |
|---|---|---|---|---|
| GET | `/decision-log` | Search the ledger by `caseId`, one page at a time, in `chain_seq` order; the read touches the ledger only, and an entry not yet collected by JOB-13 is shown as not yet sealed | Decision log, right R; scope through the authorise answer and the case read of rwb-case | 401; 403 MSG-P4-002; 503 MSG-GEN-006 |
| GET | `/decision-log/{entryId}` | Read one entry with its seven field groups, its versions and its two hashes | Decision log, right R; scope through the entry's case | 401; 403 MSG-P4-002; 404 MSG-P4-003; 503 MSG-GEN-006 |

No append operation is published: the Ownership Map gives P7 the two `GET` paths only, and the ledger is written by the ingest of `rwb.decision-record.v1` (BR1; GAP-1224; ASM-2188). Architecture v5 slide 14 names the ledger read `GET /decisions?caseId=`; this contract publishes the Ownership Map path `/decision-log` under the source precedence of Template and Rules §R3 and records the difference (GAP-1230; ASM-2194).

**DecisionLogEntry**

| Field | Type | Absent when | Field ID |
|---|---|---|---|
| `id` | uuid | never | DF-DEC-001 |
| `caseId` | uuid | the entry is an access event (decision code `AC-…`) | DF-DEC-002 |
| `decisionCode` | string(8) | never | DF-DEC-003 |
| `ruleId`, `ruleVersion` | string(20) | a decision taken without a rule | DF-DEC-004, DF-DEC-005 |
| `modelVersion`, `agentVersion` | string(40) | no model and no agent took part | DF-DEC-006, DF-DEC-007 |
| `inputsRef` | string(400) | never | DF-DEC-008 |
| `recommendation` | object | no recommendation was made | DF-DEC-009 |
| `approverUserId` | uuid | no person approved | DF-DEC-010 |
| `approvalLevel` | string(4) | no delegation level applied | DF-DEC-011 |
| `finalCall` | string(40) | never | DF-DEC-012 |
| `overrideReason` | string(1000) | the person followed the recommendation | DF-DEC-013 |
| `actions`, `outcome` | object | not known yet | DF-DEC-014, DF-DEC-015 |
| `decidedAt` | timestamp | never | DF-DEC-016 |
| `prevHash`, `entryHash` | string(64) | never | DF-DEC-017, DF-DEC-018 |
| `chainSeq` | integer | never | DF-DEC-028 |
| `correctsEntryId` | uuid | the entry corrects nothing | DF-DEC-029 |
| `actorUserId` | uuid | no actor reference was recorded | DF-DEC-030 |

`DecisionLogPage` carries `entries` (an array of `DecisionLogEntry`), `page`, `size` and `total`. The paging parameters `page` (default 1) and `size` (default 50) with their maximum of 200, and the precise error body beyond the five fields of RFC 9457, are Not specified in the source documents and are published as the working read (GAP-1229; ASM-2193).

#### 12.2 REST operations consumed

| Method | Path | Owner | Contract |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/LOV-DECISION` | P3 rwb-case | RWB-P3-E1043-CON |
| GET | `/api/recovery/case/v1/admin/lists/LOV-APPROVAL-LEVEL` | P3 rwb-case | RWB-P3-E1043-CON |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case contract of RWB-P3-E1018-CON, for the scope filter and the timeline reference |

The document declares the two reference operations because the decision code and the approval level are validated against them; the ledger stores the codes it receives and holds no list. The authorise answer is the guard library's (RWB-PLT-E1037-CON) and the contract names the answer it expects (allowed, or refused with MSG-P4-002) without declaring the access operation.

#### 12.3 Events published

None. The ledger publishes no event of its own: it consumes `rwb.decision-record.v1` and it announces a sealed entry on the same shared topic through the envelope of section 12.4, which is RWB-PLT-E1027-CON's and is not redefined here. The service topic `rwb.decision.events.v1` belongs to the approvals and the rule registry of this service — `ApprovalRequested`, `ApprovalDecided`, `RulePackageInForce` (Architecture v5 slides 14 and 42) — and this contract declares none of them.

#### 12.4 Events consumed

| Event | Topic | Producer | Ledger use |
|---|---|---|---|
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | all 19 services | The one input of the ledger: validated, deduplicated by `ce_id`, then chained |

| Envelope element | Value |
|---|---|
| Mode | CloudEvents 1.0, binary mode |
| ce_specversion | 1.0 |
| ce_type | rwb.decision.DecisionRecorded.v1 |
| ce_source | The producing service |
| ce_subject | The case ID where there is one, the entry id where there is not |
| Key | `caseId` where the record has a case, the entry id where it does not |
| ce_id and traceparent | The event identifier (the dedupe key, stored in `idempotency_key`) and the W3C trace context |
| Payload | Entry id, case ID where there is one, decision code, final call, rule ID, rule version, chain sequence, entry hash, actor reference, decided time |

The payload is the one of RWB-PLT-E1027-CON; this document restates the fields the ledger stores and adds none (BR5). The owner of every envelope element is RWB-PLT-E1027-CON, and the owner of the consuming ledger is rwb-decision.

#### 12.5 Workflows and activities

| Workflow or activity | Queue | Purpose |
|---|---|---|
| `DecisionChainCheckWorkflow` | `rwb-decision` | The 02:00 chain-check run of the ledger (JOB-14) |
| `verifyChainRange`, `raiseChainBreak`, `sendComplianceNotice`, `writeLedgerSeal` | `rwb-decision` | The four activities the run calls |

The contract names them because a strict-mode waiter and an operator both need to know that the verification is a Schedule at 02:00 and not a service call; their implementation is RWB-P7-E1008-APP's.

#### 12.6 Schedules

| Schedule | Cron | Owner | Job |
|---|---|---|---|
| `decision-log-chain-check` | 02:00 daily | rwb-decision | JOB-14 Hash-chain check (Architecture v5 slide 44) |

The legacy nightly copy to the data lake (RWB-E1-014, JOB-13 as a 01:00 batch) has no target: the ingest is continuous and the lake is removed (DP-17; GAP-1226 is the app story's record of the read).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The ledger row: the seven field groups, `chain_seq`, `prev_hash` and `entry_hash`, the correction reference and the idempotency key; append only |
| `outbox_event` | PLT library, created in `rwb_decision` by RWB-P7-E1008-DB | The sealed-entry announcement |
| `processed_event` | PLT library, created in `rwb_decision` by RWB-P7-E1008-DB | The dedupe of the ingest |
| `idempotency_key` | PLT library, created in `rwb_decision` by RWB-P7-E1008-DB | The stored answer of a repeated request at the edge |

**Named and excluded.** `delegation_limit` is P4 rwb-access and is read through its contract. `parameter_catalog`, `parameter_value`, `reference_row`, `reference_version` and `lov_value` are P3 rwb-case under DP-07. `approval`, `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7 but belong to other stories of this service. `recovery_case`, `task`, `timer` and `queue` are P3's. No foreign key, view or grant of this contract names another schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Ledger read fake | The two `GET` operations | A page in `chain_seq` order; one entry with the seven field groups; 403 with MSG-P4-002; 404 with MSG-P4-003; 503 with MSG-GEN-006 |
| DecisionRecorded fake | The shared topic of RWB-PLT-E1027-CON | One valid envelope, one repeated `ce_id`, one refused body, one envelope with no case |
| Reference fake | RWB-P3-E1043-CON | `LOV-DECISION` with `D6`, `LOV-APPROVAL-LEVEL` with `L1` to `L6` |
| Authorise fake | RWB-PLT-E1037-CON | Allowed, and a refusal with MSG-P4-002 |
| Case fake | The case contract of P3 | A case in scope, and a case out of scope for MSG-P4-003 |
| Seal target fake | Immutable storage | An accepted seal file, and a refused write |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 read operations under `/api/recovery/decision/v1` | 3: two reference lists and the case read of P3 | One hop, 2 s budget, behind gateway-bff (DP-19) |
| Kafka | 0 events declared as the ledger's own | 1 event type on the shared topic `rwb.decision-record.v1` | CloudEvents 1.0 binary mode; key `caseId` or entry id |
| Temporal | 1 workflow and 4 activities named | 0 | Queue `rwb-decision`, namespace `rwb-recovery`, one Schedule at 02:00 |
| File | 0 | 0 | The daily seal is the app story's and is named only |

### 13. Solution plan

**Package.** A contract artefact of the service: the OpenAPI 3.1 fragment of the two operations, the AsyncAPI 3.0 fragment of the consumed envelope, the JSON Schemas of `DecisionLogEntry` and `DecisionLogPage`, and the fake set, published from `th.co.scb.ace.workbench.recovery.decision.api`. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-1229; ASM-2193).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The contract declares `decision_log_entry` in `rwb_decision` only | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. This contract fixes the envelope the ledger consumes | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. The decision codes and approval levels are rows of two lists | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit. The chain check is a Schedule at 02:00 | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. The two operations are published on the decision base and the monolith base is not carried | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. The contract names the table, and the DB story creates it | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting. No copy is declared | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route. Both operations are one hop behind the gateway | H RWB-PLT-N001-CON |

The patterns **not claimed** here are DP-02, DP-04, DP-05, DP-06, DP-08 (the authorise answer is named, not declared), DP-09 (the library objects are created by the DB story and the platform contract is not a dependency of this contract), DP-11, DP-12, DP-14, DP-16, DP-18 and DP-20.

**Build steps**

1. Write the OpenAPI fragment of the two operations with their parameters, responses and the RFC 9457 errors (AC1, AC3).
2. Write the JSON Schemas of `DecisionLogEntry` and `DecisionLogPage` from TSD P7 v2 T3.1, with the absent-when rules and the legacy example (AC2).
3. Write the AsyncAPI fragment of the consumed envelope, taken from RWB-PLT-E1027-CON and not extended (AC4).
4. Write the owned-table section with the four rows and the exclusion list (AC5).
5. Generate the six fakes from the same examples and write the contract test (AC6).
6. Write the versioning section with a compatible and a breaking example (AC7).
7. Publish v1 and record the pinned version of the ledger implementation, the query API and each strict-mode waiter.

**Done when.** The document and the schemas validate, the fakes answer every criterion including the refusal, the repeat and the out-of-scope entry, the drift test is green on the build of RWB-P7-E1008-APP and of RWB-P7-E2005-APP, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P4-002 | A caller without Decision log R reads an entry | You cannot {action} here. Your role does not include it. | 403 in the problem body |
| MSG-P4-003 | The entry does not exist, or its case is outside the caller's scope | This case is not in your scope. | 404 in the problem body |
| MSG-GEN-006 | The ledger cannot be read | {system} is not available. Your request is queued and will be retried. | 503 in the problem body |
| MSG-P7-008 | The chain check finds a break (documented here for the waiter and the operator) | The decision log check for {date} found a break at entry {entryId}. Entries from that entry on cannot be relied on until Compliance reviews them. | The incident and the Compliance notice, not a response body |

The texts are copied unchanged from RWB-E1-008 and this contract adds no message identifier. Thai text follows DL10 (open; assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863).

### 15. Screens and states

No screen in this story and the contract declares none: the two operations are reached through gateway-bff (DP-19), the decision-log screen SCR-38 and its states belong to RWB-P7-E2005-APP, and the case timeline that shows an entry belongs to P3. What the contract fixes for a screen is the page order (`chain_seq` ascending), the paging contract and the two refusals a screen must display (MSG-P4-002 and MSG-P4-003). States of SCR-38: loading, as in Screen Specifications v1 section SCR-38; empty, error and no access are Not specified in the source documents (CG-ALL-6848).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P7-E1008-CON-01 | AC1 | Contract | The operation section linted: two paths under the decision base, owner `rwb-decision`, no write operation, no monolith base, one hop |
| TC-P7-E1008-CON-02 | AC2 | Contract | `DecisionLogEntry` validated field by field against TSD P7 v2 T3.1; the absent-when rules; the lengths; the legacy example with D6, R-UNI-14, UNI-2026.11, L6 and RW-2026-000123 |
| TC-P7-E1008-CON-03 | AC3 | Contract | One page with its order; the four errors with their identifiers; a parameter out of range answering 400; a personal-data scan of the examples |
| TC-P7-E1008-CON-04 | AC4 | Contract | One envelope validated against RWB-PLT-E1027-CON; the attribute set; the key with and without a case; `ce_id` as the dedupe key |
| TC-P7-E1008-CON-05 | AC5 | Contract | The owned-table section compared with the Ownership Map; the four owned objects; the exclusion list; the absence of a cross-schema key |
| TC-P7-E1008-CON-06 | AC6, AC7 | Component | The six fakes answering every example; the drift test on a consumer; a compatible change and a breaking change |
| TC-P7-E1008-CON-07 | AC5 | Contract | The four owned tables in `rwb_decision` and the named-and-excluded tables in their owners' schemas, with no cross-schema key, view or grant; no data-lake copy or reporting table |
| TC-P7-E1008-CON-08 | AC8 | Contract | The paging and error sections checked for any value no source names; each marked with GAP-1229 and ASM-2193 |
| TC-P7-E1008-CON-09 | AC9 | Contract | The paging defaults, the maximum page size and the error body checked against the sources; each marked with GAP-1229 and ASM-2193 |
| TC-P7-E1008-CON-10 | AC10 | Contract | Section 8 compared with sections 7 and 16; each of BR1 to BR9 traced to a criterion or a guardrail check |
| TC-P7-E1008-CON-11 | AC11 | Component | A read retried and a read over the 2 s budget; each answers 503 with MSG-GEN-006 and no other status or message identifier |

The legacy test cases of RWB-E1-008 are executed by RWB-P7-E1008-APP and RWB-ITG-E1008-ITG; these eight are the contract's own and no legacy identifier is renumbered.

### 17. Guardrails

- No business value in the contract: the decision codes and approval levels are values in force in the P3 reference data, and the only values this document fixes are the legacy example values.
- No personal data in a schema, an example, a fake or a log: an entry names a case, a user reference and a rule, and the scan fails the build otherwise.
- No write path and no write verb: the two operations are reads and the ingest of the shared topic is the only writer.
- No cross-schema key, view or grant in anything the document publishes; the boundary check fails the build.
- No redefinition of the shared envelope: a change to `DecisionRecorded` is a change in RWB-PLT-E1027-CON, not here.
- No list of decision codes, approval levels or limits inside the document (DP-07).
- No data-lake copy and no reporting table (DP-17).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | One record per decision with the seven field groups | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-01 | 17 Run the decision center | BR2 | TC-P7-E1008-CON-02 |
| REQ-DRI-002 | Append only; a correction is a new record naming the one it corrects | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-01 | 17 Run the decision center | BR1, BR6 | TC-P7-E1008-CON-01, TC-P7-E1008-CON-05, TC-P7-E1008-CON-07 |
| REQ-DRI-003 | Hash chained, checked, break reported to Compliance the same day | Epic 1, 3.7; Program, 5.7 | FEAT-DRI-01 | 17 Run the decision center | BR3, BR5 | TC-P7-E1008-CON-03, TC-P7-E1008-CON-04 |
| Legacy test set RWB-E1-008 | TC-E1-008-01, TC-E1-008-02, TC-E1-008-03, TC-E1-008-04, TC-E1-008-05, TC-E1-008-06, TC-E1-008-07, TC-E1-008-08, TC-E1-008-09, TC-E1-008-10 | Epic 1, 3.7 | FEAT-DRI-01 | 17 Run the decision center | The legacy rules R-UNI-24, R-UNI-39 and R-UNI-40 | Executed by RWB-P7-E1008-APP and RWB-ITG-E1008-ITG; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P7-E1008-APP | App development | H consumer: implements the two operations, the ingest and the chain against this baseline and its fakes |
| RWB-P7-E1008-DB | Database | X: creates the table and the library objects the baseline names |
| RWB-P7-E1008-OPS | DevOps | X: deploys the service and the Schedule the baseline names |
| RWB-P7-E2005-APP | App development | Extends the read with filters and SCR-38 under the same base and shapes |
| RWB-PLT-E1027-CON | Contract | The shared `DecisionRecorded` envelope and the local record this contract consumes |
| RWB-P3-E1043-CON | Contract | The two reference lists the codes and levels come from |
| RWB-PLT-E1037-CON | Contract | The authorise answer named in section 12.8 |
| RWB-PLT-N001-CON | Contract | The gateway-bff route both operations use |

### 19. Out of scope

- The implementation of the two operations, the ingest, the chain and the verification: RWB-P7-E1008-APP.
- The schema, the table, the trigger, the grants and the library objects: RWB-P7-E1008-DB.
- The pipeline, the configuration, the alerts and the seal job: RWB-P7-E1008-OPS.
- The query filters by approver, rule version and date, and the Decision log query screen SCR-38: RWB-P7-E2005-APP.
- The approvals, the delegation of authority and the approval screen: RWB-P7-E2013-APP and RWB-P7-E2014-APP.
- The rule registry and the rule version packages: RWB-P7-E1073-APP and the rule stories of this service.
- The local record and its writer in each service: RWB-PLT-E1027-CON and RWB-PLT-E1027-APP.
- The copy to the data lake and its manifest: RWB-E1-014, no target path (DP-17).
- Retention periods (DL26).
