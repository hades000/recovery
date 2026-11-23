<!-- source: 04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 012 Manual transfer and reassignment screen with reason v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5.zip!RWB E2 012 Manual transfer and reassignment screen with reason v2.md`  
> **Converted from:** Markdown (extracted)

# RWB-E2-012 Manual transfer and reassignment screen with reason

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-012 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-WKM-03 Transfer a case manually with a reason; FEAT-WKM-04 Reassign a case to another owner; FEAT-WKM-10 Reallocate when an owner is unavailable |
| Requirement IDs | REQ-WKM-003, REQ-WKM-007, REQ-WKM-008 |
| BRD section | Business Requirements Epic 2, sections 3.3 and 4; Business Requirements Program, section 5.3 |
| L3 process | All recovery processes |
| Decision | D-RCV-36; ADR-012 |
| Priority | Must |
| Depends on | RWB-E1-021, RWB-E1-072, RWB-E2-011 |
| Status | Ready for build |

## 1. Story

As a **team manager (RW-TEAMMGR)**, I want **a screen to transfer a case to another queue or reassign it to a person, with a reason code required and the TRANSFER rule package checked**, so that **a hand-off is one action with a record, not an email**.

## 2. Business rationale

Today ownership changes are agreed by email, and audit found debtors who met the criteria were not transferred to the responsible unit (CTL-03). A manual move must carry a coded reason, respect the caseload cap and the transfer rules, keep the case's state and clocks, and leave a decision log entry. This story gives the team manager one screen for a single or a bulk move.

The transfer rules are rows of the TRANSFER rule package (RWB-E1-021). The manual move is evaluated by RuleEvaluator, so the screen shows the rule ID that refused the move and the decision log names the rule and the package version that decided (D-RCV-36 T3, T5). The manual transfer API does not change: the endpoint, the request, the response and the errors are the same as RWB-E1-021.

It meets REQ-WKM-003, REQ-WKM-007 and REQ-WKM-008. The measure is that every manual move has an assignment record with a reason code, a decision log entry with a rule ID and a package version, and a rule ID on the screen when the move is refused.

## 3. Preconditions

- RWB-E1-021 is done: the TRANSFER rule package is in force, and a manual transfer is evaluated by `RuleEvaluator.evaluate("TRANSFER", facts, businessDate)`, which returns the allowing rule or refuses with the rule ID that blocks the move.
- RWB-E1-072 is done: the published RuleEvaluator and RuleCatalog exist, and the rule package store holds the TRANSFER versions.
- RWB-E2-011 is done: team queues and the case list open SCR-05 for a case or a selection.
- RWB-E1-020 is done: `AssignmentEngine` picks an owner in a queue by its method and caseload cap.
- The decision log writer (RWB-E1-027) is available through the P7 interface and accepts a rule ID with its rule version.
- LOV-TRANSFER-REASON (new, see Additions) is loaded with the agreed reason codes. Assumed values: R01 Capacity, R02 Customer deceased, R03 Skill, R04 Owner absent, R05 Legal referral, R06 Wrong queue (DL23).
- The person holds RW-TEAMMGR or RW-CAPACITY (Queue and allocation U) and the case is in their scope.

## 4. Flow

1. Team manager: opens SCR-05 Transfer case from SCR-03 Case record or from a selection on SCR-07 Team queues.
2. Team manager: chooses a target queue or a target owner, a reason code and an optional note, and confirms.
3. Front end: calls `POST /api/recovery/v1/cases/{caseId}/transfer` with a new Idempotency-Key per case.
4. Transfer service: checks the reason code, that the case is open and not under a legal hold, and the scope.
5. SY-RULES: builds TransferFacts from the case, the target queue or owner, the reason code and the business date, and calls `RuleEvaluator.evaluate("TRANSFER", facts, businessDate)`. The RuleResult names the rule ID that allows or refuses the move and the package version that decided.
6. Transfer service: on a refusal, stops and shows MSG-P3-033 with the rule ID from the result; otherwise, for a queue transfer, asks `AssignmentEngine` for the owner by the target queue's method, and for a reassignment checks the target owner is below the cap and, for reason R04, in the case's team.
7. Transfer service: writes the decision log entry through the P7 interface with the rule ID and the package version; on success, in one transaction ends the current assignment, writes the new assignment with reason, rule ID, queue and reason code, updates the case queue, owner and team, and writes CaseTransferred (EV-04) to the outbox.
8. Front end: shows state Saved with MSG-GEN-005; for a bulk move, one result per case and the summary.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No reason code | Refused; nothing changes | MSG-P3-001 | AC4 |
| X2 | A TRANSFER package rule refuses the move | Refused; the refusing rule ID from RuleEvaluator is shown | MSG-P3-033 | AC2 |
| X3 | The target owner is at the caseload cap | At cap warning; refused | MSG-P3-002 | AC5 |
| X4 | Every owner of the target queue is at the caseload cap | At cap warning naming every owner; refused | MSG-P3-002 | AC12 |
| X5 | Reason R04 and the target owner is outside the case's team | Refused naming R-UNI-18 | MSG-P3-033 | AC6 |
| X6 | The case is closed or under a legal hold | Refused | MSG-P3-005 | AC7 |
| X7 | Two transfers of one case at the same time | One succeeds; the other is refused | MSG-GEN-004 | AC8 |
| X8 | The same request is sent twice with the same Idempotency-Key | The first result is returned; no second record | None | AC9 |
| X9 | The decision log write fails | Nothing changes | MSG-P7-003 | AC10 |
| X10 | Some cases in a bulk move are refused | The others move; each refused case shows its message | MSG-P3-035 | AC11 |
| X11 | No TRANSFER package version is in force on the business date | Refused; nothing changes and no decision log entry is written | MSG-P3-027 | AC13 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the TRANSFER package and the assignment engine of Epic 1; adds the screen and the coded reason |
| Negotiable | Reason codes, the bulk limit and the rule rows are data; the checks are fixed |
| Valuable | Ends ownership changes by email; every move has a record and a meaningful refusal |
| Estimable | One endpoint extended, one service, one screen |
| Small | Fits in one sprint with its tests |
| Testable | API tests on a seeded database and a browser test of SCR-05 |

## 7. Acceptance criteria

```gherkin
Feature: Manual transfer and reassignment screen with reason

  Background:
    Given the business date is 2026-12-15
    Given TRANSFER package version "TRF-2026.12" is in force, and row "TRF-010" refuses a move while a deviation is open
    Given user "U-TM-01" holds RW-TEAMMGR for team "MTG-BKK"
    Given case "RW-2026-000401" in queue "MTG-BKK-CO" owned by "U-CO-01", status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01
    Given queue "LIT-BKK-01" uses "ROUND_ROBIN" with a caseload cap of 150 and owners "U-LO-01" with 80 cases and "U-LO-02" with 95 cases, next in turn "U-LO-02"

  Scenario: AC1 Transfer
    Given case "RW-2026-000401" in a queue of team "MTG-BKK"
    When "U-TM-01" transfers it to queue "LIT-BKK-01" with reason "R02" Customer deceased
    Then the case is in queue "LIT-BKK-01" with owner "U-LO-02"
    Then the previous assignment of "U-CO-01" has ended at the time of the transfer
    Then a new assignment has reason "TRANSFER", reason code "R02", queue "LIT-BKK-01" and the rule ID from TRANSFER version "TRF-2026.12"
    Then one decision log entry holds the rule ID, the rule version "TRF-2026.12", the from and to queue and owner and the reason code
    Then the case keeps status "IN_PROGRESS", route state "WITH_FCR_OFFICER" and stage clock start 2026-12-01
    Then one CaseTransferred event is in the outbox

  Scenario: AC2 Rule blocks
    Given case "RW-2026-000402" with deviation "X1" open and owned by the complaint officer under rule "R-DEV-02"
    When "U-TM-01" tries to transfer it to queue "LIT-BKK-01" with reason "R05"
    Then RuleEvaluator.evaluate("TRANSFER", facts, 2026-12-15) returns ruleId "TRF-010" and no allowing output
    Then the screen refuses with MSG-P3-033 naming rule "TRF-010"
    Then the case, its assignment and the decision log are unchanged

  Scenario: AC3 Bulk
    Given ten selected cases in queue "MTG-BKK-CO" owned by "U-CO-01"
    When "U-TM-01" reassigns them to owner "U-CO-03" with 60 open cases and reason "R04"
    Then all ten have owner "U-CO-03"
    Then ten assignments and ten decision log entries are written, each with its rule ID and rule version
    Then "U-CO-03" holds 70 open cases

  Scenario: AC4 No reason
    When "U-TM-01" submits a transfer of "RW-2026-000401" with no reason code
    Then the system refuses the transfer with MSG-P3-001
    Then nothing changes

  Scenario: AC5 Owner at the cap
    Given owner "U-CO-04" holds 150 open cases in queue "MTG-BKK-CO" with a cap of 150
    When "U-TM-01" reassigns "RW-2026-000401" to "U-CO-04" with reason "R01"
    Then the screen shows the at cap warning with MSG-P3-002 naming "U-CO-04"
    Then nothing changes

  Scenario: AC6 Absence reassignment outside the team
    Given owner "U-CO-09" belongs to team "SME-NTH"
    When "U-TM-01" reassigns "RW-2026-000401" to "U-CO-09" with reason "R04"
    Then the system refuses the transfer with MSG-P3-033 naming rule "R-UNI-18"

  Scenario: AC7 Case under legal hold
    Given case "RW-2026-000403" with legal hold true
    When "U-TM-01" transfers it to queue "LIT-BKK-01" with reason "R05"
    Then the system refuses the transfer with MSG-P3-005 naming "LIT-BKK-01" and "HELD_LEGAL"

  Scenario: AC8 Two transfers at once
    When "U-TM-01" and "U-TM-02" transfer "RW-2026-000401" to different queues in the same second
    Then the case ends in exactly one queue with one new assignment
    Then the system refuses the other request with MSG-GEN-004

  Scenario: AC9 Repeated request
    Given the AC1 transfer was made with Idempotency-Key "5b0c7a1e-0000-4000-8000-000000000001"
    When the same request is sent again with the same Idempotency-Key
    Then the response is the same assignment
    Then there is still one new assignment and one decision log entry

  Scenario: AC10 Decision log write fails
    Given the decision log store is unavailable
    When "U-TM-01" transfers "RW-2026-000401" to queue "LIT-BKK-01" with reason "R02"
    Then the system refuses the transfer with MSG-P7-003
    Then the case stays in queue "MTG-BKK-CO" with owner "U-CO-01" and no new assignment

  Scenario: AC11 Bulk with refusals
    Given ten selected cases, two of which are under a legal hold
    When "U-TM-01" reassigns them to "U-CO-03" with reason "R01"
    Then eight cases move
    Then the two held cases show MSG-P3-005
    Then the summary shows MSG-P3-035 with 8 of 10

  Scenario: AC12 Every owner of the target queue at the cap
    Given both owners of queue "LIT-BKK-01" hold 150 open cases
    When "U-TM-01" transfers "RW-2026-000401" to queue "LIT-BKK-01" with reason "R05"
    Then the screen shows the at cap warning with MSG-P3-002 naming every owner of "LIT-BKK-01"
    Then nothing changes

  Scenario: AC13 No TRANSFER package in force
    Given no TRANSFER package version is in force on 2026-12-20
    When "U-TM-01" transfers "RW-2026-000401" to queue "LIT-BKK-01" with reason "R02" on 2026-12-20
    Then RuleEvaluator.evaluate("TRANSFER", facts, 2026-12-20) throws NoPackageInForce
    Then the system refuses the transfer with MSG-P3-027 for the package in force check
    Then the case, its assignment and the decision log are unchanged
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A manual move needs a reason code from LOV-TRANSFER-REASON | REQ-WKM-003; REQ-CWC-010 |
| BR2 | A move the TRANSFER package refuses is not made, and the refusing rule ID returned by RuleEvaluator is shown | REQ-CWC-010; RWB-E1-021; D-RCV-36 T5 |
| BR3 | A queue transfer takes its owner from the target queue's assignment method | Queue field assignment_method; RWB-E1-020 |
| BR4 | An owner at or above the queue's cap cannot receive a case | Queue field capacity_cap; DL23 |
| BR5 | A reassignment for an absent owner stays inside the case's team | R-UNI-18 |
| BR6 | A move keeps the case status, route state, stage clock and timers | R-UNI-18; R-UNI-46 |
| BR7 | A case under a legal hold or closed is not moved | R-UNI-20 |
| BR8 | A move that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR9 | A repeated request with the same Idempotency-Key has no further effect | R-UNI-40 |
| BR10 | A case with an open deviation stays with the owner the deviation rule named | R-DEV-02; R-DEV-03 |
| BR11 | The TRANSFER version in force on the business date decides the move, and the decision log records the rule ID and that package version; a case keeps the version it was moved under | D-RCV-36 T5, T7; R-UNI-38 |
| BR12 | No TRANSFER version in force is a refusal (NoPackageInForce), never a default decision | D-RCV-36 T3; R-UNI-41 |

