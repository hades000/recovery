# RWB-P4-E8015-CON Detect a broken hash chain in the decision log

**Version 3 changes.**

- MSG-P4-001 carries the English text of Error and Message Standard v6 (RD-P1-004).

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E8015-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P4-E8015-CON-16) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P4-E8015-CON-14); no signed epic design record found in 03 Requirements and specifications |
| Contract version | Major version 1 in the path `/api/recovery/access/v1`; OpenAPI 3.1 document `openapi/rwb-access-chain-checks-v1.yaml` |
| Patterns applied | DP03, DP06, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: contract slice of RWB-E8-015 for rwb-access: the chain-check document, its run and report schemas, the outcome set, the Schedule and workflow declarations and the five fakes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E8015-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 11 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the chain check of `rwb-access`: an OpenAPI 3.1 document for the on-demand run and the run report, the `ChainCheckRun` and `ChainCheckPage` schemas with their outcome set, the error envelope with its message IDs, the consumed authorise and parameters operations with their owners and their one-hop budget, the declared `chain-check-daily` Schedule, the declared `AccessChainCheckWorkflow` with its three activities, the declared `rwb.decision.DecisionRecorded.v1` message, the contract tables of section 12 and the five contract fakes**, so that **the app story, the gateway-bff composite route and the audit harness can build against one fixed shape on Day 1 without waiting for the library, the parameters contract or the platform workflow kit to be finished**.

This contract carries no legacy acceptance criterion: AC1 and AC2 of RWB-E8-015 belong to RWB-P4-E8015-APP, and the six criteria of section 7 test the document, the schemas, the outcome set, the declared workflow and Schedule, the envelope, the consumed declarations and the fakes.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy story drew the chain check in process, inside the module that held the decision log; in the target the check belongs to the service that wrote the entries, and three other parties build against its answer at the same time: the app story that implements the walk, the composite route that shows the breach on SCR-43 Roles and access, and the harness that records the evidence for REQ-DRI-003 and NFR-035.

Without a fixed shape each of them would invent one. The route would read an outcome field the service does not answer, the harness would assert a count the app story does not compute, and the first disagreement would appear in an integration window instead of in a contract test. The baseline fixes the four things all of them need: what a run is (window, counts, outcome, first broken entry, trigger and time), what a breach is (outcome `BROKEN` with the first entry that failed), what a refusal is (one envelope with MSG-P4-002 or MSG-P7-003), and what the service does not answer at all (no case id, no person, no chain entry of another service).

