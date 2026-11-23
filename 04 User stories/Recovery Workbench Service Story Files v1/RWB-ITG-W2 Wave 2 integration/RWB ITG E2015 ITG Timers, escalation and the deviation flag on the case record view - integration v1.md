# RWB-ITG-E2015-ITG Timers, escalation and the deviation flag on the case record view

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2015-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E2015-APP, RWB-S8-E2015-APP, RWB-P4-E2015-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-015 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness that runs the timers, the escalation state, the prescription date and the deviation flag of a case through gateway-bff and the owning services**, so that **the wave 2 clocks and deviation journey is proven end to end, with evidence, before the release is accepted**.

This story builds the harness and the evidence only. It builds no production screen, endpoint, table, workflow or schedule, and it owns no table. The real behaviour is owned by the three I stories RWB-P3-E2015-APP (the two read operations, the timer ordering, the escalation fields, the prescription warning and the merge in rwb-case), RWB-S8-E2015-APP (the deviation query, the pause and the clear of the stage clock, the contact stop and the return point) and RWB-P4-E2015-APP (the role, scope and Case record right check), and those three stories block the ITG run.

### 2. Business rationale

The legacy RWB-E2-015 journey crosses more than one service: rwb-case holds the case, its timers, the tasks and their owner roles and the deviation flag; rwb-deviation holds the deviations, the pause of the stage clock and the clear; rwb-decision holds the decision log entry that names the approver of a deviation; and rwb-access answers the authorisation check. Until the real services are exercised together through the gateway, the program cannot show that the next deadline, the escalation and the reason a case left its path are visible on one case, which is the outcome the program targets at 5 days from 23 days.

The harness gives one repeatable run per business date that proves the composite route composes the case record from one hop per source inside the 2 s budget, that the timers come back ordered by due date with their type, status, warning state, next step owner role and escalation fields, that the prescription date warns inside the 90 day window and stays silent at 91 days, that a case with a deviation open shows as on hold with the deviation, its handler, its approver, the contact stop and the return point while the prescription clock keeps its date, that a case stays on hold until every open deviation clears, and that one slow source degrades one section of the answer instead of the whole screen. It meets REQ-WKM-004, REQ-WKM-005, REQ-DVH-002 and REQ-DRI-001 at the integration level and leaves every business rule and every screen behaviour where the owning stories put them.

### 3. Preconditions

- The three I stories are published and deployed in the SIT environment: RWB-P3-E2015-APP (the case and timer read operations, the timer ordering, the escalation fields, the prescription warning and the merge), RWB-S8-E2015-APP (the deviation query, the pause and the clear of the stage clock, the contact stop and the return point) and RWB-P4-E2015-APP (the authorise check).
- gateway-bff is deployed with the composite route of DP-19 available. The gateway-bff composite case-record route path and its merge order: Not specified in the source documents (GAP-0399; ASM-0574).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness can run green from Day 1 before the I stories land.
- The SERVICE_LEVEL rows that name the escalation role and the next escalation role for a product group and status, and the reference data LOV-TIMER and LOV-DEVIATION, are loaded by the owning stories through their contracts; the harness reads them and holds no copy.
- The harness environment, its test-data seeding and its evidence format and retention: Not specified in the source documents (GAP-0399; ASM-0574).

### 4. Flow

