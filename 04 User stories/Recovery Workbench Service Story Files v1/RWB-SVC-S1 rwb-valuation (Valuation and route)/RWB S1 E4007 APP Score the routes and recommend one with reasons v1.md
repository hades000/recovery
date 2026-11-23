# RWB-S1-E4007-APP Score the routes and recommend one with reasons

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S1-G |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S1-E4007-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-007 split out for rwb-valuation. Both legacy criteria of the key are copied word for word with their origin tags; the scoring step becomes an activity of `RouteDecisionWorkflow` on task queue `rwb-valuation`, ranks the open routes on the COLLINS return read on the rwb-source-data data product (DP-05), calls the route agent of rwb-agent one hop, checks its answer against the allowed-action list with a confidence threshold and falls back to the rules in force, records the recommendation with its rule version through the local decision-record library before anything changes (DP-03) and answers the route operation on base `/api/recovery/valuation/v1` (DP-13), reached by SCR-13 through the gateway-bff composite route (DP-19). No event is published, because the ownership rows give S1 none. The operation names of the five consumed rows are not published (GAP-2621; ASM-4324); the recommendation element set, the reasons and the alternatives are not published and the route operation is already baselined by RWB-S1-E4001-CON (GAP-2622; ASM-4325); no S1 route-decision rule package, decision code, confidence threshold or open-route exclusion list is in force (GAP-2623; ASM-4326); FEAT-VAL-05 and FEAT-VAL-06 are prerequisites of the feature but their stories are not in the H row (GAP-2624; ASM-4327); the agent contract of DP-20 and its C row are not in this key's pattern set (GAP-2625; ASM-4328); the store of the recommendation is not fixed (GAP-2626; ASM-4329); no source names the event or timer behind the trigger (GAP-2627; ASM-4330); the mapping of route codes R1 to R8 onto the eight routes is not published (GAP-2628; ASM-4331). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **the Workbench to run the route agent, which recommends a route and states the reasons and the alternatives**, so that **the route is chosen on expected return with reasons**.

This is the application slice of legacy RWB-E4-007. It owns:

- the two legacy criteria AC1 and AC2 of the key, copied verbatim with their origin tags, and the rules, messages and screen they depend on;
- the assessment of the open routes of a case and the expected return of each, read from the COLLINS return on the rwb-source-data data product, one hop, 2 s, read only, with no `v_ace_*` grant of this service (DP-05);
- the call of the route agent of rwb-agent, through which the recommendation, its reasons and the alternatives are produced, with the output checked against the allowed-action list, a confidence threshold and a fallback to the rules in force;
- the ranking of the open routes, the named recommendation and the alternatives with their returns, as the recommendation outcome of the step;
- the decision record of the recommendation, written through RWB-PLT-E1027-CON in the caller's transaction before anything else changes, with the rule id and the version in force (DP-03);
- the recommendation elements of the route operation `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`, its right and its `Idempotency-Key`, whose shape is baselined by RWB-S1-E4007-CON and whose approval elements sit with RWB-S1-E4008-APP (DP-13);
- the states of SCR-13 Route decision that this step produces, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the operation, the five consumed rows, the recommendation element set, the workflow elements, the rights, the error set and the fakes, which are RWB-S1-E4007-CON; the COLLINS call and the return it records per route, which are RWB-S1-E4005-APP; the payoff and the settlement range, which are RWB-S1-E4006-APP; the approval of the recommendation inside or above the limit, which are RWB-S1-E4008-APP and RWB-S1-E4009-APP; the hold and the reconsideration of the route, which are RWB-S1-E4010-APP and RWB-S1-E4011-APP; the route flow and its timers, which are RWB-S1-E4012-APP; the agent runtime, its models, its autonomy level and its fallback engine, which are rwb-agent's (P10); the ACE score, collateral and account facts, which are rwb-source-data's (P1); the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case's (P3); the rule rows, the package version and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E4-007 exists because the route used to be chosen on officer judgment written up in an account plan. The FSD keeps the feature as FEAT-VAL-07 in module S1: the Workbench runs the route agent, which recommends a route and states the reasons and the alternatives, and the result is written to the decision log with the rule version. The feature sits on two siblings: FEAT-VAL-05 asks COLLINS for the expected return on each route and records the answer with its version, and FEAT-VAL-06 works out the payoff and the settlement range with the floor applied. This story turns those two figures into a ranked, explained recommendation, and the measure of the module is unchanged: recommendations accepted, read monthly from the decision log and the Workbench records.

Under D-RCV-60 four ownership facts change, and that is what this story carries.

- **the score is ACE's, not this service's.** `v_ace_score` is ACE's and only rwb-source-data reads the `recovery.v_ace_*` views, so the COLLINS return per route arrives on the owner's data product with its model code, its model version and its freshness stamp, and is never read as a table here (DP-05; Architecture v5 slide 8).
- **the agent is a service of its own.** The route agent is one of the twelve agents of the Agent Catalog, run by rwb-agent with its own models, its own autonomy level and its own fallback, so this service calls it one hop and never embeds a model or a prompt chain (GAP-2625).
- **the decision is recorded first.** Legacy AC2 is the rule that makes the step trustworthy: when the record cannot be written nothing changes and the user sees MSG-P7-003. Under DP-03 the record is local, hash-linked and written in the same transaction as the recommendation, and R-UNI-39 says no action proceeds unlogged.
- **the recommendation is advice and nothing more.** Sub-decision D6.3 is Advised at L1 and targets L2, and the agent "may decide nothing; a person approves the route" (Agent Catalog, Route agent). So the step recommends and the approval stays with RWB-S1-E4008-APP and RWB-S1-E4009-APP.

