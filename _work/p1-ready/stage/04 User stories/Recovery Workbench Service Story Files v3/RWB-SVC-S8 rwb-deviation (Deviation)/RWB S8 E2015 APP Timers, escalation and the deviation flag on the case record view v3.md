# RWB-S8-E2015-APP Timers, escalation and the deviation flag on the case record view

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E2015-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-S8-H |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S8-E2015-APP-16) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-S8-E2015-APP-14) |
| Contract version | /v1 path only; the build version is Not specified in the source documents (DOR-RWB-S8-E2015-APP-23) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-S8-E2015-APP-22) |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2015-CON; Not specified in the source documents (DOR-RWB-S8-E2015-APP-21) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (FR-S8-005, FR-S8-006, FR-S8-007, FR-S8-008) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the quoted English to Error and Message Standard v6.


**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-015 for rwb-deviation, carrying the deviation half of the case record view (every deviation of the case, open or cleared, with its code, label, handler, pause date, return point, contact stop, cleared date, outcome and decision record) and the deviation's own service level as a durable Temporal timer. Applied: the plan's H row is None and the library contracts of DP-03, DP-07, DP-10, DP-14, DP-15 and DP-19 arrive with the service template; the Ownership Map gives S8 two write operations and no read, so the read is declared here with a gap (GAP-3099; ASM-5288); and legacy AC1 to AC10 stay with RWB-P3-E2015-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S8-E2015-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 19 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **rwb-deviation to answer the deviation section of the case record view — every deviation of the case, open or cleared, with its code, its label, its handler, the date it was raised, the point the case returns to, the contact stop, the date it cleared, its outcome and the decision record that holds its approver, together with the case-level On hold and contact-stop markers, the effect on the two clocks and the state of the deviation's own service level**, so that **the record shows why the case paused, who holds it and where it goes back, and whether its deviation service level has been breached, without the case service reading a deviation table**.

This story is the rwb-deviation part of legacy RWB-E2-015. The legacy story puts every timer, escalation and deviation on the case record view; its section 12 calls `DeviationQuery.forCase` with a 2 second timeout (NFR-008) and its section 11 reads `deviation.deviation_code`, `raised_at`, `paused_state`, `handler_user_id`, `contact_stop`, `cleared_at` and `outcome` through that interface. Those seven fields are this service's. The timers, the service levels, the prescription date and the escalation of the case belong to rwb-case and stay with RWB-P3-E2015-APP.

Inside `rwb-deviation` this is the case-record projection of the deviation service:

- Service `rwb-deviation`, schema `rwb_deviation`, REST base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1` with event names `rwb.deviation.<Event>.v1`, Temporal task queue `rwb-deviation` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.deviation` (context pack, service row).
- One read, `GET /cases/{caseId}/deviations`, answers the deviation section of SCR-03 in one hop inside 2 s: every row of the case, open and cleared, with the fields of §11, plus the case-level markers `anyOpen`, `openCount`, `contactStopActive`, `stageClockPausedSince` and the service-level state of each open row (DP-11, DP-13, DP-01).
- The labels of the codes and of the outcomes, the deviation service-level row and the business date are read on the reference-data contract of rwb-case at the version in force (DP-07); nothing of them is written in code.
- The deviation's own service level (R-DEV-20, SLA_BREACHED) runs as a durable Temporal timer in `DeviationWorkflow` on queue `rwb-deviation` (DP-10) and is recorded in the service's local decision record on `rwb.decision-record.v1` (DP-03). The timer moves no case status: R-DEV-20 leaves the deviation in `DEV_WITH_OWNER` (TSD S8 T4).
- No event is published by this slice: `rwb.deviation.DeviationRaised.v1` (EV-06) and `rwb.deviation.DeviationCleared.v1` (EV-07) stay with the raise and clear steps (DP-09 as a prohibition; DP-14 as naming).

What this story does not own: raising, routing, handling and clearing a deviation, which are the Epic 1 and Epic 7 stories of this service; the case timers, the service-level escalation, the prescription date and the warning days, which are rwb-case's in RWB-P3-E2015-APP and RWB-E1-028; the approver of the deviation decision, which is resolved on the decision log of P7 and returned by rwb-case (legacy flow step 4, BR9); the reason a caller is refused, which is the access decision of rwb-access in RWB-P4-E2015-APP; and the end-to-end proof across the four services, which is RWB-ITG-E2015-ITG.

### 2. Business rationale

Deadlines are agreed by email today, and litigation was not filed for debtors who met the criteria because nobody saw the prescription date in time (CTL-18; legacy section 2). Legacy BR4 and BR6 then put the deviation on the same screen: a case with a deviation open shows as on hold, and it leaves on hold only when every open deviation is cleared. The deviation half of that screen is a fact only this service holds.

Three target facts shape the slice.

1. **The deviation estate is this service's alone.** `deviation` is S8's single table in `rwb_deviation` (context pack ownership rows; TSD S8 T3.1), so an open code, its label, its handler, its pause point, its contact stop and its outcome are answered here and nowhere else. Under DP-01 no other service reads that table, and the case record may not either; the read is the only way the screen sees a deviation.
2. **What the screen shows is a pause, not a stop.** R-DEV-01 pauses the stage clock, keeps the prescription clock running and routes the deviation to its named owner (FSD S8 A2.2.3.1, A2.3.3.1; REQ-DVH-002). The projection therefore carries the pause date of each open row and the state the case resumes into, and states that no deviation touches the prescription clock — the fact that makes "Paused since 2026-12-10" and "Running" both true on one screen (Arch v5 slide 8).
3. **A deviation has its own clock and its own escalation.** R-DEV-20 keeps the deviation in `DEV_WITH_OWNER` on an SLA breach, and the slide 8 note is explicit: the deviation escalates if it is not resolved in 10 working days. In the target that clock is a durable Temporal timer of `DeviationWorkflow`, not a Quartz job (the ownership rows give S8 no job), so the escalation survives a restart and is recorded in the service's decision record.

The slice therefore supports REQ-WKM-005 (the deviation flag on the record view), REQ-DVH-002 (stage clock paused, prescription clock running), REQ-DRI-001 (the approver of a deviation is the approver on its decision log entry — this service supplies the record that entry names) and REQ-WKM-004 (an escalated case does not move). It changes no rule of the DEV route set and no timer of rwb-case.

### 3. Preconditions

