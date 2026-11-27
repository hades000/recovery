# RWB-S8-E2033-APP Case and queue list with status, owner and ageing

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E2033-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-033 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP08, DP13, DP14, DP15, DP19 |
| Parallel lane | L-S8-J |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S8-E2033-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2033-CON, Not specified in the source documents (DOR-RWB-S8-E2033-APP-21) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (FR-S8-018, FR-S8-019, FR-S8-020, FR-S8-028) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the quoted English to Error and Message Standard v6.


**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-033 for rwb-deviation, carrying the deviation half of the case and queue list — the flag, the codes, the raised date, the contact stop and the paused state of every case of one page, so that a paused case is never read as on time. Applied: the plan's H row is None and the platform contracts of DP-06, DP-07, DP-08, DP-14, DP-15 and DP-19 arrive with the service template (GAP-3101; ASM-5308); the Ownership Map gives S8 two write operations and no read, so the read is declared here (ASM-5306); and legacy AC1 to AC11 stay with RWB-P2-E2033-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S8-E2033-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (23 resolved, 15 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **the deviation state of every case of one page answered by rwb-deviation in one hop — is a deviation open, which codes, since when, is contact stopped, which routing state was paused and must the stage clock stay paused — beside the status, owner and ageing of the same cases**, so that **a case held by a dispute, a hardship, a death, a fraud, a bankruptcy, a lost contact or a damaged collateral is never read as an on-time case, and the list says why it is held**.

This story is the rwb-deviation part of legacy RWB-E2-033. The legacy story completes the case list for every queue in the manager's scope: a breach filter, the prescription clock beside the stage clock "so a paused case is not read as safe", and the same columns in the extract (legacy section 2, AC2). Under D-RCV-60 the case, the queue, the timer and the flags on them are rwb-case's, the roles, the scope and the rights are rwb-access's (DP-01, DP-06, DP-07, DP-08), the composed page and the Excel file are rwb-integration's in RWB-P2-E2033-APP, and AC1 to AC11 of the legacy key stay there. The one fact the split leaves unowned is the deviation itself: `deviation` is S8's single table (context pack ownership rows; TSD S8 T3.1), so a list that shows "deviation open Yes", a code, a contact stop or a paused state is asking this service.

Inside `rwb-deviation` this is the list-support capability of the deviation service:

- Service `rwb-deviation`, schema `rwb_deviation`, REST base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1` with event names `rwb.deviation.<Event>.v1`, Temporal task queue `rwb-deviation` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.deviation` (context pack, service row).
- `GET /deviation-flags` with a page of case ids answers, per case, `caseId`, `deviationOpen`, `openDeviationCount`, `openCodes`, `firstRaisedAt`, `contactStop`, `pausedState` and `pauseRequired` in one hop, so the list shows the deviation cell of every row without one call per row (DP-13).
- The answer is built from `deviation` in `rwb_deviation` only; no `recovery_case` row, no `timer` row, no `queue` row, no `v_ace_*` view and no table of another service is read (DP-01).
- `deviationOpen` on the list stays rwb-case's `deviation_open` (DF-CAS-019, read through the case contract of RWB-P2-E2033-CON); this answer is the evidence beside it, and the two are asserted equal rather than copied into either schema (ASM-5307).
- This slice is read only: it writes no deviation row, raises no flag, pauses and resumes no clock, publishes no event and starts no workflow.

What this story does not own: the product, queue, owner, status, stage, age in state, service level state and prescription clock of a row, and the breach filter, the order and the extract, which are rwb-case's and rwb-integration's in RWB-P2-E2033-APP; raising, routing, handling and clearing a deviation and the two write operations `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` (API-S8-001, API-S8-002), which are the Epic 2 stories of this service; the agent screening, which is RWB-P10-E1062-APP and RWB-S8-E1062-APP; and the end-to-end proof across the services of the page, which is RWB-ITG-E2033-ITG.

### 2. Business rationale

A team manager learns where cases wait by asking each owner or by building a spreadsheet; the legacy story replaces that with one list (legacy section 2). The split does not change the question, it changes who answers it: the row, its owner and its ageing come from the owner of the case, and the reason a row is held comes from the owner of the deviation. A list that shows only a flag and no code, no raised date, no stop and no paused state tells the manager that something is wrong and not what — and a list that shows a paused case without saying so reads exactly like an on-time case, which is the failure legacy AC2 was written against.

Three target facts shape this slice.

1. **The deviation is this service's, the row is not.** `deviation` in `rwb_deviation` holds the code, the raised date, the actor, the paused state, the contact stop, the outcome and the cleared date (TSD S8 T3.1), and `recovery_case.deviation_open` is rwb-case's copy of the fact (DF-CAS-019). One read serves the page, and the two values are tested against each other, so a flag can never be shown without its evidence and the evidence can never contradict the flag.
2. **A pause is a state of the case, decided by a deviation.** R-DEV-01 pauses the stage clock and keeps the prescription clock running, R-DEV-18 resumes the clock and returns the case to the state it paused in, and a case with two open deviations resumes only when all are cleared (FSD S8 A2.2, A2.3, A2.9; legacy BR4). The list needs one word from this service to know it must not count the case as late, and that word is `pauseRequired`.
3. **One page is one hop.** The legacy story read the timers of the whole page in one query; a per-case deviation call would put one call per row inside one page and break the one-hop, 2 s rule of ADR-020. The batched read is therefore the shape, with the page bound as a parameter row and not as a constant (DP-06).

The slice supports REQ-WKM-002 (the manager sees where work waits) and REQ-DVH-006 (the deviation flag is visible in every queue view), and it changes no rule of the DEV route set: it reports rows the raise, route and clear steps write.

### 3. Preconditions

