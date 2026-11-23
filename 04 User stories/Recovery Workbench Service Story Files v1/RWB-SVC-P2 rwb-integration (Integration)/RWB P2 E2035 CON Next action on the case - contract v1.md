# RWB-P2-E2035-CON Next action on the case - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2035-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-035 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-WKM-012, REQ-WKM-013, REQ-WKM-016, REQ-WKM-014, REQ-WKM-015) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-035 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-integration side of the next action fixed as a contract: the three operations with their paths, shapes, rights and errors; the consumed contracts of rwb-case, rwb-access and rwb-decision with their two shapes of read; the split between the compute here and the write there; the `NextActionCheckWorkflow` and its activities; the `next-action-check` Schedule; the `job_catalog` row and the `decision_record` library table; and the contract fakes**, so that **the app and operations stories of this key, the case transition of `RWB-P3-E2035-APP` and the integration harness build on Day 1 against one agreed, testable shape**.

The legacy story held the resolution, the field writes, the read endpoint and the JOB-05 step in one module and placed the read at `GET /cases/{caseId}/next-action` in the P3 backlog of the API Specification. Under D-RCV-60 the resolution is a service of rwb-integration and the case row stays with rwb-case. This contract fixes the seam between them: the resolve is side-effect free and returns the four values, the fill writes them through the rwb-case contract, and the case transition of `RWB-P3-E2035-APP` consumes the resolve inside its own transaction boundary while rwb-case keeps the write, the optimistic lock and the task lifecycle.

The Ownership Map keeps `GET /cases/{caseId}/next-action` with P3 while this work package assigns the story to rwb-integration. This document reconciles the two: the path is served by rwb-integration under its own base `/api/recovery/integration/v1` (DP-13), rwb-case keeps the case record and the write, and the conflict is carried in GAP-0668 and ASM-1178 rather than resolved silently.

The contract also states what this service does not own: the RESTRUCTURE registry rows and the catalog rows are rwb-decision's behind the `RuleCatalog.row` operation published in `RWB-P3-E2042-CON`; the evaluation of the package is the case workflow's `EvaluateRules` activity; the role rows, the service levels and timers rows and the calendar rows are rwb-case's reference data; the decision ledger is rwb-decision's; and the case row is rwb-case's. This service uses the embedded kit types `RuleResult` and `NoPackageInForce` and runs no second rule engine (DP-04).

### 2. Business rationale

Contract-first REST and one hop with a 2 s timeout is the decoupling rule (DP-11, ADR-020), and the case record is rwb-case's while the rule catalog is rwb-decision's (Arch v5 slide 41; ASM-0069). Both only work if the seam is written down once. The seam here is small and load-bearing: an operation that turns a fired rule into an action, an owner and a due date without writing anything; a fill that writes those values through the owner of the case; a read the case record screen can consume; and a Schedule that sweeps the cases the transition never filled.

Four teams move at once if the shape is agreed and faked on Day 1. The app story builds the three operations against the fakes of rwb-case, rwb-access and rwb-decision; the operations story deploys the worker, the Schedule, the flag and the runbook against the names this document fixes; the case transition story `RWB-P3-E2035-APP` builds its call and its write against the resolve shape; and the integration harness of `RWB-ITG-E2035-ITG` reads the same answer through the owning services. Without the contract, the action text, the owner role and the timer would be resolved in two places and the measure the legacy story sets — the count of active cases with no next action, with a target of zero — would have no single owner.

