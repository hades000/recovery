# RWB-S1-E4001-APP Order an appraisal when the last one is stale

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S1-A |
| Size | Not specified in the source documents (DOR-RWB-S1-E4001-APP-16); the squad sizes it at refinement |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S1-E4001-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract fake library version | Not specified in the source documents (DOR-RWB-S1-E4001-APP-22) |
| Contract version built against | Not specified in the source documents (DOR-RWB-S1-E4001-APP-23); the route base is /api/recovery/valuation/v1 |
| SCR-13 states (empty, loading, error, no access) | Not specified in the source documents (DOR-RWB-S1-E4001-APP-10) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-001 split out for rwb-valuation. The legacy criterion this story owns is copied word for word with its origin tag; the age check becomes the first step of `RouteDecisionWorkflow` on task queue `rwb-valuation`, reads the appraisal and its acceptance on the rwb-source-data data product (DP-05), computes the age against the limit held as data, raises the order through rwb-integration with no person involved, records the outcome through the local decision-record library before anything is written (DP-03) and answers the route operation on base `/api/recovery/valuation/v1` (DP-13), reached by SCR-13 through the gateway-bff composite route (DP-19). No event is published, because the ownership rows give S1 none. The operation names of the six consumed rows and the SVAF interface are not published (GAP-2590; ASM-4287); the store of the stale flag, the age and the acceptance is not fixed by any source (GAP-2591; ASM-4288); no S1 rule package is in force and no source names the age limit's parameter (GAP-2592; ASM-4289); no source names the event or the timer that starts the check on a completed batch (GAP-2593; ASM-4290). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S1-E4001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (37 resolved, 21 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **the Workbench to check the appraisal age against the limit and raise the order to SVAF with no person involved**, so that **the route is chosen on expected return with reasons**.

This is the application slice of legacy RWB-E4-001. It owns:

- the legacy criterion AC2 of the key, copied verbatim, and the rules, messages and screens it depends on;
- the age check as the first step of `RouteDecisionWorkflow` on `rwb-valuation`, started by the route-decision command of the case;
- the read of the appraisal, its date and its acceptance on the rwb-source-data data product, one hop, 2 s, read only, with no `v_ace_*` grant of this service (DP-05);
- the comparison of the appraisal age against the limit held as data with its version, and the stale flag that follows from it, computed per assessment and never written as a constant;
- the order to SVAF, raised through rwb-integration as an outbound interface run, logged and retried by its owner, with no person in the path;
- the decision record of the step, written through RWB-PLT-E1027-CON in the caller's transaction before anything else changes, with the rule id and the version in force (DP-03);
- the route operation `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`, its right, its `Idempotency-Key` and its answer, whose shape is baselined by RWB-S1-E4001-CON (DP-13);
- the states of SCR-13 Route decision that this step produces, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the route operation, the six consumed rows, the decision-record element, the workflow elements, the rights, the error set and the fakes, which are RWB-S1-E4001-CON; the cross-service journey of the key and its evidence, which is RWB-ITG-E4001-ITG and owns AC1; the ACE appraisal, collateral and acceptance facts and the freshness of the data product, which are rwb-source-data's (P1); the SVAF interface, its transport and its retry rule, which are rwb-integration's (P2); the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case's (P3); the rule rows, the package version and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; the two valuation operations, which are RWB-S1-E4002-CON; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

A route chosen on an appraisal older than the limit values the security on a stale number, and the bank then negotiates, litigates or prices a sale on a figure it cannot defend. The FSD keeps the feature as FEAT-VAL-01 in module S1: the age is checked against the limit and the order is raised to SVAF with no person involved, and the step writes its result to the decision log with its rule version. The requirement the feature serves is REQ-S1-001: an appraisal older than the policy limit triggers a new valuation order without a person asking for it. The measure of the module is unchanged: recommendations accepted, read monthly from the decision log and the Workbench records.

Under D-RCV-60 the ownership of the four facts changes, and that is what this story carries.

- **the appraisal is ACE's, not this service's.** `v_ace_valuation` is ACE's and only rwb-source-data reads the `recovery.v_ace_*` views, so the appraisal, its date and the acceptance arrive on the owner's data product with its freshness stamp and are never read as a table here (DP-05; Architecture v5 slide 8, the 30 `recovery.v_ace_*` views read only by rwb-source-data).
- **the order is not this service's interface.** rwb-integration owns every outbound item, so the order is submitted there, logged, retried on its schedule and placed in an exception queue after the retry limit; this service raises it and never writes a file or calls SVAF (GAP-2590).
- **the case stays with rwb-case.** The case, its route states, its tasks and its timers are rwb-case's; this story answers the route decision and reports the step outcome, and writes no case row.
- **the decision is recorded first.** Legacy AC2 is the rule that makes the step trustworthy: when the record cannot be written nothing changes and the user sees MSG-P7-003. Under DP-03 the record is local, hash-linked and written in the same transaction as the step, and R-UNI-39 says no action proceeds unlogged.
- **nothing is published.** The ownership rows give S1 no event, so the step adds none to `rwb.valuation.events.v1`; its outward facts are the route answer, the interface run of the order and the decision record, which the library sends to `rwb.decision-record.v1` (ASM-4286).

The limit itself is a value of reference data with a version, never a constant: the harness of this key names an appraisal stale after twelve months (RWB-ITG-E4001-ITG §2, citing the Temporal and Drools Detailed Design v1), and this story reads whatever limit is in force rather than asserting a number.

### 3. Preconditions

