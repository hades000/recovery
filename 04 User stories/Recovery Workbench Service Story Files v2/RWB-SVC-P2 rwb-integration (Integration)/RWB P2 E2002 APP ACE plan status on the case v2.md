# RWB-P2-E2002-APP ACE plan status on the case

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Size | Set by the squad at refinement |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P2-A |
| Ready to start | After RWB-P2-E2001-APP |
| Depends on (build) | RWB-P2-E2002-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P2-E2001-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E2042-CON |
| Integration dependencies | None |
| External dependencies | RWB-P2-E2002-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (FR-P2-019) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-002 for rwb-integration. The stored plan status, its date, the compare, the route move, the rule evaluation, the task, the durable timer, the local decision record and the plan status panel stay with rwb-case (RWB-P3-E2002-APP); this story keeps the call to the ACE common module, the live plan-status answer on `/api/recovery/integration/v1`, the status validation, the access check and the rule that a read writes nothing. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P2-E2002-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 27 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the restructure plan status of my case read live from the ACE common module through one integration operation that answers the plan reference, the account, the status, the status date and a flag that says it was read now**, so that **the case side can show a live status or fall back to the status the case holds, and a case with a live plan is never treated as if it had none**.

The operation is `GET /api/recovery/integration/v1/cases/{caseId}/plan-status`, served by `PlanStatusController` and `PlanStatusService` and backed by `AcePlanClient`, which wraps the ACE common module's published `RestructurePlanQuery.statusFor` in batches of 500 account numbers with a 2,000 ms budget per call (INT-34; DL14). The answer is `planRef`, `accountNo`, `status`, `statusDate`, `live` and `messageCode`. The status is validated against the plan status list LOV-PLAN-STATUS read through the rwb-case reference-data contract, the caller's Case record right and scope are checked through the rwb-access authorise contract, and the read writes nothing anywhere.

The legacy story held the plan read, the stored plan status, the broken plan rules, the route move, the task, the timer and the decision log entry in one module. Under D-RCV-60 that journey is cut across services and this story is the integration half of it:

- **Here.** The call to the ACE common module, the batching and the 2,000 ms budget, the mapping of a plan to a case by account number, the status validation, the access check, the live answer and the read-only rule.
- **In RWB-P3-E2002-APP.** The case of record: `plan_ref`, `plan_status` and `plan_status_as_of` in `rwb_case`, the compare, package RESTRUCTURE evaluated by the embedded Drools kit, the route state, the task, the durable timer, the decision record and the plan status panel. Its daily `readPlanStatus` activity calls this operation inside the plan-status step of JOB-02.
- **In RWB-P4-E2002-APP and RWB-P7-E2002-APP.** The role and scope data, and the rule package registry with the evaluation and the central ledger.
- **In RWB-ITG-E2002-ITG.** The cross-service proof of the nine legacy criteria as one journey.

### 2. Business rationale

Restructure plans are calculated and held in ACE (DL14). Without the plan status on the case, a recovery officer can start litigation on a customer who is paying a plan, or miss a plan that broke. The legacy story read the status from the ACE common module each morning and on each case view, kept the last known status with its date when ACE returned none, and raised a broken plan to the restructure rules R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 of package RESTRUCTURE.

Only one service may speak to an outside system, and in the target that service is rwb-integration: the ACE common module publishes `RestructurePlanQuery` (INT-34), and the plan status leaves the bank's plan engine through that interface and no other path. Making the read a service of its own does three things the monolith could not. It bounds the outside call: 500 account numbers per call, 2,000 ms per call, a breaker per downstream and a versioned status list, so a slow ACE cannot hold a case record screen or a nightly run. It makes the answer honest: the `live` flag says whether the value was read now, so the stored answer of the case and the live answer cannot be confused. And it keeps the read side-effect free, so a screen refresh or a rerun can never write a plan status.

**What the split changes, and why it changes here.**

- **DP-01.** `rwb_integration` holds no case row, no account row and no plan row, and no foreign key crosses a schema. The case is reached by its reference through the rwb-case contract; the plan is reached through the ACE interface.
- **DP-03.** No decision record is written by this story: a read takes no decision, and the record of a route move belongs to the service that moves the case. The decision-record library is a dependency of the service build, not of this operation.
- **DP-04.** No rule package is evaluated here. Package RESTRUCTURE, its version, the embedded Drools kit and the catalog rows stay with rwb-case and rwb-decision (RWB-P3-E2002-APP, RWB-P7-E2002-APP); this slice carries the kit dependency because the service ships it, and evaluates nothing.
- **DP-05.** The plan is read through the ACE common module's published interface (INT-34), not through a `recovery.v_ace_*` view and not through a table: the interface is a module interface, not a view, so the direct call of the legacy story stays where the legacy story has it, bounded by the 2,000 ms budget and the batching. Only rwb-source-data reads the thirty views (ADR-010; Arch v5 slides 8, 9, 13, 29, 37 and 45), and `rwb_integration` holds no grant on `recovery`. The TSD path that reads `v_ace_plan` and falls back to the case columns is recorded as a conflict, not followed.
- **DP-06.** The batch size and the timeout are data: `rwb.ace.plan.batch-size` = 500 and `rwb.ace.plan.timeout-ms` = 2000 are read through the rwb-case parameters contract, never written in code.
- **DP-07.** The plan status list LOV-PLAN-STATUS is reference data of rwb-case, read through its contract with the version in force; no status code is written in code.
- **DP-09.** No event is published or consumed by this story. The outbox, inbox and idempotency objects exist in `rwb_integration` for the service's file stories; a read writes no outbox row.
- **DP-10.** No Temporal Schedule and no workflow is created here. The daily plan-status step is a step of JOB-02 owned by rwb-case, which calls this operation inside its own activity; this operation answers synchronously on the request path.
- **DP-11.** The in-process calls of the legacy module become REST contracts with fakes: the case read, the reference-data read, the parameter read and the authorise call, plus the ACE interface call, each one hop with a 2,000 ms budget and a breaker.
- **DP-13.** The legacy operation moves from the monolith base to `/api/recovery/integration/v1` (Ownership Map; TSD P2 v3 API-P2-010).
- **DP-15.** One Flyway sequence in `rwb_integration`; this story adds no table and no column, so it adds no migration.
- **DP-19.** The case record reads the plan section through the gateway-bff composite route, which calls this operation and the rwb-case stored answer in parallel and merges them; the browser calls neither service directly.

It meets REQ-DRI-013 (the plan status is read from the ACE common module) and REQ-CHO-002 (a change to a plan status in ACE is visible on the case through the ACE common module), and it carries the legacy measure in its own half: the live answer exists, is bounded, is validated and writes nothing, so a case with a live plan can never be treated as if it had none for want of a read.

### 3. Preconditions