1. Harness: seeds the synthetic cases, their product group, status and queue, the NOTICE_PERIOD, SERVICE_LEVEL and PRESCRIPTION rows, the tasks and their owner roles, the deviations with their handlers, the decision log entries that name the approvers, and the users with their scopes through the owning contracts or the published fakes, at the fixed business date 2026-12-15.
2. Harness: calls the case record composite route through gateway-bff for RW-2026-000501 and asserts the timers ordered by due date, each with type, status, due date, warning state, the owner role of the next step, escalation level, escalated to and next escalation point.
3. Harness: asserts the prescription date 2027-02-13 with the warning MSG-P3-003 at 60 days from the business date, and that case RW-2026-000503 at 2027-03-16, 91 days away, carries no warning.
4. Harness: asserts the expired SERVICE_LEVEL timer of 2026-12-12 at escalation level 1, escalated to RW-TEAMMGR at 2026-12-12 09:05 with the next escalation point RW-PRODHEAD taken from the SERVICE_LEVEL row, and that the case queue and status are unchanged.
5. Harness: calls the composite route for RW-2026-000502 and asserts the on hold banner with MSG-P3-004 naming the deviation and keeping the prescription date, and the deviation with code, handler, approver from decision log entry DLE-9101, raised date, contact stop and return point.
6. Harness: raises deviation X1 on 2026-12-05 and X3 on 2026-12-08 on RW-2026-000504, asserts both with their own handler and approver, clears X1 on 2026-12-14 and asserts that the case stays on hold with only X3 open.
7. Harness: asserts RW-2026-000505 is not on hold, that its cleared X1 carries outcome "Returned" and that the service level timer is running again with due date 2026-12-22, and that RW-2026-000506 returns the empty timers sentence MSG-P3-018.
8. Harness: forces each failure of §5 through the fakes (the empty timers, the out-of-scope case, the deviation query that does not answer inside 2 s, the role without Case record R), asserts the message, the partial answer and that nothing was written, then returns every fake to its healthy answer and completes the journey.
9. Harness: writes one run report per business date, keyed by story and business date; the report format and retention are Not specified in the source documents (GAP-0399; ASM-0574).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | The case has no running, paused or expired timer (RW-2026-000506) | The timers section is returned empty with the empty sentence; the prescription date and the deviations are still returned | MSG-P3-018 | TC-E2-015-08-ITG |
| X2 | The case is outside the caller's scope (RW-2026-000507 in SME-NTH read with a scope Own in MTG-BKK) | 404 from the composite route; nothing is returned and nothing is written | MSG-P4-003 | TC-E2-015-09-ITG |
| X3 | The deviation query does not answer within 2 s | The timers and the prescription date are returned; the deviation section carries the message and the on hold banner still shows from the case's deviation flag | MSG-GEN-006 | TC-E2-015-10-ITG |
| X4 | Two deviations are open on one case | Both show with their own handler and approver; after one clears the case stays on hold with the other open | MSG-P3-004 | TC-E2-015-05-ITG |
| X5 | The prescription date is 91 days away with a 90 day warning | No warning; the prescription date is returned without MSG-P3-003 | None | TC-E2-015-03-ITG |
| X6 | A role without Case record R calls the timers operation | 403 on the direct call and on the composite route; the answer carries the refusal, not an empty timers list | MSG-P4-002 | TC-E2-015-11-ITG |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the three I stories are deployed; until then it runs against the §12.8 fakes |
| Negotiable | The harness pack, the data seeding, the fixed clock and the evidence format are agreed with QA; no business value is fixed by the harness |
| Valuable | The clocks, the escalation and the deviation flag are evidenced across services rather than per service |
| Estimable | One harness project, one journey specification, one fake pack, one fixed clock fixture and one run report |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each scenario of §7 is one automated journey with synthetic data and a machine-checkable result |

### 7. Acceptance criteria