- RWB-S1-E4001-CON is published: the route operation, the six consumed rows, the decision-record element, the workflow elements, the rights, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-13 Route decision reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The rwb-source-data data product that carries the appraisal of `v_ace_valuation`, the acceptance of `valuation_ext` and the collateral link is published with its fake and its freshness stamp. Its operation name is Not specified in the source documents (GAP-2590; ASM-4287), and the row is not in this story's contract-dependency list, which is None.
- rwb-integration publishes the order submission and the interface-run read; its operation names, the SVAF interface identity, its transport and its order layout are Not specified in the source documents (GAP-2590; ASM-4287).
- The rwb-case case-state read and the rwb-decision rule-in-force read are available for their fakes; the rwb-case read is `GET /cases/{caseId}` on its published base, and the rwb-decision row carries the placeholder (GAP-2590; ASM-4287).
- The limit that the age is compared against is a row of reference data or of a rule row in force, read with its version and never written in code; the sources name neither the parameter nor the rule id of this step, and no S1 rule package is in force (GAP-2592; ASM-4289).
- The service runs as its own login on schema `rwb_valuation`, holds the library objects `decision_record` and `idempotency_key`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_valuation`, `recovery.valuation_ext` or `rwb_case` is refused by the database and fails the boundary test (DP-01, DP-05).
- Where the stale flag, the age and the acceptance are persisted is not fixed: the Ownership Map gives S1 no table, TSD S1 T3.1 declares `valuation` as a NEW Workbench table and the FSD holds the acceptance in `recovery.valuation_ext` (GAP-2591; ASM-4288).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S1-E4001-CON when its tests pass.

### 4. Flow

1. The case is at the route decision and the case owner or the route flow submits the decision through `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the command starts `RouteDecisionWorkflow` on task queue `rwb-valuation` (API-S1-001; DP-13).
2. The first step of the workflow is `checkAppraisalAge`: it reads the appraisal of the asset on the rwb-source-data data product, one hop with a 2 s budget and a breaker, being the appraisal number, its type, its value, the forced sale value, the appraisal date, the acceptance fields on the rwb-source-data data product and the freshness stamp (DP-05; GAP-2589; GAP-2590).
3. If the product is stale after a late or failed ACE batch, the step holds, writes nothing, records no decision and shows MSG-P1-001 with the data date; it resumes on the next fresh answer (VR-S1-001-1, X5).
4. The step computes the age of the appraisal from its date and the business date and compares it with the limit in force, read as reference data with its version; the limit is never a constant and the source names neither the parameter nor the rule id (GAP-2592; ASM-4289).
5. Where the appraisal is inside the limit, no order is raised: the step records its outcome with the limit version, reports "not stale" to the workflow and the route decision continues on the accepted appraisal; where the acceptance is absent the route decision names the missing acceptance and no order is raised on an unaccepted value.
6. Where the appraisal is older than the limit, the step raises the order through rwb-integration with no person in the path: the case, the asset key, the appraisal number being replaced, the appraisal date, the value and the reason. rwb-integration logs the item, retries it on its schedule and places a failure in its exception queue; this service writes no file and does not call SVAF; rwb-integration owns the SVAF interface and its retries (GAP-1683; GAP-2590; ASM-4287).
7. A refused or failed order does not roll the case back: the step reports the failure and the interface-run reference, the case stays at the route decision and the failure is raised to the owner of rwb-integration; nothing is retried by this service beyond the one retry of a GET (X4).
8. Before any of the above is committed, `AppraisalDecisionRecordWriter` writes one decision record through the local library: the case, the appraisal number, the age, the limit with its version, the stale flag, the order reference with its date and the outcome. The age and the stale flag are held in this record only; the acceptance is read on the rwb-source-data data product and no column of this service holds it (GAP-1683; GAP-2591). A failed write stops the step with nothing changed and nothing raised (DP-03; AC2, R-UNI-39).
9. The step answers the workflow with the step outcome; the route operation answers `Approval` with the route elements and the appraisal elements of the baseline, and a repeat of the same `Idempotency-Key` returns the stored answer and raises no second order (R-UNI-40; API-S1-001).
10. The decision record reaches `rwb.decision-record.v1` through the library of DP-03, keyed by the case, with no personal data on it; this service publishes no event of its own (ASM-4286).
11. SCR-13 Route decision shows the appraisal, its age, the order and its interface run, and the overridden or submitted state, read through the gateway-bff composite route, read only (DP-19).
12. Where a later ACE batch brings a new appraisal, the next assessment of the same case reads it and runs the same check; the previous order and its record stay as the evidence of why the order was raised.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing, no order is submitted and the route answer is refused | MSG-P7-003 | AC2, TC-E4-001-02, TC-E4-001-04 |
| X2 | The role does not hold the Treatment and offer right of the operation | 403 before any read or write, and no record is written | MSG-P4-002 | AC3, TC-E4-001-03, TC-S1-E4001-APP-04 |
| X3 | The case is not at the route decision, or the asset of the appraisal is not on the case | The step does not run, nothing is ordered and the state is reported to the parent | None | AC4, TC-E4-001-01, TC-S1-E4001-APP-05 |
| X4 | rwb-integration refuses the order or the interface run fails after the retry limit | The case stays at the route decision, the failure and its run reference are recorded, and the exception queue of rwb-integration holds the item | None | AC5, TC-E4-001-01, TC-S1-E4001-APP-06 |
| X5 | The ACE data product is stale after a late or failed batch | The step holds, writes nothing and shows the data date; it resumes on a fresh answer | MSG-P1-001 | AC6, TC-E4-001-01, TC-S1-E4001-APP-07 |
| X6 | The appraisal has no acceptance in `valuation_ext` | No order is raised on an unaccepted value, and the route decision names the missing acceptance | MSG-GEN-001 | AC7, TC-E4-001-01, TC-S1-E4001-APP-08 |
| X7 | The appraisal is inside the limit | Nothing is ordered; the outcome is recorded with the limit version and the route decision continues | None | AC8, TC-E4-001-01, TC-S1-E4001-APP-09 |
| X8 | rwb-source-data or rwb-case does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and the caller sees 503 with the platform envelope | None | AC9, TC-E4-001-01, TC-S1-E4001-APP-10 |
| X9 | The same assessment is submitted twice with the same `Idempotency-Key` | One record, one order, and the stored answer is returned; the repeat is counted | None | AC10, TC-E4-001-01, TC-S1-E4001-APP-11 |
| X10 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC11, TC-S1-E4001-APP-12, s17, BR4, BR8 |

