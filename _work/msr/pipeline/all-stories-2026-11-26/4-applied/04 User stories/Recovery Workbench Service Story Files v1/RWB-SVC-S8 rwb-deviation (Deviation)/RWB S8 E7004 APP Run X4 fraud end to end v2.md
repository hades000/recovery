# RWB-S8-E7004-APP Run X4 fraud end to end

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7004-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S8-O |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S8-E7004-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the X4 fraud slice of RWB-E7-004 in rwb-deviation. The legacy exception criterion is kept word for word with its origin tag; the flag and the hold apply R-UNI-08 and R-DEV-01, the assignment applies R-DEV-04 with the fraud team as the named handler, the confirmed and cleared outcomes apply R-DEV-13 and R-DEV-14 and the reopen applies R-DEV-19; the decision is recorded through the local decision-record library before any row changes (DP-03); the two operations are served on base `/api/recovery/deviation/v1` (DP-13) and SCR-06 and SCR-08 reach them through the gateway-bff composite route (DP-19). The Aric referral is FEAT-ADM-13 in P4 and INT-31 is not available today, so no referral is built here. The legacy success criterion AC1 is owned by RWB-ITG-E7004-ITG. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S8-E7004-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **fraud investigator (RW-FRAUD)**, I want **the Workbench to raise X4 on the case, hold it with the stage clock paused and the prescription clock still running, name the fraud team as the handler, and route the case on the confirmed or the cleared outcome**, so that **every deviation has a handler and a clock, and a case with a fraud signal is never worked as if nothing had happened**.

This is the build slice of legacy RWB-E7-004. It owns:

- the legacy exception criterion AC2, copied verbatim with its origin tag (section 7);
- the X4 branch of `DeviationWorkflow` on task queue `rwb-deviation` in namespace `rwb-recovery`, the child workflow of `CaseWorkflow` that can start at any time and pauses the stage clock (context pack ownership rows; Temporal and Drools Design slides 8 and 13);
- the evaluation of R-UNI-08, R-DEV-01, R-DEV-04, R-DEV-13, R-DEV-14, R-DEV-19, R-DEV-20 and R-DEV-21 against the DEVIATIONS route set of 22 rules over 9 states and the UNIVERSAL package of 50 rules (Business Rules and Routing Logic v4; TSD S8 T4);
- one `deviation` row per flag in `rwb_deviation`, within the columns of DF-CAS-036 to DF-CAS-045 that this slice fills (section 11);
- the local decision record of the flag, the assignment and the outcome, written before any row or state changes, with the rule ID and the package version in force (DP-03);
- the publication of `rwb.deviation.DeviationRaised.v1` (EV-06) and `rwb.deviation.DeviationCleared.v1` (EV-07) on `rwb.deviation.events.v1` through the outbox;
- API-S8-001 `POST /cases/{caseId}/deviations` and API-S8-002 `PATCH /deviations/{deviationId}` on base `/api/recovery/deviation/v1`, and the states of SCR-06 Raise deviation and SCR-08 Deviation queue behind the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the two operations, the `DeviationRequest`, `DeviationOutcome` and `Deviation` elements, the field IDs, the consumed rows, the rights, the error set, the events as contract and the fakes, which are RWB-S8-E7004-CON; the legacy success criterion AC1 and the end-to-end proof across the real services, which are RWB-ITG-E7004-ITG; the Aric referral of INT-31, which is FEAT-ADM-13 in P4 and not available today; the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case (P3); the write-off route, which is rwb-writeoff (S7); the route decision D6, which is rwb-valuation (S1); the screening of FEAT-DVH-04 and the other six deviation codes; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The failure this story is written against is a case that is flagged for fraud and carries on being worked as an ordinary collection case. R-UNI-08 fires when Aric or an officer flags fraud and raises X4, holds the case and refers it to the fraud team the same day; R-DEV-04 assigns X4 to the fraud team, and R-DEV-01 pauses the stage clock while the prescription clock keeps running (Business Rules and Routing Logic v4). A demand letter, a settlement offer or a write-off decision taken after a fraud signal is a loss the bank creates itself. The feature objective and the measure are unchanged from the legacy story and the module FSD: "Refers to the fraud team, tracks the investigation and routes the case on the outcome", measured as "Deviations closed within the service level | Set with DL22 | Decision log and Workbench records | Monthly" (FSD S8 A2.13.1; Epics 3 to 8 Specification v3, FEAT-DVF-04).

The requirement is REQ-S8-001, "Each of X1 to X7 runs end to end with its own flow, approver, contact rules and return point", with REQ-DVH-010, "A fraud flag refers the case to the fraud team and holds recovery action until it is confirmed or cleared" (FSD S8 Requirements served). What D-RCV-60 changes is who owns each part of the sentence.

- **The deviation is this service's.** `deviation` is S8's one table in `rwb_deviation` (context pack ownership rows; TSD S8 T3.1), so the flag, its reasons and its handler are recorded here and nowhere else.
- **The two clocks stay with rwb-case.** The stage clock and the prescription clock are timers of P3; the deviation is a signal that pauses the first and never the second, because the law does not pause (R-DEV-01; Temporal and Drools Design slide 8).
- **The two outcomes are routes, not decisions taken here.** R-DEV-13 routes a confirmed fraud case to write-off and R-DEV-14 returns a cleared one to the collections decision; R-DEV-19 reopens the route decision with the segment recomputed and the hard gates re-run. This service names the outcome and answers the move; S7 and S1 own the routes.
- **The decision is recorded first**, in the same transaction as the row and the state answer, which the legacy AC2 tests and DP-03 requires.
- **The referral is not built here.** INT-31 Aric is "Not available today; by the fraud investigator" and the referral itself is FEAT-ADM-13 in the administration module (Epics 3 to 8 Specification v3), so this story raises, holds, assigns and routes, and calls no external system. Aric adds no dependency and no external row.

