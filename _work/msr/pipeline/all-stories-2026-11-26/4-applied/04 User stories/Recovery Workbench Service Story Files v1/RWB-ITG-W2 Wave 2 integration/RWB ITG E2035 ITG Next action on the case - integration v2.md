# RWB-ITG-E2035-ITG Next action on the case

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-035 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E2035-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2035-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-035 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E1018-APP, RWB-P3-E1031-APP, RWB-P3-E2042-APP, RWB-P2-E2035-APP, RWB-P4-E2035-APP, RWB-P3-E2035-APP, RWB-P7-E2035-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-WKM-012, REQ-WKM-013, REQ-WKM-016, REQ-WKM-014, REQ-WKM-015) |
| Status | Draft (realignment v1) |

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness that reads the next action of a case, its owner, its due date and the rule package version that set it through gateway-bff and the owning services**, so that **the wave 2 next action journey is proven end to end, with evidence, before the release is accepted**.

This story builds the harness and the evidence only. It builds no production screen, endpoint, table, workflow or schedule, it serves no operation, it owns no table and it starts no workflow. The real behaviour is owned by the I stories RWB-P3-E2035-APP (the next action fields, the timer resolver, the check and the panel of the case), RWB-P2-E2035-APP (the next action assigner and the case list export the legacy story carried in the P2 backlog), RWB-P7-E2035-APP (the RESTRUCTURE package registry, the rule catalog rows and the decision log), RWB-P4-E2035-APP (the role name and role class of the next action owner) and RWB-P3-E1018-APP, RWB-P3-E1031-APP and RWB-P3-E2042-APP (the case transitions, the case list and the RESTRUCTURE rows in force), and those seven stories block the ITG run.

The fourteen acceptance criteria of the legacy story stay with the APP stories that own them; this story owns none of them and restates none of them.

### 2. Business rationale

The legacy RWB-E2-035 journey crosses more than one service: rwb-case holds the case, its state, its owner, its queue, the next action fields and the case list; rwb-decision holds the RESTRUCTURE rule package, the rule catalog row and the central decision ledger; rwb-access holds the Recovery roles as data, with the name and the class of the role that owns the next action; and rwb-integration holds the file runs and outbound items through which the case list export leaves the bank. Until the real services are exercised together through the gateway, the program cannot show that no case waits with nobody owing anything on it, which is the measure the legacy story sets: the count of active cases with no next action, with a target of zero.

The harness gives one repeatable run per business date that proves the composite route composes the next action from those owners one hop at a time inside the 2 s budget, that the action text, the owner role and the timer of the firing rule R-RES-04 of package version "RES-2026.12" are read from the catalog row and not held by the harness, that a wait for CU-BORROW on rule R-SET-13 is a valid next action, that the case list carries the next action, its owner and its due date with the overdue marker on 16 December 2026, that a case with no due date raises the warning MSG-P2-023 and one exception task, that NoPackageInForce is a refusal and never an empty next action, and that a repeated transition changes nothing. It meets REQ-WKM-012, REQ-WKM-013, REQ-WKM-016, REQ-WKM-014 and REQ-WKM-015 at the integration level and leaves every business rule, every message and every screen behaviour where the owning stories put them.

### 3. Preconditions

- The seven I stories are published and deployed in the SIT environment: RWB-P3-E1018-APP (case transitions), RWB-P3-E1031-APP (case list), RWB-P3-E2042-APP (the RESTRUCTURE route-set rows in force), RWB-P2-E2035-APP (next action assigner and the case list export), RWB-P4-E2035-APP (role name and role class), RWB-P3-E2035-APP (next action fields, timer resolver, check and panel) and RWB-P7-E2035-APP (rule package registry, rule catalog row and decision log).
- gateway-bff is deployed with the composite route of DP-19 available. The gateway-bff composite next-action route path, its merge order and its call list: Not specified in the source documents (GAP-0418; ASM-0593).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness can run green from Day 1 before the I stories land.
- Package version "RES-2026.12" of code RESTRUCTURE is in force from 2026-12-01 and holds rule R-RES-04, which moves IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER with action "Assign the case to a restructuring officer and start the offer clock", owner role RW-RESTRUCT and timer "2 working days", and rule R-SET-13, which moves WITH_OPS_SETTLEMENT on SETTLEMENT_BOOKED to AWAITING_PAYMENT with action "Set the payment due date and wait for the money", owner role CU-BORROW and timer "payment due 30 days" (RWB-E2-042; RWB-E1-073).
- The service levels and timers table holds 5 working days for each state of the route sets in force until the DL22 values are loaded, and the bank holiday list holds 31 December 2026 and 1 January 2027 (configuration key rwb.calendar.bank-holidays, loaded by RWB-E1-042).
- The roles RW-CASEOWN, RW-TEAMMGR, RW-COE, RW-REFADM and RW-RESTRUCT are loaded with their class by RWB-P4-E2035-APP; the harness reads them and holds no copy.
- The harness repository and environment, its test-data seeding, and its evidence format and retention: Not specified in the source documents (GAP-0418; ASM-0593).