- RWB-P2-E2002-CON is published: the resource shape (`planRef`, `accountNo`, `status`, `statusDate`, `live`, `messageCode`), the operation, the error envelope, the ACE interface stub and the fakes of rwb-case, rwb-access and rwb-decision. This story builds against that baseline.
- RWB-P2-E1007-APP and RWB-P2-E2001-APP are delivered: the integration base with its controller conventions, its problem-response mapping, its contract-client, breaker and idempotency handling, and its worker and health surface.
- RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are published: the decision-record library, the embedded Drools kit, the parameter and reference-data client libraries, the outbox and inbox library, the workflow kit, the migration conventions and the gateway-bff composite route.
- RWB-P3-E1042-CON and RWB-P3-E1043-CON are published: the parameters contract and the reference-data contract of rwb-case, which carry `rwb.ace.plan.batch-size`, `rwb.ace.plan.timeout-ms` and LOV-PLAN-STATUS with the version in force.
- RWB-P3-E2042-CON is published: the rule catalog and package read of rwb-decision, so a case that moves can name its rule and its package version. This story consumes none of it and holds no catalog row.
- The rwb-case case read and the rwb-access authorise contract are published, or are faked to the shapes of RWB-P2-E2002-CON: the case with its account numbers and its owner and queue, and the Case record R right with the scope.
- The ACE common module publishes `RestructurePlanQuery` in SIT and UAT (INT-34; DL14), and the stub of that interface answers in SIT before the real ACE endpoint is reached.
- LOV-PLAN-STATUS holds CREATED, APPROVED, BOOKED and BROKEN in the rwb-case reference data (RW-COE), and "SUSPENDED" is the code the negative tests drive.
- The parameter rows `rwb.ace.plan.batch-size` = 500 and `rwb.ace.plan.timeout-ms` = 2000 are in force (assumed; DL11: ASM-0553, ASM-0703, ASM-1051, ASM-1104), as parameter rows and not as code.
- The feature flag `rwb.integration.ace-plan-status` is registered in the platform flag library; on, the operation answers live; off, it answers the stored-only refusal without calling ACE.
- The login is the rwb-integration login (DP-02): Not specified in the source documents (GAP-0654; ASM-1099).

### 4. Flow

1. Caller: rwb-case's `readPlanStatus` activity inside the plan-status step of DailyCaseRun, or gateway-bff on behalf of the case record, calls `GET /api/recovery/integration/v1/cases/{caseId}/plan-status` with the case ID only (one hop, 2 s client budget, DP-11). The `readPlanStatus` activity calls the operation once per case, and no batch form of the operation is used; the page size and the bounded concurrency of these calls come from the parameter `rwb.ace.plan.batch-size` = 500 and the timeout from `rwb.ace.plan.timeout-ms` = 2000 (GAP-0769).
2. rwb-integration: reads the case through the rwb-case contract, by case reference only: the account numbers used for the join, the owner and the queue, and the scope facts the authorise answer is checked against (DP-01).
3. rwb-integration: checks the Case record R right and the case scope through the rwb-access authorise contract, cached per session; a refusal ends the request before any ACE call and before any read of the cache (MSG-P4-002, MSG-P4-003).
4. rwb-integration: reads `rwb.ace.plan.batch-size` and `rwb.ace.plan.timeout-ms` through the parameters contract of rwb-case with the version in force, cached for the life of the process and refreshed on a version change (DP-06).
5. rwb-integration: reads LOV-PLAN-STATUS with the version in force through the reference-data contract of rwb-case, cached with its version (DP-07).
6. rwb-integration: checks the feature flag `rwb.integration.ace-plan-status` from the platform flag library; off ends the request with the stored-only answer and no ACE call.
7. rwb-integration: `AcePlanClient` calls `RestructurePlanQuery.statusFor` with the account numbers of the case in batches of 500, each batch bounded by the 2,000 ms budget, with a breaker per downstream and one retry of a read with jitter.
8. rwb-integration: maps each returned plan to its account number and takes the plan of the case: `planRef`, `accountNo`, `status`, `statusDate`. An account absent from the answer is an account with no plan, not an error.
9. rwb-integration: validates the status code against LOV-PLAN-STATUS. A code in the list is answered unchanged. A code not in the list is answered unchanged as well: it is never mapped, labelled, coerced or defaulted to a known value, it is counted as an unknown status for the dashboard and the alert of RWB-P2-E2002-OPS, and the case side, which reads the same list through the same contract, is what refuses to store it (MSG none; legacy X3).
10. rwb-integration: answers 200 with `planRef`, `accountNo`, `status`, `statusDate`, `live` true and `messageCode` empty, and writes nothing: no table row, no outbox row, no cache entry of the answer itself (DP-09, BR12).
11. rwb-integration: where no plan is returned for the case, answers 200 with `live` true and the plan fields absent, because ACE answered and the answer is that there is no plan; the substitution of the stored status, its date and MSG-P2-008 is rwb-case's (RWB-P3-E2002-APP).
12. rwb-integration: where ACE does not answer inside the budget, or the breaker is open, answers 503 with MSG-GEN-006 naming "ACE common module"; the caller keeps every stored status and retries in its next run.
13. gateway-bff: for the case record, calls this operation and the rwb-case stored answer in parallel, one hop each, and merges them: the live answer wins when `live` is true, the stored answer of rwb-case with MSG-P2-008 and its date is shown when this operation answers 503 or the flag is off (DP-19).
14. rwb-integration: records on every answer the case reference, the plan reference, the status code, the `live` flag, the batch count and the duration, never an account number and never a personal value (BR16).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | ACE returns no status for a plan the case holds | This operation answers `live` true with no plan; the case keeps its last known status and date through rwb-case; a break with product "DP04" lists the plan for the ACE team from the DailyCaseRun run summary until the rwb-source-data break operation is published | MSG-P2-008 (shown by rwb-case) | AC3 |
| X2 | The ACE common module is unavailable or does not answer in 2 seconds | The answer is 503 with MSG-GEN-006 naming "ACE common module"; the case side keeps every stored status and retries in its next run; the screen shows the stored status | MSG-GEN-006 | AC4 |
| X3 | ACE returns a status code not in the plan status list | The code is answered unchanged and never interpreted; it is counted and alerted; the case side refuses to store it and lists the break with check "Lists of values" in the DailyCaseRun run summary until the rwb-source-data break operation is published | None | AC5 |
| X4 | The daily step runs twice for the same day | This operation is stateless and answers the same values; no status is written twice and no event is raised twice, because neither the write nor the event is here | None | AC6 |
| X5 | The decision log write fails during the broken plan move | Nothing changes here: this operation writes no record and takes no decision; the move, the rollback and the incident are rwb-case's | MSG-P7-003 (raised by rwb-case) | AC7 |
| X6 | A user calls the operation for a case outside their scope | Refused with 404 before any ACE call; nothing is returned and nothing is written | MSG-P4-003 | AC8 |
| X7 | A role without the Case record R right calls the operation | Refused with 403 before any ACE call; nothing changes | MSG-P4-002 | AC10, TC-E2-002-10 |
| X8 | No RESTRUCTURE version is IN_FORCE on the business date | Nothing changes here, because the read never evaluates a package; the refusal, the exception queue and MSG-P3-027 are the case side's | MSG-P3-027 (raised by rwb-case) | AC9 |
| X9 | The case reference is unknown, or the case exists but holds no account | Refused with 404 for an unknown case; a case with no account answers 200 with `live` false, the plan fields absent and no ACE call, because there is nothing to ask ACE about | MSG-P4-003 (unknown case only) | AC1, AC3 |
| X10 | The reference-data, parameter or authorise call does not answer inside the budget | The answer is 503 with MSG-GEN-006 naming the source; no ACE call is made, because a status that cannot be validated is not read | MSG-GEN-006 | AC1 |
| X11 | The flag `rwb.integration.ace-plan-status` is off | The answer is 200 with `live` false and no ACE call, so the caller uses the stored value; nothing is read from ACE and nothing is written | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the contract baseline of RWB-P2-E2002-CON and the integration base of RWB-P2-E2001-APP; the case, reference-data, parameter, authorise and ACE answers come from their fakes |
| Negotiable | The batch size, the timeout, the status list, the flag and the breaker thresholds are rows, parameters and values; the story fixes only the behaviour |
| Valuable | A live plan status is available to the case side within a bounded budget, and a read can never write a plan status |
| Estimable | One operation, one service class, one ACE client, three contract clients, one access check and one status validation |
| Small | Fits one sprint with its tests |
| Testable | Each of the nine legacy criteria is one automated test at the level this slice can prove it; every cross-service answer is stubbed |