- The `rwb_deviation` baseline is in place: `deviation` exists with the columns of DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0, and the outbox, inbox and idempotency tables of the platform event library exist in the schema.
- The service runs as its own login on `rwb_deviation` (DP-02) and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery_case`, `timer` or `rwb_case` is refused by the database and fails the boundary test.
- The reference-data contract of rwb-case is on the service template (RWB-PLT-E1043-CON; DP-07), with LOV-DEVIATION (X1 to X7) and LOV-RAISED-BY at the version in force (TSD S8 T3.2). The read of the contract is faked; its operation name and field names are Not specified in the source documents (GAP-3101; ASM-5311).
- The parameters contract of rwb-case and its client library are on the service template (RWB-PLT-E1042-CON; DP-06): the page bound of the case list is a parameter row, 1 to 200 in the legacy validation, and no bound is written in code (ASM-5309).
- The authorise contract of rwb-access and the guard library are on the service template (RWB-PLT-E1037-CON; DP-08): the read needs Case record right R with the caller's scope applied (TSD S8 T6.1, T-A.1).
- The gateway-bff composite route that serves SCR-02 Case list is as published (RWB-PLT-N001-CON; DP-19); the screen layout is that story's and this one's answer is what the deviation cell shows.
- RWB-P2-E2033-CON is the contract of this legacy key, tagged on Day 1; this story builds against its fakes and changes none of its operations. Its consumed set does not carry this read, and that seam is recorded, not hidden (GAP-3101; ASM-5307).
- No approval is needed to build against a Draft contract baseline; acceptance of the seam between the two answers is the solution architect's at the contract review.
- The contract version this story builds against is Not specified in the source documents (DOR-RWB-S8-E2033-APP-23); only the /v1 path is stated.
- The contract fake library version recorded as published for this story is Not specified in the source documents (DOR-RWB-S8-E2033-APP-22).

### 4. Flow

1. The manager opens SCR-02 and the page of case rows is composed: the rows, the queues, the owner, the status, the stage, the age in state, the service level state, the prescription clock and `deviationOpen` come from the rwb-case contracts through RWB-P2-E2033-APP (DP-13, DP-19).
2. The composition takes the case ids of the page it holds, one to the page bound, and asks this service once: `GET /api/recovery/deviation/v1/deviation-flags?caseId=<caseId>` repeated, one hop, inside a 2 s budget.
3. `DeviationFlagGuard` authorises the call from the cached decision of rwb-access (Case record right R) and applies the caller's scope; a caller without the right is refused with 403 and MSG-P4-002 before a row is read (legacy X9).
4. `PageBoundValidator` checks the request against the page bound of the parameter contract and refuses an empty or over-long request with 422 (legacy AC7 validation, MSG-GEN-001, MSG-GEN-002).
5. `OpenFlagReader` reads the `deviation` rows of those case ids in `rwb_deviation` whose `cleared_at` is empty and whose `state` is not a cleared state, with the code, the raised date, the contact stop, the paused state and the outcome.
6. `DeviationFlagProjection` groups the rows per case: `deviationOpen`, `openDeviationCount`, `openCodes` in the order of LOV-DEVIATION at the version in force, `firstRaisedAt` as the earliest raised date of the open rows, `contactStop` as true when any open row stops contact, `pausedState` as the paused state of the open rows, and `pauseRequired` as true while at least one row is open (BR2, BR4).
7. `FlagAnswerAssembler` builds one row per case id of the request and no other field: no product, no queue, no owner, no status, no stage, no age, no clock and no person (BR7).
8. The scope is applied per case: a case outside the caller's scope is not answered at all, and no message says that it exists (legacy X4, AC9).
9. The answer is returned in the request: the same request on unchanged rows answers the same values, writes nothing and publishes nothing (BR8).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller holds no Case record right R | Refused with 403 before any row is read | MSG-P4-002 | AC5, TC-E2-033-12 |
| X2 | No `caseId` is named, or a value is not a case reference | Refused with 422; nothing is read | MSG-GEN-001 | AC5 |
| X3 | The request names more case ids than the page bound of the parameter contract | Refused with 422 naming the bound; nothing is read | MSG-GEN-002 | AC5, TC-E2-033-07 |
| X4 | A named case is outside the caller's scope | No row for that case; the rest of the page stands; no message reveals the case | None | AC5, TC-E2-033-09 |
| X5 | The parameter or the reference-data read does not answer inside the budget | 503 with the platform envelope naming the system; no partial answer is served | MSG-GEN-006 | AC7, AC8, TC-E2-033-16, TC-E2-033-17 |
| X6 | A case holds no deviation at all | A row with `deviationOpen` false, count 0, no code, no date, `contactStop` false, `pausedState` null and `pauseRequired` false | None | AC1 |
| X7 | A deviation is cleared while another stays open | The cleared row leaves `openCodes` and the count; `pauseRequired` stays true until the last is cleared | None | AC4 |
| X8 | A statement, a component or a test reaches a `recovery_case` row, a `timer` row, a `rwb_case` table or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | AC6, BR1 |

X1, X4 and X6 are the legacy paths carried onto the slice (the access case TC-E2-033-12, the scope case AC9 and the no-timer case AC5); X2, X3, X5, X7 and X8 are the paths the split adds. The breach decision, the page size of the list, the order across pages, the extract limit and the empty page are RWB-P2-E2033-APP's and are not restated here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Answers from `rwb_deviation` only and builds on Day 1 against the RWB-P2-E2033-CON fakes and the platform libraries of the template; it waits for no in-lane story |
| Negotiable | The path, the field order and the view name are this story's; the codes, the states, the page bound and the lists are rows read with their version |
| Valuable | A held case is never read as on time, and the list says which deviation holds it, since when, with contact stopped or not |
| Estimable | One read operation, one projection, one guard, one view and one Flyway step |
| Small | Fits one sprint as a secondary slice of the legacy key, beside RWB-P2-E2033-APP and RWB-ITG-E2033-ITG |
| Testable | Every criterion runs on synthetic deviations and synthetic reference data through the contract fakes, plus the access, scope, bound and boundary cases |

### 7. Acceptance criteria

```gherkin
Feature: Case and queue list with status, owner and ageing — the rwb-deviation half

  Background:
    Given the rwb-case reference-data contract mock returns LOV-DEVIATION with X1 to X7 and LOV-RAISED-BY at the version in force
    Given the rwb-case parameter contract mock returns the case-list page bound 1 and 200
    Given the rwb-access contract mock returns the Case record right R with Team scope for role RW-TEAMMGR over team "MTG-BKK"

  Scenario: AC1 Every case of the page carries its deviation flag in one answer (new, D-RCV-60)
    Given case "RW-2026-000101" holds no deviation and case "RW-2026-000104" holds open deviation "X1" raised on 9 December 2026 with contact stop true and paused state "WITH_FCR_OFFICER"
    When the page of case ids "RW-2026-000101", "RW-2026-000102", "RW-2026-000103" and "RW-2026-000104" is read
    Then the answer holds one row per case id with the fields caseId, deviationOpen, openDeviationCount, openCodes, firstRaisedAt, contactStop, pausedState and pauseRequired
    Then case "RW-2026-000101" answers deviationOpen No, count 0 and pauseRequired false
    Then case "RW-2026-000104" answers deviationOpen Yes with the code "X1" and firstRaisedAt 9 December 2026
    Then the page of case ids is answered in one hop inside a 2 s budget

  Scenario: AC2 A paused stage clock is never served as an on-time case (new, D-RCV-60)
    Given the rwb-case ageing contract mock returns service level state PAUSED for case "RW-2026-000104" and the prescription date 30 June 2028 with prescription clock RUNNING
    Given case "RW-2026-000104" holds open deviation "X1" raised on 9 December 2026 with contact stop true and paused state "WITH_FCR_OFFICER"
    When the page that holds "RW-2026-000104" is read at 10 December 2026 09:00
    Then the row answers pauseRequired true, pausedState "WITH_FCR_OFFICER" and contactStop true
    Then the row carries no service level state, no service level due date, no prescription date and no breach flag of its own
    Then a case with no open deviation answers pauseRequired false

  Scenario: AC3 The list and the extract show the same deviation value (new, D-RCV-60)
    Given the same page of case ids is read once for the list and once for an export with the same queue, product and breached filters
    When the two answers are compared case by case
    Then each case answers the same deviationOpen, openCodes, contactStop, pausedState and pauseRequired in both
    Then the row order, the age in state and the breach decision are not computed, changed or stored by this service

  Scenario: AC4 Two open deviations are held until the last one is cleared (new, D-RCV-60)
    Given case "RW-2026-000502" holds open deviation "X3" raised on 10 December 2026 and open deviation "X6" raised on 11 December 2026
    Given deviation "X1" on the same case was cleared on 8 December 2026
    When the page is read
    Then the row answers openDeviationCount 2 with the codes "X3" and "X6", firstRaisedAt 10 December 2026 and contactStop true
    Then the cleared "X1" is not in openCodes and is not counted
    Then pauseRequired stays true while one open deviation remains and is false only after the last is cleared

  Scenario: AC5 The right, the scope and the page bound are enforced (new, D-RCV-60)
    Given the rwb-access contract mock returns no Case record right R for role RW-REFADM
    When "RW-REFADM" reads the page of one case
    Then the call is refused with status 403 and message MSG-P4-002 and no row is read
    When the manager of team "MTG-BKK" reads a page that names case "RW-2026-000201" in queue "HP-NE-CO" of team "HP-NE"
    Then no row for "RW-2026-000201" is answered and no message says that the case exists
    When the page names 500 case ids
    Then the call is refused with status 422 and message MSG-GEN-002 naming the page bound 1 and 200

  Scenario: AC6 The answer is read only, personal-data free and carries no case column (new, D-RCV-60)
    Given a page of case ids read twice
    When the two answers, the schema and the logs are inspected
    Then no deviation row, no case row and no outbox row is written, no contact stop is set, no clock moves and no event is published
    Then no handler identity, person name, contact value or free-text note appears in the answer, a log line or a span attribute
    Then the product, queue, owner, status, stage, age in state and both clocks of each case are absent from the answer
    Then no statement of this slice reads a table of another service or a v_ace_* view

  Scenario: AC7 A read that does not answer inside the budget is refused and no partial answer is served (new, D-RCV-60)
    Given the rwb-case parameter contract mock answers after the budget Not specified in the source documents (DOR-RWB-S8-E2033-APP-3)
    When the page of case ids "RW-2026-000101" and "RW-2026-000104" is read
    Then the call is refused with status 503 and the platform envelope naming the system
    Then no partial answer is served and no row is answered

  Scenario: AC8 A reference-data read that does not answer inside the budget is refused and no partial answer is served (new, D-RCV-60)
    Given the rwb-case reference-data contract mock answers after the budget Not specified in the source documents (DOR-RWB-S8-E2033-APP-3)
    When the page of case ids "RW-2026-000101" and "RW-2026-000104" is read
    Then the call is refused with status 503 and the platform envelope naming the system
    Then no partial answer is served and no row is answered

  Scenario: AC9 The rules with no other criterion hold on every answer (new, D-RCV-60)
    Given a page of case ids is read against the reference-data rows at the version in force
    When the answer, the reads and the outputs of the service are inspected
    Then the codes, the states and the page bound are rows read at the version in force and no value is a constant in the module (BR5)
    Then the flag, the count and the codes come from open deviation rows only and deviationOpen equals rwb-case's flag on every row (BR2, BR3)
    Then a request within the page bound of the parameter row is accepted and an empty or over-long request is refused before any read (BR6)
    Then the answer carries no case column and no person value (BR7)
    Then the read reaches only deviation and v_deviation_flag in rwb_deviation and the service publishes no event, writes no outbox row, starts no workflow and creates no Schedule (BR1, BR8)

  Scenario: AC10 The provided operation answers 401 and 404 only as section 12.1 publishes them (new, D-RCV-60)
    Given the rwb-deviation contract mock is called without an identity
    When the operation of section 12.1 is called without an identity and when a path the contract does not publish is called
    Then the call without an identity is answered 401
    Then the call to a path the contract does not publish is answered 404
    Then every other error answer carries only the status code that section 12.1 publishes for it

  Scenario: AC11 A consumed call that fails or does not answer refuses the read and serves no partial answer (new, D-RCV-60)
    Given the rwb-access contract mock returns an error or does not answer for the Case record right check
    When the page of case ids "RW-2026-000101" and "RW-2026-000104" is read
    Then the call is refused with status 503 and the platform envelope naming the system
    Then no partial answer is served and no row is answered