```gherkin
Feature: Timers, escalation and the deviation flag on the case record view - wave 2 integration harness

  Background:
    Given the business date is 2026-12-15
    Given user "U-CO-01" holds RW-CASEOWN and owns case "RW-2026-000501" with product group "HIRE_PURCHASE" and status "IN_PROGRESS"
    Given prescription.warning-days is 90
    Given case "RW-2026-000501" has a "NOTICE_PERIOD" timer started on 2026-12-01 expiring on 2027-01-30, on a task owned by role "RW-LITOFF"
    Given case "RW-2026-000502" has deviation "X3" raised on 2026-12-10, handler "U-SP-01", approved in decision log entry "DLE-9101" by "U-LG-01", paused state "WITH_FCR_OFFICER" and contact stop true
    Given case "RW-2026-000504" has deviations "X1" raised on 2026-12-05 and "X3" raised on 2026-12-08, both open
    Given case "RW-2026-000505" had deviation "X1" cleared on 2026-12-14 and its "SERVICE_LEVEL" timer resumed with a new expiry of 2026-12-22
    Given case "RW-2026-000506" has no timer with status "RUNNING", "PAUSED" or "EXPIRED"
    Given case "RW-2026-000507" belongs to team "SME-NTH" and "U-CO-01" has scope Own in team "MTG-BKK"

  Scenario: AC1 The case record composite through gateway-bff (new, D-RCV-60)
    Given the harness calls the case record composite route at "Not specified in the source documents (GAP-0399; ASM-0574)" for "RW-2026-000501"
    When gateway-bff returns the composite answer and rwb-case merges its own records with the rwb-deviation and rwb-decision contracts, with rwb-access answering the authorisation check
    Then the answer holds the case, its timers, its prescription date and its deviations merged in one answer
    And the timers are ordered by due date and carry its type, its status, its due date, its warning state, the owner role of the next step, its escalation level, escalated to and the next escalation point
    And each source is called once, one hop, with the 2 s timeout and a breaker per downstream
    And no service reads another service's schema
    And the run report holds one trace spanning the gateway and each owning service

  Scenario: AC2 Escalation and prescription asserted from the answer (new, D-RCV-60)
    Given the "SERVICE_LEVEL" timer of "RW-2026-000501" expired on 2026-12-12 with escalation level 1 and was escalated to "RW-TEAMMGR" at 2026-12-12 09:05
    Given the SERVICE_LEVEL row for "HIRE_PURCHASE" status "IN_PROGRESS" names the next escalation role "RW-PRODHEAD"
    When the harness reads the answer for "RW-2026-000501"
    Then the expired service level timer carries status "Expired", escalation level 1, escalated to "RW-TEAMMGR" at 2026-12-12 09:05 and next escalation point "RW-PRODHEAD"
    And the case queue and status are the same as before the call
    When the harness reads the prescription date of "RW-2026-000501"
    Then 2027-02-13 is returned with the warning MSG-P3-003, 60 days after the business date
    When the harness reads the prescription date of "RW-2026-000503"
    Then 2027-03-16 is returned at 91 days with no warning

  Scenario: AC3 Deviation and the on hold behaviour (new, D-RCV-60)
    When the harness reads the answer for "RW-2026-000502"
    Then the answer is in state "On hold" with MSG-P3-004 naming "Deceased customer" and keeping the prescription date
    And the deviation carries code "X3", handler "U-SP-01", approver "U-LG-01" from decision log entry "DLE-9101", raised on 2026-12-10, contact stop true and return point "WITH_FCR_OFFICER"
    When the harness reads the answer for "RW-2026-000504"
    Then both deviations "X1" and "X3" are returned with their own handler and approver
    And the answer is in state "On hold"
    When "X1" is cleared on 2026-12-14 through the deviation contract
    Then the answer stays in state "On hold" with only "X3" open and "X1" shown as cleared on 2026-12-14
    When the harness reads the answer for "RW-2026-000505"
    Then the answer is not on hold
    And the deviation is shown as cleared on 2026-12-14 with outcome "Returned"
    And the service level timer carries status "Running" with due date 2026-12-22

  Scenario: AC4 Failure isolation and the partial answer (new, D-RCV-60)
    Given rwb-deviation does not answer within 2 s for "RW-2026-000502"
    When the harness reads the answer through gateway-bff
    Then the timers and the prescription date are returned
    And the deviation section carries MSG-GEN-006 naming "Deviation handling"
    And the on hold banner still shows from the case's deviation flag
    When "U-CO-01" reads "RW-2026-000507" through gateway-bff
    Then the answer is 404 with MSG-P4-003
    When the harness reads the answer for "RW-2026-000506"
    Then the timers section carries MSG-P3-018
    And no call changed a timer, a deviation or the case
```

These four criteria are new for the ITG harness and do not restate the app criteria owned by the I stories.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every timer of the case with status Running, Paused or Expired shows with type, due date, status and the owner role of its task | REQ-WKM-005; LOV-TIMER |
| BR2 | A breached service level shows the role it was escalated to, when, and the next escalation point. The case does not move | R-UNI-30; REQ-WKM-004 |
| BR3 | A deviation pauses the stage clock and keeps the prescription clock running | R-DEV-01; REQ-DVH-002 |
| BR4 | A case with a deviation open shows as on hold with the deviation and the prescription date | casemodel.txt Case status (On hold); R-UNI-04; R-UNI-05 |
| BR5 | X1, X2 and X3 show the contact stop | R-UNI-04; R-UNI-05; R-UNI-06; CTL-16 |
| BR6 | The case leaves on hold only when every open deviation is cleared | R-UNI-43; FEAT-DVH-09 |
| BR7 | The prescription date shows a warning from `prescription.warning-days` before it (assumed 90; DL22) | R-UNI-31; CTL-18 |
| BR8 | The return point of a deviation is the routing state the case was in when it paused | DF-CAS-041; R-DEV-08 |
| BR9 | The approver of a deviation is the approver on its decision log entry | REQ-DRI-001 |