## 9. State transitions

None. This story does not change a case status. It changes the case's queue, owner and team, ends one assignment and writes the next. The route state and the clocks stay as they were (R-UNI-18, R-UNI-46).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager | Transfers and reassigns cases in the team's scope (Queue and allocation CRUA) |
| RW-CAPACITY, capacity and workforce planner | Reassigns cases for capacity (Queue and allocation RU, scope All) |
| SY-CASEWF, case workflow module | Writes the assignment and updates the case (Queue and allocation CRU) |
| SY-RULES, Drools evaluator | Evaluates the TRANSFER package and returns the rule ID and the package version |
| SY-DECLOG, decision log writer | Writes the entry (Decision log C) |
| RW-CASEOWN, case owner | Reads the result only (Queue and allocation R); cannot transfer |

No approval level from the delegation of authority applies: a transfer moves work, not money.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-007 | recovery_case | route_state | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Write |
| DF-CAS-010 | recovery_case | queue_id | Write |
| DF-CAS-011 | recovery_case | team_code | Write |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-CAS-020 | recovery_case | legal_hold | Read |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-006 | queue | assignment_method | Read |
| DF-WRK-007 | queue | capacity_cap | Read |
| DF-WRK-009 to DF-WRK-016 | assignment | all fields | Write |
| DF-WRK-039 | assignment | queue_id | Write |
| DF-WRK-040 | assignment | transfer_reason_code | Write |
| DF-REF-002 | rule_row | rule_id | Read, through RuleEvaluator |
| DF-REF-281 | rule_package_version | version_label | Read, through RuleEvaluator |
| DF-REF-282 | rule_package_version | status | Read, through RuleEvaluator |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through the P7 interface |

