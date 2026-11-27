# RWB-S1-E4005-APP Call COLLINS for return by route

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4005-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S1-E |
| Ready to start | Day 1 |
| Size | Not set; the squad sizes it at refinement |
| Depends on (build) | RWB-S1-E4005-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-005 split out for rwb-valuation. Both legacy criteria are copied word for word with their origin tags; the return-by-route step becomes an activity of `RouteDecisionWorkflow` on task queue `rwb-valuation`, reads the expected return for each route of the route set in force on the rwb-source-data data product (DP-05), falls back to the rule result where an answer is missing and records the fallback (R-UNI-32), writes the answer with its model version and rule version through the local decision-record library before the answer is used (DP-03) and answers the route operation on base `/api/recovery/valuation/v1` (DP-13), reached by SCR-13 through the gateway-bff composite route (DP-19). No event is published, because the ownership rows give S1 none. The operation names of the score data product, the case-state read and the rule-in-force read are not published (GAP-2609; ASM-4311); the score element set is given twice and the store of the per-route answer is not fixed (GAP-2610; ASM-4312); no S1 rule package, rule id or route-set rule is in force (GAP-2611; ASM-4313); no source names the event or the timer that starts the step (GAP-2612; ASM-4314); the FSD names both the ACE score view and the Model gateway and no source says whether a live model call survives (GAP-2614; ASM-4316). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S1-E4005-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (31 resolved, 18 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **the Workbench to ask the COLLINS model for the expected return on each route and record the answer with its version**, so that **the route is chosen on expected return with reasons**.

This is the application slice of legacy RWB-E4-005. It owns:

- the two legacy criteria of the key, AC1 and AC2, copied verbatim with their origin tags, and the rules, messages and screen states they depend on;
- the return-by-route step as an activity of `RouteDecisionWorkflow` on `rwb-valuation`: the route set in force and its version, and the expected return for every route of that set;
- the read of the per-route score on the rwb-source-data data product, one hop, 2 s, read only, because the COLLINS answer is ACE's ingested fact and this service holds no `v_ace_*` grant (DP-05);
- the fallback to the rule result where a route of the set has no answer, recorded on the decision as the routing logic's R-UNI-32 requires, with no return invented for that route;
- the decision record of the step, written through RWB-PLT-E1027-CON in the caller's transaction before the answer is used, carrying the model code and version, the rule id and version, the scored-at time and the per-route answer (DP-03);
- the route operation `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`, its right, its `Idempotency-Key` and its answer, whose shape is baselined by RWB-S1-E4005-CON (DP-13);
- the SCR-13 Route decision states this step produces, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the route operation, the consumed rows, the record element, the workflow elements, the rights, the error set and the fakes, which are RWB-S1-E4005-CON; the route agent that recommends a route with reasons and the live model path, which are FEAT-VAL-07 and rwb-agent's (P10); the ACE score facts and the freshness of the data product, which are rwb-source-data's (P1); the case of record and its route states, which are rwb-case's (P3); the rule rows, the package version and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; the payoff and settlement range (FEAT-VAL-06), the approvals and the route flow start; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

A route chosen on officer judgment written up in an account plan cannot be defended when the bank later negotiates, litigates or prices a sale. FEAT-VAL-05 of module S1 replaces that judgment with a number per route: the expected return for each route of the set, recorded with the version of the model that produced it and the version of the rules in force, so that the recommendation that follows can be checked against it. The measure of the module is unchanged: recommendations accepted, read monthly from the decision log and the Workbench records.

Under D-RCV-60 the shape of the call changes, and that is what this story carries.

- **the answer is ACE's, not a live integration of this service.** The FSD S1 v3 change note re-points the COLLINS scores to ACE ingestion, and the feature row reads them from `v_ace_score`; only rwb-source-data reads the `recovery.v_ace_*` views, so the per-route return arrives on the owner's data product with its freshness stamp and is never read as a table here (DP-05).
- **the model gateway is not this service's.** FSD S1 A2.5 lists the Model gateway beside the ACE view, and the target gives the live model path to rwb-agent (P10) through the route agent; this step consumes no rwb-agent operation and asserts no live call (GAP-2614; ASM-4316).
- **the answer is recorded before it is used.** Legacy AC2 is the rule that makes the step trustworthy: no record, no answer, MSG-P7-003. Under DP-03 the record is local, hash-linked and written in the same transaction as the step, and R-UNI-39 says no action proceeds unlogged.
- **a missing answer does not stall the case.** R-UNI-32 falls back to the rule result when the model does not answer inside the timeout and records the fallback, so the route decision still moves inside its service level.
- **nothing is published.** The ownership rows give S1 no event, so the step adds none to `rwb.valuation.events.v1`; its outward facts are the route answer and the decision record, which the library sends to `rwb.decision-record.v1` (ASM-4312).

### 3. Preconditions

- RWB-S1-E4005-CON is published: the route operation, the consumed rows, the record element, the workflow elements, the rights, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-13 Route decision reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The rwb-source-data data product that carries the scores of `v_ace_score`, one row per route and account with its model code, model version, estimate and batch freshness, is published with its fake. Its operation name is Not specified in the source documents (GAP-2609; ASM-4311), and its row is not in this story's contract-dependency list, which is None.
- The rwb-decision recommendation read is published as `GET /cases/{caseId}/recommendation` on its base, carrying `recommended`, `reasons`, `expectedReturnByRoute`, `ruleVersion` and `agentVersion` (API Specification v5, module P7, area Decision log, right R); the rule-in-force read has no published name (GAP-2609; ASM-4311).
- The rwb-case case-state read and the rwb-access authorise call are available for their fakes; the rwb-case read is `GET /cases/{caseId}` on its published base (GAP-2609; ASM-4311).
- The route set and its version are a row in force of rwb-decision, and the route codes are those of `LOV-ROUTE` (R1 to R8) read with the list, never enumerated in code; no S1 rule package is in force and no source names the rule that maps a route set to the routes asked for (GAP-2611; ASM-4313).
- The service runs as its own login on schema `rwb_valuation`, holds the library objects `decision_record`, `idempotency_key` and `outbox`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_score` or `rwb_decision` is refused by the database and fails the boundary test (DP-01, DP-05).
- Where the per-route answer is persisted after the split is not fixed: the Ownership Map gives S1 no table, and TSD S1 T3.1 declares `score` as REUSE ACE under the module's Field IDs while the legacy Data table reads `v_ace_score` (GAP-2610; ASM-4312).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S1-E4005-CON when its tests pass.

### 4. Flow

1. The case is at the route decision and the route command is submitted through `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the command starts `RouteDecisionWorkflow` on task queue `rwb-valuation` (API-S1-001; DP-13). The step runs inside this route decision only; no batch-completion event, timer or Schedule starts it (GAP-2612).
2. The step runs after the appraisal is accepted, because FEAT-VAL-04 fixes the band the route decision runs on. It reads the rule id, the rule version and the route set in force for the business date from rwb-decision, one hop, 2 s (R-UNI-38; GAP-2611). Until the S1 route rule package exists (Phase 2), the route decision is evaluated from the embedded Drools kit with the universal rule package in force, and the package and rule version are recorded on every decision (GAP-1687).
3. It reads the expected return for every route of that set on the rwb-source-data data product: per route the model code, the model version, the estimate, the score where one is carried and the scored-at time, with the freshness stamp of the ACE batch that produced them (DP-05; GAP-2609).
4. If the product is stale after a late or failed ACE batch, the step holds, writes nothing, records no decision and shows MSG-P1-001 with the data date; it resumes on the next fresh answer (VR-S1-005-1; X5).
5. Where a route of the set has no answer, the step falls back to the rule result for that route, records the fallback on the decision and continues; it never invents a return, a model version or a route of its own (R-UNI-32; X6).
6. The step assembles one answer per assessment: the case, the route set with its version, each route with its expected return, the model code and version of the answer, the scored-at time, the fallback flag of each route, and the rule id and version in force.
7. Before any of the above is used, `ReturnDecisionRecordWriter` writes one decision record through the local library with that content. A failed write stops the step with nothing changed and nothing returned (DP-03; AC2, R-UNI-39; X1).
8. The step answers the workflow with the per-route answer and its versions; the route operation answers `Approval` with the case, the decision and the status elements of the baseline, and the recommendation read carries the same per-route answer with its `ruleVersion` and `agentVersion` (API-S1-001).
9. A repeat of the same command with the same `Idempotency-Key` returns the stored answer, raises no second record and counts the idempotency hit (R-UNI-40; X9).
10. SCR-13 Route decision shows the expected return per route, the route set and the versions, and moves through its loading, recommendation, overridden and submitted states, read only through the gateway-bff composite route (DP-19).
11. A reopened route decision (R-UNI-02, R-UNI-14, R-UNI-22, R-UNI-31, R-UNI-50) runs the step again on the model version current at that business date; the earlier record stays as the evidence of the answer the earlier decision was taken on.
12. No event is published: the answer leaves as the route answer, the recommendation read and the decision record, which the library sends to `rwb.decision-record.v1` (ASM-4312).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing, the per-route answer is not returned and the route answer is refused | MSG-P7-003 | AC2, TC-E4-005-02, TC-E4-005-04 |
| X2 | The role does not hold the Treatment and offer right of the operation | 403 before any read or write, and no record is written | MSG-P4-002 | AC3, TC-E4-005-03 |
| X3 | The case is not at the route decision, or the route set of the case is absent | The step does not run, nothing is recorded and the state is reported to the parent | None | AC4, TC-E4-005-05 |
| X4 | rwb-decision or rwb-source-data does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and the caller sees 503 with the platform envelope | None | AC5, TC-E4-005-06 |
| X5 | The ACE data product behind the scores is stale after a late or failed batch | The step holds, writes nothing and shows the data date; it resumes on a fresh answer | MSG-P1-001 | AC6, TC-E4-005-07 |
| X6 | A route of the route set has no answer on the data product | The rule result is used for that route, the fallback is recorded and the route decision continues | None | AC7, TC-E4-005-08 |
| X7 | Every route of the set is without an answer | No answer is asserted: the step records the fallback for each route and reports the missing model answer to the parent | None | AC8, TC-E4-005-09 |
| X8 | The same command is submitted twice with the same `Idempotency-Key` | One record, one answer; the stored answer is returned and the repeat is counted | None | AC9, TC-E4-005-10 |
| X9 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC10, TC-E4-005-11, s17, BR8, BR9 |

X1 and X2 are the exception paths of the legacy key carried onto the split, X3 to X8 are the paths the target call types add, and X9 is the DP-05 and DP-01 boundary. No return, percentage or threshold is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S1-E4005-CON, the rwb-source-data, rwb-decision, rwb-case and rwb-access fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P4 or P7 |
| Negotiable | The activity names, the decision code and the shape of the step outcome are this story's choice; the operation, the rules, the messages, the screen and the score elements are fixed |
| Valuable | Every route of the set carries an expected return with the version that produced it, or a recorded fallback, so the recommendation can be defended |
| Estimable | One workflow step, two activities, four clients, one record write and one screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each path runs on synthetic scores through the contract fakes, plus the stopped record write, the stale product, the missing route answer and the duplicate command |

### 7. Acceptance criteria

```gherkin
Feature: Call COLLINS for return by route

  Scenario: AC1 Call COLLINS for return by route (legacy RWB-E4-005 AC1)
    Given the rwb-source-data contract mock returns the expected return for each route with its model version
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then asks the COLLINS model for the expected return on each route and records the answer with its version
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-005 AC2)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Treatment and offer right not held (exception X2) (new, D-RCV-60)
    Given the role does not hold the Treatment and offer right of the operation
    When the role calls the route operation
    Then the call is refused with 403 before any read or write, no record is written and the user sees MSG-P4-002

  Scenario: AC4 Case not at the route decision (exception X3) (new, D-RCV-60)
    Given the case is not at the route decision or the route set of the case is absent
    When the step is due to run
    Then the step does not run, nothing is recorded and the state is reported to the parent

  Scenario: AC5 Rule or source data does not answer (exception X4) (new, D-RCV-60)
    Given rwb-decision or rwb-source-data does not answer inside 2 s or its breaker is open
    When the step runs
    Then the step waits and retries on the workflow's own schedule, nothing is written and the caller sees 503 with the platform envelope

  Scenario: AC6 Stale ACE data product (exception X5) (new, D-RCV-60)
    Given the ACE data product behind the scores is stale after a late or failed batch
    When the step runs
    Then the step holds, writes nothing, shows the data date and resumes on a fresh answer

  Scenario: AC7 Route without an answer (exception X6) (new, D-RCV-60)
    Given a route of the route set has no answer on the data product
    When the step runs
    Then the rule result is used for that route, the fallback is recorded and the route decision continues

  Scenario: AC8 Every route without an answer (exception X7) (new, D-RCV-60)
    Given every route of the set is without an answer
    When the step runs
    Then no answer is asserted, the step records the fallback for each route and reports the missing model answer to the parent

  Scenario: AC9 Repeated command (exception X8) (new, D-RCV-60)
    Given the same command is submitted twice with the same Idempotency-Key
    When the second command arrives
    Then one record and one answer exist, the stored answer is returned and the repeat is counted

  Scenario: AC10 Boundary (exception X9; rules BR1, BR5, BR8, BR9, BR10, BR11) (new, D-RCV-60)
    Given a component, a statement or a test reaches a v_ace_* view, a recovery_case row, another service's schema, a person identity, personal data or a model gateway call
    When the boundary test runs
    Then the grant refuses the statement, the boundary test fails the build, no event is published and nothing is released

  Scenario: AC11 Error answers of the route operations (status codes 401, 403 and 404) (new, D-RCV-60)
    Given a call to a provided operation of the route base is not authenticated or names a case that does not exist
    When the call is made
    Then the answer is 401 for an unauthenticated call or 404 for an unknown case, with the platform envelope, and nothing is written

  Scenario: AC12 Replay of a write with the same Idempotency-Key (new, D-RCV-60)
    Given a write with an Idempotency-Key has already been recorded
    When the same write is replayed with the same Idempotency-Key
    Then no second record is written and the stored answer is returned

  Scenario: AC13 Activity retry and timeout (new, D-RCV-60)
    Given an activity of RouteDecisionWorkflow is retried or times out
    When the activity runs again
    Then no second record is written and the step waits and retries on the workflow's own schedule

  Scenario: AC14 Consumed call fails or does not answer (new, D-RCV-60)
    Given a consumed call fails or does not answer
    When the step runs
    Then nothing is written and the caller sees 503 with the platform envelope

  Scenario: AC15 Disallowed status change (new, D-RCV-60)
    Given a status change the model does not allow is requested
    When the change is requested
    Then the change is refused and nothing is recorded
```

Both criteria are the legacy AC1 and AC2 of the key, with their origin tags added and the decision log wording changed to decision record: the legacy wording of `the data and the rule version this feature needs are in place`, `its trigger arrives`, `the action is taken` and `nothing changes` stands. The one line this story adds is the Given that names the mock, because the cross-service part of AC1 is the score answer, and every value of the legacy steps is kept as written. Neither criterion carries a business value: the route codes, the model code and the model version are data or answers in force, and the model version is read from the answer and never asserted.

### 8. Business rules

| ID | Rule | Message | BR ID |
|---|---|---|---|
| VR-S1-005-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. | BR12 |
| BR-S1-005 | No value a business person may change is written in code; it is read from reference data with its version | None | BR13 |
| R-UNI-32 | The agent or the model does not answer inside the timeout: fall back to the rule result and continue, and record the fallback on the decision | None | BR14 |
| R-UNI-38 | A new rule version reaches its effective date: apply it to decisions taken from that date; open cases keep the version they were decided under | None | BR15 |
| R-UNI-39 | The decision log entry cannot be written: block the action and raise an incident; no action proceeds unlogged | MSG-P7-003 | BR16 |
| R-UNI-40 | The same event arrives twice with the same key: ignore the second, record the idempotency hit | None | BR17 |

The two VR and BR rows are the rows of FSD S1 A2.5.3.1, copied character for character. The four universal rules are the rows of the Business Rules and Routing Logic v4 that this step depends on: R-UNI-32 is the fallback of X6 and X7, R-UNI-38 is why the record carries the rule version in force on the business date, R-UNI-39 is AC2, and R-UNI-40 is the repeat of the command.

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The expected return per route is ACE's ingested COLLINS answer, read only on the rwb-source-data data product; this service holds no `v_ace_*` grant, keeps no copy and reads no score row as a table | DP-05; Ownership Map rows of S1; FSD S1 A2.5.2 | AC10, TC-E4-005-11 |
| BR2 | The routes asked about are those of the route set in force, read with its version, and the route codes are the ones of `LOV-ROUTE`; no route code, model code or model version is a constant of the build | FSD S1 A2.5.3.1 BR-S1-005; TSD S1 T3.2; GAP-2611 | AC1, TC-E4-005-01 |
| BR3 | A route with no answer takes the rule result and the fallback is recorded on the decision; no return, model version or scored-at time is invented for it | R-UNI-32 | AC7, TC-E4-005-08 |
| BR4 | The answer is recorded before it is used, with the model code, the model version, the rule id and the rule version in force, the route set and its version, the per-route return and the fallback flags; a failed write changes nothing | DP-03; R-UNI-39; legacy AC2 | AC2, TC-E4-005-02 |
| BR5 | No person is in the path of the step: it runs under the service identity, raises no approval task and asserts no person's identity in its input | Legacy RWB-E4-005 AC1; FSD S1 A2.5.3.3 | AC10, TC-E4-005-11 |
| BR6 | The case is not this service's: no `recovery_case`, `assignment`, `task` or `timer` row is written here, and the case state is read and reported | Ownership Map (`recovery_case` owner P3) | AC4, TC-E4-005-05 |
| BR7 | One record per case and assessment: a repeated command with the same `Idempotency-Key` and a repeated fact with the same key raise no second record | API-S1-001; R-UNI-40 | AC9, TC-E4-005-10 |
| BR8 | No foreign key leaves `rwb_valuation` and no statement reaches another schema: the case, the account, the score and the rule are identifiers of other owners' facts | DP-01; TSD S1 T3.3 | AC10, TC-E4-005-11 |
| BR9 | No event is published: the ownership rows give S1 no event, and the step adds no name to `rwb.valuation.events.v1` | context pack S1 ownership rows; ASM-4312 | AC10, TC-E4-005-11 |
| BR10 | No person name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log, a data-product call or a workflow input | Template and Rules v1 §R7.2 (s17) | AC10, TC-E4-005-11 |
| BR11 | The live model path is not this step's: no rwb-agent operation is consumed and no Model gateway call is made; a later need for one is a change of this service with its own contract row | GAP-2614; ASM-4316 | AC10, TC-E4-005-11 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step reports the per-route answer and the parent `CaseWorkflow` applies it to the case of record (BR6). What this story owns is the state of the return-by-route assessment, per route and per assessment.

| From (assessment) | Event | Condition | To |
|---|---|---|---|
| Not assessed | ROUTE_ASSESSMENT_TRIGGERED | The route set in force is read and the product answers fresh | Assessing, one row per route of the set |
| Assessing | SCORE_ANSWERED | The route carries an estimate with its model code and version | RETURNED |
| Assessing | NO_SCORE_ANSWERED | The route carries no answer | FALLBACK, the rule result used and recorded (X6) |
| Assessing | PRODUCT_STALE | X5 | Held, nothing written, and the check re-runs on a fresh answer |
| RETURNED or FALLBACK | RECORD_WRITTEN | The transaction commits with the route answer | Assessed, and the workflow continues |
| RETURNED or FALLBACK | RECORD_FAILED | X1 | Unchanged, nothing returned and no answer (AC2) |
| Assessed | ROUTE_D6_REOPEN | A value, a payment, a deviation or a rule version changes the picture | Not assessed, and the step runs again on the then-current versions |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The route command of a case at the route decision | The workflow is started on `rwb-valuation` | Reading the rule and route set |
| Reading the rule and route set | The row in force answers | The route set is present | Reading the scores |
| Reading the scores | The data product answers fresh | At least one route carries an answer | Assessing, with the fallback per missing route |
| Assessing | The record is written and the transaction commits | AC1 | Waiting for the next assessment |
| Any | The record write or the transaction fails | X1 | Waiting, nothing changed |

The case states `ROUTE_D6_REOPEN` and `BACK_TO_ROUTE_DECISION` are the D6 rows of the Business Rules and Routing Logic v4, applied by rwb-case on this step's outcome; they are named here and not written here. No S1 route rule is in force, because the S1 package is Phase 2 (GAP-2611; ASM-4313).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Treatment and offer U in the legacy permission table of the key: submit the route decision and read the per-route answer and its record |
| RW-CASEOWN (CRU), RW-RESTRUCT (CRUA), RW-SPECIAL (CRU), RW-GUARANT (CRU) | TSD S1 T6.1 rows for the capability area, and the rows the legacy permission table gives right U |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Treatment and offer R: read only, in scope |
| RW-PRODHEAD, RW-CREDCOMM | Treatment and offer RA: the approval of a route, which is a sibling story's and not this step's |
| SY-CASEWF, SY-RULES, SY-AGENT | Treatment and offer R: the service identities read the step and are subject to the same checks |
| rwb-valuation service identity | Runs the step, reads the score data product and the rule row, writes the decision record and answers the route operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S1 T6.1 and of the legacy permission table of this key, and nothing wider. The step runs under the service identity with no officer task on the happy path; FSD S1 A2.5.3.3 gives the primary role as "None; runs unattended" and the case owner as the second user.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-ACE-270 to DF-ACE-279 | `v_ace_score` (P1) | score_key, account_key, model_code, model_version, score_value, estimate_value, route_code, scored_at | Read only, on the rwb-source-data data product (DP-05) |
| DF-DEC-019 to DF-DEC-027 | `score` as TSD S1 T3.1 declares it (REUSE ACE) | id, account_id, case_id, model_code, model_version, score_value, estimate_value, route_code, scored_at | Not owned and not written here: the reuse of ACE's score is read on the data product (GAP-2610; ASM-4312) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_valuation`) | rule id, rule version, inputs reference, outcome, decided at, plus the model code and version of the answer | Write, one record per assessment, before the answer is used (DP-03) |
| DF-REF-001 to DF-REF-015 | `rule_row` (P7) | rule_id, rule_version, route_set, from_state, event_code | Not read as a table: the rule, its version and the route set arrive on the rwb-decision row |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` (P3) | id, case_no, product_group, status, stage_code | Not read as a table: the case state arrives on the rwb-case row |
| The recommendation elements | `rwb_decision` (P7) | recommended, reasons, expectedReturnByRoute, ruleVersion, agentVersion | Consumed, not stored |

Field IDs are those of the Logical Data Model and Data Dictionary v9, of TSD S1 T3.1 and of the legacy Data table, with the owners changed by the target. **No new table, no new column and no migration**: the schema `rwb_valuation` and its login arrive with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in it by the library's migration (DP-03). Where the data owner names a column or a `score` table of this service, the DB story adds it and this story's writer fills it; until then the per-route answer lives in the decision record only.

**No personal data.** The rows this story reads and writes carry identifiers, codes, amounts, dates, a model version and a rule version. No name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log, a data-product call or a workflow input, and every fixture is synthetic.

### 12. Contract

Contract version: v1 (base `/api/recovery/valuation/v1`).

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This story supplies the behaviour behind the one operation the legacy story names, and its shape is baselined by RWB-S1-E4005-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out, with the case, the decision and the status elements of the baseline; the expected return per route and its versions are read on the recommendation operation of rwb-decision (API-S1-001) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat, and no second record is written |

The step itself adds no REST operation: no source names a published operation for the per-route answer, whose surface is the decision record, the recommendation read of rwb-decision and the route operation above, and the contract slice fixes that surface (GAP-2613). The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library or a consumed row does not answer.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The per-route score data-product read (operation name Not specified in the source documents (GAP-2609; ASM-4311)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The expected return, the model code and version, the scored-at time per route and the account, and the freshness stamp; faked |
| `GET /cases/{caseId}/recommendation` | `/api/recovery/decision/v1` | P7 rwb-decision | The recommendation with its reasons, `expectedReturnByRoute`, `ruleVersion` and `agentVersion`, as the ledger projects the recorded answer; read only; faked |
| The rule-in-force and route-set read (operation name Not specified in the source documents (GAP-2609; ASM-4311)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id, the rule version and the route set in force for the business date; faked |
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state and its route state, checked before the step runs; read only; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). These rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2609 with ASM-4311.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event, so this story adds no name, no outbox row and no payload to `rwb.valuation.events.v1`, and a build that publishes one here fails the absence test (BR9). The one publication of the step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1` in the transaction of the step.

#### 12.4 Events consumed

None. FSD S1 A2.5.2 names three possible triggers, "a completed ACE batch, an event or a timer", and no source publishes an event name for any of them; the ownership rows give S1 no job and no event, so the step is started by the route command inside `RouteDecisionWorkflow` and subscribes to nothing (GAP-2612; ASM-4314). The freshness of the score product is read as an element of the rwb-source-data row, and a duplicate of the route command is caught by the idempotency row and not by a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` | Input: the case, the asset key, the route set and the rule package in force; signals: the freshness answer of the data product and the outcome of each route assessment |
| `collectReturnByRoute` | Activity, the read and fallback of this story | `rwb-valuation` | The case, the account and the route set in force in; the per-route return, the model code and version, the scored-at time, the fallback flags and the freshness answer out |
| `recordReturnByRoute` | Activity, the record and answer of this story | `rwb-valuation` | The per-route answer and its versions in; the decision record, the idempotency row and the step outcome out, in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1, and the two activities are this story's; the remaining activities of the route decision belong to the sibling stories. The activity names are a target design choice and are fixed by the baseline so that the workflow history is stable.

Start rule of `RouteDecisionWorkflow` (Temporal Catalog v1): started by `CaseWorkflow` as a child when the case reaches route decision D6, or is reopened (`ROUTE_D6_REOPEN`). Workflow ID form: Not specified in the source documents (CG-ALL-8034). Start or signalWithStart: Not specified in the source documents (CG-ALL-8034). Duplicate-start policy: Not specified in the source documents (CG-ALL-8034).

#### 12.6 Schedules

None. The step runs inside the workflow from the route command and owns no Temporal Schedule and no legacy Quartz job, because the ownership rows give S1 no job. A batch-completion trigger is not built: no source names the event or the Schedule it would need (GAP-2612; ASM-4314).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table; the store of the per-route answer is not fixed (GAP-2610; ASM-4312) |
| decision_record | PLT library, created in `rwb_valuation` | The local hash-linked decision record, one per assessment (DP-03) |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

Not owned and never read as a table: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `proceeds` (P8), `template` (P6), `deviation` (S8), `document` and `document_custody` (P5), and every `v_ace_*` view (P1), `v_ace_score` included. No foreign key leaves `rwb_valuation`: the case, the account, the score and the rule are identifiers, not keys across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data score fake | Account `ACC-2026-000405` with an estimate for each route R1 to R8, model `COLLINS` at its version, a scored-at time and a fresh stamp; the same account with one route without an answer; the same account with no route answered; a stale product with its date; no answer beyond 2 s | AC1, X5, X6, X7, TC-E4-005-01 |
| rwb-decision recommendation fake | The recommendation of case `RC-2026-000405` with `expectedReturnByRoute`, `reasons`, `ruleVersion` and `agentVersion`; a case with no recommendation yet | AC1, TC-E4-005-01 |
| rwb-decision rule-in-force fake | The rule id, the rule version and the route set at their version in force for the business date; a business date with no rule row | TC-E4-005-01, X3 |
| rwb-case case-state fake | Case `RC-2026-000405` at the route decision; a case in another state | X3 |
| rwb-access authorise fake | Treatment and offer, right U accepted and refused | TC-E4-005-03, X2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000405`, with the per-route answer and the route elements read once | TC-E4-005-01 |

The fakes are test-only and are replaced by the real services in SIT. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2609; ASM-4311).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-source-data score row, the two rwb-decision rows, the rwb-case state and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `collectReturnByRoute` and `recordReturnByRoute` on `rwb-valuation`; no Schedule |
| File | None of this service | The scores arrive through ACE ingestion and the rwb-source-data contract; this service writes and reads no file (GAP-2609) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.valuation`, module `returnbyroute`, Java package `th.co.scb.ace.workbench.recovery.valuation.returnbyroute`; front end `src/modules/recovery/valuation/RouteReturn.tsx`, the fragment SCR-13 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant and reads no ACE view and no ACE table, and the COLLINS answer is the one the rwb-source-data contract carries. DP-03 is the transaction rule of the step: the record, the idempotency row and the step outcome commit together or not at all. DP-13 moves the base of the one operation. DP-19 is how SCR-13 reaches this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The five consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2609 (ASM-4311). The three H rows of the metadata are the contract of this key and the two platform contracts of DP-03 and DP-19, and no other H row is added.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RouteDecisionWorkflow` return branch | Workflow | Runs the return-by-route step after the appraisal is accepted and reports the per-route answer to the parent |
| `collectReturnByRoute` | Activity | Reads the route set and the scores, applies the fallback per missing route, computes the fallback flags and returns the answer |
| `recordReturnByRoute` | Activity | Writes the decision record and the idempotency row with the answer and returns the step outcome |
| `SourceDataScoreClient` | Client | The per-route score read of rwb-source-data, one hop, 2 s, breaker, with the stale and no-answer paths |
| `DecisionReadClient` | Client | The recommendation read and the rule-in-force and route-set read of rwb-decision, one hop, 2 s |
| `CaseStateClient` | Client | The case state read of rwb-case, one hop, 2 s |
| `ReturnDecisionRecordWriter` | Library adapter | Writes one record per assessment before the answer is used, hash-linked, and refuses the step when the write fails (DP-03) |
| `RouteController` | Controller | The route operation, its capability area and right, the `Idempotency-Key`, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `RouteReturn` | React component | Shows the expected return per route, the route set and the versions, and the held, fallback and refused states on SCR-13, read only |