- The `rwb_deviation` baseline is in place: `deviation` exists with the columns of DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0, and the outbox, inbox and idempotency tables of the platform event library exist in the schema.
- The service runs as its own login on `rwb_deviation` (DP-02) and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery_case`, `rwb_case` or a `v_ace_*` view is refused by the database and fails the boundary test.
- RWB-P3-E2015-CON is published: the case-record contract of this legacy key, which fixes the operation the record calls, the deviation view it expects and the 2 s budget. The names of the view fields not printed by the legacy story are Not specified in the source documents (GAP-3099; ASM-5289), and the story builds against its fake.
- The reference-data contract of rwb-case is on the service template (DP-07), with LOV-DEVIATION (X1 to X7), LOV-DEV-OUTCOME (RETURNED, RE_ROUTED, CASE_ENDED — TSD S8 T3.2), the deviation service-level row and the business date at the version in force.
- The decision-record library and the shared topic `rwb.decision-record.v1` of DP-03 are on the service template, so the escalation of the deviation's service level can be recorded locally (H RWB-PLT-E1027-CON arrives with the baseline).
- The Temporal workflow kit of RWB-PLT-E1071-CON is on the service template, with the `DeviationWorkflow` of this service already started for a case by the raise step; this story adds one timer to it and starts no workflow (DP-10).
- The authorisation decision of rwb-access is consumed as the cached permission of the service (DP-08, not in this story's pattern set): the read needs Case record right R (TSD S8 T-A.1).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-P3-E2015-CON when its tests pass.

### 4. Flow

1. The case owner opens SCR-03 Case record for a case. The screen is composed by the gateway-bff composite route of DP-19, which merges the case answer of rwb-case with the deviation answer of this service (legacy section 4 step 2; DP-19).
2. The composite route calls `GET /api/recovery/deviation/v1/cases/{caseId}/deviations` with the viewer's identity, one hop, inside a 2 s budget (legacy section 12; DP-11).
3. `DeviationGuard` authorises the call from the cached decision of rwb-access (Case record right R, scope applied) and refuses with 403 and MSG-P4-002 before a row is read (legacy X2, section 10).
4. `CaseDeviationReader` reads every `deviation` row of the case in `rwb_deviation`, open and cleared, with the columns of §11, and separates an open row (`cleared_at` null) from a cleared one (legacy section 11).
5. `DeviationLabelResolver` resolves the label of each code on LOV-DEVIATION and the label of each outcome on LOV-DEV-OUTCOME at the version in force on the reference-data contract (DP-07). The legacy story publishes one label, "Deceased customer" for X3 (legacy AC2).
6. `DeviationClockProjection` derives the case-level markers: `openCount`, `anyOpen`, `contactStopActive` (true when any open row carries `contact_stop` true) and `stageClockPausedSince`, the `raised_at` of the earliest open row. It states that no row of this service pauses the prescription clock, because R-DEV-01 does not pause it (legacy BR3, BR5, BR6; REQ-DVH-002).
7. `DeviationSlaProjection` derives `slaDueAt` and `slaBreached` for each open row from its `raised_at`, the deviation service-level row and the business date read on the same contract. The values are rows, never constants (legacy section 13 configuration; R-DEV-20).
8. `DeviationSlaTimer` in `DeviationWorkflow` waits from `raised_at` to the service level of the row; on firing, the `EvaluateRules` activity evaluates R-DEV-20, the `RecordAndApply` activity writes the local decision record and the deviation stays in `DEV_WITH_OWNER`. The timer is cancelled when the row is cleared (R-DEV-18; DP-10, DP-03).
9. `CaseDeviationAssembler` returns the answer of 12.1 inside the 2 s budget, one hop, with no customer data, no free-text note and no name of a person. A case this service holds no deviation for answers an empty list with 200: the case row is rwb-case's and this service does not confirm its existence (ASM-5290).

The deviation section of SCR-03 has these states: empty = the empty `deviations` array with openCount 0 and anyOpen false (section 12.1); loading = Not specified in the source documents (DOR-RWB-S8-E2015-APP-10); error = the 503 with MSG-GEN-006, which leaves the case flag to the caller (X3); no access = the 403 with MSG-P4-002 (X1).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The viewing identity holds no Case record right R | Refused with 403 before a row is read; no deviation of the case is returned | MSG-P4-002 | AC7, TC-E2-015-11 |
| X2 | The `caseId` is absent or is not a case reference | 422 and no read; nothing is written | MSG-GEN-001 | AC8, TC-E2-015-16 |
| X3 | The reference-data read or the business date does not answer inside the budget | 503 with the platform envelope naming the system; no partial answer and no half-labelled row is served, so the caller can fall back to the case flag (legacy AC10) | MSG-GEN-006 | AC6 |
| X4 | The decision-record write of the escalation fails when the timer fires | Nothing of the escalation is kept; MSG-P7-003 to the incident path and an incident is raised; the deviation state does not move | MSG-P7-003 | AC5, section 14 |
| X5 | A statement, a component or a test reaches `recovery_case`, a `rwb_case` table, a `v_ace_*` view or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC7, BR1, BR6 |
| X6 | Two deviations are open on one case | Both are returned with their own handler, decision record and pause date; `anyOpen` stays true until the last one clears | None | AC3 |
| X7 | An open row has no service-level row in force, or no label in the version of LOV-DEVIATION in force | The row is served without `slaDueAt` or with the code as its label and the marker "unmapped"; the rest of the answer stands | None | AC5, AC9, TC-E2-015-12, TC-E2-015-17 |

X1 to X3 are the legacy exception paths carried onto the slice (X2 and the timeout of AC10 of the legacy story); X4 to X7 are the paths the escalation timer and the three reference reads add. The legacy paths of the case side — no running timer, case outside the scope and the deviation module silent on the record — stay with RWB-P3-E2015-APP. Each message ID above is served from the message catalogue in Thai and in English, with the English wording the source gives; the Thai wording and its approver are left to DL10 (GAP-1831).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Answers from `rwb_deviation` only and builds on Day 1 against the RWB-P3-E2015-CON fake, the reference-data fake and the platform libraries of the baseline; it waits for no in-lane story |
| Negotiable | The view name, the field order, the flag name and the shape of the case-level markers are this story's; the codes, labels, outcomes and the service level are rows |
| Valuable | The record shows why a case paused, who holds the deviation and where it returns, and the deviation's own service level is visible without the case service reading a deviation table |
| Estimable | One module, one read operation, three projections, one timer, one view and one Flyway step |
| Small | Fits one sprint as a secondary slice of the legacy key, beside RWB-P3-E2015-APP and RWB-P4-E2015-APP |
| Testable | Every criterion runs on synthetic deviations and synthetic reference data through the contract fakes, plus the refusal, the timeout, the boundary and the timer cases on a test clock |

### 7. Acceptance criteria

```gherkin
Feature: Timers, escalation and the deviation flag on the case record view — the rwb-deviation section

  Background:
    Given the business date is 2026-12-15
    Given the rwb-case reference-data contract mock returns LOV-DEVIATION at its version in force with X1 to X7 and the label "Deceased customer" for X3
    Given the rwb-case reference-data contract mock returns LOV-DEV-OUTCOME at its version in force with RETURNED, RE_ROUTED and CASE_ENDED
    Given the rwb-access contract mock returns Case record right R with scope applied for "U-CO-01"

  Scenario: AC1 The open deviation of the case is served (new, D-RCV-60)
    Given case "RW-2026-000502" holds open deviation "X3" raised on 2026-12-10 with handler "U-SP-01", paused state "WITH_FCR_OFFICER", contact stop true and decision record "DLE-9101"
    When the case record reads the deviations of case "RW-2026-000502" on /api/recovery/deviation/v1
    Then the answer holds one open deviation with code "X3", label "Deceased customer", handler "U-SP-01", raised date 2026-12-10, return point "WITH_FCR_OFFICER", contact stop true and decision record "DLE-9101"
    Then the answer holds no customer name, no contact value and no free-text note
    Then the answer is returned in one hop inside 2 seconds

  Scenario: AC2 A cleared deviation and the case-level markers (new, D-RCV-60)
    Given case "RW-2026-000505" holds deviation "X1" raised on 2026-12-05 and cleared on 2026-12-14 with outcome "RETURNED" and no open deviation
    When the case record reads the deviations of case "RW-2026-000505"
    Then the answer holds the cleared deviation with its cleared date 2026-12-14 and outcome "Returned"
    Then the case-level marker anyOpen is false, openCount is 0 and contactStopActive is false
    Then the stage clock pause marker is absent because no row is open

  Scenario: AC3 Two deviations and the hold until the last one clears (new, D-RCV-60)
    Given case "RW-2026-000504" holds open "X1" raised on 2026-12-05 and open "X3" raised on 2026-12-08, each with its own handler and decision record
    When the case record reads the deviations of case "RW-2026-000504"
    Then both deviations show with their own handler, their own decision record and their own raised date
    Then anyOpen is true and openCount is 2
    Then when "X1" is cleared on 2026-12-14 the answer holds "X3" open and "X1" cleared on 2026-12-14, and anyOpen stays true
    Then when "X3" is cleared the answer holds both rows cleared and anyOpen is false

  Scenario: AC4 The clock effect the deviation has on the case (new, D-RCV-60)
    Given case "RW-2026-000502" holds open "X3" raised on 2026-12-10 with contact stop true and no other open row
    When the case record reads the deviations of case "RW-2026-000502"
    Then stageClockPausedSince is 2026-12-10, the raised date of the earliest open row
    Then the answer states that the prescription clock is not paused by any deviation row
    Then contactStopActive is true because an open row carries contact stop true, and it is false when no open row does
    Then neither the pause date nor the contact stop is derived from the code of the row

  Scenario: AC5 The deviation service level and its breach marker (new, D-RCV-60)
    Given the rwb-case reference-data contract mock returns the deviation service-level row of 10 working days with its calendar in force
    Given case "RW-2026-000502" holds open "X3" raised on 2026-12-10
    When the case record reads the deviations of case "RW-2026-000502"
    Then the open row carries slaDueAt computed from 2026-12-10 and that row, and slaBreached false on business date 2026-12-15
    Then with the same rows and a business date after slaDueAt the marker slaBreached is true and the row state is still unchanged
    Then a change of the service-level row alone changes slaDueAt and no code changes
    Then an open row with no service-level row in force is served without slaDueAt and the rest of the answer stands

  Scenario: AC6 The escalation timer of the deviation (new, D-RCV-60)
    Given DeviationWorkflow runs for case "RW-2026-000502" on queue rwb-deviation with open "X3" raised on 2026-12-10
    When the service-level timer of the row elapses on the test clock
    Then the EvaluateRules activity evaluates R-DEV-20 and the RecordAndApply activity writes the deviation decision record
    Then the deviation state stays DEV_WITH_OWNER, the case status does not change and no service-level timer of the case is touched
    Then when "X3" is cleared before the timer elapses, the timer is cancelled and no decision record of the escalation exists
    Then when the decision record cannot be written, nothing of the escalation is kept and the incident path is used with MSG-P7-003

  Scenario: AC7 The budget, the refusal and the boundary (new, D-RCV-60)
    Given the rwb-case reference-data contract mock does not answer for 3 seconds
    When the case record reads the deviations of case "RW-2026-000502"
    Then the call answers 503 with MSG-GEN-006 inside the 2 second budget and no partial deviation list
    Given the rwb-access contract mock returns no Case record right R for the viewing identity
    When that identity reads the same case
    Then the call is refused with 403 and MSG-P4-002 and no deviation is returned
    Then the service reads no table outside rwb_deviation and holds no grant on a v_ace_ view

  Scenario: AC8 A caseId that is absent or malformed (new, D-RCV-60)
    When the case record reads the deviations with no caseId, or with a caseId that is not a case reference
    Then the call answers 422 with MSG-GEN-001 and no row is read
    Then nothing is written

  Scenario: AC9 An open row with no label in the version in force (new, D-RCV-60)
    Given case "RW-2026-000502" holds open "X1" raised on 2026-12-10 and LOV-DEVIATION in force holds no label for "X1"
    When the case record reads the deviations of case "RW-2026-000502"
    Then the row is served with the code "X1" as its label and the marker "unmapped"
    Then the rest of the answer stands and no message is returned for the row

  Scenario: AC13 The rules with no other criterion hold on the answer (new, D-RCV-60)
    Given case "RW-2026-000502" holds open "X3" raised on 2026-12-10 with handler "U-SP-01" and decision record "DLE-9101"
    When the case record reads the deviations of case "RW-2026-000502" twice on business date 2026-12-15
    Then the two answers are identical and no row is written
    Then the answer carries the decision record reference "DLE-9101" and this service resolves no approver
    Then stageClockPausedSince is 2026-12-10 and neither the pause date nor the contact stop is derived from the code of the row
    Then the service publishes no event and makes no call to rwb-case beyond the reference read
    Then a synthetic personal value placed in handler_user_id or in a free-text column appears in neither the JSON, the log nor the span attributes
    Then the answer is built from rwb_deviation only and no foreign key leaves the schema

  Scenario: AC14 The error answers 401 and 404 of the provided operation (new, D-RCV-60)
    Given the request to read the deviations of case "RW-2026-000502" carries no Workbench identity
    When the case record calls the read without a Workbench identity
    Then the call answers 401 with message ID Not specified in the source documents (DOR-RWB-S8-E2015-APP-8) and no row is read
    Given the trigger of a 404 answer is Not specified in the source documents (NEWAC-RWB-S8-E2015-APP-AC14)
    When the case record calls the read for that trigger
    Then the call answers 404 with message ID Not specified in the source documents (NEWAC-RWB-S8-E2015-APP-AC14) and no row is read

  Scenario: AC15 An activity that fails or times out is retried (new, D-RCV-60)
    Given DeviationWorkflow runs for case "RW-2026-000502" on queue rwb-deviation with open "X3" raised on 2026-12-10
    When the EvaluateRules activity fails or exceeds its timeout
    Then the activity is retried Not specified in the source documents (NEWAC-RWB-S8-E2015-APP-AC15) times within the timeout Not specified in the source documents (NEWAC-RWB-S8-E2015-APP-AC15)
    Then after the last retry the deviation state stays DEV_WITH_OWNER and the case status does not change
