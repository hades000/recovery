# RWB-S8-E1021-APP Transfer rules and engine v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E1021-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-S8-B |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1021-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to REQ-CWC-010, REQ-CWC-016, REQ-WKM-003, REQ-CWC-005) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the deviation-triggered half of RWB-E1-021 is realigned onto rwb-deviation (S8). The engine moves into the service that raises the trigger: the `TransferTrigger` fact is built from `DeviationRaised` and `DeviationCleared` in `DeviationWorkflow` on task queue `rwb-deviation`, the TRANSFER package is evaluated by the service's embedded Drools kit with first match in row order (DP-04), the decision record is written before the move through the local library (DP-03), and the queue, team and owner move is requested from rwb-case on its published contract (DP-11; C RWB-P3-E1021-CON) because `recovery_case`, `queue` and `assignment` are P3's tables and the Ownership Map gives S8 only `deviation` (DP-01). The manual transfer endpoint, the legal-hold endpoint and the assignment swap stay with the primary slice of this legacy key in rwb-case. The two Operations of this service move onto `/api/recovery/deviation/v1` (DP-13), the read-only case screens are reached through the gateway-bff composite route (DP-19), and the events leave on `rwb.deviation.events.v1` (DP-09, DP-14). The plan's build list is empty although the DP table adds platform contract rows, and the business epic keeps wave 1 over the service wave 2 (GAP-3074; GAP-3075; ASM-5235; ASM-5236). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S8-E1021-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **the TRANSFER rule package evaluated inside rwb-deviation when a deviation is raised or cleared, so that the case moves to the queue and the owner the rule names, with the rule ID and the package version recorded before the move**.

This story owns:

- the `TransferTrigger` fact of the legacy story (event code, case number, stage, route, deviation state, legal hold) built from `DeviationRaised` and `DeviationCleared` and from the case trigger events this service subscribes to;
- the TRANSFER package evaluated by the service's **embedded Drools kit**, first match in row order, with the version in force read from rwb-decision (DP-04); a package with no version in force throws `NoPackageInForce` and moves no case;
- the legal-hold and idempotency checks that stand in front of the move (R-UNI-20, R-UNI-40);
- the transfer request to rwb-case that ends the open assignment, writes the new one with reason TRANSFER and the rule ID, and updates queue, team and owner (DP-11; C RWB-P3-E1021-CON);
- the decision record of every rule transfer and of every refused transfer, written in the caller's transaction **before** the case changes (DP-03);
- the `deviation` columns this move touches, `handler_user_id` and `state`, in `rwb_deviation` (DP-01);
- the outbox relay of `DeviationRaised` and `DeviationCleared` on `rwb.deviation.events.v1` (DP-09, DP-14);
- the transfer reason list read on the reference-data contract of rwb-case (DP-07) and the case facts read on the rwb-source-data contract (DP-05);
- the two operations of this service on `/api/recovery/deviation/v1` as the raise and clear paths that fire the trigger (DP-13), and the read-only SCR-02 and SCR-03 slices behind the gateway-bff composite route (DP-19);
- the per-service Flyway sequence of `rwb_deviation` for the story's own schema need, with no shared `recovery` migration (DP-15).

It does not own: the manual transfer endpoint and its `MANUAL` reason path, the legal-hold place and lift, the assignment swap itself and the `CaseTransferred` publication (the primary slice of RWB-E1-021 in rwb-case, P3); the `recovery_case`, `queue`, `assignment`, `timer` and `decision_log_entry` tables (P3 and P7); the TRANSFER package rows, their authoring, their approval and their version (rwb-decision, P7); the roles, the capability rights and the authorise operation (rwb-access, P4); and the contract surface with its fakes and its error envelope (RWB-P3-E1021-CON and the CON story of this service).

### 2. Business rationale

The legacy objective stands unchanged: a case changes hands without email, is held by one owner, and the rule that moved it is recorded with its version (RWB-E1-021 §2; REQ-CWC-010, REQ-CWC-016, REQ-WKM-003, REQ-CWC-005).

D-RCV-60 changes where the engine sits, not what the team manager gets:

- **The trigger is raised here, so the first evaluation runs here.** `DeviationRaised` and `DeviationCleared` are this service's own events (EV-06, EV-07 in the Ownership Map), and the deviation is flagged, routed and cleared in `DeviationWorkflow` on queue `rwb-deviation` (context pack; TSD S8 T4). Evaluating the TRANSFER rows for those two triggers in the service that owns the deviation removes a hop and the outbox wait that the monolith needed.
- **The case stays with rwb-case.** The S8 row of the connection matrix names REST and events to P3 and no shape beyond it; `recovery_case`, `queue` and `assignment` are P3's, and the plan gives this slice one class C dependency, `RWB-P3-E1021-CON`, which publishes the transfer request this story builds against (DP-11).
- **The rules are rwb-decision's.** The rule package registry is P7's by the default ruling and the package registry row is P7's in the Ownership Map; this service carries the **embedded** Drools kit and never owns a rule row (DP-04; ADR-017).
- **The decision is recorded first.** That is the monolith's own rule (BR9 of the legacy story, TSD S8 T2) and it survives the split unchanged: a failed record writes nothing and moves nothing (DP-03).
- **No data lake, no second truth.** The events carry identifiers, the code, the contact-stop flag and the rule version only, and rwb-reporting builds its read model from them (DP-09; ADR-018).