No business value moves: the deviation codes, the raised-by list, the outcome list and the 10-working-day service level of R-DEV-20 are rows of LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME and rows of the rule package, read with their version, never constants of the code.

### 3. Preconditions

- RWB-S8-E7004-CON is published: the two operations, the `DeviationRequest`, `DeviationOutcome` and `Deviation` elements, the field IDs, the consumed rows, the rights, the `Idempotency-Key` rule, the error set, the two events and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003, so the row, the record and the state answer commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-06 and SCR-08 reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The rwb-case reads are published with their fakes: the case state and the handler, and the timers of the case. The stage pause and resume are the parent `CaseWorkflow`'s and arrive as a signal on the workflow boundary; where a REST operation is published for them its name is Not specified in the source documents (GAP-3057; ASM-5163).
- The rwb-decision reads are published with their fakes: the DEVIATIONS route set at its version in force together with the UNIVERSAL package, and the decision log of the case. Their operation names are Not specified in the source documents (GAP-3057; ASM-5162).
- `deviation` exists in schema `rwb_deviation` from the DB story of this service, with the columns of DF-CAS-036 to DF-CAS-045, the lists LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME, and the standard record columns of TSD S8 T3.0; this story adds no table, no column and no migration.
- The DEVIATIONS route set is in force at its version and holds R-DEV-01, R-DEV-04, R-DEV-13, R-DEV-14, R-DEV-19, R-DEV-20 and R-DEV-21, and the UNIVERSAL package holds R-UNI-08; where the package version is absent the raise is refused with 503 and nothing changes, which is a state the story must be able to reach.
- The service runs as its own login on schema `rwb_deviation`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery_case`, `timer` or `rwb_case` is refused by the database and fails the boundary test (ASM-5162).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S8-E7004-CON when its tests pass.

### 4. Flow

1. The X4 flag arrives from an officer on SCR-06 or from the screening trigger of FEAT-DVH-04; the request names the case, the code `X4`, the reason and the raised-by value. A flag from Aric is the same request once FEAT-ADM-13 exists (R-UNI-08).
2. `DeviationWorkflow` on queue `rwb-deviation` starts, or signals the running child, and reads the version of the DEVIATIONS and UNIVERSAL packages in force from rwb-decision, one hop with a 2 s budget and a breaker (ASM-5162).
3. `EvaluateDeviationRules` evaluates R-UNI-08 and R-DEV-01 on the flag: the code is in X1 to X7, so the deviation is raised, the case is held and the move to `DEV_FLAGGED` is named with the rule ID and its version. A code outside the seven, or a code with no owner, is not a business value invented here: R-DEV-21 assigns it to the team manager and logs the unmapped code (ASM-5167).
4. `DeviationDecisionRecordWriter` writes one decision record through the local library, **before any change**: the case reference, the deviation reference, the rule ID with its package version, the code, the raised-by value, the paused state, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC2).
5. `DeviationRowWriter` inserts one `deviation` row in one `rwb_deviation` transaction with the decision record and the idempotency row: `case_id`, `deviation_code` `X4`, `raised_at`, `raised_by`, `paused_state` read from the case, `contact_stop`, and `handler_user_id` empty until the assignment. `cleared_at` and `outcome` stay empty.
6. `CaseMoveAnswer` answers rwb-case with the move `DEV_FLAGGED` and the paused state, and signals the parent `CaseWorkflow`: the parent pauses the stage timer and leaves the prescription timer running (R-DEV-01; Temporal and Drools Design slide 8).
7. The same workflow run applies R-DEV-04 to the X4 code: the fraud team is the named handler, the move is `DEV_WITH_OWNER`, and the row's `handler_user_id` is written from the answer. The assignment is the rule's and not a request field, because the published `DeviationOutcome` body carries an outcome and a note only, so no operation of this service re-assigns a deviation by hand (ASM-5163). The answer to the raise carries MSG-S8-001 with the deviation and the handler.
8. `DeviationEventPublisher` writes the `DeviationRaised` row of the outbox in the same transaction and the relay publishes `rwb.deviation.DeviationRaised.v1` on `rwb.deviation.events.v1` with `caseId`, `deviationCode` and `raisedBy`; rwb-case, rwb-comms and rwb-treatment consume it (EV-06).
9. A durable timer of the workflow runs the deviation service level of R-DEV-20; on expiry the case escalates to the team manager with the breach reported and the deviation stays at `DEV_WITH_OWNER` (ASM-5166).
10. The fraud team records the outcome on API-S8-002 with the `DeviationOutcome` body: the confirmed or the cleared step. R-DEV-13 names the move to `DEV_REROUTE` and the write-off route for a confirmed fraud; R-DEV-14 names the same move and the collections decision for a cleared one. The row's `outcome` is `RE_ROUTED` and `cleared_at` is written, and one more decision record is written first (LOV-DEV-OUTCOME; TSD S8 T4).
11. rwb-case applies the move and the deviation clears: the outbox publishes `rwb.deviation.DeviationCleared.v1` with `caseId`, `deviationCode` and `outcome`, the stage clock resumes under R-DEV-18, and R-DEV-19 reopens the route decision in rwb-valuation with the segment recomputed and the hard gates re-run, ending in `ROUTE_D6` (EV-07; ASM-5163).
12. A repeated raise with the same `Idempotency-Key`, or the same outcome twice on one deviation, writes no second row, no second record and no second event; the key answers the deviation it created and a conflicting outcome answers 409.
13. SCR-06 shows the raise in its form and saved states and SCR-08 shows the open deviations of the case in its loading and list states, read from this service through the gateway-bff composite route, next to the case state of rwb-case (DP-19; FSD S8 Screens).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written, or the central ledger does not confirm it | The transaction writes nothing: no `deviation` row, no state answer and no outbox row leave the service | MSG-P7-003 | AC2, TC-E7-004-02, TC-E7-004-04 |
| X2 | The caller does not hold Case record U of the operation | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | TC-E7-004-03 |
| X3 | A required field of the request is absent or invalid, or the code is outside LOV-DEVIATION | 422 with the field named; nothing is written | MSG-GEN-001 | AC2, X4 |
| X4 | The rwb-case or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered; the caller sees 503 | None | AC2 |
| X5 | The DEVIATIONS package version in force is absent | The raise is refused with 503 and no row exists; the flag can be re-raised once the version is published | None named | AC2 |
| X6 | The deviation sits with its owner past the service level of R-DEV-20 | The case escalates to the team manager and the breach is reported; the state does not change | None named | X6 |
| X7 | A code outside X1 to X7, or a code with no owner | R-DEV-21 assigns it to the case owner's team manager and logs the unmapped code | None named | X7 |
| X8 | A repeated raise with the same `Idempotency-Key`, or a second outcome on one deviation | One row, one record and one event; the key answers the deviation it created, a conflicting outcome answers 409 | None | X8 |
| X9 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, a `timer` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR4, BR5 |

X1 and X2 are the legacy exception paths of the story, X3 and X4 are the FSD validation rule VR-S8-013-1 and the contract budget, X5 to X7 are the package, the service level and the unmapped code, and X8 and X9 are the once-only rule and the ACE and schema boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S8-E7004-CON, the rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P7 or S7 |
| Negotiable | The activity names, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screen states, the operations and the table columns are fixed |
| Valuable | A fraud signal holds the case the same day with a named handler and one clock paused, and the outcome reaches the route decision either way, which is the failure the legacy story was written against |
| Estimable | One workflow branch, one evaluator, one record write, one row writer, one event publisher, one case-move answer, four clients, one service-level timer and one screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Every path runs on a synthetic case, a synthetic package and the contract fakes, plus the access, the failed-record, the unmapped-code and the service-level cases; the end-to-end proof is RWB-ITG-E7004-ITG's |

### 7. Acceptance criteria

```gherkin
Feature: Run X4 fraud end to end

  Background:
    Given case "RW-2026-001204" has no open deviation and the DEVIATIONS package is in force at its version with R-UNI-08 and R-DEV-01 to R-DEV-21
    Given every consumed contract is the published contract of its owner and is answered by its fake
    Given the caller holds Case record U

  Scenario: AC2 Not recorded (legacy RWB-E7-004 AC2)
    Given the rwb-decision contract mock returns no decision-log entry for the case
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The criterion is the legacy exception criterion of RWB-E7-004 word for word, with its origin tag added and nothing else changed: the two Givens, the When and the Then stand as they are. The cross-service part is the decision log, which in the target is the local decision record of DP-03 written in `rwb_deviation` and confirmed by the central ledger of rwb-decision, so one `Given the rwb-decision contract mock returns ...` line is added in front of the legacy text and nothing else. The legacy success criterion AC1 is owned by RWB-ITG-E7004-ITG word for word; this story builds the behaviour it describes — the raise, the hold, the fraud handler, the tracked investigation and the two outcome routes — and the four legacy test cases of section 16 exercise it at Component level, while the harness proves it across the real services. No new criterion is written here: the split plan gives this key's new criteria to the CON story and to the harness (GAP-3057; ASM-5169).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-UNI-08 | Universal rules | All | ANY_ACTIVE | FRAUD_FLAGGED | Aric or an officer flags fraud | Raise X4, hold the case, refer to the fraud team | HELD_DEVIATION | Fraud team | Aric, Workbench | same day |
| R-DEV-01 | Deviations | X1 to X7 | ANY_STATE | DEVIATION_FLAGGED | deviation_code in (X1..X7) | Pause the stage clock, keep the prescription clock running, route to the named owner | DEV_FLAGGED | Workbench | Workbench, the Workbench document hub | same day |
| R-DEV-04 | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code = X4 | Assign to the fraud team and refer to Aric | DEV_WITH_OWNER | Fraud team | Aric, Workbench | None |
| R-DEV-13 | Deviations | X1 to X7 | DEV_WITH_OWNER | FRAUD_CONFIRMED | deviation_code = X4 and fraud confirmed | Route to write-off; recovery continues under the fraud case | DEV_REROUTE | Write-off team | Aric, Workbench | None |
| R-DEV-14 | Deviations | X1 to X7 | DEV_WITH_OWNER | FRAUD_NOT_CONFIRMED | deviation_code = X4 and fraud not confirmed | Return to the collections decision | DEV_REROUTE | Case owner | EFS, Workbench | None |
| R-DEV-19 | Deviations | X1 to X7 | DEV_REROUTE | ROUTE_REOPENED | Any | Recompute the segment and re-run the hard gates | ROUTE_D6 | Case owner | Workbench | None |
| R-DEV-20 | Deviations | X1 to X7 | DEV_WITH_OWNER | SLA_BREACHED | time in DEV_WITH_OWNER exceeds the deviation service level | Escalate to the team manager and report the breach | DEV_WITH_OWNER | Team manager | Workbench | 10 working days |
| R-DEV-21 | Deviations | X1 to X7 | DEV_FLAGGED | OWNER_ASSIGNED | deviation_code is not one of X1 to X7, or no owner is set for the code | Assign to the case owner's team manager and log the unmapped code | DEV_WITH_OWNER | Team manager | Workbench | same day |

