# RWB-ITG-E2041-ITG Rule change governance and audit report

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-041 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E2041-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 15 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2041-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-041 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP08, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E2041-ITG-16); the squad sizes at refinement. Small: fits within two weeks |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E2041-CON, RWB-P7-E1073-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P4-E1037-CON |
| Integration dependencies | RWB-P3-E2041-APP, RWB-P4-E2041-APP, RWB-P7-E2041-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-016, FR-PLT-017, FR-PLT-018, FR-PLT-020) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness that loads a rule package version with its change checklist, has it approved by a second user, and reads the change report across rwb-decision, rwb-case and rwb-access**, so that **the wave 2 rule change governance and audit report journey is proven end to end, with evidence, before the release is accepted**.

This story builds the harness and the evidence only. It builds no production screen, endpoint, table, workflow or schedule, it serves no operation, it owns no table and it starts no workflow. The real behaviour is owned by the I stories RWB-P7-E2041-APP (the change checklist on the package version, the approval checks, the effect counts and the change report in rwb-decision), RWB-P3-E2041-APP (the case facts and the open case count the impact summary is read against) and RWB-P4-E2041-APP (the Rules and parameters right answered on every call), and those three stories block the ITG run. The screen states of SCR-39 in RWB-P3-E2041-APP are not built here: the harness asserts the empty list (ITG AC3, X6), the 403 no-access refusal (X5) and the 503 error (X8); loading is not asserted.

### 2. Business rationale

The legacy RWB-E2-041 journey crosses more than one service: rwb-decision holds the rule package, its versions, the change checklist, the rule rows, the central decision ledger and the change report; rwb-case holds the case facts and the open case count the impact summary speaks about; and rwb-access answers the Rules and parameters right on every call. Until the real services are exercised together, the program cannot show that a rule change is as controlled as a code change, which is the outcome the program targets at 5 days from 23 days.

The harness gives one repeatable run per business date that proves a version is loaded with its checklist and approved by a user other than its author, that the report shows the request, the impact, the test result, the author, the approver, the approved time, the valid from date, the checksum, the effect counts and the decisions per package version, that the decision counts reconcile with the decision log, that the CSV export and a period with no changes answer correctly, and that a refusal writes nothing. It meets REQ-CWC-013 and REQ-DRI-011 at the integration level and leaves every business rule, every message and every screen behaviour where the owning stories put them.

### 3. Preconditions

- The three I stories are published and deployed in the SIT environment: RWB-P7-E2041-APP (the checklist, the approval checks, the effect counts and the change report), RWB-P3-E2041-APP (the case facts and the open case count) and RWB-P4-E2041-APP (the Rules and parameters right on the authorise operation).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness can run green from Day 1 before the I stories land.
- Package ALLOCATION version "ALLOC-2026.11" is seeded in force with 24 rows, loaded by "U-41" and approved by "U-51"; the users "U-41" (RW-COE), "U-51" (RW-RISK) and "U-AUD-01" (RW-AUDIT) are seeded through the access contract.
- The decision log holds 96 entries with package version "ALLOC-2026.11" and 1,204 with "ALLOC-2026.12" for December 2026, seeded through the owning contract or the published fake.
- The production switch `rwb.p3.rule-change-report` is on in the harness environment; with it off the report operation answers 404 and the approval runs the earlier package-version checks only.
- The harness environment, its test-data seeding, its evidence format and retention, and the gateway-bff composite route detail used for any gateway call: Not specified in the source documents (GAP-0420; ASM-0595).

### 4. Flow