### 4. Flow

1. Harness: seeds the cases, the queues, the roles, the service levels and timers rows, the bank holiday list and package version "RES-2026.12" through the owning contracts or the published fakes, and reads each object back to assert the seeded state.
2. Harness: calls the gateway-bff composite next-action route for case RW-2026-000401 and asserts the answer is composed from rwb-case, rwb-decision, rwb-access and rwb-integration, one hop per source inside the 2 s budget, with one trace in the run report.
3. Harness: drives the move of RW-2026-000402 through the case contract on business date 2026-12-11, asserts that rule R-RES-04 of version "RES-2026.12" fired and that the case holds its action text, owner role RW-RESTRUCT, rule ID and version and due date 15 December 2026, written in the same transaction as the move to WITH_FCR_OFFICER.
4. Harness: reads the catalog row of R-RES-04 through the rwb-decision contract and asserts the action text, the owner role and the timer it returns are the ones on the case, so the harness holds no copy of any business value.
5. Harness: opens the waiting case RW-2026-000403 moved by R-SET-13 on 14 December 2026 and asserts the waiting text with owner CU-BORROW, the wait end and the waiting flag.
6. Harness: reads the case list on 16 December 2026 and asserts the next action, next action owner and due date columns, that RW-2026-000401 is marked Overdue and RW-2026-000403 is not, and that RW-2026-000404 carries the missing-action warning MSG-P2-023 with one NEXT_ACTION_MISSING task on the exception queue.
7. Harness: reads the case list export as an outbound item of rwb-integration and asserts the four next action columns on the export row.
8. Harness: forces each failure of §5 through the fakes, asserts the message and that nothing was written, then returns the fake to its healthy answer.
9. Harness: drives the no-version case on 2027-01-04 and asserts NoPackageInForce with MSG-P3-027 and no next action from that move; repeats the transition with decision log entry DLE-SYN-0402 and asserts the next action and the due date are unchanged with no second task.
10. Harness: writes one run report per business date, keyed by story and business date; the report format and retention are Not specified in the source documents (GAP-0418; ASM-0593).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | The timer spec of the firing rule is "None" or has no fixed duration | The due date is taken from the service levels and timers row of the to_state (5 working days in the seeded table), and the owner shown is the case owner when the role is the role of the case queue | None | TC-E2-035-05-ITG |
| X2 | No due date can be found from the rule or the table | The case keeps the action and the owner of R-DEV-05 with no due date, one NEXT_ACTION_MISSING task is raised for role RW-TEAMMGR of the case team, and the case record shows the warning | MSG-P2-023 | TC-E2-035-06-ITG |
| X3 | The due date falls on a weekend or on a bank holiday | Working days skip Saturday, Sunday and the holiday list, so the move of 30 December 2026 gives the due date of 5 January 2027 | None | TC-E2-035-07-ITG |
| X4 | The case closes | The next action fields are empty, the open NEXT_ACTION_MISSING task is cancelled, and the case leaves the list of active cases with no next action | None | TC-E2-035-08-ITG |
| X5 | The same transition is delivered twice with decision log entry DLE-SYN-0402 | The next action and the due date are unchanged and no second task exists; the repeated read returns the same answer with one trace | None | TC-E2-035-09-ITG |
| X6 | Two transitions of one case commit against version 7 at the same time | One commits and the other is refused and retried against version 8, and the next action is that of the rule committed last | MSG-GEN-004 | TC-E2-035-10-ITG |
| X7 | A case opened before the switch-on has no next action | The check fills the three cases of the seed from the latest state change in the decision log, with the text read from the catalog row of R-RES-04 of version "RES-2026.12" | None | TC-E2-035-11-ITG |
| X8 | The timer of the rule is "same day" | The due date is the business date of the move | None | TC-E2-035-12-ITG |
| X9 | The reader holds RW-REFADM and no role with Case record R | The direct call answers 403 and no next action data is returned; the composite route does not return the action either | MSG-P4-002 | TC-E2-035-13-ITG |
| X10 | No RESTRUCTURE package version is in force on the business date 2027-01-04 | The answer is NoPackageInForce for the package in force check, the move is refused, and the case keeps its state and holds no next action from that move | MSG-P3-027 | TC-E2-035-14-ITG |
| X11 | The case is outside the reader's scope | The case is not in the case list rows and the direct call answers 404 with no next action data | MSG-P4-003 | TC-E2-035-04-ITG |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the seven I stories are deployed; until then it runs against the §12.8 fakes |
| Negotiable | The harness pack, the data seeding and the evidence format are agreed with QA; no business value is fixed by the harness |
| Valuable | The next action, its owner, its due date and the package version that set it are evidenced across services rather than per service |
| Estimable | One harness project, one journey specification, one fake pack and one run report |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each scenario of §7 is one automated journey with synthetic data and a machine-checkable result |