Wave is the one point where the two sources disagree: business epic EP01 places the story in wave 1 and the service sits in wave 2. The W-MAP wave is kept, as §R5.6 requires, and the conflict is recorded once for this service and this business epic (GAP-3074; ASM-5235).

### 3. Preconditions

- `RWB-P3-E1021-CON` is published and tagged: the transfer request shape, the queue and assignment shapes it answers with, the version-check error, the capacity error, the error set and the fake are baselined and handed to this story.
- The platform contract stories the DP table names are published with their stubs: the local decision record and the shared topic `rwb.decision-record.v1` (DP-03), the embedded Drools kit and the package reader (DP-04), the reference-data client (DP-07), the outbox and inbox library (DP-09), the workflow kit (DP-10), the topic-naming library (DP-14), the per-service Flyway baseline (DP-15) and the gateway-bff composite route (DP-19). The plan carries no build dependency on this key, so the story starts on Day 1 against those baselines and the fakes; the rows are tracked, not blocking (GAP-3075; ASM-5236).
- `deviation` exists in `rwb_deviation` with the columns of DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0, created by the DB story of this service; this story adds no table and no column.
- The TRANSFER package is in force at a version authored, tested and approved in rwb-decision (P7) with at least 50 passing scenarios, and each row holds trigger event, condition, target queue code and row order (legacy §3; D-RCV-36 T5, carried into the package registry of P7).
- The transfer reason list `LOV-TRANSFER-REASON` with R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral and R06 Wrong queue is readable on the reference-data contract of rwb-case (DL23; DP-07).
- The case trigger events arrive on the subscription the connection matrix gives S8 to P3; the event names are Not specified in the source documents (GAP-3079; ASM-5240).
- The data product behind the case facts carries today's business date, or shows its date as stale and holds the step (VR-S8-001-1; MSG-P1-001).
- The service runs as its own login on `rwb_deviation`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` is refused by the database and fails the boundary test (DP-01, DP-05).

### 4. Flow

1. A deviation is raised on a case for one of X1 to X7, or an open deviation is cleared, through `POST /cases/{caseId}/deviations` or `PATCH /deviations/{deviationId}` on `/api/recovery/deviation/v1` (DP-13).
2. `DeviationWorkflow` receives the signal on queue `rwb-deviation` and builds one `TransferTrigger`: event code (`DeviationRaised` or `DeviationCleared`), case number, stage code, route code, deviation state and the legal-hold flag.
3. The same signal path carries the case triggers of the subscription: a stage change or a route decision, a timer due, an approval request, a document stored or a payment missed, each with its own event code (legacy BR2; EV-05, EV-09, EV-12, EV-16, EV-18).
4. `evaluateTransferRules` loads the TRANSFER package version in force through the embedded kit and evaluates the fact; the first row in row order whose trigger and condition match wins and returns its rule ID and the package version (DP-04; legacy BR1, T5). No match means no transfer and no decision record entry.
5. A package with no version in force raises `NoPackageInForce` before the case is touched; the trigger stays in the outbox and is retried when a version is in force, and no default transfer ever runs (legacy BR12, R-UNI-41; MSG-P3-027).
6. The workflow skips an automated transfer while `legal_hold` is true and records the skip with R-UNI-20 (legacy BR6; R-DEV-01 keeps the legal clock running).
7. `requestCaseTransfer` calls rwb-case with the target queue code, the chosen owner, reason TRANSFER, the rule ID and the package version, and the trigger event ID as the idempotency evidence. One hop, 2 s, a breaker, and no retry inside the step (DP-11).
8. rwb-case locks the case by its version, picks the owner in the target queue with its assignment engine and a `LOWEST_LOAD` method, checks that the move is allowed from the case status, and in one transaction ends the open assignment, writes the new one with `transfer_reason_code`, updates queue, team and owner, and publishes `CaseTransferred` (the primary slice; legacy §4 steps 5 and 6).
9. A version conflict answers MSG-GEN-004 and the transfer is refused; an owner at the cap answers MSG-P3-002 and a queue with every owner at the cap places the case in the overflow queue with no owner and tells the team manager with MSG-P3-011 (legacy X1, X3, X8).
10. `recordAndApplyTransfer` writes, in one `rwb_deviation` transaction and as the last step before commit, the decision record with the rule ID, the package version, the from and to queue and owner and the trigger; a refused transfer is recorded with final call `TRANSFER_REJECTED` (legacy BR9; DP-03).
11. In the same transaction the activity moves the `deviation` row: `handler_user_id` becomes the owner the rule names and `state` moves to DEV_WITH_OWNER, or back to RESUMED when the trigger was the clear; the outbox row for `DeviationRaised` or `DeviationCleared` is written there (DP-09).
12. A repeated event ID is ignored and counted as an idempotency hit, and a repeated call with the same `Idempotency-Key` answers the response it already gave (R-UNI-40).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Two triggers reach the same case in the same second | First commits; second refused on the version check, recorded as `TRANSFER_REJECTED`, and the case ends in exactly one queue | MSG-GEN-004 | AC4, TC-E1-021-03 |
| X2 | No TRANSFER version is in force for the trigger | `NoPackageInForce` before the case is touched; the trigger stays in the outbox for retry; no default transfer | MSG-P3-027 | AC3, TC-E1-021-14 |
| X3 | A trigger arrives while `legal_hold` is true | No automated transfer; the skip is recorded with R-UNI-20 and nothing changes | None | AC5, TC-E1-021-10 |
| X4 | The same event ID arrives twice | Second ignored and counted; one transfer | None | Flow step 12, TC-E1-021-11 |
| X5 | No TRANSFER rule matches the trigger | No transfer and no decision record entry; the deviation stays where it is | None | AC8, TC-E1-021-14 |
| X6 | The named target owner is at the caseload cap | The request is refused with the owner named and nothing changes | MSG-P3-002 | AC6, TC-E1-021-07 |
| X7 | No owner below the cap in the target queue | The case is placed in the target queue's overflow queue with no owner and the team manager is told with the count | MSG-P3-011 | AC6, TC-E1-021-12 |
| X8 | The decision record cannot be written | Nothing changes: no transfer request, no `deviation` change and no event | MSG-P7-003 | AC7, TC-E1-021-09, TC-E1-021-16 |
| X9 | The caller lacks the Case record right on the raise or the outcome that fires the trigger | 403 before any change and before any decision record | MSG-P4-002 | AC9, TC-E1-021-15 |
| X10 | A statement, a test or a component reaches a `rwb_case` row, a `v_ace_*` view or another service's schema | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | Section 17 |

X1, X3, X4, X5, X6, X7, X8 and X9 restate the legacy exception rows X1, X6, X7, X10, X3, X8, X5 and X11 for this slice, and X2 is the package-not-in-force path the legacy story states below its own table. X10 is the DP-01 and DP-05 boundary. The legacy rows that belong to the primary slice — a manual transfer without a reason (MSG-P3-001) and a hold on a case already on hold — are not restated here, and the closed case is answered by rwb-case inside the transfer request.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against `RWB-P3-E1021-CON` and its fake, the platform stubs of DP-03, DP-04, DP-07, DP-09 and DP-19, and a synthetic `deviation` row; no live P3, P4 or P7 is needed |
| Negotiable | The activity names, the shape of the transfer request this service sends and the decision code per outcome are this story's choice; the rules, the messages, the package, the target queues and the `deviation` columns are fixed |
| Valuable | A deviation that changes who holds the case moves it at once, to the queue and owner the rule names, with the rule and its version recorded before the case changes |
| Estimable | One workflow branch, three activities, one package evaluation, one request to rwb-case, two event relays, the decision record and the schema sequence |
| Small | Fits two weeks with its tests on the fakes and the access and failure tests |
| Testable | Every path runs on synthetic cases through the contract fakes, plus the forced record failure and the boundary test |

### 7. Acceptance criteria

```gherkin
Feature: Transfer rules and engine v1

  Background:
    Given the TRANSFER package is in force at version "TRF-2026.11"
    Given the rwb-case contract mock returns queue "LIT-BKK-OFF" of team "LIT-BKK" with method "LOWEST_LOAD" and cap 150

  Scenario: AC1 Rule-driven transfer on a deviation trigger (new, D-RCV-60)
    Given the rwb-case contract mock returns case "RW-2026-000301" in "IN_PROGRESS" in queue "TDR-BKK-CO" with owner "U-21"
    Given the rwb-case contract mock returns the transfer accepted with owner "U-31", the member with the lowest load
    Given transfer rule "TRF-004" moves a case to queue "DEV-HANDLER" when "DeviationRaised" carries deviation "X3"
    When the deviation "X3" is raised on the case
    Then the transfer request carries queue "DEV-HANDLER", owner "U-31" and rule ID "TRF-004"
    Then the deviation row is in state "DEV_WITH_OWNER" with handler "U-31"
    Then the decision record carries rule ID "TRF-004" and package version "TRF-2026.11"

  Scenario: AC2 First match in row order only (new, D-RCV-60)
    Given the TRANSFER package holds rule "TRF-004" before rule "TRF-007", both matching the trigger "DeviationRaised" for the case
    When the trigger "DeviationRaised" arrives for the case
    Then only rule "TRF-004" is recorded, with its target queue and its package version
    Then no decision record carries rule ID "TRF-007" for the event

  Scenario: AC3 No package in force (new, D-RCV-60)
    Given the rwb-decision contract mock returns "NoPackageInForce" for package "TRANSFER"
    When "DeviationRaised" arrives for case "RW-2026-000303"
    Then no transfer request leaves the service and the case keeps its queue and owner
    Then the trigger stays in the outbox and the caller sees MSG-P3-027

  Scenario: AC4 Refused on the version check (new, D-RCV-60)
    Given the rwb-case contract mock returns the case at record version 8 for a transfer drawn on record version 7
    When a rule transfer to "LIT-BKK-OFF" and a rule transfer to "DIL-BKK-CO" arrive in the same second
    Then the system refuses the second transfer with MSG-GEN-004
    Then the decision record records the second transfer with final call "TRANSFER_REJECTED"

  Scenario: AC5 Legal hold stops automated transfers (new, D-RCV-60)
    Given the rwb-case contract mock returns case "RW-2026-000310" with legal_hold true
    When "TimerDue" arrives for the case and matches rule "TRF-003"
    Then no transfer request leaves the service and the case keeps its queue and owner
    Then the skip is recorded with rule R-UNI-20

  Scenario: AC6 Target owner at the cap (new, D-RCV-60)
    Given the rwb-case contract mock returns owner "U-24" holding 150 open cases in queue "TDR-BKK-CO"
    When rule "TRF-002" names owner "U-24" for case "RW-2026-000307"
    Then no transfer is written and the case keeps its queue and owner
    Then the outcome names MSG-P3-002 and the owner "U-24"

  Scenario: AC7 Decision record cannot be written (new, D-RCV-60)
    Given the local decision-record stub is stopped and returns MSG-P7-003
    When a rule transfer fires for case "RW-2026-000309" with transfer reason "R03"
    Then no transfer request leaves the service, the deviation row is unchanged and no event is published
    Then the caller sees MSG-P7-003

  Scenario: AC8 No rule matches (new, D-RCV-60)
    Given no TRANSFER rule matches "DocumentStored" for case "RW-2026-000314"
    When "DocumentStored" arrives for the case
    Then the case keeps its queue and owner
    Then the system writes no decision record entry

  Scenario: AC9 Role without the right (new, D-RCV-60)
    Given a caller whose role does not hold Case record U
    When the caller raises or clears a deviation that would fire a transfer
    Then the call is refused with 403 and MSG-P4-002 before any change and before any decision record
    Then the case keeps its queue and owner