### 7. Acceptance criteria

```gherkin
Feature: ACE plan status on the case

  Background:
    Given case "RW-2026-000310" is open with synthetic account "A-0310"
    Given the ACE common module stub holds plan "TDR-SYN-0310" for "A-0310"
    Given package "RESTRUCTURE" version "RES-2026.12" is in force with rows R-RES-29, R-RES-30, R-RES-31 and R-LIT-02

  Scenario: AC1 Plan status on the case (legacy RWB-E2-002 AC1)
    Given plan "TDR-SYN-0310" has status "APPROVED" in ACE with status date 2026-12-10
    Given the rwb-case contract mock returns case "RW-2026-000310" with account "A-0310"
    Given the rwb-case contract mock returns the plan status list LOV-PLAN-STATUS with CREATED, APPROVED, BOOKED and BROKEN
    Given the rwb-access contract mock returns Case record R for the caller with the case in scope
    Given the rwb-decision contract mock returns the evaluation of package "RESTRUCTURE" version "RES-2026.12" with plan_status "APPROVED" and no R-LIT-02 move
    When the case record view loads on 2026-12-11
    Then the case shows plan "TDR-SYN-0310" with status "Approved" and date 2026-12-10
    Then RuleEvaluator.evaluate("RESTRUCTURE", facts, 2026-12-11) reads plan_status "APPROVED" for the case
    Then rule R-LIT-02 does not fire for the case because plan_status is not broken

  Scenario: AC2 Broken plan (legacy RWB-E2-002 AC2)
    Given the case is in route state "PLAN_CURE_PERIOD" with break count 0
    Given plan "TDR-SYN-0310" has status "BROKEN" in ACE with status date 2026-12-14
    Given the rwb-case contract mock returns case "RW-2026-000310" in route state "PLAN_CURE_PERIOD" with break count 0 and account "A-0310"
    Given the rwb-case contract mock returns the plan status list LOV-PLAN-STATUS with CREATED, APPROVED, BOOKED and BROKEN
    Given the rwb-case contract mock returns the moves R-RES-29 and R-RES-30 with timer_spec "5 working days" and one decision entry per move
    When the daily case update runs on 2026-12-15
    Then the case plan status is "BROKEN" with date 2026-12-14
    Then the route state moves to "PLAN_BROKEN" by R-RES-29 and then to "BACK_TO_ROUTE_DECISION" by R-RES-30
    Then the case is in the case owner's queue with a task due in 5 working days, from timer_spec "5 working days" of row R-RES-30 of version "RES-2026.12"
    Then the system writes a decision log entry for each move with the rule ID and the package version "RES-2026.12"

  Scenario: AC3 Status not available (legacy RWB-E2-002 AC3)
    Given the case holds plan "TDR-SYN-0310" with status "BOOKED" and date 2026-12-01
    Given ACE returns no status for "TDR-SYN-0310"
    Given the rwb-case contract mock returns the case holding plan "TDR-SYN-0310" with status "BOOKED" and plan_status_as_of 2026-12-01
    Given the rwb-case contract mock returns the plan status list LOV-PLAN-STATUS with CREATED, APPROVED, BOOKED and BROKEN
    When the daily case update runs on 2026-12-15
    Then the case keeps status "BOOKED" with date 2026-12-01
    Then the case record view shows message MSG-P2-008 with the date 2026-12-01
    Then a break with product "DP04" lists plan "TDR-SYN-0310" for the ACE team

  Scenario: AC4 ACE unavailable (legacy RWB-E2-002 AC4)
    Given the ACE common module does not answer within 2 seconds
    Given the rwb-case contract mock returns the case with its stored status and records that the daily step writes nothing
    Given the rwb-case contract mock returns rwb.ace.plan.batch-size 500 and rwb.ace.plan.timeout-ms 2000
    When the daily case update runs on 2026-12-16
    Then the system changes no plan status
    Then the run summary carries message MSG-GEN-006 with system "ACE common module"
    Then the next run retries every case

  Scenario: AC5 Unknown status code (legacy RWB-E2-002 AC5)
    Given ACE returns status "SUSPENDED" for plan "TDR-SYN-0310"
    Given the rwb-case contract mock returns the plan status list LOV-PLAN-STATUS without "SUSPENDED"
    Given the rwb-case contract mock returns the case holding plan "TDR-SYN-0310" with status "BOOKED" and date 2026-12-01
    When the daily case update runs
    Then the stored status does not change
    Then a break with check "Lists of values" names the code "SUSPENDED"

  Scenario: AC6 Daily step run twice (legacy RWB-E2-002 AC6)
    Given the daily case update on 2026-12-15 stored status "BROKEN" for plan "TDR-SYN-0310"
    Given the rwb-case contract mock returns the case whose stored status and date equal the ACE answer, and records that no second write and no second event are asked for
    Given the rwb-case contract mock returns the plan status list LOV-PLAN-STATUS with CREATED, APPROVED, BOOKED and BROKEN
    When the step is rerun on 2026-12-15
    Then the system writes no status row
    Then the system raises no second CURE_PERIOD_EXPIRED event for the case

  Scenario: AC7 Decision log write fails on a broken plan (legacy RWB-E2-002 AC7)
    Given the decision log store is unavailable
    Given the rwb-case contract mock returns case "RW-2026-000310" in route state "PLAN_CURE_PERIOD" and holds the decision record store unavailable
    When the daily case update finds plan "TDR-SYN-0310" broken
    Then the route state stays "PLAN_CURE_PERIOD"
    Then the system raises an incident with message MSG-P7-003
    Then the system raises the event again in the next run

  Scenario: AC8 Case outside the scope (legacy RWB-E2-002 AC8)
    Given a case owner whose scope is "Own" and case "RW-2026-000310" is owned by another person
    Given the rwb-access contract mock returns Case record R for the case owner and no Case record right for RW-REFADM
    Given the rwb-case contract mock returns case "RW-2026-000310" as outside the caller's scope
    When the case owner calls GET /cases/{caseId}/plan-status for it
    Then the response is 404 with message MSG-P4-003

  Scenario: AC9 No RESTRUCTURE version in force (legacy RWB-E2-002 AC9)
    Given no RESTRUCTURE version is IN_FORCE on 2026-12-15
    Given the rwb-case contract mock returns case "RW-2026-000310" in route state "PLAN_CURE_PERIOD" with break count 0
    Given the rwb-decision contract mock returns no RESTRUCTURE version in force on 2026-12-15
    When the daily case update finds plan "TDR-SYN-0310" broken on that date
    Then NoPackageInForce is thrown with MSG-P3-027 for package "RESTRUCTURE"
    Then no decision log entry is written and the route state stays "PLAN_CURE_PERIOD"
    Then the case goes to the exception queue for role "RW-TEAMMGR" with the gap

  Scenario: AC10 Role without Case record R covers exception X7 (new, D-RCV-60)
    Given the caller holds the role "RW-REFADM" with no Case record right on case "RW-2026-000310"
    Given the rwb-access contract mock returns no Case record right for the caller on the case
    When the caller calls GET /cases/{caseId}/plan-status for "RW-2026-000310"
    Then the response is 403 with message MSG-P4-002
    Then no ACE call is made and nothing changes

  Scenario: AC11 Read guardrails (new, D-RCV-60)
    Given the rwb-integration store and task queue are in place with no grant on recovery
    When the caller reads GET /cases/{caseId}/plan-status for "RW-2026-000310" and the read is repeated
    Then no table row, no outbox row, no decision record and no cached answer is written
    Then the operation is served on /api/recovery/integration/v1 on the rwb-integration task queue with no Schedule or workflow
    Then rwb_integration holds no grant on recovery and no foreign key into another schema
    Then the status list, batch size, timeout, flag and breaker thresholds are read as rows and parameters
    Then no account number or personal data appears in an event, log line or test report
    Then the answer reports live true only for a value read from ACE and never returns a stored value
    Then the plan section is reached only through the gateway-bff composite route

  Scenario: AC12 Caller not authenticated (new, D-RCV-60)
    Given the caller holds no valid session
    When the caller calls GET /cases/{caseId}/plan-status for "RW-2026-000310"
    Then the response is 401
    Then no ACE call is made and nothing changes
```