### 7. Acceptance criteria

```gherkin
Feature: Next action on the case - wave 2 integration harness

  Background:
    Given the business date is 2026-12-15
    Given RESTRUCTURE package version "RES-2026.12" is in force and holds rule R-RES-04, which moves IN_FCR_QUEUE on CASE_PICKED_UP to WITH_FCR_OFFICER with action "Assign the case to a restructuring officer and start the offer clock", owner role RW-RESTRUCT and timer "2 working days"
    Given the same version holds rule R-SET-13, which moves WITH_OPS_SETTLEMENT on SETTLEMENT_BOOKED to AWAITING_PAYMENT with action "Set the payment due date and wait for the money", owner role CU-BORROW and timer "payment due 30 days"
    Given the bank holiday list holds 31 December 2026 and 1 January 2027
    Given case "RW-2026-000401" with status IN_PROGRESS was moved by R-RES-04 on 2026-12-11 and holds due date 15 December 2026
    Given case "RW-2026-000403" was moved by R-SET-13 on 14 December 2026

  Scenario: AC1 The composite next-action route through gateway-bff (new, D-RCV-60)
    Given the harness calls the composite next-action route at "Not specified in the source documents (GAP-0418; ASM-0593)" for "RW-2026-000401"
    When gateway-bff composes the answer from rwb-case, rwb-decision, rwb-access and rwb-integration
    Then the route returns action "Assign the case to a restructuring officer and start the offer clock", owner "Restructuring officer (FCR)", due date 15 December 2026, rule "R-RES-04" and package version "RES-2026.12"
    And every call in the composition is one hop with the 2 s budget
    And no service reads another service's schema
    And the run report holds one trace spanning the gateway and each owning service

  Scenario: AC2 The rule sets the action, the owner, the due date and the package version (new, D-RCV-60)
    Given case "RW-2026-000402" stands in state IN_FCR_QUEUE
    When event CASE_PICKED_UP fires R-RES-04 on Friday 2026-12-11
    Then the catalog row read through the rwb-decision contract returns the action text, owner role RW-RESTRUCT and timer "2 working days"
    Then the case holds that action, owner role RW-RESTRUCT, rule "R-RES-04", package version "RES-2026.12" and due date 15 December 2026
    Then the values are written in the same transaction as the move to WITH_FCR_OFFICER
    When the harness opens the waiting case "RW-2026-000403" moved by R-SET-13
    Then the next action reads "Waiting for Customer (borrower): Set the payment due date and wait for the money"
    Then the wait ends on 13 January 2027 and the waiting flag is true
    And the owner role CU-BORROW and the package version "RES-2026.12" are on the answer

  Scenario: AC3 The list columns, the overdue marker and the missing-action warning (new, D-RCV-60)
    Given the harness reads the case list through gateway-bff on 16 December 2026
    Then next action, next action owner and due date are columns of every row
    Then row "RW-2026-000401" is marked Overdue and row "RW-2026-000403" is not
    Then the row of "RW-2026-000403" carries the waiting text of CU-BORROW
    Then the row of case "RW-2026-000404" carries the warning MSG-P2-023, no due date, and one NEXT_ACTION_MISSING task for role RW-TEAMMGR on the exception queue
    Then each row is composed from rwb-case for the case and the next action, from rwb-access for the owner role name and class, and from rwb-decision for the rule ID and the package version, with no cross-schema read
    Then the export row of the same case list, read as an outbound item of rwb-integration, carries the same four next action columns
    Given case "RW-2026-000402" belongs to a team outside the reader's scope
    When the harness calls its next action directly
    Then the answer is 404 with MSG-P4-003 and no next action data is returned

  Scenario: AC4 Failure isolation, no package in force and the idempotent repeat (new, D-RCV-60)
    Given the role read of rwb-access does not answer within 2 s
    When the harness continues the run with the other cases of the same business date
    Then the failing call writes nothing, the answer names no next action owner rather than a stale one, and the run records the failure against rwb-access only
    And every other case of the run is asserted and reported, so one slow source does not fail the journey
    Given no RESTRUCTURE package version is in force on 2027-01-04
    When event CASE_PICKED_UP fires for case "RW-2026-000407" on 2027-01-04
    Then the answer is NoPackageInForce for the package in force check with MSG-P3-027
    Then the move is refused and the case keeps its state and holds no next action from that move
    Given case "RW-2026-000402" was moved by R-RES-04 on 2026-12-11 with decision log entry "DLE-SYN-0402"
    When the same transition with "DLE-SYN-0402" is processed again
    Then the next action and the due date are unchanged, no second task exists and the repeated read returns the same answer with one trace
    Given user "U-REF-01" holds RW-REFADM and no role with Case record R
    When they read the next action directly
    Then the answer is 403 with MSG-P4-002 and no next action data is returned
```