```

The criteria AC1 to AC9 and AC13 to AC15 are new and test only this slice: the deviation section of the record and the deviation's own service level. The legacy criteria AC1 to AC10 of RWB-E2-015 are owned word for word by RWB-P3-E2015-APP, and no legacy criterion text is copied here. Four published values are reused because the sources print them — the code "X3" with the label "Deceased customer" and the return point "WITH_FCR_OFFICER" (legacy AC2), the outcome "Returned" of a cleared X1 (legacy AC7), the contact stop of X1 to X3 (BR5, R-UNI-04 to R-UNI-06) and the decision log entry "DLE-9101" that holds the approver (legacy AC2, BR9) — and each is asserted on this service's answer, not on the screen. Two points are recorded rather than smoothed over: the read is not in the Ownership Map (GAP-3099; ASM-5288), and the labels of the codes other than X3 and the value of the deviation service level are not printed by any source read here (ASM-5291; ASM-5292).

### 8. Business rules

| BR ID | Rule | Route set | Codes | From state | Event | To state | What this story does with it | Source |
|---|---|---|---|---|---|---|---|---|
| BR3 | R-DEV-01 | Deviations | X1 to X7 | ANY_STATE | DEVIATION_FLAGGED | DEV_FLAGGED | Explains each open row the record shows: the stage clock is paused from `raised_at` and the prescription clock is not | FSD S8 A2.2.3.1; TSD S8 T4 |
| Not specified in the source documents (DOR-RWB-S8-E2015-APP-4) | R-DEV-08 | Deviations | Not specified in the source documents (GAP-3099; ASM-5293) | DEV_REJECTED | CLOCK_RESUMED | RESUMED | The return point of a cleared row is `paused_state`, the state the case resumes into | FSD S8 A2.3.3.1; TSD S8 T4 |
| Not specified in the source documents (DOR-RWB-S8-E2015-APP-4) | R-DEV-18 | Deviations | X1 to X7 | DEV_RESOLVED | CLOCK_RESUMED | RESUMED | A cleared row keeps its state and its cleared date; the answer shows both and the timer is cancelled | FSD S8 A2.2.3.1, A2.3.3.1; TSD S8 T4 |
| Not specified in the source documents (DOR-RWB-S8-E2015-APP-4) | R-DEV-20 | Deviations | Not specified in the source documents (GAP-3099; ASM-5292) | DEV_WITH_OWNER | SLA_BREACHED | DEV_WITH_OWNER | The service-level timer of the deviation fires, records the decision and moves nothing; the answer shows `slaBreached` | TSD S8 T4; Arch v5 slide 8 notes |
| BR4 | R-UNI-04, R-UNI-05, R-UNI-06 | Universal | X1 to X3 | Any | Any | Unchanged | The answer carries the contact stop of each row and the case-level marker; it sets no stop itself | Legacy BR5; CTL-16 |
| BR4 | R-UNI-43 | Universal | X1 to X7 | Any | Any | Unchanged | `anyOpen` is true while any row is open, so the record leaves on hold only when the last one clears | Legacy BR6; FEAT-DVH-09 |

The two text rows of R-DEV-01 and R-DEV-18 are those of the FSD, copied character for character. R-DEV-08, R-DEV-20 and R-UNI-43 are rows of the same route sets; R-DEV-20's codes are not printed by any source read for this slice, so they are not guessed.

| ID | Rule | Source |
|---|---|---|
| BR1 | The answer is built from `deviation` in `rwb_deviation` only; no `recovery_case` row, no `rwb_case` table, no `v_ace_*` view and no table of another service is read, and no foreign key leaves the schema | DP-01; context pack ownership rows; TSD S8 T3.1, T3.3 |
| BR2 | The answer carries references, codes, labels, dates, booleans and outcome values, and no customer name, contact value, free-text note or document field value | Template and Rules §R7.2 (s17); TSD S8 T6.2; legacy section 11 |
| BR3 | A deviation pauses the stage clock and keeps the prescription clock running; the pause date the answer carries is the `raised_at` of the earliest open row and no row of this service pauses the prescription clock | R-DEV-01; REQ-DVH-002; legacy BR3; Arch v5 slide 8 |
| BR4 | The case-level marker `anyOpen` is true while any deviation of the case is open, and `contactStopActive` is true when an open row carries `contact_stop` true; neither is derived from the code of a row | Legacy BR4, BR5, BR6; R-UNI-04 to R-UNI-06; R-UNI-43 |
| BR5 | The label of a code, the label of an outcome, the deviation service-level row and the business date are reference data read with their version; none of them is a constant, a default or a branch in the module | FSD S8 BR-S8-001, BR-S8-002; TSD S8 T3.2; DP-07 |
| BR6 | The approver of a deviation is not stored here: the answer carries the decision record reference of the row and the approver is resolved on the decision log of P7 by the caller | Legacy BR9; REQ-DRI-001; TSD S8 T5.2 |
| BR7 | This service publishes no event of this slice: EV-06 and EV-07 stay with the raise and clear steps, and the escalation of the service level is a local decision record on `rwb.decision-record.v1` | DP-03; DP-09 as a prohibition; TSD S8 T5.3 |
| BR8 | The read is idempotent: the same request on the same rows, the same reference data and the same business date answers the same values and writes nothing | Legacy AC10; TSD S8 T-A.1 |

BR1 and BR2 are property tests over the serialised answer: a synthetic personal value placed in `handler_user_id` or in a free-text column must not appear in the JSON, the log or the span attributes. BR3 and BR4 are executed by the two projections, which read the rows and never a code; a build check fails on a code-to-boolean map. BR5 is executed by the reference client, which is asked for the version in force on every request. BR7 is a prohibition checked by the same build: no outbox write on this slice and no call to rwb-case beyond the reference read.

### 9. State transitions

None for the case. This story changes no case status and no deviation state: it reads the rows another step writes and adds one timer that leaves the deviation where it is (R-DEV-20, `DEV_WITH_OWNER` to `DEV_WITH_OWNER`). `DEV_FLAGGED`, `DEV_WITH_OWNER`, `DEV_RESOLVED`, `DEV_REJECTED` and `DEV_REROUTE` stay with the raise, routing, handling and clear steps of this service (TSD S8 T4).

| Read or step | Event | Condition | Result |
|---|---|---|---|
| The read request | The viewer's identity and the case | Case record right R granted | The rows of the case are answered; nothing is written |
| The read request | A case this service holds no deviation for | The right is granted | An empty list with 200; the case row is not confirmed here |
| The clock projection | The earliest open row | At least one row is open | `stageClockPausedSince` is its `raised_at`; the prescription clock is untouched |
| The service-level timer | `raised_at` plus the service-level row | The row is still open | R-DEV-20 fires; the decision record is written; the state stays `DEV_WITH_OWNER` |
| The service-level timer | The clear of the row | The timer has not fired | The timer is cancelled; no escalation record exists |
| The read request | A cleared row | `cleared_at` is set | The row is answered with its cleared date and outcome, not counted in `openCount` |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Case record CRU (TSD S8 T6.1): reads the deviation section of the case record in scope Own |
| RW-TEAMMGR, team manager | Case record R: reads the same section in scope Team |
| RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LEGAL, RW-LITOFF | Case record R or RU: read the deviation section of a case they hold or may see |
| RW-AUDIT, RW-COMPLY, RW-CONDUCT | Case record R: read the section in scope All |
| SY-CASEWF, case workflow module | Case record CRU: reads the same answer on behalf of a workflow; holds no write right on this read |
| rwb-deviation service identity (the service login, DP-02) | Serves the read, reads `deviation` in `rwb_deviation` and the reference data, runs the service-level timer and writes its local decision record; holds no grant on another schema and no `v_ace_*` grant |
| gateway-bff composite route | Merges this answer into the case record of DP-19 with the viewer's own identity; holds no right of its own |

The rights are the rows of TSD S8 T6.1 and the declared right of the read in TSD S8 T-A.1. The approver's identity is not returned by this service: the answer carries the decision record reference and the caller resolves the approver on the decision log of P7, so no Decision log right is needed here (legacy section 10).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 | deviation (S8, `rwb_deviation`) | id | Read, the deviation reference of the answer |
| DF-CAS-037 | deviation (S8, `rwb_deviation`) | case_id | Read, the case reference of the answer |
| DF-CAS-038 | deviation (S8, `rwb_deviation`) | deviation_code | Read, the code and the key of the label |
| DF-CAS-039 | deviation (S8, `rwb_deviation`) | raised_at | Read, the pause date and the start of the service level |
| DF-CAS-040 | deviation (S8, `rwb_deviation`) | raised_by | Read, not returned: the record does not show who raised it |
| DF-CAS-041 | deviation (S8, `rwb_deviation`) | paused_state | Read, the return point of the row |
| DF-CAS-042 | deviation (S8, `rwb_deviation`) | handler_user_id | Read, the handler identity of the row |
| DF-CAS-043 | deviation (S8, `rwb_deviation`) | contact_stop | Read, the per-row stop and the case-level marker |
| DF-CAS-044 | deviation (S8, `rwb_deviation`) | cleared_at | Read, to separate an open row from a cleared one |
| DF-CAS-045 | deviation (S8, `rwb_deviation`) | outcome | Read, resolved to its label on LOV-DEV-OUTCOME |
| Standard columns | deviation (S8, `rwb_deviation`) | `is_active`, `state`, `version` | Read; `state` is the row state the answer returns |
| DF-CAS-019 | recovery_case (P3) | deviation_open | Not read and not written: the case row and its flag are rwb-case's |
| DF-WRK-027 to DF-WRK-036 and DF-WRK-041 to DF-WRK-044 | timer (P3) | expired, paused, escalation fields | Not read: the case timers are rwb-case's and are the subject of RWB-P3-E2015-APP |
| DF-WRK-037 to DF-WRK-038 | queue (owner Not specified in the source documents (CG-ALL-11357)) | Not specified in the source documents (CG-ALL-11357) | Not read: not used by this story |
| DF-WRK-039 to DF-WRK-040 | assignment (owner Not specified in the source documents (CG-ALL-11357)) | Not specified in the source documents (CG-ALL-11357) | Not read: not used by this story |
| DF-DEC-010 | decision_log_entry (P7) | approver_user_id | Not read here; the answer carries the decision record reference and the caller resolves the approver |
| DF-CAS-017 | recovery_case (P3) | prescription_date | Not read: the prescription date is rwb-case's |

Field IDs are those of TSD S8 T3.1 and the Logical Data Model and Data Dictionary. **No write to a business table and no new column**: the one migration of this story creates a read-only view and an index in `rwb_deviation` (DP-15), and the only write is a decision record of the escalation through the library of DP-03. The label of a code and the label of an outcome are rows of LOV-DEVIATION and LOV-DEV-OUTCOME at the version in force; the sources read print the label of X3 only and no field ID for a label, which is recorded (GAP-3099; ASM-5291).

No personal data. The answer carries identifiers, codes, labels, states, dates, outcome values and booleans, and the class of each field read in this section is set in Data Classification v5; the class of handler_user_id (DF-CAS-042) is Not specified in the source documents (DOR-RWB-S8-E2015-APP-11). No customer name, address, contact value or identity number enters the answer, a log, a trace or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13).

| Method | Path | Query | Answer | Access | Idempotency |
|---|---|---|---|---|---|
| GET | `/cases/{caseId}/deviations` | none | The deviation section of the case record: every deviation of the case, open and cleared, with the case-level markers and the service-level state of each open row | Case record right R, scope applied | Idempotent read; no `Idempotency-Key` needed |

The answer is one object. `deviations` carries, per row, `deviationId`, `caseId`, `deviationCode`, `deviationLabel`, `state`, `raisedAt`, `handlerUserId`, `pausedState`, `contactStop`, `clearedAt`, `outcome`, `outcomeLabel`, `decisionRecordId`, `slaDueAt` and `slaBreached` — the TSD S8 T3.1 columns of `deviation` plus the resolved labels, the decision record reference and the two derived service-level values. `clock` carries `stageClockPausedSince` and states that the prescription clock is not paused. The case-level values are `openCount`, `anyOpen` and `contactStopActive`. Errors: 401 no Workbench identity (message ID Not specified in the source documents (DOR-RWB-S8-E2015-APP-8)), 403 Case record right R absent (MSG-P4-002) or case outside the scope, 422 `caseId` absent or malformed (MSG-GEN-001), 503 a reference read does not answer inside the budget (MSG-GEN-006). A case with no deviation answers an empty `deviations` array, `openCount` 0 and `anyOpen` false, with 200.

The Ownership Map gives S8 two operations, `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` (API-S8-001, API-S8-002), and no read, while legacy section 12 calls `DeviationQuery.forCase` on the record path. The read is therefore declared here with a gap and an assumption (GAP-3099; ASM-5288), and the two write operations stay with the raise and clear stories of this service. The Architecture v5 naming of the clear operation differs from the Ownership Map naming; both names and the owner of the case-record read (solution architect) are open questions, settled in the S8 contract story before the screen is built.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Use |
|---|---|---|---|
| The reference-data read of RWB-PLT-E1043-CON, as the contract RWB-P3-E1043-CON publishes (operation name Not specified in the source documents (GAP-3099; ASM-5291)) | `/api/recovery/case/v1` | P3 rwb-case | LOV-DEVIATION with its labels, LOV-DEV-OUTCOME with its labels, the deviation service-level row with its calendar, and the business date, at the version in force; faked, cached per request |

One row, one hop, 2 s timeout and a breaker (ADR-020). It is a class C dependency in fact that the plan does not hold: the plan's C row is `RWB-P3-E2015-CON`, the case-record contract this answer is built against, and the reference read arrives with the platform library of DP-07 (GAP-3099; ASM-5294). The case-record contract fixes the operation the record calls, the deviation view it expects and the 2 s budget; the fields of that view which the legacy story does not print are named here and recorded (ASM-5289).

#### 12.3 Events published

None on the service topic. This slice writes no outbox row: `rwb.deviation.DeviationRaised.v1` (EV-06) and `rwb.deviation.DeviationCleared.v1` (EV-07) on `rwb.deviation.events.v1` belong to the raise and clear steps of this service (DP-09 as a prohibition; DP-14 as naming). The one write of this slice is a local decision record of the escalation, written by the library of DP-03 to the shared topic `rwb.decision-record.v1`; the record's fields and its event name are the library's and are not restated here.

#### 12.4 Events consumed

None. This story subscribes to no topic, holds no consumer group and writes no inbox row: the deviation section is read on request and the service-level timer is a workflow timer of this service, not an event. The inbox table of DP-09 is present in `rwb_deviation` for the consumers other stories of this service add.

#### 12.5 Workflows and activities

`DeviationWorkflow` on task queue `rwb-deviation` in namespace `rwb-recovery` (the service's one workflow; Arch v5 slide 13). This story contributes one durable timer and no new workflow: the service-level timer of the deviation, started when the raise step starts the workflow.

| Step | Type | What it does |
|---|---|---|
| The service-level timer | Durable timer | Waits from `raised_at` to the deviation service level of the reference-data row; cancelled by the clear |
| `EvaluateRules` | Activity (kit) | Evaluates R-DEV-20 on the package version in force in the embedded kit; the case status is not in its input |
| `RecordAndApply` | Activity (kit) | Writes the escalation into the local decision record and the record reference in one transaction; on failure the step is retried and then surfaced as MSG-P7-003 |

#### 12.6 Schedules

None. The deviation service level is a timer of `DeviationWorkflow`, not a Temporal Schedule, and the ownership rows give this service no job (Jobs 0). Nothing of this slice runs on the bank's Airflow chain.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| deviation | S8 (`rwb_deviation`) | Read only: every row of the case, open and cleared |
| v_case_deviation | S8 (`rwb_deviation`) | Read only view over `deviation`, created by this story's migration for the case read and its index (DP-15) |
| decision record (DP-03 library) | PLT library, created in `rwb_deviation` | Written by the `RecordAndApply` activity of the escalation only; the physical table name is the library's |
| outbox_event | PLT library, created in `rwb_deviation` | Present for the raise and clear steps; this slice writes none of its rows |
| processed_event | PLT library, created in `rwb_deviation` | Present for the consumers of other stories; this slice writes none of its rows |

Not owned and never read as a table: `recovery_case`, `timer`, `task` and `deviation_open` (P3), the `v_ace_*` views and the interaction ledger (P1), `decision_log_entry` (P7). No foreign key leaves `rwb_deviation`; `case_id`, `handler_user_id` and the decision record reference are references, not keys across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documents | Used by |
|---|---|---|
| RWB-P3-E2015-CON case-record fake | The deviation view the record expects, the operation it calls and the 2 s budget; a case with no deviation and a case outside the scope | AC1, AC2, AC7 |
| rwb-case reference-data fake | LOV-DEVIATION with the X3 label, LOV-DEV-OUTCOME, the deviation service-level row with its calendar, the business date; a code with no label, an outcome with no label and no service-level row | AC1, AC5, X7 |
| rwb-access decision fake | A granted Case record right R for the case owner, a refused decision for an identity without it, and a scope that excludes one case | AC7, X1 |
| gateway-bff composite route fake | The record of `RW-2026-000502` with its deviation section in the open and the cleared state | AC1, AC2, AC3 |
| Test clock and workflow harness | The service-level timer elapsing, being cancelled by a clear, and the decision-record write failing | AC6, X4 |

The fakes are test-only and are replaced by the real services in SIT. No fake carries personal data: every deviation in the fixtures is synthetic and every field of a customer is absent from them.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 1 consumed | `GET /cases/{caseId}/deviations` on `/api/recovery/deviation/v1`; the reference-data read of rwb-case, one hop with 2 s and a breaker |
| Kafka | 0 published, 0 consumed | No service event of this slice; the escalation goes to the shared decision-record topic through the library |
| Temporal | 1 workflow, 1 timer, 2 activities | `DeviationWorkflow` on queue `rwb-deviation`: the service-level timer, `EvaluateRules`, `RecordAndApply`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.deviation`, module `case-record-projection`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DeviationGuard` | Guard | The Case record right of the read from the cached decision of rwb-access, the scope check and the problem mapping of section 14 |
| `CaseDeviationReader` | Repository | Reads every `deviation` row of the case in `rwb_deviation` with the columns of §11 and no other table |
| `DeviationLabelResolver` | Service | Resolves the label of each code on LOV-DEVIATION and of each outcome on LOV-DEV-OUTCOME at the version in force, with the "unmapped" marker |
| `DeviationClockProjection` | Service | Derives `openCount`, `anyOpen`, `contactStopActive` and `stageClockPausedSince`, and states that the prescription clock is untouched |
| `DeviationSlaProjection` | Service | Derives `slaDueAt` and `slaBreached` from `raised_at`, the service-level row and the business date |
| `CaseDeviationAssembler` | Service | Builds the answer of 12.1 with no personal data and no half-labelled row |
| `DeviationSlaTimer` | Workflow timer and activities | The durable service-level timer of `DeviationWorkflow`, its cancellation on a clear, `EvaluateRules` for R-DEV-20 and `RecordAndApply` for the decision record |
| `ReferenceDataClient` | Client | The reference-data read of rwb-case, one hop, 2 s, breaker, cached for the request |

**Database and migrations.** One step in the per-service Flyway sequence of `rwb_deviation` (DP-15): `V2015_1__case_deviation_read.sql`, which creates the read-only view `v_case_deviation` over `deviation` (the columns of §11 with the open flag) and one index on `(case_id, cleared_at)`. No business table, no column and no constraint is added, and no migration of this service touches another schema or the shared baseline. The view name and the step number are design choices fixed by no source document (ASM-5295).

**Configuration and reference data.**

- The codes, their labels, the outcome values, the service-level row, its calendar and the business date are rows read at the version in force on the reference-data contract; none is a constant of the module (DP-07, BR5). The label of X3 and the ten working days of the slide 8 note are the only values printed for this slice (ASM-5291, ASM-5292).
- The escalation the timer records is R-DEV-20 of the DEV package; the package version is read on the registry through the kit, so the rule is never copied into this service.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.
- The flag `rwb.deviation.case-record-projection` is a flag of the platform library: off means the read answers 404 to every caller and the record shows its Epic 1 fields only, while the deviation estate and the timer of the service are unchanged.

**Build steps**

1. The view and its index in the service's Flyway sequence, applied on an empty `rwb_deviation` and on a loaded one (AC1, AC2, DP-15).
2. `CaseDeviationReader` with the open and cleared filters and the columns of §11; unit tests for AC1 and AC2.
3. `DeviationLabelResolver` and `DeviationClockProjection` over the reference-data fake; unit tests for AC1, AC3 and AC4.
4. `DeviationSlaProjection` and the service-level row, with the business date, the row that changes alone and the row that is absent; unit tests for AC5 and X7.
5. `DeviationSlaTimer` on the test clock, with the firing path, the cancellation and the failing decision record; tests for AC6 and X4.
6. `CaseDeviationAssembler` and the operation with the guard, the scope check, the empty case and the timeout; API tests for AC1, AC2 and AC7.
7. The property test that places a synthetic personal value in `handler_user_id` and in a free-text fixture and asserts that it appears in no answer, no log line and no span attribute (BR2).
8. The build check that fails on a code, a label, an outcome, a service-level value or an escalation role in the source, and on any statement outside `rwb_deviation` (BR5, BR1, X5).

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

This is a secondary slice: the metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P3-E2015-CON` exactly as the Work Package fixes them, so the six platform contracts that DP-03, DP-07, DP-10, DP-14, DP-15 and DP-19 name arrive with the service template and are not written into the H row (GAP-3099; ASM-5294).