X1 and X2 are the exception paths of the legacy key carried onto the split, X3 to X9 are the paths the target call types add, and X10 is the DP-05 and DP-01 boundary. Percentages, limits and thresholds are values in force, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S1-E4001-CON, the rwb-source-data, rwb-integration, rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P2, P3 or P7 |
| Negotiable | The activity and consumer names, the decision code and the shape of the step outcome are this story's choice; the operation, the rules, the messages, the screen and the appraisal elements are fixed |
| Valuable | A stale appraisal raises its order the day the route decision is taken, with nobody chasing it, and the reason is on the record |
| Estimable | One workflow step, two activities, four clients, one record write, one order submission and one screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each path runs on synthetic appraisals through the contract fakes, plus the stopped record write, the stale product, the inside-limit case and the duplicate command |

### 7. Acceptance criteria

```gherkin
Feature: Order an appraisal when the last one is stale

  Scenario: AC2 Not recorded (legacy RWB-E4-001 AC2)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Role without the Treatment and offer right (exception X2) (new, D-RCV-60)
    Given a role does not hold the Treatment and offer right of the operation
    When the role calls the route operation
    Then the answer is 403 with MSG-P4-002 before any read or write and no decision record is written

  Scenario: AC4 Case not at the route decision or asset not on the case (exception X3) (new, D-RCV-60)
    Given the case is not at the route decision, or the asset of the appraisal is not on the case
    When the step is reached
    Then the step does not run, nothing is ordered and the state is reported to the parent

  Scenario: AC5 Order refused or interface run failed (exception X4) (new, D-RCV-60)
    Given rwb-integration refuses the order, or the interface run fails after the retry limit
    When the order is submitted
    Then the case stays at the route decision, the failure and its run reference are recorded and the exception queue of rwb-integration holds the item

  Scenario: AC6 Data product stale (exception X5) (new, D-RCV-60)
    Given the ACE data product is stale after a late or failed batch
    When the step checks freshness
    Then the step holds, writes nothing and shows MSG-P1-001 with the data date, and resumes on a fresh answer

  Scenario: AC7 No acceptance in valuation_ext (exception X6) (new, D-RCV-60)
    Given the appraisal has no acceptance in valuation_ext
    When the step checks the acceptance
    Then no order is raised on an unaccepted value and the route decision names the missing acceptance with MSG-GEN-001

  Scenario: AC8 Appraisal inside the limit (exception X7) (new, D-RCV-60)
    Given the appraisal is inside the limit
    When the step checks the age
    Then nothing is ordered and the outcome is recorded with the limit version and the route decision continues

  Scenario: AC9 Source or case no answer inside 2 s (exception X8) (new, D-RCV-60)
    Given rwb-source-data or rwb-case does not answer inside 2 s, or its breaker is open
    When the step reads
    Then nothing is written and the caller sees 503 with the platform envelope

  Scenario: AC10 Repeat with the same Idempotency-Key (exception X9) (new, D-RCV-60)
    Given the same assessment is submitted twice with the same Idempotency-Key
    When the second submission arrives
    Then one record and one order exist, the stored answer is returned and the repeat is counted

  Scenario: AC11 Boundary reached (exception X10) (new, D-RCV-60)
    Given a component, a statement or a test reaches a v_ace_* view, a recovery_case row or another service's schema
    When the statement runs
    Then the grant refuses the statement, the boundary test fails the build and nothing is released

  Scenario: AC12 Business rules BR1 to BR10 hold (new, D-RCV-60)
    Given the appraisal step runs for a case and its appraisal
    When the step reads, decides, orders and records
    Then no v_ace_* view is read, the limit is read from reference data with its version, the order leaves only through rwb-integration, no person data is stored or passed, no foreign key leaves rwb_valuation and no event is published

  Scenario: AC13 Error answers of the route operation (new, D-RCV-60)
    Given the caller presents no valid identity, or the case of the route is not found
    When the route operation is called
    Then the answer is 401 for no valid identity or 404 for an unknown case, with the platform envelope, and no read or write is made

  Scenario: AC14 Activity retried or timed out (new, D-RCV-60)
    Given an activity of the route workflow fails or does not finish inside its timeout
    When the workflow retries it
    Then the activity is retried on the workflow's schedule, and after the retry limit the case stays at the route decision with the failure recorded

  Scenario: AC15 Consumed call fails or does not answer (new, D-RCV-60)
    Given a consumed call fails or does not answer
    When the step calls the service
    Then the step waits and retries on the workflow's own schedule, and after the retry limit the case stays at the route decision with the failure recorded

  Scenario: AC16 Status change not allowed by the model (new, D-RCV-60)
    Given a status change the model does not allow is submitted
    When the change is submitted
    Then the change is refused and nothing is written
```

The criterion is the legacy AC2 of the key, word for word, with its origin tag added and nothing else changed: the legacy wording of `the decision record cannot be written` and `the action is taken` stands. AC1 of the same key, "checks the appraisal age against the limit and raises the order to SVAF with no person involved" and "the system writes the result to the decision log with the rule version", is owned by RWB-ITG-E4001-ITG, which carries the cross-service journey of the key and its evidence; the check and the order behind it are built here and are stated in sections 4, 8 and 16. Neither criterion carries a business value: the limit, the appraisal type and the route codes are data in force.