The eight rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner and systems columns name business roles and systems, not services: in the target the "Rules component" of the package is read from rwb-decision (P7) and evaluated here, "Aric" is INT-31 reached through FEAT-ADM-13 in P4 and is not called by this story, "EFS" and "ALS" are facts of the rwb-source-data products, "Workbench" is SCR-06 and SCR-08, and the case moves are written by rwb-case on this story's answer while the deviation row is written here.

| ID | Rule | Source |
|---|---|---|
| BR1 | The deviation is this service's: `deviation` is the one table of `rwb_deviation`, and no other service writes it | Context pack ownership rows (table `deviation`); TSD S8 T3.1 |
| BR2 | The decision is recorded before the row and the state change, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S8 T2 ("writes the decision log entry before any change"); legacy AC2 |
| BR3 | The DEVIATIONS route set and the UNIVERSAL package are read at their version and evaluated here; no rule row, code list or service level is a constant of the code | FSD S8 A2.13.3.1, BR-S8-013; TSD S8 T3.2; ASM-5162 |
| BR4 | The two clocks stay with rwb-case: this story signals the pause and the resume and reads the timers, and writes no `timer` row and no `recovery_case` row | R-DEV-01; Temporal and Drools Design slide 8; ASM-5163 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_deviation`; `case_id` and `handler_user_id` are identifiers of other services' facts | DP-01; TSD S8 T3.3 |
| BR6 | The fraud team is the named handler of X4, and a code with no owner goes to the team manager and is logged as unmapped | R-DEV-04; R-DEV-21; REQ-DVH-003 |
| BR7 | Every action is exactly once: one deviation per flag and key, one record and one event per action, and no second row on a repeat | TSD S8 T-A.2; X8 |
| BR8 | The two outcomes are the two rules and not a judgement taken here: R-DEV-13 for a confirmed fraud and R-DEV-14 for a cleared one, with R-DEV-19 reopening the route decision | Business Rules and Routing Logic v4; FSD S8 A2.13; ASM-5164 |
| BR9 | The referral of INT-31 Aric is FEAT-ADM-13 in P4 and is not built, called or contracted here; the story holds and routes the case without it | Epics 3 to 8 Specification v3, INT-31 and FEAT-ADM-13; ASM-5165 |
| BR10 | No person name, address, contact value or identity number enters `rwb_deviation`, an event, a log or a workflow input | Template and Rules §R7.2 (s17); TSD S8 T6.2 |
| BR11 | The document number of the case and every other case fact are read through the rwb-case contract and never copied into `rwb_deviation` | DP-05 as a prohibition; ASM-5163 |

### 9. State transitions

The deviation states are those of TSD S8 T4 and the case moves are rwb-case's; this story computes the move and answers it, and the parent `CaseWorkflow` applies it (BR4).

| From (deviation) | Event | Condition | To | Written by |
|---|---|---|---|---|
| None, no row | `DEVIATION_FLAGGED` under R-UNI-08 and R-DEV-01 | `deviation_code` = X4 | One `deviation` row, `DEV_FLAGGED` answered | S8, in the raise transaction |
| `DEV_FLAGGED` | `OWNER_ASSIGNED` under R-DEV-04 | The fraud team is the named handler | `DEV_WITH_OWNER` | S8 on the row, rwb-case on the case |
| `DEV_FLAGGED` | `OWNER_ASSIGNED` under R-DEV-21 | The code has no owner | `DEV_WITH_OWNER`, logged as unmapped | S8, to the team manager |
| `DEV_WITH_OWNER` | `FRAUD_CONFIRMED` under R-DEV-13 | The fraud team confirms | `DEV_REROUTE`, the write-off route named | S8 on the row, S7 on the route |
| `DEV_WITH_OWNER` | `FRAUD_NOT_CONFIRMED` under R-DEV-14 | The fraud team clears the case | `DEV_REROUTE`, the collections decision named | S8 on the row |
| `DEV_WITH_OWNER` | `SLA_BREACHED` under R-DEV-20 | 10 working days elapse | `DEV_WITH_OWNER`, breach reported | S8, to the team manager |
| `DEV_REROUTE` | `ROUTE_REOPENED` under R-DEV-19 | Any outcome | `ROUTE_D6`; the deviation clears under R-DEV-18 | rwb-case and rwb-valuation |

| Clock | From the raise | At the outcome |
|---|---|---|
| Stage clock (P3) | Paused by the parent `CaseWorkflow` on the signal | Resumed under R-DEV-18 when the deviation clears |
| Prescription clock (P3) | Never paused, because the law does not pause | Never paused |
| Deviation service level (R-DEV-20) | A durable timer of the workflow, 10 working days | Stops with the outcome |

The `deviation.state` column carries the state name the rule names and no list of values is published for it (TSD S8 T3.2 publishes LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME only), so the state name is a rule fact and the missing vocabulary is recorded (ASM-5167).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-FRAUD, fraud investigator | Case record RU in TSD S8 T6.1 and right U of the two operations in the legacy permission table: the primary role, raising, assigning and recording the outcome of X4 |
| RW-CASEOWN, case owner | Case record CRU and right U: raises, assigns and records the outcome, and is the FSD's also-user (FSD S8 A2.13.3.3) |
| RW-TEAMMGR, team manager | Case record R: receives the escalation of R-DEV-20 and the unmapped code of R-DEV-21; right U is not held, so the team manager reads and escalates and does not raise |
| RW-SPECIAL, RW-COMPLAIN, RW-RESTRUCT, RW-LITOFF, RW-ENFORCE, RW-SALEOFF | Case record RU or R as the matrix gives them and right U of the legacy role list: may raise an X4 flag on a case they hold |
| RW-CONDUCT, RW-HEADLIT, RW-AUDIT, RW-RISK, RW-COE, RW-BIANAL, RW-TRIBE | Case record R: read the deviation and its record, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT | Case record R as the matrix gives them: the service identities run the workflow and are subject to the same checks |
| rwb-deviation service identity | Runs `DeviationWorkflow`, writes the record and the row, publishes the two events and answers the moves; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S8 T6.1 and the legacy permission table, and nothing wider. DP-08 is not in this story's pattern set: the capability area "Case record" and its right are declared per operation and the guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 | deviation (S8, `rwb_deviation`) | id | Write, the deviation reference of the row and of both events |
| DF-CAS-037 | deviation (S8, `rwb_deviation`) | case_id | Write, from the request and the case read |
| DF-CAS-038 | deviation (S8, `rwb_deviation`) | deviation_code | Write `X4`, from LOV-DEVIATION |
| DF-CAS-039 | deviation (S8, `rwb_deviation`) | raised_at | Write, the business date of the action |
| DF-CAS-040 | deviation (S8, `rwb_deviation`) | raised_by | Write, from LOV-RAISED-BY (`OFFICER`, `SCREENING_AGENT`, `RULE` or `CUSTOMER_CONTACT`) |
| DF-CAS-041 | deviation (S8, `rwb_deviation`) | paused_state | Write, the state the case was in, read from the rwb-case contract |
| DF-CAS-042 | deviation (S8, `rwb_deviation`) | handler_user_id | Write at the assignment from the answer of R-DEV-04; empty until then |
| DF-CAS-043 | deviation (S8, `rwb_deviation`) | contact_stop | Write `false` for X4: the contact stop of R-DEV-01 is the X1 to X3 path and belongs to those stories |
| DF-CAS-044 | deviation (S8, `rwb_deviation`) | cleared_at | Write at the outcome |
| DF-CAS-045 | deviation (S8, `rwb_deviation`) | outcome | Write `RE_ROUTED` at the outcome, from LOV-DEV-OUTCOME |
| Standard columns | deviation (S8, `rwb_deviation`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write, `state` = the state name of section 9, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_deviation`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the row and the state change |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and 20 more | Not read as a table and not written: the case state and the handler arrive on the rwb-case contract |
| DF-WRK-027 to DF-WRK-036 | timer (P3) | timer_type, started_at, expires_at, paused_at | Not read as a table and not written: the clocks arrive on the rwb-case timers read |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and 10 more | Not read as a table: the rule rows arrive on the package read |