1. Harness: seeds ALLOCATION version "ALLOC-2026.11" in force with 24 rows, the three users, their roles and the decision log counts of December 2026 through the owning contracts or the published fakes, and reads the version back to assert the seeded state.
2. Harness: loads ALLOCATION version "ALLOC-2026.12" with the checklist request "CR-2026-0042", impact summary "412 open Mortgage cases in the BKK queue", verify note and verify date 2026-12-08, rollback plan "Roll back to ALLOC-2026.11" and valid from 2026-12-10, and asserts the load checks and the 50 scenarios pass.
3. Harness: approves "ALLOC-2026.12" as "U-51" on 2026-12-09 and asserts that the approver is not the author "U-41".
4. Harness: reads the change report for 2026-12-01 to 2026-12-31 as "U-AUD-01" and asserts the entry fields of AC2, including the checksum "9f2c...e1b4" and the effect counts of 1 row changed, 0 added and 0 removed against "ALLOC-2026.11".
5. Harness: asserts the decisions per package version, 96 for "ALLOC-2026.11" and 1,204 for "ALLOC-2026.12", and the decisions per rule ID "ALLOC-031" 700 and "ALLOC-032" 600, and reconciles the total with GET /api/recovery/decision/v1/decision-log for the same period and package version.
6. Harness: reads the impact summary count of 412 open cases against GET /api/recovery/case/v1/queues/{queueId}/cases in rwb-case, and asserts the Rules and parameters right was answered by POST /api/recovery/access/v1/authorise with one hop and the 2 s budget for every call of the run.
7. Harness: reads the same report with format "csv" and asserts one header row and one row per package version, with no party identifier and no case data, then reads 2026-11-01 to 2026-11-15 and asserts an empty list with total 0.
8. Harness: forces each refusal and failure of §5 through the fakes, asserts the message and that nothing was written, then returns the fake to its healthy answer.
9. Harness: writes one run report per business date, keyed by story and business date, with the trace of every call; the report format and retention are Not specified in the source documents (GAP-0420; ASM-0595).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | Approval with a checklist item missing (RES-2026.12 with no rollback plan) | The approval is refused and version "RES-2026.12" stays "LOADED"; no approver and no approved time is written | MSG-P3-022 | TC-E2-041-03-ITG | ITG AC4 |
| X2 | Approval of a version whose test result is FAILED (PMT-2026.12, 2 of 58 scenarios failing) | The approval is refused; no approver and no approved time is written | MSG-P3-022 | TC-E2-041-04-ITG | ITG AC4 |
| X3 | The verify date is before the load time (ALLOC-2026.14, verify 2026-12-07, load 2026-12-08) | The load is refused and no version row is written | MSG-GEN-003 | TC-E2-041-07-ITG | ITG AC4 |
| X4 | The report period ends before it starts | The call is refused; nothing is read from the sources and nothing is written | MSG-GEN-003 | TC-E2-041-08-ITG | ITG AC4 |
| X5 | A role without Rules and parameters R reads the report | 403 on the direct call; the answer carries the refusal and not an empty list | MSG-P4-002 | TC-E2-041-11-ITG | ITG AC4 |
| X6 | The report period has no changes | An empty list with total 0 and no error | None | TC-E2-041-06-ITG | ITG AC3 |
| X7 | A version reaches its valid from date with no approver | It is not served; the report shows the version with status "LOADED" and the approver empty | None | TC-E2-041-02-ITG | ITG AC2 |
| X8 | rwb-decision does not answer the decision log read | 503 for the report; no entry is written and the run raises the incident assertion, then the repeat after recovery answers | None | TC-E2-041-10-ITG | ITG AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the three I stories are deployed; until then it runs against the §12.8 fakes |
| Negotiable | The harness pack, the data seeding and the evidence format are agreed with QA; no business value is fixed by the harness |
| Valuable | The rule change is evidenced across services rather than per service, and the decisions per version reconcile from one source |
| Estimable | One harness project, one journey specification, one fake pack and one run report |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each scenario of §7 is one automated journey with synthetic data and a machine-checkable result |

### 7. Acceptance criteria