The contract is also where the legacy split is made explicit. Four statements of the legacy criteria belong to the case side and are proved in `RWB-P3-E2035-APP`: the write in the same transaction as the move, the cancel of the `NEXT_ACTION_MISSING` task on closure, the optimistic lock and the refusal of the move when no package version is in force. This document fixes what the case side may rely on when it does them: the resolve answer, its refusal outcomes, the idempotency of a repeat and the one-task rule of the fill.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the task queue, the Schedule name and the event names follow the platform rule (DP-13, DP-14).
- The CloudEvents 1.0 envelope, the RFC 9457 problem-details body and the platform message catalogue are the platform baseline; this document narrows them where it must and says so.
- The embedded Drools kit contract is available (RWB-PLT-E1072-CON, DP-04): the `RuleResult` and `NoPackageInForce` types, the first-match semantics, the cache bound and the checksum rule are its elements, and this document reuses them rather than redefining them.
- The workflow kit and its Schedule conventions are available (RWB-PLT-E1071-CON, RWB-PLT-WF): the task queue `rwb-integration`, the namespace `rwb-recovery`, the overlap policy, the catch-up window and the retry policy are the kit's elements.
- The rwb-case operations exist as published by the rwb-case contract stories: the case record read and write of RWB-P3-E1018-CON and RWB-P3-E2035-APP, the case list row read of RWB-P3-E1031-CON, the reference-data and parameter reads of RWB-P3-E1043-CON and RWB-P3-E1042-CON, and the `RuleCatalog.row` operation of RWB-P3-E2042-CON. This document consumes them and fakes them; it defines none of them.
- The rwb-access authorise contract (RWB-P4-E1037-CON) and the rwb-decision decision-log contract (RWB-P7-E1027-CON) are published, or are faked to the shapes this document declares.
- The three legacy values are the agreed values of this key: package code RESTRUCTURE, package version "RES-2026.12", and the rows R-RES-04, R-SET-13, R-RES-03, R-DEV-05 and R-RES-07 with their action, owner role and timer.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the three provided operations: `POST /next-actions:resolve`, `GET /cases/{caseId}/next-action` and `POST /cases/{caseId}/next-action`, with their paths, rights, inputs, answers, errors and idempotency.
2. Publish the consumed shapes: the case facts read and the next-action write of rwb-case, the case list row, the catalog row of `RuleCatalog.row`, the role class, the service level and the calendar reads, the decision-log read and the authorise call, each with the 2 s client budget.
3. State the split between the compute and the write, and reconcile the Ownership Map conflict of the read path.
4. Publish the `NextActionCheckWorkflow` contract: the input, the three activities, the output counts, the at-most-one-task rule and the non-retryable `NoPackageInForce` outcome.
5. Publish the `next-action-check` Schedule contract: the schedule ID, the cadence, the overlap policy, the catch-up window and the pause, resume and backfill operations of the kit.
6. Publish the table section: the `job_catalog` row this service owns and the `decision_record` library table, with the statement that no case, role or rule row is copied into `rwb_integration`.
7. Publish the error mapping of the five messages over the three operations and the fill.
8. Build the contract fakes of rwb-case, the catalog, the reference data, rwb-decision, rwb-access and the gateway route.
9. Add the contract tests: the operation shapes, the consumed shapes, the Schedule fields, the table section and the drift test between each fake and this document; tag the baseline and hand it to the app and operations stories.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An operation, a consumed shape or the Schedule contradicts this document | The contract test fails and the merge is blocked | None | AC1, AC2, AC3, AC4 |
| X2 | A fake drifts from this document, or answers a shape this document does not declare | The drift test fails and the merge is blocked | None | AC6 |
| X3 | The resolve is called without a rule ID, a package version or a business date | The call is refused with the field named and nothing is resolved | MSG-GEN-001 | AC5 |
| X4 | The resolve is called for a business date with no package version in force | The answer is `NoPackageInForce` and it is non-retryable for the caller; the move is refused and nothing is written | MSG-P3-027 | AC5 |
| X5 | The caller's role does not hold Case record R or U, or the case is outside the scope | The call is refused before any consumed contract is reached, and no data is returned | MSG-P4-002, MSG-P4-003 | AC5 |
| X6 | A field-level detail of a consumed operation is missing from the source material | The element is marked with the placeholder, one gap row and one assumption row are carried, and the fake is written to the assumed shape | None | AC2, AC6 |
| X7 | A document declares the case write, the catalog registry or a second rule engine as this service's own | The review refuses the document, because the case row is rwb-case's, the registry is rwb-decision's and the evaluation is the case workflow's | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes and the published rwb-case, rwb-access and rwb-decision contracts and fakes them |
| Negotiable | The field-level detail of the consumed operations is settled with their owners; the three operation names, the Schedule name and the split are fixed by this realignment |
| Valuable | Unblocks the app story, the operations story, the case transition of RWB-P3-E2035-APP and the integration harness of this legacy key |
| Estimable | Three operations, eight consumed paths, one workflow with three activities, one Schedule, two tables and six fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the schema, the fake, the table section — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Next action contract baseline for rwb-integration

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the embedded Drools kit contract of RWB-PLT-E1072-CON and the workflow kit of RWB-PLT-E1071-CON are in force
    Given the package code is RESTRUCTURE and the package version is "RES-2026.12"

  Scenario: AC1 The three provided operations are fixed (new, D-RCV-60)
    Given the contract tables of section 12
    When the three operations are reviewed
    Then POST /next-actions:resolve is documented as side-effect free with the input caseId, ruleId, packageVersion and businessDate and the answer text, ownerRole, ownerName, ownerUserId, dueDate, waiting, missing, ruleId and ruleVersion
    Then GET /cases/{caseId}/next-action is documented with text, ownerRole, ownerName, ownerUserId, dueDate, waiting, overdue, missing, ruleId and ruleVersion
    Then POST /cases/{caseId}/next-action is documented as the fill, with the Idempotency-Key header and the 200 answer of a case that already holds a next action
    Then every operation names its Case record right, its 401, 403, 404, 409, 422 and 503 answers and its message ID
    Then the old monolith base of the legacy story appears nowhere in the document

  Scenario: AC2 The eight consumed paths are published with one budget (new, D-RCV-60)
    Given the contract tables of section 12.2
    When the consumed operations are reviewed
    Then the case facts read, the case list read, the next-action write, the catalog row of RuleCatalog.row, the role class read, the service level read, the calendar read, the decision-log read and the authorise call are each described with method, path or operation name, owner, use and the 2 s client budget
    Then each one is attributed to rwb-case, rwb-access or rwb-decision and none is declared as provided by rwb-integration
    Then the write path of the fill is marked with the placeholder and cited to the gap row, because no source fixes it
    Then the fakes of section 12.8 answer every consumed path and operation with the shapes of this document

  Scenario: AC3 The compute-and-write split is fixed and the ownership conflict is reconciled (new, D-RCV-60)
    Given the contract of this story and the Ownership Map row of GET /cases/{caseId}/next-action
    When the split is reviewed
    Then the document states that rwb-integration resolves and serves and that rwb-case writes recovery_case.next_action_text, next_action_owner_role, next_action_due_date, next_action_rule_id and next_action_waiting in the same transaction as the move
    Then the document states that the optimistic lock, the cancel of the NEXT_ACTION_MISSING task and the refusal of the move when no version is in force are the case side's and are proved in RWB-P3-E2035-APP
    Then the document states that the resolve answer is what that story consumes and that a repeat of the same input answers the same output
    Then the document records that the Ownership Map keeps the read path with P3 while this work package assigns the story to rwb-integration, and cites the gap row of the conflict
    Then the case list responses of RWB-P2-E2033-APP carry nextAction, nextActionOwner, nextActionDueDate and nextActionOverdue as a contract change of this story

  Scenario: AC4 The fill workflow and the Schedule are fixed (new, D-RCV-60)
    Given the contract tables of section 12.5 and 12.6
    When the workflow and the Schedule are reviewed
    Then NextActionCheckWorkflow is documented with its input, its three activities and its output counts of filled, unchanged, missing and failed cases
    Then findCasesWithoutNextAction, resolveNextAction and fillNextAction are documented with their inputs and outputs on the task queue rwb-integration
    Then NoPackageInForce is a non-retryable outcome of resolveNextAction
    Then the next-action-check Schedule is documented with the cadence of 5 minutes, the overlap policy SKIP, the catch-up window, the business date input and its job_catalog row
    Then a fill raises at most one open NEXT_ACTION_MISSING task per case

  Scenario: AC5 The error mapping covers the five messages on the named operations (new, D-RCV-60)
    Given the contract tables of section 12 and the validation table of section 14
    When the error mapping is reviewed
    Then MSG-P4-002 and MSG-P4-003 answer the refused authorise call of the resolve, the read and the fill
    Then MSG-P3-027 answers the no-version-in-force outcome of the resolve and of the fill, naming the package in force check
    Then MSG-GEN-004 answers a case changed between the read and the write and a repeated fill of a case already filled
    Then MSG-P2-023 is the message the case record shows when a case holds no next action or no due date
    Then every message keeps the legacy text of RWB-E2-035 and no operation invents a new wording

  Scenario: AC6 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.3 names no event type of its own and says that the local decision-record library publishes DecisionRecorded on rwb.decision-record.v1
    Then 12.4 is None, because every call of this story is call-driven
    Then 12.7 names the job_catalog row of this service and the decision_record library table only, and holds no case, role or rule table
    Then the six fakes of section 12.8 answer the consumed shapes and the drift test fails on any difference
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Two operations serve the resolution and one writes it: the resolve is side-effect free, the read composes it, and the fill writes it through the owner of the case | Arch v5 slide 41; DP-01; RWB-P3-E2035-APP |
| BR2 | rwb-case is the only writer of `recovery_case`: this service writes no case column, no task row and no lock | Arch v5 slide 41; DP-01 |
| BR3 | One REST base and one task queue per service: this contract declares `/api/recovery/integration/v1` and `rwb-integration`, consumes the other bases and never declares another service's path as provided | DP-13; DP-14; Ownership Map |
| BR4 | The rule catalog is read only through `RuleCatalog.row(ruleId, packageVersion)` as published in RWB-P3-E2042-CON; no workbook, no generated DRL and no rule table is read | D-RCV-36 T3, T5, T6; DP-04 |
| BR5 | The embedded kit supplies the `RuleResult` and `NoPackageInForce` types and the version-in-force check; no second rule engine runs in this service, because the evaluation is the case workflow's activity | D-RCV-36 T5, T7; DP-04; ASM-1185 |
| BR6 | Everything a business person may change is a data row: action text, owner role, timer, role class, service level and calendar are read through their owners' contracts and written in no code path | FSD P2 Integration v3 BR-P2-001; Template and Rules §R7.2 s17 |
| BR7 | The resolve answer is a pure function of the case facts, the catalog row, the reference rows and the business date: the same input answers the same output, which is what makes a repeated transition and a repeated fill safe | Legacy RWB-E2-035 AC9 and AC11 |
| BR8 | A fill raises at most one open `NEXT_ACTION_MISSING` task per case, and the Schedule carries the overlap policy SKIP and a catch-up window so a missed run is caught by the next one | Legacy RWB-E2-035 BR7 and JOB-05 misfire rule |
| BR9 | No personal data appears in an event, an activity input, an example or a fake: case IDs, role codes, rule IDs, version labels and dates only | Arch v5 slide 42; Template and Rules §R7.2 s17 |
| BR10 | A consumed field, path or error that no source fixes is written with the placeholder and carried in one gap row plus its assumption rows, never invented | Template and Rules §R9 |
| BR11 | The legacy flag `rwb.casewf.next-action` is kept as the reference of the switch, and the switch is a feature flag of the platform flag library, never a column of a service table | R-PREC default ruling; Ownership Map `feature_flag` (PLT) |
| BR12 | The legacy values of the key are carried unchanged: package version "RES-2026.12" and the rows R-RES-04, R-SET-13, R-RES-03, R-DEV-05 and R-RES-07 with their action, owner role and timer | Legacy RWB-E2-035 section 7; RWB-E2-042 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the consumed shapes, the split, the workflow, the Schedule and the tables are described | In review |
| In review | Consumer sign-off | The app story, the operations story, the case transition story and the harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A field or an error is added to an operation without removing one | Baselined |
| Baselined | Breaking change to a consumed shape | rwb-case, rwb-access or rwb-decision removes, renames or retypes an element this contract consumes | In review, with the owner of that operation |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A package version becomes in force | rwb-decision announces it and the cached catalog row of the superseded version is dropped | Baselined |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-integration | Owns the document, the three operation shapes and the six fakes; tags the baseline |
| Solution architect | Approves a breaking change to a consumed contract and the reconciliation of the ownership conflict of the read path |
| The rwb-case owner | Owns the case facts read, the case list read, the next-action write and the `RuleCatalog.row` operation; signs off the shapes taken from its contract |
| The rwb-access owner | Owns the authorise contract and signs off its consumption |
| The rwb-decision owner | Owns the catalog rows and the decision ledger and signs off the read shapes |
| Platform workflow kit owner | Owns the Schedule conventions, the task queue and the retry policy this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an event or an activity input |