The nine criteria are copied unchanged from the legacy story, values included, with the cross-service answers replaced by a contract-mock Given. Each line of the legacy background and of each criterion is kept; no value is changed and no line is dropped. AC10 to AC12 are this story's own criteria (exception X7, rules BR12 to BR18 and the 401 answer) and have no legacy counterpart.

**What is proved here, and what is proved at the other owners.** The split puts one journey across five services, so each criterion is proved at the level the owning service can prove it, and this story runs the nine against its own operation with the contract fakes:

- **AC1 is proved here at Component level for the read half**: the case's accounts are resolved, ACE is called in batches of 500 with the 2,000 ms budget, "APPROVED" is validated against LOV-PLAN-STATUS, the answer is `planRef` "TDR-SYN-0310", `accountNo` "A-0310", `status` "APPROVED", `statusDate` 2026-12-10 and `live` true, and nothing is written. The panel value and the evaluation with its version are proved in RWB-P3-E2002-APP and RWB-P7-E2002-APP.
- **AC2 is proved here only for the answer that starts the move**: "BROKEN" with status date 2026-12-14 is answered live with its plan reference. The stored status, the two route moves, the queue, the task, the timer, the decision entries and the retry are rwb-case's and are proved in RWB-P3-E2002-APP, and the package version is rwb-decision's.
- **AC3 is proved here for the no-plan answer**: with the ACE stub returning no status, the answer is `live` true with no plan and no error, because ACE answered and the answer is that there is no plan. The stored "BOOKED" with 2026-12-01, MSG-P2-008 and the product "DP04" break are rwb-case's and are proved there; this story guarantees only that it never invents a plan, never returns a stale value and never errors on an absent one.
- **AC4 is proved here in full at Component level**: a 3-second ACE answer is cut at 2,000 ms, the answer is 503 with MSG-GEN-006 naming "ACE common module", no case answer changes and no write is attempted; the retry of the next run is the caller's.
- **AC5 is proved here for the validation half**: "SUSPENDED" is answered unchanged, is never mapped to a known status and is counted as unknown; the refusal to store it, the unchanged stored value and the "Lists of values" break are rwb-case's and are proved there.
- **AC6 and AC7 are proved here as the absence of a second effect**: the operation is stateless and idempotent by its input, so a repeat answers the same values and writes nothing, and a decision-record failure cannot leave a partial write here because there is no write. The stored-value idempotency and the decision record are rwb-case's.
- **AC8 and TC-E2-002-10 are proved here at Component level on this operation**: 404 with MSG-P4-003 for a case outside the scope and 403 with MSG-P4-002 for a role without Case record R, both before any ACE call. The role and scope data are rwb-access's (RWB-P4-E2002-APP).
- **AC9 is proved here as the absence of a package dependency**: the operation answers the plan whether or not a package version is in force, because a read never evaluates a package. The refusal, the exception queue and the message are rwb-case's and rwb-decision's.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The plan status is read from the ACE common module through its published interface `RestructurePlanQuery`, never from ACE tables and never from a `recovery.v_ace_*` view | INT-34; DL14 (ASM-0189, ASM-5687); ADR-010; DP-05 |
| BR2 | The account number is the join between the case and the ACE plan | DL21 (answer A from Business Requirements Epic 1 v5) |
| BR3 | Plan status values: CREATED, APPROVED, BOOKED, BROKEN, read from LOV-PLAN-STATUS with the version in force; any other code is held as an exception and never interpreted | LOV-PLAN-STATUS (TSD P3 v3 T3.2); legacy BR3; DP-07 |
| BR4 | A plan marked broken while the case is in the cure period marks the plan broken and records the break | R-RES-29, R-RES-30 |
| BR5 | A second break bars a further restructure | R-RES-31; parameter restructure.max_breaks |
| BR6 | A case on the litigation route with a broken plan returns to the legal route | R-LIT-02 |
| BR7 | When ACE returns no status, the last known status and its date stay on the case | FEAT-CHO-02; VR-P2-001-1 |
| BR8 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39 |
| BR9 | A repeat of the same status and date raises no event | R-UNI-40 |
| BR10 | R-RES-29, R-RES-30, R-RES-31 and R-LIT-02 are rows of package RESTRUCTURE, evaluated by the case side with the version in force; this service neither evaluates nor names them | D-RCV-36 T5, T6, T7; DP-04 |
| BR11 | No RESTRUCTURE version in force is a refusal (`NoPackageInForce`), never a default move | R-UNI-41; D-RCV-36 T7 |
| BR12 | The read writes nothing: no table row, no outbox row, no decision record, no cache of the answer; a screen refresh and a rerun have no effect on any stored value | Legacy guardrail "a read of the plan status writes nothing"; DP-01 |
| BR13 | `rwb_integration` holds no grant on `recovery` and no foreign key into any other schema; the case is reached by reference through its owner and the plan through the ACE interface | ADR-010; DP-01; Arch v5 slide 41 |
| BR14 | One base and one queue: the operation is served on `/api/recovery/integration/v1` and the service runs on the task queue of `rwb-integration`; no Schedule and no workflow is created for this key | DP-13; DP-10; Arch v5 slides 41 and 44 |
| BR15 | No business value in code: the status list, the batch size, the timeout, the flag and the breaker thresholds are rows, parameters and values, read through their owners | FSD P2 Integration v3 BR-P2-007; Template and Rules §R7.2 s17 |
| BR16 | No personal data and no account number in an event, an activity input, a log line or a test report: the case reference, the plan reference, the status code, the flag and the counters only | Arch v5 slide 42; Template and Rules §R7.2 s17 |
| BR17 | The status answer is either live from ACE now or absent; this service never answers a stored value and never reports `live` true for a value it did not read | Legacy plan-status resource; RWB-P3-E2002-APP |
| BR18 | The case record reads the plan section only through the gateway-bff composite route, never by the browser calling this service directly | DP-19 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Live answered | ACE answers a plan in LOV-PLAN-STATUS | The account of the case has a plan | Live answered (no change; nothing written) |
| Live answered | ACE answers an unknown code | The code is not in LOV-PLAN-STATUS | Live answered, unknown code, counted and never interpreted |
| Live answered | ACE answers no plan | The account of the case has no plan | No plan (200, `live` true, plan fields absent) |
| Any | The case holds no account | There is nothing to ask ACE about | No plan (200, `live` false, plan fields absent, no ACE call) |
| Live answered | ACE does not answer inside the budget | Timeout, connection error or open breaker | Unavailable (503, MSG-GEN-006) |
| Unavailable | The next call | ACE answers inside the budget | Live answered |
| Any | The caller holds no Case record R | The authorise contract refuses | Refused (403, MSG-P4-002) |
| Any | The case is outside the caller's scope, or unknown | The scope check or the case read refuses | Refused (404, MSG-P4-003) |
| Any | The flag is off | `rwb.integration.ace-plan-status` is off | Stored only (200, `live` false, no ACE call) |