These four criteria are new for the ITG harness and do not restate the app criteria owned by the I stories; legacy AC1 to AC14 of RWB-E2-035 stay with RWB-P2-E2035-APP and the secondary APP stories of the same legacy key.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | On every move, the next action text, the owner role and the rule ID come from the catalog row of the firing rule: the catalog read returns action_text, owner_role and timer_spec for the rule ID and the package version | FEAT-CWC-28; REQ-WKM-013; D-RCV-36 T6 |
| BR2 | The next action is never entered by a person | REQ-WKM-013 |
| BR3 | timer_spec "n working days" adds n working days; "n days" with any label before it adds n calendar days; "same day", "Same day" and "immediate" give the date of the move; "next working day" adds 1 working day | rule_row.timer_spec through the rwb-decision contract |
| BR4 | Any other timer_spec, including "None", takes the time for the to_state from the service levels and timers table | DL22 |
| BR5 | The next action is a wait when the owner role is of class Customer party or Partner user; the text starts "Waiting for {owner}:" | role.role_class |
| BR6 | A next action is overdue when its due date is earlier than today and the case is not closed | REQ-WKM-012 |
| BR7 | An active case with no due date or no next action raises one NEXT_ACTION_MISSING task to the team manager | REQ-WKM-016 |
| BR8 | Working days are Monday to Friday, excluding the dates in the bank holiday list | Configuration key rwb.calendar.bank-holidays |
| BR9 | When the owner role is the role of the case's queue, the owner shown is the case owner; otherwise the role name | queue.role_code |
| BR10 | The rule version is the package version label of the rule result, and the next action records the version of the move that set it; a later version does not rewrite an action already set | D-RCV-36 T5, T7; R-UNI-38 |
| BR11 | No RESTRUCTURE version in force is a refusal (NoPackageInForce), never a default move and never an empty next action | D-RCV-36 T3; R-UNI-41 |

The harness asserts these eleven rules against the owning services and re-implements none of them, so no BR row is changed by this story.

### 9. State transitions

None. The harness changes no case status, route state or stage clock, and it writes no next action field, no task and no decision record itself. The table is what it observes on the case after a call to the owning service.

| Observed on the case | Before the call | After a successful move | After a refusal |
|---|---|---|---|
| next action text, owner role, due date, rule ID, package version | the values of the previous move | the values of R-RES-04 of package version "RES-2026.12" | unchanged |
| next action waiting | false | true when the owner role is CU-BORROW under R-SET-13 | unchanged |
| exception task | none | one NEXT_ACTION_MISSING for role RW-TEAMMGR when no due date exists | none |
| status, route state, queue, owner | IN_PROGRESS, IN_FCR_QUEUE, and the queue and owner of the case | the to_state and the transition of the owning rule, with the next action in the same transaction | unchanged |

A failed or refused call leaves every row exactly as it was before the call.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | The synthetic user the harness drives: reads the next action of cases in scope (Case record R) |
| RW-TEAMMGR, team manager | Reads the case list and works NEXT_ACTION_MISSING tasks on the exception queue (Case record R; Queue and allocation RU) |
| RW-COE, centre of excellence analyst | Owns the action, owner and timer columns of the rule rows (Rules and parameters CRUD); the harness reads the rows it set and changes none |
| RW-REFADM, reference data administrator | Loads the service levels and timers table and the bank holiday list; the user U-REF-01 of the access case holds RW-REFADM and no role with Case record R |
| SY-CASEWF, case workflow module | Writes the next action fields and the exception task (Case record U; Queue and allocation C); the harness asserts its result, it does not act for it |
| SY-RULES, Drools evaluator | Evaluates the RESTRUCTURE package and serves the catalog row of the firing rule |
| No approval applies | The journey takes no decision |

