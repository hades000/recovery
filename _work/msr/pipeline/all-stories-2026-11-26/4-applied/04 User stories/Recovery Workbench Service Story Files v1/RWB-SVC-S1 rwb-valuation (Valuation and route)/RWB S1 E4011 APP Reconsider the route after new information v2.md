# RWB-S1-E4011-APP Reconsider the route after new information

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S1-K |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S1-E4011-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-011 split out for rwb-valuation. Both legacy criteria are copied word for word with their origin tags; the reconsider step becomes an activity of `RouteDecisionWorkflow` on task queue `rwb-valuation`, reads the three kinds of new information — the accepted appraisal value, the payments since the last decision and the deviations on the case — recomputes the segment and re-runs the hard gates on the rules in force, writes the reopen with its reason, its change reference and its rule version through the local decision-record library before the recoverable state is reported (DP-03), and answers on the route operation of base `/api/recovery/valuation/v1` (DP-13), reached by SCR-13 through the gateway-bff composite route (DP-19). The ACE payment and appraisal facts are read on the rwb-source-data data product and never on a `v_ace_*` view of this service (DP-05), and no event is published, because the ownership rows give S1 none. No S1 rule or parameter decides what reopens the route and no rule id is in force (GAP-2642; ASM-4350); the deviation read, the rule-in-force read and the product codes of the two data products are not published with an operation name (GAP-2643; ASM-4351); the value trigger is declared against FEAT-VAL-07 while the value is accepted in FEAT-VAL-04 (GAP-2644; ASM-4352); the retainment of the earlier decision and its versions is not fixed by a table (GAP-2645; ASM-4353); no published element carries the change that caused the reopen on the route operation (GAP-2646; ASM-4354); no source names the event or the timer that notifies a payment or a deviation change (GAP-2647; ASM-4355). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S1-E4011-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **to reopen the route decision when a value, a payment or a deviation changes the picture**, so that **the route is chosen on expected return with reasons**.

This is the application slice of legacy RWB-E4-011, on feature FEAT-VAL-11 of module S1. It owns:

- the two legacy criteria of the key, AC1 and AC2, copied verbatim with their origin tags, and the rules, messages, rights and screen states they depend on;
- the reconsider step as an activity of `RouteDecisionWorkflow` on `rwb-valuation`: the three kinds of new information, the check that the case may reopen, the recomputed segment and the hard gates re-run on the rules in force, and the reopen outcome the parent applies;
- the read of the accepted appraisal value, of the payments since the last decision and of the deviations on the case, one hop, 2 s each, read only, on the owners' contracts (DP-05);
- the decision record of the reopen, written through RWB-PLT-E1027-CON in the caller's transaction before the outcome is reported, carrying the reason, the change reference, the rule id and version in force and the reference of the earlier decision (DP-03);
- the submission on the route operation `POST /cases/{caseId}/route` of base `/api/recovery/valuation/v1`, its right, its `Idempotency-Key` and its answer, whose shape is baselined by RWB-S1-E4011-CON (DP-13);
- the SCR-13 Route decision states this step produces, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the operation, the consumed rows, the reopen element, the record element, the workflow elements, the rights, the error set and the fakes, which are RWB-S1-E4011-CON; the valuation order and acceptance (FEAT-VAL-01 to FEAT-VAL-04), the COLLINS expected return (FEAT-VAL-05), the payoff and range (FEAT-VAL-06) and the recommendation (FEAT-VAL-07), which are the sibling stories of this service that run again after the reopen; the ACE payment and appraisal facts and their freshness, which are rwb-source-data's (P1); the payment matching and posting, which are rwb-payment's (P8); the deviation, its owner and its clocks, which are rwb-deviation's (S8); the case of record and its route states, which are rwb-case's (P3); the rule rows, the segment dimensions, the gate thresholds and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; the approval inside and above the limit and the hold (FEAT-VAL-08 to FEAT-VAL-10); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

A route chosen once, on the facts of the day, goes wrong quietly: an appraisal is accepted at a new value, a part payment moves the exposure band, or a deviation pauses and then clears. FEAT-VAL-11 makes the route decision live while the facts move, so that the bank does not pursue a restructure or a sale priced on a picture that no longer exists. The measure is the module's: recommendations accepted, read monthly from the decision log and the Workbench records.

Under D-RCV-60 what changes is how the step learns and what it may assert.

