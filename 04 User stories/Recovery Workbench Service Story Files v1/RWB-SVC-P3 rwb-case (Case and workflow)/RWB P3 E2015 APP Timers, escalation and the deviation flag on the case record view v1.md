# RWB-P3-E2015-APP Timers, escalation and the deviation flag on the case record view

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2015-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-AD |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P3-E2015-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1028-CON, RWB-P3-E1035-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | RWB-P3-E2015-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-014, FR-P3-015, FR-P3-016, FR-P3-019, FR-P3-020, FR-P3-021, FR-P3-022) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-015 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the case record view to show every timer of the case with its due date, status, warning state and escalation path, the prescription date, and any deviation flag with its handler, its approver and its return point, served by rwb-case from its own timer and case rows, the rwb-deviation contract and the rwb-decision decision log**, so that **the next deadline and the reason a case left its path are visible on the case without reading another team's list**.

The two read operations of this story are `GET /api/recovery/case/v1/cases/{caseId}`, which now carries `deviations[]` and `deviationsAvailable`, and `GET /api/recovery/case/v1/cases/{caseId}/timers`, which now carries `nextStepOwnerRole`, `escalatedToRole`, `escalatedAt`, `nextEscalationRole` and `inWarning`. The clock itself is no longer a five-minute job: it is a durable Temporal timer inside CaseWorkflow on task queue `rwb-case`, owned by RWB-P3-E1028-APP, and this story renders what that timer and the deviation service record.

### 2. Business rationale

Deadlines are agreed by email today, and litigation was not filed for debtors who met the criteria because nobody saw the prescription date in time (control CTL-18). A deviation pauses the stage clock but never the prescription clock (REQ-DVH-002), so the case owner must see both, with who holds the deviation, who approved it and where the case returns. This story puts every timer, the escalation state and the deviation flag on the case record view and meets REQ-WKM-004, REQ-WKM-005, REQ-DVH-002 and REQ-DRI-001. The measure is that every open case's record view shows its next due date and its prescription date, and that the escalation state of a breached service level is readable without the case moving.

In the target the monolith's single screen model is split into one composite route at the edge and two answer sources behind it (DP-19). gateway-bff calls rwb-case twice, for the case and for the timers, in parallel with rwb-source-data for the account and customer facts, and merges the three answers into the screen model (Architecture v5 slide 10). rwb-case itself does not chain: it reads its own `recovery_case`, `timer` and `task` rows, then calls rwb-deviation once for the deviations of the case and rwb-decision once for the approvers on their decision log entries (Architecture v5 slide 13, P3 row: R to P4, R to P7, T and E to S8). A deviation that cannot be read inside the two-second budget degrades the deviation section only, and the on-hold banner still shows from `recovery_case.deviation_open`, so a slow deviation service never hides the next deadline.

The legacy `timer` row keeps its place: it stays an rwb_case projection behind the timers operation, while the clock that fires is a durable Temporal timer inside CaseWorkflow (DP-10). JOB-05 Timer check and the TimerDue event are retired (Architecture v5 slides 42 and 44); TimerBreached stays the nineteenth event of the catalogue on `rwb.case.events.v1`. The two escalation fields the legacy escalation step wrote, `timer.escalated_to_role` and `timer.escalated_at`, are written by the timer story RWB-P3-E1028-APP in the same schema, so this story is a reader with no write path of its own.

### 3. Preconditions