- **DP-11** is the whole point of the slice: `DeviationQuery.forCase` of the legacy section 12 becomes a REST read with a mock, one hop and 2 s, and the record is built against the published contract and its fake, never against a table. **DP-13** gives the read its base `/api/recovery/deviation/v1`.
- **DP-01** keeps the answer inside `rwb_deviation`; a statement on `rwb_case`, which rwb-case owns, or on a `v_ace_*` view fails the boundary test. **DP-15** puts the view and its index in the per-service Flyway sequence, never in the shared baseline.
- **DP-07** is the labels, the outcome values, the service-level row and the business date at their version; nothing of them is coded, which is what keeps a label change from being a release. **DP-03** is the local decision record of the escalation, so the approver of a deviation decision is resolvable on the decision log without this service storing it (BR6). The approval the FSD names is a step inside DeviationWorkflow taken by the role the code assigns; the decision-record library writes its entry and hash, and no P7 ApprovalWorkflow edge is added here (GAP-1820).
- **DP-10** replaces the legacy Quartz timer of the deviation service level with a durable timer in `DeviationWorkflow`; the ownership rows give the service no job, and the timer survives a restart, which is what makes R-DEV-20 trustworthy on a case that runs for months. **DP-14** keeps the two service events on `rwb.deviation.events.v1` and is applied as naming only, because this slice publishes none.
- **DP-19** is the route the record is composed on: SCR-03 merges the case answer of rwb-case with this answer, and no route calls a service that calls another.