- **the facts are other services', and they arrive by contract.** The accepted value and the payments are ACE's ingested facts read on the rwb-source-data data product, the deviation is rwb-deviation's record and the rule version is rwb-decision's row; this service reads none of their tables and holds no `v_ace_*` grant (DP-05).
- **the reopen is a decision, so it is recorded.** Legacy AC2 makes the step trustworthy: no record, no reopen, MSG-P7-003. Under DP-03 the record is local, hash-linked and written in the same transaction as the step, and R-UNI-39 says no action proceeds unlogged.
- **the rule version is the one in force on the business date.** R-UNI-38 keeps an open case on the version it was decided under, so the record names the version the reopen was taken under and the earlier decision keeps its own.
- **the segment and the gates are re-run, not re-invented.** R-UNI-02, R-UNI-22 and R-UNI-37 recompute the segment and re-run the gates; R-DEV-19 does the same when a deviation re-routes the case. The rule ids and the thresholds are rwb-decision data, never constants of this build.
- **nothing is published.** The ownership rows give S1 no event, so the step adds no name to `rwb.valuation.events.v1`; its outward facts are the route answer and the decision record, which the library sends to `rwb.decision-record.v1` (ASM-4353).

### 3. Preconditions

- RWB-S1-E4011-CON is published: the route operation, the consumed rows, the reopen element, the record element, the workflow elements, the rights, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-13 Route decision reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The rwb-source-data data products that carry the payments of `v_ace_payment` (DF-ACE-043 to DF-ACE-054) and the accepted appraisal of `v_ace_valuation` (DF-COL-021 to DF-COL-025) are published with their fakes. Their operation is `GET /data-products/{productCode}/records`, and the two product codes are Not specified in the source documents (GAP-2643; ASM-4351).
- The rwb-deviation deviation read of the case is published with its fake; its operation name is Not specified in the source documents (GAP-2643; ASM-4351), because the API Specification v4 publishes only `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}`, both writes.
- The rwb-decision recommendation read is published as `GET /cases/{caseId}/recommendation` on its base, carrying `recommended`, `reasons`, `expectedReturnByRoute`, `ruleVersion` and `agentVersion`; the rule-in-force, segment and gate read has no published name (GAP-2643; ASM-4351).
- The rwb-case case-state read `GET /cases/{caseId}` and the rwb-access authorise call `POST /authorise` are available for their fakes.
- The case is at a state that may reopen: the route decision of FEAT-VAL-07 is complete, or the case sits in a route whose facts have moved. The reopen states are rwb-case's and are read, never written here.
- No S1 rule is in force and no source names the rule, the parameter or the threshold that decides what reopens the route (GAP-2642; ASM-4350); the universal rows R-UNI-02, R-UNI-22, R-UNI-37 and R-DEV-19 give the outcome state and nothing else.
- The service runs as its own login on schema `rwb_valuation`, holds the library objects `decision_record`, `idempotency_key` and `outbox`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_payment`, `recovery.v_ace_valuation` or `rwb_decision` is refused by the database and fails the boundary test (DP-01, DP-05).
- Where the earlier route decision and its versions are retained is not fixed: the Ownership Map gives S1 no table, and TSD S1 T3.1 declares `valuation` as a new Workbench table with no route-decision object (GAP-2645; ASM-4353).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S1-E4011-CON when its tests pass.

### 4. Flow

1. New information has changed the picture: an appraisal has been accepted at a new value (FEAT-VAL-04), a payment has matched the case, or a deviation has been raised or cleared on it. The case owner opens SCR-13 and submits the reopen through `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the command starts `RouteDecisionWorkflow` on task queue `rwb-valuation` in namespace `rwb-recovery` (API-S1-001; DP-13).
2. The step checks that the case may reopen: it reads the case state and its route state from rwb-case, one hop, 2 s, and refuses a case that is closed, cancelled, merged or in a legal hold (R-UNI-20; GAP-2643).
3. It reads the new information of the three kinds: the accepted appraisal value with its appraisal type and date, and the payments since the last decision with their date, amount, capital, interest and channel, on the rwb-source-data data products; and the deviations of the case with their code, paused state, outcome and cleared-at time on the rwb-deviation read (DP-05; DF-COL-021 to DF-COL-025; DF-ACE-043 to DF-ACE-054; DF-CAS-036 to DF-CAS-045).
4. If a data product is stale after a late or failed ACE batch, the step holds, writes nothing, records no decision and shows MSG-P1-001 with the data date; it resumes on the next fresh answer (X5).
5. It reads from rwb-decision the rule id, the rule version, the segment dimensions and the gate thresholds in force for the business date, one hop, 2 s (R-UNI-38; GAP-2642).
6. It recomputes the segment and re-runs the hard gates on those rules: R-UNI-02 for a part payment that changes the exposure band, R-UNI-22 for a re-aged or reclassified account, R-UNI-37 for a corrected dimension, and R-DEV-19 for a deviation that re-routes the case. The step applies the rows in force and asserts none of its own (GAP-2642; ASM-4350).
7. Where the recompute finds no change to the picture, the step records nothing and answers that the reopen is not needed; the route decision and the case state stay as they were (X3).
8. Where the recompute finds a change, the step assembles one reopen: the case, the reason code, the change reference of each kind of new information, the segment before and after, the outcome state `ROUTE_D6_REOPEN`, the rule id and version in force and the reference of the earlier decision it supersedes.
9. Before that reopen is reported, `ReopenDecisionRecordWriter` writes one decision record through the local library with that content. A failed write stops the step with nothing changed and nothing reported (DP-03; AC2, R-UNI-39; X1).
10. The step answers the workflow with the reopen and its versions. The parent reports it to rwb-case, which applies the D6 state `ROUTE_D6_REOPEN` to the case of record, and the route decision runs again from the expected return (FEAT-VAL-05) and the recommendation (FEAT-VAL-07); the earlier record stays as the evidence of the decision it was taken on (R-UNI-38).
11. The route operation answers `Approval` with the case, the decision and the status elements of the baseline, and SCR-13 moves through its loading, recommendation, overridden and submitted states (API-S1-001).
12. A repeat of the same command with the same `Idempotency-Key` returns the stored answer, raises no second record and counts the idempotency hit (R-UNI-40; X8).
13. No event is published: the reopen leaves as the route answer, the recommend read and the decision record, which the library sends to `rwb.decision-record.v1` (ASM-4353).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing, the reopen is not reported and the route answer is refused | MSG-P7-003 | AC2, TC-E4-011-02, TC-E4-011-04 |
| X2 | The role does not hold the Treatment and offer right of the operation | 403 before any read or write, and no record is written | MSG-P4-002 | TC-E4-011-03 |
| X3 | The recompute finds no change to the picture | Nothing is recorded, the reopen is not needed and the case state stays | None | TC-E4-011-01 |
| X4 | The case is closed, cancelled, merged or in a legal hold | The step does not run, nothing is recorded and the state is reported to the parent | None | TC-E4-011-01 |
| X5 | The ACE data product behind the payments or the appraisal is stale | The step holds, writes nothing and shows the data date; it resumes on a fresh answer | MSG-P1-001 | TC-E4-011-01 |
| X6 | rwb-decision, rwb-deviation, rwb-case or rwb-source-data does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and the caller sees 503 with the platform envelope | None | TC-E4-011-01 |
| X7 | A required element of the request is absent or the reason code is not one of its list | 422 before the step runs, and no record | MSG-GEN-001 | TC-E4-011-01 |
| X8 | The same command is submitted twice with the same `Idempotency-Key` | One record, one answer; the stored answer is returned and the repeat is counted | None | TC-E4-011-01 |
| X9 | A component, a statement or a test reaches a `v_ace_*` view, `recovery_case`, a deviation row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | s17, BR8, BR9 |