Nothing is published. The ownership rows give S1 no event, so the outward facts of the step are the route answer, the agent call and the decision record, which the library sends to `rwb.decision-record.v1` (ASM-4324). Every figure the recommendation uses is data in force: no return, weight, threshold or route code is a constant of the build.

### 3. Preconditions

- RWB-S1-E4007-CON is published: the route operation and its recommendation elements, the five consumed rows, the decision-record element, the workflow elements, the rights, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-13 Route decision reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The rwb-source-data data product that carries the COLLINS score of `v_ace_score`, the account and the collateral of the case is published with its fake and its freshness stamp; its operation name is Not specified in the source documents (GAP-2621; ASM-4324), and the row is not in this story's contract-dependency list, which is None.
- rwb-agent publishes the route-agent call and its answer; its operation name, its model codes and its autonomy level are Not specified in the source documents (GAP-2621; ASM-4324), and its client contract of DP-20 is not in this key's pattern set (GAP-2625; ASM-4328).
- The rwb-case case-state read and the rwb-decision rule-in-force read are available for their fakes; the rwb-case read is `GET /cases/{caseId}` on its published base, and the rwb-decision row carries the placeholder (GAP-2621; ASM-4324).
- The expected return of each route and the payoff and the settlement range are in hand on the same assessment, because FEAT-VAL-05 and FEAT-VAL-06 are the prerequisites of the feature; their stories are siblings and the plan's H row for this slice does not list them (GAP-2624; ASM-4327).
- The open route set, the ranking rule, the confidence threshold and the reasons are data in force with a version; no S1 route-decision rule package is in force and no source names the decision code of D6.3 as a rule row (GAP-2623; ASM-4326).
- The service runs as its own login on schema `rwb_valuation`, holds the library objects `decision_record` and `idempotency_key`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_score`, `recovery.account_ext` or `rwb_case` is refused by the database and fails the boundary test (DP-01, DP-05).
- Where the recommendation, its reasons and its alternatives are persisted is not fixed: the Ownership Map gives S1 no table, TSD S1 T3.1 declares `score` as REUSE ACE with DF-DEC-019 to DF-DEC-027 and the legacy Data table names `decision_log_entry` only (GAP-2626; ASM-4329).
- The mapping of the route codes of `LOV-ROUTE` (R1 to R8) onto the eight named routes is not published; only R1, R2 and R3 appear in the sources, as the start states of restructure, settlement and deed in lieu (GAP-2628; ASM-4331).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S1-E4007-CON when its tests pass.

### 4. Flow

1. The case is at the route decision and the case owner or the route flow submits the assessment through `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the command starts `RouteDecisionWorkflow` on task queue `rwb-valuation` in namespace `rwb-recovery` (API-S1-001; DP-13).
2. The step opens the open route set of the case: the routes the case may still take, less every route barred by a fact of the case. R-RES-32 is the published example, where a second break excludes R1 and the route decision runs again; the set itself is read as data with its version, never written in code (GAP-2623).
3. The step reads the COLLINS return of each open route on the rwb-source-data data product, one hop with a 2 s budget and a breaker: the score key, the account key, the model code, the model version, the score value, the estimate value, the route code and the scored date, with the freshness stamp (DF-ACE-270 to DF-ACE-279; DP-05; GAP-2621).
4. If the product is stale after a late or failed ACE batch, the step holds, writes nothing, records no decision and shows MSG-P1-001 with the data date; it resumes on the next fresh answer (VR-S1-007-1, X5).
5. The step reads the payoff and the settlement range of the same assessment, and the rule id and the version in force for the business date, as elements of its input and of the rwb-decision row; a route with no return in hand is listed as an alternative without a figure and is never ranked on an invented number (X6; GAP-2624).
6. The step assembles the agent request from identifiers, codes, amounts and dates only: the case reference, the open routes, the return of each, the range, the collateral and its accepted value, and the rule version in force. No name, address, contact value or identity number enters the request, and the request carries no secret (NFR-052, NFR-055).
7. The step calls the route agent of rwb-agent one hop with a 2 s budget and a breaker, under the service identity of this service, and asks for the recommended route, the reasons and the alternatives (Agent Catalog, Route agent; D6.3; GAP-2625).
8. The answer is checked against the allowed-action list: every element must be of a declared type, the recommended route must be a route of the open set and a code of `LOV-ROUTE`, and the answer must carry a confidence at or above the threshold in force. A schema failure, an out-of-set route or a confidence below the threshold puts the case on the rule fallback and then, where the rules give no answer, on the owner's queue with the reasons, and the fallback is recorded (NFR-055; X3).
9. The step ranks the open routes on the expected return with the fallback figures and fixes the recommendation: the named route, the expected return of each route, the reasons for the recommendation, the alternatives with their returns and the reference of the figure each one rests on, the model codes and versions of the return and of the agent, and the rule id and version in force (GAP-2622).
10. Before any of the above is committed, `RouteRecommendationWriter` writes one decision record through the local library: the case, the assessment, the recommendation, the alternatives, the reasons, the rule id and version, the model codes and versions, the confidence and the outcome. A failed write stops the step with nothing changed and nothing recommended (DP-03; AC2, R-UNI-39).
11. The step answers the workflow with the recommendation outcome; the route operation answers `Approval` with the recommendation elements of the baseline and the approval elements left to the approval stories, and a repeat of the same `Idempotency-Key` returns the stored answer and runs no second assessment (R-UNI-40; API-S1-001).
12. The decision record reaches `rwb.decision-record.v1` through the library of DP-03, keyed by the case, with no personal data on it; this service publishes no event of its own (ASM-4324).
13. SCR-13 Route decision shows the recommended route, the return of each route, the reasons, the alternatives and the confidence, in the recommendation state, read through the gateway-bff composite route, read only (DP-19).
14. A returned case re-opens the same step: R-UNI-37 recomputes the segment and re-runs the route decision, R-RES-32 re-runs it when R1 is barred, R-UNI-41 returns a manual decision to it, and R-UNI-45 re-runs it after a partner recall. The previous recommendation and its record stay as the evidence of why the earlier route was proposed.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing, no recommendation is returned and the route answer is refused | MSG-P7-003 | AC2, TC-E4-007-02, TC-E4-007-04 |
| X2 | The role does not hold the Treatment and offer right of the operation | 403 before any read, any agent call or any write, and no record is written | MSG-P4-002 | TC-E4-007-03 |
| X3 | The agent answer fails the allowed-action check, names a route outside the open set, or falls below the confidence threshold | The step applies the rules in force and records the fallback; where the rules give no answer the case goes to the owner's queue with the reasons | None (owner's queue) | TC-E4-007-01 |
| X4 | rwb-agent does not answer inside 2 s, or its breaker is open | The step applies the rules in force, records the fallback and never blocks the case on the agent | None | TC-E4-007-01 |
| X5 | The ACE data product is stale after a late or failed batch | The step holds, writes nothing and shows the data date; it resumes on a fresh answer | MSG-P1-001 | TC-E4-007-01 |
| X6 | A route of the open set has no COLLINS return, or the range is absent | The route is listed as an alternative without a figure, is never ranked on an invented number, and the gap is named in the reasons | MSG-GEN-001 | TC-E4-007-01 |
| X7 | The case is not at the route decision, or a route of the recommendation is barred on the case | The step does not recommend, nothing is written and the state is reported to the parent | None | TC-E4-007-01 |
| X8 | The same assessment is submitted twice with the same `Idempotency-Key` | One assessment, one agent call, one record, and the stored answer is returned; the repeat is counted | None | TC-E4-007-01 |
| X9 | rwb-source-data, rwb-agent, rwb-case or rwb-decision does not answer inside 2 s | The step waits and retries on the workflow's own schedule; nothing is written and the caller sees 503 with the platform envelope | None | TC-E4-007-01 |
| X10 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | s17, BR4, BR9 |