The deployment identity that calls the consumed contracts is Not specified in the source documents (GAP-0668; ASM-1177); the document names it "the rwb-integration workload identity (DP-02)" and leaves the name to RWB-P2-E2035-OPS.

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| Resolve input | caseId, ruleId, packageVersion, businessDate |
| Resolve answer | text, ownerRole, ownerName, ownerUserId (when BR9 names the case owner), dueDate, waiting, missing, ruleId, ruleVersion |
| Read answer | The resolve answer plus overdue, and the case state and closed flag it is computed against |
| Fill answer | The case ID, the outcome filled, unchanged, missing or skipped, the task reference when one is raised, and the decision-record reference |
| Case facts read | state, status, ownerUserId, queueId, queue role code, team code, closedDate |
| Catalog row | ruleId, packageVersion, drools_rule_name, action_text, owner_role, timer_spec, target_queue_code, outputs |
| Role row, service level row, calendar row | roleCode, roleName, roleClass; state, working days; calendar date and label |
| Decision-log read | ruleId, ruleVersion, entryId, decidedAt of the latest state change |
| Workflow input and output | business date and run window in; counts of filled, unchanged, missing and failed out |
| Schedule row | job_id, job_name, owner_role, schedule_text, runbook_path, expected_minutes, alert_after_minutes |