X1 and X2 are the exception paths of the legacy key carried onto the split, X3 to X8 are the paths the target call types add, and X9 is the DP-05 and DP-01 boundary. No threshold, percentage or return is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S1-E4011-CON, the rwb-source-data, rwb-deviation, rwb-decision, rwb-case and rwb-access fakes and the decision-record stub, and needs no live neighbour |
| Negotiable | The activity names, the reason codes of the screen, the change reference and the shape of the reopen outcome are this story's choice; the operation, the rules, the messages and the rights are fixed |
| Valuable | A route priced on a picture that has moved is reopened with its reason and the version that decided it, so the route decision is live while the facts move |
| Estimable | One workflow step, two activities, four clients, one record write and one screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each path runs on synthetic payments, an accepted appraisal and a deviation through the contract fakes, plus the stopped record write, the stale product, the no-change answer and the duplicate command |

### 7. Acceptance criteria

```gherkin
Feature: Reconsider the route after new information

  Scenario: AC1 Reconsider the route after new information (legacy RWB-E4-011 AC1)
    Given the rwb-deviation contract mock returns the deviation that changed the picture
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then reopens the route decision when a value, a payment or a deviation changes the picture
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-011 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

Both criteria are the legacy AC1 and AC2 of the key, word for word, with their origin tags added and nothing else changed: the legacy wording of `the data and the rule version this feature needs are in place`, `the user acts on the screen`, `the action is taken` and `nothing changes` stands. The one line this story adds is the Given that names the mock, because the cross-service part of AC1 is the new information that reopens the route, and every value of the legacy steps is kept as written. Neither criterion carries a business value: the value, the payment and the deviation are facts of the case, the reason codes are data and the rule version is read and recorded, never asserted.

### 8. Business rules

| ID | Rule | Message |
|---|---|---|
| VR-S1-011-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S1-011 | No value a business person may change is written in code; it is read from reference data with its version | None |
| R-UNI-02 | A part payment that changes the exposure band: recompute the segment and re-run the owner ladder and the hard gates | None |
| R-UNI-22 | The account is re-aged or reclassified upstream: recompute the segment, re-run the gates, record the change | None |
| R-UNI-38 | A new rule version reaches its effective date: apply it to decisions taken from that date; open cases keep the version they were decided under | None |
| R-UNI-39 | The decision log entry cannot be written: block the action and raise an incident; no action proceeds unlogged | MSG-P7-003 |
| R-UNI-40 | The same event arrives twice with the same key: ignore the second, record the idempotency hit | None |
| R-DEV-19 | A deviation re-routes the case: recompute the segment and re-run the hard gates | None |

The two VR and BR rows are the rows of FSD S1 A2.11.3.1, copied character for character. The six universal and deviation rows are the rows of the Business Rules and Routing Logic v4 that this step depends on: R-UNI-02 is the payment trigger, R-UNI-22 and R-DEV-19 the re-age, correction and deviation triggers, R-UNI-38 is why the record carries the version in force on the business date, R-UNI-39 is AC2 and R-UNI-40 is the repeat of the command.

| ID | Rule | Source |
|---|---|---|
| BR1 | The accepted value and the payments are ACE's ingested facts, read only on the rwb-source-data data products; this service holds no `v_ace_*` grant, keeps no copy and reads no ACE row as a table | DP-05; Ownership Map rows of S1; FSD S1 A2.11.2 |
| BR2 | The deviation is rwb-deviation's record, read on its contract; no `deviation` row is read or written here | API Specification v5 `POST /cases/{caseId}/deviations` (S8); GAP-2643 |
| BR3 | What reopens the route, the segment dimensions and the gate thresholds are rows in force of rwb-decision read for the business date; no rule id, threshold or reason code is a constant of the build | FSD S1 A2.11.3.1 BR-S1-011; GAP-2642 |
| BR4 | The reopen is recorded before it is reported, with the reason, the change reference, the rule id and version in force and the earlier decision it supersedes; a failed write changes nothing | DP-03; R-UNI-39; legacy AC2 |
| BR5 | A case that is closed, cancelled, merged or in a legal hold is not reopened by this step; the state guard refuses it and records nothing | R-UNI-20; R-UNI-50 (out of scope) |
| BR6 | When the recompute finds no change, nothing is recorded and the case does not move; the step never reopens on a guess | Legacy RWB-E4-011 AC1; FSD S1 A2.11.4.1 |
| BR7 | The case is not this service's: no `recovery_case`, `assignment`, `task`, `timer` or `deviation` row is written here, and the case state is read and reported | Ownership Map (`recovery_case` owner P3) |
| BR8 | One record per case and reopen: a repeated command with the same `Idempotency-Key` raises no second record | API-S1-001; R-UNI-40 |
| BR9 | No foreign key leaves `rwb_valuation` and no statement reaches another schema: the case, the account, the payment, the appraisal and the deviation are identifiers of other owners' facts | DP-01; TSD S1 T3.3 |
| BR10 | No event is published: the ownership rows give S1 no event, and the step adds no name to `rwb.valuation.events.v1` | context pack S1 ownership rows; ASM-4353 |
| BR11 | No person name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log, a data-product call or a workflow input | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step reports the reopen and the parent applies the D6 state `ROUTE_D6_REOPEN` to the case of record (BR7). What this story owns is the state of the reconsider assessment.

| From (assessment) | Event | Condition | To |
|---|---|---|---|
| Not assessed | REOPEN_SUBMITTED | The case state allows a reopen and the reason is present | Checking, one row per kind of new information |
| Checking | FACTS_READ | The data products answer fresh and the deviation read answers | Recomputing |
| Checking | PRODUCT_STALE | X5 | Held, nothing written, and the check re-runs on a fresh answer |
| Checking | CASE_NOT_REOPENABLE | X4 | Closed, nothing written and the state reported |
| Recomputing | CHANGE_FOUND | The segment, a gate or a deviation outcome changes the picture | Recording |
| Recomputing | NO_CHANGE | The picture is unchanged | Closed, nothing recorded (X3) |
| Recording | RECORD_WRITTEN | The transaction commits with the reopen | Reopened, and the parent applies `ROUTE_D6_REOPEN` |
| Recording | RECORD_FAILED | X1 | Unchanged, nothing reported and no reopen (AC2) |
| Reopened | ROUTE_DECISION_RERUN | The route decision completes again (FEAT-VAL-05, FEAT-VAL-07) | Assessed, and the earlier record stays as its evidence |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The reopen command of a case at a route state | The workflow is started on `rwb-valuation` | Checking the case state |
| Checking the case state | The case state answers | The case may reopen | Reading the facts |
| Reading the facts | The facts and the rules answer | The rules in force are present | Recomputing |
| Recomputing | The record is written and the transaction commits | AC1 | Waiting for the next command |
| Any | The record write or the transaction fails | X1 | Waiting, nothing changed |

The case states `ROUTE_D6_REOPEN` and `BACK_TO_ROUTE_DECISION` are the D6 rows of the Business Rules and Routing Logic v4, entered by the universal rows R-UNI-02, R-UNI-22 and R-UNI-37 and by R-DEV-19; they are named here and written by rwb-case, not here. No S1 route rule is in force, because the S1 package is Phase 2 (GAP-2642; ASM-4350).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Treatment and offer U in the legacy permission table of the key: submit the reopen and read its record |
| RW-CASEOWN (CRU), RW-RESTRUCT (CRUA), RW-SPECIAL (CRU), RW-GUARANT (CRU) | TSD S1 T6.1 rows for the capability area, and the rows the legacy permission table gives right U |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Treatment and offer R: read only, in scope |
| RW-PRODHEAD, RW-CREDCOMM | Treatment and offer RA: the approval of a route, which is a sibling story's and not this step's |
| SY-CASEWF, SY-RULES, SY-AGENT | Treatment and offer R: the service identities read the step and are subject to the same checks |
| rwb-valuation service identity | Runs the step, reads the two data products, the deviation and the rule row, writes the decision record and answers the route operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S1 T6.1 and of the legacy permission table of this key, and nothing wider. FSD S1 A2.11.3.3 gives the case owner as the only primary role, and the step runs under the service identity with the officer acting on the screen.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 to DF-CAS-045 | `deviation` (S8) | id, case_id, deviation_code, raised_at, raised_by, paused_state, handler_user_id, contact_stop, cleared_at, outcome | Read only, on the rwb-deviation contract; never as a table |
| DF-ACE-043 to DF-ACE-054 | `v_ace_payment` (P1) | payment_code, account_key, payment_date, payment_amount, capital_amount, interest_amount, expense_amount, commission_amount, payment_channel, description, comments, data_as_of | Read only, on the rwb-source-data data product (DP-05) |
| DF-COL-021 to DF-COL-025 | `valuation` and `v_ace_valuation` (P1) | appraisal_no, appraisal_type, appraised_value, forced_sale_value, appraisal_date | Read only, on the rwb-source-data data product; the accepted value of FEAT-VAL-04 |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_valuation`) | rule id, rule version, inputs reference, outcome, decided at, the reason and the earlier decision reference | Write, one record per reopen, before the outcome is reported (DP-03) |
| DF-REF-001 to DF-REF-015 | `rule_row` (P7) | rule_id, rule_version, route_set, from_state, event_code | Not read as a table: the rule, its version and the segment and gate rows arrive on the rwb-decision row |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` (P3) | id, case_no, product_group, status, stage_code | Not read as a table: the case state arrives on the rwb-case row |

Field IDs are those of the Logical Data Model and Data Dictionary v9, of TSD S1 T3.1 and of the legacy Data table, with the owners changed by the target. The legacy Data table lists the first, second, fourth and fifth groups and not the appraisal value; the value is the one FEAT-VAL-04 accepts (GAP-2644; ASM-4352). **No new table, no new column and no migration**: the schema `rwb_valuation` and its login arrive with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in it by the library's migration (DP-03). Where the earlier decision and its versions are retained is not fixed (GAP-2645; ASM-4353).

**No personal data.** The rows this story reads and writes carry identifiers, codes, amounts, dates and versions. No name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log, a data-product call or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This story supplies the behaviour behind the one operation the legacy story names, and its shape is baselined by RWB-S1-E4011-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in, being `route`, `overrideReasonCode` and `note`; `Approval` out, being `id`, `caseId`, `decision`, `preparedBy`, `level`, `amount` and `status` (API-S1-001; API Specification v5) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat, and no second record is written |

The step adds no REST operation of its own: no source publishes an operation for the reopen, whose surface is the route operation above, the decision record and the recommendation read (GAP-2646; ASM-4354). The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library or a consumed row does not answer.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /data-products/{productCode}/records` | `/api/recovery/source-data/v1` | P1 rwb-source-data | The payments of `v_ace_payment` since the last decision and the accepted appraisal value with its type and date; one call per product, the two product codes are Not specified in the source documents (GAP-2643; ASM-4351); faked |
| The deviation read of a case (operation name Not specified in the source documents (GAP-2643; ASM-4351)) | `/api/recovery/deviation/v1` | S8 rwb-deviation | The deviations of the case, their code, paused state, outcome and cleared-at time; faked |
| `GET /cases/{caseId}/recommendation` | `/api/recovery/decision/v1` | P7 rwb-decision | The recommendation with `reasons`, `expectedReturnByRoute`, `ruleVersion` and `agentVersion`, as the ledger projects the earlier answer; read only; faked |
| The rule-in-force, segment and gate read (operation name Not specified in the source documents (GAP-2643; ASM-4351)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id, the rule version, the segment dimensions and the gate thresholds in force for the business date; faked |
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state and its route state, checked before the step runs; read only; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). These rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2643 with ASM-4351.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event, so this story adds no name, no outbox row and no payload to `rwb.valuation.events.v1`, and a build that publishes one here fails the absence test (BR10). The one publication of the step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1` in the transaction of the step.

#### 12.4 Events consumed

None. FSD S1 A2.11.4.4 declares "None, No background event", and the ownership rows give S1 no job and no event, so no subscription exists to notify a payment, an appraisal acceptance or a deviation, and the step is started by the reopen command inside `RouteDecisionWorkflow` (GAP-2647; ASM-4355). The freshness of the data products is read as an element of the rwb-source-data rows, and a duplicate of the command is caught by the idempotency row and not by a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` in namespace `rwb-recovery` | Input: the case, the route set and the rule package in force; signals: the freshness answer of each data product and the outcome of the reconsider step |
| `collectRouteChange` | Activity, the read and recompute of this story | `rwb-valuation` | The case, the reason and the business date in; the segment before and after, the gate results, the change reference of each kind and the freshness answer out |
| `reopenRouteDecision` | Activity, the record and outcome of this story | `rwb-valuation` | The reopen and its versions in; the decision record, the idempotency row and the step outcome out, in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1, and the two activities are this story's; the remaining activities of the route decision belong to the sibling stories. The activity names are a target design choice and are fixed by the baseline so that the workflow history is stable.

