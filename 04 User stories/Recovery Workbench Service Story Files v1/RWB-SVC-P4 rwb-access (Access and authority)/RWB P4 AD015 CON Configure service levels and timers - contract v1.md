# RWB-P4-AD015-CON Configure service levels and timers

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-AD015-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-AD-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-AD-015 for `rwb-access`. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the access-side half of the service-level load — an OpenAPI 3.1 document for the load, the approval and the read, the `ServiceLevelLoad`, `ServiceLevelRow` and `RunningTimerEffect` schemas, the state set, the error envelope and the message mapping, the three case-service operations, the own authorise operation and the parameters read declared as consumed with their owners, the statement that no timer is created and no workflow started here, the contract tables of section 12 and the contract fakes**, so that **the app story and the SCR-42 console build the whole-file gate and the four-eyes approval on Day 1 against a fixed document, while the version, the state, the timer rows and the clock stay `rwb-case`'s and no operation of that service is claimed here**.

The deliverable is a document and its fakes, nothing else: this story writes no business logic and no data.

### 2. Business rationale

Contract-first REST, one hop and a 2 second timeout is the decoupling decision of the target (DP-11; ADR-020). The legacy story wrote the service level into the monolith's own table and read it in the same module, so nothing outside that module had to know what a service level was; the load, the approval and the clock were one piece of code. In the target they are two services: administration accepts and approves the values, and the case service owns the version, the state and the clock, which is a durable Temporal timer inside its workflow rather than a job over a table (Architecture v5 slides 42 and 44).

That split only works if one document says, without ambiguity, what this service accepts, what it refuses, what it hands over, what it answers back and what it does not own. Three things decide whether the split holds: the whole-file refusal, because a partially applied service level would leave some states on old values and some on new; the effect list, because after the move to durable timers only the service holding the clock can say whether a running timer kept its due date; and the separation of duty, because a load and its approval are the act of two people and the document has to state which right opens which operation.

Agreed once and faked for the consumed operations, this baseline lets the app story build in parallel with P3, catches a change on the case side in a contract test rather than in an integration window, and fixes the shape of a refusal — every refused row with its field — before either side codes it. It also fixes the naming the checks require: schema `rwb_access`, base `/api/recovery/access/v1`, topic `rwb.access.events.v1`, task queue `rwb-access` in namespace `rwb-recovery` and package `th.co.scb.ace.workbench.recovery.access`.

### 3. Preconditions