X1 and X2 are the exception paths of the legacy key carried onto the split, X3 and X4 are the agent paths the target adds, X5 to X9 are the paths of the consumed facts and of the command, and X10 is the DP-05 and DP-01 boundary. No threshold, weight or return is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S1-E4007-CON, the rwb-source-data, rwb-agent, rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P10, P3 or P7 |
| Negotiable | The activity names, the decision code and the shape of the step outcome are this story's choice; the operation, the rules, the messages, the screen and the recommendation elements are fixed |
| Valuable | The route is proposed with its expected return, the reasons and the alternatives it beat, so the owner approves a defensible route instead of writing one up |
| Estimable | One workflow step, two activities, five clients, one record write, one ranking pass and one screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each path runs on synthetic scores and returns through the contract fakes, plus the low-confidence answer, the out-of-set route, the stopped record write, the stale product and the duplicate command |

### 7. Acceptance criteria

```gherkin
Feature: Score the routes and recommend one with reasons

  Scenario: AC1 Score the routes and recommend one with reasons (legacy RWB-E4-007 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then runs the route agent, which recommends a route and states the reasons and the alternatives
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-007 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

Both criteria are the legacy AC1 and AC2 of the key, word for word, with their origin tags added and nothing else changed: the legacy wording of `its trigger arrives` and `the action is taken` stands. The `Given` of AC1 names no value and no service, so it is realised as it stands by the contract mocks of section 12.8 and is not rewritten: the data is the COLLINS return of each open route on the rwb-source-data row and the range of the payoff step, and the rule version is the rule id and version in force read from rwb-decision. Neither criterion carries a business value: the returns, the weights, the confidence threshold and the route codes are data in force.

### 8. Business rules

| ID | Rule | Message |
|---|---|---|
| VR-S1-007-1 | Data product stale after a late or failed ACE batch for its source (`v_ace_batch_status`) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| BR-S1-007 | No value a business person may change is written in code; it is read from reference data with its version | None |
| R-UNI-37 | A segment dimension changes after a correction upstream: recompute the segment and re-run the gates | None |
| R-UNI-38 | A new rule version reaches its effective date: apply it to decisions taken from that date; open cases keep the version they were decided under | None |
| R-UNI-39 | The decision log entry cannot be written: block the action and raise an incident; no action proceeds unlogged | MSG-P7-003 |
| R-UNI-40 | The same event arrives twice with the same key: ignore the second, record the idempotency hit | None |
| R-UNI-41 | A person decides and names the missing data: return the case to the route decision and log the rule gap | None |
| R-RES-32 | A second break bars a further restructure: exclude R1 from the open routes and re-run the route decision | None |

The two VR and BR rows are the rows of FSD S1 A2.7.3.1, copied character for character. The six universal and route rows are the rows of the Business Rules and Routing Logic v4 that this step depends on; R-UNI-38 is why the record carries the rule version in force on the business date, and R-RES-32 is the one published rule that changes the open route set of a case.

| ID | Rule | Source |
|---|---|---|
| BR1 | The score, the account and the collateral are ACE's and are read only on the rwb-source-data data product; this service holds no `v_ace_*` grant, keeps no copy and reads no score row as a table | DP-05; Ownership Map rows of S1; DF-ACE-270 to DF-ACE-279 |
| BR2 | The return of each route, the ranking rule, the confidence threshold, the open route set and the route codes are data in force read with their version; no return, weight, threshold or route code is a constant of the build | FSD S1 A2.7.3.1 BR-S1-007; TSD S1 T3.2; GAP-2623 |
| BR3 | The agent is called through rwb-agent's contract and decides nothing: the step recommends, the agent's answer is checked against the allowed-action list, and a person approves the route in the sibling approval stories | NFR-051, NFR-055; Agent Catalog, Route agent and D6.3; GAP-2625 |
| BR4 | The agent request and the record carry identifiers, codes, amounts, dates and versions only; no name, address, contact value, identity number or secret enters the request, the record, a log or a workflow input | Template and Rules v1 §R7.2 (s17); NFR-052; NFR-055 |
| BR5 | The recommendation is recorded before anything changes, with the rule id and the version in force, the recommended route, the returns, the reasons, the alternatives and the confidence; a failed write changes nothing and shows MSG-P7-003 | DP-03; R-UNI-39; legacy AC2 |
| BR6 | The case is not this service's: no `recovery_case`, `assignment`, `task` or `timer` row is written here, and the case state and the open route set are read and reported | Ownership Map (`recovery_case` owner P3) |
| BR7 | One assessment per case and command: a repeated command with the same `Idempotency-Key`, and a repeated fact with the same key, return the stored recommendation and run no second assessment | API-S1-001; R-UNI-40 |
| BR8 | A route is never recommended on an invented figure: a route with no return in hand is listed as an alternative without a figure and the gap is named in the reasons | Legacy AC1; FSD S1 A2.7.2 step 2 |
| BR9 | No foreign key leaves `rwb_valuation` and no statement reaches another schema: the case, the account, the score, the agent answer and the rule are identifiers of other owners' facts | DP-01; TSD S1 T3.3 |
| BR10 | No event is published: the ownership rows give S1 no event, and the step adds no name to `rwb.valuation.events.v1` | context pack S1 ownership rows; ASM-4324 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step reports its outcome and the parent `CaseWorkflow` applies it to the case of record (BR6). What this story owns is the state of the recommendation, and the case states a route decision reaches are the start states of the route sets, the only rows a source publishes.

| From (recommendation step) | Event | Condition | To |
|---|---|---|---|
| Not scored | ROUTE_ASSESSMENT_TRIGGERED | The case is at the route decision and the returns are fresh | Scoring |
| Scoring | The return of every open route is in hand | The range and the rule version are in hand | Recommending |
| Scoring | The product is stale, or a required figure is absent | X5, X6 | Held, nothing written |
| Recommending | The agent answer passes the allowed-action check at or above the threshold | The recommended route is in the open set | Recommendation recorded |
| Recommending | The agent answer fails the check, or the agent does not answer | X3, X4 | Rule fallback applied and recorded, then Recommendation recorded |
| Recommending | The rules give no answer after the fallback | X3 | The owner's queue with the reasons, and the step outcome reported |
| Recommendation recorded | The record cannot be written | X1 | Unchanged, nothing recommended and no answer (AC2) |
| Recommendation recorded | A later fact changes the picture | R-UNI-37, R-RES-32, R-UNI-41, R-UNI-45 | Not scored, and the step runs again with the earlier record kept |

| Case of record (rwb-case applies it) | Where the sources give the state |
|---|---|
| The approved route of R1 opens its route | ROUTE_APPROVED_RESTRUCTURE, "D6 sets route R1" |
| The approved route of R2 opens its route | ROUTE_APPROVED_SETTLEMENT, "D6 sets route R2" |
| The approved route of R3 opens its route | ROUTE_APPROVED_DIL, "D6 sets route R3" |
| The approved route of R4 opens its route | LIT_ROUTE_APPROVED, "D6.3, or a broken treatment returns the case" |
| The case returns for another assessment | BACK_TO_ROUTE_DECISION and ROUTE_D6_REOPEN, both end states of the routing logic |

The step recommends and does not move the case: the move belongs to the approval stories, and the states above are the ones the parent applies on an approved route. No S1 route rule is in force, because the S1 package is Phase 2 (GAP-2623; ASM-4326). The route codes R1, R2 and R3 are the three the sources name against a route; the rest of the mapping of `LOV-ROUTE` is open (GAP-2628; ASM-4331).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Treatment and offer U in the legacy permission table of the key: submit the assessment and read the recommendation, the returns, the reasons and the record |
| RW-CASEOWN (CRU), RW-RESTRUCT (CRUA), RW-SPECIAL (CRU), RW-GUARANT (CRU) | TSD S1 T6.1 rows for the capability area, and the rows the legacy permission table gives right U |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Treatment and offer R: read only, in scope |
| RW-PRODHEAD, RW-CREDCOMM | Treatment and offer RA: the approval of a route, which is a sibling story's and not this step's |
| SY-CASEWF, SY-RULES, SY-AGENT | Treatment and offer R: the service identities read the step and are subject to the same checks |
| rwb-valuation service identity | Runs the step, reads the data product, calls the route agent, writes the decision record and answers the route operation; it holds no grant on another schema and no `v_ace_*` grant |
| rwb-agent service identity | Answers the route-agent call only; it reads no row of this service and writes none (NFR-051) |

The rights above are the rows of TSD S1 T6.1 and of the legacy permission table of this key, and nothing wider. The step runs under the service identity with no officer task on the happy path, and the agent runs under its own identity subject to the same checks. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-ACE-270 to DF-ACE-279 | `v_ace_score` (P1) | score_key, account_key, model_code, model_version, score_value, estimate_value, route_code and the rest | Read only, on the rwb-source-data data product (DP-05) |
| DF-ACE-091 to DF-ACE-098 | `v_ace_collateral` (P1) | collateral_no, asset_key, collateral_type | Read only, on the data product, as the security behind the routes |
| DF-ACE-187 to DF-ACE-195 | `v_ace_valuation` (P1) | valuation_key, asset_key, appraised_value, appraisal_date | Read only, on the data product, as the accepted value the returns rest on |
| DF-DEC-019 to DF-DEC-027 | `score` per TSD S1 T3.1, REUSE ACE | id, account_id, case_id, model_code, model_version, score_value, estimate_value, route_code, scored_at | Read on the data product; not written here |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_valuation`) | rule id, rule version, inputs reference, outcome, decided at | Write, one record per assessment, before anything else changes |
| DF-REF-001 to DF-REF-015 | `rule_row` (P7) | rule_id, rule_version, route_set, from_state, event_code | Not read as a table: the rule and its version arrive on the rwb-decision row |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` (P3) | id, case_no, product_group, status, stage_code | Not read as a table: the case state arrives on the rwb-case row |
| The agent answer elements | rwb-agent (P10) | the recommended route code, the reasons, the alternatives, the figures they rest on, the model codes and versions, the confidence | Consumed, not stored |

Field IDs are those of the Logical Data Model and Data Dictionary v8, of TSD S1 T3.1 and of the legacy Data table, with the owners changed by the target. **No new table, no new column and no migration**: the schema `rwb_valuation` and its login arrive with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in it by the library's migration (DP-03). The recommendation, its reasons and its alternatives are recorded in the decision record; where the data owner names a column or a `score` table of this service, the DB story adds it and this story's writer fills it (GAP-2626; ASM-4329).

**No personal data.** The rows this story reads and writes carry identifiers, codes, amounts, dates, route codes and versions. No name, address, contact value or identity number enters `rwb_valuation`, the decision record, the agent request, a log or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This story supplies the behaviour behind the one operation the legacy story names, and its shape is baselined by RWB-S1-E4007-CON as an additive slice of the operation RWB-S1-E4001-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out, with the recommendation elements: the recommended route code, the expected return of each route, the reasons, the alternatives, the confidence, the rule version and the override reason where the answer departs from the recommendation (API-S1-001) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat, and no second assessment runs |

The step adds no REST operation: no source names a published operation for the scoring or the agent call, whose surfaces are the rwb-agent call and the decision record, and the contract slice fixes them (GAP-2622). The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library, the agent or a consumed row does not answer.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The COLLINS score data-product read (operation name Not specified in the source documents (GAP-2621; ASM-4324)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The score, its model code and version, the return per route, the account and the collateral links and the freshness stamp; faked |
| The route-agent call (operation name Not specified in the source documents (GAP-2621; ASM-4324)) | `/api/recovery/agent/v1` | P10 rwb-agent | The recommended route, the reasons, the alternatives and the confidence, with the model codes and versions; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, its product group and the open route set, checked before a recommendation is made; read only; faked |
| The rule-in-force and decision-log read (operation name Not specified in the source documents (GAP-2621; ASM-4324)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id and the version in force for the business date, the open route set where the rules hold it, and the record the ledger holds; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). These rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None and its pattern set does not include DP-20; the absence is recorded as GAP-2621 and GAP-2625 with ASM-4324 and ASM-4328. The return per route of FEAT-VAL-05 and the range of FEAT-VAL-06 arrive on the same assessment and are not re-read here.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event, so this story adds no name, no outbox row and no payload to `rwb.valuation.events.v1`, and a build that publishes one here fails the absence test (BR10). The one publication of the step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1` in the transaction of the step.