#### 12.6 Schedules

None. The step runs inside the workflow from the reopen command and owns no Temporal Schedule and no legacy Quartz job, because the ownership rows give S1 no job and the FSD declares no background event. A change-notification Schedule is not built: no source names the event or the Schedule it would need (GAP-2647; ASM-4355).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table; the retainment of the earlier route decision and its versions is not fixed (GAP-2645; ASM-4353) |
| decision_record | PLT library, created in `rwb_valuation` | The local hash-linked decision record, one per reopen (DP-03) |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

Not owned and never read as a table: `recovery_case`, `assignment`, `task` and `timer` (P3), `deviation` (S8), `decision_log_entry`, `rule_row` and `approval` (P7), `proceeds` (P8), `template` (P6), `document` and `document_custody` (P5), `valuation_ext` of the module's own DB story, and every `v_ace_*` view (P1), `v_ace_payment` and `v_ace_valuation` included. No foreign key leaves `rwb_valuation` (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data payment fake | Account `ACC-2026-001111` with one part payment that moves the exposure band, a payment inside the band, no payment since the decision, a stale product with its date and no answer beyond 2 s | AC1, X5, TC-E4-011-01 |
| rwb-source-data appraisal fake | The accepted appraisal of asset `AST-2026-001111` at its value, type and date; an appraisal not yet accepted; a stale product | AC1, X5, TC-E4-011-01 |
| rwb-deviation fake | Case `RC-2026-001111` with a deviation cleared after a pause, a deviation still open, and no deviation | AC1, X3, TC-E4-011-01 |
| rwb-decision rule-in-force fake | The rule id and version, the segment dimensions and the gate thresholds in force for the business date; a business date with no rule row | AC1, X4, TC-E4-011-01 |
| rwb-decision recommendation fake | The recommendation of the earlier decision with `expectedReturnByRoute`, `reasons`, `ruleVersion` and `agentVersion`; a case with no recommendation yet | AC1, TC-E4-011-01 |
| rwb-case case-state fake | Case `RC-2026-001111` at a route state that may reopen; a case closed, cancelled or in a legal hold | X4 |
| rwb-access authorise fake | Treatment and offer, right U accepted and refused | TC-E4-011-03, X2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-001111`, with the reopen elements read once | TC-E4-011-01 |

The fakes are test-only and are replaced by the real services in SIT. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2643; ASM-4351).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 6 consumed rows (7 calls) | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; two rwb-source-data data products, the rwb-deviation read, two rwb-decision rows, the rwb-case state and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `collectRouteChange` and `reopenRouteDecision` on `rwb-valuation`; no Schedule |
| File | None of this service | The payments and the appraisal arrive through ACE ingestion and the rwb-source-data contract; this service writes and reads no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.valuation`, module `reopenroute`, Java package `th.co.scb.ace.workbench.recovery.valuation.reopenroute`; front end `src/modules/recovery/valuation/RouteReopen.tsx`, the fragment SCR-13 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant and reads no ACE view and no ACE table, and the payment and the appraisal are the facts the rwb-source-data contracts carry. DP-03 is the transaction rule of the step: the record, the idempotency row and the step outcome commit together or not at all. DP-13 moves the base of the one operation. DP-19 is how SCR-13 reaches this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The six consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2643 (ASM-4351). The three H rows of the metadata are the contract of this key and the two platform contracts of DP-03 and DP-19, and no other H row is added.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RouteDecisionWorkflow` reopen branch | Workflow | Runs the reconsider step on the command and reports the reopen to the parent |
| `collectRouteChange` | Activity | Reads the case state, the three kinds of new information and the rules, recomputes the segment and the gates and returns the change or the no-change answer |
| `reopenRouteDecision` | Activity | Writes the decision record and the idempotency row with the reopen and returns the step outcome |
| `SourceDataFactsClient` | Client | The payment and appraisal reads of rwb-source-data, one hop, 2 s, breaker, with the stale and no-fact paths |
| `DeviationReadClient` | Client | The deviation read of rwb-deviation, one hop, 2 s |
| `DecisionReadClient` | Client | The recommendation read and the rule-in-force, segment and gate read of rwb-decision, one hop, 2 s |
| `CaseStateClient` | Client | The case state read of rwb-case, one hop, 2 s |
| `ReopenDecisionRecordWriter` | Library adapter | Writes one record per reopen before the outcome is reported, hash-linked, and refuses the step when the write fails (DP-03) |
| `RouteController` | Controller | The route operation, its capability area and right, the `Idempotency-Key`, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `RouteReopen` | React component | Shows the reopen reason, the new information, the recomputed segment and the versions, and the held, no-change and refused states on SCR-13, read only |

**Database and migrations.** No Flyway file. `rwb_valuation` and its login arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in it by the library's migration (DP-03). No column is added for the reopen: it lives in the decision record, and the retainment of the earlier decision is GAP-2645 until its owner names it.

**Configuration and reference data.**

- The reason codes of the reopen and the route codes of `LOV-ROUTE` at their version in force, read as a list and never enumerated in code.
- The rule id, the rule version, the segment dimensions and the gate thresholds are read from rwb-decision for the business date and are never constants of the build.
- The capability area Treatment and offer and its rights are access rows of rwb-access, read through the guard.
- The consumer of the library's topic `rwb.decision-record.v1` is the ledger's; this service only writes the record.
- No parameter is named in the sources for the step's timeout or for what counts as a change, and no S1 rule package is in force (GAP-2642; ASM-4350).

**Build steps**

1. The reopen branch of `RouteDecisionWorkflow` and its input record, registered on `rwb-valuation`, with the command as its trigger.
2. `CaseStateClient` and the state guard, with the closed, cancelled, merged and legal-hold refusals (X4), then `SourceDataFactsClient` and `DeviationReadClient` against their fakes with the 2 s budget, the breaker, the stale path and the no-fact path (X5, X6).
3. `DecisionReadClient` and `collectRouteChange`, with the recompute of the segment and the gates on the rows in force and the deviation-cleared, deviation-open, no-deviation and no-change paths (AC1, X3).
4. `ReopenDecisionRecordWriter` against the library stub, with the failed-write path (AC2, X1), then `reopenRouteDecision` with the idempotency row and the repeat of the same command (X8).
5. `RouteController` with the right, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (TC-E4-011-03).
6. `RouteReopen` and SCR-13 through the composite route fake (TC-E4-011-01).
7. The boundary test: no statement outside `rwb_valuation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision`, `rwb_deviation` or `rwb_source_data`, and no outbox row (X9, BR9, BR10).

**Feature flag.** `rwb.valuation.reopen-route-v1`, read as a flag of the platform library; off means the step records the command as not taken with its reason and the route decision is not reopened.

**Done when.** The tests of section 16 pass, a changed picture reopens with its reason and versions in SIT, an unchanged picture records nothing, a stale product writes nothing, a forced record failure changes nothing and shows MSG-P7-003, no `recovery_case` and no `deviation` row and no `v_ace_*` read exists in the build, and SCR-13 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of the request or of a consumed row is absent or invalid (X7) | Enter {field}. |
| MSG-P4-002 | A role without the Treatment and offer right calls the route operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the outcome is reported (X1, AC2) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product behind the payments or the appraisal is stale (X5) | {product} is from {date}. Today's ACE batch has not arrived. |

The four message IDs are the rows of FSD S1 A2.11.3.1, of the legacy message set of this key and of the platform set, and the text is the legacy wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

SCR-13 Route decision is served through the gateway-bff composite route (DP-19), and this story fixes the reopen part of its answer and the states it can show.

| Screen | States | What this story sets |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted | Loading while the case state and the new information are read; recommendation with the reason, the change that reopened the route, the segment before and after and the version in force; overridden with the owner's coded reason; submitted with the reopen answer. Plus refused with MSG-P4-002, not recorded with MSG-P7-003, stale data with MSG-P1-001, and the no-change answer |

The screen's route elements, its merge order and its field list belong to RWB-PLT-N001-CON and the sibling route stories of this service; the reopen element list and the states above are this story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-011-01 | AC1: the route decision is reopened when a value, a payment or a deviation changes the picture, and the result is recorded with its rule version; an unchanged picture records nothing; a stale product answers nothing | Component | Case `RC-2026-001111` with account `ACC-2026-001111` and asset `AST-2026-001111`, one part payment that moves the band, one accepted appraisal, one cleared deviation, no payment, a stale product |
| TC-E4-011-02 | AC2: the decision log cannot be written | Component | The decision-record stub stopped; nothing written, no reopen reported and MSG-P7-003 shown |
| TC-E4-011-03 | Access: a role without the right | Component | A role without Treatment and offer U; 403 with MSG-P4-002 and no read |
| TC-E4-011-04 | Principle 5: a forced decision log write failure | NFR | A forced failure at the moment of the reopen and the record; no record, no reopen and no event |
| TC-S1-E4011-APP-01 | The boundary: no `v_ace_*` read, no foreign schema write, no deviation row and no published event | Component | The build scan of step 10, plus an outbox that must stay empty |

The four legacy case IDs are the legacy cases of RWB-E4-011 in their legacy order, with the Level column added. TC-E4-011-01 is Component because the step is tested on its fakes; the legacy wording of the case is kept in the Test Cases workbook, where the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases. The `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the reason codes, the route codes of `LOV-ROUTE`, the segment dimensions, the gate thresholds and the rule version stay data or rows in force, never a constant, a default or a branch of the build.
- No personal data in `rwb_valuation`, in a data-product call, in a workflow input or in a log: identifiers, codes, amounts, dates and versions only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case stays with rwb-case, the deviation with rwb-deviation and the rules with rwb-decision: no `recovery_case`, `deviation`, `assignment`, `task` or `timer` row and no `rule_row` read is written here (BR2, BR7, BR9).
- The reopen is recorded before it is reported and the command is idempotent; a build that reports a reopen before its record fails the review (DP-03, BR4, BR8).
- No reopen on a guess: an unchanged picture records nothing, and no threshold or reason is synthesised (BR6).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no event published by this step, no `v_ace_*` read.

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-011, disposition Split (rework); AC1 and AC2 owned word for word by this story | 1, 7, 16 |
| Feature | FEAT-VAL-11 Reconsider the route after new information, module S1, epic E4, depends on FEAT-VAL-07 | 1, 2, 3 |
| FSD S1 v3 | A2.11.1 intent and metric; A2.11.2 steps, integration points and prerequisite; A2.11.3.1 VR-S1-011-1 and BR-S1-011; A2.11.3.3 roles; AC-S1-011-01; AC-EXC-S1-011-01 and -02; SCR-13 | 2, 3, 4, 5, 8, 14, 15 |
| TSD S1 v2 | T2 components; T3.1 `valuation` and `score`; T3.2 `LOV-ROUTE`; T3.3 relationships; T4 no state machine; T5.2 and T5.3; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 13, 16 |
| API specification v4 | `POST /cases/{caseId}/route` with `RouteRequest` and `Approval`; `GET /cases/{caseId}/recommendation` with `Recommendation`; `GET /data-products/{productCode}/records`; `POST /cases/{caseId}/deviations` (S8) | 11, 12.1, 12.2, 12.8 |
| Logical data model | DF-CAS-036 to DF-CAS-045, DF-ACE-043 to DF-ACE-054, DF-COL-021 to DF-COL-025, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-CAS-001 to DF-CAS-023 | 11 |
| Routing logic | R-UNI-02, R-UNI-22, R-UNI-38, R-UNI-39 and R-UNI-40, R-DEV-19; the D6 states `ROUTE_D6_REOPEN` and `BACK_TO_ROUTE_DECISION`; no S1 route rule is in force | 4, 8, 9, 14 |
| Epics 3 to 8 specification | E4 FEAT-VAL-11 row, depends on FEAT-VAL-07 | 1, 3 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2642 to -6; ASM-4350 to -6 | 1, 3, 4, 11, 12, 13, 16 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The published shape of the operation, the consumed rows, the reopen element, the record element, the workflow elements, the error set and the fakes: RWB-S1-E4011-CON.
- The valuation order and acceptance (FEAT-VAL-01 to FEAT-VAL-04), the COLLINS expected return (FEAT-VAL-05), the payoff and range (FEAT-VAL-06) and the recommendation (FEAT-VAL-07): the sibling route stories of this service, which run again after the reopen.
- The ACE payment and appraisal facts, the COLLINS and SVAF ingestion and the freshness of the two data products: rwb-source-data (P1). The payment matching and posting: rwb-payment (P8).
- The deviation, its code, its handler, its clocks and its outcome: rwb-deviation (S8) (GAP-2643). The retainment of the earlier route decision and its versions: the data owner of this service (GAP-2645).
- The case of record, its route states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the segment dimensions, the gate thresholds, the package version, its approval and the central ledger: rwb-decision (P7) (GAP-2642).
- The forced litigation review of R-UNI-31 and the reopen of a closed case under R-UNI-50, which are the litigation and case stories and need an approver.
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, its merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The approval inside and above the limit, the hold, and the route flow start and its timers (FEAT-VAL-08 to FEAT-VAL-10, FEAT-VAL-12): the sibling route stories of this service.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