The harness asserts these nine rules against the owning services and the published contracts; it re-implements none of them. No BR row is changed by this story.

### 9. State transitions

None. The harness changes no case status, no timer status and no deviation state; it reads records only. The facts below are caused by the owning services and are observed and asserted by the harness.

| Observed fact | Caused by | Asserted as |
|---|---|---|
| Timer expired and escalated to a role | the durable timer inside CaseWorkflow, run by the app story | An expired timer with its escalated role, time and next escalation point (TC-E2-015-04-ITG) |
| Prescription warning raised | the prescription clock, which is never paused | MSG-P3-003 at 60 days and no warning at 91 days (TC-E2-015-03-ITG) |
| Deviation raised | rwb-deviation | The on hold banner and the deviation row (TC-E2-015-02-ITG) |
| Stage clock paused and prescription running | DeviationWorkflow and CaseWorkflow | A paused service level timer and a running prescription (TC-E2-015-06-ITG) |
| Second deviation open | rwb-deviation | Both deviations with the case still on hold (TC-E2-015-05-ITG) |
| Deviation cleared | rwb-deviation | The cleared deviation with outcome Returned and the resumed timer (TC-E2-015-07-ITG) |
| No timer of any status | the timer rows of the case | The empty timers sentence (TC-E2-015-08-ITG) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | The synthetic user the harness drives: reads the case record view with its timers, prescription date and deviations in scope (Case record R, scope Own) |
| RW-TEAMMGR, team manager | Reads the case and its timers, including the escalation it was raised to (Case record R, scope Team) |
| RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LEGAL | Read the case and its deviations (Case record R) |
| RW-AUDIT, internal audit | Reads the case and its deviations (Case record R, scope All); changes nothing |
| SY-CASEWF, case workflow module | Writes the escalation fields when a timer escalates, inside the app story; the harness only reads them |

Reading the approver needs no Decision log right: the answer carries the approver user ID only, not the decision log entry. Authorisation is answered by rwb-access through POST /api/recovery/access/v1/authorise on every call, and the harness asserts the refusal of a role without Case record R.

### 11. Data

The harness owns no table. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-017 | recovery_case | prescription_date | Read |
| DF-CAS-018 | recovery_case | stage_clock_start | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-CAS-020 | recovery_case | legal_hold | Read |
| DF-WRK-027 | timer | id | Read |
| DF-WRK-029 | timer | task_id | Read |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-031 | timer | started_at | Read |
| DF-WRK-032 | timer | expires_at | Read |
| DF-WRK-033 | timer | warn_at | Read |
| DF-WRK-034 | timer | paused | Read |
| DF-WRK-035 | timer | status | Read |
| DF-WRK-036 | timer | escalation_level | Read |
| DF-WRK-043 | timer | escalated_to_role | Read |
| DF-WRK-044 | timer | escalated_at | Read |
| DF-WRK-023 | task | owner_role | Read |
| DF-CAS-038 | deviation | deviation_code | Read through the rwb-deviation contract |
| DF-CAS-039 | deviation | raised_at | Read through the rwb-deviation contract |
| DF-CAS-041 | deviation | paused_state | Read through the rwb-deviation contract |
| DF-CAS-042 | deviation | handler_user_id | Read through the rwb-deviation contract |
| DF-CAS-043 | deviation | contact_stop | Read through the rwb-deviation contract |
| DF-CAS-044 | deviation | cleared_at | Read through the rwb-deviation contract |
| DF-CAS-045 | deviation | outcome | Read through the rwb-deviation contract |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read through the rwb-decision contract |

Test data is synthetic. No production case, party or decision is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness calls the owning services; it serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case facts, the product group, the status, the prescription date and the deviation flag the banner is built from |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The timers with their type, status, due date, warning state, next step owner role and escalation fields |
| POST | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | Seeds the X1 and X3 deviations of the journey with their handler and contact stop |
| PATCH | `/api/recovery/deviation/v1/deviations/{deviationId}` | S8 rwb-deviation | Clears X1 on 2026-12-14 and asserts the resumed stage clock |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | The approver on decision log entry DLE-9101 (Architecture v5 slide 14: central decision ledger) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and Case record right check used by the composite route and by the direct calls (Architecture v5 slide 14 and slide 41: rwb-access IN POST /authorise) |