```gherkin
Feature: Rule change governance and audit report - wave 2 integration harness

  Background:
    Given the business date is 2026-12-01
    Given package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows
    Given user "U-41" holds RW-COE, "U-51" holds RW-RISK and "U-AUD-01" holds RW-AUDIT

  Scenario: AC1 A version loaded with its checklist and approved by a different user, then read through the change report (new, D-RCV-60)
    Given "U-41" loads ALLOCATION version "ALLOC-2026.12" with the checklist request "CR-2026-0042", impact summary "412 open Mortgage cases in the BKK queue", verify note "SIT run 2026-12-08: 50 of 50 scenarios pass and the dry run covers 412 open cases", verify date 2026-12-08 and rollback plan "Roll back to ALLOC-2026.11", valid from 2026-12-10
    And the load checks and the 50 scenarios pass
    When "U-51" approves version "ALLOC-2026.12" on 2026-12-09
    Then "U-AUD-01" reads GET /api/recovery/decision/v1/admin/rule-packages/change-report for 2026-12-01 to 2026-12-31 and one entry shows request "CR-2026-0042", author "U-41", approver "U-51", approved on 2026-12-09 and valid from 2026-12-10
    And the impact summary count of 412 open cases reconciles with the 412 open Mortgage cases returned by GET /api/recovery/case/v1/queues/{queueId}/cases in rwb-case
    And the Rules and parameters right of the reader is answered by POST /api/recovery/access/v1/authorise in rwb-access
    And every call in the run is one hop with the 2 s budget and a breaker per downstream
    And no service reads another service's schema
    And the run report holds one trace spanning rwb-decision, rwb-case and rwb-access

  Scenario: AC2 The report fields and the decisions per package version, reconciled with the decision log (new, D-RCV-60)
    Given ALLOCATION version "ALLOC-2026.11" was in force until 2026-12-09 and "ALLOC-2026.12" from 2026-12-10
    Given the decision log holds 96 entries with package version "ALLOC-2026.11" and 1,204 with "ALLOC-2026.12" in December 2026
    When "U-AUD-01" reads the change report for 2026-12-01 to 2026-12-31
    Then the entry for "ALLOC-2026.12" shows request "CR-2026-0042", the impact summary, test result "PASSED", author "U-41", approver "U-51", approved time 2026-12-09, valid from 2026-12-10 and checksum "9f2c...e1b4"
    And the entry shows 1 row changed, 0 added and 0 removed against "ALLOC-2026.11"
    And the approval time is before the valid from date
    And version "ALLOC-2026.11" shows 96 decisions and version "ALLOC-2026.12" shows 1,204
    And the entry shows the decisions per rule ID across both versions: "ALLOC-031" 700 and "ALLOC-032" 600 (ALLOC-032 is test data; the ID is in no current source)
    And the total matches GET /api/recovery/decision/v1/decision-log for the same period and package version

  Scenario: AC3 CSV export and a period with no changes (new, D-RCV-60)
    When "U-AUD-01" reads the change report for 2026-12-01 to 2026-12-31 with format "csv"
    Then the response is a CSV file with one header row and one row per package version
    And it carries no party identifier and no case data
    When "U-AUD-01" reads the change report for 2026-11-01 to 2026-11-15
    Then the response is an empty list with total 0

  Scenario: AC4 Refusals and failure isolation (new, D-RCV-60)
    Given RESTRUCTURE version "RES-2026.12" is loaded with no rollback plan
    When "U-51" approves it
    Then the system refuses the approval with MSG-P3-022 naming "rollback plan"
    And version "RES-2026.12" stays "LOADED"
    Given PAYMENT_MATCH version "PMT-2026.12" whose scenario result is "FAILED" with 2 of 58 scenarios failing
    When "U-51" approves it
    Then the system refuses the approval with MSG-P3-022 naming "test result"
    Given ALLOCATION version "ALLOC-2026.14" with verify date 2026-12-07 and load time 2026-12-08
    When "U-41" loads it
    Then the system refuses the load with MSG-GEN-003 naming "verifiedAt" and "loadedAt"
    When "U-AUD-01" reads the change report from 2026-12-31 to 2026-12-01
    Then the system refuses the call with MSG-GEN-003 naming "to" and "from"
    When the harness repeats each call of this scenario as "RW-CASEOWN", a role with no Rules and parameters right
    Then every call is refused with 403 and MSG-P4-002
    And no package version row, no checklist value and no decision log entry is written by any refused call
    And the report for 2026-12-01 to 2026-12-31 is unchanged after the refusals

  Scenario: AC5 A rollback appears as its own entry naming the version it returns to (new, D-RCV-60)
    Given ALLOCATION version "ALLOC-2026.12" is rolled back to "ALLOC-2026.11"
    When "U-AUD-01" reads the change report for 2026-12-01 to 2026-12-31
    Then one entry shows the rollback of "ALLOC-2026.12" and names "ALLOC-2026.11" as the version it returns to

  Scenario: AC6 The approver differs from the author and the checklist sits on the version row (new, D-RCV-60)
    Given "U-41" is the author of ALLOCATION version "ALLOC-2026.12"
    When "U-51" approves version "ALLOC-2026.12"
    Then the approver "U-51" differs from the author "U-41"
    And the checklist is one JSON object on the package version row and no table or column is added

  Scenario: AC7 A consumed call that fails or does not answer is isolated from the report (new, D-RCV-60)
    Given "U-AUD-01" reads the change report for 2026-12-01 to 2026-12-31
    When the call to GET /api/recovery/case/v1/queues/{queueId}/cases in rwb-case fails or does not answer within the 2 s budget
    Then the failure response code is Not specified in the source documents (NEWAC-RWB-ITG-E2041-ITG-AC12)
    And no package version row, no checklist value and no decision log entry is changed by the failed call
```