Field IDs are those of TSD S8 T3.1 and the Logical Data Model and Data Dictionary, and the ACE and ledger rows are the rows the legacy Data table lists, with their owners changed to P3 and P7 by the target. **No new table, no new column and no migration**: `deviation` arrives with the DB story of this service, this story writes ten of its existing columns, and `decision_record`, `idempotency_key`, `outbox_event` and `inbox_event` are library objects created in `rwb_deviation` by the library's own migration (DP-03).

**No personal data.** The row carries identifiers, a code, a date, a state and a rule version. No name, address, contact value or identity number enters `rwb_deviation`, an event, a log or a workflow input, and the fixtures are synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). This story supplies the behaviour behind the two operations, whose shape RWB-S8-E7004-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/deviations` | DeviationRequest in, Deviation of status 200 out, the row and the state `DEV_FLAGGED` then `DEV_WITH_OWNER` by rule (API-S8-001) | Case record, right U, scope applied | `Idempotency-Key` header |
| PATCH | `/deviations/{deviationId}` | DeviationOutcome in, Deviation out, the outcome and the case move (API-S8-002) | Case record, right U, scope applied | Not applicable, as TSD S8 T-A.2 gives it; a repeat is answered 409 |

The errors are 401, 403 with MSG-P4-002, 404, 409 for a repeated raise or a conflicting outcome, 422 with MSG-GEN-001 and 503 when the library or a consumed contract does not answer, as TSD S8 T-A.2 gives them. The Ownership Map publishes these two operations and no `GET /deviations` and no clear operation, so this story provides no third operation (ASM-5168).

#### 12.2 REST operations consumed

| Operation | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3057; ASM-5163)) | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state, the paused state and the handler after each step; read only, faked |
| The timers read (operation name Not specified in the source documents (GAP-3057; ASM-5163)) | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The stage clock, the prescription clock and the deviation service level; read only, faked |
| The stage pause and resume signal (no REST path is published for it) | the parent `CaseWorkflow` on `rwb-case` | P3 rwb-case | The pause at the raise and the resume at the clear; on the workflow boundary it is the signal the parent applies; faked |
| The DEVIATIONS route set and the UNIVERSAL package in force (operation name Not specified in the source documents (GAP-3057; ASM-5162)) | `/api/recovery/decision/v1` | P7 rwb-decision | The 22 rules over 9 states with R-UNI-08, at their version; faked |
| The decision log of the case (operation name Not specified in the source documents (GAP-3057; ASM-5164)) | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The record and its central confirmation; read only, faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The five rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3057; ASM-5162, ASM-5163).

#### 12.3 Events published

| Event | Topic | Data | Consumers |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (EV-06 `DeviationRaised`) | `rwb.deviation.events.v1` with its retry and `.dlt` topics | `caseId`, `deviationCode`, `raisedBy`; no personal data | rwb-case, rwb-comms, rwb-treatment |
| `rwb.deviation.DeviationCleared.v1` (EV-07 `DeviationCleared`) | `rwb.deviation.events.v1` with its retry and `.dlt` topics | `caseId`, `deviationCode`, `outcome`; no personal data | rwb-case, rwb-comms, rwb-treatment |

The two events are the two published in TSD S8 T5.3 and in the event catalogue rows 06 and 07, and their target names follow the naming rule of §R4; the catalogue publishes the monolith names, not the target names (ASM-5164). Each row is written to the outbox in the same transaction as the `deviation` row and the record, and the relay publishes it as a CloudEvent (DP-09, ADR-015). The outbox and inbox library `RWB-PLT-TE006-CON` is the DP-09 dependency the plan does not carry for this key (ASM-5164).

#### 12.4 Events consumed

One subscription. The workflow listens to `rwb.case.CaseStateChanged.v1` on `rwb.case.events.v1`, the P3 event of the connection matrix row S8, so a case that leaves the paused state while the deviation is open is noticed and the resume point of R-DEV-18 is taken from the state of record rather than from a copy (ASM-5163). The inbox holds one processed row per event, so a replay changes nothing. The target event name follows the naming rule and is published in no source document (GAP-3057; ASM-5164). The events of rwb-payment and rwb-agent that the connection matrix gives row S8 belong to the other deviation stories.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per deviation, the child of `CaseWorkflow`, started at any time in the case, continues-as-new at each stage end | `rwb-deviation` in namespace `rwb-recovery` | Input: the case, the code, the reason and the raised-by value; signals: the assignment, the confirmed and the cleared outcome, the case state event. It pauses the stage timer through the parent and never the prescription timer |
| `EvaluateDeviationRules` | Activity | `rwb-deviation` | The case and the code in; the rule ID with its package version and the case move out |
| `RecordAndApplyDeviation` | Activity | `rwb-deviation` | The rule outcome in; the record, the `deviation` row, the outbox row and the case-move answer out, in one transaction |

No child workflow for the case exists in this service, and no workflow or activity name is a source value: the three names are a target design choice (ASM-5166).

#### 12.6 Schedules

None. The context pack gives S8 no job, and an X4 flag arrives as a request or an event and never on a cron; the service level of R-DEV-20 is a durable timer inside the workflow and not a job, which is why the clocks are read through the timers operation and never through a scheduler. No Quartz row and no shared job table is created by this story.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| deviation | S8 (`rwb_deviation`) | The deviation X1 to X7 raised on a case; this story inserts and updates the X4 rows and writes the columns of section 11 |
| decision_record | PLT library, created in `rwb_deviation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_deviation` | The key of the request and the answer it holds |
| outbox_event | PLT library, created in `rwb_deviation` | The row of the two published events (§12.3) |
| inbox_event | PLT library, created in `rwb_deviation` | The one processed row per consumed case event (§12.4) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6), `write_off` (S7) and the later stories' data. No foreign key leaves the schema and `case_id` is an identifier, not a reference (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | Case `RW-2026-001204` in `ANY_STATE`, then `DEV_FLAGGED`, then `DEV_WITH_OWNER` with the fraud team as the handler, then `DEV_REROUTE`, then `ROUTE_D6`; a case already closed | AC2, X4 |
| rwb-case timers fake | The stage clock paused and the prescription clock running; a pause refused because no timer runs | AC2, X4 |
| rwb-case pause and resume fake | The parent `CaseWorkflow` accepting the signal; a signal to a workflow that has ended | AC2 |
| rwb-decision package fake | The DEVIATIONS route set at its version in force with R-DEV-01 to R-DEV-21 and the UNIVERSAL package with R-UNI-08; an absent version | AC2, X5 |
| rwb-decision decision-log fake | The record of each action with its rule version and the central confirmation; a ledger that does not confirm | AC2, X1 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-06 and SCR-08 answers for the case, in their form, saved, loading and list states | AC2 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the consumed rows carry the placeholder until their owners confirm them (GAP-3057; ASM-5162, ASM-5163).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` on `/api/recovery/deviation/v1`; the case read and the timers read; one hop, 2 s |
| Kafka | 2 published, 1 consumed | `DeviationRaised` (EV-06) and `DeviationCleared` (EV-07) on `rwb.deviation.events.v1`; `rwb.case.CaseStateChanged.v1` on `rwb.case.events.v1` |
| Temporal | 1 workflow, 2 activities, 1 signal to the parent, 1 durable timer | `DeviationWorkflow`, `EvaluateDeviationRules`, `RecordAndApplyDeviation` and the R-DEV-20 service level on `rwb-deviation` |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.deviation`, module `x4`; front end `src/modules/recovery/deviation/RaiseDeviation.tsx` and `DeviationQueue.tsx`, the fragments SCR-06 and SCR-08 embed.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of every action: the record, the row and the state answer commit together or not at all. DP-13 moves the base of the two operations and nothing else. DP-19 is how SCR-06 and SCR-08 reach this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-05 (the ACE read), DP-09 (the outbox and inbox library) and DP-16 (the integration adapter for Aric) are real dependencies of this step that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3057; ASM-5162, ASM-5164, ASM-5165).

**Dependencies the tables add and the plan does not hold.** The five consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON`; the package is read as data and evaluated by this service's own evaluator, so no kit is declared. The outbox and inbox library of DP-09 would add `RWB-PLT-TE006-CON` and is needed for the two published events and the one consumed event. The access guard of DP-08 would add `RWB-PLT-E1037-CON` and `RWB-P4-E1037-CON`. The integration adapter of DP-16 would add `RWB-P2-E1007-CON` and is not needed while Aric is out of scope. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DeviationWorkflow` X4 branch | Workflow | Receives the flag, drives the assignment and the outcome, pauses the stage timer through the parent and runs the service-level timer |
| `EvaluateDeviationRules` | Activity | Evaluates R-UNI-08, R-DEV-01, R-DEV-04, R-DEV-13, R-DEV-14, R-DEV-19, R-DEV-20 and R-DEV-21 over the package in force |
| `RecordAndApplyDeviation` | Activity | Writes the record, the row, the outbox row and the case-move answer in one `rwb_deviation` transaction |
| `DeviationDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and the version before any change, hash-linked; refuses the step when the write fails |
| `DeviationRowWriter` | Repository | Inserts and updates the row with the idempotency row and the optimistic lock |
| `DeviationEventPublisher` | Outbox adapter | Writes the outbox row of the two events and lets the relay publish the CloudEvent |
| `CaseMoveAnswer` | Client | Answers rwb-case the move and the paused state, and signals the parent workflow |
| `CaseClient` | Client | The case read and the timers read of rwb-case, one hop, 2 s, breaker |
| `RulePackageClient` | Client | The DEVIATIONS route set and the UNIVERSAL package at their version in force |
| `DecisionLogClient` | Client | The decision log of the case and its central confirmation |
| `DeviationController` | Controller | The two operations, the capability area and right, the `Idempotency-Key` and the problem mapping |
| `RaiseDeviation`, `DeviationQueue` | React components | The form and saved states of SCR-06 and the loading and list states of SCR-08, with the refusal and not-recorded states |

**Database and migrations.** No Flyway file. `deviation` arrives with the DB story of this service, and the record, the idempotency key and the two event tables are library objects created in `rwb_deviation` by the library's migration (DP-03). No column is added for the case, the timers or the rule row: those are facts and rows of their owners and are referenced, not copied.

**Configuration and reference data.**

- The four lists `LOV-DEVIATION`, `LOV-RAISED-BY`, `LOV-DEV-OUTCOME` and the state names of section 9 are reference rows read with their version, never written in code (TSD S8 T3.2; ASM-5167).
- The 10-working-day service level of R-DEV-20 is a rule row of the package and not a constant.
- The capability area "Case record" and its right: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.

**Build steps**

1. The X4 branch of `DeviationWorkflow` and its input record, registered on `rwb-deviation` as the child of `CaseWorkflow`, with the raise as its start (AC2).
2. `RulePackageClient` against its fake, with the version in force recorded with every outcome, and the absent-version path (AC2, X5).
3. `CaseClient` and `CaseMoveAnswer` against their fakes, with the paused state, the two clocks and the pause and resume signal (AC2, X4).
4. `EvaluateDeviationRules` over the package, with the eight rules, the unmapped code of R-DEV-21 and the no-fire path (AC2, X7).
5. `DeviationDecisionRecordWriter` against the stub, with the failed-write path (AC2, X1).
6. `DeviationRowWriter` with the one transaction, the row, the idempotency row and the optimistic lock (AC2, X8).
7. `DeviationEventPublisher` and the two CloudEvents with their data, and the inbox row of the consumed case event (AC2, X8).
8. `DeviationController` with the rights, the `Idempotency-Key`, the problem mapping of the declared errors, and the two screen fragments through the composite route fake (AC2, X2, X3).
9. The service-level timer of R-DEV-20 and the escalation, then the boundary test: no statement outside `rwb_deviation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or `rwb_source_data` (X6, X9).

