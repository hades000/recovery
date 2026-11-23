# RWB-P3-E2012-APP Manual transfer and reassignment screen with reason

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2012-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-AD |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P3-E2012-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1021-CON, RWB-P3-E2011-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | RWB-P3-E2012-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-012, FR-P3-013, FR-P3-017, FR-P3-018, FR-P3-019, FR-P3-021, FR-P3-030, FR-P3-031) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-012 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **a screen to transfer a case to another queue or reassign it to a person, with a reason code required and the TRANSFER rule package checked**, so that **a hand-off is one action with a record, not an email**.

Inside `rwb-case` this is the manual move of the case service:

- Service `rwb-case`, schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` with event names `rwb.case.<Event>.v1`, Temporal task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- The move is `POST /api/recovery/case/v1/cases/{caseId}/transfer`, one call per case, single or in a selection of up to 50 cases (DP-13).
- The rule decision comes from the TRANSFER package through the embedded Drools kit (DP-04), reached by the `EvaluateRules` activity of `ManualTransferWorkflow` on task queue `rwb-case`, so a replay reuses the recorded answer.
- The decision record is the local decision-record library of DP-03 in `rwb_case`, published on `rwb.decision-record.v1` (DP-03; ADR-022).
- The assignment and the queue rows are `rwb_case` rows (DP-01, DP-15): this story reads no table of rwb-access, rwb-deviation or rwb-decision.
- The case transfer event is `rwb.case.CaseTransferred.v1` on `rwb.case.events.v1` (DP-09, DP-14).
- The screen arrives through the gateway-bff composite route that serves SCR-05 (DP-19).

The legacy behaviour is unchanged: the same endpoint, request, response, errors and authorisation; the same reason list; the same TRANSFER package code; the same decision record content; the same thirteen acceptance criteria.

### 2. Business rationale

Today ownership changes are agreed by email, and audit found debtors who met the criteria were not transferred to the responsible unit (CTL-03). A manual move must carry a coded reason, respect the caseload cap and the transfer rules, keep the case's state and clocks, and leave a decision record. This story gives the team manager one screen for a single or a bulk move, and meets REQ-WKM-003, REQ-WKM-007 and REQ-WKM-008. The measure is that every manual move has an assignment record with a reason code, a decision record entry with a rule ID and a package version, and a rule ID on the screen when the move is refused.

The transfer rules are rows of the TRANSFER rule package, version "TRF-2026.12" here, and the manual move is evaluated by the same package, so the screen shows the rule ID that refused the move and the decision record names the rule and the package version that decided.

The realignment changes the mechanism, not the business rule. The in-process `RuleEvaluator` call of the monolith becomes the embedded Drools kit of DP-04, called only inside an activity so a workflow replay reuses the recorded result. The decision log write becomes the local decision-record library of DP-03, written in the same transaction as the assignment swap and published on `rwb.decision-record.v1`; the central ledger in rwb-decision collects it and never holds the only copy. The two cross-service answers the screen needs — the authorisation decision and the open deviations of the case — are one-hop calls to rwb-access and rwb-deviation with a 2 s budget and a breaker (DP-11, ADR-020), stubbed in development by the contract fakes of RWB-P3-E2012-CON, so neither service has to exist for this story to be built and tested. The screen itself is no longer an ace-web page: gateway-bff composes it from the case read and this operation (DP-19).

This is a `Split (rework)` of RWB-E2-012. The legacy story owned one screen and one endpoint; the contract, the deployment and the rule-engine side of the same key are separate stories, and the rule-driven triggers are already built in RWB-P3-E1021-APP. What remains here is the screen, its two states beyond the form, the bulk runner, and the manual operation path over the target mechanisms.

### 3. Preconditions

- RWB-P3-E2012-CON is published: the OpenAPI 3.1 document of `POST /cases/{caseId}/transfer` single and bulk, the `TransferRequest` and `Assignment` schemas, the reason list reference, the idempotency rule, the refusal codes and the three contract fakes.
- RWB-P3-E1021-CON is published: the transfer contract baseline that fixes the transfer operation and `CaseTransferred` for rwb-case; this story extends neither its request nor its response.
- RWB-P3-E2011-CON is published: the queue view contract whose selection feeds SCR-05, so the screen receives a set of case IDs and not a copied case list.
- RWB-PLT-E1072-CON is published: the embedded Drools kit with the `EvaluateRules` activity contract and `RuleResult(packageCode, packageVersion, ruleId, outputs)` (DP-04).
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), so the entry a move writes is hash-chained and published in the same transaction.
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data client library and the reference-data contract of rwb-case, so LOV-TRANSFER-REASON is read as data with its version (DP-07).
- RWB-PLT-TE006-CON is published: the outbox, inbox and idempotency library (DP-09), so the event and the key follow the platform envelope.
- RWB-PLT-E1071-CON is published: the workflow kit in namespace `rwb-recovery`, so `ManualTransferWorkflow` runs on task queue `rwb-case` (DP-10).
- RWB-PLT-E1047-CON and RWB-PLT-E1044-CON are published: the topic and event naming library, and the per-service Flyway sequence in schema `rwb_case` (DP-14, DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-05 (DP-19). Its path and merge order are owned by that platform contract; this story fixes only the answer rwb-case returns to it.
- Package TRANSFER version "TRF-2026.12" is in force on the business date, loaded, tested and approved through RWB-P3-E1073-APP; row "TRF-010" refuses a move while a deviation is open, and the allowing rule of a target queue is first-match in row order.
- LOV-TRANSFER-REASON is loaded with the agreed reason codes. The values in force are the intended set R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral and R06 Wrong queue; who may add or retire a code is Not specified in the source documents (GAP-0712; ASM-1259).
- The `assignment` columns `queue_id` (DF-WRK-039) and `transfer_reason_code` (DF-WRK-040) exist with the migration of RWB-P3-E1021-APP, and `queue.capacity_cap` (DF-WRK-007) and `queue_member.capacity` (DF-WRK-048) are populated for every queue this screen offers; this story adds no column.
- The person holds RW-TEAMMGR or RW-CAPACITY (Queue and allocation U) and the case is in their scope; rwb-access answers the authorisation check through its contract, cached per request. No approval level from the delegation of authority applies: a transfer moves work, not money.
- The login is the rwb-case login (DP-02): one login and one connection pool for the service, with grants on schema `rwb_case` only.
- No build dependency blocks: every H dependency is a contract, so the story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Team manager: opens SCR-05 Transfer case from SCR-03 Case record, or from a selection on SCR-07 Team queues served by the queue view of RWB-P3-E2011-APP, at the fixed business date 2026-12-15.
2. gateway-bff: checks the session and the coarse permission, then calls rwb-case `GET /api/recovery/case/v1/queues` for the target queue list and `GET /api/recovery/case/v1/queues/{queueId}/cases` for the selection counts, one hop each (DP-19). `POST /api/recovery/case/v1/queues/{queueId}/placements` is not used by this screen: it places a case from a model or an agent, and it belongs to RWB-P3-E2036.
3. rwb-case: authorises the form read through the rwb-access contract, `POST /api/recovery/access/v1/authorise`, right U on Queue and allocation, scope applied, cached for the request.
4. Screen: reads LOV-TRANSFER-REASON with `GET /api/recovery/case/v1/admin/lists/{listCode}` from the reference-data contract of rwb-case (RWB-P3-E1043-CON, DP-07) and renders one row per code with its label; the list is read at run time and never frozen into the client.
5. Team manager: chooses a target queue or a target owner, a reason code and an optional note, and confirms.
6. Front end: sends one `POST /api/recovery/case/v1/cases/{caseId}/transfer` per case with a new `Idempotency-Key` per case; a selection is sent case by case, in sequence, and never as one request.
7. rwb-case: authorises the call, then runs the pre-checks in this order — reason code present and in LOV-TRANSFER-REASON, case open and not under a legal hold, case in the caller's scope, the caller's queue and allocation right — and answers the first refusal with its message ID and changes nothing.
8. rwb-case: starts `ManualTransferWorkflow` on task queue `rwb-case` with the manual request, the caller and the idempotency key as its input; the workflow ID carries the case ID and the idempotency key, so a repeated key returns the running or finished execution instead of a second move.
9. `EvaluateRules` activity: the embedded Drools kit evaluates the TRANSFER package for the fact of the case, the target queue or owner, the reason code and the business date, and returns `RuleResult` with `packageCode`, `packageVersion` "TRF-2026.12", `ruleId` and the outputs. No version in force raises `NoPackageInForce`, which is non-retryable.
10. rwb-case: on a refusal result, stops before any write and answers MSG-P3-033 with `RuleResult.ruleId`; otherwise it reads the open deviations of the case once from rwb-deviation, one hop with a 2 s timeout and a breaker, and refuses a move that the deviation answer contradicts (BR10).
11. rwb-case: for a queue transfer, asks the assignment engine of RWB-P3-E1020-APP for the owner by the target queue's `assignment_method`; for a reassignment, checks the target owner is below `queue.capacity_cap` and, for reason R04, in the case's team. Every owner of the target queue at the cap is refused with the same message ID, naming each owner.
12. `RecordAndApply` activity: in one transaction in `rwb_case`, ends the current assignment, writes the new assignment with reason TRANSFER or MANUAL, the reason code, the queue and the rule ID, updates `recovery_case.queue_id`, `owner_user_id` and `team_code` under the version check, writes the decision record with the rule ID and the package version, and writes the outbox row for `rwb.case.CaseTransferred.v1`. A failed decision-record write leaves everything as it was.
13. rwb-case: answers 200 `Assignment` with `id`, `caseId`, `assigneeUserId`, `assignedAt`, `reason`, `ruleId`.
14. Screen: shows state Saved with MSG-GEN-005; for a selection, one result per case on its row and the count summary MSG-P3-035, with 8 of 10 when two of ten are refused.
15. The case keeps its status, route state, stage clock and timers; the route state and the prescription date are not recomputed by a move (BR6).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No reason code | Refused; nothing changes | MSG-P3-001 | AC4 |
| X2 | A TRANSFER package rule refuses the move | Refused; the refusing rule ID from `EvaluateRules` is shown | MSG-P3-033 | AC2 |
| X3 | The target owner is at the caseload cap | At cap warning; refused | MSG-P3-002 | AC5 |
| X4 | Every owner of the target queue is at the caseload cap | At cap warning naming every owner; refused | MSG-P3-002 | AC12 |
| X5 | Reason R04 and the target owner is outside the case's team | Refused naming R-UNI-18 | MSG-P3-033 | AC6 |
| X6 | The case is closed or under a legal hold | Refused | MSG-P3-005 | AC7 |
| X7 | Two transfers of one case at the same time | One succeeds; the other is refused | MSG-GEN-004 | AC8 |
| X8 | The same request is sent twice with the same Idempotency-Key | The first result is returned; no second record | None | AC9 |
| X9 | The decision record write fails | Nothing changes | MSG-P7-003 | AC10 |
| X10 | Some cases in a bulk move are refused | The others move; each refused case shows its message | MSG-P3-035 | AC11 |
| X11 | No TRANSFER package version is in force on the business date | Refused; nothing changes and no decision record is written | MSG-P3-027 | AC13 |

Three target-specific failures sit outside the criteria above and are covered by the guardrails of section 17 rather than by an owned criterion. A rwb-deviation read that does not answer inside 2 s makes the move a refusal that changes nothing, because the deviation answer is part of the decision and a move is never taken on an unread deviation; the caller may retry. A rwb-access answer that is unavailable refuses the call rather than granting it, so a failed authorisation never widens a right; the answer is a 503 with the platform problem envelope and never a 403 that would read as a missing role. A gateway-bff route that does not answer leaves the case untouched, because the operation is only reachable through the composite route and the queue and case reads it composes.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the TRANSFER package through the Drools kit, the assignment engine and the decision-record library of earlier stories; adds the screen, the manual operation path and the bulk runner |
| Negotiable | Reason codes, the selection limit and the rule rows are data; the checks, the message IDs and the event name are fixed |
| Valuable | Ends ownership changes by email; every move has a record and a refusal that names its cause |
| Estimable | One endpoint path extended to a manual workflow, one screen with four states, one bulk runner, four consumed contracts |
| Small | Fits one sprint with its tests |
| Testable | API and workflow tests on a seeded schema and a browser test of SCR-05 through the composite route |

### 7. Acceptance criteria

```gherkin
Feature: Manual transfer and reassignment screen with reason

  Background:
    Given the business date is 2026-12-15
    Given TRANSFER package version "TRF-2026.12" is in force, and row "TRF-010" refuses a move while a deviation is open
    Given user "U-TM-01" holds RW-TEAMMGR for team "MTG-BKK"
    Given the rwb-access contract mock returns Queue and allocation U for "U-TM-01" over team "MTG-BKK"
    Given case "RW-2026-000401" in queue "MTG-BKK-CO" owned by "U-CO-01", status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01
    Given queue "LIT-BKK-01" uses "ROUND_ROBIN" with a caseload cap of 150 and owners "U-LO-01" with 80 cases and "U-LO-02" with 95 cases, next in turn "U-LO-02"

  Scenario: AC1 Transfer (legacy RWB-E2-012 AC1)
    Given the rwb-decision contract mock returns package TRANSFER version "TRF-2026.12" with the allowing rule of queue "LIT-BKK-01"
    Given case "RW-2026-000401" in a queue of team "MTG-BKK"
    When "U-TM-01" transfers it to queue "LIT-BKK-01" with reason "R02" Customer deceased
    Then the case is in queue "LIT-BKK-01" with owner "U-LO-02"
    Then the previous assignment of "U-CO-01" has ended at the time of the transfer
    Then a new assignment has reason "TRANSFER", reason code "R02", queue "LIT-BKK-01" and the rule ID from TRANSFER version "TRF-2026.12"
    Then one decision log entry holds the rule ID, the rule version "TRF-2026.12", the from and to queue and owner and the reason code
    Then the case keeps status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01
    Then one CaseTransferred event is in the outbox

  Scenario: AC2 Rule blocks (legacy RWB-E2-012 AC2)
    Given the rwb-deviation contract mock returns deviation "X1" open on case "RW-2026-000402" with the complaint officer as owner under rule "R-DEV-02"
    Given the rwb-decision contract mock returns package TRANSFER version "TRF-2026.12" with ruleId "TRF-010" and no allowing output for case "RW-2026-000402"
    Given case "RW-2026-000402" with deviation "X1" open and owned by the complaint officer under rule "R-DEV-02"
    When "U-TM-01" tries to transfer it to queue "LIT-BKK-01" with reason "R05"
    Then RuleEvaluator.evaluate("TRANSFER", facts, 2026-12-15) returns ruleId "TRF-010" and no allowing output
    Then the screen refuses with MSG-P3-033 naming rule "TRF-010"
    Then the case, its assignment and the decision log are unchanged

  Scenario: AC3 Bulk (legacy RWB-E2-012 AC3)
    Given the rwb-access contract mock returns Queue and allocation U for "U-TM-01" over the ten selected cases
    Given ten selected cases in queue "MTG-BKK-CO" owned by "U-CO-01"
    When "U-TM-01" reassigns them to owner "U-CO-03" with 60 open cases and reason "R04"
    Then all ten have owner "U-CO-03"
    Then ten assignments and ten decision log entries are written, each with its rule ID and rule version
    Then "U-CO-03" holds 70 open cases

  Scenario: AC4 No reason (legacy RWB-E2-012 AC4)
    When "U-TM-01" submits a transfer of "RW-2026-000401" with no reason code
    Then the system refuses the transfer with MSG-P3-001
    Then nothing changes

  Scenario: AC5 Owner at the cap (legacy RWB-E2-012 AC5)
    Given the rwb-access contract mock returns Queue and allocation U for "U-TM-01" over queue "MTG-BKK-CO" and no delegation of authority level for a transfer
    Given owner "U-CO-04" holds 150 open cases in queue "MTG-BKK-CO" with a cap of 150
    When "U-TM-01" reassigns "RW-2026-000401" to "U-CO-04" with reason "R01"
    Then the screen shows the at cap warning with MSG-P3-002 naming "U-CO-04"
    Then nothing changes

  Scenario: AC6 Absence reassignment outside the team (legacy RWB-E2-012 AC6)
    Given the rwb-decision contract mock returns rule "R-UNI-18" refusing the reassignment of case "RW-2026-000401" to team "SME-NTH"
    Given owner "U-CO-09" belongs to team "SME-NTH"
    When "U-TM-01" reassigns "RW-2026-000401" to "U-CO-09" with reason "R04"
    Then the system refuses the transfer with MSG-P3-033 naming rule "R-UNI-18"

  Scenario: AC7 Case under legal hold (legacy RWB-E2-012 AC7)
    Given case "RW-2026-000403" with legal hold true
    When "U-TM-01" transfers it to queue "LIT-BKK-01" with reason "R05"
    Then the system refuses the transfer with MSG-P3-005 naming "LIT-BKK-01" and "HELD_LEGAL"

  Scenario: AC8 Two transfers at once (legacy RWB-E2-012 AC8)
    When "U-TM-01" and "U-TM-02" transfer "RW-2026-000401" to different queues in the same second
    Then the case ends in exactly one queue with one new assignment
    Then the system refuses the other request with MSG-GEN-004

  Scenario: AC9 Repeated request (legacy RWB-E2-012 AC9)
    Given the AC1 transfer was made with Idempotency-Key "5b0c7a1e-0000-4000-8000-000000000001"
    When the same request is sent again with the same Idempotency-Key
    Then the response is the same assignment
    Then there is still one new assignment and one decision log entry

  Scenario: AC10 Decision record write fails (legacy RWB-E2-012 AC10)
    Given the decision record store is unavailable
    When "U-TM-01" transfers "RW-2026-000401" to queue "LIT-BKK-01" with reason "R02"
    Then the system refuses the transfer with MSG-P7-003
    Then the case stays in queue "MTG-BKK-CO" with owner "U-CO-01" and no new assignment

  Scenario: AC11 Bulk with refusals (legacy RWB-E2-012 AC11)
    Given ten selected cases, two of which are under a legal hold
    When "U-TM-01" reassigns them to "U-CO-03" with reason "R01"
    Then eight cases move
    Then the two held cases show MSG-P3-005
    Then the summary shows MSG-P3-035 with 8 of 10

  Scenario: AC12 Every owner of the target queue at the cap (legacy RWB-E2-012 AC12)
    Given the rwb-access contract mock returns Queue and allocation U for "U-TM-01" over queue "LIT-BKK-01" and no delegation of authority level for a transfer
    Given both owners of queue "LIT-BKK-01" hold 150 open cases
    When "U-TM-01" transfers "RW-2026-000401" to queue "LIT-BKK-01" with reason "R05"
    Then the screen shows the at cap warning with MSG-P3-002 naming every owner of "LIT-BKK-01"
    Then nothing changes

  Scenario: AC13 No TRANSFER package in force (legacy RWB-E2-012 AC13)
    Given the rwb-decision contract mock returns NoPackageInForce for package TRANSFER on 2026-12-20
    Given no TRANSFER package version is in force on 2026-12-20
    When "U-TM-01" transfers "RW-2026-000401" to queue "LIT-BKK-01" with reason "R02" on 2026-12-20
    Then RuleEvaluator.evaluate("TRANSFER", facts, 2026-12-20) throws NoPackageInForce
    Then the system refuses the transfer with MSG-P3-027 for the package in force check
    Then the case, its assignment and the decision log are unchanged