#### 12.4 Events consumed

None. FSD S1 A2.7.2 names three possible triggers, "a completed ACE batch, an event or a timer", and no source publishes an event name for any of them; the ownership rows give S1 no job and no event, so the step is started by the route command inside `RouteDecisionWorkflow` and subscribes to nothing (GAP-2627; ASM-4330). The freshness of the data product is read as an element of the rwb-source-data row, and a duplicate of the route command is caught by the idempotency row and not by a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` in namespace `rwb-recovery` | Input: the case, the open route set, the returns of the routes, the range and the rule package in force; signals: the freshness answer, the agent answer and the fallback outcome |
| `scoreRoutes` | Activity, the ranking of this story | `rwb-valuation` | The open route set, the return of each route and the range in; the ranked routes, the figures and the gaps out |
| `recommendRoute` | Activity, the recommendation of this story | `rwb-valuation` | The ranked routes, the agent request and the rule version in; the recommendation, the reasons, the alternatives, the confidence, the decision record and the step outcome out, with the record and the idempotency row in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1, and the two activities are this story's; the remaining activities of the route decision belong to the sibling stories. The activity names are a target design choice and are fixed by the baseline so that the workflow history is stable.

#### 12.6 Schedules

None. The step runs inside the workflow from the route command and owns no Temporal Schedule and no legacy Quartz job, because the ownership rows give S1 no job. A batch-completion trigger is not built: no source names the event or the Schedule it would need (GAP-2627; ASM-4330).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table; the store of the recommendation, its reasons and its alternatives is not fixed (GAP-2626; ASM-4329) |
| decision_record | PLT library, created in `rwb_valuation` | The local hash-linked decision record, one per assessment (DP-03) |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

Not owned and never read as a table: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `score` as an ACE object, `v_ace_score`, `v_ace_collateral` and `v_ace_valuation` (P1), `deviation` (S8), `proceeds` (P8). No foreign key leaves `rwb_valuation`: the case, the account, the score, the agent answer and the rule are identifiers, not keys across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | Case `RC-2026-000407` with three open routes, the return of each from model `CRR_RET_380` and its version, the accepted value and the freshness stamp; the same case with one route without a return; a stale product with its date; no answer beyond 2 s | AC1, X5, X6 |
| rwb-agent route-agent fake | The recommended route R2 with its reasons, the alternatives with their returns, the model codes and versions and a confidence above the threshold; an answer below the threshold; an answer naming a route outside the open set; an answer that fails the schema check; no answer beyond 2 s | AC1, X3, X4 |
| rwb-case case-state fake | Case `RC-2026-000407` at the route decision with its product group and open route set; a case in another state; a case with R1 barred | X7, TC-E4-007-01 |
| rwb-decision rule and log fake | The rule id and the version in force for the business date; the fallback answer of the rules; the record the ledger holds | AC1, X3 |
| rwb-access authorise fake | Treatment and offer, right U accepted and refused | TC-E4-007-03, X2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000407`, with the recommendation, the returns, the reasons and the confidence read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2621; ASM-4324). No fake returns a real customer fact: every identifier and every amount is synthetic.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-source-data data product, the rwb-agent route-agent call, the rwb-case state, the rwb-decision row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `scoreRoutes` and `recommendRoute` on `rwb-valuation`; no Schedule |
| File | None of this service | No file leaves or enters this step; the scores arrive on the rwb-source-data data product and the agent answer on the rwb-agent call (GAP-2621) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.valuation`, module `routescore`, Java package `th.co.scb.ace.workbench.recovery.valuation.routescore`; front end `src/modules/recovery/valuation/RouteRecommendation.tsx`, the fragment SCR-13 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant and reads no ACE view and no ACE table, and the score, the account and the collateral are the ones the rwb-source-data contract answers. DP-03 is the transaction rule of the step: the record, the idempotency row and the recommendation answer commit together or not at all. DP-13 moves the base of the one operation. DP-19 is how SCR-13 reaches this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The five consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2621 and GAP-2625 (ASM-4324, ASM-4328). DP-20 names the agent client contract `RWB-P10-TE013-CON`; it is not in this key's pattern set and is not added to the metadata, so the row is carried as an assumption and the client is built against the agent's fake. The two prerequisite features of the key, FEAT-VAL-05 and FEAT-VAL-06, are siblings whose outputs arrive on the same assessment (GAP-2624; ASM-4327). The three H rows of the metadata are the contract of this key and the two platform contracts of DP-03 and DP-19, and no other H row is added.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RouteDecisionWorkflow` recommendation branch | Workflow | Waits for the assessment command, opens the route set, runs the ranking, obtains the recommendation and reports the outcome to the parent |
| `scoreRoutes` | Activity | Reads the return of each open route, applies the range and the rules in force, and returns the ranked routes and the gaps |
| `recommendRoute` | Activity | Assembles the agent request, calls the agent, checks the answer, applies the fallback, writes the decision record and the idempotency row, and returns the recommendation |
| `SourceDataProductClient` | Client | The score, account and collateral read of rwb-source-data, one hop, 2 s, breaker, with the stale path |
| `RouteAgentClient` | Client | The route-agent call of rwb-agent, one hop, 2 s, breaker, under the service identity, with the schema check of the answer |
| `CaseStateClient` | Client | The case state, the product group and the open route set read of rwb-case, one hop, 2 s |
| `RuleInForceClient` | Client | The rule id and the version in force, and the fallback answer, from rwb-decision, one hop, 2 s |
| `RouteRecommendationWriter` | Library adapter | Writes one record per assessment before anything else changes, hash-linked, and refuses the step when the write fails (DP-03) |
| `RouteController` | Controller | The route operation, its capability area and right, the `Idempotency-Key`, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `RouteRecommendation` | React component | Shows the recommended route, the return of each route, the reasons, the alternatives and the confidence on SCR-13, read only |