The field-level detail of the case facts read, the catalog row, the reference rows, the decision-log read and the next-action write — property types, lengths, required flags and the query parameters — is Not specified in the source documents (GAP-0668; ASM-1179); this document fixes the element names above and leaves the types to the review with each owner. The values of the rule rows are the legacy values of this key and are carried unchanged (BR12).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/next-actions:resolve` | Input caseId, ruleId, packageVersion, businessDate; answer text, ownerRole, ownerName, ownerUserId, dueDate, waiting, missing, ruleId, ruleVersion; 401, 403, 404, 409 (MSG-P3-027, MSG-GEN-004), 422 (MSG-GEN-001), 503 (MSG-GEN-006) | Case record R, scope applied | Side-effect free: the same input answers the same output |
| GET | `/cases/{caseId}/next-action` | Answer text, ownerRole, ownerName, ownerUserId, dueDate, waiting, overdue, missing, ruleId, ruleVersion; 401, 403, 404, 503 | Case record R, scope applied | Read only |
| POST | `/cases/{caseId}/next-action` | The fill: answer case ID, outcome filled, unchanged, missing or skipped, task reference, decision-record reference; 200 for a case already filled, 409 (MSG-GEN-004), 422, 503 | Case record U for the service identity, scope applied | `Idempotency-Key`; at most one open NEXT_ACTION_MISSING task per case |

The `:resolve` suffix is the operation name this contract fixes for a resolution and not a resource: the legacy story called the component `NextActionAssigner` and its interface `NextActionAssigner.assign(...)`, and no source fixes an HTTP name for it (GAP-0668; ASM-1183). The read path is the Ownership Map row that the map keeps with P3; this contract serves it from rwb-integration under its own base and records the conflict (GAP-0668; ASM-1178).

Two responses of `RWB-P2-E2033-APP` change and are documented here as a change, not as a new operation: each Case item of `GET /cases` and each row of `GET /cases/export` gains `nextAction`, `nextActionOwner`, `nextActionDueDate` and `nextActionOverdue`, resolved by this service, with that story's authorization and errors unchanged.

#### 12.2 REST operations consumed

One hop per call, no chaining; 2 s timeout and a breaker per downstream (DP-11).

| Method | Path or operation | Owner | Contracted use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case facts of the resolve and the read |
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | The active cases with no next action and the case list rows that carry the four columns |
| POST | Not specified in the source documents (GAP-0668; ASM-1179) | P3 rwb-case | The write of the four next-action fields and the raise or cancel of the NEXT_ACTION_MISSING task, called by the fill |
| GET | `/api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion=`, the `RuleCatalog.row(ruleId, packageVersion)` operation | P7 rwb-decision, published in RWB-P3-E2042-CON | action_text, owner_role, timer_spec and outputs of the firing rule |
| GET | `/api/recovery/case/v1/reference-data/role-classes/{roleCode}` | P3 rwb-case | role_name and role_class of the owner role |
| GET | `/api/recovery/case/v1/reference-data/service-levels/{toState}` | P3 rwb-case | The service levels and timers row of the to_state |
| GET | `/api/recovery/case/v1/parameters/rwb.calendar.bank-holidays` | P3 rwb-case | The bank holiday list of BR8 of the app story |
| GET | `/api/recovery/decision/v1/decision-log?caseId=&latestStateChange=true` | P7 rwb-decision | The latest state change of a case: rule ID and rule version |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Case record R or U and the case scope, cached per session |

The reference-data and parameter paths are named by the reference tables and the configuration key of the legacy story; no source fixes them and they are taken from the P3 contract baseline when it is published (GAP-0668; ASM-1179). The catalog operation is the one `RWB-P3-E2042-CON` publishes over the rwb-decision catalog, so this service holds no registry row and reads no rule table (BR4).

#### 12.3 Events published

None. This story declares no event type and publishes on no topic of its own. The fill writes through the rwb-case contract, and the event of the record is the shared ledger event: the local decision-record library of DP-03 publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` from the same transaction as the record it writes, and this contract only names that event and its key (the decision-record reference). The move's own record is written by rwb-case's library call in `RWB-P3-E2035-APP`.