These seven criteria are new for the ITG harness and do not restate the app criteria owned by the I stories.

Scope: rule package versions only. The reference-data change checklist and its report stay with RWB-E1-043 and are not covered here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A package version can be approved only when it carries a change request reference, an impact summary, a verify record, a rollback plan and a test result of PASSED | CTL-08; rule package change process steps 1 to 4 |
| BR2 | The approver is not the author | roles.txt Separation of duty; CTL-08 |
| BR3 | A version that is not approved never takes effect | R-UNI-38; REQ-CWC-013 |
| BR4 | The verify item is dated on or after the load and before the approval | rule package change process step 6 |
| BR5 | The report lists every package version whose load, approval, valid from, verification or rollback falls in the period | REQ-DRI-011 |
| BR6 | The effect of a version is the count of rows added, changed and removed against the version it replaces, by Drools rule name and row order, and the rule IDs changed | D-RCV-36 T4, T5; ADR-012 |
| BR7 | A rollback appears as its own entry naming the version it returns to | REQ-CWC-013; R-UNI-38 |
| BR8 | The decisions per package version are counted from decision_log_entry rule_id and rule_version; the report never recomputes a decision | REQ-DRI-011; D-RCV-36 T5 |
| BR9 | The checklist is one JSON object on the package version row; this journey adds no table and no column | D-RCV-36 T4; RWB-E1-072 |

The harness asserts these nine rules against the owning services and re-implements none of them, so no BR row is changed by this story.

### 9. State transitions

None. The harness changes no case status and no package version state; it calls the owning service and reads the result. The table is what it observes on the package version after a call to the owning service.

| Observed on the package version | Before the call | After a successful call | After a refusal |
|---|---|---|---|
| status | LOADED | APPROVED, then IN_FORCE on the valid from date with the previous version SUPERSEDED | LOADED or APPROVED (unchanged) |
| author, approver | U-41, empty | U-41, U-51 | unchanged |
| approved time, valid from | empty, 2026-12-10 | 2026-12-09, 2026-12-10 | unchanged |
| change checklist | the seven items of §1 | unchanged | unchanged |
| decision log entries for the version | 96 for "ALLOC-2026.11" | 1,204 for "ALLOC-2026.12" after the period closes | unchanged |

A refused approval or a refused report leaves every row exactly as it was before the call, and a rollback appears as a further entry that names the version it returns to.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | The synthetic user the harness drives to load a version with its checklist (Rules and parameters CRUD) |
| RW-RISK, risk and model risk officer | Approves a package version (Rules and parameters A); the harness asserts that the approver is not the author |
| RW-AUDIT, internal audit | Reads and exports the change report (Rules and parameters R); changes nothing |
| RW-PLATADM, platform administrator | Reads the report (Rules and parameters R); used by the access case only |
| RW-CASEOWN, case owner | Holds no Rules and parameters right; the access case proves the refusal with MSG-P4-002 |
| SY-RULES, Drools evaluator | Evaluates the version in force and writes its rule ID and version to the decision log; the harness asserts its result, it does not act for it |

No delegation of authority level applies: a package version is not a credit decision. Authorisation is answered by rwb-access through the authorise operation of §12.2.

### 11. Data