- The service template and the naming library are available, so the base, the topic and the event names follow the platform rule rather than a local choice (R4; DP-13, DP-14).
- The platform error envelope, the RFC 9457 problem response and the `Idempotency-Key` rule on every POST are the platform baseline; where this document narrows them, it does so explicitly.
- The operations and their owners are taken from the ownership map only. `timer`, `recovery_case` and the service-level version are `rwb-case`'s, and the three case-service operations this document consumes are that service's; this document defines none of them.
- The API Specification v4 and TSD P4 v3 declare no `rwb-access` path for this gate — their inventory is the general reference-load pair API-P4-005 and API-P4-006 — so the three provided operations are new work and their paths are Not specified in the source documents (GAP-2277; ASM-3757).
- The service-level file format is Not specified in the source documents (GAP-2277; ASM-3758): the document declares the columns an accepted row must carry, and their exact names, order and delimiter are fixed at the contract review.
- The state code list, the working-day calendar and the escalation roles a row may name are Not specified in the source documents (GAP-2277; ASM-3760; ASM-3761).
- The shape of the effect the case service answers per running timer, the version label it stores and the parameter rows behind the four-eyes switch and the row and file limits are Not specified in the source documents (GAP-2277; ASM-3759; ASM-3760).
- Which right letters open the gate is a recorded conflict between the legacy permission table and TSD P4 v3 (GAP-2276; ASM-3763); the document names the letters once and the app story applies them.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document for the three administration operations of `rwb-access` with the shared components the service uses.
2. Declare `POST /admin/service-level-loads` with the multipart part `file`, the query `validFrom`, the `Idempotency-Key` header and the `Location` of the read on a created load.
3. Declare `POST /admin/service-level-loads/{loadId}/approve` with the decision form field and its own `Idempotency-Key`, and `GET /admin/service-level-loads/{loadId}` as the read.
4. Declare the `ServiceLevelLoad` schema with its six fields and the `effects[]` list, the `ServiceLevelRow` schema with the seven columns an accepted row carries, and the `RunningTimerEffect` schema with four fields per running timer and its two outcomes.
5. Agree the error envelope and the message mapping: 400, 401, 403, 404, 409, 422 and 503, one message ID per condition, with the 422 carrying every refused row and its field and the 409 carrying the four-eyes refusal.
6. Declare the consumed operations with their owners, one hop and the 2 second client budget: the three `rwb-case` service-level operations, the own authorise operation and the `rwb-case` parameters read.
7. State what this service does not do: no timer is created, paused or closed, no `recovery_case` row is read, no service-level version is stored and no workflow, activity or Schedule is registered.
8. Publish the nine contract sub-tables of section 12 and the contract fakes of 12.8.
9. Add the contract tests: schema validation, envelope validation, message mapping, the whole-file refusal shape, the consumed-operation list, the no-timer statement and drift detection between a fake and the document.
10. Tag the baseline and hand it to RWB-P4-AD015-APP, the SCR-42 console build and the P3 owner of the service-level and timer contract.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body, query field or multipart part fails schema validation | 400 or 422 with the error envelope and the failing pointer | MSG-GEN-001 | AC1, AC3 |
| X2 | A caller without the load, approval or read right | 403 with the error envelope and the refusal code | MSG-P4-002 | AC1, AC3 |
| X3 | The approver is the author of the load | 409 with the error envelope and the four-eyes code; the envelope declares the shape and the state it leaves | MSG-P7-002 | AC3 |
| X4 | One row of the file fails a check while the rest are valid | The document declares that the whole file is refused and that the refusal names every refused row and its field | MSG-GEN-001 | AC3, AC5 |
| X5 | The case service does not answer inside the 2 second budget | 503 declared on all three operations; no load and no approval is reported | MSG-P7-003 | AC3, AC4 |
| X6 | A field of the load, of a row or of the effect has no source definition | The property is marked with the placeholder and carried as a gap in the app story | None | AC2 |
| X7 | A contract fake drifts from the document | The contract test fails and the merge is blocked | None | AC6 |
| X8 | A document, an example or a fake carries a personal data field | The contract test fails: no name, no e-mail address and no personal field is declared | None | AC6 |
| X9 | The read names a load the case service does not hold | 404 with the error envelope; no empty answer is invented | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the ownership map, the platform envelopes and the own, P3 and platform contracts only |
| Negotiable | The column names of the file, the field names of the effect list and the screen field list are settled with the reference-data community and the case service owner; the operations, the schemas, the envelope and the no-timer statement are fixed |
| Valuable | Unblocks the app story and the SCR-42 console on Day 1 and keeps the clock, the timer rows and the version out of the `rwb-access` document |
| Estimable | One OpenAPI document, one envelope, one whole-file refusal shape, nine contract tables, seven fakes and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Access-side service-level load contract baseline for rwb-access

  Background:
    Given the service naming rule of the platform library is in force
    Given the access-side half of the legacy journey is the file gate, its approval and the read of the load

  Scenario: AC1 The OpenAPI 3.1 document describes the three administration operations (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-access is published
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the base /api/recovery/access/v1
    Then it declares POST /admin/service-level-loads, POST /admin/service-level-loads/{loadId}/approve and GET /admin/service-level-loads/{loadId} with the owner rwb-access
    Then the load declares the multipart part file, the query validFrom and the Idempotency-Key header, and the approval declares the decision field and its own Idempotency-Key
    Then the load names the load right, the approval names the approval right and the read names the read right
    Then all three declare 401 and 403, the load declares 409 and 422, the approval declares 404, 409 and 503, and the read declares 404

  Scenario: AC2 The load, the row and the effect are declared once (new, D-RCV-60)
    Given the ServiceLevelLoad, ServiceLevelRow and RunningTimerEffect schemas of the document
    Then ServiceLevelLoad carries loadId, rowCount, versionLabel, validFrom, state and effects
    Then ServiceLevelRow carries stateCode, allowedWorkingDays, warningAt, escalationAt, escalationRole, recomputeInstruction and validFrom
    Then RunningTimerEffect carries timerId, startedAt, dueDate and outcome, and outcome is one of kept and recomputed
    Then the state set the document names is LOADED and APPROVED, and every other state is declared as read from the case service
    Then no property of any schema is a name, an e-mail address or a personal field

  Scenario: AC3 Every failure is one envelope with one message (new, D-RCV-60)
    Given the error envelope component of the document
    Then every declared error response uses the same envelope with messageId, detail, instance and status
    Then the mapping names MSG-GEN-001 for validation, MSG-P4-001 for no session, MSG-P4-002 for an absent right, MSG-P7-002 for the four eyes and MSG-P7-003 for a record or case-service failure
    Then the 422 schema carries the refused rows with their row number and field
    Then the 409 schema carries the load id and the state the load keeps
    Then the wording of MSG-P7-002 is declared as Not specified in the source documents (GAP-2277; ASM-3764)

  Scenario: AC4 The five consumed operations are declared as consumed (new, D-RCV-60)
    Given the consumed-operation list of the document
    Then it names the load, the approval and the read of the case service, the own authorise operation and the parameters read of the case service
    Then each row names its owner and its base, rwb-case for four of them and rwb-access for the authorise operation
    Then each row states one hop, a 2 s timeout and a breaker, and no consumed operation is also declared as provided here

  Scenario: AC5 The document states that no timer and no case row is written here (new, D-RCV-60)
    Given the document and its description of what this service does not own
    Then it states that no timer is created, paused or closed, that no recovery_case, queue or task row is read and that no service-level version is stored
    Then it states that no workflow, activity or Schedule is registered on the rwb-access queue
    Then no path of the document names a table or a view of rwb_case

  Scenario: AC6 The fakes match the document and carry no personal data (new, D-RCV-60)
    Given the contract fakes of section 12.8
    When the contract tests compare every stub with the document
    Then every stub validates against its schema and every declared error status has a stub
    Then a stub that is changed without the document fails the drift test
    Then no example and no stub carries a name, an e-mail address or a personal field
```

These six criteria test the artefact only: the document, its schemas, its envelope, its consumed list, its no-ownership statement and its fakes. No business value is asserted here, and the legacy criteria of the journey are owned and proved by RWB-P4-AD015-APP.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The document follows the platform naming: base `/api/recovery/access/v1`, schema `rwb_access`, topic `rwb.access.events.v1`, event names `rwb.access.<Event>.v1`, queue `rwb-access` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.access` | R4; DP-13; DP-14 |
| BR2 | Every operation names exactly one owner and one right, and no operation of another service is declared as provided here | DP-11; ownership rows of P4; GAP-2276; ASM-3763 |
| BR3 | Every failure is one RFC 9457 envelope with one message ID, and the 422 names every refused row and its field | Template and Rules §R7.2 s17; legacy RWB-AD-015 messages; GAP-2277; ASM-3764 |
| BR4 | Every consumed operation is declared with its owner, one hop and a 2 second budget, and is stubbed by a fake | DP-11; GAP-2277; ASM-3757 |
| BR5 | The document states what it does not own: no timer, no case row, no version, no workflow and no Schedule | DP-01; DP-10; Architecture v5 slides 42 and 44 |
| BR6 | No example, stub or schema property carries personal data | Template and Rules §R7.2 s17; NFR-039; NFR-040 |
| BR7 | A fake that drifts from the document fails the build | DP-11; ASM-3757 |
| BR8 | The file columns, the effect fields, the version label and the parameter rows that have no source are marked with the placeholder and carried as one gap row for each story | Template and Rules §R9; GAP-2275; GAP-2277 |

These rules are contract-review statements: BR1, BR2, BR5 and BR6 are asserted by a linter over the published document; BR3 and BR4 are asserted by the contract tests against the fakes; BR7 is the drift test itself.

### 9. State transitions

The document declares two states of a load and reads the rest from its owner.

| From | Event | Condition | To |
|---|---|---|---|
| (none) | A valid file is accepted and stored by the case service | The load answers 201 | `LOADED` |
| (none) | A row fails a check | The gate refuses before the call | No load and no state; 422 |
| `LOADED` | An approval by a caller other than the author, recorded first | The approval answers 200 | `APPROVED` |
| `LOADED` | An approval by the author | The references are equal | Unchanged; 409 |
| `APPROVED` | The valid-from date arrives | None | In force, as the case service reports it |
| `APPROVED` | A later version is approved | None | `SUPERSEDED`, read from the case service |

Every state after `APPROVED` is declared as read from `rwb-case` and no transition of this document changes a case, a queue or a timer.

### 10. Authority

| Who | What they may do with this deliverable |
|---|---|
| The tech lead of `rwb-access` | Owns the document, its schemas and its fakes, and tags the baseline |
| The P3 owner of the service-level and timer contract | Agrees the consumed operations and their shapes; owns the version, the state and the clock |
| The SCR-42 console owner | Builds against the document and reports a gap rather than a local variation |
| The QA lead | Owns the contract tests and signs the baseline off |
| The security administrator role | Confirms that the rights named per operation are the rights of the legacy permission table or records the conflict |
| The reference data community | Agrees the file columns, the state code list and the calendar with the app story |
| No other party | This document grants no right to load, approve or read a service level; it only names the right each operation requires |

### 11. Data

| Datum | Where it appears in the baseline | Owner |
|---|---|---|
| `loadId`, `rowCount`, `versionLabel`, `validFrom`, `state`, `effects` | `ServiceLevelLoad` schema, request and response examples | P3 `rwb-case` for the stored values; the shape is this document's |
| `stateCode`, `allowedWorkingDays`, `warningAt`, `escalationAt`, `escalationRole`, `recomputeInstruction`, `validFrom` | `ServiceLevelRow` schema and the file example | This document declares the columns; the values are the reference data community's |
| `timerId`, `startedAt`, `dueDate`, `outcome` | `RunningTimerEffect` schema | P3 `rwb-case`; the clock is its durable Temporal timer |
| The right letter per operation | Operation description and the security block | The legacy permission table, with the conflict of GAP-2276 recorded |
| The error envelope and the message IDs | `Problem` component and one example per status | This document; the wording except MSG-P7-002 is copied from RWB-AD-015 |

No table of `rwb_access`, `rwb_case` or ACE is named in a path, an example or a stub. No personal data appears in the document, in an example or in a fake.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|---|
| POST | `/api/recovery/access/v1/admin/service-level-loads` | P4 `rwb-access` | multipart `file` and query `validFrom` | `ServiceLevelLoad` with `Location` of the read | 400, 401, 403, 409, 422, 503 | The load right | `Idempotency-Key` header |
| POST | `/api/recovery/access/v1/admin/service-level-loads/{loadId}/approve` | P4 `rwb-access` | form field `decision` | `ServiceLevelLoad` with `state` `APPROVED` and `effects[]` | 401, 403, 404, 409, 503 | The approval right | `Idempotency-Key` header |
| GET | `/api/recovery/access/v1/admin/service-level-loads/{loadId}` | P4 `rwb-access` | None | The fields and `effects[]` | 401, 403, 404, 503 | The read right | Not applicable |

The three paths are new work off the declared inventory, whose reference-load pair is API-P4-005 and API-P4-006 (GAP-2277; ASM-3757). The right letters are declared once, from the legacy permission table, with the conflict against the TSD P4 reference-data rights recorded (GAP-2276; ASM-3763).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/case/v1/admin/service-levels` | P3 `rwb-case` | The accepted file and `validFrom`; answers the load with its state and author reference |
| POST | `/api/recovery/case/v1/admin/service-levels/{loadId}/approve` | P3 `rwb-case` | Puts the version in force and answers the state and the effect per running timer |
| GET | `/api/recovery/case/v1/admin/service-levels/{loadId}` | P3 `rwb-case` | The load, its state and the effect list |
| POST | `/api/recovery/access/v1/authorise` | P4 `rwb-access` (this service) | The right check behind all three operations (DP-08) |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case` | The four-eyes switch and the row and file limits with the version in force (DP-06) |

The four `rwb-case` rows are declared as consumed only. Their paths and shapes are Not specified in the source documents (GAP-2277; ASM-3757; ASM-3759; ASM-3760); they are proposed names on the published bases of RWB-P3-E1028-CON and RWB-P3-E1042-CON and are fixed at the contract review.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | the load id | the load or approval entry of DP-03: action, load id, state codes, row count, version label, `validFrom`, caller reference and outcome |

Nothing is published on `rwb.access.events.v1`: that topic carries `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoaLimitChanged.v1`, and a service-level load changes neither. The breach event and the retired `TimerDue` are `rwb-case`'s and are not declared here.

#### 12.4 Events consumed

None. The approval is a command and the effect on the running timers is answered by the approval's own call and by the read; the document declares no subscription and no inbox.

#### 12.5 Workflows and activities

None. No workflow and no activity is declared or registered on the `rwb-access` queue: the clock is a durable Temporal timer inside `rwb-case`'s `CaseWorkflow` and the escalation is a signal there (Architecture v5 slides 42 and 44; Temporal and Drools Design slide 13). The five-minute timer check and the `TimerDue` event are retired and no Schedule replaces them.

#### 12.6 Schedules

None. This service owns one Schedule, the access review list (JOB-18), and its story is RWB-P4-AD008-APP. A service-level load is request-driven, so the document declares no Schedule.

#### 12.7 Tables owned

| Table | Owner | Use in this baseline |
|---|---|---|
| `role` | P4 (`rwb_access`) | Named as an escalation role must be one of its rows; read only |
| `permission` | P4 (`rwb_access`) | Named as the source of the load, approval and read letters; read only |
| `idempotency_key` | PLT library, created in `rwb_access` | Declared as the store of the `Idempotency-Key` answer (DP-09) |
| `outbox_event`, `processed_event` | PLT library, through DP-03 | Declared as the record and message store; no inbox use |

`timer`, `recovery_case`, `queue`, `task`, `lov_value`, `rule_row` and the `parameter_*` and `reference_*` tables are P3's and appear nowhere in the document as a read or a write (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs declared by the baseline |
|---|---|---|
| rwb-case service-level WireMock | RWB-P3-E1028-CON | A 201 load answer with load "SL-000042", 12 rows, version "SL-2027.01", `validFrom` 2027-01-01, state `LOADED`, author reference "U-7125"; a 422; a 503 and a timeout |
| rwb-case approval and read WireMock | RWB-P3-E1028-CON | A 200 approval with `APPROVED` and two effects, "T-9001" kept at 2026-12-15 09:00 and "T-9002" recomputed to 2026-12-20 09:00; a 409 when the version is no longer `LOADED`; a 200 and a 404 for the read |
| reference-data fake | RWB-P3-E1043-CON | The state code list with LIT_PACK, the working-day calendar in force on 15 December 2026, and an unknown state code |
| parameters fake | RWB-P3-E1042-CON | The four-eyes switch on, the row limit 500 and the file limit 2 MB |
| decision-record fake | RWB-PLT-E1027-CON | The append and the publish on `rwb.decision-record.v1`, including a forced failure |
| authorise and guard fake | RWB-P4-AD015-CON, RWB-P4-E1037-CON | A granted answer per right and a refused answer with MSG-P4-002 |
| gateway-bff composite route fake | RWB-PLT-N001-CON | The SCR-42 route that calls the three operations, one hop each |

Every stub validates against the schema of the document, every declared error status has a stub, and no stub carries a name, an e-mail address or a personal field.

#### 12.9 Call-type summary

| Call type | Count in this baseline | Detail |
|---|---|---|
| REST | Provided 3; consumed 5 | Base `/api/recovery/access/v1`; four `rwb-case` rows and the own authorise operation, one hop and 2 s each |
| Kafka | Published 0 own; 1 record type; consumed 0 | `DecisionRecorded` through DP-03 on `rwb.decision-record.v1`; nothing on `rwb.access.events.v1` |
| Temporal | 0 workflows, 0 activities | The clock is `rwb-case`'s durable timer in `CaseWorkflow`; nothing is declared here |
| File | One in, none out | The multipart service-level file, forwarded unchanged to `rwb-case` |

### 13. Solution plan

**Package.** The document is published with the service's API artefacts in `th.co.scb.ace.workbench.recovery.access`, module `access/servicelevel`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/access/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The document carries these six patterns as declarations rather than code: DP-03 names the record type and its topic, DP-05 names the own ACE view, DP-06 and DP-07 declare the two consumed contracts of `rwb-case`, DP-13 gives the base, and DP-19 names the composite route the console uses.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `openapi/access-service-level-v1.yaml` | OpenAPI 3.1 document | The three operations, the three schemas, the `Problem` component and the examples |
| Schema set | Components | `ServiceLevelLoad`, `ServiceLevelRow`, `RunningTimerEffect`, `Problem` |
| Consumed-operation list | Section of the document | The five rows of 12.2 with owner, budget and breaker |
| Ownership statement | Section of the document | What this service does not own, in the words of BR5 |
| Fake pack | WireMock stubs | The seven fakes of 12.8 |
| Contract test suite | Tests | Schema validation, envelope, message mapping, refusal shape, consumed list, no-timer statement and drift |

**Database and migrations.** None. The document names tables but creates none, and no Flyway file belongs to this story; the per-service sequence of DP-15 is the DB story's.

**Configuration and reference data.** The document declares the four-eyes switch, the row and file limits, the state code list and the calendar as values read through DP-06 and DP-07, and marks the rows that carry them as Not specified in the source documents (GAP-2277; ASM-3760; ASM-3761).

**Build steps**

1. The document skeleton with the base, the security block, the `Problem` component and the three paths.
2. The three schemas and their examples, with a contrast test that proves no personal field is declared.
3. The error mapping per status and message ID, with the 422 refusal shape and the 409 body.
4. The consumed-operation list with owner, one hop, 2 s and breaker, and the ownership statement of BR5.
5. The fake pack for the seven fakes, each stub validated against the document.
6. The contract test suite, including the drift test of AC6.

**Done when.** The document validates against OpenAPI 3.1; every operation declares its owner, its right and its errors; the three schemas are declared once; the five consumed rows are declared with their budgets; the ownership statement is present; and every fake validates and the drift test runs green.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-GEN-001 | A required part, field or column is empty, a value is not a whole number of working days, the warning or escalation order is broken, a state code or an escalation role is unknown, or a limit is exceeded | Enter {field}. | Declared on the 422 of the load; the app story produces it |
| MSG-P4-001 | The caller has no session | You have no Recovery Workbench role. Ask your team manager to request one. | Declared on 401 of all three operations |
| MSG-P4-002 | The caller holds no load, approval or read right | You cannot {action} here. Your role does not include it. | Declared on 403 of all three operations |
| MSG-P7-002 | The approver is the author of the load | Wording Not specified in the source documents (GAP-2277; ASM-3764) | Declared on 409 of the approval |
| MSG-P7-003 | The decision record cannot be written, or the case service cannot be reached inside 2 s | The action was not taken because the decision could not be recorded. Try again in a few minutes. | Declared on 503 of all three operations |

The envelope is one component: `messageId`, `detail` with its placeholders, `instance` and `status`. The 422 body carries the refused rows with their row number and field, and the 409 body carries the load id and the state the load keeps.

### 15. Screens and states

The document serves the service-level panel of SCR-42 Queues and service levels through the gateway-bff composite route of DP-19; it builds no screen and owns no field of the queue panel. Which service serves which panel of SCR-42 is Not specified in the source documents (GAP-2277; ASM-3762).

| Screen | State | What the baseline lets the console show |
|---|---|---|
| SCR-42 Queues and service levels | Empty | An empty list with a total of 0 and no error |
| SCR-42 Queues and service levels | Refused | The row numbers and fields of the 422, so the analyst corrects the file |
| SCR-42 Queues and service levels | Loaded, waiting for approval | The load id, the row count, the version label and `validFrom` |
| SCR-42 Queues and service levels | Approved | The state `APPROVED` and the effect list per running timer |
| SCR-42 Queues and service levels | Read | The same fields and effect list from the read |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-AD-015-CON-01 | AC1, BR1, BR2 | Contract | The published document validated against OpenAPI 3.1, with the base, the three paths, the owner, the rights and the declared error statuses |
| TC-AD-015-CON-02 | AC2, BR6 | Contract | The three schemas and their examples, with the property list of each and a scan for a personal field name |
| TC-AD-015-CON-03 | AC3, BR3 | Contract | One example per declared status, its `messageId`, the 422 refusal shape and the 409 body |
| TC-AD-015-CON-04 | AC4, BR4 | Contract | The consumed-operation list: five rows, owner per row and the 2 s budget |
| TC-AD-015-CON-05 | AC5, BR5 | Contract | The ownership statement and a scan of every path for a table or view of `rwb_case` and for a workflow or Schedule declaration |
| TC-AD-015-CON-06 | AC6, BR7 | Contract | The seven fakes validated against the document, the drift test and the personal-data scan of every stub |

The four legacy test cases TC-AD-015-01 to TC-AD-015-04 belong to the app slice, which owns the legacy criteria; no `-ITG` copy is written here, because the plan splits RWB-ITG-AD015-ITG from this legacy key.

### 17. Guardrails

- No business value in the document beyond the copied message wording and the legacy test values used as examples: a working day, a warning point, an escalation point, a role or a limit appears only as a schema property or an example, never as a default.
- No personal data in the document, the examples or the stubs: no name, no e-mail address and no party value. A scan is part of the contract tests.
- No read of another service's tables (DP-01): no path, example or stub names `timer`, `recovery_case`, `queue`, `task` or a `rwb_case` relation.
- ACE data only through the owner's contract or its own `v_ace_*` views: the document names `v_ace_iam_group` as the only ACE read of the gate (DP-05).
- One owner per operation: no operation of `rwb-case` or `rwb-decision` is declared as provided here, and the drift test blocks a fake that invents one.
- The clock is not declared here: no workflow, activity or Schedule appears on the `rwb-access` queue.
- The conflict on the right letters is visible in the document, so a reviewer sees it before either side codes.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-011 | Service levels per queue and status, warning thresholds and escalation targets are held as data | Program: case and workflow | ADM-01 | All recovery processes | BR2, BR5 | TC-AD-015-CON-01, TC-AD-015-CON-05 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Program: decision and rules | ADM-01 | All recovery processes | BR3 | TC-AD-015-CON-03 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned | Program: decision and rules | ADM-01 | All recovery processes | BR3, BR4 | TC-AD-015-CON-03, TC-AD-015-CON-04 |
| REQ-DRI-011 | A reference data service holds every versioned table with its valid-from and valid-to dates | Program: decision and rules | ADM-01 | All recovery processes | BR4 | TC-AD-015-CON-04 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the administrator | Program: access and authority | ADM-01 | All recovery processes | BR2 | TC-AD-015-CON-01 |

| Legacy reference | Where it is kept |
|---|---|
| The legacy endpoints of RWB-AD-015 and their rights | Sections 3, 10, 12.1; GAP-2276 and GAP-2277 |
| The legacy message table of RWB-AD-015 | Section 14; TC-AD-015-CON-03 |
| Screens SCR-42 and SCR-39 | Sections 15, 19 |
| The `timer` and `recovery_case` facts the journey touches, declared as not owned | Sections 11, 12.7, 17 |
| Legacy key RWB-AD-015, app slice RWB-P4-AD015-APP, contract slice RWB-P4-AD015-CON | Metadata, sections 3, 12 |

### 19. Out of scope

- The implementation of the gate: the parser, the row gate, the four-eyes gate, the client, the record writer and their tests are RWB-P4-AD015-APP's.
- The case service's half: the version store, the state, the effect computation and the clock are RWB-P3-E1028-CON's and RWB-P3-E1028-APP's.
- The parameters and reference-data contracts themselves: they are RWB-P3-E1042-CON and RWB-P3-E1043-CON and are declared here as consumed only.
- The rule-version operations of the same administration area (RWB-P4-AD011-APP, RWB-P4-AD012-APP) and the general reference-load approval of RWB-P4-AD010-APP.
- The queue panel of SCR-42 and its fields: the queue configuration journey is RWB-P4-AD014-APP.
- The console, the composite route and the screen design: they are the gateway-bff stories' and the design system's.
- The integration harness and the `-ITG` copies of the test cases: they belong to RWB-ITG-AD015-ITG.
- Deployment, migration and runbook work: no OPS or DB story is split from this legacy key in the plan.