#### 12.4 Events consumed

None. Every call of this story is call-driven: the resolve is called by the case transition, the read by the case record screen through gateway-bff, and the fill by the `next-action-check` Schedule. The latest state change is read from the decision-log contract at the time of the fill, so the service subscribes to no topic, holds no inbox and keeps no projection.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| NextActionCheckWorkflow | Workflow | `rwb-integration` | Input: business date, run window. Output: counts of filled, unchanged, missing and failed cases, and the run reference |
| findCasesWithoutNextAction | Activity | `rwb-integration` | Input: business date. Output: the active cases with no next action from the rwb-case contract |
| resolveNextAction | Activity | `rwb-integration` | Input: caseId, ruleId, packageVersion, business date. Output: the resolve answer; raises `NoPackageInForce`, which is non-retryable |
| fillNextAction | Activity | `rwb-integration` | Input: caseId and the resolve answer. Output: filled, unchanged, missing or skipped; one rwb-case call, at most one task per case, idempotent by case ID and task code |

The activities carry the kit's retry policy; the workflow carries the Schedule's overlap policy and never runs two executions for the same fire window.

#### 12.6 Schedules

| Schedule | Cadence | Documented fields | Legacy reference |
|---|---|---|---|
| `next-action-check` | Every 5 minutes | Schedule ID `next-action-check`; workflow `NextActionCheckWorkflow`; task queue `rwb-integration`; overlap policy SKIP; catch-up window; input business date and run window; pause, resume and backfill as kit operations | JOB-05 Timer check, the next action step |