```

**Note.** The thirteen criteria above are owned by this story, and every Given, When and Then line and every value is the legacy line unchanged; only the mock Givens are added, and each one stands for a cross-service answer that the service cannot produce by itself in development. The `rwb-decision` mock stands for the package version and the rule IDs the embedded Drools kit returns; the `rwb-deviation` mock stands for the open-deviation read that the refusal in AC2 depends on; the `rwb-access` mock stands for the authorisation answer, its scope and the statement that no delegation of authority level applies to a transfer. The three mocks are the contract fakes of RWB-P3-E2012-CON and are the only stubs in the story: every case, queue, owner, cap and count is a row of `rwb_case`.

Two legacy markers inside those criteria are read in the target mechanism, and sections 1, 4, 8, 12 and 13 describe the mechanism: `RuleEvaluator.evaluate("TRANSFER", facts, date)` is the embedded Drools kit of DP-04 called inside the `EvaluateRules` activity, because Drools is never called from workflow code or from a controller; and the decision log entry is the local decision record of DP-03, written in the same transaction and published on `rwb.decision-record.v1`, which keeps the content, the rule ID, the rule version and the place of the legacy entry.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A manual move needs a reason code from LOV-TRANSFER-REASON, read through the reference-data contract of rwb-case and never frozen into the client | REQ-WKM-003; REQ-CWC-010; DP-07 |
| BR2 | A move the TRANSFER package refuses is not made, and the refusing rule ID returned by the kit is shown | REQ-CWC-010; D-RCV-36 T5; DP-04 |
| BR3 | A queue transfer takes its owner from the target queue's assignment method | Queue field assignment_method; RWB-P3-E1020-APP |
| BR4 | An owner at or above the queue's cap cannot receive a case, and every owner of the target queue at the cap is named in the refusal | Queue field capacity_cap; DL23 |
| BR5 | A reassignment for an absent owner stays inside the case's team | R-UNI-18 |
| BR6 | A move keeps the case status, route state, stage clock and timers | R-UNI-18; R-UNI-46 |
| BR7 | A case under a legal hold or closed is not moved | R-UNI-20 |
| BR8 | A move whose decision record cannot be written in the same transaction does not proceed | Principle 5; R-UNI-39; CTL-06; DP-03 |
| BR9 | A repeated request with the same Idempotency-Key has no further effect, at the operation and at the workflow ID | R-UNI-40; DP-09 |
| BR10 | A case with an open deviation stays with the owner the deviation rule named | R-DEV-02; R-DEV-03 |
| BR11 | The TRANSFER version in force on the business date decides the move, and the decision record holds the rule ID and that package version; a case keeps the version it was moved under | D-RCV-36 T5, T7; R-UNI-38 |
| BR12 | No TRANSFER version in force is a refusal (NoPackageInForce), never a default decision, and it is non-retryable in the activity | D-RCV-36 T3; R-UNI-41 |
| BR13 | The move reads no table of another service: the case, the queue, the assignment, the queue member and the timer rows are `rwb_case` rows, the right comes from the rwb-access contract and the deviation flag from the rwb-deviation contract | DP-01; DP-11; ADR-020 |
| BR14 | Each cross-service answer is one hop with a 2 s budget and a breaker; a move never waits on a chain of calls | DP-11; NFR-008; ADR-020 |
| BR15 | The rule package is evaluated only inside the `EvaluateRules` activity, so a replay of `ManualTransferWorkflow` reuses the recorded rule ID and version | DP-04; Temporal and Drools design slide 14 |
| BR16 | The transfer event is `rwb.case.CaseTransferred.v1` on `rwb.case.events.v1`, keyed by the case ID, and the decision record leaves on `rwb.decision-record.v1`; both are written to the outbox in the transaction that changes the case | DP-09; DP-14; EV-04 |

### 9. State transitions

None. This story does not change a case status. It changes the case's queue, owner and team, ends one assignment and writes the next, and rejects a second concurrent move on the version check. The route state, the stage clock, the prescription date and the timers stay as they were (R-UNI-18, R-UNI-46).

| What changes | From | To | Written by |
|---|---|---|---|
| `assignment` | One open row for the previous owner | The same row with `ended_at` set, and one new open row with reason, reason code, queue and rule ID | The `RecordAndApply` activity, one transaction |
| `recovery_case` | The previous `queue_id`, `owner_user_id`, `team_code` and version | The target `queue_id`, `team_code`, the picked or named `owner_user_id` and version + 1 | The `RecordAndApply` activity, same transaction |
| Decision record | No entry | One entry with the rule ID, the rule version "TRF-2026.12", the from and to queue and owner, the reason code and the hash link | The decision-record library of DP-03, same transaction |
| Outbox | No row | One `rwb.case.CaseTransferred.v1` row and one decision-record row | The outbox library of DP-09, same transaction |

The workflow states of the manual path are these, and no case state is among them.

| From | Event | To |
|---|---|---|
| No workflow | A manual request passes the pre-checks | `ManualTransferWorkflow` started with the case ID and the idempotency key |
| `ManualTransferWorkflow` running | `EvaluateRules` answers with a rule | `RecordAndApply` scheduled |
| `ManualTransferWorkflow` running | `EvaluateRules` raises `NoPackageInForce` or refuses | The workflow ends with the refusal; the case is unchanged |
| `RecordAndApply` committed | The record, the change and the outbox commit together | The workflow returns the assignment; the caller answers 200 |
| `ManualTransferWorkflow` finished | The same Idempotency-Key arrives again | The finished execution is returned; no second move |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | Transfers and reassigns cases in the team's scope (Queue and allocation U) |
| RW-CAPACITY, capacity and workforce planner | Reassigns cases for capacity (Queue and allocation RU, scope All) |
| SY-CASEWF, case workflow identity | Runs `ManualTransferWorkflow` and writes the assignment and the case (Queue and allocation CRU) |
| SY-RULES, Drools evaluator | Evaluates package TRANSFER inside the `EvaluateRules` activity and returns the rule ID and the package version |
| SY-DECLOG, decision-record writer | Writes the record and publishes it on the shared topic |
| RW-CASEOWN, case owner | Reads the result only (Queue and allocation R); cannot transfer |
| rwb-access | Answers the role, scope and Queue and allocation U check through its contract, cached per request |
| rwb-deviation | Answers the open-deviation read the refusal of AC2 depends on |

No approval level from the delegation of authority applies: a transfer moves work, not money. The authorisation decision is rwb-access's; this story consumes it and adds no guard of its own beyond the cached decision the service template's library holds.

### 11. Data

| BR Field ID | Table in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `recovery_case` | id | Read |
| DF-CAS-005 | `recovery_case` | status | Read |
| DF-CAS-007 | `recovery_case` | route_state | Read |
| DF-CAS-009 | `recovery_case` | owner_user_id | Write |
| DF-CAS-010 | `recovery_case` | queue_id | Write |
| DF-CAS-011 | `recovery_case` | team_code | Write |
| DF-CAS-019 | `recovery_case` | deviation_open | Read |
| DF-CAS-020 | `recovery_case` | legal_hold | Read |
| DF-CAS-021 | `recovery_case` | rule_version | Write |
| DF-WRK-001 | `queue` | id | Read |
| DF-WRK-004 | `queue` | team_code | Read |
| DF-WRK-006 | `queue` | assignment_method | Read |
| DF-WRK-007 | `queue` | capacity_cap | Read |
| DF-WRK-009 to DF-WRK-016 | `assignment` | all fields | Write |
| DF-WRK-039 | `assignment` | queue_id | Write |
| DF-WRK-040 | `assignment` | transfer_reason_code | Write |
| DF-WRK-045 to DF-WRK-052 | `queue_member` | the member capacity and the open-case count of an owner | Read |
| DF-DEC-003, DF-DEC-004, DF-DEC-005 | decision-record library table | decision_code, rule_id, rule_version | Write, in the same transaction |
| DF-DEC-012, DF-DEC-014, DF-DEC-016 | decision-record library table | final_call, actions (from and to queue and owner, reason code), decided_at | Write, in the same transaction |
| DF-DEC-017, DF-DEC-018, DF-DEC-028 | decision-record library table | prev_hash, entry_hash, chain_seq | Write, in the same transaction |
| DF-DEC-030, DF-DEC-031 | decision-record library table | actor_user_id, idempotency_key | Write, in the same transaction |
| (rule row, through the kit) | package TRANSFER, held by rwb-decision | rule_id, package version label, condition, row order, target queue code, outputs | Read only through the evaluated model |
| (deviation) | owned by S8 | deviation_code, raised_at, handler_user_id, paused_state | Read, through the rwb-deviation contract |
| DF-REF-159 to DF-REF-184 | `reference_version`, `reference_row` | LOV-TRANSFER-REASON rows with their version in force | Read, through the reference-data contract |

The rule row is read only as the evaluated model returned by the kit: this story reads no workbook, no DRL source and no rule row table, and `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are rwb-decision's. `deviation` is S8's and is read only through its contract; no deviation row is copied into `rwb_case`. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3). This story adds no operation: it builds the manual path of the transfer operation and reads it back through the existing reads.