- RWB-P3-E2015-CON is published: the OpenAPI 3.1 document of the two read operations with the added response fields, the composed deviation object, the error envelope and the three contract fakes.
- RWB-P3-E1035-CON is published: the case record view contract that fixes the shape of the case resource this story extends, so the added fields sit on one agreed resource and not on a second copy of it.
- RWB-P3-E1028-CON is published: the timer story's contract, which fixes the meaning of `warn_at`, `expires_at`, `escalated_to_role`, `escalated_at`, `nextEscalationRole` and `inWarning`, and the projection the durable timer writes.
- RWB-PLT-E1071-CON is published: the Temporal workflow kit in namespace `rwb-recovery`, so the durable timer that drives the projection runs on task queue `rwb-case` (DP-10).
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract of rwb-case with its client library, so LOV-TIMER, LOV-DEVIATION and the SERVICE_LEVEL escalation roles are read as data with their version (DP-07).
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), so the approver a deviation displays is the approver of the decision record and never a value copied into rwb_case.
- RWB-PLT-E1047-CON is published: the topic and event naming library (DP-14). RWB-PLT-E1044-CON is published: the per-service Flyway sequence in schema `rwb_case` (DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-03 (DP-19). Its path and merge order are owned by that platform contract; this story fixes only the two answers rwb-case returns.
- The `timer` and `task` rows exist for the case, written by RWB-P3-E1028-APP and RWB-P3-E1018-APP; the columns `timer.escalated_to_role` (DF-WRK-043) and `timer.escalated_at` (DF-WRK-044) exist with that story's migration, and this story adds no column.
- SERVICE_LEVEL rows carry the escalation role and the next escalation role for each product group and status, held in the rwb-case reference tables with their version (DP-07).
- `prescription.warning-days` is in force and is applied where `timer.warn_at` is computed (RWB-P3-E1028-APP); this story only reads `inWarning` from that warning point and never recomputes it.
- The person holds a role with Case record R and the case is in the caller's scope; rwb-access answers the authorisation check through its contract, cached per request.
- The login is the rwb-case login (DP-02): one login and one connection pool for the service, with grants on schema `rwb_case` only (Architecture v5 slide 29).

### 4. Flow

1. Case owner: opens SCR-03 Case record for a case at the fixed business date 2026-12-15, reached through the App Gateway at `/recovery/*` and the gateway-bff session (DP-19).
2. gateway-bff: checks the session in Redis and the coarse permission, then calls three owners in parallel, one hop each: rwb-case `GET /api/recovery/case/v1/cases/{caseId}`, rwb-case `GET /api/recovery/case/v1/cases/{caseId}/timers`, and rwb-source-data for the account and customer facts of the case. No service calls another service inside a business step.
3. rwb-case: authorises the read through the rwb-access contract, `POST /api/recovery/access/v1/authorise`, right R on Case record, scope applied, cached for the request.
4. rwb-case, case answer: reads `recovery_case` for `id`, `case_no`, `product_group`, `status`, `prescription_date`, `stage_clock_start`, `deviation_open` and `legal_hold`.
5. rwb-case, case answer: calls rwb-deviation once, `GET /api/recovery/deviation/v1/cases/{caseId}/deviations`, one hop, 2 s timeout and a breaker per downstream (DP-11), and receives the open and the cleared deviations of the case with code, raised date, handler, paused state, contact stop, cleared date and outcome (GAP-0714; ASM-1261).
6. rwb-case, case answer: calls rwb-decision once, `GET /api/recovery/decision/v1/decision-log?caseId={caseId}`, one hop, 2 s timeout, and takes for each deviation the approver on the decision log entry whose decision code matches the deviation code and whose decision time is the raise of that deviation; the answer carries the approver user ID only, never the entry.
7. rwb-case, case answer: merges the deviation rows with their approvers into `deviations[]`, orders them by raised date, and sets `deviationsAvailable` true. When the S8 call times out or fails, it returns the case with `deviationsAvailable` false, an empty `deviations[]` and MSG-GEN-006 in the section, and the banner is still built from `deviation_open`.
8. rwb-case, timer answer: reads the `timer` rows of the case and, for each timer with a task, the `task.owner_role` of that task; it reads no rule row and computes no deadline.
9. rwb-case, timer answer: for each row returns `timerType`, `startedAt`, `expiresAt`, `warnAt`, `paused`, `status`, `escalationLevel`, `nextStepOwnerRole`, the escalated role and time written by the timer story, and `nextEscalationRole` from the SERVICE_LEVEL row for the product group and status in force (DP-07).
10. rwb-case, timer answer: sets `inWarning` true when the business date is on or after `warn_at` and the timer is RUNNING or PAUSED, and false otherwise; it orders the list by `expires_at` ascending.
11. gateway-bff: merges the two rwb-case answers and the rwb-source-data answer into the screen model and returns the screen inside the 2 s budget (Architecture v5 slide 10: about 1.2 s at the 95th percentile).
12. Screen: renders the timers ordered by due date, each with type, due date, status, warning state, escalation level, escalated-to role, escalated time, next escalation point and the owner role of the next step; renders the prescription date with its warning; renders the deviation rows and the On hold banner with MSG-P3-004.
13. Nothing in this flow writes: the two operations are reads, the view changes no timer, no deviation and no case, and the read path publishes no event.
14. The clock itself runs outside this story: the durable timer inside CaseWorkflow fires at `expires_at`, raises the escalation and publishes `rwb.case.TimerBreached.v1` (event #19) on `rwb.case.events.v1`, and the projection this story reads shows the result (RWB-P3-E1028-APP).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case has no running, paused or expired timer | The timers answer is an empty list and the timers section shows the empty sentence; the prescription date and the deviations are still returned | MSG-P3-018 | AC8 |
| X2 | The case is outside the person's scope | The operation answers 404; nothing is returned and nothing is written | MSG-P4-003 | AC9 |
| X3 | The deviation service does not answer inside the timeout | The timers and the prescription date are returned; the deviation section shows that it could not be read; the on-hold banner still shows from `recovery_case.deviation_open` | MSG-GEN-006 | AC10 |
| X4 | Two deviations are open on one case | Both show with their own handler and approver; the case stays on hold until both clear | MSG-P3-004 | AC5 |
| X5 | The prescription date is 91 days away with a 90 day warning | No warning; the date is returned without MSG-P3-003 | None | AC3 |
| X6 | The deviation read passes 2 s on the first attempt | One retry with jitter, then the breaker opens for that downstream; the answer degrades as in X3 and the timer answer is untouched | MSG-GEN-006 | AC10 |
| X7 | The decision log read passes 2 s or answers an error | The deviations are returned with their handler, paused state and contact stop; `approverUserId` is omitted and the deviation section carries MSG-GEN-006 naming the decision center; the timers and the prescription date are untouched | MSG-GEN-006 | AC2 |
| X8 | A role without Case record R calls either operation | Refused with 403 by the rwb-access check behind the endpoint; the answer carries the refusal and not an empty list | MSG-P4-002 | TC-E2-015-11 |
| X9 | The case ID is unknown, or belongs to another service's case space | 404 with MSG-P4-003; no partial case is composed | MSG-P4-003 | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads what RWB-P3-E1028-APP, S8 and P7 already write; builds against the published contracts and their fakes, so neither the deviation nor the decision service needs to exist in the development environment |
| Negotiable | The layout, the column order and the wording of the panels are negotiable; the content is fixed by REQ-WKM-005 and the warning point by the timer story |
| Valuable | The next deadline, the escalation and the deviation are on one screen, composed inside one 2 s budget |
| Estimable | Two read operations extended, two consumed contracts, one reference-data read, one merge and two screen panels |
| Small | Fits one sprint with its tests |
| Testable | Every owned criterion has a test case in section 16; the S8 and P7 answers are stubbed in the contract fakes and real in SIT |

### 7. Acceptance criteria

```gherkin
Feature: Timers, escalation and the deviation flag on the case record view

  Background:
    Given the business date is 2026-12-15
    Given user "U-CO-01" holds RW-CASEOWN and owns case "RW-2026-000501" with product group "HIRE_PURCHASE" and status "IN_PROGRESS"
    Given prescription.warning-days is 90

  Scenario: AC1 Timers shown (legacy RWB-E2-015 AC1)
    Given case "RW-2026-000501" has a "NOTICE_PERIOD" timer started on 2026-12-01 expiring on 2027-01-30, on a task owned by role "RW-LITOFF"
    When "U-CO-01" opens the case record
    Then the timer shows type "Notice period", due date 2027-01-30, status "Running" and owner of the next step "Litigation officer"

  Scenario: AC2 Deviation flag (legacy RWB-E2-015 AC2)
    Given the rwb-deviation contract mock returns deviation "X3" on case "RW-2026-000502" raised on 2026-12-10, handler "U-SP-01", paused state "WITH_FCR_OFFICER" and contact stop true
    Given the rwb-decision contract mock returns approver "U-LG-01" on decision log entry "DLE-9101" for decision code "X3"
    Given case "RW-2026-000502" has deviation "X3" raised on 2026-12-10, handler "U-SP-01", approved in decision log entry "DLE-9101" by "U-LG-01", paused state "WITH_FCR_OFFICER" and contact stop true
    When "U-CO-01" opens the case record
    Then the screen is in state "On hold" with MSG-P3-004 naming "Deceased customer" and the prescription date
    Then the deviation shows code "X3", handler "U-SP-01", approver "U-LG-01", raised on 2026-12-10, return point "WITH_FCR_OFFICER" and "Contact stopped"

  Scenario: AC3 Prescription (legacy RWB-E2-015 AC3)
    Given case "RW-2026-000501" has prescription date 2027-02-13, 60 days after the business date
    When "U-CO-01" opens the case record
    Then the prescription date 2027-02-13 shows with the warning MSG-P3-003
    Then for case "RW-2026-000503" with prescription date 2027-03-16, 91 days after the business date, no warning shows

  Scenario: AC4 Escalation state (legacy RWB-E2-015 AC4)
    Given case "RW-2026-000501" has a "SERVICE_LEVEL" timer that expired on 2026-12-12 with escalation level 1, escalated to "RW-TEAMMGR" at 2026-12-12 09:05
    Given the SERVICE_LEVEL row for "HIRE_PURCHASE" status "IN_PROGRESS" names the next escalation role "RW-PRODHEAD"
    When "U-CO-01" opens the case record
    Then the timer shows status "Expired", escalated to "Team manager" at 2026-12-12 09:05 and next escalation point "Product head"
    Then the case stays in queue and status as before

  Scenario: AC5 Two deviations (legacy RWB-E2-015 AC5)
    Given the rwb-deviation contract mock returns deviations "X1" raised on 2026-12-05 and "X3" raised on 2026-12-08 on case "RW-2026-000504", both open
    Given case "RW-2026-000504" has deviations "X1" raised on 2026-12-05 and "X3" raised on 2026-12-08, both open
    When "U-CO-01" opens the case record
    Then both deviations show with their own handler and approver
    Then the screen stays in state "On hold"
    Then when "X1" is cleared on 2026-12-14, the screen stays in state "On hold" with only "X3" open and "X1" shown as cleared on 2026-12-14

  Scenario: AC6 Stage clock paused and prescription running (legacy RWB-E2-015 AC6)
    Given the rwb-deviation contract mock returns deviation "X3" on case "RW-2026-000502" open since 2026-12-10
    Given case "RW-2026-000502" with deviation "X3" open since 2026-12-10
    Given its "SERVICE_LEVEL" timer paused on 2026-12-10 and its "PRESCRIPTION" timer running
    When "U-CO-01" opens the case record
    Then the service level timer shows "Paused since 2026-12-10"
    Then the prescription timer shows "Running" with its date

  Scenario: AC7 Deviation cleared and timers resumed (legacy RWB-E2-015 AC7)
    Given the rwb-deviation contract mock returns deviation "X1" on case "RW-2026-000505" cleared on 2026-12-14 with outcome "Returned"
    Given case "RW-2026-000505" had deviation "X1" cleared on 2026-12-14 and its "SERVICE_LEVEL" timer resumed with a new expiry of 2026-12-22
    When "U-CO-01" opens the case record
    Then the screen is not on hold
    Then the service level timer shows "Running" with due date 2026-12-22
    Then the deviation shows as cleared on 2026-12-14 with outcome "Returned"

  Scenario: AC8 No running timer (legacy RWB-E2-015 AC8)
    Given case "RW-2026-000506" has no timer with status "RUNNING", "PAUSED" or "EXPIRED"
    When "U-CO-01" opens the case record
    Then the timers section shows MSG-P3-018

  Scenario: AC9 Case outside scope (legacy RWB-E2-015 AC9)
    Given the rwb-access contract mock returns that "U-CO-01" holds scope Own in team "MTG-BKK" and no scope over team "SME-NTH"
    Given case "RW-2026-000507" belongs to team "SME-NTH" and "U-CO-01" has scope Own in team "MTG-BKK"
    When "U-CO-01" opens it
    Then the system does not find the response with MSG-P4-003

  Scenario: AC10 Deviation module does not answer (legacy RWB-E2-015 AC10)
    Given the rwb-deviation contract mock does not answer within 2 seconds for case "RW-2026-000502"
    Given the deviation query does not answer within 2 seconds for case "RW-2026-000502"
    When "U-CO-01" opens the case record
    Then the timers and the prescription date show
    Then the deviation section shows MSG-GEN-006 naming "Deviation handling"
    Then the on hold banner shows from the case's deviation flag
```

**Note.** The `timer` row stays an rwb_case projection behind `GET /cases/{caseId}/timers`, and the clock that fires is now a durable Temporal timer inside CaseWorkflow on task queue `rwb-case`, so JOB-05 Timer check and the TimerDue event are retired and TimerBreached stays event #19 on `rwb.case.events.v1` (Architecture v5 slides 42 and 44; Ownership Map ruling ASM-0078). `timer.escalated_to_role` (DF-WRK-043) and `timer.escalated_at` (DF-WRK-044) are written by the timer story RWB-P3-E1028-APP; this story only reads them and displays the escalation level, the escalated-to role, the escalated time, the next escalation role and `inWarning` from `warn_at`. The deviation rows come from S8 through the read path of the S8 contract and the approvers from P7 through the decision log, both called by rwb-case, which is what the mock Givens above stand in for; `prescription.warning-days` is applied where `timer.warn_at` is computed by RWB-P3-E1028-APP and is never re-applied here. The ten criteria above are owned by this story, and the wave 2 harness RWB-ITG-E2015-ITG copies each one with the `-ITG` suffix.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every timer of the case with status Running, Paused or Expired shows with type, due date, status and the owner role of its task | REQ-WKM-005; LOV-TIMER; DF-WRK-023 |
| BR2 | A breached service level shows the role it was escalated to, when, and the next escalation point. The case does not move | R-UNI-30; REQ-WKM-004 |
| BR3 | A deviation pauses the stage clock and keeps the prescription clock running | R-DEV-01; REQ-DVH-002 |
| BR4 | A case with a deviation open shows as on hold with the deviation and the prescription date | Case status On hold; R-UNI-04; R-UNI-05; DF-CAS-019 |
| BR5 | X1, X2 and X3 show the contact stop | R-UNI-04; R-UNI-05; R-UNI-06; CTL-16 |
| BR6 | The case leaves on hold only when every open deviation is cleared | R-UNI-43; FEAT-DVH-09 |
| BR7 | The prescription date shows a warning from the warning point `timer.warn_at` that the timer story computes from `prescription.warning-days` (assumed 90; DL22); this view never recomputes it | R-UNI-31; CTL-18; DF-WRK-033 |
| BR8 | The return point of a deviation is the routing state the case was in when it paused | DF-CAS-041; R-DEV-08 |
| BR9 | The approver of a deviation is the approver on its decision log entry, read through the rwb-decision contract; rwb_case holds no copy of it | REQ-DRI-001; DP-03; DF-DEC-010 |
| BR10 | The two operations are reads of a projection: they write no timer, no deviation and no case, and the escalation fields are written by the durable timer in RWB-P3-E1028-APP | Ownership Map ruling ASM-0078; DP-01 |
| BR11 | A role without Case record R is refused with 403 and a case outside the caller's scope is not found with 404; a refusal never returns an empty list | REQ-WKM-005; the rwb-access contract |
| BR12 | Each downstream is called once, one hop, with the 2 s timeout and a breaker; a timeout degrades the section it belongs to and never empties the timers or the prescription date | DP-11; NFR-008; Architecture v5 slide 11 |

### 9. State transitions

None on the case. This story changes no case status, no timer status and no deviation state; it reads and displays them. The facts below are caused by other stories and are what this view shows.

| Timer state change | Cause | What this view shows | Owner story |
|---|---|---|---|
| RUNNING to EXPIRED | The durable timer inside CaseWorkflow reaches `expires_at`, raises the escalation and publishes TimerBreached (event #19) | Status Expired, escalation level 1, escalated-to role and time, next escalation role; the case queue and status unchanged | RWB-P3-E1028-APP |
| RUNNING to PAUSED | DeviationRaised consumed by rwb-case into the case workflow | Status Paused with the pause date; the prescription timer keeps running with the same date | RWB-P3-E1028-APP; S8 |
| PAUSED to RUNNING | DeviationCleared consumed by rwb-case after the last open deviation clears | Status Running with `expires_at` moved by the paused working days and `inWarning` recomputed from `warn_at` | RWB-P3-E1028-APP |
| Any status to STOPPED | The stage ends or the case closes | The timer leaves the timers section | RWB-P3-E1028-APP |
| PRESCRIPTION never changes state for a deviation | The prescription clock is never paused | The same prescription date and the same warning while a deviation is open | RWB-P3-E1028-APP |

The two escalation fields this view reads are not added by this story: `timer.escalated_to_role` and `timer.escalated_at` arrive with the migration of RWB-P3-E1028-APP, which also sets `recovery_case.deviation_open` that the on-hold banner is built from.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads the case record view with its timers, prescription date and deviations (Case record R, scope Own) |
| RW-TEAMMGR, team manager | Reads the same, including the escalation the case was raised to (Case record R, scope Team) |
| RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LEGAL | Read the case and its deviations (Case record R) |
| RW-AUDIT, internal audit | Reads (Case record R, scope All); changes nothing |
| SY-CASEWF, case workflow identity | Writes the escalation fields and raises TimerBreached inside the durable timer, in RWB-P3-E1028-APP; this story only reads the projection |
| rwb-access | Answers the role, scope and Case record right check through its authorise contract, cached per request |
| rwb-deviation | Answers the deviation read; owns `deviation` |
| rwb-decision | Answers the decision log read that names the approver; owns `decision_log_entry` |

Reading the approver needs no Decision log right: the case service returns the approver's user ID only, not the decision log entry.

### 11. Data

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
| DF-WRK-043 | timer | escalated_to_role | Read only (written by RWB-P3-E1028-APP) |
| DF-WRK-044 | timer | escalated_at | Read only (written by RWB-P3-E1028-APP) |
| DF-WRK-023 | task | owner_role | Read |
| DF-CAS-038 | deviation | deviation_code | Read, through the rwb-deviation contract |
| DF-CAS-039 | deviation | raised_at | Read, through the rwb-deviation contract |
| DF-CAS-041 | deviation | paused_state | Read, through the rwb-deviation contract |
| DF-CAS-042 | deviation | handler_user_id | Read, through the rwb-deviation contract |
| DF-CAS-043 | deviation | contact_stop | Read, through the rwb-deviation contract |
| DF-CAS-044 | deviation | cleared_at | Read, through the rwb-deviation contract |
| DF-CAS-045 | deviation | outcome | Read, through the rwb-deviation contract |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read, through the rwb-decision contract |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | `prescription.warning-days` version in force, for traceability of `warn_at` | Read, through the reference-data contract |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row | LOV-TIMER, LOV-TIMER-STATUS, LOV-DEVIATION and the SERVICE_LEVEL escalation roles | Read, through the reference-data contract |

Field IDs are those in the Logical Data Model and Data Dictionary v8. The deviation and decision fields are read only through their owners' contracts; no deviation row and no decision log row is copied into `rwb_case`.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3). The two operations are the ones this story extends; the rest of the rwb-case surface is unchanged.

| Method | Path | Purpose | Added in this story | Access |
|---|---|---|---|---|
| GET | `/cases/{caseId}` | Read one case with its clocks, its flags and its deviations | `deviations[]` (`deviationCode`, `raisedAt`, `handlerUserId`, `approverUserId`, `pausedState`, `contactStop`, `clearedAt`, `outcome`) and `deviationsAvailable` (boolean) on the Case resource that already carries `prescriptionDate`, `stageClockStart`, `deviationOpen` and `legalHold` | Case record R, scope applied |
| GET | `/cases/{caseId}/timers` | Read the clocks on a case: stage, service level, prescription, notice | `nextStepOwnerRole`, `escalatedToRole`, `escalatedAt`, `nextEscalationRole`, `inWarning` on each `Timer`, beside `timerType`, `startedAt`, `expiresAt`, `warnAt`, `paused`, `status` and `escalationLevel` | Case record R, scope applied |

The timers answer is ordered by `expiresAt` ascending. Errors for both: 401 no session (MSG-P4-001), 403 no Case record R (MSG-P4-002), 404 unknown or out of scope (MSG-P4-003), 503 store down. Idempotency is not applicable to a read.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | The open and cleared deviations of the case with code, raised date, handler, paused state, contact stop, cleared date and outcome (GAP-0714; ASM-1261) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The approver on the decision log entry of each deviation decision | One hop, 2 s (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and Case record right check, cached per request | One hop, 2 s (DP-11) |

Three calls, no chain. The deviation call and the decision call are made by rwb-case inside the case answer, so gateway-bff still sees one hop per owner.

#### 12.3 Events published

None in this story. When the durable timer inside CaseWorkflow fires, RWB-P3-E1028-APP publishes `rwb.case.TimerBreached.v1` (event #19) on `rwb.case.events.v1` with `caseId`, `caseNo`, `timerId`, `timerType` and `expiresAt`, keyed by `caseId`; this read path publishes nothing and writes no outbox row.

#### 12.4 Events consumed

None in this story. `rwb.deviation.DeviationRaised.v1`, `rwb.deviation.DeviationCleared.v1` and `rwb.decision.RulePackageInForce.v1` are consumed by the timer story RWB-P3-E1028-APP into `rwb_case`, where they set the pause, the resume and the rule version; this view reads the result and subscribes to nothing.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = case ID | `rwb-case` | Holds the durable stage timer, the warning point and the escalation, and publishes TimerBreached when it fires; owned by RWB-P3-E1028-APP, and this story adds no workflow and no activity to it |
| Timers projection read | Query inside the service | `rwb-case` | Orders the timer rows by `expires_at`, joins `task.owner_role`, and resolves `nextEscalationRole` from the SERVICE_LEVEL reference row in force |

#### 12.6 Schedules

None. There is no timer-check Schedule and no timer-check job: the five-minute check is replaced by the durable timer inside CaseWorkflow (DP-10; Architecture v5 slide 44, JOB-05 retired). This story registers no Schedule and reads no scheduler state.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| timer | P3 (rwb_case) | The projection row: type, start, expiry, warning point, paused flag, status, escalation level, escalated role and time |
| recovery_case | P3 (rwb_case) | Prescription date, stage clock start, deviation flag and legal hold |
| task | P3 (rwb_case) | The owner role of the next step on the timer |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Not written by this read path; the timer story uses them for TimerBreached |

`deviation` is owned by S8 and `decision_log_entry` by P7; neither is read directly, and `rwb_case` holds no foreign key into another schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-deviation WireMock | The S8 contract | `GET /cases/{caseId}/deviations` with X3 on RW-2026-000502, X1 and X3 on RW-2026-000504, X1 cleared on RW-2026-000505, the empty answer of RW-2026-000501 and a delayed answer beyond 2 s |
| rwb-decision WireMock | The P7 contract | `GET /decision-log?caseId=` with entry DLE-9101 and approver U-LG-01 for X3, the approvers of the X1 entries, and a delayed answer beyond 2 s |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Case record R, refusing RW-REFADM, and refusing scope over SME-NTH for a scope Own in MTG-BKK |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | Case and timers provided; deviations, decision log and authorise consumed; one hop, 2 s timeout, breaker per downstream |
| Kafka | None published, none consumed | TimerBreached is published by RWB-P3-E1028-APP and consumed by gateway-bff; this read path carries no Kafka traffic |
| Temporal | None added | The durable timer lives in CaseWorkflow and belongs to RWB-P3-E1028-APP |
| File | None | No file is read or written |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.case.caseview`, module `caseview`; front end folder `src/modules/recovery/case/caserecord`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | The monolith base path of the legacy API (Template and Rules §R5.5, DP-13) | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The same-service CON baselines RWB-P3-E2015-CON, RWB-P3-E1028-CON and RWB-P3-E1035-CON are class H dependencies of this story and are not DP rows; no pattern moves, and DP-06 is not claimed because this story reads no parameter and re-applies no warning day.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseClocksController | Controller | The two read operations with the added fields; maps a refusal to 403 and an unknown case to 404 |
| CaseViewService | Service | Builds the case answer: the case row, the deviation read, the approver read, the merge and `deviationsAvailable` |
| TimerViewService | Service | Builds the timers answer: ordering, the task owner role, the escalation fields, the next escalation role and `inWarning` |
| TimerProjectionRepository | Repository | Reads `timer` and `task` of the case from schema `rwb_case` only; no write path |
| DeviationClient | Client | Calls the S8 read with the 2 s timeout and the breaker; never reads `deviation` |
| ApproverClient | Client | Calls the P7 decision log once per case with the 2 s timeout; matches an entry to a deviation by decision code and raise time |
| EscalationRoleReader | Service | Resolves the next escalation role from the SERVICE_LEVEL reference row in force, through the reference-data contract (DP-07) |
| AccessCheckClient | Client | Calls the rwb-access authorise contract, cached per request |
| CaseClocksPanel | React component | The timers, the prescription date, the warnings and the escalation state on SCR-03 |
| DeviationPanel | React component | The deviations with handler, approver, contact stop and return point, and the On hold banner |

**Database.** No migration adds a column in this story. The projection columns `timer.escalated_to_role` (DF-WRK-043) and `timer.escalated_at` (DF-WRK-044) arrive with the migration of RWB-P3-E1028-APP, and this story's migration is limited to the read-side index it needs, `ix_timer_case_expiry ON timer (case_id, expires_at)`, added in its own Flyway step in schema `rwb_case`. Reads use `ix_timer_case_id` and `ix_task_case_id` where they already exist. No column of `recovery_case` and no column of `task` is added.

**Configuration and reference data.** `caseview.deviation-timeout-ms` = 2000 and `caseview.approver-timeout-ms` = 2000 are service configuration values fixed by the 2 s budget of DP-11, held in the service configuration and never in code. LOV-TIMER, LOV-TIMER-STATUS, LOV-DEVIATION and the SERVICE_LEVEL escalation roles are read through the reference-data contract with their version in force; the timer and deviation labels come from LOV-TIMER and LOV-DEVIATION. `prescription.warning-days` is not read here: it is applied where `timer.warn_at` is computed (RWB-P3-E1028-APP).

**Build steps**

1. Extend the OpenAPI document and the generated types for the two operations with the added fields; contract test against RWB-P3-E2015-CON.
2. TimerProjectionRepository and TimerViewService over schema `rwb_case`: ordering, owner role, escalation level, escalated role and time, next escalation role, `inWarning`; tests for AC1, AC4, AC6, AC7 and AC8.
3. DeviationClient with the 2 s timeout, the single retry on GET, the breaker and the degradation flag; tests for AC2, AC5 and AC10.
4. ApproverClient with the case-scoped query and the match by decision code and raise time; tests for AC2 and the approver timeout of section 5.
5. CaseViewService merge: `deviations[]` ordered by raised date, `deviationsAvailable`, and the banner from `deviation_open`; tests for AC2, AC5, AC7 and AC10.
6. Prescription warning from `warn_at` and the on-hold banner; tests for AC3 and AC6.
7. Authorisation through the rwb-access contract with the scope check; tests for AC9 and the refusal of section 16.
8. CaseClocksPanel and DeviationPanel against the merged screen model returned by the composite route of RWB-PLT-N001-CON; browser test of SCR-03 for AC1 to AC10.

**Feature switch.** `rwb.p3.case-clocks`, a service configuration value. Off: SCR-03 shows the Epic 1 read-only fields and the two operations return the case and the timers without the added deviation block; on: the timers with the escalation state, the prescription warning and the deviation flag.

**Done when.** Every test in section 16 passes, the two contract fakes drive every cross-service answer, a case with 6 timers and 50 documents loads inside 2 s through the composite route (NFR-009), and the contract tests of RWB-P3-E2015-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-003 | A timer or the prescription date is inside its warning period | {timer} ends on {date}. |
| MSG-P3-004 | The case is on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-018 | The case has no running, paused or expired timer | There are no running timers on this case. |
| MSG-GEN-006 | The deviation or the decision service does not answer in time | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A role without Case record R opens the view | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the person's scope | This case is not in your scope. |

For MSG-GEN-006 the {system} value is "Deviation handling" on the deviation read and "Decision center" on the approver read. MSG-P3-018 is new (see Additions). Thai text follows DL10.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-03 Case record | Loading | Sees skeleton rows in the clocks and deviation panels; the composite route answers once, inside the 2 s budget |
| SCR-03 Case record | Read only | Reads the timers ordered by due date, the escalation state, the prescription date and the warnings |
| SCR-03 Case record | Editable | The same panels; edits elsewhere on the record belong to other stories and this view never writes |
| SCR-03 Case record | On hold | Reads the banner with MSG-P3-004 and each open deviation with handler, approver, contact stop and return point, and the cleared deviations with their outcome |
| SCR-03 Case record | Degraded | Reads the timers and the prescription date, and the deviation section with MSG-GEN-006 while the banner still shows from the case flag |

The composite route that serves these states is owned by RWB-PLT-N001-CON; its path and merge order are not fixed here, and this story only fixes the two answers it contributes.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-015-01 | AC1, BR1 | End to end | NOTICE_PERIOD timer on a task owned by RW-LITOFF |
| TC-E2-015-02 | AC2, BR4, BR5, BR8, BR9 | End to end | X3 with handler, approver, paused state and contact stop |
| TC-E2-015-03 | AC3, BR7 | End to end | Prescription 60 and 91 days ahead |
| TC-E2-015-04 | AC4, BR2 | End to end | SERVICE_LEVEL expired, level 1, escalated to RW-TEAMMGR, next role RW-PRODHEAD |
| TC-E2-015-05 | AC5, BR6 | End to end | X1 and X3 open, then X1 cleared |
| TC-E2-015-06 | AC6, BR3 | End to end | Paused service level and running prescription |
| TC-E2-015-07 | AC7, BR6 | End to end | X1 cleared and the timer resumed with 2026-12-22 |
| TC-E2-015-08 | AC8 | End to end | Case with only stopped timers |
| TC-E2-015-09 | AC9 | End to end | Case of team SME-NTH opened by an MTG-BKK owner |
| TC-E2-015-10 | AC10, BR12 | NFR | Stubbed deviation query delayed 3 seconds; the timer answer and the prescription date still returned inside 2 s |
| TC-E2-015-11 | BR11 | Component | RW-REFADM (no Case record right) calls `GET /cases/{caseId}/timers`; refused with MSG-P4-002 |

The legacy levels map System to End to end, Access to Component and Resilience to NFR; TC-E2-015-10 is the timeout case of the legacy story and is levelled NFR here because it proves the 2 s budget and the degradation of one section rather than a business outcome.

### 17. Guardrails

- No business value in code: the warning point, the escalation roles, the next escalation role, the timeouts and the timer and deviation labels are data read through the parameters and reference-data contracts of rwb-case or written by the timer story.
- No personal data in logs, tests, workflow history or events: the panels show staff user IDs resolved to display names by the ACE common module, no customer data is read into an answer, and test data is synthetic.
- No read of another service's table and no ACE view: deviations come only through the rwb-deviation contract, approvers only through the rwb-decision contract, and authorisation only through the rwb-access contract (DP-01, DP-11).
- ACE data is read only through the owner's contract or the `v_ace_*` views of rwb-source-data; this story reads no ACE view at all.
- No cross-schema read: `rwb_case` holds no foreign key and no join into `rwb_deviation` or `rwb_decision`.
- The view never writes: no timer, no deviation and no case is changed by either operation, and the read path writes no outbox row.
- One hop only: rwb-case calls S8 and P7 once each and returns; it never calls a service that calls another.
- Every answer carries IDs, codes, dates and amounts only; no name, address, identity number or contact point appears in a response or in a log line.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-004 | A breached service level visible to the escalation role without the case moving | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-07 | All recovery processes | R-UNI-30 | TC-E2-015-04, TC-E2-015-11 |
| REQ-WKM-005 | Timers, escalation state and the deviation flag on the case record view | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-05, FEAT-WKM-06 | All recovery processes | R-UNI-31, R-UNI-04, R-UNI-05 | TC-E2-015-01 to TC-E2-015-03, TC-E2-015-08 to TC-E2-015-10 |
| REQ-DVH-002 | A deviation pauses the stage clock and keeps the prescription clock running | Business Requirements Epic 2, section 4; Program, section 5.15 | FEAT-DVH-02, FEAT-DVH-03, FEAT-DVH-05, FEAT-DVH-06, FEAT-DVH-09 | 11 Handle customer care and deviations | R-DEV-01, R-UNI-43 | TC-E2-015-02, TC-E2-015-05 to TC-E2-015-07 |
| REQ-DRI-001 | Every decision writes one record holding the case, the decision, the recommendation, the approval and the outcome | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-DRI-01 | All recovery processes; 11 Handle customer care and deviations | R-UNI-24, R-UNI-39 | TC-E2-015-02 |

### 19. Out of scope

- Raising, handling and clearing deviations (S8, SCR-06 and SCR-08).
- Starting, pausing and resuming timers, computing `warn_at`, writing the escalation fields and publishing TimerBreached (RWB-P3-E1028-APP).
- The contract baseline of the two read operations, the deviation object and the fakes (RWB-P3-E2015-CON).
- The deployment, the consumer groups, the dashboards and the runbook (RWB-P3-E2015-OPS).
- The cross-service journey harness and its evidence (RWB-ITG-E2015-ITG).
- The history timeline on the case (RWB-P3-E2016-APP).
- The next action panel and its due date (RWB-P3-E1035-APP).
- The case record view's accounts, parties, documents, notices, payments and legal sections (their own stories of RWB-SVC-P3 and the route epics).