The five minutes are the legacy cadence of JOB-05. The catch-up window, the overlap window and the backfill limit are Not specified in the source documents (GAP-0668; ASM-1184) and are fixed as values of the deployment in RWB-P2-E2035-OPS. The timer vocabulary of the legacy story is JOB-05; in the target JOB-05 is retired (Arch v5 slide 44; the Ownership Map ruling on `timer`) and this Schedule is the mechanism that does the fill (ASM-1180).

#### 12.7 Tables owned

| Table | Schema | Owner | Contracted use |
|---|---|---|---|
| job_catalog | rwb_integration | P2 (Ownership Map; TSD P2 v3 T3.1) | One row for `next-action-check`: job_id, job_name, owner_role, schedule_text, runbook_path, expected_minutes, alert_after_minutes, first_release |
| decision_record | rwb_integration | PLT library, created in rwb_integration (DP-03) | The local decision record of a fill, written by the library in the same transaction as the record |

No case table, no task table, no role table and no rule table is owned, read or copied: the case facts, the case write, the role rows, the service levels, the calendar and the rule row come through their owners' contracts (DP-01, BR2). The Ownership Map ruling on `job_catalog` stands: each service's Schedules are not rows of a shared table, so this row exists for the job catalogue of the deployment and for the alerts, not to drive the Schedule.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case WireMock — case | `GET /cases/{caseId}` for `RW-2026-000401` in WITH_FCR_OFFICER, `RW-2026-000402` in IN_FCR_QUEUE at version 7 and 8, `RW-2026-000403` in AWAITING_PAYMENT, `RW-2026-000404` closed with reason SETTLED, `RW-2026-000405` at version 7 with a 409, and three active cases with no next action; one 404 for a case out of scope | App story, contract tests |
| rwb-case WireMock — write | The next-action write accepted, a repeated write answering 200 unchanged, a version conflict answering 409 with MSG-GEN-004, and the task raise and cancel accepted | App story, contract tests |
| Catalog WireMock (shapes of RWB-P3-E2042-CON) | `RuleCatalog.row` for R-RES-04, R-SET-13, R-RES-03, R-DEV-05 and R-RES-07 of version "RES-2026.12", one 404 and one `NoPackageInForce` for 2027-01-04 | App story, contract tests |
| rwb-case reference-data and parameter stub | role classes PARTNER_USER and INTERNAL, 5 working days for BACK_TO_ROUTE_DECISION, no row for DEV_WITH_OWNER, calendar rows 2026-12-31 and 2027-01-01 | App story, contract tests |
| rwb-decision WireMock | The latest state change R-RES-04 of version "RES-2026.12" with entry DLE-SYN-0402, an empty answer for a case with no state change, and one slow answer beyond 2 s | App story, contract tests |
| rwb-access WireMock | Case record R and U granted in scope; refused for RW-REFADM with MSG-P4-002; a case out of scope answered 404 with MSG-P4-003 | App story, contract tests |