| Method | Path | Purpose | Added in this story | Access |
|---|---|---|---|---|
| POST | `/cases/{caseId}/transfer` | Transfer or reassign one case with a reason code; `Idempotency-Key` required; one call per case, a selection is sent case by case | The manual path over `ManualTransferWorkflow`, the three refusals and the reason-list read; the request and response shapes are RWB-P3-E1021-CON's and do not change | Queue and allocation U, scope applied |
| GET | `/cases/{caseId}` | Read the case after the move, so the screen shows the new queue and owner | None; the operation is RWB-P3-E1023-CON's | Case record R, scope applied |
| GET | `/queues` | The target queue list with counts, age and cap use, for the form | None; the operation is RWB-P3-E2011-CON's | Queue and allocation R, scope applied |
| GET | `/queues/{queueId}/cases` | The cases of a queue, so SCR-07 hands a selection of case IDs to SCR-05 | None; the operation is RWB-P3-E2011-CON's | Queue and allocation R, scope applied |

`POST /queues/{queueId}/placements` is owned by P3 and is not used by this screen: it places a case on a queue from a model or an agent, and it belongs to RWB-P3-E2036-APP. The reference-list read the form needs, `GET /api/recovery/case/v1/admin/lists/{listCode}`, is provided by the same service under RWB-P3-E1043-CON (Ownership Map api row, ASM-0041) and is listed in 12.2 as an own-contract read; this story consumes it and changes nothing on it. The per-case result element a selection renders is the contract's `TransferSelection`, one entry per case with its assignment or its message ID and the done and total counts; its order and its required fields are Not specified in the source documents (GAP-0710; ASM-1257). Errors of the transfer operation: 401 no session (MSG-P4-001); 403 no Queue and allocation U (MSG-P4-002); 404 case unknown or out of scope (MSG-P4-003); 409 case closed or held (MSG-P3-005), rule refuses (MSG-P3-033), record changed (MSG-GEN-004); 422 no reason (MSG-P3-001), owner at cap (MSG-P3-002), no package in force (MSG-P3-027); 503 decision record write failed (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId`, `detail`, `instance` and `traceId`.