The composite screen route itself is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order are Not specified in the source documents (GAP-0399; ASM-0574). The deviation data reaches the composite answer through the S8 contract that RWB-S8-E2015-APP publishes; the harness reads no deviation list path, because the ownership map gives none.

#### 12.3 Events published

None. The harness produces no event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.case.TimerBreached.v1 | rwb.case.events.v1 | P3 rwb-case | The event is raised when the durable timer inside CaseWorkflow fires, carries the case ID and the timer type, and the escalated role, the escalated time and the next escalation point appear on the timer row the harness reads |
| rwb.deviation.DeviationRaised.v1 | rwb.deviation.events.v1 | S8 rwb-deviation | One event per deviation raised on RW-2026-000502 and RW-2026-000504, carrying the case ID and the deviation code, is present within 5 minutes of the seeding call, and the case then answers as on hold |
| rwb.deviation.DeviationCleared.v1 | rwb.deviation.events.v1 | S8 rwb-deviation | The clear of X1 on RW-2026-000504 and on RW-2026-000505 is announced within 5 minutes, and the answer then carries the cleared deviation and the resumed timer |

The events are consumed for assertion only; order per case is guaranteed by the case key on both topics, and the harness reads timers and deviations through the owning contracts rather than from a topic.

#### 12.5 Workflows and activities

None added. The harness starts no workflow and adds no activity; it drives REST only. The durable timers belong to CaseWorkflow in rwb-case and the pause and the clear to DeviationWorkflow in rwb-deviation, both owned and started by the app stories; the five minute timer check is retired and the harness replaces it with a fixed clock and seeded timer rows.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow, and it seeds its timer rows rather than waiting for a scheduler.

#### 12.7 Tables owned

None.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-case | cases/{caseId}, cases/{caseId}/timers | RW-2026-000501 with the NOTICE_PERIOD, SERVICE_LEVEL and PRESCRIPTION rows, the expired service level at level 1 escalated to RW-TEAMMGR at 2026-12-12 09:05 with next role RW-PRODHEAD, and the prescription date 2027-02-13; RW-2026-000503 with 2027-03-16; RW-2026-000506 with an empty timers answer; RW-2026-000507 in SME-NTH; the deviation flag on RW-2026-000502 |
| rwb-deviation | cases/{caseId}/deviations, deviations/{deviationId} | X3 on RW-2026-000502 with handler U-SP-01, paused state WITH_FCR_OFFICER, contact stop true and approver U-LG-01; X1 and X3 on RW-2026-000504, X1 cleared on 2026-12-14; X1 cleared on RW-2026-000505 with outcome Returned; a slow answer beyond 2 s for the timeout case |
| rwb-decision | decision-log/{entryId} | Decision log entry DLE-9101 with approver U-LG-01 and decision code X3; the approver of the X1 entries of RW-2026-000504 |
| rwb-access | authorise | Allow RW-CASEOWN in scope; allow the read roles of §10; refuse a role without Case record R with MSG-P4-002; refuse SME-NTH for a scope Own in MTG-BKK with MSG-P4-003 |

The fakes are published from the owning services' OpenAPI documents and are replaced by the real service as each I story lands, contract by contract. The harness repository and its environment: Not specified in the source documents (GAP-0399; ASM-0574).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Six consumed operations of §12.2 through gateway-bff and the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes rwb.case.TimerBreached.v1 on rwb.case.events.v1 and rwb.deviation.DeviationRaised.v1 and rwb.deviation.DeviationCleared.v1 on rwb.deviation.events.v1 for the assertions; publishes nothing |
| Temporal | No | Starts no workflow and adds no activity; the durable timers belong to CaseWorkflow and the app story |
| File | No | Reads no file; the run report is a harness artefact, not a service file exchange |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list. The blocking dependencies of this story are the three I stories.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs one journey per business date, keyed by story and business date, and stops at the first failed assertion with the trace |
| CaseRecordClient | Harness adapter | Calls the composite case-record route and the six consumed operations of §12.2 with the Idempotency-Key header where the operation requires one |
| FakePack | WireMock project | Serves rwb-case, rwb-deviation, rwb-decision and rwb-access from the published OpenAPI documents of §12.8 |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference found in the trace, so a service never reads another service's tables |
| TimerClockFixture | Fixture | Holds the business date at 2026-12-15 and seeds the NOTICE_PERIOD, SERVICE_LEVEL and PRESCRIPTION rows, so the same timer state is produced on every run without waiting for a scheduler |
| PartialAnswerCheck | Assertion | Fails the run when a slow deviation query empties the timers or the prescription section, when the on hold banner is lost, or when a refusal returns an empty list instead of the message |
| RunReportWriter | Reporter | Writes one run report with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0399; ASM-0574) |