Authorisation is answered by rwb-access through the role data read of §12.2, and the refusal of a role without Case record R is asserted by the harness on the owning service's answer.

### 11. Data

The harness owns no table. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through rwb-case contract |
| DF-CAS-005 | recovery_case | status | Read through rwb-case contract |
| DF-CAS-007 | recovery_case | route_state | Read through rwb-case contract |
| DF-CAS-009 | recovery_case | owner_user_id | Read through rwb-case contract |
| DF-CAS-010 | recovery_case | queue_id | Read through rwb-case contract |
| DF-CAS-011 | recovery_case | team_code | Read through rwb-case contract |
| DF-CAS-022 | recovery_case | closed_date | Read through rwb-case contract |
| DF-CAS-049 | recovery_case | next_action_text | Read through rwb-case contract |
| DF-CAS-050 | recovery_case | next_action_owner_role | Read through rwb-case contract |
| DF-CAS-051 | recovery_case | next_action_due_date | Read through rwb-case contract |
| DF-CAS-052 | recovery_case | next_action_rule_id | Read through rwb-case contract |
| DF-CAS-053 | recovery_case | next_action_waiting | Read through rwb-case contract |
| DF-WRK-005 | queue | role_code | Read through rwb-case contract |
| DF-WRK-017 to DF-WRK-026 | task | all fields | Read through rwb-case contract |
| DF-REF-002 | rule_row | rule_id | Read through rwb-decision contract |
| DF-REF-003 | rule_row | rule_version | Read through rwb-decision contract |
| DF-REF-008 | rule_row | action_text | Read through rwb-decision contract |
| DF-REF-009 | rule_row | to_state | Read through rwb-decision contract |
| DF-REF-010 | rule_row | owner_role | Read through rwb-decision contract |
| DF-REF-011 | rule_row | timer_spec | Read through rwb-decision contract |
| DF-REF-281 | rule_package_version | version_label | Read through rwb-decision contract |
| DF-REF-282 | rule_package_version | status | Read through rwb-decision contract |
| DF-REF-036 | role | role_name | Read through rwb-access contract |
| DF-REF-037 | role | role_class | Read through rwb-access contract |
| DF-DEC-004 | decision_log_entry | rule_id | Read through rwb-decision contract |
| DF-DEC-005 | decision_log_entry | rule_version | Read through rwb-decision contract |