These are answer states of one operation, not case states: the case status stays "In progress" and the route state does not move here. The route states of the legacy story — `PLAN_CURE_PERIOD` to `PLAN_BROKEN` to `BACK_TO_ROUTE_DECISION`, and `LIT_ROUTE_APPROVED` to `NOTICE_GENERATED` — are `recovery_case.route_state` writes of rwb-case, caused by the evaluation of package RESTRUCTURE and proved in RWB-P3-E2002-APP.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-integration service identity (the rwb-integration login, DP-02) | Calls the ACE common module; reads the case, the reference data and the parameters; checks the right and the scope; answers the plan status; writes nothing |
| RW-CASEOWN, case owner | Reads the plan status of cases in scope (Case record R) |
| RW-RESTRUCT, restructuring officer | Reads the plan status of cases in scope (Case record R) |
| RW-REFADM | Holds no Case record right; refused on the read operation with MSG-P4-002 |
| rwb-case, through its contract | Answers the case and its account numbers, and owns the stored plan status, the route state, the task and the timer |
| rwb-access, through its contract | Answers the Case record right and the scope |
| rwb-case reference data and parameters, through their contracts | Answer LOV-PLAN-STATUS and the two settings, with their versions in force |
| The ACE common module | Answers `statusFor` for the account numbers asked, within the 2,000 ms budget |
| gateway-bff | Composes the case record plan section from this operation and the rwb-case stored answer |

The service runs as the rwb-integration login (DP-02). The login name is Not specified in the source documents (GAP-0654; ASM-1099).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case, through the rwb-case contract | id (the path reference) | Read |
| DF-CAS-026 | case_account, through the rwb-case contract | account_key (the join key of DL21) | Read |
| DF-CAS-009, DF-CAS-010 | recovery_case, through the rwb-case contract | owner_user_id, queue_id (the scope facts of the authorise answer) | Read |
| DF-REF-159 to DF-REF-184 | reference_row, through the rwb-case reference-data contract | LOV-PLAN-STATUS with its version in force | Read |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value, through the rwb-case parameters contract | `rwb.ace.plan.batch-size`, `rwb.ace.plan.timeout-ms` and their versions in force | Read |
| Not specified in the source documents (DOR-RWB-P2-E2002-APP-7) | The ACE common module interface | planRef, accountNo, status, statusDate of the plan of the case | Read, from `RestructurePlanQuery.statusFor`; not a table and not a view |
| None | Any table of `rwb_integration` | No field | Write none |

The plan fields `planRef`, `status`, `statusDate` and the flag `live` are read from the ACE common module interface and are not read from any table; the account number used for the join is `case_account.account_key` read through the rwb-case contract. The plan fields of the case record (DF-CAS-046 `plan_ref`, DF-CAS-047 `plan_status`, DF-CAS-048 `plan_status_as_of`) are written only by rwb-case in RWB-P3-E2002-APP and are not written, cached or copied here. No ACE row is copied into `rwb_integration`, and no foreign key crosses a schema (DP-01).

The plan reference, the status and the status date come from the ACE interface and carry no field ID in the Logical Data Model, because the interface is a module interface and not a view (INT-34; ADR-010). The element names of the interface answer are the ones the legacy story publishes: planRef, accountNo, status, statusDate. The types, lengths and null rules of the remaining interface elements are Not specified in the source documents (GAP-0654; ASM-1102).

### 12. Contract