### 8. Business rules

| ID | Rule | Message |
|---|---|---|
| BR11 (VR-S1-001-1) | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR12 (BR-S1-001) | No value a business person may change is written in code; it is read from reference data with its version | None |
| BR13 (R-UNI-39) | The decision log entry cannot be written: block the action and raise an incident; no action proceeds unlogged | MSG-P7-003 |
| BR14 (R-UNI-38) | A new rule version reaches its effective date: apply it to decisions taken from that date; open cases keep the version they were decided under | None |
| BR15 (R-UNI-40) | The same event arrives twice with the same key: ignore the second, record the idempotency hit | None |

The two VR and BR rows are the rows of FSD S1 A2.1.3.1, copied character for character. The three universal rules are the rows of the Business Rules and Routing Logic v4 that this step depends on; R-UNI-38 is why the record carries the limit and the rule version in force on the business date.

| ID | Rule | Source |
|---|---|---|
| BR1 | The appraisal, its date, its value and its type are ACE's and are read only on the rwb-source-data data product; this service holds no `v_ace_*` grant, keeps no copy and reads no appraisal row as a table | DP-05; Ownership Map rows of S1; REQ-S1-001 |
| BR2 | The limit the age is compared with is reference data or a rule row in force, read with its version; no limit, appraisal type or threshold is a constant of the build | FSD S1 A2.1.3.1 BR-S1-001; TSD S1 T3.2; GAP-2592 |
| BR3 | The order leaves only through rwb-integration, which logs it, retries it on its schedule and places a failure in its exception queue; this service writes no file, calls no external system and retries nothing beyond the one retry of a GET | GAP-2590; ASM-4287 |
| BR4 | No person is in the path of the order: the step runs under the service identity, raises no approval task for the order itself and asserts no person's identity in its input | Legacy RWB-E4-001 AC1; FSD S1 A2.1.2 |
| BR5 | The decision is recorded before anything changes, with the rule id and the version in force, the appraisal number, the age, the limit version and the outcome; a failed write changes nothing and shows MSG-P7-003 | DP-03; R-UNI-39; legacy AC2 |
| BR6 | The case is not this service's: no `recovery_case`, `assignment`, `task` or `timer` row is written here, and the case state is read and reported | Ownership Map (`recovery_case` owner P3) |
| BR7 | One order per case and assessment: a repeated command with the same `Idempotency-Key`, and a repeated fact with the same key, raise no second order | API-S1-001; R-UNI-40 |
| BR8 | No foreign key leaves `rwb_valuation` and no statement reaches another schema: the case, the asset, the appraisal and the rule are identifiers of other owners' facts | DP-01; TSD S1 T3.3 |
| BR9 | No event is published: the ownership rows give S1 no event, and the step adds no name to `rwb.valuation.events.v1` | context pack S1 ownership rows; ASM-4286 |
| BR10 | No person name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log, an interface input or a workflow input | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step reports its outcome and the parent `CaseWorkflow` applies it to the case of record (BR6). What this story owns is the state of the appraisal step, and the appraisal states the sources give are the valuation states of the D6.4 route set, the only rows a source publishes for an appraisal order.

| From (appraisal step) | Event | Condition | To |
|---|---|---|---|
| Not assessed | ROUTE_ASSESSMENT_TRIGGERED | The appraisal is older than the limit and accepted | VALUATION_ORDERED, with the order raised and the record written |
| Not assessed | ROUTE_ASSESSMENT_TRIGGERED | The appraisal is inside the limit | Unchanged, the outcome recorded and no order (X7) |
| Not assessed | ROUTE_ASSESSMENT_TRIGGERED | The product is stale, or the acceptance is absent | Held, nothing written (X5, X6) |
| VALUATION_ORDERED | The order reported by rwb-integration | The interface run is delivered | AWAITING_VALUER, and the case waits on the value |
| VALUATION_ORDERED | The order reported by rwb-integration | The run failed after the retry limit | Unchanged, the failure recorded and the exception queue holds the item (X4) |
| VALUATION_ORDERED | The record cannot be written | X1 | Unchanged, nothing raised and no answer (AC2) |
| AWAITING_VALUER | A new appraisal arrives on the data product | The next assessment of the case reads it | Not assessed, and the check runs again |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The route command of a case at the route decision | The workflow is started on `rwb-valuation` | Reading the appraisal |
| Reading the appraisal | The data product answers fresh | The appraisal is accepted | Evaluating the age |
| Evaluating the age | The limit in force is loaded | The age is over the limit | Ordering |
| Ordering | The order is accepted by rwb-integration and the record is written | The transaction commits | Waiting for the next assessment |
| Any | The record write or the transaction fails | X1 | Waiting, nothing changed |