```

The nine criteria are new: this slice owns no legacy criterion, because the split gives the criteria of RWB-E1-021 to the primary slice in rwb-case (`acs` is empty on this slice), and each criterion here tests only the deliverable of the title — the engine, the request it sends and the record it keeps. Every business value in the scenarios — the package version, the rule IDs, the queues, the owner IDs, the cap of 150, the reason list, the message IDs — is copied character for character from RWB-E1-021 §7, §5 and §14; no value is invented.

### 8. Business rules

| Rule | Route set | Codes | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DEV-01 | Deviations | X1 to X7 | ANY_STATE | DEVIATION_FLAGGED | deviation_code in (X1..X7) | Pause the stage clock, keep the prescription clock running, route to the named owner | DEV_FLAGGED | Workbench | Workbench | Same day |
| R-DEV-02 | Deviations | X1 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X1 | Assign to the complaint officer | DEV_WITH_OWNER | Complaint officer | Workbench | None |
| R-DEV-03 | Deviations | X2, X3 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code in (X2,X3) | Assign to the specialist; Legal joins X3 for the estate claim | DEV_WITH_OWNER | Hardship and vulnerability specialist | Workbench | None |
| R-DEV-18 | Deviations | X1 to X7 | DEV_RESOLVED | CLOCK_RESUMED | Any | Resume the stage clock and return the case | RESUMED | Previous owner | Workbench | None |

The four rows are copied character for character from FSD S8 A2.2.3.1, A2.4.3.1 and the DEVIATION machine of TSD S8 T4. R-DEV-04 to R-DEV-06 assign X4 to X7 to their named owners; their text is Not specified in the source documents (GAP-3078; ASM-5239). The owner column is a business role, not a service.

| ID | Rule | Source |
|---|---|---|
| BR1 | A case moves by the first TRANSFER row, in row order, whose trigger and condition match the `TransferTrigger`; the rule ID and the package version are returned and recorded | Legacy BR1; D-RCV-36 T5 |
| BR2 | The trigger is the one event code the fact carries: a deviation raised or cleared here, or a case trigger of the subscription forwarded to this child | Legacy BR2; R-DEV-01 |
| BR3 | The package is read from rwb-decision and evaluated by the embedded kit of this service; no rule row, row order or target queue is written in code | DP-04; ADR-017; legacy §17 |
| BR4 | No automated transfer while a legal hold is in force, and the skip is recorded | R-UNI-20; legacy BR6 |
| BR5 | Every transfer, applied or refused, is recorded with the rule ID and the package version before it takes effect; a failed record changes nothing and answers MSG-P7-003 | Legacy BR9; DP-03; TSD S8 T2 |
| BR6 | A version not in force leaves the trigger in the outbox, moves no case and is never a default transfer | R-UNI-41; legacy BR12 |
| BR7 | An event with the same ID is processed once, and an `Idempotency-Key` answers the response it already gave | R-UNI-40; legacy BR8 |
| BR8 | The move itself is rwb-case's: this service requests it on the owner's contract and writes no `recovery_case`, `queue` or `assignment` row | DP-01, DP-11; context pack ownership rows |
| BR9 | A transfer keeps the case status and both clocks: it moves the queue, the team and the owner only | Legacy BR10; R-UNI-18 |
| BR10 | No person name, contact value, address or identity number enters the deviation row, the decision record, a log, a workflow input or an event | Template and Rules v1 §R7.2 s17 |

### 9. State transitions

This story moves the `deviation` record of the case and requests a move of the case; it never writes the case state.

| From (`deviation.state`) | Event | Condition | To |
|---|---|---|---|
| No row, or DEV_FLAGGED | OWNER_ASSIGNED | R-DEV-02 or R-DEV-03 fires for the code, and the transfer request is accepted | DEV_WITH_OWNER, `handler_user_id` = the owner the rule names |
| DEV_WITH_OWNER | DEVIATION_RESOLVED | The clear path fires and R-DEV-18 applies | RESUMED with `cleared_at` written |
| Any | OWNER_ASSIGNED | The transfer is refused on the version check, the cap or the record | Unchanged, with the refusal recorded |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A deviation or case trigger arrives | The package version in force is loaded | Evaluating |
| Evaluating | A TRANSFER row matches | The legal-hold check passes | Requesting |
| Evaluating | No row matches, or no version in force | X2, X5 | Waiting, nothing changed, no record |
| Requesting | rwb-case accepts the move | The decision record is written | Applying |
| Requesting | rwb-case refuses on the version check or the cap, or the record write fails | X1, X6, X8 | Waiting, the refusal recorded, nothing else changed |
| Applying | The `deviation` update and the outbox row commit | The transaction commits | Waiting for the next trigger |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Team manager (RW-TEAMMGR) | Holds R on the case record (TSD S8 T6.1) and is the role the legacy story serves; receives the overflow notice of MSG-P3-011 |
| Complaint officer, Hardship and vulnerability specialist, Fraud investigator, Legal counsel | Are the named owners R-DEV-02 and R-DEV-03 route X1 to X3 to, and hold RU or R on the case record (FSD S8 A2.4.3.3; TSD S8 T6.1) |
| Case owner (RW-CASEOWN) | Holds CRU and raises or clears the deviation that fires the trigger |
| The rules component of this service (embedded kit) | Evaluates the TRANSFER package; it holds no right of its own and writes nothing |
| rwb-case (P3) | Owns the case, its assignment, its queue and its version check, and executes the move on this story's request |
| rwb-decision (P7) | Owns the TRANSFER package, its rows, their version and their approval; this story only evaluates the version in force |
| rwb-access (P4) | Owns the roles and the capability rights checked on the two operations |
| Solution architect | Confirms the transfer request shape and the event subscription (GAP-3076; GAP-3079) |

The legacy story named `RuleEvaluator` as the one evaluator; after the split the evaluator is the embedded kit of each service and the package registry stays in rwb-decision, which is ADR-017. No delegated-authority limit applies: a transfer takes no credit decision.

### 11. Data

| BR Field ID | Table | Owner | Use in this story |
|---|---|---|---|
| DF-CAS-036 to DF-CAS-045 | `deviation` | S8, `rwb_deviation` | **Write** `handler_user_id`, `state`, `cleared_at` and `outcome` on the transfer and clear paths; the other columns are read |
| None: library table | `decision_record` | Platform library in `rwb_deviation` | The hash-linked record written before the move (DP-03) |
| None: library table | `outbox_event`, `idempotency_key` | Platform library in `rwb_deviation` | The two event rows and the trigger key with the answer it holds |
| DF-CAS-001, DF-CAS-005, DF-CAS-006, DF-CAS-008, DF-CAS-009, DF-CAS-010, DF-CAS-011, DF-CAS-020 | `recovery_case` | P3 rwb-case | The case reference, status, stage, route, owner, queue, team and legal hold; consumed on the contract, never written |
| DF-WRK-001, DF-WRK-002, DF-WRK-004, DF-WRK-007, DF-WRK-008, DF-WRK-009 to DF-WRK-016, DF-WRK-040 | `queue`, `assignment` | P3 rwb-case | The target queue, its team, its cap, its overflow queue and the assignment swap with `transfer_reason_code`; named, never written |
| DF-REF-002, DF-REF-003, DF-REF-006, DF-REF-007, DF-REF-052, DF-REF-053, DF-REF-054, DF-REF-296 to DF-REF-298 | `rule_row` | P7 rwb-decision | The TRANSFER rows, their order and their version; read through the package, never written |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | P7 rwb-decision | The central ledger; the local record is copied to it by rwb-decision, not written here |
| DF-CAS-021 | `recovery_case.rule_version` | P3 rwb-case | Holds the package version label; written on P3's side, reported on the request |

The rule version this story records lives in the decision record: TSD S8 T3.1 gives `deviation` no rule or transfer column, and the legacy columns `recovery_case.rule_version` and `assignment.transfer_reason_code` are P3's (GAP-3080; ASM-5241). The lists are reference data read at their version: `LOV-DEVIATION` with X1 to X7, `LOV-RAISED-BY` and `LOV-DEV-OUTCOME` from TSD S8 T3.2, and `LOV-TRANSFER-REASON` with R01 to R06 on the rwb-case contract.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). These are the two operations the Ownership Map gives this service; this story adds none.

| Method | Path | Shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/deviations` | `DeviationRequest` in, `Deviation` out (API-S8-001) | Case record, right U, scope applied | `Idempotency-Key` header |
| PATCH | `/deviations/{deviationId}` | `DeviationOutcome` in, `Deviation` out (API-S8-002) | Case record, right U, scope applied | Not applicable |