Contract version: 5.0.0 (`info.version` of rwb-integration.yaml, Recovery Workbench API Specification v5). The operation is on the path `/api/recovery/integration/v1`.

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}/plan-status` | The live ACE restructure plan status of the case: `planRef`, `accountNo`, `status`, `statusDate`, `live` (true when read from ACE now) and `messageCode` | Case record R, scope applied | Not applicable: the call writes nothing and answers the same values for the same ACE state |

Response: the legacy PlanStatus shape with `accountNo` added, because the ACE answer carries the account and the case side joins on it. Errors: 401 no session (MSG-P4-001); 403 no Case record R (MSG-P4-002); 404 unknown case or out of scope (MSG-P4-003); 503 the ACE common module, the reference data, the parameters or the authorise contract did not answer inside the budget (MSG-GEN-006). `live` is true on every 200 answer that read ACE, because such an answer means ACE answered, and false on the flag-off answer, which carries no plan because no call was made; `live` false with MSG-P2-008 is otherwise the stored answer of rwb-case and reaches the merged screen from there. `messageCode` is empty on every answer of this service, because this service holds no stored value to date; MSG-P2-008 is set by rwb-case on its stored answer (GAP-0654; ASM-1101).

The operation name, path and base are the ones the Ownership Map and TSD P2 v3 API-P2-010 fix, moved to the integration base under DP-13. The JSON field names are the legacy PlanStatus names; the `accountNo` field and the `messageCode` rule are the two places where this story fixes a shape the API Specification leaves open (GAP-0654; ASM-1101).

#### 12.2 REST operations consumed

One hop per call, no chaining; 2 s timeout and a breaker per downstream (DP-11).

| Method | Path or operation | Owner | Used for |
|---|---|---|---|
| GET | the case read of the rwb-case contract, by case reference | P3 rwb-case | The account numbers of the case, the owner and the queue, and the scope facts |
| GET | the reference-data read of the rwb-case contract (RWB-P3-E1043-CON) | P3 rwb-case | LOV-PLAN-STATUS with the version in force |
| GET | the parameters read of the rwb-case contract (RWB-P3-E1042-CON) | P3 rwb-case | `rwb.ace.plan.batch-size` and `rwb.ace.plan.timeout-ms` with the version in force |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Case record right and the case scope, cached per session |
| Call | `RestructurePlanQuery.statusFor(List<String> accountNos)` of the ACE common module (INT-34) | ACE team, the ACE common module | The plans of the account numbers, in batches of 500 within a 2,000 ms budget |

The three rwb-case reads and the authorise call are the published contracts of the case and access services, and this story builds against their fakes; RWB-P3-E1042-CON and RWB-P3-E1043-CON are the two of the contract-dependency row this story uses, and RWB-P3-E2042-CON is the third of that row and is consumed by the case side, not here. The case read and the authorise call are the case baseline and the platform guard. The paths of the case read and of the authorise call, and the element names of the reference-data and parameter answers, are Not specified in the source documents (GAP-0654; ASM-1103): the case read is taken from the case contract baseline, the authorise path from the access contract, and the two reference shapes from the P3 contract baseline when it is published.

The ACE interface is a published module interface and not a view: it is not on a `/api/recovery/...` base, it is not reached through gateway-bff, and `rwb_integration` holds no grant on `recovery` (INT-34; ADR-010; DP-05).

#### 12.3 Events published

None. This story publishes no event type and writes no outbox row: a read takes no decision and changes no state. `rwb.integration.events.v1` carries FileDelivered and FileFailed, which belong to the outbound-file stories of this service, and `rwb.decision-record.v1` carries DecisionRecorded from the services that take the decision — here, rwb-case on each route move (DP-03, DP-09).

#### 12.4 Events consumed

None. The operation is called on the request path by rwb-case's activity and by gateway-bff; the service subscribes to no topic for this story, keeps no projection and holds no inbox row.

#### 12.5 Workflows and activities

None owned by this story. The daily step is `PlanStatusStep` of DailyCaseRun in rwb-case, and its `readPlanStatus` activity is the caller of this operation on the task queue `rwb-case` (RWB-P3-E2002-APP). This service registers no workflow and no activity for this key: the batching, the 2,000 ms budget and the breaker run inside the request on the service's own worker, which RWB-P2-E2002-OPS deploys. The integration harness lists a "plan-status step" on `rwb-integration`; that row conflicts with the sibling story and with the job map, where JOB-02 is rwb-case's, and the conflict is carried in the gap row rather than resolved by creating a second step (GAP-0654).

#### 12.6 Schedules

None. No Schedule is created by this story or by this key: the legacy plan-status step of JOB-02 is a step of the event-started DailyCaseRun in rwb-case (DP-10), and this service answers a synchronous read. A Schedule here would be a second daily run over the same cases, which the job map does not allow (Arch v5 slide 44).

#### 12.7 Tables owned

| Table | Schema | Owner | Use in this story |
|---|---|---|---|
| interface_config | rwb_integration | P2 (Ownership Map; Arch v5 slide 41) | Not used: the ACE endpoint is configuration of the deployment, not an interface row |
| outbound_item | rwb_integration | P2 (Ownership Map; Arch v5 slide 41) | Not used: this story builds and sends no file |
| job_catalog | rwb_integration | P2 (Ownership Map; TSD P2 v3 T3.1) | Not used: no job is catalogued for this key, because no P2 Schedule exists |
| outbox_event, processed_event, outbox_delivery, idempotency_key | rwb_integration | PLT library, created in `rwb_integration` (DP-09) | Present from the service baseline and unused: a read writes no outbox row and consumes no event |

This story writes no table and adds no column; it adds no migration (DP-15). `rwb_integration` reads no table of another service, holds no foreign key across services and holds no grant on `recovery` (DP-01, BR13).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case WireMock | The P3 case contract | Case "RW-2026-000310" with account "A-0310" in PLAN_CURE_PERIOD with break count 0, the case of AC8 owned by another person, an unknown case (404) and a case with no account |
| rwb-case reference-data WireMock | The P3 reference-data contract | LOV-PLAN-STATUS with CREATED, APPROVED, BOOKED and BROKEN and its version, a version without "SUSPENDED" for AC5, and one answer beyond 2 s |
| rwb-case parameters WireMock | The P3 parameters contract | `rwb.ace.plan.batch-size` 500 and `rwb.ace.plan.timeout-ms` 2000 with their versions, and one answer beyond 2 s |
| rwb-access WireMock | The P4 contract | Case record R granted in scope, refused for RW-REFADM, and a case outside an Own scope (404) |
| ACE common module stub behind this service | `RestructurePlanQuery.statusFor` | "APPROVED" with 2026-12-10, "BROKEN" with 2026-12-14, no plan for "A-0310", a 3-second answer, "SUSPENDED", and an answer for more than 500 accounts that forces two batches |
| rwb-case and rwb-decision WireMock | The P3 and P7 contracts | The evaluation answer of AC1 and the move answers of AC2, so the criteria that end in the case can be driven against the fakes; the parts that are not this slice's are asserted as calls, not as writes |
| gateway-bff composite route stub | The edge route of RWB-PLT-N001-CON | The merged plan section of AC1 and the fallback to the stored answer of rwb-case of AC3 |

Every fake is generated from the owning service's published OpenAPI document where one exists, and the drift test fails when a fake answers a shape or an error this story does not declare.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | The plan-status read provided; the case read, the reference-data read, the parameters read and the authorise call consumed; one hop, 2 s timeout each, GET retried once with jitter |
| Kafka | None published, none consumed | A read publishes no event and subscribes to none (DP-09) |
| Temporal | None owned | No workflow, no activity and no Schedule in this service for this key; the daily step and its activity are rwb-case's (DP-10) |
| File | None | This story reads and writes no file; the ACE common module is a published module interface (INT-34) and is counted in the consumed table, not as a file exchange |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.integration`, module `planstatus`, Java package `th.co.scb.ace.workbench.recovery.integration.planstatus`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; no record is written by a read | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit and packages from rwb-decision; this slice evaluates no package, so the kit is only part of the service image | H RWB-PLT-E1072-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The ACE common module's published interface (INT-34) with a 2 s budget and batching; no view and no grant on `recovery` | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents; no event is published or consumed here | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit; the daily step is rwb-case's, so no Schedule is created here | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/integration/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema; no migration is added by this story | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