**Database and migrations.** No Flyway file. `rwb_valuation` and its login arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in it by the library's migration (DP-03). No column is added for the recommendation: it is recorded in the decision record, and the store is GAP-2626 until its owner names it.

**Configuration and reference data.**

- The route codes of `LOV-ROUTE` (TSD S1 T3.2) and the open route set, read as data with their version and never as constants.
- The ranking rule, the confidence threshold and the allowed-action list of the agent answer, read as platform or reference data with their version.
- The model codes and versions of the COLLINS return arrive on the data product; no model code is written in code.
- The capability area Treatment and offer and its rights are access rows of rwb-access, read through the guard.
- The consumer of the library's topic `rwb.decision-record.v1` is the ledger's; this service only writes the record.
- No parameter is named in the sources for the threshold, the weights or the open route set, and no S1 rule package is in force (GAP-2623; ASM-4326).

**Build steps**

1. The recommendation branch of `RouteDecisionWorkflow` and its input record, registered on `rwb-valuation`, with the assessment command as its trigger.
2. `SourceDataProductClient` against its fake, with the 2 s budget, the breaker, the stale path and the no-answer path (X5, X9).
3. `CaseStateClient` and the open route set, with the barred-route and wrong-state paths (X7).
4. `scoreRoutes` with the ranking, the missing-return path and the range (X6).
5. `RouteAgentClient` against its fake, with the schema check, the confidence threshold, the out-of-set route and the no-answer path (X3, X4).
6. `RuleInForceClient` and the fallback, with the rules-give-no-answer path (X3).
7. `RouteRecommendationWriter` against the library stub, with the failed-write path (AC2, X1).
8. The idempotency row and the repeat of the same command (X8).
9. `RouteController` with the right, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (TC-E4-007-03).
10. `RouteRecommendation` and SCR-13 through the composite route fake (TC-E4-007-01).
11. The boundary test: no statement outside `rwb_valuation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or `rwb_agent`, and no outbox row (X10, BR9, BR10).

**Feature flag.** `rwb.valuation.route-recommendation-v1`, read as a flag of the platform library; off means the step applies the rules in force only, records the fallback as its outcome and calls no agent.

**Done when.** The tests of section 16 pass, a case with three open routes gets one recommendation with its reasons and alternatives and one record in SIT, a low-confidence or out-of-set agent answer falls back to the rules and is recorded, a forced record failure changes nothing and shows MSG-P7-003, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-13 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of a request, of a return or of the agent answer is absent or invalid (X6) | Enter {field}. |
| MSG-P4-002 | A role without the Treatment and offer right calls the route operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the step changes anything (X1, AC2) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product behind the score is stale after a late or failed batch (X5) | {product} is from {date}. Today's ACE batch has not arrived. |

The four message IDs are the rows of FSD S1 A2.7.3.1, of the legacy message set of this key and of the platform set, and the text is the legacy wording, copied unchanged; no message is reworded and no new one is added. The low-confidence and no-answer paths of the agent carry no message: they are recorded as a fallback and, where the rules give no answer, raised on the owner's queue with the reasons (X3, X4).

### 15. Screens and states

SCR-13 Route decision is served through the gateway-bff composite route (DP-19), and this story fixes the recommendation part of its answer and the states it can show.

| Screen | States | What this story sets |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted | Loading while the routes are scored; recommendation with the recommended route, the return of each route, the reasons, the alternatives and the confidence; overridden with the owner's reason, which is the approval story's act; submitted with the route answer. Plus refused with MSG-P4-002, not recorded with MSG-P7-003, stale data with MSG-P1-001, held while a route has no return, and the fallback state where the rules answered instead of the agent |

The screen's route elements, its merge order and its field list belong to RWB-PLT-N001-CON and the sibling route stories of this service; the recommendation element list and the states above are this story's. The screen displays the recommendation and offers no approval here: the approve action is RWB-S1-E4008-APP's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-007-01 | AC1: three open routes are scored and one is recommended with its reasons and alternatives, and the result is recorded with the rule version | Component | Case `RC-2026-000407` with three open routes, the return of each from `CRR_RET_380`, the range, and an agent answer above the threshold |
| TC-E4-007-02 | AC2: the decision log cannot be written | Component | The decision-record stub stopped; nothing written, no recommendation returned, and MSG-P7-003 shown |
| TC-E4-007-03 | Access: a role without the right | Component | A role without Treatment and offer U; 403 with MSG-P4-002 and no read and no agent call |
| TC-E4-007-04 | Principle 5: a forced decision log write failure | NFR | A forced failure at the moment of the recommendation and the record; no record, no answer and no event |
| TC-S1-E4007-APP-01 | X3, X4: a low-confidence answer, an out-of-set route, a schema failure and an agent that does not answer all fall back to the rules and record the fallback | Component | Four agent fakes, the fallback answer of the rules and a rules-gives-no-answer case |
| TC-S1-E4007-APP-02 | X5, X6, X8: the stale product, a route without a return and the duplicate command | Component | A stale product with its date, one route without a return, and the same `Idempotency-Key` twice |
| TC-S1-E4007-APP-03 | The boundary: no `v_ace_*` read, no foreign schema write and no published event | Component | The build scan of step 11, plus an outbox that must stay empty |

The four legacy case IDs are the legacy cases of RWB-E4-007 in their legacy order, with the Level column added. TC-E4-007-01 is Component because the step is tested on its fakes; the legacy `System` wording of the case is kept in the Test Cases workbook, where the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases. The three `TC-S1-E4007-APP-` cases are new and cover the agent, the data and the boundary paths no legacy case touches. The `-ITG` copies, where a wave 3 harness takes them, are outside this story.

### 17. Guardrails

- No business value in code: the route codes, the open route set, the ranking rule, the confidence threshold and the weights stay reference data or a rule row read with their version, never a constant, a default or a branch of the build.
- No personal data in `rwb_valuation`, in the agent request, in a workflow input or in a log: identifiers, codes, amounts, dates and versions only, no secret in a prompt, and every fixture is synthetic (NFR-052).
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case stays with rwb-case and the model with rwb-agent: no `recovery_case`, `assignment`, `task` or `timer` row, no model artefact and no prompt chain is written or embedded here (BR3, BR6).
- The recommendation is advice: a build that approves a route inside this step fails the review, because the approval and its delegation of authority belong to RWB-S1-E4008-APP and RWB-S1-E4009-APP.
- The decision is recorded before the change and the command is idempotent; a build that returns a recommendation before its record fails the review (DP-03, BR5, BR7).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no event published by this step, no `v_ace_*` read, no data-lake export.

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-007, disposition Split (rework); AC1 and AC2 owned word for word by this story | 1, 7, 16 |
| Feature | FEAT-VAL-07 Score the routes and recommend one with reasons, module S1, epic E4, depends on FEAT-VAL-05 and FEAT-VAL-06 | 1, 2, 3 |
| FSD S1 v3 | A1.4 preconditions; A2.7.2 steps and integration points (Workbench, Model gateway); A2.7.3.1 VR-S1-007-1 and BR-S1-007; A2.7.3.3 roles; A2.7.4.1 and A2.7.4.3 criteria; SCR-13 | 2, 3, 4, 5, 8, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `score`; T3.2 `LOV-ROUTE`; T4 no state machine; T5.2 and T5.3; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 13, 16 |
| Epics 3 to 8 Specification v3 | E4 row FEAT-VAL-07: system, runs unattended, Workbench and Model gateway, prerequisites FEAT-VAL-05 and FEAT-VAL-06 | 2, 3, 4 |
| Agent Catalog v2 | Route agent; sub-decision D6.3 Advised, L1 at go-live, L2 target, route return and C-score models; a person approves the route | 2, 4, 8, 12.2, 13 |
| Logical data model | DF-ACE-270 to DF-ACE-279, DF-ACE-091 to DF-ACE-098, DF-ACE-187 to DF-ACE-195, DF-DEC-019 to DF-DEC-027, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-CAS-001 to DF-CAS-023 | 11 |
| Routing logic | R-UNI-37 to R-UNI-41; R-RES-32; the start states ROUTE_APPROVED_RESTRUCTURE, ROUTE_APPROVED_SETTLEMENT, ROUTE_APPROVED_DIL and LIT_ROUTE_APPROVED; BACK_TO_ROUTE_DECISION and ROUTE_D6_REOPEN | 4, 8, 9 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5); DP-20 noted and not applied (GAP-2625) | 13 |
| Gaps and assumptions | GAP-2621 to -8; ASM-4324 to -8 | 1, 3, 4, 11, 12, 13, 14, 16 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The published shape of the operation, the five consumed rows, the recommendation element set, the workflow elements, the rights, the error set and the fakes: RWB-S1-E4007-CON.
- The COLLINS call and the return it records per route: RWB-S1-E4005-APP and RWB-S1-E4005-CON.
- The payoff and the settlement range with the floor applied: RWB-S1-E4006-APP and RWB-S1-E4006-CON.
- The approval inside the limit and above the limit at committee, the delegation of authority and the committee view: RWB-S1-E4008-APP, RWB-S1-E4009-APP and rwb-decision (P7).
- The hold, the review date, the reconsideration and the route flow with its timers: RWB-S1-E4010-APP, RWB-S1-E4011-APP and RWB-S1-E4012-APP.
- The agent runtime, its models, its prompts, its autonomy level, its confidence floor and its own fallback engine: rwb-agent (P10) (GAP-2625).
- The ACE score, collateral and account facts and the freshness of the data product: rwb-source-data (P1). The store of the recommendation, its reasons and its alternatives: the data owner of this service (GAP-2626).
- The case of record, its route states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the package version, its approval and the central ledger: rwb-decision (P7). The route-decision rule package, its decision code and the confidence threshold as data: GAP-2623.
- The mapping of the route codes R1 to R8 onto the eight named routes: GAP-2628.
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, its merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