Both answer 401, 403 with MSG-P4-002, 404, 409, 422 and 503 in the platform error envelope; the shapes and the exact status list are the CON story's of this service. The POST is the raise path and the PATCH is the clear path that fire the trigger.

#### 12.2 REST operations consumed

| Operation | Owner | Use |
|---|---|---|
| The transfer request that ends the open assignment and writes the new one; operation name Not specified in the source documents (GAP-3076; ASM-5237) | P3 rwb-case, contract `RWB-P3-E1021-CON` | The move of the case with reason TRANSFER, the rule ID, the package version and the trigger event ID; answers the assignment or a refusal |
| The queue, capacity and owner selection read; operation name Not specified in the source documents (GAP-3076; ASM-5237) | P3 rwb-case | The target queue, its team, its cap, its overflow queue and the member with the lowest load |
| The reference-data read of `LOV-TRANSFER-REASON` (DP-07); operation name Not specified in the source documents (GAP-3076; ASM-5237) | P3 rwb-case | The six reason codes R01 to R06 with their version |
| The package and rule-in-force read (DP-04); operation name Not specified in the source documents (GAP-3076; ASM-5237) | P7 rwb-decision | The TRANSFER package in force with its version and its rows |
| The authorise call; operation name Not specified in the source documents (GAP-3076; ASM-5237) | P4 rwb-access | The Case record right on the two operations |
| The case-facts read (DP-05); operation name Not specified in the source documents (GAP-3076; ASM-5237) | P1 rwb-source-data | The case facts the trigger is built from, with their freshness stamp |