**Done when.** The tests of section 16 pass, the answer of `RW-2026-000502` carries X3 with its label, handler, return point and contact stop, a cleared row shows its cleared date and outcome, `anyOpen` is false only when every row is cleared, the service-level due date changes with the row alone, the timer fires R-DEV-20 without moving the case and is cancelled by a clear, an identity without the right is refused with MSG-P4-002, the migration applies cleanly on an empty `rwb_deviation`, and no statement outside the schema exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The viewing identity holds no Case record right R (X1, AC7) | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | The `caseId` is absent or malformed (X2) | Enter {field}. |
| MSG-GEN-006 | The reference data or the business date does not answer inside the budget (X3, AC7) | {system} is not available. Try again in a few minutes. |
| MSG-P7-003 | The decision record of the escalation cannot be written (X4, AC6) | Not specified in the source documents (GAP-3099; ASM-5297) |
| None | An open row with no service-level row in force, or a code with no label (X7) | No message: the row is served without `slaDueAt` or with the code as its label and the marker "unmapped" |

The four IDs are those of the legacy and FSD message sets, copied unchanged. MSG-P7-003 is published as an identifier only — FSD S8 AC-EXC-S8-002-04 gives its behaviour ("nothing changes; MSG-P7-003; incident raised") and the Error Handling and Resilience Standard gives the same, but no source read prints its user text, so the text is recorded as missing and the id travels with the platform error envelope. For MSG-P4-002, {action} names the action the caller tried — "read the deviations of this case" — and never a case fact. For MSG-GEN-006, {system} is "Reference data" on the one path. Errors are RFC 9457 problem responses with `messageId`, `detail` with the placeholders filled and `instance` naming the request; the HTTP mapping is 403 for MSG-P4-002, 422 for MSG-GEN-001, 503 for MSG-GEN-006 and 503 for MSG-P7-003. MSG-P3-004, MSG-P3-018 and MSG-P4-003 (the on-hold banner, the empty timer section and the case out of scope) are RWB-P3-E2015-APP's and are not restated here.