**Feature flag.** `rwb.deviation.x4-v1`, a flag of the platform library; off means the raise is refused with 503, nothing is written and the other six codes are unaffected.

**Done when.** The tests of section 16 pass, the X4 flow runs on the fakes in SIT through `DEV_FLAGGED`, `DEV_WITH_OWNER` and `DEV_REROUTE` on both outcomes, a forced record failure changes nothing, a repeated raise and a repeated outcome write once, no `recovery_case` or `timer` row and no `v_ace_*` read exists in the build, and the criteria of RWB-ITG-E7004-ITG pass against this service.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | The X4 deviation is raised, with the deviation and the handler the rule names (R-DEV-01, R-DEV-04) | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required field of the request is absent or invalid, or the code is outside LOV-DEVIATION (X3, VR-S8-013-1) | Enter {field}. |
| MSG-P4-002 | A role without the Case record right U calls an operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the row and the state change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set and of FSD S8 A2.13.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. The escalation of R-DEV-20 and the unmapped code of R-DEV-21 have no message ID in any source and are recorded as such (GAP-3057).

### 15. Screens and states

SCR-06 Raise deviation and SCR-08 Deviation queue are served through the gateway-bff composite route (DP-19). The route calls rwb-deviation for the deviation and its state, rwb-case for the case and its route state and rwb-decision for the record; this story fixes the rwb-deviation answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives SCR-06 as "Form; saved" and SCR-08 as "Loading; list". The form and saved states are this story's, and so is the list state of the open deviations with their handler and their age against the service level. The refusal, not-recorded and re-routed states read the messages of section 14. The queue shows the handler and the service level; it shows no contact-stop flag for X4, because the contact stop of R-DEV-01 covers X1 to X3.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-004-01 | The X4 success path as legacy AC1 states it; ITG AC1 to AC5 assert it across the services | Component | Case `RW-2026-001204` with the package in force and no open deviation; the raise, the assignment, both outcomes and the moves asserted on the fakes |
| TC-E7-004-02 | AC2 | Component | The rwb-decision decision-log fake and the decision-record stub refusing; nothing written and MSG-P7-003 shown |
| TC-E7-004-03 | Access | Component | A role without the Case record right U; 403 with MSG-P4-002 and no read |
| TC-E7-004-04 | Principle 5 | Component | A forced decision log write failure inside the raise transaction; no `deviation` row, no outbox row and no state answer |