All six are one hop with a 2 s budget and a breaker, and none retries inside the step (DP-11, ADR-020). Only the first is a row of the plan's C list, which holds `RWB-P3-E1021-CON` alone.

#### 12.3 Events published

| Event | Topic | Data | Consumers |
|---|---|---|---|
| `DeviationRaised` (EV-06, `rwb.deviation.DeviationRaised.v1`) | `rwb.deviation.events.v1`, with `.retry` and `.dlt` | Case reference, deviation reference, code, raised-at, paused state, contact-stop flag, rule ID and package version; CloudEvents envelope; no personal data | rwb-case, rwb-comms and rwb-reporting (connection matrix column S8) |
| `DeviationCleared` (EV-07, `rwb.deviation.DeviationCleared.v1`) | `rwb.deviation.events.v1`, with `.retry` and `.dlt` | Case reference, deviation reference, outcome, cleared-at, rule ID and package version; CloudEvents envelope; no personal data | rwb-case, rwb-comms and rwb-reporting (connection matrix column S8) |

The ids are the two events the Ownership Map gives S8; their names are the two TSD S8 T5.3 publishes. No new event name is added by this story, and `CaseTransferred` (EV-04) is published by rwb-case, not here.

#### 12.4 Events consumed

| Event | Owner | Use |
|---|---|---|
| The case triggers: stage change or route decided, timer due, approval requested, document stored, payment missed; event names Not specified in the source documents (GAP-3079; ASM-5240) | P3 rwb-case | Builds the `TransferTrigger` for those trigger codes and keeps an open deviation aligned with its case |
| The source-data events the matrix names; event names Not specified in the source documents (GAP-3079; ASM-5240) | P1 rwb-source-data | The case facts behind the trigger and their freshness stamp |