#### 12.2 REST operations consumed

| Method | Path | Owner | Used for | Timeout |
|---|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and Queue and allocation U check, cached per request | One hop, 2 s (DP-11) |
| GET | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | The open deviations of the case, which decide the refusal of AC2 and the rule R-DEV-02 owner | One hop, 2 s (DP-11) |
| GET | `/api/recovery/decision/v1/rule-models/{packageCode}/{version}` | P7 rwb-decision | The TRANSFER model the embedded Drools kit fetches, verifies by checksum and swaps in; the element names are fixed in RWB-P3-E2042-CON | One hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case, own contract (RWB-P3-E1043-CON, DP-07; Ownership Map api row, ASM-0041) | The LOV-TRANSFER-REASON values in force with their version, which the form renders and the operation checks a code against | In process, no hop |

Three hops at most per move, and the kit fetch is cached per package version so a move normally pays for two: the authorise answer and the deviation read.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.case.CaseTransferred.v1` (EV-04) | `rwb.case.events.v1` | P3 | caseId | caseId, fromOwner, toOwner, reasonCode, ruleId |
| decision record | `rwb.decision-record.v1` | PLT library, consumed by P7 | caseId | the hash-chained decision record |

Both are written to the outbox in the transaction that changes the case, and the relay publishes them; the transfer path publishes nothing else. CloudEvents 1.0 envelope; no personal data in either payload.

#### 12.4 Events consumed

None. The manual path is started by the REST call and not by an event; the seven trigger events of the rule-driven path are the case router's and belong to RWB-P3-E1021-APP. The deviation answer this story needs is read over REST and is not an event subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `ManualTransferWorkflow` | Workflow, one execution per manual request, workflow ID carries the case ID and the idempotency key | `rwb-case` | Input: case ID, target queue or owner, reason code, note, caller, idempotency key, business date. Output: the assignment view or the refusal |
| `EvaluateRules` | Activity, from the workflow kit | `rwb-case` | Input: package code TRANSFER, the facts, the business date. Output: `RuleResult(packageCode, packageVersion, ruleId, outputs)`; raises `NoPackageInForce`, non-retryable |
| `RecordAndApply` | Activity, from the workflow kit | `rwb-case` | Input: the decision record, the state change and the outbox rows; one transaction, no partial write |
| `CaseWorkflow` | Workflow, parent, one per case | `rwb-case` | Not changed by this story; the manual execution is its own workflow so the 2 s answer never waits on a case's timer history |

The retry policy of the two activities, their start-to-close and schedule-to-close values and the concurrency of the manual path are deployment values carried by RWB-P3-E2012-OPS (GAP-0713; ASM-1260).

#### 12.6 Schedules

None. A manual move is started by a person, not by a clock; this story registers no Schedule and reads no scheduler state. The 06:30 rebalancing Schedule and the morning allocation stay with RWB-P3-E1020-APP and RWB-P3-E1021-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `recovery_case` | P3 (rwb_case) | Queue, team, owner, status, legal hold, deviation flag and rule version; the version column is the optimistic lock of the move |
| `assignment` | P3 (rwb_case) | End the open row and insert the new one with reason, reason code, queue and rule ID |
| `queue` | P3 (rwb_case) | Target queue, team, assignment method and capacity cap |
| `queue_member` | P3 (rwb_case) | Member capacity and the open-case count used by the cap check |
| decision-record library table, `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in rwb_case | The record, the outbox row and the stored response of the idempotency key |