The baseline also fixes the naming the checks require: schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` for the service and `rwb.decision-record.v1` for the record, task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`. Two of its elements are not ownership-map rows — the two paths and the Schedule name — and both are carried in GAP-2293 and GAP-2296 with ASM-3799 and ASM-3804.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, the base path, the topic and the event names follow the platform rule rather than a local choice.
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19) that consumes this answer on SCR-43 Roles and access and merges it with the access log of RWB-P4-AD007-APP, one hop each.
- The platform error envelope and the CloudEvents 1.0 envelope are the platform baseline; where this document narrows them it does so explicitly.
- The run entry is an entry of the DP-03 library (RWB-PLT-E1027-CON); this document describes the entry as that library publishes it and adds no field.
- The owners of the consumed operations are taken from the ownership map: the authorise operation is P4 `rwb-access`'s own path, declared as consumed with the fake of RWB-P4-E1037-CON, and the parameters operation is P3 `rwb-case`'s under DP-06. The two chain-check paths are not ownership-map rows: no source names a chain-check endpoint, so this contract fixes them on the DP-13 base and the point is carried in GAP-2293 and ASM-3799. `GET /admin/roles` (API-P4-007), `GET /me/session` (API-P4-012) and `GET /admin/access-log` (API-P4-008) are other P4 stories' and are neither provided nor consumed here. No table of another service is named (DP-01).
- The workflow kit and the Schedule API are the platform's (RWB-PLT-WF, RWB-PLT-E1071-CON); the document declares the Schedule and the workflow by name and adds no element of its own (GAP-2296; ASM-3804).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document with the shared components used across the `rwb-access` operations: the security scheme, the problem envelope and the version fields.
2. Fix the two operations on the base `/api/recovery/access/v1`: `POST /admin/chain-checks` with no body and a required `Idempotency-Key`, and `GET /admin/chain-checks` with `outcome`, `page` and `size`.
3. Fix the `ChainCheckRun` schema: `checkId`, `outcome`, `entriesChecked`, `verifiedThrough`, `firstBrokenEntryId`, `windowFrom`, `windowTo`, `trigger`, `checkedAt` and `entryId`, and the `ChainCheckPage` schema with its `items`, `checkpointEntryId`, `page`, `size` and `total`.
4. Fix the outcome set as a closed enumeration of `CLEAN` and `BROKEN`, and state that `firstBrokenEntryId` is present when and only when the outcome is `BROKEN`, and that `verifiedThrough` is the last entry that verified.
5. Declare the `chain-check-daily` Schedule on the `rwb-access` queue with its cadence as a parameter row, and declare `AccessChainCheckWorkflow` with its three activities and their inputs and outputs.
6. Declare the `rwb.decision.DecisionRecorded.v1` message of a run on `rwb.decision-record.v1` with its key and its payload, and declare no `rwb.access.<Event>.v1` message.
7. Agree the error envelope and the message mapping for 401, 403, 422 and 503, with the business texts copied unchanged from the legacy story where the message already existed.
8. Declare the consumed authorise and parameters operations as consumed, each with its owner, one hop and the 2 s client budget.
9. Publish the contract tables of section 12 (nine sub-tables) and the five contract fakes, with the seeded chain fixture of any length and one variant with a broken link.
10. Add the contract tests: schema validation, the two schemas, the outcome set, the workflow and Schedule declarations, the message declaration, the envelope, the consumed declarations and drift detection between a fake and the document.
11. Tag the baseline and hand it to RWB-P4-E8015-APP, the composite route work of RWB-PLT-N001-CON and the wave 4 audit journey harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The document fails OpenAPI 3.1 validation | The pipeline fails and no baseline is tagged | None | AC1 |
| X2 | A declared operation names another service's base, path or owner | The review refuses the document; the operation is declared as consumed instead | None | AC1, AC5 |
| X3 | A response of 401, 403, 422 or 503 is declared without the envelope or without a message ID | The contract test fails | None | AC4 |
| X4 | A run field is declared without a source in the library entry or in the run store | The contract test fails and the field is carried as a gap instead of a value | None | AC2 |
| X5 | The outcome set carries a third value, or `firstBrokenEntryId` is declared as always present | The contract test fails | None | AC2 |
| X6 | The document declares a Schedule or an activity the platform kit does not provide, or a cadence as a constant | The review refuses the document | None | AC3 |
| X7 | A fake answers a path, a status or a payload the document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X8 | An example, a fake or a schema carries a name, an e-mail address, a case id or a personal field | The review and the pipeline refuse the document | None | AC6 |
| X9 | A consumed operation is declared without an owner, without the one-hop rule or without the 2 s budget | The contract test fails | None | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes, the DP-03 entry schema and the P4 and P3 contracts only |
| Negotiable | The field names of the run row and the filter name are settled with the app story and the screen route; the base, the outcome set and the envelopes are fixed by the target architecture |
| Valuable | Unblocks the app story, the composite route and the audit harness on Day 1, and keeps the central ledger and the chain of every other service out of this contract |
| Estimable | One OpenAPI document, two schemas, one outcome set, one Schedule declaration, one workflow declaration, one declared message, nine contract tables, five fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Chain-check contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the chain checked is the local decision-record chain of rwb-access and the central ledger is not part of this document

  Scenario: AC1 The OpenAPI 3.1 document describes the run and the report (new, D-RCV-60)
    Given the OpenAPI 3.1 document of the chain check is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/chain-checks and GET /admin/chain-checks with the owner rwb-access
    Then each operation names its security right, Platform administration R, and its error responses 401, 403 and 503, with 422 on the read
    Then no operation of another service is declared as provided by rwb-access, and GET /admin/roles, GET /me/session and GET /admin/access-log are absent from the provided set
    Then the document states that a schema change is additive within major version 1 and that a removed, renamed or retyped field is a new major version

  Scenario: AC2 The run and report schemas and the outcome set are fixed (new, D-RCV-60)
    Given the ChainCheckRun and ChainCheckPage schemas of the document
    When the schemas are checked against the run and report definitions of the document
    Then the run row carries checkId, outcome, entriesChecked, verifiedThrough, firstBrokenEntryId, windowFrom, windowTo, trigger, checkedAt and entryId
    Then outcome is a closed enumeration of CLEAN and BROKEN
    Then firstBrokenEntryId is required when the outcome is BROKEN and absent when it is CLEAN
    Then the page carries items, checkpointEntryId, page, size and total
    Then the document states that no run row carries a case id, a name, an e-mail address or a user reference

  Scenario: AC3 The Schedule and the workflow are declared and carry no constant cadence (new, D-RCV-60)
    Given the Schedule and workflow declarations of the document
    When the declarations are checked against the platform kit
    Then the chain-check-daily Schedule is declared on the queue rwb-access
    Then AccessChainCheckWorkflow is declared with the activities readCheckWindow, recomputeChainRange and recordCheckResult
    Then the cadence, the start time, the batch size and the page bounds are declared as parameter rows read through DP-06 and not as values
    Then no other Schedule and no other workflow is declared by this document

  Scenario: AC4 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    When a 401, 403, 422 or 503 response is produced by either operation
    Then the body is one RFC 9457 problem response carrying type, title, status, detail, instance, messageId and traceId
    Then 401 carries MSG-P4-001, 403 carries MSG-P4-002, 422 carries MSG-GEN-001 and 503 carries MSG-P7-003
    Then no operation declares a second error shape

  Scenario: AC5 The consumed operations are declared as consumed (new, D-RCV-60)
    Given the authorise operation and the parameters read this service calls
    When the consumed operations are checked against the ownership map
    Then POST /api/recovery/access/v1/authorise is declared as consumed with the owner P4 rwb-access
    Then GET /api/recovery/case/v1/admin/parameters is declared as consumed with the owner P3 rwb-case
    Then each carries one hop and the 2 s client budget with a breaker
    Then no operation owned by rwb-decision, rwb-case, rwb-comms or rwb-document is declared as provided by rwb-access

  Scenario: AC6 The record message and the fakes match the document and carry no personal data (new, D-RCV-60)
    Given the event declaration and the five contract fakes of the baseline
    Then rwb.decision.DecisionRecorded.v1 is declared on the topic rwb.decision-record.v1 with the entry id as its key
    Then no rwb.access.AccessPolicyChanged.v1 and no rwb.access.DoaLimitChanged.v1 is declared by this document
    When the fakes are run against the document
    Then every fake answers only paths, statuses and payloads the document declares
    Then a fake that drifts from the document fails the build
    Then no schema, example or fake carries a name, an e-mail address, a case id or a personal field

  Scenario: AC7 The document names no table of another service and no central ledger (new, D-RCV-60)
    Given the tables this service owns are listed in the baseline document
    When the document is searched for table and view names
    Then it names only the local decision-record table, the checkpoint row, idempotency_key and the DP-03 outbox
    Then no decision_log_entry, parameter table, list table, case, task or rule_row view and no central ledger is named

  Scenario: AC8 A retried or timed-out activity is bounded by parameter rows (new, D-RCV-60)
    Given an activity of AccessChainCheckWorkflow fails or exceeds its time limit
    When the workflow retries the activity
    Then the retry count and the time limit are read as parameter rows through DP-06 and not as values
    Then the run row is written once per run and carries no outcome outside CLEAN and BROKEN

  Scenario: AC9 A status change outside the closed outcome set is refused (new, D-RCV-60)
    Given a chain-check run row is written with an outcome
    When an outcome other than CLEAN or BROKEN is written to the run row
    Then the write is refused and no row is stored with that outcome

  Scenario: AC10 Every error of a provided operation carries a declared status (new, D-RCV-60)
    Given the provided operations POST /admin/chain-checks and GET /admin/chain-checks
    When an error response of either operation is produced
    Then its status is one of 401, 403, 422 or 503 as declared in AC1 and no other status is declared
    Then the body is the problem envelope of AC4

  Scenario: AC11 A replay of a write with the same idempotency key records no second run (new, D-RCV-60)
    Given a POST /admin/chain-checks has been answered for an idempotency key
    When the same write is replayed with the same idempotency key
    Then no second run row is recorded for that key
    Then the replay is answered from the stored idempotency_key