The S8 row of the connection matrix names an event subscription to P3 and to P1 and publishes no event name for either, so both consumer groups are declared against the placeholder and faked.

#### 12.5 Workflows and activities

| Name | Type | Queue | Element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per case, started at any time, child of `CaseWorkflow`, parent close policy ABANDON, continues-as-new | `rwb-deviation` in namespace `rwb-recovery` | Hosts the trigger branch that fires the engine (DP-10) |
| `evaluateTransferRules` | Activity, the EvaluateRules step | `rwb-deviation` | The `TransferTrigger` in; rule ID, package version and target queue out |
| `requestCaseTransfer` | Activity, the one-hop request | `rwb-deviation` | The rule result in; the accepted assignment or a refusal out |
| `recordAndApplyTransfer` | Activity, the RecordAndApply step | `rwb-deviation` | The outcome in; the decision record, the `deviation` update and the outbox row out, one transaction |

The four names are this story's; the workflow is the one the Ownership Map gives S8 and the three activities sit on the same queue.

#### 12.6 Schedules

None. The Ownership Map gives S8 no job, the trigger is an event or a signal, and the legacy JOB-05 and its timer events stay with the owner of the timers. The story declares no Quartz row and no shared job table (DP-10 is applied as an event-started workflow, not as a Schedule).

#### 12.7 Tables owned

| Table | Owner | Use |
|---|---|---|
| `deviation` | S8, `rwb_deviation` | The row whose handler and state the transfer moves |
| `decision_record` | Platform library in `rwb_deviation` | The local record written before the move (DP-03) |
| `outbox_event`, `idempotency_key` | Platform library in `rwb_deviation` | The event rows and the trigger key |

`recovery_case`, `queue`, `assignment`, `timer`, `decision_log_entry`, `rule_row` and every `v_ace_*` view are other owners' and are named only; no foreign key leaves `rwb_deviation` (DP-01).

#### 12.8 Contract fakes

| Fake | Answer | Used by |
|---|---|---|
| rwb-case transfer fake (`RWB-P3-E1021-CON`) | An accepted move with owner U-31 and the assignment; a version conflict; a refusal at the cap; a queue at the cap with its overflow queue | AC1, AC4, AC6 |
| rwb-case queue and capacity fake | Queue `LIT-BKK-OFF` of team `LIT-BKK`, method `LOWEST_LOAD`, cap 150; the overflow queue | AC1, AC6 |
| rwb-case reference-data fake | `LOV-TRANSFER-REASON` R01 to R06 at its version | AC1, AC7 |
| rwb-decision package fake | The TRANSFER package at `TRF-2026.11` with the rows of the tests; `NoPackageInForce` | AC2, AC3 |
| rwb-access authorise fake | A granted Case record right; a refused one | AC9 |
| rwb-source-data data-product fake | The case facts with a fresh stamp; a stale stamp | Section 5 X10 |
| Local decision-record stub (DP-03) | A healthy chain; a stopped chain answering MSG-P7-003 | AC7 |
| Outbox relay stub (DP-09) | A relayed `DeviationRaised` and `DeviationCleared`; a relay that fails and retries | AC1, AC7 |
| gateway-bff composite route fake (DP-19) | The merged SCR-02 and SCR-03 answer for a synthetic case | Section 15 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 6 consumed | `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` on `/api/recovery/deviation/v1`; the rwb-case transfer, queue and reference-data reads, the rwb-decision package read, the rwb-access authorise and the rwb-source-data read; one hop, 2 s |
| Kafka | 2 published, 2 consumed | `DeviationRaised` and `DeviationCleared` on `rwb.deviation.events.v1`; the P3 and P1 subscriptions; the decision record rides the library's `rwb.decision-record.v1` and is not this service's event |
| Temporal | 1 workflow and 3 activities | `DeviationWorkflow` with `evaluateTransferRules`, `requestCaseTransfer` and `recordAndApplyTransfer` on `rwb-deviation`; no Schedule |
| File | None | No file is read, built or delivered by this story |