RWB-P3-E1042-CON and RWB-P3-E1043-CON are another service's contract stories, so they sit in the contract-dependency row; RWB-P3-E2042-CON is the third contract of the row and this story consumes none of it, because the read evaluates no package. The H dependencies this table adds are held by the platform contract stories and are not repeated in the metadata rows. DP-05 resolves to the published interface with its batch and its budget (ASM-1100), DP-06 to the two parameter rows read through their owner (ASM-1104), and DP-10 to no Schedule at all, because the daily step is rwb-case's.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PlanStatusController | Controller | `GET /cases/{caseId}/plan-status`; request and path validation; the problem responses; the flag gate; the read-only rule |
| PlanStatusService | Service | Resolves the case and its accounts, drives the access check, the settings and the status list, calls the client, validates the status and composes the answer |
| AcePlanClient | Client | Wraps `RestructurePlanQuery.statusFor` with batches of 500, the 2,000 ms budget per call, the breaker per downstream and one retry of a read with jitter |
| PlanStatusValidator | Service | Validates the returned code against LOV-PLAN-STATUS; never coerces an unknown code; counts it for the unknown-status series |
| CaseClient | Client | The case read by reference: accounts, owner, queue and the scope facts |
| AccessCheckClient | Client | The authorise contract, cached per session, before any ACE call |
| ReferenceDataClient | Client | LOV-PLAN-STATUS with the version in force, cached with its version (DP-07) |
| ParameterClient | Client | `rwb.ace.plan.batch-size` and `rwb.ace.plan.timeout-ms` with the version in force (DP-06) |
| AcePlanStatusMetrics | Component | The counters and timers of the answer: batch count, duration, live answers, no-plan answers, unknown codes and unavailable answers |

**Database and migrations**

- None. This story adds no table, no column and no index, and therefore adds no migration to the `rwb_integration` Flyway sequence (DP-15). The outbox, inbox, delivery and idempotency objects the library needs exist from the service baseline of RWB-P2-E1007-APP and the DB story of the service.
- No cache of the answer is stored: the case, the status list, the settings and the plan are read per request or held in memory with the version of the reference data they came from, and an eviction on a version change is what makes a reload safe (BR12).

**Configuration and reference data**

- LOV-PLAN-STATUS with CREATED, APPROVED, BOOKED and BROKEN (RW-COE), read through the reference-data contract of rwb-case with the version in force (DP-07).
- `rwb.ace.plan.batch-size` = 500 and `rwb.ace.plan.timeout-ms` = 2000 (assumed; DL11), read through the parameters contract of rwb-case as rows, never as code (DP-06).
- The ACE endpoint of the environment, the client certificate and the breaker thresholds are deployment values of RWB-P2-E2002-OPS; the endpoint is not an `interface_config` row, because the interface is called by this service and not run as an outbound file.
- The feature flag `rwb.integration.ace-plan-status` is registered in the platform flag library (R-PREC default ruling); off means no ACE call and a 200 answer with `live` false.

**Build steps**

1. PlanStatusController with the path, the problem responses and the read-only rule; AC1 and AC8 at Component level.
2. CaseClient and the account resolution by case reference; AC1, AC3 and AC8.
3. AccessCheckClient and the guard on the operation, before any ACE call; AC8, TC-E2-002-10.
4. ParameterClient and ReferenceDataClient with the versions in force and the cache eviction; AC1, AC4, AC5.
5. AcePlanClient over the `RestructurePlanQuery` stub, with batches of 500, the 2,000 ms budget, the breaker and the retry; AC1, AC2, AC4.
6. PlanStatusValidator and the unknown-code path, with its counter and no coercion; AC5.
7. The no-plan answer, the unavailable answer and the flag-off answer; AC3, AC4, AC1.
8. AcePlanStatusMetrics and the five series the deployment publishes; AC4, AC5.
9. The contract-fake run of every cross-service answer in isolation, so the story builds before rwb-case, rwb-access and ACE are reachable; all nine criteria.
10. The composite-route stub run, so the case record plan section is shown reaching both providers; AC1, AC3.

**Done when.** The tests in section 16 pass, every 200 answer that read ACE has `live` true and the flag-off answer has `live` false with no plan, every 503 names its source and message, an unknown code is answered unchanged and counted, no statement of the story writes a row anywhere, the two reference reads carry the version in force, and the contract tests of RWB-P2-E2002-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-008 | Plan status shown from the stored value | The ACE plan status is from {date}. Today's status was not returned. |
| MSG-GEN-006 | The ACE common module, the reference data, the parameters or the authorise contract did not answer | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | Decision log write failed on a broken plan | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No RESTRUCTURE version is in force | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P4-003 | Case outside the caller's scope, or unknown | This case is not in your scope. |
| MSG-P4-002 | A role without the Case record right | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | No session, or the person holds no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |

This story returns MSG-GEN-006, MSG-P4-001, MSG-P4-002 and MSG-P4-003 itself, and it reads and shows no other message. MSG-P2-008, MSG-P7-003 and MSG-P3-027 are the case side's and are listed here because the criteria of section 7 carry them: the stored-value message with its date is set by rwb-case on its stored answer, the decision-message by the case side when its record fails, and the package message by the evaluation. For MSG-GEN-006, {system} is "ACE common module" when the outside interface did not answer, and the name of the contract when a service did not. For MSG-P3-027, {check} is "no package in force" and {table} names the package code "RESTRUCTURE" and the business date only, never a case fact.

### 15. Screens and states

SCR-03 Case record, states loading and read only (empty, error and no access: Not specified in the source documents (CG-ALL-3066)): the plan status panel shows the plan reference, the status, the date and, when the answer is not live, MSG-P2-008 with the stored date. SCR-14 Treatment record, state broken, shows the broken plan once the case returns to the route decision. Empty, loading, error and no access: Not specified in the source documents (CG-ALL-3067).