**Database and migrations.** The schemas `rwb_case`, `rwb_decision` and `rwb_source_data` are owned by P3, P7 and P1 and are named here only as schemas the boundary test refuses (DP-01). No Flyway file. `rwb_valuation` and its login arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in it by the library's migration (DP-03). No column is added for the per-route answer: it lives in the decision record, and the store is GAP-2610 until its owner names it.

**Configuration and reference data.**

- The route codes of `LOV-ROUTE` at their version in force (TSD S1 T3.2), read as a list and never enumerated in code.
- The rule id, the rule version and the route set are read from rwb-decision for the business date and are never constants of the build.
- The capability area Treatment and offer and its rights are access rows of rwb-access, read through the guard.
- The consumer of the library's topic `rwb.decision-record.v1` is the ledger's; this service only writes the record.
- No parameter is named in the sources for the step's timeout or its fallback, and no S1 rule package is in force (GAP-2611; ASM-4313).
- Reference-data contract: the lists and the parameters of this step are read from reference data; the parameter names are Not specified in the source documents (DOR-RWB-S1-E4005-APP-20).

**Build steps**

1. The return branch of `RouteDecisionWorkflow` and its input record, registered on `rwb-valuation`, with the route command as its trigger.
2. `SourceDataScoreClient` against its fake, with the 2 s budget, the breaker, the stale path and the no-answer path (X4, X5).
3. `DecisionReadClient` and `collectReturnByRoute`, with the full answer, the one-route-missing and the no-route-answered paths (X6, X7).
4. `ReturnDecisionRecordWriter` against the library stub, with the failed-write path (AC2, X1).
5. `recordReturnByRoute` with the idempotency row and the repeat of the same command (X8).
6. `CaseStateClient` and the state guard of the step (X3).
7. `RouteController` with the right, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (TC-E4-005-03).
8. `RouteReturn` and SCR-13 through the composite route fake (TC-E4-005-01).
9. The boundary test: no statement outside `rwb_valuation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or `rwb_source_data`, and no outbox row (X9, BR8, BR9).

**Feature flag.** `rwb.valuation.return-by-route-v1`, read as a flag of the platform library; off means the step records the rule result for every route with its fallback flag and the route decision continues without a model answer.

**Done when.** The tests of section 16 pass, every route of the set carries an answer or a recorded fallback in SIT, the record carries the model version and the rule version, a stale product writes nothing, a forced record failure changes nothing and shows MSG-P7-003, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-13 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of a request or of the score row is absent or invalid (X3) | Enter {field}. |
| MSG-P4-002 | A role without the Treatment and offer right calls the route operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the answer is used (X1, AC2) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product behind the scores is stale after a late or failed batch (X5) | {product} is from {date}. Today's ACE batch has not arrived. |

The four message IDs are the rows of FSD S1 A2.5.3.1, of the legacy message set of this key and of the platform set, and the text is the legacy wording, copied unchanged; no message is reworded and no new one is added.

SCR-13 Route decision has no empty or error state in the source documents: Not specified in the source documents (CG-ALL-8041). Its no-access state is the refusal with MSG-P4-002.

### 15. Screens and states

SCR-13 Route decision is served through the gateway-bff composite route (DP-19), and this story fixes the return part of its answer and the states it can show.

| Screen | States | What this story sets |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted; empty, error and no access: Not specified in the source documents (CG-ALL-8041) | Loading while the per-route answer is collected; recommendation with the expected return per route, the route set and its version, the model version and the fallback flags; overridden with the owner's reason; submitted with the route answer. Plus refused with MSG-P4-002, not recorded with MSG-P7-003, and stale data with MSG-P1-001 |

The screen's route elements, its merge order and its field list belong to RWB-PLT-N001-CON and the sibling route stories of this service; the per-route element list and the four service states above are this story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-005-01 | AC1: the expected return for each route of the set is read and recorded with its model version and its rule version; a route with no answer takes the recorded fallback; a stale product answers nothing | Component | Case `RC-2026-000405` with account `ACC-2026-000405`, a score for each route R1 to R8, one route without an answer, a stale product |
| TC-E4-005-02 | AC2: the decision record cannot be written | Component | The decision-record stub stopped; nothing written, no answer returned and MSG-P7-003 shown |
| TC-E4-005-03 | Access: a role without the right | Component | A role without Treatment and offer U; 403 with MSG-P4-002 and no read |
| TC-E4-005-05 | AC4: the case is not at the route decision or the route set is absent; the step does not run and the state is reported | Component | Case `RC-2026-000405` at a state other than the route decision, and a business date with no rule row |
| TC-E4-005-06 | AC5: rwb-decision or rwb-source-data does not answer inside 2 s or its breaker is open; the step retries, writes nothing and the caller sees 503 | Component | rwb-source-data score fake with no answer beyond 2 s; breaker open |
| TC-E4-005-07 | AC6: a stale ACE data product holds the step, writes nothing and shows the data date | Component | rwb-source-data score fake with a stale product and its date |
| TC-E4-005-08 | AC7: a route with no answer takes the rule result, the fallback is recorded and the route decision continues | Component | Case `RC-2026-000405` with one route of account `ACC-2026-000405` without an answer |
| TC-E4-005-09 | AC8: every route without an answer; no answer is asserted, the fallback is recorded for each route and the missing answer is reported to the parent | Component | Case `RC-2026-000405` with account `ACC-2026-000405` and no route answered |
| TC-E4-005-10 | AC9: a repeated command with the same Idempotency-Key gives one record and returns the stored answer | Component | The route command submitted twice with the same key |
| TC-E4-005-11 | AC10: boundary: no statement outside rwb_valuation, no v_ace_* read, no event, no personal data and no model gateway call | Component | The read and write statements of the service and its build |
| TC-E4-005-12 | AC11: error answers 401 and 404 of the route operations, with 403 as in AC3 | Component | Not specified in the source documents (NEWAC-RWB-S1-E4005-APP-AC12) |
| TC-E4-005-13 | AC12: a replay of a write with the same Idempotency-Key writes no second record and returns the stored answer | Component | Not specified in the source documents (NEWAC-RWB-S1-E4005-APP-AC13) |
| TC-E4-005-14 | AC13: a retried or timed-out activity writes no second record and the step waits and retries on the workflow's own schedule | Component | Not specified in the source documents (NEWAC-RWB-S1-E4005-APP-AC14) |
| TC-E4-005-15 | AC14: a consumed call that fails or does not answer writes nothing and the caller sees 503 with the platform envelope | Component | Not specified in the source documents (NEWAC-RWB-S1-E4005-APP-AC15) |
| TC-E4-005-16 | AC15: a status change the model does not allow is refused and nothing is recorded | Component | Not specified in the source documents (NEWAC-RWB-S1-E4005-APP-AC16) |
| TC-E4-005-04 | Principle 5: a forced decision record write failure | NFR | A forced failure at the moment of the answer and the record; no record, no answer and no event |
| TC-S1-E4005-APP-01 | The boundary: no `v_ace_*` read, no foreign schema write and no published event | Component | The build scan of step 9, plus an outbox that must stay empty |
| TC-S1-E4005-APP-02 | Contract: the operations of the route base `/api/recovery/valuation/v1`, the activities `collectReturnByRoute` and `recordReturnByRoute` of section 12.5 and the no-event rule of the change log match their contract elements | Contract | The API yaml of the route base and the section 12.5 contract elements |
| TC-S1-E4005-APP-03 | The boundary for the tables of section 12.7: only `decision_record` and `idempotency_key` are written, in `rwb_valuation`, and no other table is read or written | Component | The read and write statements of the service against each table of section 12.7 |

The four legacy case IDs are the legacy cases of RWB-E4-005 in their legacy order, with the Level column added. TC-E4-005-01 is Component because the step is tested on its fakes; the legacy wording of the case is kept in the Test Cases workbook, where the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases. The `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the route codes of `LOV-ROUTE`, the route set, the rule version and the model code stay data or answers in force, never a constant, a default or a branch of the build.
- No personal data in `rwb_valuation`, in a data-product call, in a workflow input or in a log: identifiers, codes, amounts, dates, a model version and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case stays with rwb-case and the rules with rwb-decision: no `recovery_case`, `assignment`, `task` or `timer` row and no `rule_row` read is written here (BR6, BR8).
- The answer is recorded before it is used and the command is idempotent; a build that returns an answer or shows it before its record fails the review (DP-03, BR4, BR7).
- No answer is invented: a route without a score takes the rule result with its fallback flag, and no return, model version or scored-at time is synthesised (R-UNI-32, BR3).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no event published by this step, no `v_ace_*` read, no direct Model gateway call.