```

The criteria AC1 to AC11 are new and test only this slice: the deviation estate of one page and the pause word the list needs. The legacy criteria AC1 to AC11 of RWB-E2-033 are owned word for word by RWB-P2-E2033-APP, and no legacy criterion text is copied here. Two legacy values are reused because the sources publish them — case `RW-2026-000104` with deviation X1 raised on 9 December 2026, the prescription date 30 June 2028 and the paused state `WITH_FCR_OFFICER` (legacy AC2 and BR4) — and they are asserted on this service's answer, not on the page. Two points are recorded rather than smoothed over: the read is not a row of the Ownership Map (GAP-3101; ASM-5306), and the list's `deviationOpen` remains rwb-case's flag, which this answer explains and never replaces (ASM-5307).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The answer is built from `deviation` in `rwb_deviation` only; no `recovery_case`, `timer`, `queue`, `role` or reference row of another service is read, and no foreign key leaves the schema | DP-01; context pack ownership rows; TSD S8 T3.1, T3.3 |
| BR2 | A case is flagged while at least one deviation row is open — `cleared_at` empty and `state` not a cleared state — and the flag, the count, the codes, the earliest raised date, the contact stop and the paused state come from those rows only | Legacy BR3 to BR5; FSD S8 A2.6, A2.9; TSD S8 T3.1 |
| BR3 | `deviationOpen` on the list stays rwb-case's `deviation_open` (DF-CAS-019) and this answer is the evidence beside it; the two are asserted equal on every page and neither is copied into the other schema | Legacy AC1, AC2; REQ-DVH-006; ASM-5307 |
| BR4 | `pauseRequired` is true while at least one deviation is open and false only when all are cleared; the pause holds the stage clock and never the prescription clock, and the clock itself is rwb-case's | R-DEV-01; R-DEV-18; FEAT-DVH-09; legacy BR4; ASM-5313 |
| BR5 | The codes, the actor values, the states and the lists are rows read at the version in force; no code, state, marker or bound is a constant, a default or a branch in the module | FSD S8 BR-S8-001, BR-S8-004; TSD S8 T3.2; DP-07 |
| BR6 | The request carries one to `pageBound` case ids, the bound is a parameter row (1 to 200 in the legacy validation), and an empty or over-long request is refused before any read | Legacy AC7, X2; DP-06 |
| BR7 | The answer carries identifiers, a boolean, a count, codes, a date and a state, and no case column and no person: no product, queue, owner, status, stage, age, clock, handler identity, name, contact value or note | Template and Rules §R7.2 (s17); legacy guardrail 2; TSD S8 T6.2 |
| BR8 | One base, one topic, one queue, one schema and one login per service; this slice publishes no event, writes no outbox row, starts no workflow and creates no Schedule | DP-13; DP-14; TSD S8 T5.3; legacy section 9 |

Covered by: BR1 AC6 and TC-E2-033-15; BR2 AC1 and AC4 with TC-E2-033-01 and TC-E2-033-02; BR3 AC3 with TC-E2-033-03; BR4 AC2 and AC4 with TC-E2-033-02; BR5 AC1 with TC-E2-033-01; BR6 AC5 with TC-E2-033-07; BR7 and BR8 AC6 with TC-E2-033-13; BR1, BR2, BR3, BR5, BR6, BR7 and BR8 also AC9 with TC-E2-033-18.

BR2 and BR3 are the two halves of one fact and are the reason this story exists: the owner of the deviation answers the evidence, the owner of the case answers the flag, and a test asserts they agree. BR4 is the word the page needs and is not a decision of this story — the pause and the resume are executed by the raise, route and clear steps in `DeviationWorkflow`. BR5 is executed by `DeviationFlagProjection`, which asks the reference-data contract for LOV-DEVIATION and never types a code; a build check fails on a code, a state or a bound in the source. BR7 is a property test: a synthetic personal value placed in a fixture column must not appear in the JSON, a log line or a span attribute.

### 9. State transitions

None. This story changes no case status, raises no deviation, clears none, pauses no clock and resumes none: it reads the `deviation` rows of a page and reports them, so the state machine of the DEV route set is not entered (TSD S8 T4). `DEV_FLAGGED`, `DEV_WITH_OWNER`, `DEV_RESOLVED`, `DEV_REROUTE` and `RESUMED` belong to the raise, route, handle and clear steps of this service, and `deviation_open` and the `SERVICE_LEVEL` and `PRESCRIPTION` timers are rwb-case's.

| Read or step | Condition | Result |
|---|---|---|
| The page read | The Case record right R is granted and the page is inside the bound | One row per case id in scope; nothing is written |
| The page read | A named case is outside the caller's scope | No row for it, and no message that names it |
| The projection | No open deviation | `deviationOpen` false, count 0, no code, no date, no stop, no paused state, `pauseRequired` false |
| The projection | One open deviation | `deviationOpen` true with one code, its raised date, the stop and the paused state, `pauseRequired` true |
| The projection | Two open deviations, one cleared | Count 2 with two codes; the cleared row is absent; `pauseRequired` stays true |
| The projection | The parameter or the reference-data read does not answer | 503 with MSG-GEN-006; no partial answer is served |

The case-side states that the list shows beside this answer — NEW, ASSIGNED, IN_PROGRESS, the service level state BREACHED, RUNNING, PAUSED or NONE and the prescription clock RUNNING, EXPIRED or NONE — are rwb-case's and RWB-P2-E2033-APP's, and this slice neither computes nor stores them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | Case record R (TSD S8 T6.1): reads the deviation state of every case of the team's queues |
| RW-CASEOWN, case owner | Case record CRU: reads the same answer for the cases they own; raises and clears a deviation in the Epic 2 stories, not here |
| RW-PRODHEAD, RW-AUDIT, RW-CONDUCT, RW-COE and other roles with Case record R | Read the answer in their scope |
| RW-REFADM and a role without Case record R | Refused with 403 and MSG-P4-002 before a row is read |
| rwb-deviation service identity (the service login, DP-02) | Serves the read, reads `deviation` in `rwb_deviation` and the two owner contracts of DP-06 and DP-07, and holds no grant on another schema and no `v_ace_*` grant |
| SY-RULES, the embedded rule kit | Not used by this slice: it evaluates no rule of the DEV package and only reports rows the raise and clear steps wrote |
| No approval applies | The story takes no decision and changes no state |

The rights are the rows of TSD S8 T6.1 and the declared right of the read in T-A.1. The scope and its default are rwb-access's data and are applied per case; this story adds no right, widens none and names no person.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 | deviation (S8, `rwb_deviation`) | id | Read, the reference of each open row |
| DF-CAS-037 | deviation (S8, `rwb_deviation`) | case_id | Read, the key of the projection |
| DF-CAS-038 | deviation (S8, `rwb_deviation`) | deviation_code | Read, into `openCodes` |
| DF-CAS-039 | deviation (S8, `rwb_deviation`) | raised_at | Read, into `firstRaisedAt` |
| DF-CAS-041 | deviation (S8, `rwb_deviation`) | paused_state | Read, into `pausedState` |
| DF-CAS-043 | deviation (S8, `rwb_deviation`) | contact_stop | Read, into `contactStop` |
| DF-CAS-044 | deviation (S8, `rwb_deviation`) | cleared_at | Read, to tell an open row from a cleared one |
| DF-CAS-045 | deviation (S8, `rwb_deviation`) | outcome | Read, to tell a resolved row from an open one |
| Standard columns | deviation (S8, `rwb_deviation`) | `is_active`, `state`, `version` | Read, `state` as the second test of an open row |
| DF-CAS-002 to DF-CAS-019 | recovery_case (P3) | case_no, product_group, status, stage_code, owner_user_id, queue_id, entry_date, stage_clock_start, deviation_open | Not read: the row and the flag are rwb-case's and reach the page through RWB-P2-E2033-CON; `deviation_open` is asserted equal, never copied |
| DF-WRK-002 to DF-WRK-035 | queue, timer (P3) | queue_code, team_code, timer_type, expires_at, paused, status | Not read: the queue and the clocks are rwb-case's |
| DF-REF-038 | role (P4) | default_scope | Not read: the scope arrives in the cached authorise decision |

Field IDs are those of TSD S8 T3.1 and the Logical Data Model and Data Dictionary v9. **No write, no new column and no new business table**: this story reads rows another step writes, and its one migration adds a read-only view and an index in `rwb_deviation` (DP-15; ASM-5314).

No personal data. The answer carries a case reference, a boolean, a count, codes of LOV-DEVIATION, one date and one state name. `handler_user_id` (DF-CAS-042) is deliberately not read into the answer, because it identifies a person and a list cell does not need it (BR7).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13).

| Method | Path | Query | Answer | Access | Idempotency |
|---|---|---|---|---|---|
| GET | `/deviation-flags` | `caseId` repeated, required, 1 to the page bound of the parameter contract | One row per case id and no other field: `caseId`, `deviationOpen`, `openDeviationCount`, `openCodes`, `firstRaisedAt`, `contactStop`, `pausedState`, `pauseRequired` | Case record right R, scope applied per case, through the rwb-access authorise contract | Idempotent read; no `Idempotency-Key` and no stored response |

Errors: 401 no Workbench identity (MSG-P4-001); 403 no Case record right R (MSG-P4-002); 422 `caseId` absent or malformed (MSG-GEN-001) or more case ids than the page bound (MSG-GEN-002); 503 a consumed contract that does not answer inside the budget (MSG-GEN-006). A case in scope with no deviation answers a row with `deviationOpen` false, and a case outside the scope is absent from the answer with no message.

The path and the field names are not rows of the Ownership Map and are not named by any source: the Ownership Map gives S8 `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` and no read, so this operation is declared here with a gap and an assumption and its exact form is fixed at the contract review (GAP-3101; ASM-5306). `deviationOpen` on the page stays the rwb-case field of RWB-P2-E2033-CON; this answer is what the deviation cell of a row shows when the flag is Yes (BR3), and the extract's deviation column is the same answer, while the Excel file itself is RWB-P2-E2033-APP's (ASM-5315).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Case record right R, the caller's scope and its default scope, cached per session by the guard library (DP-08; RWB-P4-E1037-CON) |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The page bound of the request, with the version in force (DP-06; RWB-P3-E1042-CON) |
| GET | The reference-data read of the RWB-P3-E1043-CON contract (path Not specified in the source documents (GAP-3101; ASM-5311)) | P3 rwb-case | LOV-DEVIATION and LOV-RAISED-BY at the version in force (DP-07) |

Every row is one hop with a 2 s client budget and a breaker per downstream (ADR-020). The three rows are class C dependencies in fact that the plan does not hold, because this story's C row is `RWB-P2-E2033-CON` and its H row is None; they arrive with the platform libraries of DP-06, DP-07 and DP-08 (GAP-3101; ASM-5308).

#### 12.3 Events published

None. A list read raises nothing: `rwb.deviation.DeviationRaised.v1` (EV-06) and `rwb.deviation.DeviationCleared.v1` (EV-07) on `rwb.deviation.events.v1` belong to the raise and clear steps of this service, and this slice writes no outbox row (DP-14 as a prohibition; TSD S8 T5.3).

#### 12.4 Events consumed

None. The page is composed per request, so this slice subscribes to no topic, holds no consumer group and writes no inbox row; a deviation raised or cleared between two reads is seen on the next read and not through a projection of `rwb.deviation.DeviationRaised.v1`.

#### 12.5 Workflows and activities

None. The read is synchronous, in the caller's thread, one hop and 2 s. `DeviationWorkflow` on queue `rwb-deviation` is the always-on child of `CaseWorkflow` that pauses and resumes the stage clock, and it belongs to the raise, route, handle and clear steps; this slice starts no workflow and contributes no activity to it.

#### 12.6 Schedules

None. The answer is read on request; the service owns no job in its ownership rows (Jobs 0). The deviation service level of R-DEV-20 is a workflow timer of the handling step and not a Temporal Schedule, and no batch window is declared here.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| deviation | S8 (`rwb_deviation`) | Read only: the open rows of the cases of one page |
| v_deviation_flag | S8 (`rwb_deviation`) | Read only view over `deviation`, created by this story's migration, with its index (DP-15); a migration object recorded here, not a field of LDM v9 or Data Classification v5 |
| outbox_event | PLT library, created in `rwb_deviation` | Present for the raise and clear steps; this slice writes none of its rows |
| processed_event | PLT library, created in `rwb_deviation` | Present for the consumers of other stories; this slice writes none of its rows |
| idempotency_key | PLT library, created in `rwb_deviation` | Present for the write operations; this slice writes none of its rows |

Not owned and never read as a table: `recovery_case`, `queue` and `timer` (P3), the `v_ace_*` views (P1), `role` and the access log (P4). `case_id` is a reference and not a key across schemas, and no foreign key leaves `rwb_deviation` (DP-01).

#### 12.8 Contract fakes

| Fake | Documents | Used by |
|---|---|---|
| RWB-P2-E2033-CON case-list fake | Cases `RW-2026-000101` to `RW-2026-000105`, `RW-2026-000201` and `RW-2026-000502` with their queue, team, owner, status and stage clock, and `deviationOpen` set to agree with this answer on every row | AC1, AC3, AC5 |
| rwb-case parameters fake | The case-list page bound 1 and 200; a bound absent and a bound of a different version | AC5, X3, X5 |
| rwb-case reference-data fake | LOV-DEVIATION with X1 to X7 and LOV-RAISED-BY at the version in force; a code that has left the version and a slow answer beyond 2 s | AC1, AC4, X5 |
| rwb-access decision fake | A granted Case record right R with Team scope over `MTG-BKK`, a refused decision for `RW-REFADM`, and a scope that excludes `HP-NE-CO` | AC5, X1, X4 |
| gateway-bff composite route stub | The SCR-02 route and the row model the deviation cell sits in (DP-19) | AC2, AC3 |

The fakes are test-only and are replaced by the real services in SIT. No fake carries personal data: every deviation and every case in the fixtures is synthetic.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 consumed | `GET /deviation-flags` on `/api/recovery/deviation/v1`; the authorise check, the parameter read and the reference-data read, each one hop with 2 s and a breaker |
| Kafka | 0 published, 0 consumed | The two events of the service belong to the raise and clear steps |
| Temporal | None | No workflow, no activity and no Schedule in this slice |
| File | None | No file is read, built or delivered here; the extract is RWB-P2-E2033-APP's |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.deviation`, module `list-support`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DeviationFlagController` | Controller | The operation of 12.1, the query binding of the repeated `caseId`, the problem mapping of section 14 |
| `DeviationFlagGuard` | Guard | The Case record right R from the cached decision of rwb-access, the per-case scope and the refusal before any read |
| `PageBoundValidator` | Service | The request against the page bound of the parameter contract (BR6) |
| `OpenFlagReader` | Repository | The open rows of the page from `v_deviation_flag` in `rwb_deviation`, with the columns of §11 and no other table |
| `DeviationFlagProjection` | Service | Groups the rows per case into the eight fields of 12.1, with the codes in the order of LOV-DEVIATION at the version in force and `pauseRequired` from the open count (BR2, BR4) |
| `FlagAnswerAssembler` | Service | One row per case id of the request, no other field, no person, no case column (BR7) |
| `AuthoriseClient`, `ParameterClient`, `ReferenceDataClient` | Client | The three consumed contracts, one hop, 2 s, breaker, cached for the request |

**Database and migrations.** One step in the per-service Flyway sequence of `rwb_deviation` (DP-15): `V2033_1__deviation_flag_read.sql`, which creates the read-only view `v_deviation_flag` over `deviation` — the open rows with their case, code, raised date, contact stop, paused state, state and cleared date — and one index on `(case_id)` with the open predicate. No business table, no column and no constraint is added, and no migration of this service touches another schema or the shared baseline. The view and index names are a design choice fixed by no source document (ASM-5314).

**Configuration and reference data.**

- LOV-DEVIATION and LOV-RAISED-BY are read at the version in force; no code is a constant of the module (DP-07, BR5).
- The page bound of the request is a parameter row of rwb-case, 1 to 200 in the legacy validation; its value and version come from the parameter contract (DP-06; ASM-5309).
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.
- The flag `rwb.deviation.list-support` is a flag of the platform library: off means the operation answers 503 with MSG-GEN-006 and the composed page shows `deviationOpen` from rwb-case alone, while no deviation row changes.

**Build steps**

1. The view and its index in the service's Flyway sequence, applied on an empty `rwb_deviation` and on a loaded one (AC1, DP-15).
2. `OpenFlagReader` with the open-row predicate and the columns of §11; unit tests for AC1 and X6.
3. `DeviationFlagProjection` over the reference-data fake, with one code, two codes, a cleared code and a code absent from the version in force; unit tests for AC1, AC4 and X7.
4. The operation with the guard, the per-case scope and the bound validator; API tests for AC1, AC5, X1, X2, X3 and X4.
5. `FlagAnswerAssembler` and the property test that a synthetic personal value in `handler_user_id` and in a free-text fixture reaches no answer, no log line and no span attribute (AC6, BR7).
6. The build check that fails on a code, a state or a bound in the source and on any statement outside `rwb_deviation` (BR5, X8).
7. The agreement test with the RWB-P2-E2033-CON fake: for every case of the fixture, `deviationOpen` here equals `deviationOpen` there (AC3, BR3).
8. A fake run of the three consumed contracts, including the slow answer, so the refusal and the unavailable answer are reachable before SIT (X5, AC5).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/deviation/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.deviation.events.v1`; naming library; no event is added | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: the metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P2-E2033-CON` exactly as the Work Package fixes them, so the six platform contracts that DP-06, DP-07, DP-08, DP-14, DP-15 and DP-19 name arrive with the service template and are not written into the H row (GAP-3101; ASM-5308).

- **DP-01** keeps the whole answer inside `rwb_deviation`; a statement on any other service's schema or table, or on a `v_ace_*` view, fails the boundary test. **DP-15** puts the view and its index in the per-service Flyway sequence, never in the shared baseline.
- **DP-06** is the page bound of the request and **DP-07** the two lists, each read at the version in force, which is what lets the projection cover exactly the codes in force. **DP-08** is the authorisation decision, consumed as the cached permission of the service and not built here.
- **DP-13** gives the read its base `/api/recovery/deviation/v1`, **DP-14** keeps the topic and the event names of the service untouched because this slice adds no event, and **DP-19** is the route the composed list reads through.
- **DP-17** does not apply: no file, no data-lake copy and no extract is built here.

**Done when.** The tests of section 16 pass, the read answers the eight fields of `RW-2026-000101`, `RW-2026-000104` and `RW-2026-000502` on the fakes, `pauseRequired` holds while one of two deviations is open and falls only after the last is cleared, every page answers the same `deviationOpen` as the RWB-P2-E2033-CON fake, an identity without the right is refused with MSG-P4-002 and a case outside the scope is absent without a message, the migration applies cleanly on an empty `rwb_deviation`, and no statement outside the schema exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No valid session or no Workbench role (X1) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | The caller holds no Case record right R (X1, AC5) | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | No `caseId` is named or a value is not a case reference (X2) | Enter {field}. |
| MSG-GEN-002 | More case ids than the page bound (X3, AC5) | {field} must be between {min} and {max}. |
| MSG-GEN-006 | The parameter or the reference-data read does not answer inside the budget (X5) | Not specified in the source documents (GAP-3101; ASM-5310) |
| None | A case outside the scope (X4) | No message: the row is absent, and a message would reveal that the case exists |

The message identifiers and texts are those of the legacy story and the FSD message set, copied unchanged. For MSG-P4-002, {action} names the action the caller tried — "read the deviations of this page" — and never a case fact. For MSG-GEN-002 the bound pair is the one the parameter contract returns. The FSD names MSG-GEN-006 in its exception flows with the name of the module and prints no text, so the placeholder stands and the text is fixed by the platform Error and Message Standard (ASM-5310). Here MSG-GEN-006 carries only the timeout meaning of the parameter or reference-data read; the use in the legacy P2 story is not this story's. Errors are RFC 9457 problem responses with `messageId`, `detail` with the placeholders filled and `instance` naming the request; the HTTP mapping is 403 for MSG-P4-002, 422 for MSG-GEN-001 and MSG-GEN-002, and 503 for MSG-GEN-006. MSG-P3-020, MSG-P3-021, MSG-GEN-007 and MSG-P7-003 are the composed page's and the export's in RWB-P2-E2033-APP and are not restated here.

### 15. Screens and states

No screen is built in this story. The answer is what the deviation cell of SCR-02 Case list shows: the flag, the codes, the date the earliest open deviation was raised, "Contact stopped" and the paused state, with the text "Held" when `pauseRequired` is true so the cell does not rely on colour alone. The screen, its Loading, Empty, List and Filtered states, the "Breached" and "Paused" markers, the twelve columns and the Extract button belong to RWB-P2-E2033-APP, and the composition reaches this answer through the gateway-bff composite route of RWB-PLT-N001-CON (DP-19). The Loading and Empty states of SCR-02 Case list are those of Screen Specifications v1; its error and no-access states are Not specified in the source documents (CG-ALL-11394). The empty, loading, error and no-access states of the screens named in this section are not built here and stay with RWB-P2-E2033-APP.

The deviation screens of this service — SCR-06 Raise deviation and SCR-08 Deviation queue — are other stories' and are untouched here: this story adds no column to them and changes no behaviour of the case record view. Their states here: SCR-06 Raise deviation has empty, loading, error and no-access states Not specified in the source documents (CG-ALL-11395); SCR-08 Deviation queue has a loading state of Screen Specifications v1 and empty, error and no-access states Not specified in the source documents (CG-ALL-11396). None of them is built here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-033-12 | AC5 for the refusal of this read: an identity without Case record R is refused with 403 and MSG-P4-002 before a row is read | Component | RW-REFADM reads a page of one case; RW-TEAMMGR is granted the same read |
| TC-E2-033-01 | AC1 for the flag half: three cases with no deviation answer `deviationOpen` No and `pauseRequired` false. The status, owner and age columns belong to RWB-P2-E2033-APP | Component | Cases `RW-2026-000101` to `RW-2026-000103` of team MTG-BKK as in the legacy story |
| TC-E2-033-02 | AC2 and AC4 for the paused case: open X1 answers `pauseRequired` true, paused state, contact stop and the raised date, beside the case's PAUSED service level and RUNNING prescription clock | Component | Case `RW-2026-000104`, X1 raised 9 December 2026, prescription date 30 June 2028 |
| TC-E2-033-03 | AC3 for the extract half: the page and the export with the same filters answer the same deviation value for every case. The file is built by RWB-P2-E2033-APP | Component | Four cases; filters queue, product and breached; two reads compared |
| TC-E2-033-04 | No criterion here: the breach boundary at 09:00 and 09:01 is the case-side computation of RWB-P2-E2033-APP; this answer carries no breach flag | Component | Timer due 10 December 2026 09:00 |
| TC-E2-033-05 | AC1 for the no-timer case: a NEW case with no deviation answers `deviationOpen` No. The NONE service level state belongs to RWB-P2-E2033-APP | Component | Case `RW-2026-000103`, no SERVICE_LEVEL timer |
| TC-E2-033-06 | No criterion here: the product filter value is the page's, validated against the rwb-case reference data | Component | Product filter CAR |
| TC-E2-033-07 | AC5 for the bound: a request with 500 case ids is refused with 422 and MSG-GEN-002 naming 1 and 200 | Component | Page bound 1 and 200 from the parameter fake; 500 case ids |
| TC-E2-033-08 | No criterion here: the empty page is the page's; this read is asked for no case and answers no row | Component | Filter product SSME with no case |
| TC-E2-033-09 | AC5 for the scope: a case of team HP-NE named by the MTG-BKK manager is absent from the answer with no message | Component | Case `RW-2026-000201` in queue `HP-NE-CO` |
| TC-E2-033-10 | No criterion here: the extract row limit is the export's in RWB-P2-E2033-APP | Component | 10,001 matching cases |
| TC-E2-033-11 | No criterion here: the order across pages is composed by RWB-P2-E2033-APP; this answer keeps the order of the requested case ids | Component | 120 cases of equal age, pages of 50 |
| TC-E2-033-14 | Contract: the operation of section 12.1 and its errors answer as rwb-deviation.yaml publishes them, with the fields and the 422 and 503 cases of section 12.1 | Contract | Not specified in the source documents (DOR-RWB-S8-E2033-APP-12) |
| TC-E2-033-15 | Boundary: the read reaches the tables of section 12.7 only through `deviation` and `v_deviation_flag` in `rwb_deviation`; no other table or schema is read (ASM-3438) | Component | Not specified in the source documents (DOR-RWB-S8-E2033-APP-12) |
| TC-E2-033-16 | AC7 for the budget: a parameter or reference-data read that answers after the budget Not specified in the source documents (DOR-RWB-S8-E2033-APP-3) is refused with 503 and no partial answer is served | Component | Parameter or reference-data fake that answers after the budget Not specified in the source documents (DOR-RWB-S8-E2033-APP-3) |
| TC-E2-033-17 | AC8 for the reference-data read: a reference-data read that answers after the budget Not specified in the source documents (DOR-RWB-S8-E2033-APP-3) is refused with 503 and no partial answer is served | Component | Reference-data fake that answers after the budget Not specified in the source documents (DOR-RWB-S8-E2033-APP-3) |
| TC-E2-033-18 | AC9 for the rules with no other criterion: BR1, BR2, BR3, BR5, BR6, BR7 and BR8 hold on every answer | Component | A page of case ids read against the reference-data rows at the version in force; the answer, the reads and the outputs inspected |
| TC-E2-033-19 | AC10 for the 401 and 404 answers of the provided operation as section 12.1 publishes them | Contract | Calls without identity and to a path the contract does not publish |
| TC-E2-033-20 | AC11 for a consumed call that fails: the read is refused with 503 and no partial answer is served | Component | Access contract fake that returns an error for the Case record right check |

The twelve legacy cases of RWB-E2-033 are listed in their legacy order with the Level column added, and each names the slice of behaviour this story answers: the flag and the pause for TC-E2-033-01, -02, -05 and the access, bound and scope cases for -12, -07 and -09; every other case is the page's and is listed with no criterion here. The legacy table publishes no level, so one is assigned per case: legacy "System" maps to Component for a single-service half, and "Access" maps to Component (GAP-3101; ASM-5312). The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID. No `-ITG` copy is written here: the same values across rwb-case, rwb-deviation, rwb-access and the composed page are RWB-ITG-E2033-ITG's.

### 17. Guardrails

- No business value in code: the codes, the states, the actor values, the markers and the page bound are rows or parameters read with their version. A build check fails on a code, a state or a bound in the source.
- No personal data in the answer, an event, a workflow input or a log: a case reference, a boolean, a count, codes, one date and one state only. `handler_user_id` is not read into the answer, and a property test asserts that a synthetic personal value never reaches the JSON, a log line or a span attribute.
- ACE data only through the owner's contract or a `v_ace_*` view: this service holds no `v_ace_*` grant, reads no ACE table and needs no ACE product.
- No cross-schema read and no cross-schema key: `rwb_deviation` holds the row, `case_id` is a reference, and a statement on `rwb_case` or `rwb_access` fails the boundary test (DP-01).
- The case column is never copied: product, queue, owner, status, stage, age and the two clocks stay rwb-case's, and a row that carries one of them fails the contract test (BR7).
- One event owner per fact: this slice publishes nothing and writes no outbox row, and a build that raises an event from a list read fails the acceptance test (DP-14).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- Any migration is a step in the per-service Flyway sequence of `rwb_deviation`, versioned and repeatable, and touches no other schema (DP-15).
- No retired element is reintroduced: no Quartz row, no shared job table, no monolith base, no login of the retired shared recovery service and no data-lake extract.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Story element | Test cases |
|---|---|---|---|---|---|
| REQ-WKM-002 | The team manager sees every queue of the team, filters by status, product and ageing, and exports the view (Business Requirements Epic 2, section 3.2) | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | The deviation state of every case of one page, so the list says where work waits and why | TC-E2-033-01, TC-E2-033-03 |
| REQ-DVH-006 | The deviation flag is visible on the case record view and in every queue view (Epic 2, section 3.2; FEAT-DVH-01) | FEAT-DVH-01 | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | `deviationOpen`, the codes, the raised date, the contact stop and the paused state of a page, asserted equal to the case-side flag | TC-E2-033-01, TC-E2-033-02, TC-E2-033-03 |
| REQ-ACA-006 | Every read of the case store is written to the access log | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | Not answered here: the entry belongs to the export in RWB-P2-E2033-APP, and this read is a deviation read that carries no case content | TC-E2-033-03 (no criterion here) |
| D-RCV-60 DP-01 | The row and the view are this service's and no other service's table is read | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | `deviation` and `v_deviation_flag` in `rwb_deviation`, the boundary test | TC-E2-033-01, TC-E2-033-09, TC-E2-033-15 |
| D-RCV-60 DP-06 | The page bound is a parameter row and not a constant | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | `PageBoundValidator` and the parameter read | TC-E2-033-07 |
| D-RCV-60 DP-07 | The codes and the lists are read at the version in force | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | `DeviationFlagProjection` and the reference-data read | TC-E2-033-02, TC-E2-033-04 |
| D-RCV-60 DP-08 | The right and the scope come from rwb-access | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | `DeviationFlagGuard` and the authorise read | TC-E2-033-12, TC-E2-033-09 |
| D-RCV-60 DP-13, DP-19 | One base per service and one composite route per screen | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | Not specified in the source documents (DOR-RWB-S8-E2033-APP-2) | `GET /api/recovery/deviation/v1/deviation-flags` and the SCR-02 route | TC-E2-033-03, TC-E2-033-14 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy story RWB-E2-033 — the list, its columns and the paused clock (sections 2, 4, 5, 11 and 15; BR4; AC2, AC5, AC9) | Sections 1 to 5, 7, 8, 11, 16 |
| Legacy values reused — cases `RW-2026-000101` to `RW-2026-000105`, `RW-2026-000201` and `RW-2026-000502`, X1 raised 9 December 2026, prescription date 30 June 2028, paused state `WITH_FCR_OFFICER`, the date 10 December 2026 09:00, the page bound 1 and 200, teams MTG-BKK and HP-NE | Background, sections 7 to 16 |
| MSG-P4-001, MSG-P4-002, MSG-GEN-001, MSG-GEN-002, MSG-GEN-006 | Section 14, exception paths |
| TC-E2-033-12 and TC-E2-033-01 to TC-E2-033-11 | Section 16 |
| Legacy criteria AC1 to AC11 | Owned by RWB-P2-E2033-APP; not restated here (section 7) |
| R-DEV-01, R-DEV-09, R-DEV-18, FEAT-DVH-01, FEAT-DVH-04, FEAT-DVH-09 | Sections 2, 8, 9 |

### 19. Out of scope

- The case rows, the queues, the owner, the status, the stage, the age in state, the service level state and the prescription clock of the list, the breach filter, the order, the paging and the Excel extract: RWB-P2-E2033-APP and the contracts of RWB-P2-E2033-CON.
- The case-side fields themselves (`recovery_case`, `queue`, `timer`) and the `deviation_open` flag: rwb-case, in its own stories and schema.
- Raising, routing, handling and clearing a deviation, the contact stop and the pause and resume of the clocks: the Epic 2 stories of this service and `DeviationWorkflow`; the two write operations API-S8-001 and API-S8-002.
- The deviation screening agent, its policy and its evaluation: RWB-P10-E1062-APP and RWB-S8-E1062-APP.
- The deviation screens SCR-06 and SCR-08 and their states: the other stories of this service.
- The right, the scope, the default scope and the access log: RWB-P4-E1037-CON and the rwb-access stories.
- The gateway-bff composite route, its path and its merge order: RWB-PLT-N001-CON.
- The service baseline, the problem mapping, the naming library and the Flyway conventions of rwb-deviation: RWB-PLT-TPL, RWB-PLT-E1044-CON, RWB-PLT-E1047-CON and RWB-SVC-S8's baseline stories.
- Any data-lake copy of the list or of a deviation: DP-17.
- The real cross-service journey with all services live: RWB-ITG-E2033-ITG.
- The field-level completeness of the consumed contracts and the exact form of the declared path (GAP-3101).