`deviation` is owned by S8 and `decision_log_entry` by P7; neither is read directly, and `rwb_case` holds no foreign key into another schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Queue and allocation U to "U-TM-01" over the team and the selected cases, refusing RW-CASEOWN with MSG-P4-002, refusing scope over SME-NTH, and answering "no delegation of authority level" for a transfer |
| rwb-deviation WireMock | The S8 contract | `GET /cases/{caseId}/deviations` with X1 open on RW-2026-000402, the empty answer for RW-2026-000401 and a delayed answer beyond 2 s |
| rwb-decision WireMock | The P7 contract | `GET /rule-models/{packageCode}/{version}` for TRANSFER "TRF-2026.12" with its checksum, one wrong checksum and a 404 for the version that is not in force |
| Drools kit stub | RWB-PLT-E1072-CON | Package TRANSFER "TRF-2026.12" with row "TRF-010" refusing and the allowing rule of "LIT-BKK-01"; `NoPackageInForce` for 2026-12-20; rule "R-UNI-18" refusing the out-of-team reassignment |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 3 consumed plus 1 own contract | The transfer and the three reads provided; authorise, deviations and the rule model consumed; the reference-data contract read is in process |
| Kafka | 2 published, none consumed | `rwb.case.CaseTransferred.v1` and the decision record, both through the outbox; the read path carries no Kafka traffic |
| Temporal | 1 workflow, 2 activities | `ManualTransferWorkflow` with `EvaluateRules` and `RecordAndApply`; `CaseWorkflow` is not changed |
| File | None | No file is read or written; the reason list is reference data, not a file |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.case.transfer`, module `case/transfer`; front end folder `src/modules/recovery/case/transfer`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The same-service CON baselines RWB-P3-E2012-CON, RWB-P3-E1021-CON, RWB-P3-E2011-CON and RWB-P3-E1043-CON are class H dependencies of this story and are not DP rows. DP-06 is not claimed: the story reads no business parameter, and the selection limit of 50 cases is a screen value, not a decision input.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TransferController | Controller | `POST /cases/{caseId}/transfer` for the manual path; the pre-checks; the problem responses; the `Idempotency-Key` handling |
| ManualTransferService | Service | Starts `ManualTransferWorkflow`, waits for its result inside the 2 s budget, maps a refusal to its status and message |
| TransferFactsBuilder | Service | Builds the facts of the case, the target queue or owner, the reason code and the business date for `EvaluateRules` |
| DeviationCheckClient | Client | Reads the open deviations of the case once, one hop, 2 s, with a breaker; never reads the `deviation` table |
| AccessCheckClient | Client | Calls the rwb-access authorise contract, cached per request |
| OwnerLoadRepository | Repository | Counts the open cases of an owner in a queue for the cap check, from `assignment` and `queue_member` |
| AssignmentRepository | Repository | Ends the open row and writes the new one inside `RecordAndApply` |
| ReasonListReader | Service | Reads LOV-TRANSFER-REASON through the reference-data contract and caches it per version |
| TransferCasePage | React component | SCR-05 with the Form, At cap, Refused and Saved states |
| BulkTransferRunner | React component | Sends one request per selected case in sequence, keeps the per-row result and renders the MSG-P3-035 summary |

**Database.** No migration adds a column: `assignment.queue_id` (DF-WRK-039) and `assignment.transfer_reason_code` (DF-WRK-040) arrive with the migration of RWB-P3-E1021-APP, and `recovery_case.version` is the optimistic lock of the move. This story's Flyway step adds one read-side index in schema `rwb_case`, `ix_assignment_case_open ON assignment (case_id) WHERE ended_at IS NULL`, and nothing else. `idempotency_key` is the platform library's object, created in `rwb_case` by the same sequence (DP-09, DP-15).

**Configuration and reference data.** LOV-TRANSFER-REASON is read with the reference-list operation `GET /api/recovery/case/v1/admin/lists/{listCode}` of the reference-data contract of rwb-case (RWB-P3-E1043-CON, DP-07; Ownership Map api row, ASM-0041) with its version in force; the six codes in force are the intended set of section 3 and no code is written in code. The maximum number of cases one selection carries is 50, the legacy assumed value of DL23, held as a screen value of this story and enforced by the screen and the composite route. `transfer.deviation-timeout-ms` = 2000 and `transfer.authorise-timeout-ms` = 2000 are service configuration values fixed by the 2 s budget of DP-11. The TRANSFER package rows are authored and approved through RWB-P3-E1073-APP; this story loads none.

**Build steps**

1. Extend the generated client types from RWB-P3-E2012-CON and add the contract test for the manual path; the request and response stay those of RWB-P3-E1021-CON.
2. `ReasonListReader` over the reference-list operation `GET /admin/lists/{listCode}` of the reference-data contract, with the version in force cached and the AC4 refusal for a missing code; tests AC4.
3. `ManualTransferService` and `TransferController` pre-checks in this order: reason, case state and hold, scope, right; map each refusal to its status and message ID; tests AC4, AC5, AC6, AC7 and the refusal of section 16.
4. `TransferFactsBuilder` and the `ManualTransferWorkflow` start with the workflow ID that carries the idempotency key; tests AC9 and AC8.
5. `EvaluateRules` wiring: map `RuleResult` to the assignment's rule ID and the record's `ruleVersion`, and map `NoPackageInForce` to 422 with MSG-P3-027; tests AC1, AC2, AC6, AC13.
6. `DeviationCheckClient` with the 2 s timeout and the breaker, and the BR10 refusal; tests AC2.
7. `OwnerLoadRepository` and the cap check, including the every-owner case; tests AC5, AC12.
8. `RecordAndApply` wiring of the decision record and the outbox, with the failure path of AC10 leaving the case unchanged; tests AC1, AC3, AC10.
9. `BulkTransferRunner` with the per-row result and the MSG-P3-035 summary; tests AC3, AC11.
10. `TransferCasePage` against the composite route of RWB-PLT-N001-CON; browser test of SCR-05 for AC1 to AC13.

**Feature switch.** `rwb.p3.manual-transfer`, a service configuration value. Off: SCR-05 is hidden and the operation answers 403 for every role except SY-CASEWF. The rule evaluation stays behind `rwb.p3.drools` (RWB-P3-E1073-APP); with that switch off the operation refuses every move with MSG-P3-027.

**Done when.** Every test in section 16 passes, the four contract fakes drive every cross-service answer, one manual transfer of each reason code in SIT shows on the case queue history with the rule ID and the package version on its decision record entry, and a selection of ten cases with two refusals renders the summary with 8 of 10.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-001 | No reason code | Choose a reason for the transfer. |
| MSG-P3-002 | Target owner, or every owner of the target queue, at the cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-005 | Case closed or under a legal hold | This case cannot move to {state} from {current}. |
| MSG-P3-027 | No TRANSFER package version in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P3-033 | A TRANSFER rule refuses the move | Rule {rule} does not allow this transfer. |
| MSG-P3-035 | Bulk move with refusals | {done} of {total} cases were moved. The others show the reason on their row. |
| MSG-GEN-004 | Two moves of one case at once | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-005 | Move saved | Saved. |
| MSG-P4-002 | A role without Queue and allocation U | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | No session, or no Recovery Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-003 | The case is unknown or outside the caller's scope | This case is not in your scope. |

For MSG-P3-027 the {check} value is "package in force" and {detail} names the package code TRANSFER and the business date only. For MSG-P3-033 the {rule} value is `RuleResult.ruleId`; for the out-of-team reassignment it is R-UNI-18. For MSG-P3-005 in AC7 the {state} value is the target queue "LIT-BKK-01" and the {current} value is "HELD_LEGAL". MSG-P3-033 and MSG-P3-035 are new in this key; their text is the legacy text. The answer the screen renders for the cap and for the hold before any write is Not specified in the source documents (GAP-0711; ASM-1258); this story renders the contract's refusal element, which names the owner, or every owner, on the cap answer and the target state and the hold state on the hold answer. Thai text follows DL10.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-05 Transfer case | Form | Chooses a queue or an owner, a reason code from the list in force, and a note; confirms |
| SCR-05 Transfer case | At cap warning | Reads MSG-P3-002 naming the owner or every owner of the queue; chooses another owner or the team queue |
| SCR-05 Transfer case | Refused | Reads MSG-P3-033 with the rule ID, MSG-P3-005 with the state, or MSG-P3-027 when no TRANSFER version is in force |
| SCR-05 Transfer case | Saved | Reads MSG-GEN-005, or the per-case results and MSG-P3-035 for a selection |
| SCR-07 Team queues | List | Selects up to 50 cases and opens SCR-05 for them |
| SCR-09 Exception queue | List | Not used by this story; a refused move is not queued |

The screen itself is a gateway-bff composite route (DP-19): the route owns the path and the merge order, and rwb-case contributes the form's queue list, the case read after the move and the move itself. The screen never renders a rule row, a package or a deviation row of another service; it renders the rule ID, the message ID and the state.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-012-01 | AC1, BR1, BR3, BR6, BR11 | End to end | RW-2026-000401 to LIT-BKK-01, reason R02, TRANSFER version TRF-2026.12 |
| TC-E2-012-02 | AC2, BR2, BR10 | End to end | RW-2026-000402 with X1 open under R-DEV-02; row TRF-010 refuses |
| TC-E2-012-03 | AC3, BR4, BR5, BR11 | End to end | Ten cases to U-CO-03 with 60 open cases, reason R04 |
| TC-E2-012-04 | AC4, BR1 | End to end | Request with no reason code |
| TC-E2-012-05 | AC5, BR4 | End to end | U-CO-04 at 150 of 150 |
| TC-E2-012-06 | AC6, BR5 | End to end | U-CO-09 in team SME-NTH, reason R04; rule R-UNI-18 |
| TC-E2-012-07 | AC7, BR7 | End to end | RW-2026-000403 with legal hold true |
| TC-E2-012-08 | AC8, BR9 | Component | Two parallel requests for one case; the version check and the workflow ID |
| TC-E2-012-09 | AC9, BR9 | Component | Same Idempotency-Key twice, at the operation and at the workflow |
| TC-E2-012-10 | AC10, BR8 | End to end | Decision record store stopped |
| TC-E2-012-11 | AC11 | End to end | Ten cases, two under a legal hold |
| TC-E2-012-12 | AC12, BR4 | End to end | Both LIT-BKK-01 owners at 150 |
| TC-E2-012-13 | Access | Component | RW-CASEOWN (Queue and allocation R) calls the transfer operation; refused with MSG-P4-002 |
| TC-E2-012-14 | Principle 5 | NFR | Decision record write forced to fail; case, assignment and outbox unchanged |
| TC-E2-012-15 | AC13, BR12 | End to end | No TRANSFER version in force on 2026-12-20; NoPackageInForce and MSG-P3-027 |

The fifteen legacy IDs are kept in the order of the legacy story. The legacy levels map System to End to end, Access to Component and Resilience to NFR; TC-E2-012-08 and TC-E2-012-09 are levelled Component because they prove the concurrency and the idempotency of the operation rather than a business outcome on the screen. The full test, with its Given, When and Then, is kept under the same test case ID in the recovered test set.

### 17. Guardrails

- No business value in code: the reason codes, the caps and the transfer rows are data read through the reference-data contract and the evaluated package; the selection limit of 50 is a screen value.
- No personal data in logs, tests, workflow history or prompts: the note field is not logged, the events carry IDs and codes only, and the workflow payload codec encrypts every payload.
- No read of another service's table (DP-01): the deviation comes only through the rwb-deviation contract, the right only through the rwb-access contract and the rule row only as the evaluated model.
- The decision record is written in the same transaction as the change; a failed write leaves the case, the assignment and the outbox as they were.
- Each case in a selection is its own request, its own workflow, its own rule evaluation and its own transaction.
- One evaluator: the transfer rules are read only through the embedded Drools kit, inside the `EvaluateRules` activity, and no caller reads a workbook, a DRL source or a rule row.
- One hop per cross-service answer, 2 s timeout and a breaker; a downstream that does not answer refuses the move and grants nothing.
- The request, the response, the errors and the authorisation of the manual transfer are RWB-P3-E1021-CON's; this story adds no field to the API.
- A move never resets the stage clock, the route state or the prescription date.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-003 | Manual transfer or reassignment only with a reason code from the agreed list | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-03 | All recovery processes | R-DEV-02, R-UNI-20, R-UNI-39, R-UNI-40 | TC-E2-012-01, TC-E2-012-02, TC-E2-012-04, TC-E2-012-07 to TC-E2-012-10, TC-E2-012-13, TC-E2-012-14, TC-E2-012-15 |
| REQ-WKM-007 | An absent or over-cap owner's cases reallocated inside the team, keeping state and clocks | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-04, FEAT-WKM-10 | All recovery processes | R-UNI-18, R-UNI-46 | TC-E2-012-03, TC-E2-012-05, TC-E2-012-06, TC-E2-012-11, TC-E2-012-12 |
| REQ-WKM-008 | Queue and transfer history visible on the case | Business Requirements Epic 2, section 4; Program, section 5.3 | FEAT-WKM-03 | All recovery processes | R-UNI-18 | TC-E2-012-01, TC-E2-012-03 |
| REQ-CWC-010 | Cases move by rule or by manual request with a reason code | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-10 | All recovery processes | R-UNI-20, R-UNI-21, R-UNI-40 | TC-E2-012-01, TC-E2-012-02, TC-E2-012-15 |
| REQ-CWC-016 | Every transfer logged with the rule ID and the rule version that caused it | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-10 | All recovery processes | R-UNI-39 | TC-E2-012-01, TC-E2-012-03, TC-E2-012-10, TC-E2-012-14 |
| ADR-017 | Embedded Drools per service; the registry in rwb-decision | — | — | All recovery processes | D-RCV-36 T5 | TC-E2-012-01, TC-E2-012-02, TC-E2-012-15 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | — | — | All recovery processes | R-UNI-39 | TC-E2-012-02, TC-E2-012-14 |
| ADR-022 | Local decision record plus central ledger | — | — | All recovery processes | R-UNI-39 | TC-E2-012-01, TC-E2-012-10, TC-E2-012-14 |

The rule ID and the package version on the decision record entry satisfy REQ-CWC-016 through RWB-P3-E1021-APP and the kit; this story adds no requirement ID of its own.

### 19. Out of scope

- The rule-driven transfers on stage change, route decided, timer expired, deviation raised or cleared, approval needed, document received and payment missed (RWB-P3-E1021-APP).
- The automatic reallocation when an owner is absent or over the cap (R-UNI-18, R-UNI-19, JOB-06, RWB-P3-E1020-APP).
- The queue view screens, the filters and the ageing, and the selection that opens SCR-05 (RWB-P3-E2011-APP).
- The queue history and the timeline on the case (RWB-P3-E2016-APP).
- The contract document, its request and response shapes, the reason-list reference and the fakes (RWB-P3-E2012-CON).
- The Helm values, the consumer groups, the activity timeouts, the dashboards, the alerts and the runbook (RWB-P3-E2012-OPS).
- The cross-service journey harness and its evidence (RWB-ITG-E2012-ITG).
- The TRANSFER package rows themselves, their scenarios, their approval and their rollback (RWB-P3-E1073-APP).
- Partner placement and recall (Epic 6), placement on a queue from a model or an agent (RWB-P3-E2036-APP).