Each fake is generated from the owning service's published OpenAPI document where one exists, and the drift test fails when a fake answers a shape or an error this document does not declare.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 9 consumed | The resolve, the read and the fill provided; the case facts, the case list, the case write, the catalog row, the role class, the service level, the calendar, the decision-log read and the authorise call consumed; one hop, 2 s timeout |
| Kafka | None declared, 1 published by the library | `rwb.decision-record.v1` carries DecisionRecorded on the service's behalf on a fill (DP-03) |
| Temporal | 1 workflow, 3 activities, 1 Schedule | NextActionCheckWorkflow, findCasesWithoutNextAction, resolveNextAction, fillNextAction; `next-action-check` every 5 minutes |
| File | None | This contract names no file; the WIN and debt-buyer files are other stories of this service |

### 13. Solution plan

**Deliverables.** `contract/next-action-openapi.yaml` (the three operations and the two changed case list responses), `contract/next-action-consumed.yaml` (the nine consumed paths and operations with the 2 s budget), `contract/next-action-split.md` (the compute-and-write split and the ownership reconciliation), `contract/next-action-workflow.yaml` (the workflow input, the three activities and their outputs), `contract/next-action-schedule.yaml` (the Schedule fields and the kit operations), and six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit types; the catalog read through rwb-decision's registry; no second engine | H RWB-PLT-E1072-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | No ACE read: the case facts come from rwb-case | none |
| DP-06 | Parameters, casewf.config | The parameters contract of rwb-case for the calendar key | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | The reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | The Schedule and the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/integration/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.integration.events.v1`; the naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_integration` | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route for the SCR-03 header | H RWB-PLT-N001-CON |

**Build steps**

1. Write the OpenAPI document of the three operations, with the input, the answer, the errors and the idempotency of each; AC1, AC5.
2. Write the consumed document: nine paths and operations, their owner, their use and the 2 s budget; AC2.
3. Write the split note: the compute here, the write there, the four case-side statements and the ownership reconciliation; AC3.
4. Write the workflow contract and the Schedule contract, with the overlap policy, the catch-up window and the one-task rule; AC4.
5. Write the table section: the `job_catalog` row and the `decision_record` library table, with the absence rule for the case, role and rule tables; AC6.
6. Build the six fake sets and their fixtures.
7. Add the contract tests, including the drift test between each fake and this document, and the check that the legacy monolith base appears nowhere.
8. Tag the baseline and collect the sign-off of the app story, the operations story, the case transition story and the harness.

**Done when.** The six contract files validate in the pipeline, the contract tests pass, the six fakes answer every consumed path and operation, and the app, operations, case transition and harness stories of this legacy key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-023 | The case has no next action or no due date | This case has no next action. It is on the exception list for {team}. |
| MSG-P3-027 | No RESTRUCTURE version is in force on the business date | The rule version was refused at the {check} check: {detail}. |
| MSG-GEN-004 | A case changed between the read and the write, or a fill repeats a case already filled | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | A role without Case record R or U calls an operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |

The texts are the agreed texts of the legacy story and of the platform catalogue; this contract adds no message. For MSG-P3-027 the `{check}` value is "package in force" and the `{detail}` names the package code and the business date only. The operation that carries each message is named in section 12.1; MSG-P2-023 is carried by the case record and never returned as a problem body.

### 15. Screens and states