The rule row and the package version are read only through the rwb-decision contract; the harness reads no workbook, no drl_source and no rule_row row directly. The role name and class are read only through the rwb-access contract. Test data is synthetic. No production case, party or task is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness calls the owning services; it serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}/next-action` | P3 rwb-case | The next action text, owner, due date, waiting flag, overdue and missing flags, rule ID and package version |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case status, route state, owner, queue, team and closure date after the move |
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | The case list rows with the next action, next action owner, due date and overdue marker |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The latest state change of a case with its rule ID and rule version |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The RESTRUCTURE version in force on the business date and its status |
| GET | `/api/recovery/decision/v1/admin/rule-versions` | P7 rwb-decision | The catalog row of the firing rule: action text, owner role and timer spec (D-RCV-36 T6) |
| GET | `/api/recovery/access/v1/admin/roles` | P4 rwb-access | The name and the class of the owner role, used for the waiting text and the owner shown |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | The case list export file run and its outbound item, which carry the four next action columns |

The composite screen route itself is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path, merge order and call list are Not specified in the source documents (GAP-0418; ASM-0593).

#### 12.3 Events published

None. The harness produces no event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.case.CaseStateChanged.v1 | rwb.case.events.v1 | P3 rwb-case | One event per move, keyed by caseId, in the same transaction as the next action fields |
| rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | P7 rwb-decision | Package version "RES-2026.12" is announced in force for the business date 2026-12-11, and no version is in force on 2027-01-04 |
| rwb.decision-record.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 rwb-decision (ledger); every service publishes its own record | The record of the move names rule R-RES-04 and package version "RES-2026.12" and reaches the central ledger within 5 minutes |
| rwb.integration.FileDelivered.v1 | rwb.integration.events.v1 | P2 rwb-integration | The case list export file carrying the next action columns is delivered once for the business date |

The events are consumed for assertion only; order per case is guaranteed by the case key on the topic, and the harness reads the case, the ledger and the outbound item through the owning contracts rather than from a topic.

#### 12.5 Workflows and activities

None added. The harness starts no workflow and adds no activity; it drives REST only and observes the transition of the case through the case contract. The check that the legacy story ran as JOB-05 is a durable timer inside the case workflow in the target design, and the harness asserts its result on the case, not the timer itself.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow.

#### 12.7 Tables owned

None.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-case | cases/{caseId}/next-action, cases/{caseId}, cases | RW-2026-000401 IN_PROGRESS moved by R-RES-04 on 2026-12-11 with due date 15 December 2026; RW-2026-000403 moved by R-SET-13 on 14 December 2026 with the waiting text and wait end 13 January 2027; RW-2026-000404 with no due date and one NEXT_ACTION_MISSING task for RW-TEAMMGR; RW-2026-000407 with no move on 2027-01-04; a case of another team for the scope case; 403 with MSG-P4-002 for a role without Case record R; 404 with MSG-P4-003 for a case outside scope |
| rwb-decision | decision-log, admin/rule-packages/{packageCode}/versions, admin/rule-versions | RESTRUCTURE version "RES-2026.12" in force from 2026-12-01 with rows R-RES-04 and R-SET-13 and their action text, owner role and timer; R-RES-03 with timer "None"; R-RES-07 with timer "same day"; R-DEV-05 with timer "deadline driven"; decision log entry DLE-SYN-0402; no version in force on 2027-01-04; a forced failure for the failure isolation case |
| rwb-access | admin/roles | Role name "Restructuring officer (FCR)" and class for RW-RESTRUCT; role class Customer party for CU-BORROW; the roles of RW-CASEOWN, RW-TEAMMGR, RW-COE and RW-REFADM; a slow answer beyond 2 s for the failure isolation case |
| rwb-integration | admin/outbound-items | The case list export file run of the business date with one outbound item carrying the next action, next action owner, due date and overdue columns; a cleared answer for every other case |

The fakes are published from the owning services' OpenAPI documents and are replaced by the real service as each I story lands, contract by contract. The harness repository and its environment: Not specified in the source documents (GAP-0418; ASM-0593).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Eight consumed operations of §12.2 through gateway-bff and the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes rwb.case.CaseStateChanged.v1, rwb.decision.RulePackageInForce.v1, rwb.decision-record.DecisionRecorded.v1 and rwb.integration.FileDelivered.v1; publishes nothing |
| Temporal | No | Starts no workflow and adds no activity or Nexus operation; it observes the case transition and the durable timer of the case workflow |
| File | No | The case list export is asserted as an outbound item through the rwb-integration contract; the harness reads and writes no file itself |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list. The blocking dependencies of this story are the seven I stories.

DP-10 applies because the legacy check ran as JOB-05 on Quartz; in the target design the check is a durable timer inside the case workflow and the shared Quartz and job tables are no longer used. DP-14 applies because the legacy topics were named after the monolith module; the events the harness reads are on the owner's topic. DP-05 applies to the case and the account facts the case list carries; the harness reads them through the rwb-case contract and no service reads an ACE view for this journey except rwb-source-data.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs one journey per business date, keyed by story and business date, and stops at the first failed assertion with the trace |
| NextActionClient | Harness adapter | Calls the composite next-action route and the eight consumed operations of §12.2 through gateway-bff |
| FakePack | WireMock project | Serves rwb-case, rwb-decision, rwb-access and rwb-integration from the published OpenAPI documents of §12.8 |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference found in the trace, so a service never reads another service's tables |
| CatalogFidelityCheck | Assertion | Compares the action text, the owner role, the timer, the rule ID and the package version on the case with the catalog row read through the rwb-decision contract, and fails the run on a difference |
| DueDateCheck | Assertion | Recomputes the working-day arithmetic from the timer spec, the service levels row and the holiday list, and fails the run when the due date on the case differs |
| IsolationCheck | Assertion | Fails the run when one slow or failed source stops another case of the same run, or when a failed call wrote anything |
| RunReportWriter | Reporter | Writes one run report with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0418; ASM-0593) |

**Environment and test data**

- Environment: SIT, one namespace, the seven I stories deployed from their wave 2 builds or replaced by the §12.8 fakes. Harness repository, environment and data seeding: Not specified in the source documents (GAP-0418; ASM-0593).
- Data: synthetic cases RW-2026-000401, RW-2026-000402, RW-2026-000403, RW-2026-000404 and RW-2026-000407; package version "RES-2026.12" with rows R-RES-04, R-SET-13, R-RES-03, R-RES-07 and R-DEV-05; owner roles RW-RESTRUCT, CU-BORROW, RW-CASEOWN, RW-TEAMMGR, RW-COE and RW-REFADM; the service levels row of 5 working days; the holiday list of 31 December 2026 and 1 January 2027; the business dates 2026-12-11, 2026-12-15, 2026-12-16 and 2027-01-04; decision log entry DLE-SYN-0402. No production record is copied.
- Reset: each run starts from the seeded state, so a repeated run is deterministic and the same report is produced.

**Build steps**

1. Build JourneyRunner and NextActionClient against the published OpenAPI documents of the owning services.
2. Publish FakePack for the four owning services from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Add the composite route assertion of AC1, including the four sources, the one-hop check, the 2 s per-call budget, the single trace and the SchemaBoundaryCheck.
4. Add the rule-set journey of AC2 with CatalogFidelityCheck and DueDateCheck: the action, the owner, the due date and the package version of R-RES-04, and the waiting case of R-SET-13.
5. Add the list assertion of AC3: the columns, the overdue marker, the waiting text, the missing-action warning with its task, the export outbound item and the scope refusal.
6. Add the failure isolation, the no-version refusal and the idempotent repeat of AC4, then replace each fake with the real service as its I story lands and publish the run report per business date; the gate definition: Not specified in the source documents (GAP-0418; ASM-0593).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switch it exercises is `rwb.casewf.next-action` from the legacy solution plan, with `rwb.p3.drools` on the evaluation path; with the next-action flag off the assigner is not called, the check does not run and the panel and the columns are hidden, and with `rwb.p3.drools` off every move is refused with MSG-P3-027. The harness asserts the disabled and the enabled state of both.

**Done when:** the journey runs green against the seven deployed I stories in SIT, the run report for the business date holds every assertion of §7 and §16 with its trace, the next action of every case in the run matches the catalog row and its package version, and the pass/fail gate agreed with QA is met for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-023 | The case has no next action or no due date | This case has no next action. It is on the exception list for {team}. |
| MSG-P3-027 | No RESTRUCTURE version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-GEN-004 | A transition commits against a changed version | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role lacks Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |

The harness asserts the message ID and the substituted values; it does not own the message text. For MSG-P3-027 in this journey {check} is "package in force" and {detail} names the package code RESTRUCTURE and the business date only. For MSG-P2-023 {team} is the team code of the case. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-03 Case record | Read only, Editable, On hold | The header answer carries the next action, its owner, its due date and the rule ID with its package version; a wait shows the waiting text and the wait end date; an overdue action carries the overdue marker; a missing action carries MSG-P2-023 |
| SCR-02 Case list | List | The rows carry the next action, next action owner and due date columns, the overdue marker on RW-2026-000401 and no marker on RW-2026-000403 |
| SCR-09 Exception queue | List | The NEXT_ACTION_MISSING task of RW-2026-000404 is listed for role RW-TEAMMGR of the case team |

The harness opens no screen and renders no page; it asserts the composite route answer that the screen consumes, together with the outbound item of the case list export. Screen-level behaviour remains with the owning APP stories. The harness environment and evidence detail: Not specified in the source documents (GAP-0418; ASM-0593).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-035-01-ITG | legacy AC1, BR1, BR9, BR10; ITG AC1 | Integration | Case moved by R-RES-04 on 11 December 2026; four sources in one trace |
| TC-E2-035-02-ITG | legacy AC2, BR1, BR2, BR3, BR10; ITG AC2 | Integration | CASE_PICKED_UP on Friday 11 December 2026 with package version RES-2026.12 |
| TC-E2-035-03-ITG | legacy AC3, BR5; ITG AC2 | Integration | Case moved by R-SET-13 on 14 December 2026; owner role CU-BORROW |
| TC-E2-035-04-ITG | legacy AC4, BR6; ITG AC3 | Integration | Two cases read on 16 December 2026; one case outside scope |
| TC-E2-035-05-ITG | legacy AC5, BR4, BR9; ITG AC2 | Integration | R-RES-03 with timer None; service levels row of 5 working days |
| TC-E2-035-06-ITG | legacy AC6, BR7; ITG AC3 | Integration | R-DEV-05 with timer "deadline driven" and no service levels row; MSG-P2-023 |
| TC-E2-035-07-ITG | legacy AC7, BR8; ITG AC2 | Integration | Move on 30 December 2026 with two holidays |
| TC-E2-035-08-ITG | legacy AC8; ITG AC3 | Integration | Case with an open NEXT_ACTION_MISSING task closes |
| TC-E2-035-09-ITG | legacy AC9; ITG AC4 | Integration | Same transition with DLE-SYN-0402 processed twice |
| TC-E2-035-10-ITG | legacy AC10; ITG AC4 | Integration | Two transitions against version 7; MSG-GEN-004 |
| TC-E2-035-11-ITG | legacy AC11; ITG AC3 | Integration | Three cases with no next action before the check runs |
| TC-E2-035-12-ITG | legacy AC12, BR3; ITG AC2 | Integration | Rule R-RES-07 with timer "same day" |
| TC-E2-035-13-ITG | legacy AC13, Access; ITG AC4 | Component | RW-REFADM reads the next action; refused with MSG-P4-002 |
| TC-E2-035-14-ITG | legacy AC14, BR11; ITG AC4 | Integration | No RESTRUCTURE version in force on 2027-01-04; NoPackageInForce and MSG-P3-027 |

The Covers column names the legacy AC of RWB-E2-035 that the copy is derived from and the ITG criterion of §7 that the copy asserts at integration level; the Level column maps the legacy System level to Integration and the legacy Access level of TC-E2-035-13 to Component. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the action text, the owner role, the timer spec, the service levels row and the holiday list are data held by the owning services; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces or reports: the next action holds rule text only, the owner is a role code, the case list read is limited to the next action columns, and the harness uses synthetic cases and parties.
- No read of another service's schema: every read goes through the owner's contract, the SchemaBoundaryCheck fails the run on a cross-schema reference, and only rwb-source-data reads the ACE views.
- No production data and no outside system: the harness calls only the owning services and their fakes, never an outside gateway or a production endpoint, and the outbound item it reads is the seeded one.
- The rule row is read only through the rwb-decision contract: the harness reads no workbook, no drl_source and no rule_row row, and CatalogFidelityCheck fails the run when the case and the catalog disagree.
- No second rule engine: the harness asserts the rule ID and the package version returned by the owning service and never evaluates a rule itself.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner.
- The journey never writes: the harness asserts that a refusal, a no-version answer and a repeated transition leave every source unchanged.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-012 | Every open case carries one next action with owner and due date | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-RES-04, R-SET-13 | TC-E2-035-01-ITG, TC-E2-035-03-ITG, TC-E2-035-04-ITG, TC-E2-035-08-ITG, TC-E2-035-13-ITG |
| REQ-WKM-013 | The next action comes from the rule that moved the case | Business Requirements Epic 2, section 3.2 | FEAT-CWC-28 | 06 to 10 Recovery case processes | R-RES-03, R-RES-04, R-SET-13 | TC-E2-035-02-ITG, TC-E2-035-05-ITG, TC-E2-035-07-ITG, TC-E2-035-09-ITG, TC-E2-035-10-ITG, TC-E2-035-12-ITG, TC-E2-035-14-ITG |
| REQ-WKM-016 | A case with no next action is reported as an exception | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27 | 06 to 10 Recovery case processes | R-DEV-05 | TC-E2-035-06-ITG, TC-E2-035-11-ITG |
| REQ-WKM-014 | Next action visible on the case record and every queue view | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | None | TC-E2-035-01-ITG, TC-E2-035-04-ITG |
| REQ-WKM-015 | An overdue next action escalates like a service level breach | Business Requirements Epic 2, section 3.2 | FEAT-CWC-27, FEAT-CWC-28 | 06 to 10 Recovery case processes | None | TC-E2-035-01-ITG, TC-E2-035-04-ITG |

The five requirement IDs are those of the legacy story and keep their legacy BRD section, feature, process and rule text. Escalation of an overdue next action is out of scope for this story and is traced for completeness under REQ-WKM-015 only.

### 19. Out of scope

- The seven owning I stories RWB-P3-E1018-APP, RWB-P3-E1031-APP, RWB-P3-E2042-APP, RWB-P2-E2035-APP, RWB-P4-E2035-APP, RWB-P3-E2035-APP and RWB-P7-E2035-APP, and every screen, endpoint, table, rule and workflow they build.
- Legacy AC1 to AC14 of RWB-E2-035, which the APP stories of the same legacy key own.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-case, rwb-decision, rwb-access and rwb-integration, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- Escalation when a next action passes its due date (RWB-E2-015, REQ-WKM-015).
- The next action column in the queue view screens (RWB-E2-011).
- The values of the service levels per state (DL22) and the loading of the route set rule rows beyond allocation, assignment and transfer (DL24; the RESTRUCTURE rows are RWB-E2-042).
- The RESTRUCTURE package checks, scenarios and four-eyes approval (RWB-E1-073).
- The durable timers that replace the legacy JOB-05 check in the target design (ADR-011; Architecture v5 slide 44); the harness asserts their result on the case, not the timer.