The rule row is read only through RuleEvaluator; this story reads no workbook, no drl_source and no rule_row row directly. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/cases/{caseId}/transfer** (P3; the endpoint and payload of RWB-E1-021, unchanged)

| Item | Value |
|---|---|
| Request | Header `Idempotency-Key` (uuid, required). Body `TransferRequest`: `toQueueId` or `toOwnerId` (one required), `reasonCode` (TRANSFER for a queue move, MANUAL for a reassignment), `transferReasonCode` (new, LOV-TRANSFER-REASON, required), `note` (max 500) |
| Response | 200 `Assignment`: `id`, `caseId`, `assigneeUserId`, `assignedAt`, `reason`, `ruleId` |
| Errors | 401 (MSG-P4-001); 403 no Queue and allocation U (MSG-P4-002); 404 case unknown or out of scope (MSG-P4-003); 409 case closed or held (MSG-P3-005), rule refuses (MSG-P3-033), record changed (MSG-GEN-004); 422 no reason (MSG-P3-001), owner at cap (MSG-P3-002), no package in force (MSG-P3-027); 503 decision log write failed (MSG-P7-003) |
| Authorization | Queue and allocation, right U, scope applied |
| Idempotency | `Idempotency-Key` header, kept 24 hours. A repeat returns the stored response |