None in this story. The contract serves the SCR-03 next action header through the gateway-bff composite route and the SCR-02 columns through the case list of RWB-P2-E2033-APP, and it renders no page and holds no screen state. The Schedule states are operator states of the deployment and are carried by RWB-P2-E2035-OPS as metrics and as a run view, not as a screen of this story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E2035-CON-01 | AC1 | Contract | The three operations validated against the OpenAPI document; a wrong path, a missing error and a missing idempotency element are each refused |
| TC-P2-E2035-CON-02 | AC2 | Contract | The nine consumed paths and operations with owner, use and the 2 s budget; the placeholder on the write path |
| TC-P2-E2035-CON-03 | AC3 | Contract | The split note against the Ownership Map row; the four case-side statements; the two changed case list responses |
| TC-P2-E2035-CON-04 | AC4 | Contract | The workflow input and output, the three activities, the non-retryable outcome and the Schedule fields with SKIP and the catch-up window |
| TC-P2-E2035-CON-05 | AC5 | Contract | The five messages mapped on the named operations, with the refused authorise, the no-version and the repeated-fill answers |
| TC-P2-E2035-CON-06 | AC6 | Component | The nine sub-tables present; 12.3 and 12.4 with no event type; the two tables of 12.7; the six fakes match the document |

### 17. Guardrails

- No business value in the contract: action text, owner role, timer, role class, service level, calendar and route state are data rows of their owners.
- No personal data in an answer, an event, an activity input, an example or a fake: case IDs, role codes, rule IDs, version labels and dates only.
- The contract names only rwb-integration operations as provided; the case facts, the case write, the catalog row, the reference rows, the decision-log read and the authorise call are consumed and never restated as this service's (DP-01, DP-13).
- One base, one queue and one namespace: a document that names another service's base as provided, or a topic outside `rwb.<short>.events.v1`, fails the review (DP-13, DP-14).
- The rule row is read only through `RuleCatalog.row`; a workbook, a generated DRL or a rule table in a shape of this contract fails the review (BR4).
- No second rule engine: the kit's types and the version-in-force check are used and the evaluation stays with the case workflow's activity (BR5).
- The legacy flag name is kept as a reference only, and the switch is the platform flag library's (BR11).
- Every example and fixture is synthetic; no production payload, case number or rule row is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-WKM-012 | Every open case carries one next action with owner and due date | The resolve answer, the read answer and the four case list fields | TC-P2-E2035-CON-01, TC-P2-E2035-CON-03 |
| REQ-WKM-013 | The next action comes from the rule that moved the case | The catalog row of `RuleCatalog.row` and the rule ID and version of every answer | TC-P2-E2035-CON-02, TC-P2-E2035-CON-05 |
| REQ-WKM-016 | A case with no next action is reported as an exception | The missing flag, the one-task rule and the fill outcome | TC-P2-E2035-CON-04, TC-P2-E2035-CON-05 |
| REQ-WKM-014 | Next action visible on the case record and every queue view | The read operation and the four case list fields | TC-P2-E2035-CON-01, TC-P2-E2035-CON-03 |
| REQ-WKM-015 | An overdue next action escalates like a service level breach | The overdue marker of the read answer, which the escalation story consumes | TC-P2-E2035-CON-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The nine consumed paths and operations with the 2 s budget | TC-P2-E2035-CON-02 |
| D-RCV-60 | The split of the legacy key into a service contract, an app story and an operations story | The three operations, the split note and the Schedule contract | TC-P2-E2035-CON-01, TC-P2-E2035-CON-03, TC-P2-E2035-CON-04 |

### 19. Out of scope

- The implementation of the three operations, the resolver, the read composition and the fill (RWB-P2-E2035-APP).
- The deployment of the worker, the Schedule, the flag, the dashboards, the alerts and the runbook (RWB-P2-E2035-OPS).
- The write of the four case columns, the task lifecycle and the optimistic lock (RWB-P3-E2035-APP).
- The registry rows of the RESTRUCTURE package, the catalog and the central ledger (RWB-P7-E2035-APP).
- The role rows, the role classes and the authorise contract (RWB-P4-E2035-APP, RWB-P4-E1037-CON).
- The service levels and timers rows, the calendar rows and the reference versions (RWB-P3-E1043-CON, RWB-P3-E1042-CON).
- The case list and the export resources the four columns are added to (RWB-P2-E2033-APP).
- The platform envelopes, the workflow kit and the naming library (RWB-PLT-LIB, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON).
- The real cross-service proof of the journey (RWB-ITG-E2035-ITG).
- The field-level detail of the consumed shapes and the write path of the fill (GAP-0668).