### 13. Solution plan

**Deliverables.** The trigger branch of `DeviationWorkflow`, the three activities, the TRANSFER package evaluation against the version in force, the legal-hold and idempotency checks, the one-hop transfer request to rwb-case, the decision record writer, the `deviation` update with its outbox row, the two event relays, and the per-service Flyway sequence of `rwb_deviation`.

**Pattern application** (§R5.5)

| DP | Legacy marker | Pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>`, "recovery schema" | Owner's schema `rwb_deviation`; no other service's table is read | None |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H `RWB-PLT-E1027-CON` |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H `RWB-PLT-E1072-CON`; C `RWB-P7-E1073-CON` |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract | None |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H `RWB-PLT-E1043-CON`; C `RWB-P3-E1043-CON` |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library, owner topic, CloudEvents | H `RWB-PLT-TE006-CON` |
| DP-10 | Quartz, JOB-nn | Event-started workflow through the workflow kit | H `RWB-PLT-E1071-CON` |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | None (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/deviation/v1` | None |
| DP-14 | `rwb.p<n>.` and `rwb.casewf.` topic names | `rwb.deviation.events.v1` through the naming library | H `RWB-PLT-E1047-CON` |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_deviation` | H `RWB-PLT-E1044-CON` |
| DP-19 | Screen, ace-web | gateway-bff composite route | H `RWB-PLT-N001-CON` |

The eight H rows the table adds are platform contract rows; the plan's build list for this key is empty and therefore stays empty in the metadata, and the rows are tracked as platform dependencies (GAP-3075; ASM-5236). DP-11 keeps the one class C dependency the plan gives, `RWB-P3-E1021-CON`; DP-04 and DP-07 also add a C row each, which the metadata does not carry.

**Build steps.** (1) Wire the trigger branch and the three activities on `rwb-deviation`. (2) Load the TRANSFER package version through the embedded kit and evaluate the `TransferTrigger`, first match in row order. (3) Add the legal-hold and event-ID checks and the `NoPackageInForce` path. (4) Send the transfer request to rwb-case with the rule ID, the version and the trigger event ID, and map its refusals. (5) Write the decision record first, then the `deviation` update and the outbox row, in one transaction. (6) Relay `DeviationRaised` and `DeviationCleared`. (7) Fold the story's schema need into the per-service Flyway sequence, with no shared `recovery` migration. (8) Prove AC1 to AC9 on the fakes and run the boundary test.

**Feature flag.** `rwb.s8.transfer`. Off: no rule transfer runs, the trigger stays in the outbox, and the two operations keep working without firing the engine.

**Done when.** AC1 to AC9 pass at component and contract level on the fakes, every transfer and every refusal leaves one decision record with its rule ID and the package version, the repeat test writes once and publishes once, and the boundary test shows no `rwb_case` statement and no `v_ace_*` read.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-001 | A manual transfer without a reason (the primary slice's path, named for traceability) | Choose a reason for the transfer. |
| MSG-P3-002 | Target owner at the cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-005 | Move not allowed from the status | This case cannot move to {state} from {current}. |
| MSG-P3-011 | Target queue full, case in overflow | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-027 | No TRANSFER version is in force for a trigger | The rule version was refused at the {check} check: {detail}. |
| MSG-GEN-004 | Second transfer on a changed record | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | The data product behind the case facts is stale | {product} is from {date}. Today's ACE batch has not arrived. |

The text is RWB-E1-021 §14 and FSD S8 A2.1.3.1, copied unchanged; no message is reworded and none is added. For MSG-P3-027 the {check} value is "package in force" and the {detail} names the package code only.

### 15. Screens and states

No screen in this story. The transfer screen SCR-05 comes in Epic 2 (RWB-E2-012) and the transfer is programmatic here.

| Screen | States | What this story answers |
|---|---|---|
| SCR-02 Case list | List; filtered | The new queue and owner after a transfer, read through the gateway-bff composite route (DP-19) |
| SCR-03 Case record | Read only; on hold | The owner, the queue and the hold banner of a case whose deviation moved it; the transfer itself is not editable here |

Both screens are the edge contract's; this story fixes only its own read answers and the refusals of section 14.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-021-01 | AC1, BR1 | Component | Case in TDR-BKK-CO, "DeviationRaised" for X3; package TRANSFER "TRF-2026.11", rule TRF-004 |
| TC-E1-021-02 | AC1, BR2 (the raise path that fires the trigger) | Component | Raise with reason R03 on a case whose rule names a new owner |
| TC-E1-021-03 | AC4, BR7 | Contract | Two transfers on record version 7 and 8 |
| TC-E1-021-04 | AC1, BR2 | Component | Eight TRANSFER rows, one per trigger |
| TC-E1-021-05 | AC5 (skip and resume) | Component | legal_hold true, then the clear that resumes |
| TC-E1-021-06 | AC9, X9 | Component | No Case record right on the raise |
| TC-E1-021-07 | AC6, BR4 | Contract | Owner U-24 at 150, refusal MSG-P3-002 |
| TC-E1-021-08 | AC4 (status does not allow the move) | Contract | Closed case answered by the rwb-case fake |
| TC-E1-021-09 | AC7, BR5 | Component | Decision-record stub stopped for a rule transfer |
| TC-E1-021-10 | AC5, BR4 | Component | legal_hold true and "TimerDue" matching TRF-003 |
| TC-E1-021-11 | AC1, BR7 | Component | The same event ID twice, one transfer and one idempotency hit |
| TC-E1-021-12 | AC6, X7 | Contract | Every member of LIT-BKK-OFF at 150, overflow queue |
| TC-E1-021-13 | AC7 (the clear path) | Component | The record write forced to fail on the clear path; the deviation stays open |
| TC-E1-021-14 | AC8, BR1, BR6 | Component | "DocumentStored" with no match, and `NoPackageInForce` |
| TC-E1-021-15 | AC9, access | Component | A role without Case record U calls the raise; 403 with MSG-P4-002 |
| TC-E1-021-16 | AC7, resilience | Component | The record write forced to fail for a rule transfer; the trigger retried and the case unchanged |

The sixteen ids are the legacy cases of RWB-E1-021 in their legacy order, carried as the proof of this slice; the Covers column names the criterion of this story that each one now exercises, because the legacy criteria are owned by the primary slice. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same id. No `-ITG` copy belongs to this story: it has no class I dependency.

### 17. Guardrails

- No business value in code: the trigger rows, the target queues, the row order, the reason list and the caps are package rows, reference data or rwb-case facts, read with their version.
- No personal data in the `deviation` row, the decision record, an event, a workflow input, a log or a prompt: identifiers, codes, instants and a rule version only.
- ACE data and case data only through the owner's contract: no `v_ace_*` view, no `rwb_case` statement, no document blob and no other service's schema (DP-01, DP-05, DP-11).
- One evaluator per service and one package registry: TRANSFER is evaluated only through the embedded kit against the version in force from rwb-decision, and no trigger list or target queue is written in code (DP-04; ADR-017).
- One base, one topic, one queue and one login per service; this story adds no second topic and no Schedule (DP-13, DP-14).
- The decision record is written before the move and in its transaction; a failure rolls the row back, and a transfer never resets the stage clock or the prescription date.

### 18. Traceability

| Legacy | Owner after the split | This story |
|---|---|---|
| RWB-E1-021 AC1 to AC14 | The primary slice of this legacy key in rwb-case (`acs` is empty on this slice) | AC1 to AC9 prove the engine, the request and the record on the fakes; the end-to-end move is proved where the criteria are owned |
| RWB-E1-021 TC-E1-021-01 to -14, -16 | This story | TC-E1-021-01 to -14 and -16, on the component and contract levels |
| RWB-E1-021 TC-E1-021-15 (access) | This story | TC-E1-021-15 |
| RWB-E1-021 manual transfer API, legal hold (BR11, legacy X2, X9) | The primary slice | Not restated; named in section 5 and section 19 |

| Source | What it supplies |
|---|---|
| REQ-CWC-010, REQ-CWC-016, REQ-WKM-003, REQ-CWC-005 | Transfer by rule on eight triggers and a manual request with a reason; every transfer logged with the rule ID and version; the reason list; one queue and one open assignment |
| RWB-E1-021 §1 to §19 | The `TransferTrigger`, the package TRANSFER, the eight triggers, R-UNI-20, R-UNI-39 to R-UNI-41, the message texts, the states and the legacy tests |
| FSD S8 A2.2, A2.4, A2.6 and the DEVIATION machine | R-DEV-01 to R-DEV-03, R-DEV-18, the roles, the deviation states and the contact stop |
| TSD S8 T2, T3.0, T3.1, T3.2, T4, T5.3, T6.1 and T-A.1 | The decision-first rule, the `deviation` columns and lists, the state machine, the two events, the rights and the two operations |
| Context pack S8, the connection matrix and the Ownership Map | The schema, base, topic, queue, the two events, the one owned table, the workflow and the listeners |
| Split plan, slice RWB-S8-E1021-APP | H, C, I, X, the lane, the wave and the release (GAP-3074; GAP-3075) |

### 19. Out of scope

- The manual transfer endpoint, its `MANUAL` reason path, the legal-hold place and lift, the assignment swap, the version check and the `CaseTransferred` publication: the primary slice of this legacy key in rwb-case.
- The contract surface: the OpenAPI and AsyncAPI documents, the `deviation` element, the lists, the envelopes, the error set and the fakes (the CON stories of this service and of P3).
- The TRANSFER package rows, their authoring, approval, promotion and rollback in rwb-decision, and the DEV transfer rows themselves (GAP-3078).
- The other six deviation codes and their flows (X2 to X7), the screening agent, the low-confidence review, two deviations on one case, the contact-breach path and the override review — each is its own story of this service.
- The case of record, its status, its route state, its timers and its queues (rwb-case, P3); the notices (rwb-comms, P6); the roles and reference data (rwb-access, P4).
- The schema, migration, login, deployment, observability and pipeline of `rwb_deviation` beyond this story's own Flyway sequence (the DB, INF and OPS stories of this legacy key).
- Any change to a legacy file, to a master or to built Epic 1 code.