The harness owns no table. It reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through rwb-case contract |
| DF-CAS-005 | recovery_case | status | Read through rwb-case contract |
| DF-CAS-010 | recovery_case | queue_id | Read through rwb-case contract |
| DF-REF-274 | rule_package | id | Read through rwb-decision contract |
| DF-REF-275 | rule_package | package_code | Read through rwb-decision contract |
| DF-REF-276 | rule_package | title | Read through rwb-decision contract |
| DF-REF-279 | rule_package_version | id | Read through rwb-decision contract |
| DF-REF-281 | rule_package_version | version_label | Read through rwb-decision contract |
| DF-REF-282 | rule_package_version | status | Read through rwb-decision contract |
| DF-REF-285 | rule_package_version | checksum | Read through rwb-decision contract |
| DF-REF-286 | rule_package_version | valid_from | Read through rwb-decision contract |
| DF-REF-287 | rule_package_version | valid_to | Read through rwb-decision contract |
| DF-REF-288 | rule_package_version | author | Read through rwb-decision contract |
| DF-REF-289 | rule_package_version | approver | Read through rwb-decision contract |
| DF-REF-290 | rule_package_version | loaded_at | Read through rwb-decision contract |
| DF-REF-291 | rule_package_version | approved_at | Read through rwb-decision contract |
| DF-REF-292 | rule_package_version | test_result | Read through rwb-decision contract |
| DF-REF-293 | rule_package_version | dry_run_counts | Read through rwb-decision contract |
| DF-REF-294 | rule_package_version | rollback_of | Read through rwb-decision contract |
| DF-REF-002 | rule_row | rule_id | Read through rwb-decision contract |
| DF-REF-296 | rule_row | package_version_id | Read through rwb-decision contract |
| DF-REF-297 | rule_row | drools_rule_name | Read through rwb-decision contract |
| DF-DEC-004 | decision_log_entry | rule_id | Read through rwb-decision contract |
| DF-DEC-005 | decision_log_entry | rule_version | Read through rwb-decision contract |
| DF-DEC-016 | decision_log_entry | decided_at | Read through rwb-decision contract |

Package titles (DF-REF-276) are the seeded values of rwb_decision: "Allocation rules" for ALLOCATION, "Restructure rules" for RESTRUCTURE and "Payment match rules" for PAYMENT_MATCH. DF-REF-293 holds, as integer values, the counts of open cases each changed row would move, from the dry run; the keys of that breakdown are Not specified in the source documents (GAP-1302). The body of the rollback answer beyond the two version states is Not specified in the source documents (GAP-1302). For these two unspecified points the harness asserts presence and stability only, never an invented business number.

The change checklist is part of the package version record and is read through the same contract; the harness holds no copy of it. Test data is synthetic. No production case, party or package version is copied, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness calls the owning services; it serves no operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