This story supplies only the live half of the panel. The panel, its field-level behaviour and the stored fallback are the screen work of RWB-P3-E2002-APP, and the merge of the two answers is the composite route of RWB-PLT-N001-CON (DP-19). The route path, the merge order and the field-level masking are Not specified in the source documents (GAP-0654; ASM-1101).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-002-10 | Access, AC10 | Component | RW-REFADM (no Case record right) calls GET /cases/{caseId}/plan-status; refused with MSG-P4-002 |
| TC-E2-002-12 | Read | Component | A plan status read is repeated and the store, outbox, decision log and cache are checked: nothing is written (BR12) |
| TC-E2-002-13 | Data | Component | The grants and foreign keys of rwb_integration are checked: no grant on recovery and no foreign key into another schema (BR13) |
| TC-E2-002-14 | Platform | Component | The operation is served on /api/recovery/integration/v1 on the rwb-integration task queue and no Schedule or workflow is created (BR14) |
| TC-E2-002-15 | Config | Component | The status list, batch size, timeout, flag and breaker thresholds are read as rows and parameters and none is coded (BR15) |
| TC-E2-002-16 | Privacy | Component | An event, activity input, log line and test report carry no account number or personal data (BR16) |
| TC-E2-002-17 | Answer | Component | An answer never reports live true for a value not read from ACE and never returns a stored value (BR17) |
| TC-E2-002-18 | Route | Component | The case record reaches the plan section only through the gateway-bff composite route, not by the browser calling this service (BR18) |
| TC-E2-002-01 | AC1, BR1, BR2, BR6, BR10 | End to end | ACE stub plan TDR-SYN-0310 APPROVED |
| TC-E2-002-02 | AC2, BR4, BR5, BR10 | End to end | Case in PLAN_CURE_PERIOD; ACE plan BROKEN |
| TC-E2-002-03 | AC3, BR7 | End to end | ACE stub returns no plan |
| TC-E2-002-04 | AC4 | NFR | ACE stub delayed 3 seconds |
| TC-E2-002-05 | AC5, BR3 | End to end | ACE stub returns SUSPENDED |
| TC-E2-002-06 | AC6, BR9 | End to end | Step run twice on 2026-12-15 |
| TC-E2-002-07 | AC7, BR8 | End to end | Decision log store stopped |
| TC-E2-002-08 | AC8 | End to end | Case owner with scope Own and a case of another owner |
| TC-E2-002-09 | AC9, BR11 | End to end | No RESTRUCTURE version in force on 2026-12-15 |
| TC-E2-002-11 | Principle 5 | NFR | Decision log write forced to fail on the R-RES-29 move; route state unchanged |
| TC-E2-002-19 | AC11, BR12, BR13, BR14, BR15, BR16, BR17, BR18 | Component | Not specified in the source documents (NEWAC-RWB-P2-E2002-APP-AC11) |
| TC-E2-002-20 | AC12 | Component | Call with no valid session to GET /cases/{caseId}/plan-status; answered 401 |
| TC-E2-002-21 | Section 12 operations, events and activities | Component | Contract fake of RWB-P2-E2002-CON; each operation, event and activity of section 12 checked against it |
| TC-E2-002-22 | Section 12.7 tables (ASM-3438) | Component | Boundary value of each table of section 12.7; test data not specified in the source documents (DOR-RWB-P2-E2002-APP-12) |

The legacy levels map System to End to end, Access to Component and Resilience to NFR. The `-ITG` copy of each case is held by RWB-ITG-E2002-ITG and is not written here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

**How this story runs the eleven.** TC-E2-002-01, 02, 03, 05, 06, 07, 08, 09 and 11 are run here at Component level against the operation with the contract fakes, so the read half of each is proved on Day 1; the case-side, access-side and package-side halves are proved in RWB-P3-E2002-APP, RWB-P4-E2002-APP and RWB-P7-E2002-APP and as one journey in RWB-ITG-E2002-ITG. TC-E2-002-04 is run here as the NFR case that matters for this slice: a 3-second ACE answer is cut at the 2,000 ms budget, the answer is 503 with MSG-GEN-006 and no write is attempted. TC-E2-002-10 is run here at Component level on this endpoint.

### 17. Guardrails

- No business value in code: the four status codes, the batch size, the timeout, the flag and the breaker thresholds are reference rows, parameter rows and values files of their owners.
- No personal data in logs, tests, reports or traces: the case reference, the plan reference, the status code, the live flag and counters only; the account number is used for the join and is not logged, and no decoded payload is written.
- No ACE table and no ACE view: the plan comes from the published `RestructurePlanQuery` interface (INT-34), `rwb_integration` holds no grant on `recovery`, and no statement of the story reads another service's table (DP-01, DP-05, BR13).
- A read writes nothing: no row, no outbox entry, no cache of the answer, no decision record; the operation is safe to call from a screen refresh and from a rerun (BR12).
- The status is never interpreted: a code outside LOV-PLAN-STATUS is answered unchanged and counted, never mapped, defaulted or stored (BR3, AC5).
- Every outside call is bounded: one hop per contract, 2 s, batches of 500, a breaker per downstream and one retry of a read with jitter.
- No Schedule and no workflow is created for this key: the daily step and its activity stay with rwb-case, and a second step over the same cases fails the review (DP-10, BR14).
- The plan section is reached only through the gateway-bff composite route, never by the browser calling this service (DP-19).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Plan status read from the ACE common module | Program 5.2; Epic 2 3.2 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39, R-UNI-40 | TC-E2-002-01, TC-E2-002-04, TC-E2-002-06, TC-E2-002-07, TC-E2-002-21, TC-E2-002-22 |
| REQ-CHO-002 | Plan status change visible on the case | Program 5.3; Epic 2 3.2 | FEAT-CHO-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-29, R-RES-30, R-RES-31, R-LIT-02 | TC-E2-002-02, TC-E2-002-03, TC-E2-002-05, TC-E2-002-08, TC-E2-002-09 |
| D-RCV-60 DP-05 | The ACE plan is read through the published module interface, not through a view, and `rwb_integration` holds no grant on `recovery` | Decision log, D-RCV-60; Template and Rules §R5.5; ADR-010 | FEAT-CHO-02 | 7.3 | R-UNI-39 | TC-E2-002-01, TC-E2-002-04 |
| D-RCV-60 DP-13 | The plan-status operation sits on the integration base `/api/recovery/integration/v1` | Template and Rules §R5.5; TSD P2 v3 API-P2-010; Ownership Map | FEAT-CHO-02 | 7.3 | None | TC-E2-002-01, TC-E2-002-08, TC-E2-002-10 |
| D-RCV-60 DP-19 | The case record plan section is read as one gateway answer through the composite route | Template and Rules §R5.5; Architecture v5 slides 10 and 12 | FEAT-CHO-02 | 7.3 | None | TC-E2-002-01, TC-E2-002-03 |

### 19. Out of scope

- The stored plan status, its date, the compare, the route state, the task, the durable timer and the local decision record: carried by RWB-P3-E2002-APP in `rwb_case`.
- The plan status panel on SCR-03 and the plan section of SCR-14, and their field-level behaviour: RWB-P3-E2002-APP.
- The evaluation of package RESTRUCTURE and the rule catalog rows: RWB-P7-E2002-APP; the packages and their versions: RWB-P3-E2042-APP.
- The roles, the scope and the rights data: RWB-P4-E2002-APP; this story reads the authorise answer only.
- The break on the data-quality console and the `reconciliation_result` table: rwb-source-data's, raised by the case side.
- Creating or changing a plan: ACE, under DL14.
- The treatment record and the plan timers: RWB-E2-004.
- Booking confirmation of the plan from the ALS load: RWB-E2-007.
- The deployment of this capability: the chart, the values, the flag, the dashboards, the alerts and the runbook are RWB-P2-E2002-OPS.
- The cross-service proof of the journey: RWB-ITG-E2002-ITG.
- The full restructure route in the Workbench: Epic 3.