**GET /api/recovery/v1/cases/{caseId}** (P3) reads the case after the move (Case record R).

**Published interfaces used**

```java
// P3, RWB-E1-020
Optional<UUID> AssignmentEngine.pickOwner(UUID queueId, UUID caseId, LocalDate businessDate);
// P3, published in RWB-E1-072 (recovery.casewf.rules)
RuleResult RuleEvaluator.evaluate(String packageCode, Object facts, LocalDate onDate); // throws NoPackageInForce
// P7, RWB-E1-027
UUID DecisionLogWriter.record(DecisionLogEntryCommand command);
```

`RuleResult` carries packageCode, packageVersion, ruleId and outputs (RWB-E1-072). The rule ID shown with MSG-P3-033 is `RuleResult.ruleId`; the rule version written to the decision log is `RuleResult.packageVersion`. No caller receives a KieBase, a KieSession or a Drools type.

**Events.** CaseTransferred (EV-04) published with caseId, fromOwner, toOwner, reasonCode, ruleId, in the same transaction as the change.

## 13. Solution plan

**Package.** `recovery.casewf.transfer` in the recovery module; front end folder `src/modules/recovery/casewf/transfer`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseAndWorkflowController | Controller | `POST /api/recovery/v1/cases/{caseId}/transfer`; idempotency; problem responses |
| ManualTransferService | Service | Checks, RuleEvaluator call, owner pick, decision log write, then the transaction |
| TransferFactsBuilder | Service | Builds the TransferFacts of the case, the target queue or owner, the reason code and the business date |
| IdempotencyStore | Repository | Stores the key, the request hash and the response for 24 hours |
| AssignmentRepository | Repository | Ends the current assignment and writes the new one |
| OwnerLoadRepository | Repository | Counts open cases per owner in a queue for the cap check |
| TransferCasePage | React component | SCR-05 with the Form, At cap warning and Saved states, single and bulk |
| BulkTransferRunner | React component | Sends one request per selected case in sequence and collects the results |