**Environment and test data**

- Environment: SIT, one namespace, the three I stories deployed from their wave 2 builds or replaced by the §12.8 fakes, with the clock of TimerClockFixture fixed at the business date 2026-12-15. Harness repository, environment and data seeding: Not specified in the source documents (GAP-0399; ASM-0574).
- Data: synthetic cases RW-2026-000501 with the three timers and the escalated service level, RW-2026-000502 on hold for X3, RW-2026-000503 at 91 days, RW-2026-000504 with X1 and X3 open, RW-2026-000505 with X1 cleared and the timer resumed, RW-2026-000506 with no timer and RW-2026-000507 in SME-NTH; the users U-CO-01 with RW-CASEOWN, U-SP-01 as the handler and U-LG-01 as the approver; the decision log entry DLE-9101. No production record is copied.
- Reset: each run starts from the seeded state at the fixed business date, so a repeated run is deterministic and the same report is produced.

**Build steps**

1. Build JourneyRunner and CaseRecordClient against the published OpenAPI documents of the owning services.
2. Publish FakePack for the four services from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Build TimerClockFixture with the business date 2026-12-15 and the seeded timer rows, and prove a run is repeatable without a live scheduler.
4. Add the composite route assertion of AC1, including the one-hop check, the 2 s per-call budget, the single trace and the SchemaBoundaryCheck.
5. Add the escalation and prescription assertions of AC2, the deviation and on hold assertions of AC3 with the clear of X1, and the partial answer of AC4 with PartialAnswerCheck.
6. Replace each fake with the real service as its I story lands, contract by contract, and confirm the same assertions hold against the real services.
7. Publish the run report per business date and add the pass/fail gate agreed with QA; the gate definition: Not specified in the source documents (GAP-0399; ASM-0574).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switch it exercises is `rwb.p3.case-clocks` from the legacy solution plan; the harness asserts the disabled state, where SCR-03 shows the Epic 1 read only fields, and the enabled state, where the timers, the escalation and the deviation flag are returned.

**Done when:** the journey runs green against the three deployed I stories in SIT, the run report for the business date holds every assertion of §7 and §16 with its trace, every message of §14 carries its substituted values, and the pass/fail gate agreed with QA is met for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-003 | A timer or the prescription date is inside its warning period | {timer} ends on {date}. |
| MSG-P3-004 | The case is on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-018 | The case has no running, paused or expired timer | There are no running timers on this case. |
| MSG-GEN-006 | The deviation module does not answer in time | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A role without Case record R opens the view | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the person's scope | This case is not in your scope. |

The harness asserts the message ID and the substituted values, including "Deceased customer" in MSG-P3-004 and "Deviation handling" in MSG-GEN-006; it does not own the message text. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-03 Case record | Loading | The composite route answers at once with the case, the timers and the prescription date; the harness reads the answer the skeleton rows consume |
| SCR-03 Case record | Read only | The timers ordered by due date with type, status, warning state, next step owner role, escalation level, escalated to and next escalation point; the prescription date with its warning |
| SCR-03 Case record | Editable | The same clocks and deviation panels are returned; the edits elsewhere on the record are not exercised by the harness |
| SCR-03 Case record | On hold | The banner with MSG-P3-004 and the prescription date, each open deviation with code, handler, approver, raised date, contact stop and return point, and the cleared deviation with its outcome and the resumed timer |