### 15. Screens and states

No screen is owned by this story. The read feeds the deviation section of SCR-03 Case record, which is rwb-case's screen and is composed by the gateway-bff composite route of DP-19; the states it serves are these.

| Screen | State | What this answer supplies |
|---|---|---|
| SCR-03 Case record | Loading | Nothing: the route shows skeleton rows until the answer or the budget ends |
| SCR-03 Case record | Read only | Each deviation with its code, label, handler, raised date, return point, contact stop, cleared date, outcome and service-level state |
| SCR-03 Case record | On hold | `anyOpen` true, `openCount`, `contactStopActive` and the pause date; the banner text with MSG-P3-004 is rwb-case's |
| SCR-03 Case record | Deviation read failed | Nothing: on 503 the route shows MSG-GEN-006 for the section and the record keeps its case fields, including the deviation flag of rwb-case |
| SCR-03 Case record | Empty | Not specified in the source documents (CG-ALL-11366) |
| SCR-03 Case record | Error | Not specified in the source documents (CG-ALL-11366) |
| SCR-03 Case record | No access | Not specified in the source documents (CG-ALL-11366) |
| SCR-06 Raise deviation | Empty | Not specified in the source documents (CG-ALL-11367) |
| SCR-06 Raise deviation | Loading | Not specified in the source documents (CG-ALL-11367) |
| SCR-06 Raise deviation | Error | Not specified in the source documents (CG-ALL-11367) |
| SCR-06 Raise deviation | No access | Not specified in the source documents (CG-ALL-11367) |
| SCR-08 Deviation queue | Empty | Not specified in the source documents (CG-ALL-11368) |
| SCR-08 Deviation queue | Loading | Per Screen Specifications v1 section SCR-08 (CG-ALL-11368) |
| SCR-08 Deviation queue | Error | Not specified in the source documents (CG-ALL-11368) |
| SCR-08 Deviation queue | No access | Not specified in the source documents (CG-ALL-11368) |