**Database.** Migration `V<next>__rwb_e2_012_assignment_reason.sql` adds `assignment.queue_id uuid REFERENCES queue (id)` and `assignment.transfer_reason_code varchar(10)`, index `ix_assignment_case_open` on `(case_id) WHERE ended_at IS NULL`, and the idempotency table `idempotency_key (key uuid PK, endpoint varchar(100), request_hash char(64), response jsonb, created_at timestamptz)`. The case update uses the optimistic lock column `recovery_case.version`. No table holds a transfer rule; the rules are rows of the TRANSFER package (RWB-E1-072, RWB-E1-073).

**Configuration and reference data.** LOV-TRANSFER-REASON values (center of excellence; DL23). `transfer.bulk.max` = 50 (assumed; DL23). The TRANSFER package rows are authored and loaded by RW-COE through RWB-E1-073; this story loads none. Queue caps (DL23).

**Build steps**

1. Write the migration and extend the assignment entity.
2. Build `IdempotencyStore` and the header handling in the controller.
3. Build `TransferFactsBuilder` and `ManualTransferService` checks in this order: reason, case state and hold, scope, `RuleEvaluator.evaluate("TRANSFER", facts, businessDate)`, owner pick or cap check, team check for R04.
4. Map `NoPackageInForce` to 422 with MSG-P3-027 and a refusal result to 409 with MSG-P3-033 carrying the rule ID.
5. Add the decision log write with the rule ID and the package version before the transaction; map its failure to 503 with MSG-P7-003.
6. Write the transaction: end assignment, new assignment, case update with the version check, outbox row.
7. Build `TransferCasePage` with its three states and `BulkTransferRunner` with the per-row result and the MSG-P3-035 summary.
8. Write the tests in section 16, including two parallel requests and the refusal of AC2.

**Feature flag.** `rwb.p3.manual-transfer`. Off: SCR-05 is hidden and the endpoint returns 403 for every role except SY-CASEWF. The rule evaluation is also behind `rwb.p3.drools` (RWB-E1-072); with that flag off the transfer endpoint refuses every move with MSG-P3-027.

**Done when.** The tests in section 16 pass, and a transfer made in SIT shows on the case timeline queue history (RWB-E2-016) with the rule ID and the package version on its decision log entry.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-001 | No reason code | Choose a reason for the transfer. |
| MSG-P3-002 | Target owner, or every owner of the target queue, at the cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-005 | Case closed or under a legal hold | This case cannot move to {state} from {current}. |
| MSG-P3-027 | No TRANSFER package version in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P3-033 | A TRANSFER rule refuses the move | Rule {rule} does not allow this transfer. |
| MSG-P3-035 | Bulk move with refusals | {done} of {total} cases were moved. The others show the reason on their row. |
| MSG-GEN-004 | Two moves of one case at once | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-005 | Move saved | Saved. |
| MSG-P4-002 | A role without Queue and allocation U | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 in this story {check} is "package in force" and {detail} names the package code TRANSFER and the business date only. MSG-P3-033 and MSG-P3-035 are new (see Additions); the {rule} value is the rule ID from RuleEvaluator. Thai text follows DL10.