The harness opens no screen and renders no page; it asserts the composite route answer that the screen consumes. Screen-level behaviour remains with the owning APP stories. The harness environment and evidence detail: Not specified in the source documents (GAP-0399; ASM-0574).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-015-01-ITG | AC1, BR1 | Integration | NOTICE_PERIOD timer on a task owned by RW-LITOFF |
| TC-E2-015-02-ITG | AC2, BR4, BR5, BR8, BR9 | Integration | X3 with handler, approver, paused state and contact stop |
| TC-E2-015-03-ITG | AC3, BR7 | Integration | Prescription 60 and 91 days ahead |
| TC-E2-015-04-ITG | AC4, BR2 | Integration | SERVICE_LEVEL expired, level 1, escalated to RW-TEAMMGR |
| TC-E2-015-05-ITG | AC5, BR6 | Integration | X1 and X3 open, then X1 cleared |
| TC-E2-015-06-ITG | AC6, BR3 | Integration | Paused service level and running prescription |
| TC-E2-015-07-ITG | AC7, BR6 | Integration | X1 cleared and timer resumed |
| TC-E2-015-08-ITG | AC8 | Integration | Case with only stopped timers |
| TC-E2-015-09-ITG | AC9 | Integration | Case of team SME-NTH opened by an MTG-BKK owner |
| TC-E2-015-10-ITG | AC10 | Integration | Stubbed deviation query delayed 3 seconds |
| TC-E2-015-11-ITG | Access | Component | RW-REFADM (no Case record right) calls `GET /cases/{caseId}/timers`; refused with MSG-P4-002 |

The Covers column is the legacy AC of RWB-E2-015 that the copy is derived from, and every copy also asserts its integration criterion of §7: AC1 takes TC-E2-015-01-ITG, -02-ITG, -04-ITG, -06-ITG and -11-ITG; AC2 takes -03-ITG and -04-ITG; AC3 takes -02-ITG, -05-ITG, -07-ITG and -10-ITG; AC4 takes -08-ITG, -09-ITG and -10-ITG. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the warning days, the escalation roles, the next escalation role, the timeout and the timer and deviation labels are data held by the owning services; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces or reports: only staff user IDs are asserted, customer data is never read into a report, and the harness uses synthetic cases and stores IDs and assertions only.
- No read of another service's schema: every read goes through the owner's contract, the SchemaBoundaryCheck fails the run on a cross-schema reference, and only rwb-source-data reads the ACE views.
- No production data and no outside system: the harness calls only the owning services and their fakes, never an outside gateway or a production endpoint.
- The view never changes a timer, a deviation or the case: the harness asserts that a read, a refusal and the timeout case leave every source unchanged.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-004 | A breached service level visible to the escalation role without the case moving | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-07 | All recovery processes | R-UNI-30 | TC-E2-015-04-ITG, TC-E2-015-11-ITG |
| REQ-WKM-005 | Timers, escalation state and the deviation flag on the case record view | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-05, FEAT-WKM-06 | All recovery processes | R-UNI-31, R-UNI-04, R-UNI-05 | TC-E2-015-01-ITG to TC-E2-015-03-ITG, TC-E2-015-08-ITG to TC-E2-015-10-ITG |
| REQ-DVH-002 | A deviation pauses the stage clock and keeps the prescription clock running | Business Requirements Epic 2, section 4; Program, section 5.15 | FEAT-DVH-02, FEAT-DVH-03, FEAT-DVH-05, FEAT-DVH-06, FEAT-DVH-09 | 11 Handle customer care and deviations | R-DEV-01, R-UNI-43 | TC-E2-015-02-ITG, TC-E2-015-05-ITG to TC-E2-015-07-ITG |
| REQ-DRI-001 | Every decision writes one record holding the case, the decision, the recommendation, the approval and the outcome | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-DRI-01 | All recovery processes; 11 Handle customer care and deviations | R-UNI-24, R-UNI-39 | TC-E2-015-02-ITG |

The three requirements the legacy story tabulates keep their legacy BRD section, feature, L3 process and rule text. REQ-DRI-001 is tabulated here because the approver a deviation shows is the approver on its decision log entry; it is traced for that link only.

### 19. Out of scope

- The three owning I stories: RWB-P3-E2015-APP (the case and timer read operations, the ordering, the escalation fields, the prescription warning and the merge), RWB-S8-E2015-APP (the deviation query, the pause, the contact stop, the return point and the clear) and RWB-P4-E2015-APP (the authorise check), and every screen, endpoint, table and rule they build.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-case, rwb-deviation, rwb-decision and rwb-access, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- Raising, handling and clearing deviations (S8, SCR-06 and SCR-08).
- Starting, pausing and resuming timers and the escalation itself (RWB-E1-028).
- The history timeline on the case (RWB-E2-016).
- The next action panel (RWB-E2-035).