### 18. Traceability

| Source | Reference | Used in | Feature | L3 process |
|---|---|---|---|---|
| Legacy story | RWB-E4-005, disposition Split (rework); AC1 and AC2 owned word for word by this story | 1, 7, 16 | FEAT-VAL-05 | Not specified in the source documents (DOR-RWB-S1-E4005-APP-2) |
| Feature | FEAT-VAL-05 Call COLLINS for return by route, module S1, epic E4, depends on FEAT-AGT-01 | 1, 2, 3 | FEAT-VAL-05 | Not specified in the source documents (DOR-RWB-S1-E4005-APP-2) |
| FSD S1 v3 | A1.4 preconditions; A2.5.1 intent and metric; A2.5.2 steps, integration points and prerequisite; A2.5.3.1 VR-S1-005-1 and BR-S1-005; A2.5.3.3 roles; A2.5.4.1 AC-S1-005-01; A2.5.4.3 exception flows; SCR-13 | 2, 3, 4, 5, 8, 14, 15 | FEAT-VAL-05 | Not specified in the source documents (DOR-RWB-S1-E4005-APP-2) |
| TSD S1 v2 | T2 components; T3.1 `score` (REUSE ACE) and `valuation`; T3.2 `LOV-ROUTE`; T3.3 relationships; T4 no state machine; T5.2 and T5.3; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 13, 16 | FEAT-VAL-05 | Not specified in the source documents (DOR-RWB-S1-E4005-APP-2) |
| API specification v4 | `POST /cases/{caseId}/route` with `RouteRequest` and `Approval`; `GET /cases/{caseId}/recommendation` with `expectedReturnByRoute`, `reasons`, `ruleVersion` and `agentVersion` | 11, 12.1, 12.2, 12.8 | FEAT-VAL-05 | Not specified in the source documents (DOR-RWB-S1-E4005-APP-2) |
| Logical data model | DF-ACE-270 to DF-ACE-279, DF-DEC-001 to DF-DEC-018, DF-DEC-019 to DF-DEC-027, DF-REF-001 to DF-REF-015, DF-CAS-001 to DF-CAS-023 | 11 | FEAT-VAL-05 | Not specified in the source documents (DOR-RWB-S1-E4005-APP-2) |
| Routing logic | R-UNI-32, R-UNI-38, R-UNI-39 and R-UNI-40; the D6 rows ROUTE_D6_REOPEN and BACK_TO_ROUTE_DECISION; no S1 route rule is in force, because the S1 package is Phase 2 | 4, 8, 9, 14 | FEAT-VAL-05 | Not specified in the source documents (DOR-RWB-S1-E4005-APP-2) |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 | FEAT-VAL-05 | Not specified in the source documents (DOR-RWB-S1-E4005-APP-2) |
| Gaps and assumptions | GAP-2609 to -4 and -6; ASM-4311 to -4 and -6; the contract gaps GAP-2610, -5 and -6 belong to RWB-S1-E4005-CON and are cited here where the surface is read | 1, 3, 4, 11, 12, 13, 14, 16 | FEAT-VAL-05 | Not specified in the source documents (DOR-RWB-S1-E4005-APP-2) |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all | FEAT-VAL-05 | Not specified in the source documents (DOR-RWB-S1-E4005-APP-2) |

### 19. Out of scope

- The published shape of the route operation, the consumed rows, the record element, the workflow elements, the error set and the fakes: RWB-S1-E4005-CON.
- The route agent that scores the routes and recommends one with reasons (FEAT-VAL-07), and every live model call through the Model gateway and INT-23: rwb-agent (P10) (GAP-2614).
- The ACE score facts, the COLLINS ingestion and the freshness of the data product: rwb-source-data (P1). The store of the per-route answer: the data owner of this service (GAP-2610).
- The case of record, its route states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the package version, its approval and the central ledger: rwb-decision (P7). The rule id and the route set of this step: GAP-2611.
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, its merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The appraisal order and acceptance, the payoff and settlement range, the approvals inside and above the limit, the hold and the route flow start: the sibling route stories of this service.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