The deviation screens of this service — SCR-06 Raise deviation and SCR-08 Deviation queue — belong to its other stories and are unchanged here. Both are carried as gateway-bff composite routes at the edge (DP-19) over this service's read and command contract; their owner is Not specified in the source documents (GAP-1830), and the read operation and composite route are confirmed with the platform edge owner before the wave 2 screen test.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-015-02 | AC2 for the deviation half: the code, label, handler, pause date, return point, contact stop and decision record of the open row. The banner and the prescription date on the screen belong to RWB-P3-E2015-APP | Component | X3 raised 2026-12-10 on case RW-2026-000502, handler U-SP-01, return point WITH_FCR_OFFICER, contact stop true |
| TC-E2-015-05 | AC5 for the deviation half: two open rows with their own handler and decision record, and the markers after the first clears. The screen staying on hold belongs to RWB-P3-E2015-APP | Component | X1 raised 2026-12-05 and X3 raised 2026-12-08 on case RW-2026-000504; X1 cleared 2026-12-14 |
| TC-E2-015-06 | AC6 for the deviation half: the pause date of the open row and the statement that the prescription clock is untouched. The paused service-level timer itself belongs to RWB-P3-E2015-APP | Component | X3 open since 2026-12-10 on case RW-2026-000502 |
| TC-E2-015-07 | AC7 for the deviation half: a cleared row with its cleared date and outcome, and `anyOpen` false. The resumed service-level timer belongs to RWB-P3-E2015-APP | Component | X1 cleared 2026-12-14 with outcome RETURNED on case RW-2026-000505 |
| TC-E2-015-10 | AC10 for the deviation half: the 2 s budget and the 503 with MSG-GEN-006 that lets the caller degrade. The banner fallback belongs to RWB-P3-E2015-APP | Component | Reference-data stub silent 3 seconds; the read answers inside the budget with no partial list |
| TC-E2-015-11 | AC7: an identity holding no Case record right R is refused with 403 and MSG-P4-002, and the boundary test fails on a foreign statement | Component | RW-REFADM reads the deviations of case RW-2026-000502; refused; a statement on rwb_case fails the build |
| TC-E2-015-01 | No criterion here: the case timer, its due date and the owner role of the task belong to RWB-P3-E2015-APP | Component | NOTICE_PERIOD timer on a task owned by RW-LITOFF |
| TC-E2-015-03 | No criterion here: the prescription date and its warning days belong to RWB-P3-E2015-APP | Component | Prescription 60 and 91 days ahead |
| TC-E2-015-04 | No criterion here: the service-level escalation, its role and the next escalation point belong to RWB-P3-E2015-APP | Component | SERVICE_LEVEL expired, level 1, escalated to RW-TEAMMGR |
| TC-E2-015-08 | No criterion here: the empty timer section belongs to RWB-P3-E2015-APP | Component | Case with only stopped timers |
| TC-E2-015-09 | No criterion here: the case out of scope is refused by rwb-case before this read is called | Component | Case of team SME-NTH opened by an MTG-BKK owner |
| TC-E2-015-12 | AC5: the deviation service level and its breach marker, as written in section 7 | Component | X3 raised 2026-12-10 on case RW-2026-000502; service-level row of 10 working days; business date 2026-12-15 |
| TC-E2-015-13 | AC6: the escalation timer of the deviation, as written in section 7 | Component | X3 raised 2026-12-10 on case RW-2026-000502; the service-level timer of the row elapses on the test clock |
| TC-E2-015-14 | Contract test: every operation, event and activity of section 12 | Component | Not specified in the source documents (DOR-RWB-S8-E2015-APP-12) |
| TC-E2-015-15 | Boundary test: the tables of section 12.7 (ASM-3438), the v_ace_* views and the ACE tables | Component | A write to any table not listed in section 12.7 fails the build; a read of a v_ace_* view or an ACE table fails the build |
| TC-E2-015-16 | AC8: a caseId that is absent or malformed answers 422 with MSG-GEN-001 and no read is made, as written in section 7 | Component | caseId absent; a malformed caseId |
| TC-E2-015-17 | AC9: an open row with no label in the version of LOV-DEVIATION in force is served with the code as its label and the marker unmapped | Component | Open X1 raised 2026-12-10 on case RW-2026-000502; LOV-DEVIATION with no label for X1 |
| TC-E2-015-18 | AC13: the rules of section 8 with no other criterion (BR1, BR2, BR3, BR4, BR6, BR7, BR8), as written in section 7 | Component | Open X3 raised 2026-12-10 on case RW-2026-000502 with decision record DLE-9101; two reads on business date 2026-12-15; synthetic personal value in handler_user_id and in a free-text column |
| TC-E2-015-19 | AC14: the 401 answer of section 12.1 and the 404 answer, as written in section 7 | Component | Read with no Workbench identity; 404 trigger Not specified in the source documents (NEWAC-RWB-S8-E2015-APP-AC14) |
| TC-E2-015-20 | AC15: the retry and timeout of a failed or timed-out activity, as written in section 7 | Component | Retry count and timeout Not specified in the source documents (NEWAC-RWB-S8-E2015-APP-AC15) |