The states VALUATION_ORDERED, AWAITING_VALUER, VALUATION_RECEIVED and VALUATION_ACCEPTED are the valuation states of the D6.4 route set (R-DIL-07 to R-DIL-11), the only rows a source publishes for a valuation order; they live on the case of record and are applied by rwb-case on this step's outcome. No S1 route rule is in force, because the S1 package is Phase 2 (GAP-2592; ASM-4289).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Treatment and offer U in the legacy permission table of the key: submit the route decision and read the appraisal, the order and the record |
| RW-CASEOWN (CRU), RW-RESTRUCT (CRUA), RW-SPECIAL (CRU), RW-GUARANT (CRU) | TSD S1 T6.1 rows for the capability area, and the rows the legacy permission table gives right U |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Treatment and offer R: read only, in scope |
| RW-PRODHEAD, RW-CREDCOMM | Treatment and offer RA: the approval of a route, which is a sibling story's and not this step's |
| SY-CASEWF, SY-RULES, SY-AGENT | Treatment and offer R: the service identities read the step and are subject to the same checks |
| rwb-valuation service identity | Runs the step, reads the data product, submits the order through rwb-integration, writes the decision record and answers the route operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S1 T6.1 and of the legacy permission table of this key, and nothing wider. The step runs under the service identity with no officer task on the happy path. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-ACE-187 to DF-ACE-195 | `v_ace_valuation` (P1) | valuation_key, asset_key, appraisal_no, appraisal_type, appraised_value, forced_sale_value, appraisal_date | Read only, on the rwb-source-data data product (DP-05) |
| DF-EXT-036 to DF-EXT-049 | `valuation_ext` (P1 data product; the acceptance is the accept story's of S1) | valuation_key, accepted, accepted_at, accepted_by, stale_flag, age_days | Read on the data product; the acceptance is written by the accept story and not by this one |
| DF-ACE-091 to DF-ACE-098 | `v_ace_collateral` (P1) | collateral_no, asset_key, collateral_type, register_date | Read only, on the data product, to link the appraisal to the asset of the case |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_valuation`) | rule id, rule version, inputs reference, outcome, decided at | Write, one record per assessment, before anything else changes |
| DF-REF-001 to DF-REF-015 | `rule_row` (P7) | rule_id, rule_version, route_set, from_state, event_code | Not read as a table: the rule and its version arrive on the rwb-decision row |
| DF-COL-018 to DF-COL-027, DF-COL-043 and DF-COL-044 | `valuation` as TSD S1 T3.1 declares it | id, appraisal_no, appraisal_type, appraised_value, appraisal_date, accepted, stale_flag, age_days | Not written here: the store of the flag, the age and the acceptance is not fixed (GAP-2591; ASM-4288) |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` (P3) | id, case_no, product_group, status, stage_code | Not read as a table: the case state arrives on the rwb-case row |
| The order and interface-run elements | `rwb_integration` (P2) | the case, the asset key, the appraisal being replaced, the order reference, the run status and its failure reason | Consumed, not stored |

Field IDs are those of the Logical Data Model and Data Dictionary v9, of TSD S1 T3.1 and of the legacy Data table, with the owners changed by the target. **No new table, no new column and no migration**: the schema `rwb_valuation` and its login arrive with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in it by the library's migration (DP-03). The stale flag and the age are computed per assessment and recorded in the decision record; where the data owner names a column or a `valuation` table, the DB story adds it and this story's writer fills it.

**No personal data.** The rows this story reads and writes carry identifiers, codes, amounts, dates and a rule version. No name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log, an interface input or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This story supplies the behaviour behind the one operation the legacy story names, and its shape is baselined by RWB-S1-E4001-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out, with the appraisal elements, the order and its interface run and the override reason where the answer departs from the recommendation (API-S1-001) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat, and no second order is raised |

The step itself adds no REST operation: no source names a published operation for the appraisal order, whose surface is the rwb-integration interface run and the decision record, and the contract slice fixes that surface (GAP-2590). The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library or a consumed row does not answer. The two valuation operations of the map are the appraisal-intake slice of RWB-S1-E4002-CON and are not touched here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The appraisal and acceptance data-product read (operation name Not specified in the source documents (GAP-2590; ASM-4287)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The appraisal, its date, its value and its type, the acceptance fields, the collateral link and the freshness stamp; faked |
| The SVAF order submission (operation name Not specified in the source documents (GAP-2590; ASM-4287)) | `/api/recovery/integration/v1` | P2 rwb-integration | The order raised to SVAF, logged and retried by its owner and placed in its exception queue on failure; faked |
| The interface-run read (operation name Not specified in the source documents (GAP-2590; ASM-4287)) | `/api/recovery/integration/v1` | P2 rwb-integration | The status of the order as an interface run, keyed by case and appraisal; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state and its asset link, checked before an order is raised; read only; faked |
| The rule-in-force and decision-log read (operation name Not specified in the source documents (GAP-2590; ASM-4287)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id and the version in force, and the record the ledger holds; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). These rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2590 with ASM-4287.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event, so this story adds no name, no outbox row and no payload to `rwb.valuation.events.v1`, and a build that publishes one here fails the absence test (BR9). The one publication of the step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1` in the transaction of the step.

#### 12.4 Events consumed

None. FSD S1 A2.1.2 names three possible triggers, "a completed ACE batch, an event or a timer", and no source publishes an event name for any of them; the ownership rows give S1 no job and no event, so the step is started by the route command inside `RouteDecisionWorkflow`, at the decision start, at its reopening and when an appraisal arrives, and subscribes to nothing (GAP-2593; ASM-4290). The freshness of the data product is read as an element of the rwb-source-data row, and a duplicate of the route command is caught by the idempotency row and not by a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` | Input: the case, the asset key, the route set and the rule package in force; signals: the freshness answer and the interface-run status |
| `checkAppraisalAge` | Activity, the age check of this story | `rwb-valuation` | The appraisal date and the limit in force in; the age, the stale flag and the limit version out |
| `orderAppraisal` | Activity, the order of this story | `rwb-valuation` | The case, the asset and the appraisal being replaced in; the interface-run reference, the decision record and the step outcome out, with the record and the idempotency row in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1, and the two activities are this story's; the remaining activities of the route decision belong to the sibling stories. The activity names are a target design choice and are fixed by the baseline so that the workflow history is stable. `RouteDecisionWorkflow` is started by `CaseWorkflow` as a child, when the case reaches route decision D6 or the case is reopened (`ROUTE_D6_REOPEN`); its workflow ID form and its duplicate-start policy are Not specified in the source documents (CG-ALL-7929). The consumed rows (rwb-source-data appraisal and acceptance read, rwb-integration order and interface-run read, rwb-case state read, rwb-decision rule and decision-log read, rwb-access authorise) carry placeholder operation names until their owners publish them before the wave 3 tag; the clients are built against their documented use and a published name replaces the placeholder with no behaviour change (GAP-2587; GAP-2590).

#### 12.6 Schedules

None. The step runs inside the workflow from the route command and owns no Temporal Schedule and no legacy Quartz job, because the ownership rows give S1 no job. A batch-completion trigger is not built: no source names the event or the Schedule it would need (GAP-2593; ASM-4290).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table; the store of the stale flag, the age and the acceptance is not fixed (GAP-2591; ASM-4288) |
| decision_record | PLT library, created in `rwb_valuation` | The local hash-linked decision record, one per assessment (DP-03) |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

Not owned and never read as a table: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `proceeds` (P8), `template` (P6), `deviation` (S8), `document` and `document_custody` (P5), every `v_ace_*` view and `valuation_ext` (P1). No foreign key leaves `rwb_valuation`: the case, the asset, the appraisal and the rule are identifiers, not keys across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | Asset `AST-2026-000401` with an appraisal from `2025-10-02`, its value, type and acceptance; the same asset inside the limit; the same asset with the acceptance absent; a stale product with its date; no answer beyond 2 s | AC2, X5, X6, X7 |
| rwb-integration order-submission fake | The order accepted with its interface-run reference; a rejected order with its reason; no answer beyond 2 s | TC-E4-001-01, X4 |
| rwb-integration interface-run fake | The run delivered, and the run failed after the retry limit | TC-E4-001-01, X4 |
| rwb-case case-state fake | Case `RC-2026-000401` at the route decision with its asset link; a case in another state | X3 |
| rwb-decision rule and log fake | The limit and the rule id at their version in force for the business date; the record the ledger holds | TC-E4-001-01 |
| rwb-access authorise fake | Treatment and offer, right U accepted and refused | TC-E4-001-03, X2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000401`, with the appraisal, the order and the route elements read once | TC-E4-001-01 |

The fakes are test-only and are replaced by the real services in SIT. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2590; ASM-4287).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 6 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-source-data data product, the two rwb-integration rows, the rwb-case state, the rwb-decision row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `checkAppraisalAge` and `orderAppraisal` on `rwb-valuation`; no Schedule |
| File | None of this service | The SVAF order travels as an interface run of rwb-integration, and this service writes no file (GAP-2590) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.valuation`, module `appraisalorder`, Java package `th.co.scb.ace.workbench.recovery.valuation.appraisalorder`; front end `src/modules/recovery/valuation/RouteAppraisal.tsx`, the fragment SCR-13 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant and reads no ACE view and no ACE table, and the appraisal and the acceptance are the ones the rwb-source-data contract answers. DP-03 is the transaction rule of the step: the record, the idempotency row and the order answer commit together or not at all. DP-13 moves the base of the one operation. DP-19 is how SCR-13 reaches this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The six consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2590 (ASM-4287). The three H rows of the metadata are the contract of this key and the two platform contracts of DP-03 and DP-19, and no other H row is added.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RouteDecisionWorkflow` appraisal branch | Workflow | The first step of the route decision: waits for the command, runs the check, submits the order and reports the outcome to the parent |
| `checkAppraisalAge` | Activity | Reads the appraisal on the data product, computes the age, compares it with the limit in force and returns the stale flag and the limit version |
| `orderAppraisal` | Activity | Submits the order through rwb-integration, writes the decision record and the idempotency row, and returns the run reference and the outcome |
| `SourceDataProductClient` | Client | The appraisal, acceptance and collateral read of rwb-source-data, one hop, 2 s, breaker, with the stale path |
| `IntegrationOrderClient` | Client | The order submission and the interface-run read of rwb-integration, one hop, 2 s, breaker |
| `CaseStateClient` | Client | The case state and the asset link read of rwb-case, one hop, 2 s |
| `RuleInForceClient` | Client | The limit and the rule id at their version in force, from rwb-decision, one hop, 2 s |
| `AppraisalDecisionRecordWriter` | Library adapter | Writes one record per assessment before anything else changes, hash-linked, and refuses the step when the write fails (DP-03) |
| `RouteController` | Controller | The route operation, its capability area and right, the `Idempotency-Key`, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `RouteAppraisal` | React component | Shows the appraisal, its age, the order and its interface run, and the refused, held and stale states on SCR-13, read only |

**Database and migrations.** No Flyway file. `rwb_valuation` and its login arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in it by the library's migration (DP-03). No column is added for the stale flag or the age: they are computed per assessment and recorded, and the store is GAP-2591 until its owner names it.

**Configuration and reference data.**

- The age limit and the appraisal types of `LOV-APPRAISAL` at their version in force (TSD S1 T3.2), read as reference data or as a rule row and never as constants. Parameter name of the age limit: Not specified in the source documents (DOR-RWB-S1-E4001-APP-20; GAP-0429). Both are read under the reference-data contract of DP-06 and DP-07. The staleness parameter and the data product code it reads: Not specified in the source documents (GAP-0429); the harness pack is agreed at the wave 3 entry check.
- The route codes of `LOV-ROUTE` are the sibling stories' and are read here only as elements of the answer.
- The capability area Treatment and offer and its rights are access rows of rwb-access, read through the guard.
- The consumer of the library's topic `rwb.decision-record.v1` is the ledger's; this service only writes the record.
- No parameter is named in the sources for the limit or for the step, and no S1 rule package is in force (GAP-2592; ASM-4289).

**Build steps**

1. The appraisal branch of `RouteDecisionWorkflow` and its input record, registered on `rwb-valuation`, with the route command as its trigger.
2. `SourceDataProductClient` against its fake, with the 2 s budget, the breaker, the stale path and the no-answer path (X5, X8).
3. `RuleInForceClient` and `checkAppraisalAge`, with the inside-limit, over-limit and absent-acceptance paths (X6, X7).
4. `IntegrationOrderClient` and `orderAppraisal`, with the accepted order, the refused order and the failed run (X4).
5. `AppraisalDecisionRecordWriter` against the library stub, with the failed-write path (AC2, X1).
6. The idempotency row and the repeat of the same command (X9).
7. `CaseStateClient` and the state guard of the step (X3).
8. `RouteController` with the right, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (TC-E4-001-03).
9. `RouteAppraisal` and SCR-13 through the composite route fake (TC-E4-001-01).
10. The boundary test: no statement outside `rwb_valuation`, no `v_ace_*` read, no write to the schema of any other owner, and no outbox row (X10, BR8, BR9).

**Feature flag.** `rwb.valuation.appraisal-order-v1`, read as a flag of the platform library; off means the step records its outcome and raises no order, and the route decision continues on the appraisal in hand.

**Done when.** The tests of section 16 pass, a stale appraisal raises exactly one order in SIT with its interface run, an appraisal inside the limit raises none, a stale product writes nothing, a forced record failure changes nothing and shows MSG-P7-003, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-13 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of a request or of the appraisal row is absent or invalid (X6) | Enter {field}. |
| MSG-P4-002 | A role without the Treatment and offer right calls the route operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the step changes anything (X1, AC2) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product behind the appraisal is stale after a late or failed batch (X5) | {product} is from {date}. Today's load has not arrived. |

The four message IDs are the rows of FSD S1 A2.1.3.1, of the legacy message set of this key and of the platform set, and the text is the legacy wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

SCR-13 Route decision is served through the gateway-bff composite route (DP-19), and this story fixes the appraisal part of its answer and the states it can show.

| Screen | States | What this story sets |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted; empty, error and no access: Not specified in the source documents (CG-ALL-7936) | Loading while the age check runs; recommendation with the appraisal, its age and the order it raised; overridden with the owner's reason; submitted with the route answer. Plus refused with MSG-P4-002, not recorded with MSG-P7-003, stale data with MSG-P1-001, and held while an order waits on the valuer |

The screen's route elements, its merge order and its field list belong to RWB-PLT-N001-CON and the sibling route stories of this service; the appraisal element list and the four service states above are this story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-001-01 | The age check and the order: an appraisal over the limit raises one order through rwb-integration and records it; one inside the limit raises none; a stale product raises none; BR1, BR2, BR3, BR4, BR11, BR12 and BR14 | Component | Case `RC-2026-000401` with asset `AST-2026-000401`, an appraisal from `2025-10-02`, an inside-limit appraisal and a stale product |
| TC-E4-001-02 | AC2: the decision record cannot be written; BR5 and BR13 | Component | The decision-record stub stopped; nothing written, no order, and MSG-P7-003 shown |
| TC-E4-001-03 | Access: a role without the right | Component | A role without Treatment and offer U; 403 with MSG-P4-002 and no read |
| TC-E4-001-04 | Principle 5: a forced decision record write failure; BR5 | NFR | A forced failure at the moment of the order and the record; no order, no record and no event |
| TC-S1-E4001-APP-01 | The boundary: no `v_ace_*` read, no foreign schema write and no published event (BR1, BR8, BR9) | Component | The build scan of step 10, plus an outbox that must stay empty |
| TC-S1-E4001-APP-02 | Contract: the route operation, its events and its activities of §12 answer as the contract of RWB-S1-E4001-CON; no person data in any payload (BR10) | Contract | The route operation and the appraisal activities of §12 against the contract fake of RWB-S1-E4001-CON |
| TC-S1-E4001-APP-03 | Boundary of the §12.7 tables: `decision_record` and `idempotency_key` are the only tables written, and no other table of §12.7 is written or read (BR6, BR8) | Component | The build scan of the statements against the tables of §12.7, with the grant of `rwb_valuation` |
| TC-S1-E4001-APP-04 | AC3: a role without the Treatment and offer right is refused before any read or write | Component | A role without Treatment and offer U; 403 with MSG-P4-002 and no read or record |
| TC-S1-E4001-APP-05 | AC4: the case is not at the route decision, or the asset of the appraisal is not on the case | Component | Case `RC-2026-000401` not at the route decision, and an appraisal whose asset is not on the case; nothing ordered and the state reported to the parent |
| TC-S1-E4001-APP-06 | AC5: rwb-integration refuses the order, or the interface run fails after the retry limit | Component | The order-submission fake refusing and the interface-run fake failed; the case stays at the route decision and the exception queue holds the item |
| TC-S1-E4001-APP-07 | AC6: the ACE data product is stale after a late or failed batch | Component | The stale data product of TC-E4-001-01; nothing written and MSG-P1-001 shown with the data date |
| TC-S1-E4001-APP-08 | AC7: the appraisal has no acceptance in valuation_ext | Component | An appraisal with no acceptance; no order and MSG-GEN-001 naming the missing acceptance |
| TC-S1-E4001-APP-09 | AC8: the appraisal is inside the limit | Component | The inside-limit appraisal of TC-E4-001-01; nothing ordered and the outcome recorded with the limit version |
| TC-S1-E4001-APP-10 | AC9: rwb-source-data or rwb-case does not answer inside 2 s, or its breaker is open | Component | The no-answer and open-breaker fakes; nothing written and 503 with the platform envelope |
| TC-S1-E4001-APP-11 | AC10: the same assessment is submitted twice with the same Idempotency-Key (BR7, BR15) | Component | The same command twice; one record, one order and the stored answer returned |
| TC-S1-E4001-APP-12 | AC11: a statement reaches a v_ace_* view, a recovery_case row or another service's schema | Component | The build scan of step 10 with a forced statement; the grant refuses it, the build fails and nothing is released |
| TC-S1-E4001-APP-13 | AC12: BR1 to BR10 hold on the step and its record | Component | The build scan, the limit and rule fakes at their version in force, and the outbox that must stay empty |
| TC-S1-E4001-APP-14 | AC13: error answers 401 and 404 of the route operation, with 403 of AC3 | Component | No valid identity; an unknown case; 401 or 404 with the platform envelope and no read or write |
| TC-S1-E4001-APP-15 | AC14: activity retry and timeout | Component | The activity fake failing and timing out; retried on the workflow schedule, and the case stays at the route decision after the retry limit |
| TC-S1-E4001-APP-16 | AC15: a consumed call fails or does not answer | Component | The call fake failing and not answering; retried on the workflow schedule, and the case stays at the route decision after the retry limit |
| TC-S1-E4001-APP-17 | AC16: a status change the model does not allow is refused | Component | Not specified in the source documents (NEWAC-RWB-S1-E4001-APP-AC16) |

The four legacy case IDs are the legacy cases of RWB-E4-001 in their legacy order, with the Level column added. TC-E4-001-01 is Component because the step is tested on its fakes; the legacy `System` wording of the case is kept in the Test Cases workbook, where the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases. The `-ITG` copies belong to the wave 3 harness and are owned by RWB-ITG-E4001-ITG.

### 17. Guardrails

- No business value in code: the age limit, the appraisal types and the route codes stay reference data or a rule row read with their version, never a constant, a default or a branch of the build.
- No personal data in `rwb_valuation`, in the order input, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case stays with rwb-case and the order with rwb-integration: no `recovery_case`, `assignment`, `task` or `timer` row, no file and no direct external call is written here (BR3, BR6).
- The decision is recorded before the change and the command is idempotent; a build that writes a row or raises an order before its record fails the review (DP-03, BR5, BR7).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no event published by this step, no `v_ace_*` read.

### 18. Traceability

| Source | Reference | Feature | L3 process | Used in |
|---|---|---|---|---|
| Legacy story | RWB-E4-001, disposition Split (rework); AC2 owned word for word by this story; AC1 is owned by RWB-ITG-E4001-ITG | FEAT-VAL-01 | Not specified in the source documents (DOR-RWB-S1-E4001-APP-2) | 1, 7, 16 |
| Feature | FEAT-VAL-01 Order an appraisal when the last one is stale, module S1, epic E4, depends on FEAT-RDF-06 | FEAT-VAL-01 | Not specified in the source documents (DOR-RWB-S1-E4001-APP-2) | 1, 2, 3 |
| FSD S1 v3 | A1.4 preconditions; A2.1.2 steps and integration points; A2.1.3.1 VR-S1-001-1 and BR-S1-001; A2.1.3.3 roles; A2.1.4.3 exception flows; requirements REQ-S1-001 to REQ-S1-008; SCR-13 | FEAT-VAL-01 | Not specified in the source documents (DOR-RWB-S1-E4001-APP-2) | 2, 3, 4, 5, 8, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `valuation` and `score`; T3.2 `LOV-APPRAISAL` and `LOV-ROUTE`; T3.3 relationships; T4 no state machine; T5.2 and T5.3; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | FEAT-VAL-01 | Not specified in the source documents (DOR-RWB-S1-E4001-APP-2) | 3, 10, 11, 12, 13, 16 |
| Logical data model | DF-ACE-091 to DF-ACE-098, DF-ACE-187 to DF-ACE-195, DF-EXT-036 to DF-EXT-049, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-COL-018 to DF-COL-027 and DF-COL-043 to DF-COL-044 | FEAT-VAL-01 | Not specified in the source documents (DOR-RWB-S1-E4001-APP-2) | 11 |
| Routing logic | R-UNI-38, R-UNI-39 and R-UNI-40; the valuation states of R-DIL-07 to R-DIL-11; no S1 route rule is in force, because the S1 package is Phase 2 | FEAT-VAL-01 | Not specified in the source documents (DOR-RWB-S1-E4001-APP-2) | 4, 8, 9, 14 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5) | FEAT-VAL-01 | Not specified in the source documents (DOR-RWB-S1-E4001-APP-2) | 13 |
| Gaps and assumptions | GAP-2590 to -7; ASM-4287 to -8; the contract gaps GAP-2587 to -3 belong to RWB-S1-E4001-CON and are cited here where the surface is read | FEAT-VAL-01 | Not specified in the source documents (DOR-RWB-S1-E4001-APP-2) | 1, 3, 4, 11, 12, 13, 14, 16 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | FEAT-VAL-01 | Not specified in the source documents (DOR-RWB-S1-E4001-APP-2) | all |

### 19. Out of scope

- AC1 of the legacy key and the cross-service journey that evidences it: RWB-ITG-E4001-ITG.
- The published shape of the route operation, the six consumed rows, the decision-record element, the workflow elements, the error set and the fakes: RWB-S1-E4001-CON.
- The two valuation operations and the appraisal intake, the acceptance of the value and the outlier flag: RWB-S1-E4002-CON and the appraisal stories of this service.
- The SVAF interface itself, its identity, its transport, its order layout, its retry schedule and its exception queue: rwb-integration (P2) (GAP-2590).
- The ACE appraisal, collateral and acceptance facts and the freshness of the data product: rwb-source-data (P1). The store of the stale flag, the age and the acceptance: the data owner of this service (GAP-2591).
- The case of record, its route states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the package version, its approval and the central ledger: rwb-decision (P7). The limit's parameter and the S1 rule package: GAP-2592.
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, its merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The COLLINS return, the payoff and the settlement range, the route agent, the approvals and the route flow start: the sibling route stories of this service.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