The four legacy cases are those of RWB-E7-004 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to RWB-ITG-E7004-ITG.

### 17. Guardrails

- No business value in code: the codes, the raised-by list, the outcome list, the state names, the service level and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch.
- No personal data in `rwb_deviation`, in an event, in a workflow input or in a log: identifiers, a code, a date, a state and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR11).
- The case and the two clocks stay with rwb-case: no `recovery_case` row, no `timer` row and no case route-state column here (BR4).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No referral of Aric is built, called or contracted here, and no Aric endpoint, topic or status word is invented (BR9).
- No retired element is reintroduced: no Quartz job row, no shared job table, no monolith base, no data-lake extract.
- The decision is recorded before the change; a build that writes a row outside the record's transaction fails the review (DP-03).
- Every action is exactly once: a build that writes a second row or a second event on a repeat fails the idempotency test (BR7).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S8-001 | Each of X1 to X7 runs end to end with its own flow, approver, contact rules and return point (FSD S8 Requirements served) | The X4 flow through the three states and the two outcomes | TC-E7-004-01 |
| REQ-DVH-010 | A fraud flag refers the case to the fraud team and holds recovery action until it is confirmed or cleared (FSD S8 Requirements served) | The hold, the fraud handler and the outcome | TC-E7-004-01 |
| REQ-DVH-002 | A deviation pauses the stage clock, keeps the prescription clock running and does not replace the case state | The pause and resume signal to the parent | TC-E7-004-01 |
| ADR-013 | 19 services inside ACE | rwb-deviation as the owner of the deviation | TC-E7-004-01 |
| ADR-014 | Schema and login per service | `rwb_deviation` and its own login | TC-E7-004-01 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The two published events and the consumed case event | TC-E7-004-01 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The child workflow, the durable timer and no Schedule | TC-E7-004-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two provided and the two consumed rows | TC-E7-004-01 |
| ADR-022 | Local decision record plus central ledger | The record written before the change | TC-E7-004-02, TC-E7-004-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-004, disposition Split (rework); feature FEAT-DVF-04 |
| Legacy criteria | AC2, owned word for word by this story; AC1 owned word for word by RWB-ITG-E7004-ITG |
| Source text | Legacy RWB-E7-004; FSD S8 Deviation handling v3 A2.13 and Requirements served; TSD S8 Deviation handling v2 T2, T3, T4, T5.3, T6 and T-A; Business Rules and Routing Logic v4 rows R-UNI-08 and R-DEV-01 to R-DEV-21; Epics 3 to 8 Specification v3, FEAT-DVF-04 and INT-31 |
| Test cases | TC-E7-004-01 to TC-E7-004-04 |
| Feature and screens | FEAT-DVF-04, SCR-06 Raise deviation, SCR-08 Deviation queue |
| Rules | R-UNI-08 and R-DEV-01, R-DEV-04, R-DEV-13, R-DEV-14, R-DEV-19, R-DEV-20, R-DEV-21, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the two operations, the elements, the field IDs, the consumed rows, the events as contract, the error set and the fakes: RWB-S8-E7004-CON.
- The legacy success criterion AC1 and the end-to-end proof across the real services: RWB-ITG-E7004-ITG.
- The Aric referral of INT-31 and FEAT-ADM-13: P4's story in Epic 8; no Aric operation is built or called here (ASM-5165).
- The case of record, its route states, the parent `CaseWorkflow` and the two clocks: rwb-case (P3).
- The write-off route of R-DEV-13: rwb-writeoff (S7). The route decision D6 of R-DEV-19: rwb-valuation (S1).
- The screening of FEAT-DVH-04 and the agent path: the screening and agent stories of this service.
- The other six deviation codes X1, X2, X3, X5, X6 and X7 and their own flows, contact stops and approvers: the sibling stories of this epic.
- The gateway-bff composite route and the screen field lists of SCR-06 and SCR-08: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