The eleven legacy cases of RWB-E2-015 are listed in their legacy order with the Level column added, and each names the slice of behaviour this story answers: the deviation fields for TC-E2-015-02, the two open rows for TC-E2-015-05, the pause date for TC-E2-015-06, the cleared row for TC-E2-015-07, the budget for TC-E2-015-10 and the refusal with the boundary for TC-E2-015-11; every other case is the case side's and is listed with no criterion here. The legacy table publishes no level, so one is assigned per case: legacy "System" maps to Component for a single-service half and to End to end where a case crosses services, and "Access" maps to Component (GAP-3099; ASM-5296). The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID. No `-ITG` copy is written here: the same values across rwb-case, rwb-deviation, rwb-access and P7 are RWB-ITG-E2015-ITG's.

### 17. Guardrails

- No business value in code: the codes, their labels, the outcome values, the service-level row, its calendar and the escalation target are rows or configuration read with their version. A build check fails on a code, a label, a service-level value or an escalation role in the source.
- No personal data in the answer, an event, a workflow input or a log: identifiers, codes, labels, states, dates, outcome values and booleans only. `raised_by` is not returned, and a property test asserts that a synthetic personal value never reaches the JSON, a log line or a span attribute.
- ACE data only through the owner's contract or a `v_ace_*` view: this service holds no `v_ace_*` grant, reads no ACE table and needs no ACE product at all; the case row, the timers and the decision log are read on their owners' contracts.
- The read never changes a case, a timer, a deviation or a decision: the only write of this slice is the escalation's local decision record, written by the workflow activity of the service itself.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-005 | Timers, escalation state and the deviation flag on the case record view | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-05, FEAT-WKM-06 | All recovery processes | R-UNI-31, R-UNI-04, R-UNI-05 | TC-E2-015-02, TC-E2-015-04, TC-E2-015-07 |
| REQ-DVH-002 | A deviation pauses the stage clock and keeps the prescription clock running | Business Requirements Epic 2, section 4; Program, section 5.15 | FEAT-DVH-02, FEAT-DVH-03, FEAT-DVH-06, FEAT-DVH-09 | 11 Handle customer care and deviations | R-DEV-01, R-DEV-18, R-UNI-43 | TC-E2-015-02, TC-E2-015-06, TC-E2-015-07 |
| REQ-WKM-004 | A breached service level visible to the escalation role without the case moving | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-07 | All recovery processes | R-UNI-30, R-DEV-20 | TC-E2-015-04, TC-E2-015-06, TC-E2-015-07 |
| REQ-DRI-001 | The approver of a decision is the approver on its decision log entry | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-06 | 11 Handle customer care and deviations | R-DEV-20 | TC-E2-015-02 |

The requirement rows are the four of the legacy key; this slice answers their deviation half and names the case half in RWB-P3-E2015-APP. R-DEV-20 is the only rule of the DEV route set this story executes; the rest are read to explain what the row shows.

### 19. Out of scope

- Raising, routing, handling and clearing deviations (SCR-06 and SCR-08; the Epic 1 and Epic 7 stories of this service).
- The case timers, the service levels, the prescription date and its warning, and the escalation of the case (RWB-E1-028, RWB-P3-E2015-APP, RWB-P3-E2015-OPS).
- The approver of the deviation decision, which is resolved on the decision log of P7 by the caller.
- The access decision and the reference-data and parameter estate of rwb-case (RWB-P4-E2015-APP, RWB-E1-043).
- The history timeline on the case (RWB-E2-016) and the next action panel (RWB-E2-035).
- The end-to-end proof across rwb-case, rwb-deviation, rwb-access and P7 (RWB-ITG-E2015-ITG).