Contract version built against: API Specification v5, `rwb-decision.yaml` and `rwb-case.yaml`, each at version 5.0.0, and `rwb-access.yaml` at version 5.0.0. The authorise operation is not yet published in `rwb-access.yaml` (CG-ALL-791).

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/admin/rule-packages/change-report` | P7 rwb-decision | The change report for a period and a package, as JSON or CSV (Architecture v5 slide 27: audit of every version) |
| POST | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The package version load with its change checklist (Architecture v5 slide 27: author and test) |
| POST | `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/approve` | P7 rwb-decision | The four-eyes approval of a version (Architecture v5 slide 27: four-eyes sign-off) |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The version in force, its status and the rule rows the effect counts are read against |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The decisions per rule ID and package version the report is reconciled with (Architecture v5 slide 14: central decision ledger) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Rules and parameters right check used by every call (Architecture v5 slide 14: rwb-access IN POST /authorise) |
| GET | `/api/recovery/case/v1/queues/{queueId}/cases` | P3 rwb-case | The open case count of the queue the impact summary names |

The composite screen route itself is gateway-bff (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order, and any gateway call this run makes, are Not specified in the source documents (GAP-0420; ASM-0595).

#### 12.3 Events published

None. The harness produces no event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | P7 rwb-decision | One event on the valid from date, at 00:01, naming the package and the version, and the version in force in each owning service changes only after it |
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 rwb-decision (ledger); every service publishes its own record | The 96 and the 1,204 records of December 2026 reach the ledger with rule ID and package version, and the report count matches the ledger query |

The two events are consumed for assertion only; the harness reads the ledger through the P7 contract rather than from a topic.

#### 12.5 Workflows and activities

None added. The harness starts no workflow and adds no activity; it drives REST only. The rule promotion at 00:01 and the chain check at 02:00 in rwb-decision are owned and started by the owning services.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow.

#### 12.7 Tables owned

None.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-decision | change-report, rule-packages/{packageCode}/versions, rule-package-versions/{versionId}/approve, decision-log | ALLOCATION "ALLOC-2026.11" in force with 24 rows loaded by U-41 and approved by U-51; "ALLOC-2026.12" load with the checklist and approval by U-51; "ALLOC-2026.13" loaded and never approved; RESTRUCTURE "RES-2026.12" with no rollback plan; PAYMENT_MATCH "PMT-2026.12" with test result FAILED, 2 of 58 scenarios failing; "ALLOC-2026.14" with verify date before the load; checksum "9f2c...e1b4"; 1 row changed, 0 added, 0 removed; 96 and 1,204 decisions, "ALLOC-031" 700 and "ALLOC-032" 600; a CSV answer; an empty answer with total 0; 409 for MSG-P3-022, 422 for MSG-GEN-003 naming "to" and "from" or "verifiedAt" and "loadedAt", and a forced failure for the 503 case |
| rwb-case | queues/{queueId}/cases | 412 open Mortgage cases in queue "MTG-BKK-CO" on 2026-12-01 |
| rwb-access | authorise | Allow RW-COE, RW-RISK and RW-AUDIT with Rules and parameters R, CRUD, A and R; refuse RW-CASEOWN for Rules and parameters with MSG-P4-002 |

The fakes are replaced by the real service as each I story lands, contract by contract. The harness repository, its environment and seeding, its evidence format and retention, and the composite route detail: Not specified in the source documents (GAP-0420; ASM-0595).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Seven consumed operations of §12.2 through the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes rwb.decision.RulePackageInForce.v1 and rwb.decision.DecisionRecorded.v1 for the in-force and ledger assertions; publishes nothing |
| Temporal | No | Starts no workflow and adds no activity or Nexus operation; it observes the 00:01 promotion and the 02:00 chain check |
| File | No | The CSV answer is a REST response read as text and compared row by row; the harness writes no file to a service |

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
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
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
| ChangeReportClient | Harness adapter | Calls the seven consumed operations of §12.2 for the load, the approval, the version read, the report in JSON and CSV and the decision log |
| FakePack | WireMock project | Serves rwb-decision, rwb-case and rwb-access from the published OpenAPI documents of §12.8 |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema reference found in the trace, so a service never reads another service's tables |
| FourEyesCheck | Assertion | Fails the run when the approver equals the author, or when a refused approval writes an approver or an approved time |
| DecisionCountReconciler | Assertion | Compares the decisions per package version and per rule ID with the decision log query for the same period and fails the run on any difference |
| RunReportWriter | Reporter | Writes one run report with the trace and the per-assertion result; format and retention Not specified in the source documents (GAP-0420; ASM-0595) |

**Environment and test data**

- Environment: SIT, one namespace, the three I stories deployed from their wave 2 builds or replaced by the §12.8 fakes. Harness repository, environment and data seeding: Not specified in the source documents (GAP-0420; ASM-0595).
- Data: the package ALLOCATION with versions "ALLOC-2026.11" in force with 24 rows and "ALLOC-2026.12" loaded and approved, plus "ALLOC-2026.13" loaded and never approved and "ALLOC-2026.14" with a verify date before the load; RESTRUCTURE "RES-2026.12"; PAYMENT_MATCH "PMT-2026.12"; request "CR-2026-0042"; users "U-41", "U-51" and "U-AUD-01"; the 96 and 1,204 decision log entries; the business date 2026-12-01 and the period 2026-12-01 to 2026-12-31.
- Reset: each run starts from the seeded state, so a repeated run is deterministic and the same report is produced. The seeding order and the seeding script: Not specified in the source documents (GAP-0420; ASM-0595).

**Build steps**

1. Build JourneyRunner and ChangeReportClient against the published OpenAPI documents of the owning services.
2. Publish FakePack for the three services from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Add the load, the approval and the report read of AC1 with FourEyesCheck, the case count and the authorise call, the one-hop check and the 2 s per-call budget.
4. Add the report fields, the effect counts, the decisions per version and per rule ID and the decision log reconciliation of AC2 with DecisionCountReconciler.
5. Add the CSV export and the empty period of AC3, asserting one header row, one row per version and no party or case data.
6. Add the refusals of AC4 for a missing checklist item, a FAILED test result, a verify date before the load, a period end before the start and a role without Rules and parameters right, and assert that nothing was written.
7. Add the decision log failure of X8, replace each fake with the real service as its I story lands, then publish the run report per business date and the pass/fail gate; the gate definition: Not specified in the source documents (GAP-0420; ASM-0595).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switch it exercises is `rwb.p3.rule-change-report` from the legacy solution plan; with the flag off the report operation answers 404 and the approval runs the earlier package-version checks only, and the harness asserts the disabled and the enabled state.

**Done when:** the journey runs green against the three deployed I stories in SIT, the run report for the business date holds every assertion of §7 and §16 with its trace, the decisions per package version reconcile with the decision log, and the pass/fail gate agreed with QA is met for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-022 | Approval with a missing checklist item or a FAILED test result | The change cannot be approved: {item} is missing or failed. |
| MSG-GEN-003 | Verify date before the load, or a report period in the wrong order | {field} cannot be before {other}. |
| MSG-GEN-001 | A required checklist value is empty | Enter {field}. |
| MSG-P7-002 | The author approves their own version | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | A role without the right reads the report | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values, including "rollback plan" and "test result" in MSG-P3-022, and "verifiedAt", "loadedAt", "to" and "from" in MSG-GEN-003; it does not own the message text. Thai text for each message follows decision DL10. DL10 is still open in the decision log; this story is built on its recommended answer: the business lead drafts per module one epic ahead, and Legal and Compliance approve (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863). The harness asserts message IDs and substituted values, so DL10 does not block it.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-39 Rules and parameters | Report list | The report answer the screen consumes: the entry fields of AC2 for the period, with the checksum, the effect counts and the decisions per package version |
| SCR-39 Rules and parameters | Export | The CSV answer holds one header row and one row per package version, with no party identifier and no case data |
| SCR-39 Rules and parameters | No changes in the period | The answer is an empty list with total 0 and no error |
| SCR-39 Rules and parameters | Empty | An empty list with total 0 and no error, as in the no-changes row above (X6) |
| SCR-39 Rules and parameters | Loading | Not specified in the source documents (CG-ALL-796) |
| SCR-39 Rules and parameters | Error | 503 for the report when rwb-decision does not answer the decision log read; no entry is written (X8) |
| SCR-39 Rules and parameters | No access | 403 on the direct call with MSG-P4-002; the answer carries the refusal and not an empty list (X5) |

The harness opens no screen and renders no page; it asserts the answer the screen consumes. Screen-level behaviour remains with the owning APP stories. The harness environment, seeding, evidence format, retention, pass/fail gate and gateway-bff composite route are held as data in the harness pack and agreed with QA and the integration lead at the wave 2 entry check; the values are not in this story. Not specified in the source documents (GAP-0420; ASM-0595). Report field shapes, CSV column order, the rulesChanged element, the decision-code and item-list values and the DP-02 login name are agreed at the wave 2 contract review of RWB-P3-E2041-CON; until then the build uses the confirmed assumptions of GAP-2413.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-041-11-ITG | Access; ITG AC4 | Component | RW-CASEOWN (no Rules and parameters right) reads the change report; refused with MSG-P4-002 |
| TC-E2-041-01-ITG | AC1, BR1, BR5, BR6; ITG AC1, ITG AC2 | Integration | ALLOCATION v11 to v12, request CR-2026-0042, one changed row |
| TC-E2-041-02-ITG | AC2, BR3; ITG AC1 | Integration | ALLOCATION v13 loaded and never approved |
| TC-E2-041-03-ITG | AC3, BR1; ITG AC4 | Integration | RESTRUCTURE v12 with no rollback plan |
| TC-E2-041-04-ITG | AC4, BR1; ITG AC4 | Integration | PAYMENT_MATCH v12 with a FAILED scenario result |
| TC-E2-041-05-ITG | AC5, BR1, BR4; ITG AC2 | Integration | Verify date 2026-12-08, approval 2026-12-09 |
| TC-E2-041-06-ITG | AC6; ITG AC3 | Integration | Period 2026-11-01 to 2026-11-15 with no versions |
| TC-E2-041-07-ITG | AC7, BR4; ITG AC4 | Integration | Verify date one day before the load |
| TC-E2-041-08-ITG | AC8; ITG AC4 | Integration | Period end before start |
| TC-E2-041-09-ITG | AC9; ITG AC3 | Integration | CSV export of December versions |
| TC-E2-041-10-ITG | AC10, BR8; ITG AC2 | Integration | 96 and 1,204 decisions in December 2026 |
| TC-E2-041-12-ITG | BR2; ITG AC6 | Integration | ALLOCATION v12 approved by U-51 with author U-41; the approver differs from the author |
| TC-E2-041-13-ITG | BR7; ITG AC5 | Integration | ALLOCATION v12 rolled back to ALLOCATION v11; one rollback entry naming v11 in the December report |
| TC-E2-041-14-ITG | BR9; ITG AC6 | Integration | ALLOCATION v12 with its checklist; the checklist is one JSON object on the version row and no table or column is added |
| TC-E2-041-15-ITG | ITG AC7 | Integration | Call to rwb-case queue cases fails or does not answer within the 2 s budget |

The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case ID. The Covers column names the legacy AC of RWB-E2-041 that the ITG copy is derived from and the criterion of §7 it asserts at integration level; the Level column maps the legacy System level to Integration and the legacy Access level to Component.

### 17. Guardrails

- No business value in code: the checklist items, the impact summary, the rollback plan and the package rows are data held by rwb-decision; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces or reports: the report carries staff user IDs and no customer or case data, and the harness uses synthetic data.
- No read of another service's schema: every read goes through the owner's contract, the SchemaBoundaryCheck fails the run on a cross-schema reference, and only rwb-source-data reads the ACE views.
- No production data and no outside system: the harness calls only the owning services and their fakes, never a production endpoint.
- The approver is never the author; FourEyesCheck fails the run when they are equal or when a refused approval writes an approver.
- No second rule engine and no recomputation: the counts and the effect of a version are read through the rwb-decision contract, and no caller reads the workbook, the generated DRL or a rule row directly.
- A refused call writes nothing: the harness asserts every row before and after each refusal and fails the run on any change.
- One hop only: the harness fails a run when the trace shows a call chain deeper than one owner.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Rule change by validated package version with a checklist and rollback | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | TC-E2-041-01-ITG to TC-E2-041-04-ITG, TC-E2-041-11-ITG, TC-E2-041-12-ITG, TC-E2-041-13-ITG |
| REQ-DRI-011 | Versioned tables with author and approver, and a count of decisions per version | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | CTL-08 | TC-E2-041-01-ITG, TC-E2-041-05-ITG to TC-E2-041-10-ITG, TC-E2-041-14-ITG, TC-E2-041-15-ITG |

The requirement IDs and their BRD sections are those of the legacy story; this story adds no requirement ID of its own.

### 19. Out of scope

- The three owning I stories RWB-P7-E2041-APP, RWB-P3-E2041-APP and RWB-P4-E2041-APP, and every screen, endpoint, table, rule and workflow they build.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-decision, rwb-case and rwb-access, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- The load, checks, scenarios, approval and rollback mechanics of a rule package version as built (RWB-E1-073) and the rule package rows themselves.
- The reference table checklist fields and their report (RWB-E1-043); this journey covers rule package versions only.
- The rules and parameters screen (SCR-39, Epic 8); the harness asserts the answer it consumes only.
- The QA sample against the rule package version applied (FEAT-ADM-08, Epic 8).
- The decision log store, its read operation and its chain check (RWB-E1-008, RWB-E1-027, JOB-14).