```

These eleven criteria test the artefact only. No criterion restates a legacy acceptance criterion; AC1 and AC2 of RWB-E8-015 belong to RWB-P4-E8015-APP.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One REST base per service: `/api/recovery/access/v1`; a document never declares another service's path | DP-13; Architecture v5 slide 41 | AC1 / TC-E8-015-CON-01 |
| BR2 | A consumed operation is described as consumed, never as provided; its owner comes from the ownership map | DP-11; Ownership Map v1 | AC5 / TC-E8-015-CON-05 |
| BR3 | Error responses use one envelope and one message ID per condition; the business texts are copied unchanged from the legacy story | Architecture v5 slide 11; Template and Rules §R7.2 s14 | AC4 / TC-E8-015-CON-04 |
| BR4 | The run entry is the decision-record entry of DP-03: the contract describes it and adds no field | DP-03; RWB-PLT-E1027-CON | AC2, AC6 / TC-E8-015-CON-02, TC-E8-015-CON-06 |
| BR5 | The contract declares no table of another service and no central ledger; the chain of every other service and `decision_log_entry` are P7's | DP-01; ASM-3798 | AC5, AC7 / TC-E8-015-CON-05, TC-E8-015-CON-07 |
| BR6 | The outcome set is closed: `CLEAN` and `BROKEN`, with `firstBrokenEntryId` only on a breach and `verifiedThrough` the last entry that verified | RWB-E8-015 AC1; DP-03 | AC2 / TC-E8-015-CON-02 |
| BR7 | The cadence, the start time, the batch size and the page bounds are parameter rows behind the contract, never values in the document or in code | DP-06; BR-P4-026 | AC3 / TC-E8-015-CON-03 |
| BR8 | A schema change is additive within major version 1; a removed, renamed or retyped field is a new major version | Architecture v5 slide 42 | AC1 / TC-E8-015-CON-01 |
| BR9 | No personal data in a schema, an example or a fake: entry ids, counts, outcome codes, role codes, versions and times only | NFR-040 | AC2, AC6 / TC-E8-015-CON-02, TC-E8-015-CON-06 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the two schemas, the outcome set, the Schedule, the workflow, the message and the consumed operations are described | In review |
| In review | Consumer sign-off | The app story, the composite route and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1 | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or the outcome set changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A parameter row changes | A new cadence, batch size or page bound is in force | Baselined, with no document change |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-access | Owns the document, the two schemas, the outcome set, the declarations and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and a change to the outcome set |
| Internal audit (RW-AUDIT) | Reviews the run and report fields against what the control must prove, and the filter the report offers |
| Platform workflow owner | Reviews the `chain-check-daily` Schedule and the three activities as the kit declares them |
| Tech lead of rwb-case (P3) | Reviews the parameters operation as rwb-access uses it; owns its definition |
| Owner of the gateway-bff contract | Reviews the answer as the composite route consumes it, and confirms that no chain of another service is declared |
| Data steward | Confirms that no personal data field is declared in the schemas, the examples or a fake |

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Run row | `checkId`, `outcome` (`CLEAN` or `BROKEN`), `entriesChecked` (whole number), `verifiedThrough` (entry id), `firstBrokenEntryId` (entry id, on a breach), `windowFrom` and `windowTo` (entry ids), `trigger` (`SCHEDULED` or `ON_DEMAND`), `checkedAt` (timestamp), `entryId` (the decision-record entry of the run) | Not specified in the source documents (DOR-RWB-P4-E8015-CON-7) |
| Report page | `items[]` of the run row, `checkpointEntryId`, `page`, `size`, `total` | Not specified in the source documents (DOR-RWB-P4-E8015-CON-7) |
| Record entry | The decision-record entry of DF-DEC-001 to DF-DEC-018: `decision_code` DF-DEC-003 with the library's chain-check code, `case_id` DF-DEC-002 empty, `inputs_ref` DF-DEC-008 with the run row, the parameter version and the library's algorithm version, `decided_at` DF-DEC-016, `prev_hash` DF-DEC-017 and `entry_hash` DF-DEC-018 | DF-DEC-001 to DF-DEC-018 |
| Refusal | `messageId` MSG-P4-001, MSG-P4-002, MSG-GEN-001 or MSG-P7-003 with the detail text and the instance | Not specified in the source documents (DOR-RWB-P4-E8015-CON-7) |

The record code of a chain check, the order and batch of the walk, the start time of the Schedule and the same-day channel to Compliance are Not specified in the source documents (GAP-2294; ASM-3801); the schema of this contract fixes the run-row field names and the outcome set before the paths are frozen, and the app story reads and writes them as the document publishes them. The two paths themselves are not ownership-map rows (GAP-2293; ASM-3799).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-access (P4); base `/api/recovery/access/v1`.

| Method | Path | Documented shape | Access |
|---|---|---|---|
| POST | `/admin/chain-checks` | No body; `Idempotency-Key` header required as the idempotency key of the write. Answer: the run row of section 11 with `trigger` `ON_DEMAND`, and the `Location` of the report | Platform administration R |
| GET | `/admin/chain-checks` | Query `outcome` (`CLEAN` or `BROKEN`), `page`, `size`. Answer: the report page of section 11 | Platform administration R, scope applied |

The full paths are `/api/recovery/access/v1/admin/chain-checks` for both operations, on the base of DP-13. Errors: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 422 a page bound (MSG-GEN-001, read only) and 503 the run cannot be recorded or a parameters row is missing (MSG-P7-003). The write answers 201 and never 202; the read carries no `Idempotency-Key` and the document states it so that no consumer sends the header. Major version 1 sits in the path; an additive field within version 1 is a compatible change, and a removed, renamed or retyped field is a new major version tested against the registry with BACKWARD compatibility (BR8).

The provided set of this document is two operations on one path. `GET /admin/roles` is API-P4-007 of RWB-P4-E1019-APP, `GET /me/session` is API-P4-012 and `GET /admin/access-log` is API-P4-008 of RWB-P4-AD007-APP; none of them appears as provided here, and the legacy `POST /admin/rule-versions` and its approve path are not declared at all because the rule registry is `rwb-decision`'s (GAP-2295).

#### 12.2 REST operations consumed

One hop per call, 2 s timeout and a breaker per downstream (DP-11).

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Platform administration R check behind both operations, cached for the session |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The cadence, the start time, the batch size and the page bounds, with the version in force (DP-06) |

Neither is declared as provided by rwb-access, and no operation of `rwb-decision`, `rwb-comms` or `rwb-document` appears in the document at all: the central ledger and its chain check are P7's and the chain walked is this service's own.

#### 12.3 Events published

| Event | Topic | Owner | Contract element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | The entry of a run with the window, the counts, the outcome, the first broken entry, the trigger, the parameter version and the algorithm version, with its `prev_hash` and `entry_hash`, in the CloudEvents 1.0 envelope |

This document declares the record message only. `rwb.access.AccessPolicyChanged.v1` belongs to RWB-P4-E1037-APP and `rwb.access.DoaLimitChanged.v1` to RWB-P4-E8008-APP; neither is declared here, and the service publishes no other event of the chain check.

#### 12.4 Events consumed

None. `rwb-access` subscribes to no topic for this capability: the run is started by its own Schedule or by its own request, and the document declares no subscription.

#### 12.5 Workflows and activities

| Element | Kind | Queue | Declared use |
|---|---|---|---|
| `AccessChainCheckWorkflow` | Workflow | `rwb-access` | One run: window, walk, result, checkpoint |
| `readCheckWindow` | Activity | `rwb-access` | Input: the business date; output: the window, the checkpoint and the chain head |
| `recomputeChainRange` | Activity | `rwb-access` | Input: the window and the batch size; output: the entries checked, `verifiedThrough` and optionally `firstBrokenEntryId` |
| `recordCheckResult` | Activity | `rwb-access` | Input: the run row; output: the entry id and the moved checkpoint |

Namespace `rwb-recovery`. The document declares the three activities and their inputs and outputs so that the app story and the harness agree on the evidence, and it declares no retry policy of its own: the retry is the kit's.

#### 12.6 Schedules

| Schedule | Queue | Cadence | Declared use |
|---|---|---|---|
| `chain-check-daily` | `rwb-access` | Daily, from the parameter row in force with its version; the start time is a parameter row | The daily check of REQ-DRI-003 and NFR-035 |

The cadence is declared as a reference to the parameter row and never as a value (BR7); the same Schedule starts an on-demand run only through the request of section 12.1, which uses the same workflow definition.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| the local decision-record table of the DP-03 library | P4 (rwb_access) | The entry the document describes and the report reads |
| the checkpoint row of this service | P4 (rwb_access) | The `checkpointEntryId` the report answers |
| `idempotency_key` | Platform library, in `rwb_access` | The on-demand request row |
| `outbox_event` | Platform library, in `rwb_access` | The record row of the entry |

No table of another service is named in the contract (DP-01): `decision_log_entry` is P7 `rwb_decision`'s, the parameters and lists are P3's, and no view of `case`, `task` or `rule_row` is named.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| authorise fake | `POST /authorise` with a granted answer for RW-AUDIT, RW-PLATADM, RW-SECADM, RW-DATASTEW, RW-COE and RW-COMPLY with Platform administration R, and a refused answer with MSG-P4-002 for RW-PHONECOL | App story, contract tests, harness |
| parameters fake | `GET /admin/parameters` with the cadence, the start time, the batch size and the page bounds as rows and the version in force | App story, contract tests |
| decision-record fake | The append of a run entry with its `prev_hash` and `entry_hash`, the hash-link check, the canonical form and a forced failure | App story, contract tests |
| chain fixture | A seeded chain of any length, one variant with a broken link at a named entry and one clean variant | App story, contract tests, harness |
| gateway-bff fake | The SCR-43 Roles and access route: the breach list of this answer merged with the access log of RWB-P4-AD007-APP, one hop each | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The run and the report provided; the authorise and the parameters reads consumed; one hop, 2 s timeout |
| Kafka | 1 published, 0 consumed | `rwb.decision.DecisionRecorded.v1` through the DP-03 outbox |
| Temporal | 1 workflow, 3 activities, 1 Schedule | Declared on queue `rwb-access`; `chain-check-daily` |
| File | 0 | No file input and no file answer |

### 13. Solution plan

**Deliverables.** `openapi/rwb-access-chain-checks-v1.yaml` (OpenAPI 3.1) with the two operations and the shared components, `contract/error-envelope.yaml`, the `ChainCheckRun` and `ChainCheckPage` schemas with their examples, the `CLEAN` and `BROKEN` examples, the AsyncAPI fragment that declares `rwb.decision.DecisionRecorded.v1` for a run, the Schedule and workflow declaration fragment, the versioning rules and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/access/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the build dependency of the owning story; this story is Day 1 by rule and carries no H and no C of its own. The workflow kit and its Schedule API are a platform prerequisite of the declared Schedule and are not in this story's metadata list (GAP-2296; ASM-3804).

**Build steps**

1. OpenAPI 3.1 skeleton with the base path, the security scheme, the problem responses and the shared components; schema lint in the pipeline.
2. The two operations with the shape of section 11; the run row, the report page and the filter.
3. The outcome set and the two conditional fields: `firstBrokenEntryId` on a breach only, `verifiedThrough` always.
4. The Schedule and workflow declarations with the three activities, their inputs and outputs.
5. The message declaration of `rwb.decision.DecisionRecorded.v1` with its key, its payload and the library's chain-check code.
6. The consumed operations with their owners, the one-hop rule and the 2 s client budget.
7. The error envelope and the message mapping, with the business texts copied unchanged from the legacy story.
8. The five fakes and the chain fixture of section 12.8.
9. The six contract tests; a drift between a fake and the document fails the build.
10. Baseline tag and the consumer sign-off note from the app story, the screen route and the harness.

**Feature switch.** The run is switched by the service baseline of this contract and by the cadence parameter row; the document declares no 404 branch of its own and adds no flag.

**Done when.** The document validates in the pipeline, the six contract tests pass, the five fakes answer every declared path, the Schedule and workflow declarations match the kit, and the app story, the screen route and the harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A role without Platform administration R calls either operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field or page bound has no valid value in the rows in force | Enter {field}. |
| MSG-P7-003 | The entry of the run cannot be written, or a version the run needs is missing | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-004 | A break-glass grant is active for the caller | Emergency access is on until {time}. Every action is recorded. |

The message IDs are contract elements; the text is the agreed text taken from the legacy story RWB-E8-015, where all five messages already exist. The document declares the 401, the 403, the 422 and the 503 of these operations and no other error shape; MSG-P4-004 is declared as the warning header of the session, not as an error.

### 15. Screens and states

| Screen | State | Contract element the screen consumes |
|---|---|---|
| SCR-43 Roles and access, audit panel | Day clean | The latest run row with outcome `CLEAN`, `entriesChecked`, `verifiedThrough` and `checkedAt` |
| SCR-43 Roles and access, audit panel | Breach | The run row with outcome `BROKEN`, `firstBrokenEntryId` and `verifiedThrough`, and the report filtered to `outcome=BROKEN` |
| SCR-43 Roles and access, audit panel | Running | The run in flight with `trigger` `ON_DEMAND` and the `checkpointEntryId` it started from |
| SCR-43 Roles and access, audit panel | Refused | The 403 of the envelope with MSG-P4-002 and no row |
| SCR-43 Roles and access, audit panel | Not recorded | The 503 of the envelope with MSG-P7-003 and no row |
| SCR-43 Roles and access, audit panel | Break-glass warning | The warning of the session read, shown as the MSG-P4-004 banner over the panel |
| SCR-43 Roles and access, audit panel | Empty | Not specified in the source documents (CG-ALL-5620) |
| SCR-43 Roles and access, audit panel | Loading | Not specified in the source documents (CG-ALL-5620) |
| SCR-43 Roles and access, audit panel | Error | Not specified in the source documents (CG-ALL-5620) |
| SCR-43 Roles and access, audit panel | No access | Not specified in the source documents (CG-ALL-5620) |
| SCR-39 Rules and parameters | Empty | Not specified in the source documents (CG-ALL-5618) |
| SCR-39 Rules and parameters | Loading | Not specified in the source documents (CG-ALL-5618) |
| SCR-39 Rules and parameters | Error | Not specified in the source documents (CG-ALL-5618) |
| SCR-39 Rules and parameters | No access | Not specified in the source documents (CG-ALL-5618) |
| SCR-41 Delegation of authority | Empty | Not specified in the source documents (CG-ALL-5619) |
| SCR-41 Delegation of authority | Loading | Not specified in the source documents (CG-ALL-5619) |
| SCR-41 Delegation of authority | Error | Not specified in the source documents (CG-ALL-5619) |
| SCR-41 Delegation of authority | No access | Not specified in the source documents (CG-ALL-5619) |

The panel is served by the gateway-bff composite route (DP-19), which calls this read and the access log of RWB-P4-AD007-APP in parallel, one hop each, and merges the answers. The composite route specification and the screen field list belong to RWB-PLT-N001-CON and to the Epic 8 screen work; the document fixes the chain-check side of the merge only. The legacy screens SCR-39 Rules and parameters and SCR-41 Delegation of authority are not part of this feature (GAP-2295).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-015-CON-01 | AC1 | Contract | The document validates; the base, the two provided operations, Platform administration R and the four error responses are present; no foreign operation is provided; the additive-change rule of major version 1 is stated |
| TC-E8-015-CON-02 | AC2 | Contract | The run and report fields, the closed outcome set, the conditional `firstBrokenEntryId`, and no case id and no person in either schema |
| TC-E8-015-CON-03 | AC3 | Contract | The `chain-check-daily` Schedule on queue `rwb-access`, the workflow with its three activities, and the cadence, start time, batch size and page bounds as parameter references |
| TC-E8-015-CON-04 | AC4 | Contract | A 401, 403, 422 and 503 response carry one problem envelope with a valid message ID |
| TC-E8-015-CON-05 | AC5 | Contract | Two consumed operations with their owners P4 and P3, one hop and the 2 s budget; none declared as provided |
| TC-E8-015-CON-06 | AC6 | Component | The record message on `rwb.decision-record.v1` with its key; the five fakes match the document; a drifted fake fails the build; no name, e-mail address, case id or personal field |
| TC-E8-015-CON-07 | AC7 | Contract | Only the four owned tables are named; no decision_log_entry, parameter or list table, no case, task or rule_row view and no central ledger |
| TC-E8-015-CON-08 | AC8 | Component | A retried activity and a timed-out activity: retry count and time limit read as parameter rows; one run row per run with no outcome outside CLEAN and BROKEN |
| TC-E8-015-CON-09 | AC9 | Contract | An outcome other than CLEAN or BROKEN is refused and no row is stored with it |
| TC-E8-015-CON-10 | AC10 | Contract | Error responses of both operations carry only 401, 403, 422 or 503, each as the problem envelope; no other status is declared |
| TC-E8-015-CON-11 | AC11 | Component | A replayed write with the same idempotency key records no second run row |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The eleven rows test the artefact and are the contract story's own; the four legacy rows TC-E8-015-01 to TC-E8-015-04 stay with RWB-P4-E8015-APP, which owns AC1 and AC2, so this story restates none of them (ASM-3805). No `-ITG` id appears in this table, because no integration slice is split from this key.

### 17. Guardrails

- No business value in the contract: the cadence, the start time, the batch size and the page bounds are parameter rows behind the document, and the record code is the library's (BR7).
- No personal data in a schema, an example or a fake: entry ids, counts, outcome codes, role codes, versions and times only (BR9).
- The contract names only `rwb-access` tables and only operations owned by `rwb-access`; the central ledger, the chain of every other service and the parameters are consumed or absent, never named as this service's (DP-01, BR5).
- One REST base and one topic per service; a document that names another service's base or topic fails the review (DP-13).
- Every example in the document is synthetic; no production entry, no production hash and no personal payload is copied into a schema or a fake.
- The document declares one path, two operations and no chain of another service, so no consumer can read a verdict the service did not reach (BR6).
- The error envelope and the CloudEvents envelope come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-002 | The decision log is append only; a record cannot be changed or deleted | The run row is one append of the DP-03 entry, and the document declares no update and no delete path | TC-E8-015-CON-02, TC-E8-015-CON-06 |
| REQ-DRI-003 | The decision log is hash chained and the chain integrity is checked every day, with a break reported to Compliance the same day | The `chain-check-daily` Schedule, the outcome set, `firstBrokenEntryId` and the report the Compliance role reads | TC-E8-015-CON-02, TC-E8-015-CON-03, TC-E8-015-CON-06 |
| NFR-035 | The decision log hash chain is checked daily, and a break is reported to Compliance the same day | The daily Schedule and the 503 with MSG-P7-003 when the run cannot be recorded | TC-E8-015-CON-03, TC-E8-015-CON-04 |
| REQ-ACA-007 | Access requested outside the authority matrix is refused and the refusal is recorded | Platform administration R on both operations and the 403 with MSG-P4-002 in the envelope | TC-E8-015-CON-01, TC-E8-015-CON-04 |

The requirement IDs are the four rows this story serves; each is taken from the Program BRD and the FSD P4 v3 requirements table under the fill order of Template and Rules §R7.3, because the Work Package carries no requirement list for this story.

### 19. Out of scope

- The implementation of the walk, the run and the report (RWB-P4-E8015-APP).
- The central decision ledger, its chain and its 02:00 check (RWB-P7-E1008-APP), and the decision log query API (RWB-P7-E2005-APP); neither is defined or called here.
- The access log writer and its read `GET /admin/access-log` (RWB-P4-AD007-APP), the break-glass grant (RWB-P4-AD006-APP) and the access event (RWB-P4-E1039-APP).
- `GET /admin/roles` (RWB-P4-E1019-APP) and `GET /me/session`; neither is defined here.
- The rule-version operations and the data table of the legacy story: the rule registry is `rwb-decision`'s (RWB-P4-E8007-APP, RWB-P4-AD011-APP, RWB-P4-AD012-APP).
- The reference-data and parameter administration of the same module (RWB-P4-AD009-APP, RWB-P4-AD010-APP) and the access review Schedule JOB-18 (RWB-P4-AD008-APP).
- The workflow kit, the namespace and the Schedule API themselves (RWB-PLT-E1071-CON), the parameters client (RWB-PLT-E1042-CON) and the composite route (RWB-PLT-N001-CON).
- The schema migration, the indexes and the grants; the deployment, the Helm chart, the topic subscription, the dashboards and the runbook.
- The cross-service journey harness and its evidence.