## 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-05 Transfer case | Form | Chooses a queue or an owner, a reason code and a note; confirms |
| SCR-05 Transfer case | At cap warning | Reads MSG-P3-002; chooses another owner or the team queue |
| SCR-05 Transfer case | Refused | Reads MSG-P3-033 with the rule ID, or MSG-P3-027 when no TRANSFER version is in force |
| SCR-05 Transfer case | Saved | Reads MSG-GEN-005, or the per-case results and MSG-P3-035 for a bulk move |
| SCR-07 Team queues | List | Selects up to 50 cases and opens SCR-05 for them |
| SCR-09 Exception queue | List | Not used by this story; a refused move is not queued |

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-012-01 | AC1, BR1, BR3, BR6, BR11 | System | RW-2026-000401 to LIT-BKK-01, reason R02, TRANSFER version TRF-2026.12 |
| TC-E2-012-02 | AC2, BR2, BR10 | System | RW-2026-000402 with X1 open under R-DEV-02; row TRF-010 refuses |
| TC-E2-012-03 | AC3, BR4, BR5, BR11 | System | Ten cases to U-CO-03 with 60 open cases, reason R04 |
| TC-E2-012-04 | AC4, BR1 | System | Request with no reason code |
| TC-E2-012-05 | AC5, BR4 | System | U-CO-04 at 150 of 150 |
| TC-E2-012-06 | AC6, BR5 | System | U-CO-09 in team SME-NTH, reason R04 |
| TC-E2-012-07 | AC7, BR7 | System | RW-2026-000403 with legal hold true |
| TC-E2-012-08 | AC8 | System | Two parallel requests for one case |
| TC-E2-012-09 | AC9, BR9 | System | Same Idempotency-Key twice |
| TC-E2-012-10 | AC10, BR8 | System | Decision log store stopped |
| TC-E2-012-11 | AC11 | System | Ten cases, two under a legal hold |
| TC-E2-012-12 | AC12, BR4 | System | Both LIT-BKK-01 owners at 150 |
| TC-E2-012-13 | Access | Access | RW-CASEOWN (Queue and allocation R) calls the transfer endpoint; refused with MSG-P4-002 |
| TC-E2-012-14 | Principle 5 | Resilience | Decision log write forced to fail; case, assignment and outbox unchanged |
| TC-E2-012-15 | AC13, BR12 | System | No TRANSFER version in force on 2026-12-20; NoPackageInForce and MSG-P3-027 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: reason codes, caps, the bulk limit and the transfer rows are data.
- No personal data in logs, tests, workflow history or prompts: the note field is not logged, and events carry IDs and codes only.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: the decision log is written through the P7 interface, and deviation ownership comes from the TRANSFER package and the case flag.
- The decision log entry is written before the case changes; a failed write leaves the case as it was.
- Each case in a bulk move is its own request, its own rule evaluation and its own transaction.
- No second rule engine: the transfer rules are read only through RuleEvaluator, and no caller reads the workbook, drl_source or rule_row.
- The endpoint, the request and the response are those of RWB-E1-021; this story adds no field to the API.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-003 | Manual transfer or reassignment only with a reason code from the agreed list | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-03 | All recovery processes | R-DEV-02, R-UNI-20, R-UNI-39, R-UNI-40 | TC-E2-012-01, TC-E2-012-02, TC-E2-012-04, TC-E2-012-07 to TC-E2-012-10, TC-E2-012-13, TC-E2-012-14, TC-E2-012-15 |
| REQ-WKM-007 | An absent or over-cap owner's cases reallocated inside the team, keeping state and clocks | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-WKM-04, FEAT-WKM-10 | All recovery processes | R-UNI-18, R-UNI-46 | TC-E2-012-03, TC-E2-012-05, TC-E2-012-06, TC-E2-012-11, TC-E2-012-12 |
| REQ-WKM-008 | Queue and transfer history visible on the case | Business Requirements Epic 2, section 4; Program, section 5.3 | FEAT-WKM-03 | All recovery processes | R-UNI-18 | TC-E2-012-01, TC-E2-012-03 |

The rule ID and the package version on the decision log entry satisfy REQ-CWC-016 through RWB-E1-072; this story adds no requirement ID of its own.

## 19. Out of scope

- Automatic reallocation when an owner is absent or over the cap (R-UNI-18 and R-UNI-19, JOB-06 Daily rebalancing, RWB-E1-030).
- The queue history view on the case (RWB-E2-016).
- Rule-driven transfers on stage change, route decision and timer expiry (RWB-E1-021).
- The TRANSFER package rows themselves, their scenarios and their approval (RWB-E1-073).
- Partner placement and recall (Epic 6).
